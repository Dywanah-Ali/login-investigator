"""T54 seams 5 and 6: the Langfuse mirror against a fake destination, and label export.

Expected behaviour comes from T54's criteria and the author's transport ruling (3 November 2026):
off by default behind one switch; keys never in records; everything outbound masked; local
records saved first and never lost to an upload failure; each trial's trace sent once; no model
call and no read from Langfuse.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from evals.comparison import assessment, mirror, records, review, runner
from evals.comparison.adapters import FakeAdapter, FakeClock, ModelConfig, ModelResponse

SECRET = "sk-or-v1-abcdefghijklmnopqrstuvwxyz0123"
CONFIGS = [ModelConfig(config_id="m1", label="Alpha", model="vendor/alpha", provider="prov",
                       reasoning={"effort": "medium"})]


class FakeLangfuse:
    """Records every POST; `fail` maps a path to an HTTP status or to 'drop' (no answer)."""

    def __init__(self, fail: dict[str, object] | None = None):
        self.calls: list[tuple[str, dict, dict]] = []
        self.fail = fail or {}

    def post(self, path, payload, headers=None):
        self.calls.append((path, payload, headers or {}))
        outcome = self.fail.get(path)
        if outcome == "drop":
            raise OSError("ReadTimeout")
        if isinstance(outcome, int):
            return outcome, {"message": "rejected"}
        return 200, {"id": "remote-dataset-1"} if path == mirror.DATASETS_PATH else {}


@pytest.fixture(scope="module")
def base_run(tmp_path_factory):
    root = tmp_path_factory.mktemp("mirror") / "run"
    clock = FakeClock()
    script = (lambda r, n: ModelResponse(
        text=f"Assessment [L1]. Leaked {SECRET} here.", usage={"input": 7, "output": 3},
        cost_usd=None if n == 0 else 0.001, continuation={"encrypted": "opaque-blob"}))
    adapter = FakeAdapter(script, clock)
    bundle = runner.new_run(root, stage="screening", configs=CONFIGS, case_ids=["O1-06", "O1-09"],
                            passes=1, designs=["A"], adapter=adapter, experiment_id="exp",
                            clock=clock)
    runner.Runner(bundle, adapter, clock=clock, sleep=clock.advance).run()
    return root


@pytest.fixture
def bundle(base_run, tmp_path):
    shutil.copytree(base_run, tmp_path / "run")
    return records.RunBundle.open(tmp_path / "run")


def _traces(fake):
    return [p for path, p, _ in fake.calls if path == mirror.OTLP_PATH]


# --- the switch ------------------------------------------------------------------------------

def test_mirroring_is_off_by_default_and_reads_no_keys():
    with pytest.raises(mirror.MirrorDisabled):
        mirror.MirrorSettings.from_env({"LANGFUSE_SECRET_KEY": "x", "LANGFUSE_PUBLIC_KEY": "y"})
    with pytest.raises(mirror.MirrorDisabled):
        mirror.MirrorSettings.from_env({mirror.SWITCH: "off"})


def test_switching_on_needs_both_keys_and_defaults_the_cloud_address():
    with pytest.raises(ValueError):
        mirror.MirrorSettings.from_env({mirror.SWITCH: "on", "LANGFUSE_PUBLIC_KEY": "pk"})
    settings = mirror.MirrorSettings.from_env(
        {mirror.SWITCH: "on", "LANGFUSE_PUBLIC_KEY": "pk", "LANGFUSE_SECRET_KEY": "sk"})
    assert settings.base_url == mirror.DEFAULT_BASE_URL


def test_the_runner_never_touches_langfuse():
    source = (Path(runner.__file__)).read_text()
    assert "mirror" not in source and "langfuse" not in source.lower()


# --- what is sent ------------------------------------------------------------------------------

def test_every_outbound_record_is_masked(bundle, monkeypatch):
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-lf-very-secret-value")
    fake = FakeLangfuse()
    mirror.mirror(bundle, fake)
    sent = json.dumps([payload for _, payload, _ in fake.calls])
    assert SECRET not in sent and "sk-lf-very-secret-value" not in sent
    assert "opaque-blob" not in sent and records.REDACTED in sent


def test_a_trace_carries_the_records_own_times_ids_and_experiment_links(bundle):
    fake = FakeLangfuse()
    mirror.mirror(bundle, fake)
    trace = _traces(fake)[0]
    spans = trace["resourceSpans"][0]["scopeSpans"][0]["spans"]
    started = next(e for e in bundle.events() if e["type"] == "trial_started")
    root = spans[0]
    assert root["traceId"] == mirror.trace_id(bundle, started["trial_id"])
    assert root["startTimeUnixNano"] == str(round(started["at"] * 1e9))
    attributes = {a["key"]: a["value"] for a in root["attributes"]}
    assert attributes["langfuse.experiment.dataset.id"] == {"stringValue": "remote-dataset-1"}
    assert attributes["langfuse.experiment.item.root_observation_id"] == {
        "stringValue": root["spanId"]}
    generation = spans[1]
    assert generation["parentSpanId"] == root["spanId"]
    gen_attributes = {a["key"]: a["value"] for a in generation["attributes"]}
    assert gen_attributes["langfuse.observation.type"] == {"stringValue": "generation"}
    for span in spans:
        keys = {a["key"] for a in span["attributes"]}
        assert {"langfuse.experiment.id", "langfuse.experiment.item.id"} <= keys


def test_unknown_cost_is_sent_as_unknown_not_zero(bundle):
    fake = FakeLangfuse()
    mirror.mirror(bundle, fake)
    first_generation = _traces(fake)[0]["resourceSpans"][0]["scopeSpans"][0]["spans"][1]
    keys = {a["key"]: a["value"] for a in first_generation["attributes"]}
    assert "langfuse.observation.cost_details" not in keys
    assert keys["langfuse.observation.metadata.cost_known"] == {"boolValue": False}


def test_the_otlp_export_names_ingestion_version_4(bundle):
    fake = FakeLangfuse()
    mirror.mirror(bundle, fake)
    headers = [h for path, _, h in fake.calls if path == mirror.OTLP_PATH]
    assert headers and all(h == {"x-langfuse-ingestion-version": "4"} for h in headers)


def test_labels_go_out_as_idempotent_scores_with_n_a_distinct(bundle):
    batch = review.prepare_batch(bundle, size=2, seed=1)
    item = batch["items"][0]
    assessment.record_label(bundle, review_id=item["review_id"], case_id=item["case_id"],
                            criterion="facts", score=0, excerpt="", evidence_ref="L1",
                            reason="count wrong", assessor="author")
    fake = FakeLangfuse()
    mirror.mirror(bundle, fake)
    scores = [p for path, p, _ in fake.calls if path == mirror.SCORES_PATH]
    facts = next(s for s in scores if s["name"] == "criterion.facts")
    assert facts["value"] == "0" and facts["dataType"] == "CATEGORICAL"
    again = FakeLangfuse()
    mirror.mirror(bundle, again)
    assert not [c for c in again.calls if c[0] == mirror.SCORES_PATH]


# --- send once, local first ----------------------------------------------------------------------

def test_each_trace_is_sent_once(bundle):
    first = FakeLangfuse()
    assert mirror.mirror(bundle, first)["sent"] >= 2
    second = FakeLangfuse()
    result = mirror.mirror(bundle, second)
    assert _traces(second) == [] and result["skipped"] == 2
    assert not [c for c in second.calls if c[0] == mirror.DATASETS_PATH]


def test_a_rejected_upload_is_reported_kept_local_and_safe_to_retry(bundle):
    events_before = [e for e in bundle.events() if e["type"] != "mirror_status"]
    answers_before = sorted(p.read_text() for p in (bundle.root / "artifacts" / "answers").iterdir())
    result = mirror.mirror(bundle, FakeLangfuse({mirror.OTLP_PATH: 503}))
    assert len(result["failures"]) == 2
    assert [e for e in bundle.events() if e["type"] != "mirror_status"] == events_before
    assert sorted(p.read_text() for p in (bundle.root / "artifacts" / "answers").iterdir()) == \
        answers_before
    retry = FakeLangfuse()
    mirror.mirror(bundle, retry)
    assert len(_traces(retry)) == 2


def test_an_upload_without_an_answer_is_never_resent_silently(bundle):
    mirror.mirror(bundle, FakeLangfuse({mirror.OTLP_PATH: "drop"}))
    statuses = [e["status"] for e in bundle.events() if e["type"] == "mirror_status"
                and e["target"] == "trace"]
    assert statuses.count("unresolved") == 2
    quiet = FakeLangfuse()
    mirror.mirror(bundle, quiet)
    assert _traces(quiet) == []
    forced = FakeLangfuse()
    mirror.mirror(bundle, forced, resend_unresolved=True)
    assert len(_traces(forced)) == 2


def test_a_crash_while_sending_counts_as_unresolved(bundle):
    trial = next(e["trial_id"] for e in bundle.events() if e["type"] == "trial_finished")
    bundle.append("mirror_status", target="trace", key=trial, status="sending", path="x",
                  mask_version=mirror.MASK_VERSION)
    fake = FakeLangfuse()
    mirror.mirror(bundle, fake)
    assert len(_traces(fake)) == 1


def test_traces_wait_while_the_dataset_is_unavailable(bundle):
    fake = FakeLangfuse({mirror.DATASETS_PATH: 500})
    result = mirror.mirror(bundle, fake)
    assert _traces(fake) == [] and result["skipped"] == 2


def test_an_interrupted_trial_is_mirrored_with_its_unresolved_request(bundle):
    bundle.append("trial_started", trial_id="p9-x", slot=99, stage="screening", case_id="O1-06",
                  pass_number=9, config_id="m1", design="A", memory_id="m",
                  evidence_mode="fixed_evidence", input=bundle.write_artifact("inputs/p9.txt", "q"))
    bundle.append("request_started", request_id="r-open", trial_id="p9-x", role="investigator",
                  attempt=1, input=bundle.write_artifact("requests/r-open.json", "{}"))
    records.recover(bundle)
    fake = FakeLangfuse()
    mirror.mirror(bundle, fake)
    trace = next(t for t in _traces(fake) if t["resourceSpans"][0]["scopeSpans"][0]["spans"][0][
        "traceId"] == mirror.trace_id(bundle, "p9-x"))
    root, request = trace["resourceSpans"][0]["scopeSpans"][0]["spans"]
    assert root["status"] == {"code": 2, "message": "interrupted"}
    assert request["status"]["message"] == "unresolved"


def test_the_mirror_only_posts_and_needs_no_model(bundle):
    fake = FakeLangfuse()
    mirror.mirror(bundle, fake)
    assert fake.calls and all(path.startswith("/api/public/") for path, _, _ in fake.calls)
    assert not hasattr(fake, "get")


# --- label export (seam 6) ---------------------------------------------------------------------

def _label(bundle, item, criterion, score):
    assessment.record_label(bundle, review_id=item["review_id"], case_id=item["case_id"],
                            criterion=criterion, score=score, excerpt="", evidence_ref="L1",
                            reason="r", assessor="author")


def test_label_exports_are_numbered_and_never_rewritten(bundle):
    item = review.prepare_batch(bundle, size=1, seed=2)["items"][0]
    _label(bundle, item, "facts", 2)
    first = review.export_labels(bundle)
    assert first["version"] == 1 and first["count"] == 1
    assert review.export_labels(bundle)["version"] == 1
    v1 = (bundle.root / first["file"]["path"]).read_text()
    _label(bundle, item, "support", 1)
    second = review.export_labels(bundle)
    assert second["version"] == 2 and second["count"] == 2
    assert (bundle.root / first["file"]["path"]).read_text() == v1
    assert review.verify_exports(bundle) == []


def test_an_export_keeps_review_ids_but_not_the_identity_map(bundle):
    item = review.prepare_batch(bundle, size=1, seed=2)["items"][0]
    _label(bundle, item, "facts", 2)
    data = json.loads((bundle.root / review.export_labels(bundle)["file"]["path"]).read_text())
    assert data["events"][0]["review_id"] == item["review_id"]
    assert "p1-" not in json.dumps(data)


def test_a_tampered_export_is_detected(bundle):
    item = review.prepare_batch(bundle, size=1, seed=2)["items"][0]
    _label(bundle, item, "facts", 2)
    export = review.export_labels(bundle)
    path = bundle.root / export["file"]["path"]
    path.write_text(path.read_text().replace('"score": 2', '"score": 1'))
    assert review.verify_exports(bundle)
