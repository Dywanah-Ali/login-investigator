"""Door 2: hybrid search through the knowledge-base interface, with real PostgreSQL."""

import asyncio
import math
import shutil
from pathlib import Path

import pytest
from langchain_core.embeddings import Embeddings
from pydantic import Field

from login_investigator.knowledge_base import Reranker, build_knowledge_base, open_knowledge_base, reader_settings
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


class NumberReranker(Reranker):
    """Higher document numbers score higher, so the kept five differ from the fused order."""
    calls: list[list[str]] = Field(default_factory=list)

    async def ascore(self, query: str, texts: list[str]) -> list[float]:
        self.calls.append(texts)
        return [int(content.split("Document ")[1][:2]) / 100 for content in texts]


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
        dataset = search_dataset(tmp_path, 46)
        # This one passage loses to 25 nearer vectors and many keyword matches unless filtering
        # takes place before each leg's limit. An exact version restricts both legs to it.
        for number in range(25, 45):
            path = dataset / f"corpus/own/doc-{number:02}.md"
            path.write_text(path.read_text().replace("zebra approval", "zebra zebra zebra approval"))
        path = dataset / "corpus/own/doc-45.md"
        path.write_text(path.read_text().replace('version: "1.0"', 'version: "2.0"'))
        await build_knowledge_base(dataset, build_database, embedder)
        async with open_knowledge_base(reader_settings(build_database), embedder=embedder) as kb:
            unfiltered = await kb.search_corpus("zebra")
            assert not any(c.chunk.id == "doc-45@2.0#document-45/1" for c in unfiltered.candidates)
            result = await kb.search_corpus("zebra", filters=SearchFilters(document_type="policy", version="2.0"))
        assert len(result.chunks) == 1
        assert result.chunks[0].chunk.id == "doc-45@2.0#document-45/1"
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
        reranker = NumberReranker()
        async with open_knowledge_base(reader_settings(build_database), embedder=embedder,
                                       reranker=reranker) as kb:
            empty_reranked = await kb.search_corpus("orchard", filters=SearchFilters(version="missing"))
        assert found.verdict == "found"
        assert weak.verdict == disabled.verdict == "weak"
        assert enabled.verdict == "none"
        assert enabled.chunks == disabled.chunks  # closest misses remain available
        # Author's T23 ruling: zero passages is a counted fact, so the empty-result rule needs no
        # threshold and applies with the re-ranker off (the fallback) and on.
        assert (empty.verdict, empty.reason, empty.chunks) == ("none", "empty_result", [])
        assert (empty_reranked.verdict, empty_reranked.reason) == ("none", "empty_result")
        assert reranker.calls == []
        with pytest.raises(ValueError, match="calibrat"):
            VerdictPolicy(none_enabled=True)

    asyncio.run(check())


def test_reranker_scores_the_fused_twenty_and_search_keeps_its_best_five(
    build_database: ServerSettings, tmp_path: Path,
):
    async def check():
        embedder, reranker = RankedEmbedder(), NumberReranker()
        await build_knowledge_base(search_dataset(tmp_path, 45), build_database, embedder)
        async with open_knowledge_base(reader_settings(build_database), embedder=embedder,
                                       reranker=reranker) as kb:
            result = await kb.search_corpus("zebra")
        # Fused 20: documents 0-9 lead the vector leg, 25-34 lead the keyword leg.
        assert [c.chunk.id for c in result.chunks] == [
            f"doc-{n}@1.0#document-{n}/1" for n in (34, 33, 32, 31, 30)]
        assert [len(texts) for texts in reranker.calls] == [20]
        assert all(c.rerank_score is not None for c in result.candidates[:20])
        assert all(c.rerank_score is None for c in result.candidates[20:])
        fused = [c.fused_score for c in result.candidates]
        assert fused == sorted(fused, reverse=True)  # candidates keep their fused order
        assert result.verdict == "weak" and result.reason == "not_calibrated"

    asyncio.run(check())


def test_with_the_reranker_on_its_score_drives_the_verdict(build_database: ServerSettings, tmp_path: Path):
    from login_investigator.knowledge_base import VerdictPolicy

    async def check():
        embedder = RankedEmbedder()
        await build_knowledge_base(search_dataset(tmp_path, 45), build_database, embedder)
        async with open_knowledge_base(reader_settings(build_database), embedder=embedder,
                                       reranker=NumberReranker()) as kb:
            # The kept five score 0.34, 0.33, 0.32, 0.31 and 0.30.
            found = await kb.search_corpus("zebra", verdict_policy=VerdictPolicy(min_relevance=0.33))
            weak = await kb.search_corpus("zebra", verdict_policy=VerdictPolicy(min_relevance=0.34))
            refused = await kb.search_corpus("zebra", verdict_policy=VerdictPolicy(
                min_relevance=0.35, none_enabled=True))
            # A cosine threshold every passage meets must not stand in for an uncalibrated re-ranker.
            cosine_only = await kb.search_corpus("zebra", verdict_policy=VerdictPolicy(min_similarity=-1.0))
        assert (found.verdict, found.reason) == ("found", "multiple_chunks_above_threshold")
        assert (weak.verdict, weak.reason) == ("weak", "single_chunk_above_threshold")
        assert (refused.verdict, refused.reason) == ("none", "below_threshold")
        assert len(refused.chunks) == 5  # closest misses remain available
        assert (cosine_only.verdict, cosine_only.reason) == ("weak", "not_calibrated")
        for bad in (1.5, -0.1, math.nan):
            with pytest.raises(ValueError, match="between 0 and 1"):
                VerdictPolicy(min_relevance=bad)

    asyncio.run(check())


@pytest.mark.parametrize("scores", [[0.5], [math.nan] * 3, [math.inf] * 3])
def test_a_reranker_reply_that_does_not_score_every_candidate_stops_the_search(
    build_database: ServerSettings, tmp_path: Path, scores: list[float],
):
    class BrokenReranker(Reranker):
        async def ascore(self, query: str, texts: list[str]) -> list[float]:
            return scores

    async def check():
        embedder = RankedEmbedder()
        await build_knowledge_base(search_dataset(tmp_path, 3), build_database, embedder)
        async with open_knowledge_base(reader_settings(build_database), embedder=embedder,
                                       reranker=BrokenReranker()) as kb:
            with pytest.raises(ValueError, match="one finite score per candidate"):
                await kb.search_corpus("orchard")

    asyncio.run(check())


def test_the_compressor_slot_keeps_the_best_five_of_twenty_with_their_scores():
    from langchain_core.documents import Document

    documents = [Document(f"Document {n:02}", id=f"chunk-{n:02}") for n in range(20)]
    kept = asyncio.run(NumberReranker().acompress_documents(documents, "question"))
    assert [d.id for d in kept] == ["chunk-19", "chunk-18", "chunk-17", "chunk-16", "chunk-15"]
    assert [d.metadata["relevance_score"] for d in kept] == [0.19, 0.18, 0.17, 0.16, 0.15]
