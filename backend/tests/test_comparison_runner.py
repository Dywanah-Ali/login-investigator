"""T54 seam 3: the comparison runner, driven by a scripted fake model.

Expected values come from T52's approved policy: 6 x 4 x 3 = 72 trials with the first pass as
the first 24, rotated order, 180 s per request and 600 s per trial, recorded retries with no
count cap, no retry of permanent errors, fresh memory and no gold in model input.
"""

from __future__ import annotations

import json
from collections import Counter

import pytest

from evals.comparison import fixtures, records, roles, runner
from evals.comparison.adapters import (
    AdapterError,
    FakeAdapter,
    FakeClock,
    ModelConfig,
    ModelResponse,
)

CASES = ["O1-02", "O1-06", "O1-09", "O1-12-D"]
CONFIGS = [ModelConfig(config_id=f"m{i}", label=f"Model {i}", model=f"vendor/model-{i}",
                       provider="prov", reasoning={"effort": "medium"}) for i in range(1, 7)]


def answer(text="Assessment [L1]."):
    return lambda request, n: ModelResponse(text=text, usage={"input": 10, "output": 5},
                                            cost_usd=0.001, generation_id=f"gen-{n}")


def make(tmp_path, script, *, stage="screening", configs=CONFIGS, cases=CASES, passes=3,
         designs=("A",), elapsed=lambda r, n: 1.0):
    clock = FakeClock()
    adapter = FakeAdapter(script, clock, elapsed)
    bundle = runner.new_run(tmp_path / "run", stage=stage, configs=list(configs),
                            case_ids=list(cases), passes=passes, designs=list(designs),
                            adapter=adapter, experiment_id="exp", clock=clock)
    return bundle, adapter, runner.Runner(bundle, adapter, clock=clock, sleep=clock.advance)


def finished(bundle):
    return {e["trial_id"]: e for e in bundle.events() if e["type"] == "trial_finished"}


def requests_of(bundle, trial_id):
    return [e for e in bundle.events() if e["type"] == "request_started" and e["trial_id"] == trial_id]


# --- schedule ----------------------------------------------------------------------------------

def test_screening_schedule_is_72_trials_with_the_first_pass_first():
    schedule = runner.build_schedule("screening", CONFIGS, CASES, 3, ["A"])
    assert len(schedule) == 72
    assert {s["pass"] for s in schedule[:24]} == {1}
    for number in (1, 2, 3):
        block = [s for s in schedule if s["pass"] == number]
        assert Counter(s["config_id"] for s in block) == {c.config_id: 4 for c in CONFIGS}
    assert len({s["trial_id"] for s in schedule}) == 72


def test_rotation_puts_every_model_first_equally_often():
    schedule = runner.build_schedule("screening", CONFIGS, CASES, 3, ["A"])
    firsts = [schedule[i]["config_id"] for i in range(0, 72, 6)]
    assert Counter(firsts) == {c.config_id: 2 for c in CONFIGS}


def test_calibration_is_one_model_three_designs_four_cases():
    schedule = runner.build_schedule("architecture_calibration", CONFIGS[:1], CASES, 1,
                                     ["A", "B", "C"])
    assert len(schedule) == 12
    assert Counter(s["design"] for s in schedule) == {"A": 4, "B": 4, "C": 4}


def test_screening_refuses_specialist_designs(tmp_path):
    with pytest.raises(ValueError):
        make(tmp_path, answer(), designs=("A", "B"))


def test_manifest_freezes_versions_settings_and_schedule(tmp_path):
    bundle, _, _ = make(tmp_path, answer())
    manifest = bundle.manifest
    assert manifest["fixture_version"] == fixtures.fixture_version()
    assert manifest["prompt_version"] == roles.prompt_version()
    assert manifest["settings"]["request_timeout_s"] == 180
    assert manifest["settings"]["trial_timeout_s"] == 600
    assert manifest["settings"]["token_caps"] is None
    assert manifest["settings"]["retry_policy"]["count_cap"] is None
    assert len(manifest["schedule"]) == 72
    assert manifest["code"]["comparison_source_sha256"]


# --- running -----------------------------------------------------------------------------------

def test_a_full_screen_runs_every_trial_once_in_order(tmp_path):
    bundle, adapter, run = make(tmp_path, answer())
    run.run()
    done = finished(bundle)
    assert len(done) == 72 and {e["status"] for e in done.values()} == {"completed"}
    started = [e["trial_id"] for e in bundle.events() if e["type"] == "trial_started"]
    assert started == [s["trial_id"] for s in bundle.manifest["schedule"]]
    assert len(adapter.requests) == 72


