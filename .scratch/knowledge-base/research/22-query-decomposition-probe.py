"""Diagnostic only: human-written queries, fixed before running, no application policy change.

Run from the repository root:
uv run --directory backend python ../.scratch/knowledge-base/research/22-query-decomposition-probe.py
"""

import asyncio
from dataclasses import asdict, replace
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "backend"))

from login_investigator.generator import DATASET_DIR
from login_investigator.knowledge_base import STATE_FILE, check_knowledge_base, open_knowledge_base, reader_settings
from login_investigator.knowledge_base.embedding import embedding_service
from login_investigator.knowledge_base.staleness import source_fingerprint
from login_investigator.postgres import ServerSettings


async def main():
    questions = json.loads((ROOT / "backend/evals/knowledge_base_questions.json").read_text())["questions"]
    question = next(q for q in questions if q["id"] == "K04")
    queries = [
        ("original", question["turns"][0]),
        ("focused_neutral", "Why did amelia.ward's successful sign-ins not require MFA?"),
        ("focused_exception", "Does amelia.ward have an approved MFA exception?"),
        ("focused_procedure", "How should we investigate MFA when a password spray succeeds?"),
    ]
    name = await check_knowledge_base(DATASET_DIR, STATE_FILE)
    if name is None:
        raise RuntimeError("Build the knowledge base before running this diagnostic")
    reader = reader_settings(replace(ServerSettings.from_env(), database=name))
    report = {
        "started_at": datetime.now(timezone.utc).isoformat(),
        "purpose": "Human-written query diagnostic on an already-inspected failure; not a held-out evaluation or an automatic decomposition policy.",
        "source_fingerprint": source_fingerprint(DATASET_DIR),
        "gold": question["gold"]["chunks"],
        "runs": [],
    }
    async with embedding_service() as (embedder, usage):
        async with open_knowledge_base(reader, dataset=DATASET_DIR, embedder=embedder) as kb:
            await kb.check_graph_integrity()
            for label, query in queries:
                result = await kb.search_corpus(query)
                ids = [c.chunk.id for c in result.chunks]
                row = {
                    "label": label, "query": query,
                    "gold_ranks": {gold: ids.index(gold) + 1 if gold in ids else None
                                   for gold in question["gold"]["chunks"]},
                    "keyword_candidates": sum(c.keyword_rank is not None for c in result.candidates),
                    "candidates": [{"id": c.chunk.id, "dense_rank": c.dense_rank,
                                    "keyword_rank": c.keyword_rank, "cosine_distance": c.cosine_distance,
                                    "keyword_score": c.keyword_score, "fused_score": c.fused_score}
                                   for c in result.candidates],
                    "top20": ids,
                }
                report["runs"].append(row)
                print(json.dumps({key: value for key, value in row.items() if key not in {"candidates", "top20"}}), flush=True)
        report["embedding_usage"] = asdict(usage)
    output = Path(__file__).with_suffix(".json")
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("Saved", output.name)
    print(json.dumps(report["embedding_usage"]))


asyncio.run(main())
