"""Mirror a saved run bundle to Langfuse (T54 checkpoint 2). The bundle stays the original.

Off by default. `LI_LANGFUSE=on` enables it; only then are LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY
and LANGFUSE_BASE_URL read, and they never enter a record. The mirror reads finished trials from
the bundle and posts copies; it never calls a model and nothing at runtime reads from Langfuse.

Transport (author's ruling, 3 November 2026): our own OTLP HTTP/JSON export to Langfuse v4's
`/api/public/otel/v1/traces`, plus the REST datasets and scores APIs, through `requests`. Every
timestamp and ID comes from the bundle. Langfuse can duplicate a span sent twice, so each trial's
trace is sent once: a `sending` status is saved before the POST, then `sent`, `failed` (the server
answered with an error, so nothing was accepted and a later attempt is safe) or `unresolved` (no
answer: it may have been accepted, so it is never re-sent unless the operator says so). Dataset
items upsert by ID and scores carry idempotent IDs, so those may be re-sent.

Everything outbound passes `mask()` first, recorded as MASK_VERSION.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Protocol

from evals.comparison import assessment, fixtures, records, review
from evals.comparison.records import RunBundle

SWITCH = "LI_LANGFUSE"
DEFAULT_BASE_URL = "https://cloud.langfuse.com"
MASK_VERSION = "mask-1: secrets and key-shaped strings removed; provider continuation data dropped"
OTLP_PATH = "/api/public/otel/v1/traces"
DATASETS_PATH = "/api/public/v2/datasets"
DATASET_ITEMS_PATH = "/api/public/dataset-items"
SCORES_PATH = "/api/public/scores"
DROPPED_KEYS = ("continuation",)
CLOSED = ("trial_finished", "trial_interrupted")


class MirrorDisabled(RuntimeError):
    pass


@dataclass(frozen=True)
class MirrorSettings:
    base_url: str
    public_key: str
    secret_key: str

    @classmethod
    def from_env(cls, env: Mapping[str, str] = os.environ) -> MirrorSettings:
        switch = env.get(SWITCH, "off").strip().lower()
        if switch not in ("on", "off", ""):
            raise ValueError(f"{SWITCH} is 'on' or 'off', not {switch!r}")
        if switch != "on":
            raise MirrorDisabled(f"Langfuse mirroring is off; set {SWITCH}=on to enable it")
        missing = [k for k in ("LANGFUSE_PUBLIC_KEY", "LANGFUSE_SECRET_KEY") if not env.get(k)]
        if missing:
            raise ValueError(f"{SWITCH}=on needs {', '.join(missing)} in .env")
        return cls(env.get("LANGFUSE_BASE_URL") or DEFAULT_BASE_URL,
                   env["LANGFUSE_PUBLIC_KEY"], env["LANGFUSE_SECRET_KEY"])


class Destination(Protocol):
    def post(self, path: str, payload: dict, headers: dict[str, str] | None = None) -> tuple[int, Any]:
        """Return the HTTP status and parsed body, or raise OSError when no answer arrived."""
        ...


class LangfuseHttp:
    """The real destination. Keys live only in this object, never in records."""

    def __init__(self, settings: MirrorSettings, timeout_s: float = 30.0):
        import requests  # imported only when mirroring is enabled

        self._requests = requests
        self._base = settings.base_url.rstrip("/")
        token = base64.b64encode(f"{settings.public_key}:{settings.secret_key}".encode()).decode()
        self._auth = {"Authorization": f"Basic {token}"}
        self._timeout = timeout_s

    def post(self, path: str, payload: dict, headers: dict[str, str] | None = None) -> tuple[int, Any]:
        try:
            response = self._requests.post(self._base + path, json=payload, timeout=self._timeout,
                                           headers={**self._auth, **(headers or {})})
        except self._requests.RequestException as error:
            raise OSError(type(error).__name__) from None
        try:
            body = response.json()
        except ValueError:
            body = response.text[:500]
        return response.status_code, body


def mask(value: Any) -> Any:
    """The outbound filter: secrets removed, provider continuation blobs dropped."""
    if isinstance(value, dict):
        return {k: mask(v) for k, v in value.items() if k not in DROPPED_KEYS}
    if isinstance(value, list):
        return [mask(v) for v in value]
    return records.redact(value)


def _hex(text: str, length: int) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:length]


def trace_id(bundle: RunBundle, trial_id: str) -> str:
    return _hex(f"{bundle.manifest['run_id']}|{bundle.manifest['experiment_id']}|{trial_id}", 32)


def _span_id(bundle: RunBundle, key: str) -> str:
    return _hex(f"{bundle.manifest['run_id']}|span|{key}", 16)


def _nanos(seconds: float) -> str:
    return str(round(seconds * 1_000_000_000))


def _attr(key: str, value: Any) -> dict:
    if isinstance(value, bool):
        return {"key": key, "value": {"boolValue": value}}
    if isinstance(value, int):
        return {"key": key, "value": {"intValue": str(value)}}
    if isinstance(value, float):
        return {"key": key, "value": {"doubleValue": value}}
    if not isinstance(value, str):
        value = json.dumps(value, ensure_ascii=False)
    return {"key": key, "value": {"stringValue": value}}


def _span(*, trace: str, span: str, parent: str | None, name: str, start: float, end: float,
          attributes: dict[str, Any], error: str | None = None) -> dict:
    body = {"traceId": trace, "spanId": span, "name": name, "kind": 1,
            "startTimeUnixNano": _nanos(start), "endTimeUnixNano": _nanos(max(end, start)),
            "attributes": [_attr(k, v) for k, v in attributes.items() if v is not None],
            "status": {"code": 2, "message": error} if error else {"code": 1}}
    if parent:
        body["parentSpanId"] = parent
    return body


def dataset_name(bundle: RunBundle) -> str:
    return f"t54-{bundle.manifest['stage']}-cases-{bundle.manifest['fixture_version']}"


def dataset_item_id(bundle: RunBundle, case_id: str) -> str:
    return f"t54-{bundle.manifest['fixture_version']}-{case_id}"


def build_trace(bundle: RunBundle, trial_id: str, dataset_id: str | None) -> dict:
    """The OTLP/JSON export for one finished trial, built only from saved records."""
    events = bundle.events()
    started = next(e for e in events if e["type"] == "trial_started" and e["trial_id"] == trial_id)
    # An interrupted trial is mirrored too: its requests and unresolved attempts stay visible.
    finished = next(e for e in events if e["type"] in CLOSED and e["trial_id"] == trial_id)
    finished = {"status": "interrupted", **finished}
    config = next(c for c in bundle.manifest["configs"] if c["config_id"] == started["config_id"])
    trace, root = trace_id(bundle, trial_id), _span_id(bundle, trial_id)
    scored = started["case_id"] in fixtures.CASE_IDS
    common: dict[str, Any] = {"langfuse.environment": "experiment",
                              "langfuse.trace.name": f"t54-{started['stage']}",
                              "langfuse.trace.tags": [started["stage"], started["case_id"]]}
    if scored and dataset_id:
        common.update({
            "langfuse.experiment.id": _hex(f"{bundle.manifest['run_id']}|experiment", 32),
            "langfuse.experiment.name": f"{bundle.manifest['experiment_id']}/{bundle.manifest['run_id']}",
            "langfuse.experiment.dataset.id": dataset_id,
            "langfuse.experiment.item.id": dataset_item_id(bundle, started["case_id"]),
            "langfuse.experiment.item.root_observation_id": root})
    answer_ref = finished.get("final_answer") or finished.get("partial_answer")
    answer = bundle.read_artifact(answer_ref) if answer_ref else None
    metadata = {"trial_id": trial_id, "pass": started["pass_number"], "case_id": started["case_id"],
                "config_id": config["config_id"], "model": config["model"],
                "provider": config["provider"], "design": started["design"],
                "status": finished["status"], "answer_kind": (
                    "final" if finished.get("final_answer") else "partial" if answer else "none"),
                "fixture_version": bundle.manifest["fixture_version"],
                "prompt_version": bundle.manifest["prompt_version"],
                "rubric_version": bundle.manifest["rubric_version"],
                "code_revision": bundle.manifest["code"]["revision"], "mask_version": MASK_VERSION,
                "evidence_mode": started["evidence_mode"]}
    spans = [_span(trace=trace, span=root, parent=None, name=f"trial {started['case_id']}",
                   start=started["at"], end=finished["at"], attributes={
                       **common, "langfuse.observation.type": "agent",
                       "langfuse.observation.input": bundle.read_artifact(started["input"]),
                       "langfuse.observation.output": answer,
                       **{f"langfuse.observation.metadata.{k}": v for k, v in metadata.items()}},
                   error=None if finished["status"] == "completed" else finished["status"])]
    requests_done = {e["request_id"]: e for e in events if e["type"] == "request_finished"}
    unresolved = {e["request_id"] for e in events if e["type"] == "request_unresolved"}
    for begun in [e for e in events if e["type"] == "request_started" and e["trial_id"] == trial_id]:
        done = requests_done.get(begun["request_id"])
        output = bundle.read_artifact(done["output"]) if done and done.get("output") else None
        usage = (done or {}).get("usage")
        cost = (done or {}).get("cost_usd")
        status = done["status"] if done else ("unresolved" if begun["request_id"] in unresolved
                                              else "unfinished")
        spans.append(_span(
            trace=trace, span=_span_id(bundle, begun["request_id"]), parent=root,
            name=f"{begun['role']} attempt {begun['attempt']}", start=begun["at"],
            end=(done or begun)["at"], error=None if status == "completed" else (
                (done or {}).get("error") or status),
            attributes={**common, "langfuse.observation.type": "generation",
                        "langfuse.observation.model.name": config["model"],
                        "langfuse.observation.input": bundle.read_artifact(begun["input"]),
                        "langfuse.observation.output": output,
                        "langfuse.observation.usage_details": usage,
                        "langfuse.observation.cost_details": (
                            {"total": cost} if cost is not None else None),
                        "langfuse.observation.metadata.request_id": begun["request_id"],
                        "langfuse.observation.metadata.status": status,
                        "langfuse.observation.metadata.retry_of": begun.get("retry_of"),
                        "langfuse.observation.metadata.retry_reason": begun.get("retry_reason"),
                        "langfuse.observation.metadata.cost_known": cost is not None,
                        "langfuse.observation.metadata.model_reported": (done or {}).get(
                            "model_reported")}))
    for call in [e for e in events if e["type"] == "tool_call" and e["trial_id"] == trial_id]:
        parent = _span_id(bundle, call["request_id"]) if call.get("request_id") else root
        spans.append(_span(
            trace=trace, span=_span_id(bundle, f"tool|{call['seq']}"), parent=parent,
            name=f"tool {call['name']}", start=call["at"] - (call.get("elapsed_s") or 0),
            end=call["at"], error=None if call["executed"] else "tool error",
            attributes={**common, "langfuse.observation.type": "tool",
                        "langfuse.observation.input": call.get("arguments"),
                        "langfuse.observation.output": call.get("result")}))
    payload = {"resourceSpans": [{
        "resource": {"attributes": [_attr("service.name", "li-comparison-runner"),
                                    _attr("langfuse.environment", "experiment")]},
        "scopeSpans": [{"scope": {"name": "evals.comparison.mirror", "version": "1"},
                        "spans": spans}]}]}
    return mask(payload)


def build_scores(bundle: RunBundle) -> list[dict]:
    """Latest labels per assessor type, with assistant scores identified separately.

    History stays local. Saved event times make retry payloads stable across upload dates.
    """
    trials = review.identity_map(bundle)
    latest: dict[tuple[str, str], dict] = {}
    for event in bundle.events():
        if event["type"] in ("label", "critical_flag") and event.get("assessor_type") in (
                "human", "assistant"):
            name = (f"criterion.{event['criterion']}" if event["type"] == "label"
                    else f"critical.{event['error_id']}")
            if event["assessor_type"] == "assistant":
                name = f"assistant.{name}"
            latest[(event["review_id"], name)] = event
        elif event["type"] == "deterministic_check":
            latest[(event["trial_id"], "check.unresolved_references")] = event
    scores = []
    for (key, name), event in sorted(latest.items(), key=lambda kv: kv[1]["seq"]):
        trial = trials.get(key, key)
        trace = trace_id(bundle, trial)
        score: dict[str, Any] = {"id": _hex(f"{trace}|{name}", 32), "traceId": trace,
                                 "name": name, "environment": "experiment",
                                 "timestamp": datetime.fromtimestamp(
                                     event["at"], timezone.utc).isoformat()}
        if event["type"] == "label":
            score.update(dataType="CATEGORICAL", value=str(event["score"]),
                         comment=f"{event['reason']} (rubric {event['rubric_version']}, "
                                 f"{event['phase']})")
        elif event["type"] == "critical_flag":
            score.update(dataType="BOOLEAN", value=1 if event["present"] else 0,
                         comment=event["reason"])
        else:
            score.update(dataType="NUMERIC", value=len(event["unresolved"]),
                         comment="bracketed references not found in the case file; resolution "
                                 "does not establish support; "
                                 f"{len(event.get('unsupported_citations', []))} unsupported "
                                 "citation group(s) retained in local checks")
        if event["type"] in ("label", "critical_flag"):
            score["comment"] = (f"{event['assessor_type']} assessment by {event['assessor']}: "
                                f"{score['comment']}")
        scores.append(mask(score))
    return scores


def _status(bundle: RunBundle) -> dict[tuple[str, str], str]:
    state: dict[tuple[str, str], str] = {}
    for event in bundle.events():
        if event["type"] == "mirror_status":
            state[(event["target"], event["key"])] = event["status"]
    return state


def _remote_id(bundle: RunBundle, target: str, key: str) -> str | None:
    for event in reversed(bundle.events()):
        if event["type"] == "mirror_status" and event["target"] == target and event["key"] == key \
                and event["status"] == "sent":
            return event.get("remote_id")
    return None


def _send(bundle: RunBundle, destination: Destination, *, target: str, key: str, path: str,
          payload: dict, headers: dict[str, str] | None = None) -> tuple[str, Any]:
    bundle.append("mirror_status", target=target, key=key, status="sending", path=path,
                  mask_version=MASK_VERSION)
    try:
        code, body = destination.post(path, payload, headers)
    except OSError as error:
        bundle.append("mirror_status", target=target, key=key, status="unresolved",
                      error=f"no answer ({error}); the server may have accepted it")
        return "unresolved", None
    if 200 <= code < 300:
        remote = body.get("id") if isinstance(body, dict) else None
        bundle.append("mirror_status", target=target, key=key, status="sent", http_status=code,
                      remote_id=remote)
        return "sent", body
    bundle.append("mirror_status", target=target, key=key, status="failed", http_status=code,
                  error=records.redact(str(body))[:500])
    return "failed", body


def mirror(bundle: RunBundle, destination: Destination, *, resend_unresolved: bool = False) -> dict:
    """Send what the bundle holds and Langfuse lacks. Local evidence is never changed except by
    appended status events. Returns counts by outcome; failures are listed, never hidden."""
    state = _status(bundle)
    summary: dict[str, list[str]] = {"sent": [], "failed": [], "unresolved": [], "skipped": []}

    def note(outcome: str, key: str) -> None:
        summary[outcome].append(key)

    dataset_id = _remote_id(bundle, "dataset", dataset_name(bundle))
    scored_cases = sorted({e["case_id"] for e in bundle.events() if e["type"] == "trial_started"
                           and e["case_id"] in fixtures.CASE_IDS})
    if scored_cases and dataset_id is None:
        outcome, body = _send(bundle, destination, target="dataset", key=dataset_name(bundle),
                              path=DATASETS_PATH, payload=mask({
                                  "name": dataset_name(bundle),
                                  "description": "T54 fixed-evidence screening cases",
                                  "metadata": {"fixture_version": bundle.manifest["fixture_version"]}}))
        note(outcome, f"dataset {dataset_name(bundle)}")
        if outcome == "sent" and isinstance(body, dict):
            dataset_id = body.get("id")
    if scored_cases:
        for case_id in scored_cases:
            if state.get(("dataset_item", case_id)) == "sent":
                continue
            case = fixtures.load_case(case_id)
            gold = assessment.load_gold(case_id)
            outcome, _ = _send(bundle, destination, target="dataset_item", key=case_id,
                               path=DATASET_ITEMS_PATH, payload=mask({
                                   "id": dataset_item_id(bundle, case_id),
                                   "datasetName": dataset_name(bundle),
                                   "input": {"question": case["question"],
                                             "case_file": fixtures.render_case(case)},
                                   "expectedOutput": {
                                       "required_findings": gold["required_findings"],
                                       "critical_errors": [c["id"] for c in gold["critical_errors"]]},
                                   "metadata": {"case_id": case_id}}))
            note(outcome, f"dataset item {case_id}")

    scored_trials = {e["trial_id"] for e in bundle.events() if e["type"] == "trial_started"
                     and e["case_id"] in fixtures.CASE_IDS}
    for event in [e for e in bundle.events() if e["type"] in CLOSED]:
        key = event["trial_id"]
        previous = state.get(("trace", key))
        if previous == "sent" or (previous in ("sending", "unresolved") and not resend_unresolved):
            note("skipped", key)
            continue
        if key in scored_trials and dataset_id is None:
            # Experiment links need the dataset; a trace is sent once, so it waits for it.
            note("skipped", key)
            continue
        outcome, _ = _send(bundle, destination, target="trace", key=key, path=OTLP_PATH,
                           payload=build_trace(bundle, key, dataset_id),
                           headers={"x-langfuse-ingestion-version": "4"})
        note(outcome, key)

    for score in build_scores(bundle):
        key = f"{score['id']}:{_hex(json.dumps(score, sort_keys=True), 12)}"
        if state.get(("score", key)) == "sent":
            continue
        outcome, _ = _send(bundle, destination, target="score", key=key, path=SCORES_PATH,
                           payload=score)
        note(outcome, f"score {score['name']}")
    return {k: len(v) for k, v in summary.items()} | {"failures": summary["failed"] + summary["unresolved"]}
