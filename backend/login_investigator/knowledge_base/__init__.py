"""Door 2: build a dataset's knowledge base, open it, and read named records.

The build and LangChain store share one SQLAlchemy async engine on psycopg. Readers open a
separate engine. Nothing here imports the API, the agent or the screen.
"""

import json
import math
import tempfile
import time
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import AsyncExitStack, asynccontextmanager
from dataclasses import dataclass, replace
from pathlib import Path

import networkx as nx
import pandas as pd
import tiktoken
from langchain_core.embeddings import Embeddings
from langchain_postgres import PGEngine, PGVectorStore
from langchain_postgres.v2.engine import Column as PGColumn
from langchain_postgres.v2.hybrid_search_config import HybridSearchConfig
from sqlalchemy import URL, func, select, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from login_investigator.corpus_check import read_table
from login_investigator.generator import REPO_ROOT
from login_investigator.postgres import (
    DatabaseUnavailable,
    ServerSettings,
    check_server,
    create_fresh_database,
    drop_database,
)
from login_investigator.rules import Finding

from . import chunking as chunking
from . import schema as schema
from .access import check_reader_role, grant_read_only
from .access import reader_settings as reader_settings
from .chunking import Chunk, read_chunks
from .graph import build_graph
from .graph_queries import GraphQueries, NetworkXQueries
from .integrity import GraphCounts, check_graph_integrity
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
    SERVER_DOWN,
    SETTINGS_INCOMPLETE,
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
    previous_database_retained: str | None = None


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
        self._graph: nx.MultiDiGraph | None = None
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

    @property
    def graph(self) -> nx.MultiDiGraph:
        if self._graph is None:
            raise ValueError("Open the knowledge base with its dataset to use the graph")
        return self._graph

    async def check_graph_integrity(self, graph: nx.MultiDiGraph | None = None) -> GraphCounts:
        if self._graph_verifier is not None:
            if graph is not None:
                raise ValueError('A native graph cannot be checked against an in-memory replacement')
            return await self._graph_verifier()
        if self._dataset is None:
            raise ValueError("Open the knowledge base with its dataset to check the graph")
        return await check_graph_integrity(self.engine, self._dataset, self.graph if graph is None else graph)

    @property
    def graph_queries(self) -> GraphQueries:
        if self._graph_queries is None:
            raise ValueError("Open the knowledge base with its dataset to use the graph")
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
    """With no re-ranker, search behaves as ticket 22 left it: the fused 20 are the result."""
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
            kb._graph, kb._log = await build_graph(engine, dataset)
            await kb.check_graph_integrity()
            nx.freeze(kb.graph)
            kb._graph_queries = NetworkXQueries(kb.graph, kb._log)
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


async def rebuild_knowledge_base(
    dataset: Path, server: ServerSettings, embedder: Embeddings, state_file: Path,
    *, reader_role: str = "li_reader",
) -> BuildReport:
    """Publish a fresh successful build atomically. Retain the previous database for inspection.

    The local state file contains no credentials. The fingerprint lives in the database itself,
    where `check_knowledge_base` reads it. A failed new build is dropped; the prior pointer and
    database remain usable.
    """
    previous = json.loads(state_file.read_text()) if state_file.exists() else {}
    if not isinstance(previous, dict) or (previous and not isinstance(previous.get("database"), str)):
        raise ValueError("The knowledge-base state file must name its previous database")
    check_server(server)
    database = create_fresh_database(server, prefix="li_kb")
    temporary: Path | None = None
    try:
        report = await build_knowledge_base(dataset, database, embedder, reader_role=reader_role)
        report = replace(report, previous_database_retained=previous.get("database"))
        state_file.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(mode="w", dir=state_file.parent, delete=False) as handle:
            temporary = Path(handle.name)
            json.dump({"database": database.database, "dataset": str(dataset.resolve())}, handle)
            handle.write("\n")
        temporary.replace(state_file)
        return report
    except BaseException:
        drop_database(database)
        raise
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


async def check_knowledge_base(
    dataset: Path, state_file: Path, server: ServerSettings | None = None,
) -> str | None:
    """The staleness guard (T18), run at the app's startup as the read-only role.

    Returns None when nothing has been built (decision 1): the app runs without a knowledge base.
    Returns the database's name when its recorded fingerprint matches the folder. Anything else
    raises `KnowledgeBaseNotReady` with fixed text (decision 2: a guard that cannot check refuses).
    Causes are suppressed, because database errors can carry hosts, names and paths.
    """
    if not state_file.exists():
        return None
    try:
        selection = json.loads(state_file.read_text(encoding="utf-8"))
        if isinstance(selection, dict) and 'format' in selection:
            async with open_current_knowledge_base(dataset, state_file, server=server) as kb:
                if kb is None:
                    return None
                return kb.engine.url.database
        name = selection["database"]
        if not isinstance(name, str):
            raise TypeError("database must be a name")
    except (OSError, ValueError, KeyError, TypeError):
        raise KnowledgeBaseNotReady(UNCHECKABLE) from None
    try:
        reader = reader_settings(replace(server or ServerSettings.from_env(), database=name))
    except DatabaseUnavailable:
        raise KnowledgeBaseNotReady(SETTINGS_INCOMPLETE) from None
    try:
        check_server(reader)
    except DatabaseUnavailable:
        raise KnowledgeBaseNotReady(SERVER_DOWN) from None
    try:
        expected = source_fingerprint(dataset)
        async with open_knowledge_base(reader) as kb:
            recorded = await kb.recorded_fingerprints()
    except (OSError, SQLAlchemyError):
        raise KnowledgeBaseNotReady(UNCHECKABLE) from None
    if len(recorded) != 1:
        raise KnowledgeBaseNotReady(UNCHECKABLE)
    if recorded[0] != expected:
        raise KnowledgeBaseNotReady(STALE)
    return name


@asynccontextmanager
async def open_current_knowledge_base(
    dataset: Path, state_file: Path, *, embedder: Embeddings | None = None,
    reranker: Reranker | None = None, server: ServerSettings | None = None,
) -> AsyncIterator[KnowledgeBase | None]:
    """Own the checked reader for one application lifetime; no build needs no database."""
    if state_file.exists():
        try:
            selected = json.loads(state_file.read_text())
            paired = isinstance(selected, dict) and 'format' in selected
        except (OSError, ValueError):
            raise KnowledgeBaseNotReady(UNCHECKABLE) from None
        if paired:
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
            return
    name = await check_knowledge_base(dataset, state_file, server)
    if name is None:
        yield None
        return
    try:
        reader = reader_settings(replace(server or ServerSettings.from_env(), database=name))
    except DatabaseUnavailable:
        raise KnowledgeBaseNotReady(SETTINGS_INCOMPLETE) from None
    # Only opening errors are translated. An exception in the caller's body must retain its
    # own meaning; the context still releases the pool in all cases.
    async with AsyncExitStack() as cleanup:
        try:
            kb = await cleanup.enter_async_context(open_knowledge_base(
                reader, dataset=dataset, embedder=embedder, reranker=reranker))
        except (OSError, ValueError, SQLAlchemyError):
            raise KnowledgeBaseNotReady(UNCHECKABLE) from None
        yield kb
