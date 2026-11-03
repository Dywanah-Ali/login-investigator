"""T54 seam 2: the run bundle (the local evidence logbook).

Local records are authoritative: every event is on disk before the next step, a crash cannot erase
earlier requests, recovery never repeats a possibly billed request, unknown cost stays unknown and
a settlement replaces a charge instead of adding to it.
"""

from __future__ import annotations

import json

import pytest

from evals.comparison import records

MANIFEST = {"stage": "screening", "experiment_id": "exp-test"}


def _bundle(tmp_path):
    return records.RunBundle.create(tmp_path / "run", MANIFEST)


def test_manifest_is_frozen_and_cannot_be_overwritten(tmp_path):
    bundle = _bundle(tmp_path)
    assert records.RunBundle.open(tmp_path / "run").manifest["stage"] == "screening"
    with pytest.raises(FileExistsError):
        records.RunBundle.create(tmp_path / "run", MANIFEST)
    assert bundle.manifest["record_schema"] == records.SCHEMA


def test_events_are_ordered_and_survive_reopening(tmp_path):
    bundle = _bundle(tmp_path)
    bundle.append("trial_started", trial_id="t1")
    bundle.append("trial_finished", trial_id="t1", status="completed")
    reopened = records.RunBundle.open(tmp_path / "run")
    assert [(e["seq"], e["type"]) for e in reopened.events()] == [
        (1, "trial_started"), (2, "trial_finished")]


def test_a_torn_last_line_from_a_crash_is_reported_not_lost(tmp_path):
    bundle = _bundle(tmp_path)
    bundle.append("trial_started", trial_id="t1")
    with (tmp_path / "run" / "events.jsonl").open("a") as handle:
        handle.write('{"seq": 2, "type": "request_sta')
    reopened = records.RunBundle.open(tmp_path / "run")
    assert [e["type"] for e in reopened.events()] == ["trial_started"]
    assert reopened.torn_tail is True
    reopened.append("trial_interrupted", trial_id="t1", reason="test")
    assert [e["seq"] for e in reopened.events()] == [1, 2]
    assert '"request_sta' in (tmp_path / "run" / "torn-fragments.txt").read_text()


def test_secrets_are_removed_before_anything_reaches_disk(tmp_path, monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "real-key-value-123456")
    bundle = _bundle(tmp_path)
    bundle.append("request_finished", request_id="r1",
                  error="401 for key real-key-value-123456 with Authorization: Bearer abc.def")
    artifact = bundle.write_artifact("answers/r1.txt", "sk-or-v1-0123456789abcdefghij leaked")
    on_disk = (tmp_path / "run" / "events.jsonl").read_text()
    assert "real-key-value-123456" not in on_disk and "abc.def" not in on_disk
    assert "sk-or-v1-0123456789abcdefghij" not in (tmp_path / "run" / artifact["path"]).read_text()
    assert records.REDACTED in on_disk


def test_artifacts_are_referenced_by_path_and_hash(tmp_path):
    bundle = _bundle(tmp_path)
    ref = bundle.write_artifact("inputs/t1.txt", "hello")
    assert ref == {"path": "artifacts/inputs/t1.txt",
                   "sha256": "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"}
    assert bundle.read_artifact(ref) == "hello"


def test_recovery_marks_unfinished_requests_unresolved_and_never_repeats_them(tmp_path):
    bundle = _bundle(tmp_path)
    bundle.append("trial_started", trial_id="t1", slot=1)
    bundle.append("request_started", request_id="r1", trial_id="t1")
    bundle.append("request_finished", request_id="r1", status="completed", cost_usd=0.01)
    bundle.append("request_started", request_id="r2", trial_id="t1")  # crash here
    report = records.recover(bundle)
    assert report == {"unresolved_requests": ["r2"], "interrupted_trials": ["t1"]}
    state = records.trial_states(bundle)
    assert state["t1"] == "interrupted"
    assert records.recover(bundle) == {"unresolved_requests": [], "interrupted_trials": []}
    resources = records.resources(bundle)
    assert resources["requests"]["r2"]["cost_usd"] is None
    assert resources["requests"]["r2"]["status"] == "unresolved"


def test_unknown_cost_is_not_zero(tmp_path):
    bundle = _bundle(tmp_path)
    bundle.append("request_started", request_id="r1", trial_id="t1")
    bundle.append("request_finished", request_id="r1", status="completed", cost_usd=0.02)
    bundle.append("request_started", request_id="r2", trial_id="t1")
    bundle.append("request_finished", request_id="r2", status="error", cost_usd=None)
    totals = records.resources(bundle)["total"]
    assert totals["known_cost_usd"] == pytest.approx(0.02)
    assert totals["unknown_cost_requests"] == 1
    assert totals["cost_complete"] is False


def test_a_settlement_replaces_the_charge_instead_of_adding(tmp_path):
    bundle = _bundle(tmp_path)
    bundle.append("request_started", request_id="r1", trial_id="t1")
    bundle.append("request_finished", request_id="r1", status="completed", cost_usd=None)
    bundle.append("cost_settled", request_id="r1", cost_usd=0.03, source="generation lookup")
    bundle.append("cost_settled", request_id="r1", cost_usd=0.031, source="generation lookup")
    resources = records.resources(bundle)
    assert resources["total"]["known_cost_usd"] == pytest.approx(0.031)
    assert resources["total"]["unknown_cost_requests"] == 0
    assert resources["requests"]["r1"]["cost_source"] == "generation lookup"


def test_usage_sums_keep_unknown_separate(tmp_path):
    bundle = _bundle(tmp_path)
    for rid, usage in (("r1", {"input": 100, "output": 20, "reasoning": 5}), ("r2", None)):
        bundle.append("request_started", request_id=rid, trial_id="t1")
        bundle.append("request_finished", request_id=rid, status="completed", usage=usage,
                      cost_usd=0.0)
    total = records.resources(bundle)["total"]
    assert total["usage"]["input"] == 100 and total["usage"]["output"] == 20
    assert total["unknown_usage_requests"] == 1
    # r1 reported no cache_read: that field is unknown for both requests, not zero.
    assert total["unknown_usage_by_key"] == {"input": 1, "output": 1, "reasoning": 1,
                                             "cache_read": 2}


def test_events_file_is_plain_json_lines(tmp_path):
    bundle = _bundle(tmp_path)
    bundle.append("trial_started", trial_id="t1")
    line = (tmp_path / "run" / "events.jsonl").read_text().splitlines()[0]
    assert json.loads(line)["type"] == "trial_started"
