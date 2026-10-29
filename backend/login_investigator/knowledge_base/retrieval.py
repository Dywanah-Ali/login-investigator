"""Hybrid corpus retrieval. Ranks order evidence; they do not establish relevance."""

from collections.abc import Sequence
from dataclasses import dataclass, replace
from datetime import date
import math
from typing import Any, Literal

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_postgres import PGEngine, PGVectorStore
from langchain_postgres.v2.hybrid_search_config import HybridSearchConfig
from sqlalchemy.engine import RowMapping
from sqlalchemy.ext.asyncio import AsyncEngine

from . import schema
from .chunking import Chunk
from .reranking import Reranker

LIMIT = 20
RRF_K = 60


@dataclass(frozen=True)
class SearchFilters:
    document_type: str | None = None
    technique_id: str | None = None
    incident_id: str | None = None
    version: str | None = None
    effective_date: date | None = None

    def as_store_filter(self) -> dict[str, Any]:
        return {name: getattr(self, name) for name in schema.FILTER_COLUMNS
                if getattr(self, name) is not None}


@dataclass(frozen=True)
class Candidate:
    chunk: Chunk
    dense_rank: int | None
    keyword_rank: int | None
    cosine_distance: float | None
    keyword_score: float | None
    fused_score: float
    rerank_score: float | None = None


@dataclass(frozen=True)
class SearchResult:
    chunks: list[Candidate]
    candidates: list[Candidate]
    verdict: Literal["none", "weak", "found"]
    reason: str


@dataclass(frozen=True)
class VerdictPolicy:
    """No live cutoff until T39. Explicit cutoffs allow the switch to be tested offline.

    Each score source has its own threshold: a cosine cutoff never judges re-ranked chunks.
    """
    min_similarity: float | None = None
    min_relevance: float | None = None
    none_enabled: bool = False

    def __post_init__(self) -> None:
        if self.none_enabled and self.min_similarity is None and self.min_relevance is None:
            raise ValueError("The none rule requires a calibrated threshold")
        if self.min_similarity is not None and (
            not math.isfinite(self.min_similarity) or not -1 <= self.min_similarity <= 1
        ):
            raise ValueError("Cosine similarity threshold must be finite and between -1 and 1")
        if self.min_relevance is not None and (
            not math.isfinite(self.min_relevance) or not 0 <= self.min_relevance <= 1
        ):
            raise ValueError("Re-ranker relevance threshold must be finite and between 0 and 1")

    def evaluate(self, chunks: list[Candidate], reranked: bool) -> tuple[Literal["none", "weak", "found"], str]:
        # Author's T23 ruling: zero passages is a counted fact and needs no threshold.
        if not chunks:
            return "none", "empty_result"
        threshold = self.min_relevance if reranked else self.min_similarity
        if threshold is None:
            return "weak", "not_calibrated"
        supported = sum(score is not None and score >= threshold
                        for score in (_score(c, reranked) for c in chunks))
        if supported == 0 and self.none_enabled:
            return "none", "below_threshold"
        if supported >= 2:
            return "found", "multiple_chunks_above_threshold"
        return "weak", "single_chunk_above_threshold" if supported else "none_rule_disabled"


def _score(candidate: Candidate, reranked: bool) -> float | None:
    if reranked:
        return candidate.rerank_score
    return None if candidate.cosine_distance is None else 1 - candidate.cosine_distance


async def search_corpus(engine: AsyncEngine, embedder: Embeddings, query: str,
                        filters: SearchFilters | None = None,
                        verdict_policy: VerdictPolicy | None = None,
                        reranker: Reranker | None = None) -> SearchResult:
    if not query.strip():
        raise ValueError("A corpus search needs a non-empty question")
    candidates: list[Candidate] = []

    def fuse(primary: Sequence[RowMapping], secondary: Sequence[RowMapping],
             fetch_top_k: int = LIMIT, **kwargs: Any) -> list[dict[str, Any]]:
        # Break equal scores by stable chunk ID. Keep raw scores before replacing distance.
        dense = sorted(primary, key=lambda row: (row["distance"], row["chunk_id"]))
        keyword = sorted(secondary, key=lambda row: (-row["distance"], row["chunk_id"]))
        dense_by_id = {row["chunk_id"]: (rank, row["distance"]) for rank, row in enumerate(dense, 1)}
        keyword_by_id = {row["chunk_id"]: (rank, row["distance"]) for rank, row in enumerate(keyword, 1)}
        rows = {row["chunk_id"]: dict(row) for row in [*dense, *keyword]}
        for chunk_id, row in rows.items():
            dense_rank, distance = dense_by_id.get(chunk_id, (None, None))
            keyword_rank, score = keyword_by_id.get(chunk_id, (None, None))
            fused = sum(1 / (RRF_K + rank) for rank in (dense_rank, keyword_rank) if rank is not None)
            chunk = Chunk(chunk_id, row["content"], {
                **(row["langchain_metadata"] or {}), **{key: row[key] for key in schema.FILTER_COLUMNS},
            })
            candidates.append(Candidate(chunk, dense_rank, keyword_rank, distance, score, fused))
            row["distance"] = fused
        candidates.sort(key=lambda candidate: (-candidate.fused_score, candidate.chunk.id))
        return [rows[candidate.chunk.id] for candidate in candidates[:fetch_top_k]]

    # The library mutates fts_query and fusion parameters. Never share a config across calls.
    hybrid = HybridSearchConfig(
        tsv_column="content_tsv", tsv_lang="pg_catalog.english", fusion_function=fuse,
        primary_top_k=LIMIT, secondary_top_k=LIMIT,
    )
    store = await PGVectorStore.create(
        PGEngine.from_engine(engine), embedder, "chunks", id_column="chunk_id",
        metadata_columns=schema.FILTER_COLUMNS, hybrid_search_config=hybrid,
    )
    await store.asimilarity_search(query, k=LIMIT, hybrid_search_config=hybrid,
                                  filter=filters.as_store_filter() if filters else None)
    chunks = candidates[:LIMIT]
    if reranker is not None:
        ranking = await reranker.arank([Document(c.chunk.text, id=c.chunk.id) for c in chunks], query)
        candidates[:LIMIT] = [replace(c, rerank_score=s) for c, s in zip(chunks, ranking.scores)]
        chunks = [candidates[index] for index in ranking.kept]
    verdict, reason = (verdict_policy or VerdictPolicy()).evaluate(chunks, reranked=reranker is not None)
    return SearchResult(chunks, candidates, verdict, reason)
