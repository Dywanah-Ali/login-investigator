"""Isolated, read-only retrieval experiment. No answer model or production policy changes.

uv run --directory backend python ../.scratch/knowledge-base/research/22-retrieval-experiment.py --check
uv run --directory backend python ../.scratch/knowledge-base/research/22-retrieval-experiment.py
Recovery: --base PATH --recovery PATH, where the latter is a reviewed list of case/need IDs.
"""

import argparse
import asyncio
from dataclasses import asdict, replace
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
CASES = HERE / "22-retrieval-experiment-cases.json"
sys.path.insert(0, str(ROOT / "backend"))

from login_investigator.generator import DATASET_DIR
from login_investigator.knowledge_base import (
    STATE_FILE, check_knowledge_base, open_knowledge_base, reader_settings,
)
from login_investigator.knowledge_base.chunking import read_chunks
from login_investigator.knowledge_base.embedding import embedding_service
from login_investigator.knowledge_base.retrieval import LIMIT, RRF_K
from login_investigator.knowledge_base.schema import EMBEDDING_MODEL
from login_investigator.knowledge_base.staleness import source_fingerprint
from login_investigator.postgres import ServerSettings


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def merge(lists):
    """Gold-free, stable fusion; candidate identity is the only deduplication key."""
    scores = {}
    for ids in lists:
        assert len(ids) == len(set(ids))
        for rank, chunk_id in enumerate(ids, 1):
            scores[chunk_id] = scores.get(chunk_id, 0) + 1 / (RRF_K + rank)
    return sorted(scores, key=lambda chunk_id: (-scores[chunk_id], chunk_id))[:LIMIT]


def query_id(query):
    return hashlib.sha256(query.encode()).hexdigest()


def routes(case):
    focused = [n["query"] for n in case["needs"] if n["id"] in case["focused_need_ids"]]
    return {"whole": [case["question"]], "focused": focused,
            "focused_broad": [*focused, case["question"]]}


def select(queries, results):
    keys = [query_id(q) for q in dict.fromkeys(queries)]
    selected = merge([results[key]["top20"] for key in keys])
    return {"query_ids": keys, "top20": selected,
            "query_count": len(keys),
            "candidate_occurrences": sum(len(results[k]["candidates"]) for k in keys),
            "elapsed_search_seconds_sum": sum(results[k]["seconds"] for k in keys),
            "embedding_tokens": sum(results[k]["usage"]["tokens"] for k in keys),
            "embedding_cost_usd": (sum(results[k]["usage"]["cost_usd"] for k in keys)
                                   if all(results[k]["usage"]["cost_usd"] is not None for k in keys)
                                   else None)}


def grade(case, selected):
    """Offline answer-key scoring only, after selection; never triggers a search."""
    ids = selected["top20"]
    gold = list(dict.fromkeys(g for n in case["needs"] for g in n["gold"]))
    return {"gold_ranks": {g: ids.index(g) + 1 if g in ids else None for g in gold},
            "all_required_evidence": all(g in ids for g in gold) if gold else None,
            "missing_needs": [n["id"] for n in case["needs"]
                              if n["gold"] and not all(g in ids for g in n["gold"])],
            "unanswerable_needs": [n["id"] for n in case["needs"] if not n["answer_available"]],
            "answer_quality": "not_measured", "runtime_sufficiency": "not_implemented"}


def validate(manifest):
    assert manifest["final_limit"] == LIMIT == 20
    chunks = {c.id for c in read_chunks(DATASET_DIR)}
    cases = manifest["cases"]
    assert len({c["id"] for c in cases}) == len(cases)
    for case in cases:
        needs = case["needs"]
        assert len({n["id"] for n in needs}) == len(needs)
        assert set(case["focused_need_ids"]) <= {n["id"] for n in needs}
        assert case["focused_need_ids"]
        for n in needs:
            assert set(n["gold"]) <= chunks, (case["id"], n["gold"])
            assert n["query"].strip() and n["recovery_query"].strip()
            assert n["answer_available"] == bool(n["gold"])
    # Check the evidence-budget mechanism with disjoint lists and a shared candidate.
    a = [f"a{i:02}" for i in range(20)]
    b = [f"b{i:02}" for i in range(20)]
    assert merge([a]) == a
    assert len(merge([a, b])) == 20
    assert merge([a, b]) == [item for pair in zip(a[:10], b[:10]) for item in pair]
    assert merge([["x", "a"], ["b", "x"]])[0] == "x"
    assert len(merge([["x"], ["x"]])) == 1
    print(f"Validated {len(cases)} cases, all gold IDs, deterministic fusion and 20-passage cap.")


