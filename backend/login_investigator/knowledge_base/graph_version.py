"""Capture source inputs for one isolated, reproducible graph version."""

import shutil
import re
from pathlib import Path

from .staleness import source_fingerprint


def capture_snapshot(source: Path, destination: Path) -> str:
    """Copy once, verify the copy, and remove write permissions before any store reads it."""
    if destination.exists():
        raise FileExistsError("A source snapshot cannot be overwritten")
    if destination.resolve().is_relative_to(source.resolve()):
        raise ValueError("Store snapshots outside the source dataset")
    if any(path.is_symlink() for path in source.rglob('*')):
        raise ValueError("Source snapshots cannot contain symbolic links")
    fingerprint = source_fingerprint(source)
    shutil.copytree(source, destination, ignore=shutil.ignore_patterns('.*'))
    if source_fingerprint(source) != fingerprint or source_fingerprint(destination) != fingerprint:
        shutil.rmtree(destination)
        raise ValueError("Source inputs changed during snapshot capture; retry the build")
    for path in destination.rglob('*'):
        path.chmod(0o500 if path.is_dir() else 0o400)
    destination.chmod(0o500)
    return fingerprint


# The isolated command is intentionally separate from the active application's pointer.
import asyncio
import json
import uuid
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass, replace

from dotenv import dotenv_values
from langchain_core.embeddings import Embeddings
from sqlalchemy import text

from login_investigator.workers import owned_operation
from login_investigator.loader import load_log
from login_investigator.postgres import ServerSettings, check_server, create_fresh_database, drop_database
from . import KnowledgeBase, Reranker, build_knowledge_base, database_engine, reader_settings
from .graph_ingestion import import_graph
from .graph_service import GraphService, docker, check_serving_protection, execute
from .graph_verification import verify_graph
from .neo4j_graph import GraphSettings, Neo4jQueries, GraphUnavailable


@dataclass(frozen=True)
class GraphVersion:
    build_id: str
    database: str
    container: str
    fingerprint: str
    snapshot: Path
    marker: Path
    offline_embeddings: bool = False

    def description(self) -> dict[str, str | bool]:
        return {'build_id': self.build_id, 'database': self.database, 'container': self.container,
                'fingerprint': self.fingerprint, 'snapshot': str(self.snapshot),
                'offline_embeddings': self.offline_embeddings}


def remove_snapshot(path: Path) -> None:
    if path.exists():
        path.chmod(0o700)
        for child in path.rglob('*'):
            if child.is_dir():
                child.chmod(0o700)
        shutil.rmtree(path)


async def build_version(dataset: Path, root: Path, server: ServerSettings,
                        embedder: Embeddings, *, offline_embeddings: bool = False) -> GraphVersion:
    """Return a complete isolated pair; never publish to the application's active pointer."""
    check_server(server)
    build_id = uuid.uuid4().hex
    directory = root.resolve() / build_id
    directory.mkdir(parents=True, mode=0o700)
    service = GraphService('li-graph-' + build_id, directory)
    database = None
    try:
        fingerprint = capture_snapshot(dataset, directory / 'source')
        database = create_fresh_database(server, prefix='li_kb')
        reader = reader_settings(database)
        await build_knowledge_base(directory / 'source', database, embedder, reader_role=reader.user)
        engine = database_engine(database)
        try:
            async with engine.begin() as connection:
                await connection.execute(text('CREATE TABLE graph_pair (build_id TEXT PRIMARY KEY, fingerprint TEXT NOT NULL)'))
                await connection.execute(text('INSERT INTO graph_pair VALUES (:id, :fingerprint)'),
                                         {'id': build_id, 'fingerprint': fingerprint})
                role = engine.dialect.identifier_preparer.quote_identifier(reader_settings(database).user)
                await connection.execute(text(f'GRANT SELECT ON graph_pair TO {role}'))
            builder = await owned_operation(service.prepare)
            await import_graph(engine, directory / 'source', builder, build_id, fingerprint)
            await verify_graph(engine, directory / 'source', builder, build_id, fingerprint)
            serving = await owned_operation(lambda: service.seal(builder))
            protection = {'before_restart': await owned_operation(lambda: check_serving_protection(serving))}
            await owned_operation(lambda: docker('restart', service.name))
            serving = GraphSettings(service.uri(), serving.user, serving.password)
            await owned_operation(lambda: service.wait(serving))
            protection['after_restart'] = await owned_operation(lambda: check_serving_protection(serving))
            from neo4j.exceptions import AuthError
            try:
                await asyncio.to_thread(execute, GraphSettings(serving.uri, builder.user, builder.password), 'RETURN 1')
            except AuthError:
                pass
            else:
                raise ValueError('Retired graph builder credentials still work')
            await verify_graph(engine, directory / 'source', serving, build_id, fingerprint)
            (directory / 'protection.json').write_text(json.dumps(protection, indent=2) + '\n')
        finally:
            await engine.dispose()
        version = GraphVersion(build_id, database.database, service.name, fingerprint,
                               directory / 'source', directory / 'complete.json', offline_embeddings)
        # Validate the configured reader before publishing any completion marker.
        reader_engine = database_engine(reader)
        try:
            await verify_graph(reader_engine, directory / 'source', serving, build_id, fingerprint)
        finally:
            await reader_engine.dispose()
        temporary = directory / 'complete.tmp'
        temporary.write_text(json.dumps(version.description(), indent=2) + '\n')
        temporary.replace(version.marker)
        return version
    except BaseException:
        await owned_operation(lambda: dispose_resources(service, database, directory))
        raise


