"""Write the knowledge graph as GEXF for Gephi Lite. From backend/:
uv run python -m scripts.export_graph --output graph.gexf

--finding-id writes one finding's neighbourhood instead of the whole graph. The script opens the
published knowledge base as the read-only role, after the same staleness check the app runs.
No API endpoint serves the file (knowledge-base ticket 08, decision 9).
"""

import argparse
import asyncio
import os
import sys
from dataclasses import replace
from pathlib import Path

from dotenv import dotenv_values

from login_investigator import knowledge_base
from login_investigator.generator import DATASET_DIR
from login_investigator.knowledge_base import (
    ExportRefused, KnowledgeBaseNotReady, check_knowledge_base, open_knowledge_base,
    reader_settings,
)
from login_investigator.knowledge_base.staleness import BUILD_COMMAND
from login_investigator.postgres import ENV_PATH, DatabaseUnavailable, ServerSettings


async def run(args: argparse.Namespace) -> bool:
    """False when nothing has been built, so there is no graph to export."""
    name = await check_knowledge_base(args.dataset_dir, args.state_file)
    if name is None:
        return False
    reader = reader_settings(replace(ServerSettings.from_env(), database=name))
    async with open_knowledge_base(reader, dataset=args.dataset_dir) as kb:
        kb.export_gexf(args.output, args.finding_id)
    return True


def main(argv: list[str] | None = None) -> int:
    values = {**dotenv_values(ENV_PATH), **os.environ}
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--finding-id")
    parser.add_argument("--dataset-dir", type=Path,
                        default=Path(values.get("LI_DATASET_DIR") or DATASET_DIR))
    # The pointer the build writes and the app reads, from the environment only, as they do.
    parser.add_argument("--state-file", type=Path, default=Path(
        os.environ.get("LI_KNOWLEDGE_BASE_STATE", "").strip() or knowledge_base.STATE_FILE))
    args = parser.parse_args(argv)
    try:
        built = asyncio.run(run(args))
    except (KnowledgeBaseNotReady, DatabaseUnavailable, ExportRefused) as error:
        # On this script's path these carry texts written in this project: the staleness guard's
        # fixed texts, the settings readers' texts and the export's refusals.
        print(f"Export refused: {error}", file=sys.stderr)
        return 1
    except Exception as error:
        # Database exceptions can contain hosts, names and credentials. Never print them.
        print(f"Export failed ({type(error).__name__}). Check the PostgreSQL setup and rebuild the "
              "knowledge base if its graph no longer passes the integrity check.", file=sys.stderr)
        return 1
    if not built:
        print(f"Export refused: no knowledge base has been built. Build it from backend/ with: "
              f"{BUILD_COMMAND}", file=sys.stderr)
        return 1
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
