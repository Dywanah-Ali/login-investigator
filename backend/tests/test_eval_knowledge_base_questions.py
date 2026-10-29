"""The knowledge base's question file: every question is answerable and checkable before any search
runs (ticket 21). Gold IDs that name nothing would make the exam fail, or pass, for the wrong reason.
"""

import asyncio
import csv
import json
from pathlib import Path

from login_investigator.generator import DATASET_DIR
from login_investigator.knowledge_base import build_knowledge_base, open_knowledge_base
from login_investigator.postgres import ServerSettings
from test_knowledge_base import FakeEmbedder, build_database  # noqa: F401

QUESTIONS_PATH = Path(__file__).resolve().parents[1] / "evals" / "knowledge_base_questions.json"
QUESTIONS = json.loads(QUESTIONS_PATH.read_text(encoding="utf-8"))["questions"]
QUESTION_TYPES = {"document_lookup", "graph_lookup", "mixed", "absent_topic", "twin"}
TRUTH = json.loads((DATASET_DIR / "truth.json").read_text(encoding="utf-8"))


def world_record_ids() -> set[str]:
    """Every record ID the world's files define: the first column of each organisation table."""
    ids: set[str] = set()
    for table in (DATASET_DIR / "org").glob("*.csv"):
        with table.open(encoding="utf-8", newline="") as handle:
            ids.update(next(iter(row.values())) for row in csv.DictReader(handle))
    return ids


def document_of(chunk_id: str) -> str:
    """The document a chunk comes from: chunk IDs read `<document>@<version>#<section>/<n>`."""
    return chunk_id.split("@")[0]


def s6_questions() -> list[dict]:
    return [question for question in QUESTIONS if question["type"] == "mixed" and "S6" in question["provenance"]]


def test_every_question_has_its_fields_and_something_to_check():
    assert 6 <= len(QUESTIONS) <= 10
    assert len({question["id"] for question in QUESTIONS}) == len(QUESTIONS)
    for question in QUESTIONS:
        assert question["type"] in QUESTION_TYPES, question["id"]
        assert question["split"] in {"test", "tune"}, question["id"]
        assert question["provenance"].strip(), question["id"]
        assert question["turns"] and all(turn.strip() for turn in question["turns"]), question["id"]
        gold = question["gold"]
        assert set(gold) == {"chunks", "records", "paths"}, question["id"]
        assert any(gold.values()) or question.get("verdict"), question["id"]


def test_the_first_questions_cover_each_kind_the_ticket_names():
    assert {question["type"] for question in QUESTIONS} == QUESTION_TYPES
    assert s6_questions()


def test_an_absent_topic_expects_none_and_carries_no_gold():
    for question in QUESTIONS:
        if question["type"] == "absent_topic":
            assert question["verdict"] == "none", question["id"]
            assert not any(question["gold"].values()), question["id"]


def test_every_gold_record_and_path_step_exists_in_the_world():
    known = world_record_ids()
    assert len(known) > 50  # the eight tables were read, not an empty folder
    for question in QUESTIONS:
        gold = question["gold"]
        assert set(gold["records"]) <= known, question["id"]
        for path in gold["paths"]:
            assert set(path) <= known, (question["id"], path)
            assert path[-1] in gold["records"], (question["id"], path)


def test_the_s6_question_carries_the_planted_radius():
    radius = TRUTH["scenarios"]["S6"]["blast_radius"]
    [s6] = s6_questions()
    assert sorted(s6["gold"]["records"]) == sorted(radius["groups"] + radius["assets"] + radius["device_peers"])
    assert sorted(s6["gold"]["paths"]) == sorted(radius["paths"])
    assert {document_of(chunk) for chunk in s6["gold"]["chunks"]} <= set(
        TRUTH["scenarios"]["S6"]["expected_document_ids"])


def test_a_twin_expects_benign_and_cites_its_clearing_document():
    twins = TRUTH["twins"].values()
    for question in [q for q in QUESTIONS if q["type"] == "twin"]:
        [twin] = [t for t in twins if t["user"] in question["turns"][-1]]
        assert question["conclusion"] == twin["verdict"] == "benign", question["id"]
        assert question["gold"]["chunks"], question["id"]
        assert {document_of(chunk) for chunk in question["gold"]["chunks"]} == {twin["clearing_document_id"]}


def test_every_gold_chunk_exists_in_a_fresh_build_of_the_world(build_database: ServerSettings):
    gold = {chunk for question in QUESTIONS for chunk in question["gold"]["chunks"]}

    async def built_chunk_ids() -> set[str]:
        await build_knowledge_base(DATASET_DIR, build_database, FakeEmbedder())
        async with open_knowledge_base(build_database) as kb:
            return {chunk.id for chunk in await kb.chunks()}

    assert gold
    assert gold - asyncio.run(built_chunk_ids()) == set()