def dispose_resources(service: GraphService, database: ServerSettings | None, directory: Path) -> None:
    failures = []
    try:
        service.remove()
    except Exception:
        failures.append('neo4j')
    if database is not None:
        try:
            drop_database(database)
        except Exception:
            failures.append('postgresql')
    if failures:
        (directory / 'cleanup.json').write_text(json.dumps({
            'container': service.name, 'volume': service.volume,
            'database': database.database if database else None, 'incomplete': failures,
        }, indent=2) + '\n')
        raise GraphUnavailable('Cleanup incomplete. Retained version directory contains cleanup.json; '
                               'restore the unavailable service before removing these named resources.')
    remove_snapshot(directory)


@asynccontextmanager
async def open_version(marker: Path, server: ServerSettings, *, embedder: Embeddings | None = None,
                       reranker: Reranker | None = None) -> AsyncIterator[KnowledgeBase]:
    """Own both read clients for one selected source world, including failed startup."""
    value = json.loads(marker.read_text())
    version = GraphVersion(**value, marker=marker)
    if (not re.fullmatch(r'[0-9a-f]{32}', version.build_id)
            or version.container != 'li-graph-' + version.build_id
            or not re.fullmatch(r'li_kb_[0-9a-f]{12}', version.database)
            or not re.fullmatch(r'[0-9a-f]{64}', version.fingerprint)
            or marker.parent.name != version.build_id
            or Path(version.snapshot).resolve() != (marker.parent / 'source').resolve()):
        raise ValueError('Invalid isolated graph version descriptor')
    snapshot = Path(version.snapshot)
    if source_fingerprint(snapshot) != version.fingerprint:
        raise ValueError('Source snapshot changed; rebuild the isolated graph version')
    directory = marker.parent
    service = GraphService(version.container, directory)
    values = dotenv_values(directory / '.env')
    settings = GraphSettings(await owned_operation(service.uri), values.get('LI_GRAPH_USER') or '', values.get('LI_GRAPH_PASSWORD') or '')
    database = replace(server, database=version.database)
    engine = database_engine(reader_settings(database), bounded=True)
    graph = None
    try:
        async with engine.connect() as connection:
            rows = (await connection.execute(text('SELECT build_id, fingerprint FROM graph_pair'))).all()
            fingerprints = (await connection.execute(text('SELECT fingerprint FROM build_record'))).all()
        if rows != [(version.build_id, version.fingerprint)] or fingerprints != [(version.fingerprint,)]:
            raise ValueError('PostgreSQL and graph build identities do not match')
        await owned_operation(lambda: check_serving_protection(settings))
        await verify_graph(engine, snapshot, settings, version.build_id, version.fingerprint)
        kb = KnowledgeBase(engine, embedder, reranker)
        kb._dataset = snapshot
        kb._log = await owned_operation(lambda: load_log(snapshot / 'logins.csv'))
        kb.build_id = version.build_id
        kb.offline_embeddings = version.offline_embeddings

        async def check_integrity():
            if source_fingerprint(snapshot) != version.fingerprint:
                raise ValueError('Source snapshot changed')
            return await verify_graph(engine, snapshot, settings, version.build_id, version.fingerprint)

        kb._graph_verifier = check_integrity
        graph = Neo4jQueries(settings, kb._log)
        kb._graph_queries = graph
        yield kb
    finally:
        try:
            if graph is not None:
                await owned_operation(graph.close)
        finally:
            await engine.dispose()


def remove_version(version: GraphVersion, server: ServerSettings) -> None:
    """Explicit disposal for the caller that created this isolated version; never scans builds."""
    service = GraphService(version.container, version.marker.parent)
    service.container_created = service.volume_created = True
    dispose_resources(service, replace(server, database=version.database), version.marker.parent)
