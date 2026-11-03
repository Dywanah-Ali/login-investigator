"""Execute a frozen comparison plan and write its run bundle (T54 checkpoint 1).

Three stages share one record contract:

    compatibility            one tool round-trip session per configuration, outside scoring
    screening                configurations x cases x passes, design A, fixed evidence
    architecture_calibration one configuration x cases x designs A/B/C, fixed evidence

Approved execution policy (T52): one trial at a time in a frozen, rotated order; 180 s per request
and 600 s per trial, wall clock, with retries and backoff inside the trial's clock; no token, call
or retry count caps; every attempt recorded before dispatch. Transient errors and request timeouts
are retried while trial time remains; permanent errors are not. A rerun is only ever an explicit,
versioned, linked trial. Gold files are never read here.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import time
import uuid
from collections.abc import Callable
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path

from evals.comparison import fixtures, records, roles
from evals.comparison.adapters import (
    Adapter,
    AdapterError,
    ModelConfig,
    ModelRequest,
    ModelResponse,
)

STAGES = ("compatibility", "screening", "architecture_calibration")
DESIGNS = ("A", "B", "C")
REQUEST_TIMEOUT_S = 180.0
TRIAL_TIMEOUT_S = 600.0
BACKOFF_S = (1.0, 2.0, 4.0, 8.0, 16.0, 30.0)  # then 30 s each time; no count cap
RETRY_POLICY = {
    "retried": ["transient", "timeout"], "not_retried": ["permanent"],
    "backoff_s": list(BACKOFF_S), "backoff_after_last": BACKOFF_S[-1], "count_cap": None,
    "deadline": "a retry is sent only if its backoff ends before the trial deadline",
    "adapter_retries": "disabled; every retry is the runner's and is recorded",
}
SETTINGS = {
    "request_timeout_s": REQUEST_TIMEOUT_S, "trial_timeout_s": TRIAL_TIMEOUT_S,
    "timeouts": "wall clock from dispatch and from trial start; retries never reset them",
    "concurrency": 1, "token_caps": None, "call_caps": None, "retry_policy": RETRY_POLICY,
    "cost_tracking": "actual charges; unknown stays unknown; no reservations",
    "planning_budget_usd": 25.0, "review_points": ["US$15 spent", "after the first 24 results"],
    "evidence_mode": "fixed_evidence (screening and calibration); tool round trip only in "
                     "compatibility sessions",
}
COMPARISON_DIR = Path(__file__).parent
# What a run depends on beyond this package: the core it imports, the source data and the locks.
RELEVANT_PATHS = ("evals/comparison", "login_investigator", "data/datasets/default",
                  "pyproject.toml", "uv.lock")


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def code_version() -> dict:
    """The git revision, any uncommitted change to what a run depends on (paths and a diff hash),
    and a hash of this package's source, which also covers its untracked files."""
    sources = sorted(p for p in COMPARISON_DIR.rglob("*.py"))
    digest = hashlib.sha256()
    for path in sources:
        digest.update(path.relative_to(COMPARISON_DIR).as_posix().encode())
        digest.update(path.read_bytes())

    def git(*args: str) -> str:
        try:
            return subprocess.run(["git", *args], cwd=COMPARISON_DIR, capture_output=True,
                                  text=True, check=True).stdout.strip()
        except (OSError, subprocess.CalledProcessError):
            return "unknown"

    backend = COMPARISON_DIR.parents[1]
    relevant = [str(backend / p) for p in RELEVANT_PATHS]
    status = git("status", "--porcelain", "--", *relevant)
    diff = git("diff", "HEAD", "--", *relevant)
    return {"revision": git("rev-parse", "--short", "HEAD"),
            "dirty": bool(status), "dirty_paths": status.splitlines(),
            "dirty_diff_sha256": _sha(diff) if diff else None,
            "comparison_source_sha256": digest.hexdigest()}