async def run(args, manifest):
    started = datetime.now(timezone.utc)
    name = await check_knowledge_base(DATASET_DIR, STATE_FILE)
    if name is None:
        raise RuntimeError("Build the knowledge base before running this experiment")
    fingerprint = source_fingerprint(DATASET_DIR)
    report = {
        "started_at": started.isoformat(), "manifest_sha256": digest(CASES),
        "runner_sha256": digest(Path(__file__)), "source_fingerprint": fingerprint,
        "official_gold_sha256": digest(ROOT / "backend/evals/knowledge_base_questions.json"),
        "embedding_model": EMBEDDING_MODEL, "database": name,
        "limits": {"per_leg": LIMIT, "per_query": LIMIT, "final": LIMIT, "rrf_k": RRF_K},
        "scope": "Corpus only; no graph, answer model, runtime coverage or calibrated refusal. Queries and fusion fixed before first run.",
        "queries": {}, "cases": [],
    }
    recovery = {}
    if args.base:
        base = json.loads(args.base.read_text())
        assert base["manifest_sha256"] == report["manifest_sha256"]
        assert base["source_fingerprint"] == fingerprint
        assert base["runner_sha256"] == report["runner_sha256"]
        report["queries"] = base["queries"]
        report["base_artifact"] = str(args.base.relative_to(ROOT))
        report["base_sha256"] = digest(args.base)
        decisions = json.loads(args.recovery.read_text())
        assert decisions["base_sha256"] == digest(args.base)
        for decision in decisions["recover"]:
            assert decision["case_id"] not in recovery, "At most one recovery per case"
            recovery[decision["case_id"]] = decision["need_id"]
        assert set(recovery) <= {c["id"] for c in manifest["cases"]}
        report["recovery_decisions"] = decisions
    reader = reader_settings(replace(ServerSettings.from_env(), database=name))
    async with embedding_service() as (embedder, usage):
        async with open_knowledge_base(reader, dataset=DATASET_DIR, embedder=embedder) as kb:
            await kb.check_graph_integrity()
            async def fetch(query):
                key = query_id(query)
                if key in report["queries"]:
                    return
                before = asdict(usage)
                tick = time.perf_counter()
                result = await kb.search_corpus(query)
                elapsed = time.perf_counter() - tick
                after = asdict(usage)
                delta = {k: after[k] - before[k] if after[k] is not None and before[k] is not None else None
                         for k in before}
                report["queries"][key] = {
                    "query": query, "seconds": elapsed, "usage": delta,
                    "verdict": result.verdict, "reason": result.reason,
                    "top20": [c.chunk.id for c in result.chunks],
                    "candidates": [{"id": c.chunk.id, "text": c.chunk.text,
                                    "dense_rank": c.dense_rank, "keyword_rank": c.keyword_rank,
                                    "cosine_distance": c.cosine_distance,
                                    "keyword_score": c.keyword_score, "fused_score": c.fused_score}
                                   for c in result.candidates],
                }
            for case in manifest["cases"]:
                methods = routes(case)
                if case["id"] in recovery:
                    need = next(n for n in case["needs"] if n["id"] == recovery[case["id"]])
                    methods["human_recovery"] = [*methods["focused_broad"], need["recovery_query"]]
                for queries in methods.values():
                    for query in queries:
                        await fetch(query)
                row = {"id": case["id"], "methods": {}}
                for method, queries in methods.items():
                    selected = select(queries, report["queries"])
                    row["methods"][method] = {**selected, **grade(case, selected)}
                report["cases"].append(row)
                print(json.dumps({"case": case["id"], "coverage": {
                    method: {"all": value["all_required_evidence"], "missing": value["missing_needs"]}
                    for method, value in row["methods"].items()}}), flush=True)
        report["physical_usage_this_run"] = asdict(usage)
    assert source_fingerprint(DATASET_DIR) == fingerprint
    report["finished_at"] = datetime.now(timezone.utc).isoformat()
    label = "recovery" if args.base else "initial"
    output = HERE / f"22-retrieval-experiment-{started.strftime('%Y%m%dT%H%M%S%fZ')}-{label}.json"
    with output.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2)
        stream.write("\n")
    print(f"Saved {output.name}")
    print(json.dumps(report["physical_usage_this_run"]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--base", type=lambda p: Path(p).resolve())
    parser.add_argument("--recovery", type=lambda p: Path(p).resolve())
    args = parser.parse_args()
    if bool(args.base) != bool(args.recovery):
        parser.error("--base and --recovery must be supplied together")
    manifest = json.loads(CASES.read_text())
    validate(manifest)
    if not args.check:
        asyncio.run(run(args, manifest))
