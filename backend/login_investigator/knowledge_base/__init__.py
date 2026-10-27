"""Door 2: build a dataset's knowledge base, open it, and read named records.

The build and LangChain store share one SQLAlchemy async engine on psycopg. Readers open a
separate engine. Nothing here imports the API, the agent or the screen.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path
import math
import json
import tempfile
import time
from dataclasses import dataclass, replace

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
    DatabaseUnavailable, ServerSettings, check_server, create_fresh_database, drop_database,
)
from . import chunking as chunking, schema as schema
from .chunking import Chunk, read_chunks
from .access import check_reader_role, grant_read_only, reader_settings as reader_settings
from .mentions import find_mentions
from .staleness import (
    NOT_BUILT as NOT_BUILT, SERVER_DOWN, SETTINGS_INCOMPLETE, STALE, UNCHECKABLE,
    KnowledgeBaseNotReady as KnowledgeBaseNotReady, source_fingerprint,
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


def database_engine(settings: ServerSettings) -> AsyncEngine:
    return create_async_engine(URL.create(
        "postgresql+psycopg", username=settings.user, password=settings.password,
        host=settings.host, port=settings.port, database=settings.database,
    ), hide_parameters=True)


class KnowledgeBase:
    def __init__(self, engine: AsyncEngine):
        self.engine = engine

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
async def open_knowledge_base(settings: ServerSettings) -> AsyncIterator[KnowledgeBase]:
    engine = database_engine(settings)
    try:
        yield KnowledgeBase(engine)
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
        name = json.loads(state_file.read_text(encoding="utf-8"))["database"]
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