def build_schedule(stage: str, configs: list[ModelConfig], case_ids: list[str], passes: int,
                   designs: list[str]) -> list[dict]:
    """Pass-major order, so the first pass is the first block (the first-24 checkpoint). Within
    each case the arms (configuration, design) rotate by one place per case and pass, so no arm
    always goes first."""
    if stage == "compatibility":
        return [{"slot": i, "trial_id": f"compat-{c.config_id}", "stage": stage, "pass": 1,
                 "case_id": "compatibility", "config_id": c.config_id, "design": "compat"}
                for i, c in enumerate(configs, start=1)]
    arms = [(c.config_id, d) for c in configs for d in designs]
    schedule, block = [], 0
    for number in range(1, passes + 1):
        for case_id in case_ids:
            shift = block % len(arms)
            for config_id, design in arms[shift:] + arms[:shift]:
                schedule.append({"slot": len(schedule) + 1,
                                 "trial_id": f"p{number}-{case_id}-{config_id}-{design}",
                                 "stage": stage, "pass": number, "case_id": case_id,
                                 "config_id": config_id, "design": design})
            block += 1
    return schedule


def new_run(root: Path, *, stage: str, configs: list[ModelConfig], case_ids: list[str],
            passes: int, designs: list[str], adapter: Adapter, experiment_id: str,
            clock: Callable[[], float] = time.time) -> records.RunBundle:
    if stage not in STAGES:
        raise ValueError(f"unknown stage {stage!r}")
    if stage == "screening" and designs != ["A"]:
        raise ValueError("screening uses the single-investigator design A only")
    if stage == "architecture_calibration" and len(configs) != 1:
        raise ValueError("architecture calibration holds one provisional configuration")
    fixture_manifest = json.loads((fixtures.FROZEN / "manifest.json").read_text())
    gold_hashes = {k: v for k, v in fixture_manifest["files"].items() if k.startswith("gold/")}
    manifest = {
        "experiment_id": experiment_id, "run_id": root.name, "stage": stage,
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "code": code_version(),
        "fixture_version": fixture_manifest["fixture_version"],
        "case_files": {k: v for k, v in fixture_manifest["files"].items()
                       if k.startswith("cases/")},
        "prompt_version": roles.prompt_version(),
        "tool_version": _sha(json.dumps(roles.COMPATIBILITY_TOOL, sort_keys=True))[:12],
        "rubric_version": _sha(json.dumps(gold_hashes, sort_keys=True))[:12],
        "settings": SETTINGS,
        "adapter": {"name": adapter.name, "version": adapter.version},
        "configs": [c.to_dict() for c in configs],
        "designs": designs, "case_ids": case_ids, "passes": passes,
        "schedule": build_schedule(stage, configs, case_ids, passes, designs),
    }
    return records.RunBundle.create(root, manifest, clock)


def schedule_rerun(bundle: records.RunBundle, original_trial_id: str, *, reason: str,
                   repair_version: str) -> str:
    """Add an explicit rerun linked to its original. The original stays in the record."""
    slots = {s["trial_id"]: s for s in _all_slots(bundle)}
    if original_trial_id not in slots:
        raise KeyError(f"no trial {original_trial_id!r} in this run")
    count = sum(1 for t in slots if t.startswith(f"{original_trial_id}-r"))
    new_id = f"{original_trial_id}-r{count + 1}"
    slot = {**slots[original_trial_id], "trial_id": new_id, "rerun_of": original_trial_id,
            "repair_version": repair_version, "slot": len(slots) + 1}
    bundle.append("rerun_scheduled", original_trial_id=original_trial_id, trial_id=new_id,
                  reason=reason, repair_version=repair_version, slot=slot)
    return new_id


def _all_slots(bundle: records.RunBundle) -> list[dict]:
    return bundle.manifest["schedule"] + [e["slot"] for e in bundle.events()
                                          if e["type"] == "rerun_scheduled"]


class _TrialTimeout(Exception):
    pass


class _TrialFailed(Exception):
    def __init__(self, status: str, partial_text: str = ""):
        super().__init__(status)
        self.status = status
        self.partial_text = partial_text


