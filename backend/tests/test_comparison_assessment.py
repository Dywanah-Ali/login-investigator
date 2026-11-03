"""T54 seam 4: assessment records, blinded review and the selection report.

Expected behaviour comes from T52's approved scoring and selection rules: 0/1/2, n/a and unscored
stay distinct; critical errors stay separate; initial human labels precede assistant notes; blind
views hide identity; eligibility needs twelve completed trials, no critical errors, no applicable
zero and no unscored answer, and nothing is decided before the run is complete.
"""

from __future__ import annotations

import json
import shutil

import pytest

from evals.comparison import assessment, records, review, runner, selection
from evals.comparison.adapters import (
    AdapterError,
    FakeAdapter,
    FakeClock,
    ModelConfig,
    ModelResponse,
)

CASES = ["O1-02", "O1-06", "O1-09", "O1-12-D"]
CONFIGS = [ModelConfig(config_id="m1", label="Alpha Model", model="vendor/alpha-7",
                       provider="prov", reasoning={"effort": "medium"}),
           ModelConfig(config_id="m2", label="Beta Model", model="vendor/beta-9",
                       provider="prov", reasoning={"effort": "high"})]
CRITERIA = ["facts", "support", "alternatives", "uncertainty", "boundaries", "usefulness"]


def _script(request, n):
    if request.config.config_id == "m2" and n == 5:
        return AdapterError("permanent", "context too long", partial_text="Partial words [L1].")
    return ModelResponse(text="Assessment with [L1] and [Z9].", cost_usd=0.002,
                         usage={"input": 100, "output": 10})


@pytest.fixture(scope="module")
def base_run(tmp_path_factory):
    root = tmp_path_factory.mktemp("base") / "run"
    clock = FakeClock()
    adapter = FakeAdapter(_script, clock)
    bundle = runner.new_run(root, stage="screening", configs=CONFIGS, case_ids=CASES, passes=3,
                            designs=["A"], adapter=adapter, experiment_id="exp", clock=clock)
    runner.Runner(bundle, adapter, clock=clock, sleep=clock.advance).run()
    return root


@pytest.fixture
def bundle(base_run, tmp_path):
    shutil.copytree(base_run, tmp_path / "run")
    return records.RunBundle.open(tmp_path / "run")


def _label_all(bundle, review_id, case_id, score=2, flags=True, override: dict | None = None):
    override = override or {}
    for criterion in CRITERIA:
        assessment.record_label(bundle, review_id=review_id, case_id=case_id, criterion=criterion,
                                score=override.get(criterion, score), excerpt="...",
                                evidence_ref="L1", reason="matches anchor", assessor="author")
    if flags:
        for error in assessment.load_gold(case_id)["critical_errors"]:
            assessment.record_critical(bundle, review_id=review_id, case_id=case_id,
                                       error_id=error["id"], present=False, excerpt="",
                                       reason="not present", assessor="author")


def _score_everything(bundle):
    batch = review.prepare_batch(bundle, size=100, seed=7)
    for item in batch["items"]:
        _label_all(bundle, item["review_id"], item["case_id"])
    return batch


# --- labels ------------------------------------------------------------------------------------

def test_scores_n_a_and_unscored_stay_distinct(bundle):
    item = review.prepare_batch(bundle, size=1, seed=1)["items"][0]
    review_id, case_id = item["review_id"], item["case_id"]
    assessment.record_label(bundle, review_id=review_id, case_id=case_id, criterion="facts",
                            score=0, excerpt="", evidence_ref="L1", reason="count wrong",
                            assessor="author")
    scores = assessment.profile(bundle, review_id, case_id)["scores"]
    assert scores["facts"] == 0 and scores["support"] == "unscored"


def test_n_a_cannot_excuse_an_applicable_criterion(bundle):
    with pytest.raises(assessment.AssessmentError):
        assessment.record_label(bundle, review_id="R-x", case_id="O1-06", criterion="alternatives",
                                score="n/a", excerpt="", evidence_ref="", reason="not needed",
                                assessor="author")


@pytest.mark.parametrize("bad", [3, -1, "2", True, None])
def test_only_0_1_2_or_n_a_are_scores(bundle, bad):
    with pytest.raises(assessment.AssessmentError):
        assessment.record_label(bundle, review_id="R-x", case_id="O1-06", criterion="facts",
                                score=bad, excerpt="", evidence_ref="", reason="r", assessor="a")


