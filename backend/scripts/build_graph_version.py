"""Build and verify an isolated PostgreSQL/Neo4j pair without switching the application."""

import argparse
import asyncio
import json
import statistics
import sys
import time
from dataclasses import asdict
from pathlib import Path

from langchain_core.embeddings import Embeddings

from login_investigator.generator import DATASET_DIR, REPO_ROOT
from login_investigator.knowledge_base.embedding import embedding_service
from login_investigator.knowledge_base.graph_version import build_version, open_version, remove_version
from login_investigator.knowledge_base.graph_service import docker, IMAGE
from login_investigator.knowledge_base.schema import VECTOR_SIZE
from login_investigator.postgres import ServerSettings


class OfflineEmbeddings(Embeddings):
    """Deterministic placeholder vectors for graph verification, never retrieval evaluation."""
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [[1.0] + [0.0] * (VECTOR_SIZE - 1) for _ in texts]

    def embed_query(self, text: str) -> list[float]:
        return self.embed_documents([text])[0]


async def run(args: argparse.Namespace) -> dict[str, object]:
    server = ServerSettings.from_env()
    started = time.monotonic()
    if args.offline:
        version = await build_version(args.dataset_dir, args.versions_dir, server, OfflineEmbeddings(), offline_embeddings=True)
    else:
        async with embedding_service() as (embedder, _):
            version = await build_version(args.dataset_dir, args.versions_dir, server, embedder)
    preparation = time.monotonic() - started
    try:
        samples = []
        answer: dict[str, object] = {}
        async with open_version(version.marker, server) as kb:
            for _ in range(5):
                tick = time.perf_counter()
                answer = kb.lookup_account(args.account)
                samples.append(1000 * (time.perf_counter() - tick))
        resources = json.loads(docker('stats', '--no-stream', '--format', '{{json .}}', version.container))
        return {'build_id': version.build_id, 'database': version.database,
                'container': version.container, 'image': IMAGE, 'driver': '6.1.0',
                'offline_embeddings': args.offline, 'disposed': args.dispose,
                'preparation_seconds': round(preparation, 3), 'lookup_median_ms': round(statistics.median(samples), 3),
                'lookup_samples_ms': samples, 'container_memory': resources['MemUsage'],
                'answer': answer, 'source_fingerprint': version.fingerprint}
    finally:
        if args.dispose:
            remove_version(version, server)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dataset-dir', type=Path, default=DATASET_DIR)
    parser.add_argument('--versions-dir', type=Path, default=REPO_ROOT / '.graph-versions')
    parser.add_argument('--offline', action='store_true', help='Use offline vectors for graph checks only')
    parser.add_argument('--dispose', action='store_true', help='Remove only the newly built pair after checking it')
    parser.add_argument('--account', default='amelia.ward')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args(argv)
    try:
        result = asyncio.run(run(args))
    except Exception as error:
        print(f'Isolated graph build failed ({type(error).__name__}). Start Docker Desktop, '
              'run docker pull neo4j:2026.10.1, and check PostgreSQL and reader settings. '
              'The active application pointer is unchanged.', file=sys.stderr)
        return 1
    rendered = json.dumps(result, indent=2) + '\n'
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered)
    print(rendered, end='')
    return 0


if __name__ == '__main__':
    sys.exit(main())