class Runner:
    def __init__(self, bundle: records.RunBundle, adapter: Adapter, *,
                 clock: Callable[[], float] = time.monotonic,
                 sleep: Callable[[float], None] = time.sleep,
                 case_root: Path = fixtures.FROZEN):
        self.bundle = bundle
        self.adapter = adapter
        self.clock = clock
        self.sleep = sleep
        self.case_root = case_root
        self.configs = {c["config_id"]: ModelConfig(**c) for c in bundle.manifest["configs"]}

    def run(self, until_slot: int | None = None, *, stop_cost_usd: float | None = None,
            prior_cost_usd: float = 0.0, reruns_only: bool = False) -> dict:
        """Run every slot not yet started, in order, up to `until_slot`. Anything a crash left
        open is closed first and never re-sent."""
        recovery = records.recover(self.bundle)
        started = {e["trial_id"] for e in self.bundle.events() if e["type"] == "trial_started"}
        ran = []
        stop_reason = None
        for slot in sorted(_all_slots(self.bundle), key=lambda s: s["slot"]):
            if reruns_only and not slot.get("rerun_of"):
                continue
            if until_slot is not None and slot["slot"] > until_slot:
                break
            if slot["trial_id"] in started:
                continue
            if (stop_cost_usd is not None
                    and prior_cost_usd + records.resources(self.bundle)["total"]["known_cost_usd"]
                    >= stop_cost_usd):
                stop_reason = "spending review due before the next trial"
                break
            self._trial(slot)
            ran.append(slot["trial_id"])
        return {"recovery": recovery, "ran": ran, "stop_reason": stop_reason}

    # --- one trial ---------------------------------------------------------------------------

    def _trial(self, slot: dict) -> None:
        config = self.configs[slot["config_id"]]
        start = self.clock()
        self._deadline = start + TRIAL_TIMEOUT_S
        self._trial_id = slot["trial_id"]
        self._last_request: str | None = None
        self._partial = ""
        if slot["design"] == "compat":
            case_text = roles.COMPATIBILITY_QUESTION
        else:
            case_text = fixtures.render_case(fixtures.load_case(slot["case_id"], self.case_root))
        input_ref = self.bundle.write_artifact(f"inputs/{slot['trial_id']}.txt", case_text)
        self.bundle.append("trial_started", trial_id=slot["trial_id"], slot=slot["slot"],
                           stage=slot["stage"], case_id=slot["case_id"], pass_number=slot["pass"],
                           config_id=slot["config_id"], design=slot["design"],
                           memory_id=str(uuid.uuid4()), evidence_mode=(
                               "tool_round_trip" if slot["design"] == "compat" else "fixed_evidence"),
                           input=input_ref, rerun_of=slot.get("rerun_of"),
                           repair_version=slot.get("repair_version"))
        answer, status, partial = "", "completed", ""
        try:
            if slot["design"] == "compat":
                answer = self._compatibility(config)
            else:
                design = {"A": self._design_A, "B": self._design_B, "C": self._design_C}
                answer = design[slot["design"]](config, case_text)
            if not answer.strip():
                status = "no_answer"
        except _TrialTimeout:
            status, partial = "timeout", self._partial
        except _TrialFailed as failure:
            status, partial = failure.status, failure.partial_text
        self.bundle.append(
            "trial_finished", trial_id=slot["trial_id"], status=status,
            final_answer=(self.bundle.write_artifact(f"answers/{slot['trial_id']}.txt", answer)
                          if answer.strip() and status == "completed" else None),
            partial_answer=(self.bundle.write_artifact(f"partial/{slot['trial_id']}.txt", partial)
                            if partial.strip() else None),
            elapsed_s=round(self.clock() - start, 3))

    def _design_A(self, config: ModelConfig, case_text: str) -> str:
        return self._ask(config, "investigator", [_system(roles.INVESTIGATOR), _user(case_text)]).text

    def _design_B(self, config: ModelConfig, case_text: str) -> str:
        findings = self._ask(config, "applicability_specialist",
                             [_system(roles.APPLICABILITY), _user(case_text)]).text
        self._role_output("applicability_specialist", findings)
        handoff = roles.SPECIALIST_HANDOFF.format(findings=findings)
        return self._ask(config, "investigator",
                         [_system(roles.INVESTIGATOR), _user(case_text + "\n\n" + handoff)]).text

    def _design_C(self, config: ModelConfig, case_text: str) -> str:
        first = [_system(roles.INVESTIGATOR), _user(case_text)]
        draft = self._ask(config, "investigator_draft", first)
        self._role_output("investigator_draft", draft.text)
        review = self._ask(config, "reviewer", [
            _system(roles.REVIEWER),
            _user(roles.REVIEW_REQUEST.format(case=case_text, draft=draft.text))]).text
        self._role_output("reviewer", review)
        return self._ask(config, "investigator", [
            *first, _assistant(draft.text, draft.continuation),
            _user(roles.REVIEW_HANDOFF.format(review=review))]).text

    def _compatibility(self, config: ModelConfig) -> str:
        messages = [_system(roles.COMPATIBILITY), _user(roles.COMPATIBILITY_QUESTION)]
        tool_round_trip, response = False, None
        identity, settings = [], []
        while True:
            response = self._ask(config, "compatibility", messages, tools=[roles.COMPATIBILITY_TOOL])
            identity.append({"model_reported": response.model_reported,
                             "provider_reported": response.provider_reported})
            settings.append(response.settings_reported)
            if not response.tool_calls:
                break
            messages.append(_assistant(response.text, response.continuation, response.tool_calls))
            for call in response.tool_calls:
                result = self._tool(call)
                tool_round_trip = tool_round_trip or "error" not in result
                messages.append({"role": "tool", "tool_call_id": call["id"],
                                 "content": json.dumps(result)})
        answer = response.text
        self.bundle.append(
            "compatibility_checks", trial_id=self._trial_id, config_id=config.config_id,
            tool_round_trip=tool_round_trip,
            output_contract=("[CMP-1]" in answer and roles.COMPATIBILITY_EXPECTED in answer),
            requested={"model": config.model, "provider": config.provider,
                       "reasoning": config.reasoning, "sampling": config.sampling,
                       "service_tier": config.service_tier},
            reported_identity=identity, reported_settings=settings,
            settings_note="reported settings are returned gateway fields; echoed or accepted "
                          "values do not prove native application; missing values are unverified")
        return answer

    def _tool(self, call: dict) -> dict:
        begun = self.clock()
        name, arguments = call.get("name"), call.get("arguments")
        try:
            args = json.loads(arguments) if isinstance(arguments, str) else dict(arguments or {})
            if name != "get_record":
                raise ValueError(f"unknown tool {name!r}")
            ref = str(args.get("ref", ""))
            if ref not in roles.COMPATIBILITY_RECORDS:
                raise ValueError(f"no record {ref!r}")
            result = {"ref": ref, "text": roles.COMPATIBILITY_RECORDS[ref]}
        except (ValueError, TypeError) as error:
            result = {"error": str(error)}
        self.bundle.append("tool_call", trial_id=self._trial_id, request_id=self._last_request,
                           call_id=call.get("id"), name=name, arguments=arguments,
                           executed="error" not in result, result=result,
                           elapsed_s=round(self.clock() - begun, 3))
        return result

    def _role_output(self, role: str, text: str) -> None:
        ref = self.bundle.write_artifact(f"roles/{self._trial_id}-{role}.txt", text)
        self.bundle.append("role_output", trial_id=self._trial_id, role=role,
                           request_id=self._last_request, output=ref)

    # --- one request, with recorded retries ----------------------------------------------------

    def _ask(self, config: ModelConfig, role: str, messages: list[dict],
             tools: list[dict] | None = None) -> ModelResponse:
        retry_of, reason, attempt = None, None, 0
        input_text = json.dumps({"messages": messages, "tools": tools}, ensure_ascii=False)
        input_ref = self.bundle.write_artifact(
            f"requests/{self._trial_id}-{role}-{uuid.uuid4().hex[:8]}.json", input_text)
        while True:
            attempt += 1
            remaining = self._deadline - self.clock()
            if remaining <= 0:
                raise _TrialTimeout()
            timeout = min(REQUEST_TIMEOUT_S, remaining)
            request = ModelRequest(config, messages, timeout, tools)
            details = self.adapter.request_details(request)
            request_id = f"{self._trial_id}-{uuid.uuid4().hex[:12]}"
            self.bundle.append("request_started", request_id=request_id, trial_id=self._trial_id,
                               role=role, attempt=attempt, parent_request_id=self._last_request,
                               retry_of=retry_of, retry_reason=reason,
                               retry_origin="runner" if retry_of else None,
                               timeout_s=round(timeout, 3), input=input_ref,
                               wire_input=(self.bundle.write_artifact(
                                   f"wire/{request_id}.json", json.dumps(details)) if details else None))
            sent = self.clock()
            # Wire preparation and fsyncs consume the same case deadline. Recompute after
            # persistence so an allowance calculated before that work cannot escape it.
            dispatch_timeout = min(REQUEST_TIMEOUT_S, self._deadline - sent)
            if dispatch_timeout <= 0:
                self._finish(request_id, sent, status="timeout",
                             error="case deadline elapsed before dispatch")
                raise _TrialTimeout()
            request = replace(request, timeout_s=dispatch_timeout)
            try:
                response = self.adapter.complete(request)
            except AdapterError as error:
                self._finish(request_id, sent, status="timeout" if error.kind == "timeout" else "error",
                             error=f"{error.kind}: {error}", usage=error.usage,
                             cost_usd=error.cost_usd, generation_id=error.generation_id,
                             partial=error.partial_text, error_details=error.details,
                             dispatch_timeout_s=dispatch_timeout)
                if error.partial_text:
                    self._partial = error.partial_text
                if error.kind == "permanent":
                    raise _TrialFailed("error", error.partial_text) from None
                wait = BACKOFF_S[min(attempt - 1, len(BACKOFF_S) - 1)]
                if self.clock() + wait >= self._deadline:
                    raise _TrialTimeout() from None
                self.sleep(wait)
                retry_of, reason = request_id, f"{error.kind}: {error}"
                continue
            self._finish(request_id, sent, status="completed", response=response,
                         usage=response.usage, cost_usd=response.cost_usd,
                         generation_id=response.generation_id, dispatch_timeout_s=dispatch_timeout)
            self._last_request = request_id
            if self.clock() > self._deadline:
                self._partial = response.text  # arrived after the deadline: kept, not counted
                raise _TrialTimeout()
            return response

    def _finish(self, request_id: str, sent: float, *, status: str,
                response: ModelResponse | None = None, error: str | None = None,
                usage: dict | None = None, cost_usd: float | None = None,
                generation_id: str | None = None, partial: str = "",
                error_details: dict | None = None, dispatch_timeout_s: float | None = None) -> None:
        fields: dict = {"request_id": request_id, "status": status,
                        "elapsed_s": round(self.clock() - sent, 3), "usage": usage,
                        "cost_usd": cost_usd,
                        "cost_source": "response" if cost_usd is not None else None,
                        "generation_id": generation_id, "error": error,
                        "error_details": error_details, "dispatch_timeout_s": dispatch_timeout_s}
        if response is not None:
            fields.update(
                model_reported=response.model_reported, provider_reported=response.provider_reported,
                finish_reason=response.finish_reason, settings_reported=response.settings_reported,
                tool_calls=response.tool_calls,
                output=self.bundle.write_artifact(f"outputs/{request_id}.txt", response.text),
                continuation=(self.bundle.write_artifact(
                    f"continuations/{request_id}.json", json.dumps(response.continuation))
                    if response.continuation else None))
        if partial:
            fields["partial_output"] = self.bundle.write_artifact(f"outputs/{request_id}.partial.txt",
                                                                  partial)
        self.bundle.append("request_finished", **fields)


def _system(text: str) -> dict:
    return {"role": "system", "content": text}


def _user(text: str) -> dict:
    return {"role": "user", "content": text}


def _assistant(text: str, continuation: dict | None = None,
               tool_calls: list[dict] | None = None) -> dict:
    message: dict = {"role": "assistant", "content": text}
    if tool_calls:
        message["tool_calls"] = tool_calls
    if continuation:
        message["continuation"] = continuation
    return message