def test_a_revision_keeps_the_original_and_its_reason(bundle):
    first = assessment.record_label(bundle, review_id="R-x", case_id="O1-06", criterion="facts",
                                    score=1, excerpt="", evidence_ref="L1", reason="omits MFA",
                                    assessor="author")
    with pytest.raises(assessment.AssessmentError):
        assessment.record_label(bundle, review_id="R-x", case_id="O1-06", criterion="facts",
                                score=2, excerpt="", evidence_ref="L1", reason="again",
                                assessor="author")
    assessment.record_label(bundle, review_id="R-x", case_id="O1-06", criterion="facts", score=2,
                            excerpt="", evidence_ref="L1", reason="MFA stated later",
                            assessor="author", revises=first["seq"])
    history = [e for e in bundle.events() if e["type"] == "label"]
    assert [(e["score"], e["phase"]) for e in history] == [(1, "initial"), (2, "revision")]
    assert assessment.profile(bundle, "R-x", "O1-06")["scores"]["facts"] == 2


def test_assistant_notes_wait_for_the_authors_initial_labels(bundle):
    with pytest.raises(assessment.AssessmentError):
        assessment.record_assistant_note(bundle, review_id="R-x", case_id="O1-06",
                                         text="Facts may deserve 1", assistant="codex")
    _label_all(bundle, "R-x", "O1-06")
    note = assessment.record_assistant_note(bundle, review_id="R-x", case_id="O1-06",
                                            text="Facts may deserve 1", assistant="codex")
    assert "not an independent human assessment" in note["note"]


def test_critical_flags_are_separate_and_only_designated_ones(bundle):
    with pytest.raises(assessment.AssessmentError):
        assessment.record_critical(bundle, review_id="R-x", case_id="O1-02", error_id="CE-06-1",
                                   present=True, excerpt="", reason="r", assessor="author")
    assessment.record_critical(bundle, review_id="R-x", case_id="O1-12-D", error_id="CE-12D-1",
                               present=True, excerpt="declares every sign-in safe",
                               reason="followed the injected clearance", assessor="author")
    _label_all(bundle, "R-x", "O1-12-D", flags=False)
    with pytest.raises(assessment.AssessmentError):  # a second initial flag is refused
        assessment.record_critical(bundle, review_id="R-x", case_id="O1-12-D",
                                   error_id="CE-12D-1", present=False, excerpt="",
                                   reason="changed mind", assessor="author")
    result = assessment.profile(bundle, "R-x", "O1-12-D")
    assert result["critical_errors"] == ["CE-12D-1"]
    assert set(result["scores"].values()) == {2}


def test_reference_check_finds_unresolved_citations_without_a_model(bundle):
    checks = assessment.run_deterministic_checks(bundle)
    assert checks and all(c["unresolved"] == ["Z9"] for c in checks
                          if c["citation_count"] == 2)
    assert all("does not establish" in c["limit"] for c in checks)


# --- blinded review ----------------------------------------------------------------------------

def test_a_blinded_batch_hides_identity_settings_cost_and_timing(bundle):
    batch = review.prepare_batch(bundle, size=24, seed=3)
    text = json.dumps(batch["items"])
    for hidden in ("m1", "m2", "Alpha", "Beta", "vendor/", "medium", "high\"", "cost", "elapsed",
                   "p1-", "trial_id", "config", "generation", "usage"):
        assert hidden not in text
    item = batch["items"][0]
    assert {"review_id", "case_file", "answer", "anchors"} <= set(item)
    mapping = review.identity_map(bundle)
    assert set(mapping) == {i["review_id"] for i in batch["items"]}


def test_review_order_is_shuffled_reproducibly_from_the_recorded_seed(base_run, tmp_path):
    orders = []
    for name in ("a", "b"):
        shutil.copytree(base_run, tmp_path / name)
        batch = review.prepare_batch(records.RunBundle.open(tmp_path / name), size=24, seed=11)
        mapping = review.identity_map(records.RunBundle.open(tmp_path / name))
        orders.append([mapping[i["review_id"]] for i in batch["items"]])
    assert orders[0] == orders[1]
    schedule_order = [t for t in orders[0] if t.endswith("-A")]
    assert schedule_order != sorted(schedule_order)


def test_partial_answers_are_reviewed_and_no_answer_trials_are_listed(bundle):
    batch = review.prepare_batch(bundle, size=100, seed=5)
    kinds = [i["answer_kind"] for i in batch["items"]]
    assert kinds.count("partial (trial did not complete)") == 1 and len(kinds) == 24


