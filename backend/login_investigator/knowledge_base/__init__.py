"""Door 2: build a dataset's knowledge base, open it, and read named records.

The build and LangChain store share one SQLAlchemy async engine on psycopg. Readers open a
separate engine. Nothing here imports the API, the agent or the screen.
"""

import math
import time
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import AsyncExitStack, asynccontextmanager
from dataclasses import dataclass, replace
from pathlib import Path

import pandas as pd
import tiktoken
from langchain_core.embeddings import Embeddings
from langchain_postgres import PGEngine, PGVectorStore
from langchain_postgres.v2.engine import Column as PGColumn
from langchain_postgres.v2.hybrid_search_config import HybridSearchConfig
from sqlalchemy import URL, func, select, text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from login_investigator.corpus_check import read_table
from login_investigator.generator import REPO_ROOT
from login_investigator.postgres import (
    ServerSettings,
)
from login_investigator.rules import Finding

from . import chunking as chunking
from . import schema as schema
from .access import check_reader_role, grant_read_only
from .access import reader_settings as reader_settings
from .chunking import Chunk, read_chunks
from .graph_queries import GraphQueries
from .integrity import GraphCounts
from .integrity import GraphIntegrityError as GraphIntegrityError
from .mentions import find_mentions
from .radius import FindingRadius, GraphWalk
from .reranking import Reranker as Reranker
from .reranking import RerankerUnavailable as RerankerUnavailable
from .retrieval import SearchFilters as SearchFilters
from .retrieval import SearchResult, search_corpus
from .retrieval import VerdictPolicy as VerdictPolicy
from .staleness import (
    NOT_BUILT as NOT_BUILT,
)
from .staleness import (
    STALE,
    UNCHECKABLE,
    source_fingerprint,
)
from .staleness import (
    KnowledgeBaseNotReady as KnowledgeBaseNotReady,
)

# Where the build command publishes its pointer and the app's startup reads it. Git-ignored.
STATE_FILE = REPO_ROOT / ".knowledge-base.json"


@dataclass(frozen=True)
class BuildReport:
    database: str
    documents: int
    chunks: int
    organisation_rows: dict[str, int]
    mentions: int
    vector_dimensions: list[int]
    keyword_index: bool
    keyword_parser: dict[str, list[dict[str, object]]]
    input_tokens: int
    elapsed_seconds: float = 0


def database_engine(settings: ServerSettings, *, bounded: bool = False) -> AsyncEngine:
    return create_async_engine(URL.create(
        "postgresql+psycopg", username=settings.user, password=settings.password,
        host=settings.host, port=settings.port, database=settings.database,
    ), hide_parameters=True, pool_timeout=5 if bounded else 30,
        connect_args=({'connect_timeout': 5, 'options': '-c statement_timeout=10000 -c lock_timeout=5000'}
                      if bounded else {}))


