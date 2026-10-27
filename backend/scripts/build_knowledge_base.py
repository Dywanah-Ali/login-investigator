"""Build a fresh knowledge base. From backend/: uv run python -m scripts.build_knowledge_base.

--check-embedder sends one short string to OpenRouter without building a database.
--report saves measured build evidence as JSON. No credentials are written or printed.
"""

import argparse
import asyncio
import json
import os
import sys
import time
from dataclasses import asdict
from pathlib import Path

from dotenv import dotenv_values

from login_investigator.generator import DATASET_DIR, REPO_ROOT
from login_investigator.knowledge_base import reader_settings, rebuild_knowledge_base
from login_investigator.knowledge_base.embedding import embedding_service
from login_investigator.knowledge_base.schema import EMBEDDING_MODEL, VECTOR_SIZE
from login_investigator.postgres import ENV_PATH, ServerSettings


async def run(args: argparse.Namespace) -> dict[str, object]:
    started = time.monotonic()
    async with embedding_service() as (embedder, usage):
        if args.check_embedder:
            vector = await embedder.aembed_query("A password spray targets multiple accounts.")
            if len(vector) != VECTOR_SIZE:
                raise ValueError("Embedding service returned an unexpected vector length")
            result: dict[str, object] = {"check": "passed", "vector_dimensions": len(vector)}
        else:
            server = ServerSettings.from_env()
            reader = reader_settings(server)
            report = await rebuild_knowledge_base(
                args.dataset_dir, server, embedder, args.state_file, reader_role=reader.user,
            )
            result = asdict(report)
        return {**result, "embedding_model": EMBEDDING_MODEL, "usage": asdict(usage),
                "total_elapsed_seconds": round(time.monotonic() - started, 3)}


def main(argv: list[str] | None = None) -> int:
    values = {**dotenv_values(ENV_PATH), **os.environ}
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset-dir", type=Path,
                        default=Path(values.get("LI_DATASET_DIR") or DATASET_DIR))
    parser.add_argument("--state-file", type=Path, default=REPO_ROOT / ".knowledge-base.json")
    parser.add_argument("--report", type=Path)
    parser.add_argument("--check-embedder", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = asyncio.run(run(args))
    except Exception as error:
        # Provider and database exceptions can contain credentials or source text. Never print them.
        print(f"Build failed ({type(error).__name__}). Check the dataset, PostgreSQL setup and "
              "embedding credentials. The previous database has been retained.", file=sys.stderr)
        return 1
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