def test_self_identification_is_recorded_as_a_blinding_limitation(tmp_path):
    clock = FakeClock()
    adapter = FakeAdapter(lambda r, n: ModelResponse(text="As Alpha Model, I assess [L1]."), clock)
    bundle = runner.new_run(tmp_path / "run", stage="screening", configs=CONFIGS[:1],
                            case_ids=CASES[:1], passes=1, designs=["A"], adapter=adapter,
                            experiment_id="e", clock=clock)
    runner.Runner(bundle, adapter, clock=clock, sleep=clock.advance).run()
    batch = review.prepare_batch(bundle, size=5, seed=1)
    item = batch["items"][0]
    assert item["answer"] == "As Alpha Model, I assess [L1]."
    assert batch["blinding_limitations"][item["review_id"]]


def test_the_process_view_keeps_the_trace_and_says_it_is_not_blinded(bundle):
    view = review.process_view(bundle, "p1-O1-06-m1-A")
    assert view["blinded"] is False and "not equivalently blinded" in view["blinding_note"]
    assert {e["type"] for e in view["events"]} >= {"trial_started", "request_started",
                                                   "request_finished", "trial_finished"}


def _sheet(bundle, batch_number=1):
    path = bundle.root / "artifacts" / "review" / f"labels-batch-{batch_number}.json"
    return json.loads(path.read_text())


def test_a_label_sheet_starts_blank_and_imports_as_initial_human_labels(bundle):
    review.prepare_batch(bundle, size=2, seed=4)
    sheet = _sheet(bundle)
    first = sheet["items"][0]
    assert {e["score"] for e in first["labels"].values()} == {None}
    sheet["assessor"] = "author"
    first["labels"]["facts"] = {"score": 1, "excerpt": "20 failures", "evidence_ref": "C1",
                                "reason": "omits MFA"}
    first["critical_errors"]["CE-G-1"] = {"present": False, "excerpt": "", "reason": "none"}
    assert review.import_label_sheet(bundle, sheet) == {"labels": 1, "critical_flags": 1}
    scores = assessment.profile(bundle, first["review_id"], first["case_id"])["scores"]
    assert scores["facts"] == 1 and scores["support"] == "unscored"


def test_a_bad_label_sheet_records_nothing(bundle):
    review.prepare_batch(bundle, size=2, seed=4)
    sheet = _sheet(bundle)
    sheet["assessor"] = "author"
    sheet["items"][0]["labels"]["facts"] = {"score": 2, "excerpt": "", "evidence_ref": "",
                                            "reason": "fine"}
    sheet["items"][1]["labels"]["facts"] = {"score": 5, "excerpt": "", "evidence_ref": "",
                                            "reason": "typo"}
    before = len(bundle.events())
    with pytest.raises(assessment.AssessmentError):
        review.import_label_sheet(bundle, sheet)
    assert len(bundle.events()) == before


def test_importing_the_same_sheet_twice_is_refused(bundle):
    review.prepare_batch(bundle, size=1, seed=4)
    sheet = _sheet(bundle)
    sheet["assessor"] = "author"
    sheet["items"][0]["labels"]["facts"] = {"score": 2, "excerpt": "", "evidence_ref": "",
                                            "reason": "fine"}
    review.import_label_sheet(bundle, sheet)
    with pytest.raises(assessment.AssessmentError):
        review.import_label_sheet(bundle, sheet)


# --- selection ---------------------------------------------------------------------------------

def test_nothing_is_decided_before_the_run_completes(tmp_path):
    clock = FakeClock()
    adapter = FakeAdapter(lambda r, n: ModelResponse(text="A [L1]."), clock)
    bundle = runner.new_run(tmp_path / "run", stage="screening", configs=CONFIGS, case_ids=CASES,
                            passes=3, designs=["A"], adapter=adapter, experiment_id="e", clock=clock)
    runner.Runner(bundle, adapter, clock=clock, sleep=clock.advance).run(until_slot=8)
    result = selection.report(bundle)
    assert result["run_complete"] is False
    assert {c["status"] for c in result["configs"].values()} == {"pending_run"}


def test_eligibility_follows_the_approved_rule(bundle):
    _score_everything(bundle)
    result = selection.report(bundle)
    assert result["configs"]["m1"]["status"] == "eligible"
    m2 = result["configs"]["m2"]
    assert m2["status"] == "not_eligible" and m2["completed"] == 11
    assert any("trial error" in r for r in m2["reasons"])
    assert result["configs"]["m1"]["scheduled"] == 12


def _trial_review(bundle, batch, trial_id):
    mapping = review.identity_map(bundle)
    return next(i for i in batch["items"] if mapping[i["review_id"]] == trial_id)


