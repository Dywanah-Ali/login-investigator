"""Door 6: direct retrieval is graded from evidence, with no answer-generating model."""

from evals import scoring
import asyncio
import json
from pathlib import Path
import pytest

from login_investigator.knowledge_base import build_knowledge_base, open_knowledge_base, reader_settings
from login_investigator.postgres import ServerSettings
from test_knowledge_base import DATASET, FakeEmbedder, build_database  # noqa: F401


def test_retrieval_requires_every_gold_chunk_in_the_shortlist_not_just_the_union():
    question = {"gold": {"chunks": ["a", "b"], "records": [], "paths": []}}
    artifact = {"search": {"chunks": [{"chunk": {"id": "x"}}, {"chunk": {"id": "a"}}],
                           "candidates": [{"chunk": {"id": "b"}}]}, "walk": None}
    result = scoring.score_retrieval(question, artifact)
    assert result["first_gold_rank"] == 2
    assert result["passed"] is False
    assert result["checks"][0]["missing"] == ["b"]
    artifact["search"]["chunks"].append({"chunk": {"id": "b"}})
    assert scoring.score_retrieval(question, artifact)["passed"] is True


@pytest.mark.parametrize("records,paths,passed", [
    (["group-a"], [["user-a", "group-a"]], True),
    (["group-a", "group-b"], [["user-a", "group-a"]], False),
    ([], [], False),
    (["group-a"], [["user-b", "group-a"]], False),
])
def test_graph_gate_requires_exact_records_and_paths(records, paths, passed):
    question = {"gold": {"chunks": [], "records": ["group-a"], "paths": [["user-a", "group-a"]]}}
    artifact = {"search": None, "walk": {"records": records, "paths": paths}}
    assert scoring.score_retrieval(question, artifact)["passed"] is passed


def test_absent_topic_is_reported_as_a_miss_while_none_is_disabled():
    question = {"gold": {"chunks": [], "records": [], "paths": []}, "verdict": "none"}
    result = scoring.score_retrieval(question, {"search": {"chunks": [], "verdict": "weak"}})
    assert result["passed"] is False
    assert result["checks"] == [{"id": "verdict", "passed": False, "expected": "none", "actual": "weak"}]


def test_direct_runner_walks_the_world_without_using_gold_to_choose_records(build_database: ServerSettings):
    from evals.retrieval import evaluate_retrieval

    questions = json.loads((Path(__file__).parents[1] / "evals/knowledge_base_questions.json").read_text())["questions"]
    questions = [q for q in questions if q["id"] in {"K03", "K04"}]
    # A wrong answer key must fail the grade, not change what the walk returns.
    questions[0]["gold"]["records"].append("group-invented")

    async def check():
        await build_knowledge_base(DATASET, build_database, FakeEmbedder())
        async with open_knowledge_base(reader_settings(build_database), dataset=DATASET, embedder=FakeEmbedder()) as kb:
            report = await evaluate_retrieval(kb, questions)
        assert report["integrity"]["nodes"]["person"] == 50
        first, second = report["records"]
        assert first["artifact"]["search"] is None
        assert first["artifact"]["walk"]["records"] == ["group-all-staff", "group-finance-approvers"]
        assert first["passed"] is False
        assert all(c["passed"] for c in second["checks"] if c["id"].startswith("graph"))
        assert len(second["artifact"]["search"]["chunks"]) == 20

    asyncio.run(check())


def test_runner_checks_integrity_before_calling_the_embedding_service(build_database: ServerSettings):
    from evals.retrieval import evaluate_retrieval
    from login_investigator.knowledge_base import GraphIntegrityError

    class MustNotQuery(FakeEmbedder):
        def embed_query(self, text: str) -> list[float]:
            raise AssertionError("A corrupt graph must stop before retrieval")

    async def check():
        await build_knowledge_base(DATASET, build_database, FakeEmbedder())
        async with open_knowledge_base(reader_settings(build_database), dataset=DATASET, embedder=MustNotQuery()) as kb:
            kb.graph.nodes["user-amelia.ward"]["department"] = "corrupted"
            with pytest.raises(GraphIntegrityError):
                await evaluate_retrieval(kb, [{"id": "test", "type": "document_lookup", "turns": ["MFA"]}])

    asyncio.run(check())


def test_saved_retrieval_results_use_per_question_gates_and_rescore_offline(tmp_path, monkeypatch):
    from datetime import datetime, timezone
    from evals import run

    monkeypatch.setattr(run, "RESULTS", tmp_path)
    record = {"question": "K05", "category": "absent_topic", "run": 1,
              "security_checked": False, "security_passed": True,
              "artifact": {"search": {"chunks": [], "verdict": "weak"}},
              "checks": [{"id": "verdict", "passed": False}], "passed": False}
    run.save([record], datetime.now(timezone.utc), "retrieval-test", "test", 1, 1,
             "offline", mode="retrieval", details={"integrity": {"checked": True}})
    [path] = tmp_path.glob("*.json")
    saved = json.loads(path.read_text())
    assert saved["model"] is None
    assert saved["targets"] == {"every_applicable_check": True}
    assert saved["details"]["integrity"]["checked"] is True
    assert not (tmp_path / "summary.md").exists()
    assert (tmp_path / "retrieval-summary.md").exists()
    run.rescore(path, "offline rescore")
    newest = max(tmp_path.glob("*.json"), key=lambda p: p.stat().st_mtime_ns)
    rescored = json.loads(newest.read_text())
    assert rescored["records"][0]["passed"] is False
    assert rescored["records"][0]["checks"][0]["actual"] == "weak"