def test_the_setup_checkpoint_stops_after_24_and_resumes_without_repeats(tmp_path):
    bundle, adapter, run = make(tmp_path, answer())
    run.run(until_slot=24)
    assert len(finished(bundle)) == 24
    run.run()
    assert len(finished(bundle)) == 72 and len(adapter.requests) == 72


def test_every_trial_has_fresh_memory(tmp_path):
    bundle, adapter, run = make(tmp_path, answer("Unique answer text 42 [L1]."), passes=1)
    run.run()
    memories = [e["memory_id"] for e in bundle.events() if e["type"] == "trial_started"]
    assert len(set(memories)) == len(memories) == 24
    for request in adapter.requests:
        assert [m["role"] for m in request.messages] == ["system", "user"]
        assert "Unique answer text 42" not in json.dumps(request.messages)


def test_gold_never_reaches_any_model_request(tmp_path):
    _, adapter, run = make(tmp_path, answer(), passes=1)
    run.run()
    sent = json.dumps([r.messages for r in adapter.requests])
    for case_id in CASES:
        gold = json.loads((fixtures.FROZEN / "gold" / f"{case_id}.json").read_text())
        for text in gold["required_findings"] + [c["text"] for c in gold["critical_errors"]]:
            assert text not in sent


def test_screening_offers_no_tools(tmp_path):
    _, adapter, run = make(tmp_path, answer(), passes=1)
    run.run()
    assert all(r.tools is None for r in adapter.requests)


def test_transient_errors_are_retried_with_recorded_lineage(tmp_path):
    def script(request, n):
        return AdapterError("transient", "429 rate limited") if n < 2 else answer()(request, n)
    bundle, _, run = make(tmp_path, script, cases=CASES[:1], configs=CONFIGS[:1], passes=1)
    run.run()
    attempts = requests_of(bundle, "p1-O1-02-m1-A")
    assert [a["attempt"] for a in attempts] == [1, 2, 3]
    assert attempts[0]["retry_of"] is None
    assert attempts[1]["retry_of"] == attempts[0]["request_id"]
    assert attempts[2]["retry_of"] == attempts[1]["request_id"]
    assert attempts[1]["retry_origin"] == "runner" and "429" in attempts[1]["retry_reason"]
    assert finished(bundle)["p1-O1-02-m1-A"]["status"] == "completed"
    totals = records.resources(bundle)["total"]
    assert totals["retry_count"] == 2 and totals["unknown_cost_requests"] == 2


def test_permanent_errors_are_not_retried(tmp_path):
    bundle, adapter, run = make(tmp_path, lambda r, n: AdapterError("permanent", "400 bad request"),
                                cases=CASES[:1], configs=CONFIGS[:1], passes=1)
    run.run()
    assert len(adapter.requests) == 1
    assert finished(bundle)["p1-O1-02-m1-A"]["status"] == "error"


def test_request_and_trial_deadlines_hold_across_retries(tmp_path):
    bundle, adapter, run = make(tmp_path, answer(), cases=CASES[:1], configs=CONFIGS[:1],
                                passes=1, elapsed=lambda r, n: 999.0)
    run.run()
    timeouts = [r.timeout_s for r in adapter.requests]
    assert timeouts[0] == 180 and all(t <= 180 for t in timeouts)
    elapsed_total = finished(bundle)["p1-O1-02-m1-A"]["elapsed_s"]
    assert finished(bundle)["p1-O1-02-m1-A"]["status"] == "timeout"
    assert elapsed_total <= 600
    statuses = [e["status"] for e in bundle.events() if e["type"] == "request_finished"]
    assert statuses and set(statuses) == {"timeout"}
    assert len(statuses) == len(adapter.requests)


def test_a_partial_answer_from_a_failed_request_is_kept(tmp_path):
    bundle, _, run = make(tmp_path, lambda r, n: AdapterError("permanent", "stream cut",
                                                               partial_text="Half an answer"),
                          cases=CASES[:1], configs=CONFIGS[:1], passes=1)
    run.run()
    trial = finished(bundle)["p1-O1-02-m1-A"]
    assert trial["status"] == "error" and trial["final_answer"] is None
    assert bundle.read_artifact(trial["partial_answer"]) == "Half an answer"


def test_an_interrupted_run_never_resends_the_open_request(tmp_path):
    def script(request, n):
        return KeyboardInterrupt() if n == 1 else answer()(request, n)
    bundle, adapter, run = make(tmp_path, script, cases=CASES[:1], configs=CONFIGS[:3], passes=1)
    with pytest.raises(KeyboardInterrupt):
        run.run()
    interrupted_trial = bundle.manifest["schedule"][1]["trial_id"]
    result = run.run()
    assert result["recovery"]["interrupted_trials"] == [interrupted_trial]
    assert len(result["recovery"]["unresolved_requests"]) == 1
    assert len(requests_of(bundle, interrupted_trial)) == 1
    assert records.trial_states(bundle)[interrupted_trial] == "interrupted"
    assert len(adapter.requests) == 3


