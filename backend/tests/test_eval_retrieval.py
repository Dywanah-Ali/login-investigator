"""Door 6: direct retrieval is graded from evidence, with no answer-generating model."""

import asyncio
import json
import sys
from pathlib import Path

import pytest
from test_knowledge_base import FakeEmbedder
from test_knowledge_base import build_database as build_database  # noqa: PLC0414 - Explicitly expose this imported pytest fixture.

from evals import scoring
from login_investigator.knowledge_base import (
    Reranker,
)
from login_investigator.knowledge_base.graph_version import open_version
from login_investigator.postgres import ServerSettings


def test_retrieval_requires_every_gold_chunk_in_the_fused_twenty_not_just_the_union():
    question = {"gold": {"chunks": ["a", "b"], "records": [], "paths": []}}
    # Candidates arrive in fused order; the re-ranker's kept chunks do not change the gate.
    fused = ["x", "a"] + [f"filler-{n}" for n in range(18)] + ["b"]
    artifact = {"search": {"chunks": [{"chunk": {"id": "b"}}],
                           "candidates": [{"chunk": {"id": i}} for i in fused]}, "walk": None}
    result = scoring.score_retrieval(question, artifact)
    assert result["first_gold_rank"] == 2
    assert result["passed"] is False
    assert result["checks"][0]["missing"] == ["b"]
    artifact["search"]["candidates"].insert(5, {"chunk": {"id": "b"}})
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


def test_direct_runner_walks_the_world_without_using_gold_to_choose_records(paired_default):
    from evals.retrieval import evaluate_retrieval

    questions = json.loads((Path(__file__).parents[1] / "evals/knowledge_base_questions.json").read_text())["questions"]
    questions = [q for q in questions if q["id"] in {"K03", "K04"}]
    # A wrong answer key must fail the grade, not change what the walk returns.
    questions[0]["gold"]["records"].append("group-invented")

    async def check():
        async with open_version(paired_default.marker, ServerSettings.from_env(), embedder=FakeEmbedder()) as kb:
            report = await evaluate_retrieval(kb, questions)
        assert report["integrity"]["nodes"]["person"] == 50
        first, second = report["records"]
        assert first["artifact"]["search"] is None
        assert first["artifact"]["walk"]["records"] == ["group-all-staff", "group-finance-approvers"]
        assert first["passed"] is False
        assert all(c["passed"] for c in second["checks"] if c["id"].startswith("graph"))
        assert len(second["artifact"]["search"]["chunks"]) == 20

    asyncio.run(check())


class LengthReranker(Reranker):
    async def ascore(self, query: str, texts: list[str]) -> list[float]:
        return [len(content) % 1000 / 1000 for content in texts]


def test_runner_records_reranker_scores_and_kept_chunks_and_grades_the_fused_twenty(paired_default):
    from evals.retrieval import evaluate_retrieval

    questions = json.loads((Path(__file__).parents[1] / "evals/knowledge_base_questions.json").read_text())["questions"]
    questions = [q for q in questions if q["id"] == "K04"]

    async def check():
        async with open_version(paired_default.marker, ServerSettings.from_env(),
                                embedder=FakeEmbedder()) as kb:
            [off] = (await evaluate_retrieval(kb, questions))["records"]
        async with open_version(paired_default.marker, ServerSettings.from_env(),
                                embedder=FakeEmbedder(), reranker=LengthReranker()) as kb:
            [on] = (await evaluate_retrieval(kb, questions))["records"]
        search = on["artifact"]["search"]
        assert len(search["chunks"]) == 5
        assert all(c["rerank_score"] is not None for c in search["chunks"])
        assert all(c["rerank_score"] is not None for c in search["candidates"][:20])
        assert off["artifact"]["search"]["chunks"][0]["rerank_score"] is None
        # The retrieval gate reads the fused 20 either way; the re-ranker is judged at T41.
        assert on["checks"] == off["checks"]
        assert on["first_gold_rank"] == off["first_gold_rank"]
        kept = {c["chunk"]["id"] for c in search["chunks"]}
        rank, dropped = next((rank, c["chunk"]["id"]) for rank, c in enumerate(search["candidates"][:20], 1)
                             if c["chunk"]["id"] not in kept)
        graded = scoring.score_retrieval({"gold": {"chunks": [dropped], "records": [], "paths": []}},
                                         on["artifact"])
        assert (graded["passed"], graded["first_gold_rank"]) == (True, rank)

    asyncio.run(check())


def test_runner_checks_integrity_before_calling_the_embedding_service(paired_default):
    from dataclasses import replace

    from sqlalchemy import text

    from evals.retrieval import evaluate_retrieval
    from login_investigator.knowledge_base import GraphIntegrityError, database_engine

    class MustNotQuery(FakeEmbedder):
        def embed_query(self, text: str) -> list[float]:
            raise AssertionError("A corrupt pair must stop before retrieval")

    async def check():
        server = ServerSettings.from_env()
        engine = database_engine(replace(server, database=paired_default.database))
        try:
            async with open_version(paired_default.marker, server, embedder=MustNotQuery()) as kb:
                try:
                    async with engine.begin() as connection:
                        await connection.execute(text("UPDATE people SET department='wrong' WHERE person_id='user-amelia.ward'"))
                    with pytest.raises(GraphIntegrityError):
                        await evaluate_retrieval(kb, [{'id': 'test', 'type': 'document_lookup', 'turns': ['MFA']}])
                finally:
                    async with engine.begin() as connection:
                        await connection.execute(text("UPDATE people SET department='IT' WHERE person_id='user-amelia.ward'"))
        finally:
            await engine.dispose()
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


def test_retrieval_command_preserves_the_safe_staleness_instruction(tmp_path, monkeypatch, capsys):
    from evals import run
    from login_investigator.knowledge_base.staleness import PAIR_UNCHECKABLE

    state = tmp_path / 'active.json'
    state.write_text(json.dumps({'format': 'paired-v1', 'current': str(tmp_path / 'missing.json'), 'previous': None}))
    monkeypatch.setenv('LI_KNOWLEDGE_BASE_STATE', str(state))
    monkeypatch.setattr(sys, 'argv', ['evals.run', '--layer', 'retrieval'])
    with pytest.raises(SystemExit) as caught:
        run.main()
    assert caught.value.code == 2
    assert PAIR_UNCHECKABLE in capsys.readouterr().err
