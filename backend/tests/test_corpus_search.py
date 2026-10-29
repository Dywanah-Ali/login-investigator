"""Door 2: hybrid search through the knowledge-base interface, with real PostgreSQL."""

import asyncio
import math
import shutil
from pathlib import Path

import pytest
from langchain_core.embeddings import Embeddings

from login_investigator.knowledge_base import build_knowledge_base, open_knowledge_base, reader_settings
from login_investigator.postgres import ServerSettings
from test_knowledge_base import DATASET, build_database  # noqa: F401


class RankedEmbedder(Embeddings):
    """Document number fixes semantic distance independently of keyword matches."""

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        vectors = []
        for content in texts:
            number = int(content.split("Document ")[1][:2])
            angle = (number + 1) / 50
            vectors.append([math.cos(angle), math.sin(angle)] + [0.0] * 1534)
        return vectors

    def embed_query(self, text: str) -> list[float]:
        return [1.0] + [0.0] * 1535


def search_dataset(path: Path, count: int) -> Path:
    shutil.copytree(DATASET / "org", path / "org")
    own = path / "corpus/own"
    own.mkdir(parents=True)
    for number in range(count):
        keyword = "zebra" if number >= 25 else "orchard"
        kind = "policy" if number >= 25 else "guidance"
        (own / f"doc-{number:02}.md").write_text(
            f'---\nid: "doc-{number:02}"\ntitle: "Document {number:02}"\n'
            f'kind: "{kind}"\nversion: "1.0"\ndate: "2026-09-01"\n---\n'
            f'# Document {number:02}\n\n{keyword} approval.\n', encoding="utf-8",
        )
    return path


def test_search_combines_ranks_and_keeps_raw_scores(build_database: ServerSettings, tmp_path: Path):
    async def check():
        embedder = RankedEmbedder()
        await build_knowledge_base(search_dataset(tmp_path, 3), build_database, embedder)
        async with open_knowledge_base(reader_settings(build_database), embedder=embedder) as kb:
            result = await kb.search_corpus("orchard")
        assert len(result.chunks) == 3
        first = result.chunks[0]
        assert first.chunk.id == "doc-00@1.0#document-00/1"
        assert first.dense_rank == first.keyword_rank == 1
        assert first.cosine_distance == pytest.approx(0.0001999933, abs=1e-7)
        assert first.keyword_score is not None and first.keyword_score > 0
        assert first.fused_score == pytest.approx(0.03278688524590164)
        assert result.verdict == "weak"
        assert result.reason == "not_calibrated"

    asyncio.run(check())


def test_both_legs_supply_twenty_and_the_second_question_has_fresh_keywords(
    build_database: ServerSettings, tmp_path: Path,
):
    async def check():
        embedder = RankedEmbedder()
        await build_knowledge_base(search_dataset(tmp_path, 45), build_database, embedder)
        async with open_knowledge_base(reader_settings(build_database), embedder=embedder) as kb:
            first = await kb.search_corpus("zebra")
            second = await kb.search_corpus("orchard")
        assert len(first.chunks) == 20
        assert len(first.candidates) == 40
        assert {c.dense_rank for c in first.candidates if c.dense_rank} == set(range(1, 21))
        assert {c.keyword_rank for c in first.candidates if c.keyword_rank} == set(range(1, 21))
        assert all("zebra" in c.chunk.text for c in first.candidates if c.keyword_rank)
        assert all("orchard" in c.chunk.text for c in second.candidates if c.keyword_rank)
        assert any(c.keyword_rank for c in second.candidates)
        assert all(c.cosine_distance is None for c in first.candidates if c.dense_rank is None)
        assert all(c.keyword_score is None for c in first.candidates if c.keyword_rank is None)

    asyncio.run(check())


def test_filters_narrow_both_legs_before_their_limits(build_database: ServerSettings, tmp_path: Path):
    from login_investigator.knowledge_base.retrieval import SearchFilters

    async def check():
        embedder = RankedEmbedder()
        dataset = search_dataset(tmp_path, 45)
        # This one passage loses to 25 nearer vectors and many keyword matches unless filtering
        # takes place before each leg's limit. An exact version restricts both legs to it.
        path = dataset / "corpus/own/doc-44.md"
        path.write_text(path.read_text().replace('version: "1.0"', 'version: "2.0"'))
        await build_knowledge_base(dataset, build_database, embedder)
        async with open_knowledge_base(reader_settings(build_database), embedder=embedder) as kb:
            result = await kb.search_corpus("zebra", filters=SearchFilters(document_type="policy", version="2.0"))
        assert len(result.chunks) == 1
        assert result.chunks[0].chunk.id == "doc-44@2.0#document-44/1"
        assert result.chunks[0].dense_rank == result.chunks[0].keyword_rank == 1

    asyncio.run(check())


def test_verdict_uses_recorded_scores_and_none_requires_an_enabled_calibrated_rule(
    build_database: ServerSettings, tmp_path: Path,
):
    from login_investigator.knowledge_base import SearchFilters, VerdictPolicy

    async def check():
        embedder = RankedEmbedder()
        await build_knowledge_base(search_dataset(tmp_path, 3), build_database, embedder)
        async with open_knowledge_base(reader_settings(build_database), embedder=embedder) as kb:
            found = await kb.search_corpus("orchard", verdict_policy=VerdictPolicy(min_similarity=0.999))
            weak = await kb.search_corpus("orchard", verdict_policy=VerdictPolicy(min_similarity=0.9995))
            disabled = await kb.search_corpus("orchard", verdict_policy=VerdictPolicy(min_similarity=1.0))
            enabled = await kb.search_corpus("orchard", verdict_policy=VerdictPolicy(min_similarity=1.0, none_enabled=True))
            empty = await kb.search_corpus("orchard", filters=SearchFilters(version="missing"))
        assert found.verdict == "found"
        assert weak.verdict == disabled.verdict == empty.verdict == "weak"
        assert enabled.verdict == "none"
        assert enabled.chunks == disabled.chunks  # closest misses remain available
        assert empty.chunks == [] and empty.reason == "not_calibrated"
        with pytest.raises(ValueError, match="calibrat"):
            VerdictPolicy(none_enabled=True)

    asyncio.run(check())