class KnowledgeBase:
    def __init__(self, engine: AsyncEngine, embedder: Embeddings | None = None,
                 reranker: Reranker | None = None):
        self.engine = engine
        self._embedder = embedder
        self._reranker = reranker
        self._graph_queries: GraphQueries | None = None
        self._dataset: Path | None = None
        self._log: pd.DataFrame | None = None
        self._graph_verifier: Callable[[], Awaitable[GraphCounts]] | None = None
        self.build_id: str | None = None
        self.offline_embeddings = False

    @property
    def source_snapshot(self) -> Path | None:
        """The selected source world; callers must not fall back to working inputs."""
        return self._dataset

    async def search_corpus(self, query: str, *, filters: SearchFilters | None = None,
                            verdict_policy: VerdictPolicy | None = None) -> SearchResult:
        if self._embedder is None:
            raise ValueError("Open the knowledge base with an embedder to search the corpus")
        return await search_corpus(self.engine, self._embedder, query, filters, verdict_policy, self._reranker)

    async def check_graph_integrity(self) -> GraphCounts:
        if self._graph_verifier is None:
            raise ValueError("Open a complete paired version to check the graph")
        return await self._graph_verifier()

    @property
    def graph_queries(self) -> GraphQueries:
        if self._graph_queries is None:
            raise ValueError("Open a complete paired version to use the graph")
        return self._graph_queries

    def finding_radius(self, finding: Finding, start: str | None = None, end: str | None = None) -> FindingRadius:
        return self.graph_queries.finding_radius(finding, start, end)

    def account_groups(self, username: str) -> GraphWalk:
        return self.graph_queries.account_groups(username)

    def lookup_account(self, account_id: str) -> dict[str, object]:
        return self.graph_queries.lookup_account(account_id)

    def finding_walk(self, finding_id: str) -> GraphWalk:
        return self.graph_queries.finding_walk(finding_id)

    async def organisation_records(self, name: str) -> list[dict[str, object]]:
        table = schema.ORG_TABLES[name]
        async with self.engine.connect() as connection:
            rows = await connection.execute(select(table).order_by(*table.primary_key))
            return [dict(row) for row in rows.mappings()]

    async def chunks(self) -> list[Chunk]:
        async with self.engine.connect() as connection:
            rows = await connection.execute(select(schema.chunks).order_by(schema.chunks.c.chunk_id))
            return [Chunk(row["chunk_id"], row["content"], {
                **row["langchain_metadata"], **{key: row[key] for key in schema.FILTER_COLUMNS},
            }) for row in rows.mappings()]

    async def mentions(self) -> list[dict[str, str]]:
        async with self.engine.connect() as connection:
            rows = await connection.execute(select(schema.mentions).order_by(*schema.mentions.primary_key))
            return [dict(row) for row in rows.mappings()]

    async def recorded_fingerprints(self) -> list[str]:
        """The build writes exactly one. Any other count means the record cannot be trusted."""
        async with self.engine.connect() as connection:
            return list((await connection.scalars(select(schema.build_record.c.fingerprint))).all())

    async def describe(self, database: str) -> BuildReport:
        """Read build evidence from storage, including PostgreSQL's actual identifier parsing."""
        async with self.engine.connect() as connection:
            counts = {name: int((await connection.scalar(select(func.count()).select_from(table))) or 0)
                      for name, table in schema.ORG_TABLES.items()}
            chunks = await self.chunks()
            dimensions = list((await connection.scalars(
                select(func.vector_dims(schema.chunks.c.embedding)).distinct())).all())
            index = await connection.scalar(text("""SELECT EXISTS (
                SELECT 1 FROM pg_indexes WHERE schemaname = 'public' AND tablename = 'chunks'
                AND indexdef LIKE '%USING gin (content_tsv)%')"""))
            parser: dict[str, list[dict[str, object]]] = {}
            for identifier in ("T1110.003", "LT-DHUGHES", "203.0.113.10", "thomas.price@corp.example"):
                rows = await connection.execute(text("""
                    SELECT alias, token, lexemes FROM ts_debug('pg_catalog.english', :identifier)
                """), {"identifier": identifier})
                parser[identifier] = [dict(row) for row in rows.mappings()]
            mentions = int((await connection.scalar(select(func.count()).select_from(schema.mentions))) or 0)
        encoding = tiktoken.get_encoding("cl100k_base")
        return BuildReport(database, len({chunk.metadata["id"] for chunk in chunks}), len(chunks),
                           counts, mentions, dimensions, bool(index), parser,
                           sum(len(encoding.encode(chunk.text)) for chunk in chunks))


@asynccontextmanager
async def open_knowledge_base(
    settings: ServerSettings, *, dataset: Path | None = None, embedder: Embeddings | None = None,
    reranker: Reranker | None = None,
) -> AsyncIterator[KnowledgeBase]:
    """Open passage storage for building/search tests. Application graphs require a complete pair."""
    engine = database_engine(settings)
    try:
        kb = KnowledgeBase(engine, embedder, reranker)
        if dataset is not None:
            fingerprints = await kb.recorded_fingerprints()
            if len(fingerprints) != 1:
                raise KnowledgeBaseNotReady(UNCHECKABLE)
            if fingerprints[0] != source_fingerprint(dataset):
                raise KnowledgeBaseNotReady(STALE)
            kb._dataset = dataset
        yield kb
    finally:
        await engine.dispose()