def test_a_rerun_is_explicit_linked_and_keeps_the_original(tmp_path):
    bundle, _, run = make(tmp_path, answer(), cases=CASES[:1], configs=CONFIGS[:1], passes=1)
    run.run()
    new_id = runner.schedule_rerun(bundle, "p1-O1-02-m1-A", reason="prompt fence fixed",
                                   repair_version="repair-1")
    run.run()
    done = finished(bundle)
    assert set(done) == {"p1-O1-02-m1-A", new_id}
    started = {e["trial_id"]: e for e in bundle.events() if e["type"] == "trial_started"}
    assert started[new_id]["rerun_of"] == "p1-O1-02-m1-A"
    assert started[new_id]["repair_version"] == "repair-1"


# --- designs -----------------------------------------------------------------------------------

def _calibration(tmp_path, design):
    def script(request, n):
        return ModelResponse(text=f"output {n} [D1]", continuation={"id": f"c{n}"})
    return make(tmp_path, script, stage="architecture_calibration", configs=CONFIGS[:1],
                cases=CASES[1:2], passes=1, designs=(design,))


def test_design_b_hands_the_specialist_findings_to_the_investigator(tmp_path):
    bundle, adapter, run = _calibration(tmp_path, "B")
    run.run()
    specialist, investigator = adapter.requests
    assert specialist.messages[0]["content"] == roles.APPLICABILITY
    assert investigator.messages[0]["content"] == roles.INVESTIGATOR
    assert "<<<SPECIALIST FINDINGS\noutput 0 [D1]" in investigator.messages[1]["content"]
    assert fixtures.render_case(fixtures.load_case("O1-06")) in investigator.messages[1]["content"]
    assert [e["role"] for e in bundle.events() if e["type"] == "role_output"] == [
        "applicability_specialist"]


def test_design_c_reviews_its_own_draft_then_finalises(tmp_path):
    bundle, adapter, run = _calibration(tmp_path, "C")
    run.run()
    _draft, review, final = adapter.requests
    assert review.messages[0]["content"] == roles.REVIEWER
    assert "<<<DRAFT ASSESSMENT\noutput 0 [D1]" in review.messages[1]["content"]
    assert [m["role"] for m in final.messages] == ["system", "user", "assistant", "user"]
    assert final.messages[2]["continuation"] == {"id": "c0"}
    assert "<<<REVIEW\noutput 1 [D1]" in final.messages[3]["content"]
    trial = next(iter(finished(bundle).values()))
    assert bundle.read_artifact(trial["final_answer"]) == "output 2 [D1]"


# --- compatibility -------------------------------------------------------------------------------

def test_compatibility_completes_a_tool_round_trip(tmp_path):
    def script(request, n):
        if n == 0:
            return ModelResponse(text="", tool_calls=[{"id": "call-1", "name": "get_record",
                                                       "arguments": '{"ref": "CMP-1"}'}],
                                 model_reported="vendor/model-1", provider_reported="prov")
        assert request.messages[-1] == {"role": "tool", "tool_call_id": "call-1", "content": json.dumps(
            {"ref": "CMP-1", "text": roles.COMPATIBILITY_RECORDS["CMP-1"]})}
        return ModelResponse(text="The colour code is 7 [CMP-1].", model_reported="vendor/model-1")
    bundle, adapter, run = make(tmp_path, script, stage="compatibility", configs=CONFIGS[:1],
                                cases=[], passes=1)
    run.run()
    checks = next(e for e in bundle.events() if e["type"] == "compatibility_checks")
    assert checks["tool_round_trip"] is True and checks["output_contract"] is True
    assert adapter.requests[0].tools == [roles.COMPATIBILITY_TOOL]
    tool = next(e for e in bundle.events() if e["type"] == "tool_call")
    assert tool["executed"] is True and tool["name"] == "get_record"


def test_compatibility_records_a_missing_tool_call(tmp_path):
    bundle, _, run = make(tmp_path, answer("I think it is 7 [CMP-1]."), stage="compatibility",
                          configs=CONFIGS[:2], cases=[], passes=1)
    run.run()
    checks = [e for e in bundle.events() if e["type"] == "compatibility_checks"]
    assert len(checks) == 2 and all(c["tool_round_trip"] is False for c in checks)