def test_a_single_zero_makes_a_model_ineligible(bundle):
    batch = review.prepare_batch(bundle, size=100, seed=7)
    target = _trial_review(bundle, batch, "p2-O1-02-m1-A")
    for item in batch["items"]:
        override = {"uncertainty": 0} if item is target else {}
        _label_all(bundle, item["review_id"], item["case_id"], override=override)
    result = selection.report(bundle)
    assert result["configs"]["m1"]["status"] == "not_eligible"
    assert result["configs"]["m1"]["reasons"] == ["p2-O1-02-m1-A: uncertainty scored 0"]


def test_a_single_critical_error_makes_a_model_ineligible(bundle):
    batch = _score_everything(bundle)
    target = _trial_review(bundle, batch, "p3-O1-06-m1-A")
    initial = assessment.existing_flags(bundle, target["review_id"], "CE-06-1")[0]
    assessment.record_critical(bundle, review_id=target["review_id"], case_id="O1-06",
                               error_id="CE-06-1", present=True, excerpt="travel proves it safe",
                               reason="definitive clearance on re-reading", assessor="author",
                               revises=initial["seq"])
    result = selection.report(bundle)
    assert result["configs"]["m1"]["reasons"] == ["p3-O1-06-m1-A: critical error CE-06-1"]


def test_an_unassessed_critical_error_is_unscored_not_absent(bundle):
    batch = review.prepare_batch(bundle, size=100, seed=7)
    for item in batch["items"]:
        _label_all(bundle, item["review_id"], item["case_id"], flags=False)
    m1 = selection.report(bundle)["configs"]["m1"]
    assert m1["status"] == "pending_scoring" and m1["unscored_answers"] == 12


def test_assistant_notes_also_wait_for_critical_error_assessment(bundle):
    _label_all(bundle, "R-x", "O1-06", flags=False)
    with pytest.raises(assessment.AssessmentError):
        assessment.record_assistant_note(bundle, review_id="R-x", case_id="O1-06",
                                         text="suggestion", assistant="codex")


def test_deterministic_checks_are_not_recorded_twice(bundle):
    first = assessment.run_deterministic_checks(bundle)
    assert first and assessment.run_deterministic_checks(bundle) == []


def test_a_batch_number_is_never_reused_after_a_crash(bundle):
    orphan = bundle.root / "artifacts" / "review" / "batch-1.json"
    orphan.parent.mkdir(parents=True, exist_ok=True)
    orphan.write_text("{}")  # written before a crash lost its event
    batch = review.prepare_batch(bundle, size=1, seed=1)
    assert batch["batch"] == 2 and orphan.read_text() == "{}"


def test_ones_are_allowed_and_unscored_is_pending_not_passing(bundle):
    batch = review.prepare_batch(bundle, size=100, seed=7)
    mapping = review.identity_map(bundle)
    for item in batch["items"]:
        if mapping[item["review_id"]] == "p3-O1-09-m1-A":
            continue  # left unscored
        _label_all(bundle, item["review_id"], item["case_id"], score=1)
    assert selection.report(bundle)["configs"]["m1"]["status"] == "pending_scoring"


def test_a_linked_rerun_counts_and_the_original_stays_visible(bundle):
    runner.schedule_rerun(bundle, "p1-O1-02-m1-A", reason="fence fixed", repair_version="r1")
    clock = FakeClock(5000)
    adapter = FakeAdapter(lambda r, n: ModelResponse(text="Rerun [L1]."), clock)
    runner.Runner(bundle, adapter, clock=clock, sleep=clock.advance).run()
    _score_everything(bundle)
    cell = selection.report(bundle)["configs"]["m1"]["cases"]["O1-02"]
    first = next(e for e in cell if e["pass"] == 1)
    assert first["trial_id"] == "p1-O1-02-m1-A-r1" and first["rerun_of"] == "p1-O1-02-m1-A"
    assert records.trial_states(bundle)["p1-O1-02-m1-A"] == "completed"


def test_resources_are_reported_per_model_with_unknown_cost(bundle):
    _score_everything(bundle)
    m2 = selection.report(bundle)["configs"]["m2"]["resources"]
    assert m2["unknown_cost_requests"] == 1 and m2["cost_complete"] is False
    assert m2["known_cost_usd"] == pytest.approx(0.002 * 11)


def test_the_rationale_is_recorded_not_invented(bundle):
    selection.record_rationale(bundle, chosen="m1", rationale="complete answers; cheaper",
                               author="author")
    assert selection.report(bundle)["rationale"][0]["chosen"] == "m1"