async def build_knowledge_base(
    dataset: Path, database: ServerSettings, embedder: Embeddings,
    *, reader_role: str = "li_reader",
) -> BuildReport:
    """Load an empty database supplied by the command or the real PostgreSQL test fixture."""
    started = time.monotonic()
    # Taken before any file is read. A file edited mid-build then leaves a database whose record
    # no longer matches the folder, so the guard refuses it: the safe direction.
    fingerprint = source_fingerprint(dataset)
    chunks = read_chunks(dataset)
    engine = database_engine(database)
    pg = PGEngine.from_engine(engine)
    try:
        await check_reader_role(engine, reader_role)
        async with engine.begin() as connection:
            await connection.run_sync(lambda conn: schema.metadata.create_all(
                conn, tables=list(schema.ORG_TABLES.values())))
            for name, table in schema.ORG_TABLES.items():
                rows = [{key: value or None for key, value in row.items()}
                        for row in read_table(dataset, name)]
                if rows:
                    await connection.execute(table.insert(), rows)
        hybrid = HybridSearchConfig(tsv_column="content_tsv", tsv_lang="pg_catalog.english")
        await pg.ainit_vectorstore_table(
            "chunks", schema.VECTOR_SIZE, id_column=PGColumn("chunk_id", "TEXT"),
            metadata_columns=[PGColumn(name, "DATE" if name == "effective_date" else "TEXT")
                              for name in schema.FILTER_COLUMNS], hybrid_search_config=hybrid,
        )
        store = await PGVectorStore.create(
            pg, embedder, "chunks", id_column="chunk_id",
            metadata_columns=schema.FILTER_COLUMNS, hybrid_search_config=hybrid,
        )
        texts = [chunk.text for chunk in chunks]
        vectors = await embedder.aembed_documents(texts)
        if (len(vectors) != len(chunks) or any(
            len(vector) != schema.VECTOR_SIZE or not all(math.isfinite(value) for value in vector)
            for vector in vectors
        )):
            raise ValueError(f"Embedding response must contain one finite {schema.VECTOR_SIZE}-dimensional vector per passage")
        await store.aadd_embeddings(texts, vectors, metadatas=[chunk.metadata for chunk in chunks],
                                    ids=[chunk.id for chunk in chunks])
        await store.aapply_hybrid_search_index()
        async with engine.begin() as connection:
            await connection.run_sync(lambda conn: schema.mentions.create(conn))
            links = find_mentions(dataset, chunks)
            if links:
                await connection.execute(schema.mentions.insert(), links)
            # Written last, so only a database whose every step succeeded carries a record.
            await connection.run_sync(lambda conn: schema.build_record.create(conn))
            await connection.execute(schema.build_record.insert(), {"fingerprint": fingerprint})
        await grant_read_only(engine, database.database, reader_role)
        report = await KnowledgeBase(engine).describe(database.database)
        return replace(report, elapsed_seconds=round(time.monotonic() - started, 3))
    finally:
        await engine.dispose()


@asynccontextmanager
async def open_current_knowledge_base(
    dataset: Path, state_file: Path, *, embedder: Embeddings | None = None,
    reranker: Reranker | None = None, server: ServerSettings | None = None,
) -> AsyncIterator[KnowledgeBase | None]:
    """Own one checked pair for the application lifetime; no selection needs no database."""
    if not state_file.exists():
        yield None
        return
    from .graph_selection import read_selection
    from .graph_version import open_version
    from .staleness import PAIR_UNCHECKABLE

    async with AsyncExitStack() as cleanup:
        try:
            selected = read_selection(state_file)
            kb = await cleanup.enter_async_context(
                open_version(Path(selected['current']), server or ServerSettings.from_env(),
                             embedder=embedder, reranker=reranker))
        except Exception:  # noqa: BLE001 - Refuse startup with a fixed, credential-safe error.
            raise KnowledgeBaseNotReady(PAIR_UNCHECKABLE) from None
        yield kb
