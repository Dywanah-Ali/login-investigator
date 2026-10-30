"""An evaluation owns a complete disposable version; the application keeps its selection."""

import asyncio
import tempfile
from collections.abc import AsyncIterator, Iterator
from contextlib import asynccontextmanager, contextmanager
from dataclasses import dataclass
from pathlib import Path

from langchain_core.embeddings import Embeddings
from sqlalchemy import select

from login_investigator.postgres import ServerSettings
from login_investigator.workers import owned_operation
from . import open_current_knowledge_base, schema
from .graph_selection import select_version
from .graph_version import build_version, remove_version
from .staleness import KnowledgeBaseNotReady

EVALUATION_UNAVAILABLE = ('An isolated evaluation version could not be prepared. Check PostgreSQL, '
                          'Docker and the selected complete source version. The application selection is unchanged.')


@dataclass(frozen=True)
class EvaluationVersion:
    dataset: Path
    state_file: Path
    build_id: str | None


class StoredEmbeddings(Embeddings):
    """Reuse only exact unchanged passage vectors from the checked source build.

    This avoids buying the same embeddings again. Queries still use the configured provider.
    A source/settings change refuses the clone; there is no missing-text fallback.
    """
    def __init__(self, vectors: dict[str, list[float]]):
        self.vectors = vectors

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [list(self.vectors[text]) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        raise ValueError('Stored passage vectors cannot embed evaluation queries')


@asynccontextmanager
async def isolated_evaluation(dataset: Path, state_file: Path, *, root: Path | None = None
                              ) -> AsyncIterator[EvaluationVersion]:
    async with open_current_knowledge_base(dataset, state_file) as source:
        if source is None:
            if root is not None:
                root.mkdir(parents=True, exist_ok=True)
            with tempfile.TemporaryDirectory(prefix='li-evaluation-', dir=root) as directory:
                yield EvaluationVersion(dataset, Path(directory) / 'selected.json', None)
            return
        if source.offline_embeddings:
            raise KnowledgeBaseNotReady('Offline graph versions cannot provide evaluation evidence. Build with real embeddings.')
        source_directory = source.source_snapshot
        if source_directory is None:
            raise KnowledgeBaseNotReady(EVALUATION_UNAVAILABLE)
        fingerprints = await source.recorded_fingerprints()
        vectors = {}
        async with source.engine.connect() as connection:
            for content, vector in (await connection.execute(select(schema.chunks.c.content,
                                                                     schema.chunks.c.embedding))):
                converted = [float(value) for value in vector]
                if content in vectors and vectors[content] != converted:
                    raise KnowledgeBaseNotReady(EVALUATION_UNAVAILABLE)
                vectors[content] = converted
    if root is not None:
        root.mkdir(parents=True, exist_ok=True)
    server = ServerSettings.from_env()
    directory = Path(tempfile.mkdtemp(prefix='li-evaluation-', dir=root))
    selected = directory / 'selected.json'
    version = None
    try:
        try:
            version = await build_version(source_directory, directory, server, StoredEmbeddings(vectors))
            if fingerprints != [version.fingerprint]:
                raise ValueError('Source version changed while preparing the evaluation')
            await select_version(version.marker, selected, server)
        except Exception:
            raise KnowledgeBaseNotReady(EVALUATION_UNAVAILABLE) from None
        yield EvaluationVersion(version.snapshot, selected, version.build_id)
    finally:
        try:
            if version is not None:
                await owned_operation(lambda: remove_version(version, server))
        finally:
            # Cancellation may be re-raised after disposal finishes. Remove its pointer too,
            # but retain all recovery state when resource disposal was not confirmed.
            if version is not None and not version.marker.parent.exists():
                selected.unlink(missing_ok=True)
            if directory.exists() and not any(directory.iterdir()):
                directory.rmdir()


@contextmanager
def evaluation_version(dataset: Path, state_file: Path) -> Iterator[EvaluationVersion]:
    """The synchronous API evaluator owns the same async preparation/cleanup lifecycle."""
    with asyncio.Runner() as runner:
        context = isolated_evaluation(dataset, state_file)
        version = runner.run(context.__aenter__())
        try:
            yield version
        finally:
            runner.run(context.__aexit__(None, None, None))
