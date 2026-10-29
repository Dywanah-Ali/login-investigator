"""Hybrid corpus retrieval. Ranks order evidence; they do not establish relevance."""

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date
import math
from typing import Any, Literal

from langchain_core.embeddings import Embeddings
from langchain_postgres import PGEngine, PGVectorStore
from langchain_postgres.v2.hybrid_search_config import HybridSearchConfig
from sqlalchemy.engine import RowMapping
from sqlalchemy.ext.asyncio import AsyncEngine

from . import schema
from .chunking import Chunk

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


@dataclass(frozen=True)
class SearchResult:
    chunks: list[Candidate]
    candidates: list[Candidate]
    verdict: Literal["none", "weak", "found"]
    reason: str


@dataclass(frozen=True)
class VerdictPolicy:
    """No live cutoff until T39. Explicit cutoffs allow the switch to be tested offline."""
    min_similarity: float | None = None
    none_enabled: bool = False

    def __post_init__(self) -> None:
        if self.none_enabled and self.min_similarity is None:
            raise ValueError("The none rule requires a calibrated threshold")
        if self.min_similarity is not None and (
            not math.isfinite(self.min_similarity) or not -1 <= self.min_similarity <= 1
        ):
            raise ValueError("Cosine similarity threshold must be finite and between -1 and 1")

    def evaluate(self, chunks: list[Candidate]) -> tuple[Literal["none", "weak", "found"], str]:
        if self.min_similarity is None:
            return "weak", "not_calibrated"
        supported = sum(c.cosine_distance is not None and 1 - c.cosine_distance >= self.min_similarity
                        for c in chunks)
        if supported == 0 and self.none_enabled:
            return "none", "below_threshold" if chunks else "empty_result"
        if supported >= 2:
            return "found", "multiple_chunks_above_threshold"
        return "weak", "single_chunk_above_threshold" if supported else "none_rule_disabled"


async def search_corpus(engine: AsyncEngine, embedder: Embeddings, query: str,
                        filters: SearchFilters | None = None,
                        verdict_policy: VerdictPolicy | None = None) -> SearchResult:
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
    verdict, reason = (verdict_policy or VerdictPolicy()).evaluate(chunks)
    return SearchResult(chunks, candidates, verdict, reason)
