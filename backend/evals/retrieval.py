"""The existing eval runner's direct retrieval layer. No agent or answer model is called."""

from dataclasses import asdict, replace
from datetime import date
import json
import hashlib
import os
from pathlib import Path
import time

from evals.scoring import score_retrieval
from dotenv import dotenv_values

from login_investigator import knowledge_base
from login_investigator.generator import DATASET_DIR
from login_investigator.knowledge_base import KnowledgeBase, check_knowledge_base, open_knowledge_base, reader_settings
from login_investigator.knowledge_base.embedding import embedding_service
from login_investigator.knowledge_base.reranking import reranker_service
from login_investigator.knowledge_base.retrieval import LIMIT, RRF_K, VerdictPolicy
from login_investigator.knowledge_base.schema import EMBEDDING_MODEL
from login_investigator.knowledge_base.staleness import NOT_BUILT, source_fingerprint
from login_investigator.postgres import ENV_PATH, ServerSettings

QUESTIONS = Path(__file__).with_name("knowledge_base_questions.json")
REQUESTS = Path(__file__).with_name("retrieval_requests.json")


def _date_json(value: object) -> str:
    if isinstance(value, date):
        return value.isoformat()
    raise TypeError(f"Not a JSON value: {type(value).__name__}")


async def evaluate_retrieval(kb: KnowledgeBase, questions: list[dict]) -> dict:
    """Check integrity before any retrieval. Execution never reads a question's gold fields."""
    integrity = await kb.check_graph_integrity()
    requests = json.loads(REQUESTS.read_text(encoding="utf-8"))["walks"]
    records = []
    for question in questions:
        started = time.monotonic()
        query = "\n".join(question["turns"])
        search = None if question["type"] == "graph_lookup" else await kb.search_corpus(query)
        request = requests.get(question["id"])
        walk = None
        if request:
            if request["kind"] == "account_groups":
                walk = kb.account_groups(request["username"])
            elif request["kind"] == "finding_radius":
                walk = kb.finding_walk(request["finding_id"])
            else:
                raise ValueError("Unknown direct graph request")
        elif question["type"] in {"graph_lookup", "mixed"}:
            raise ValueError(f"No direct graph request for {question['id']}")
        artifact = json.loads(json.dumps({
            "query": query, "request": request,
            "search": asdict(search) if search is not None else None,
            "walk": asdict(walk) if walk is not None else None,
        }, default=_date_json))
        records.append({
            "question": question["id"], "category": question["type"], "run": 1,
            "security_checked": False, "security_passed": True,
            "seconds": round(time.monotonic() - started, 3), "artifact": artifact,
            **score_retrieval(question, artifact),
        })
    return {"integrity": asdict(integrity), "records": records}


async def run_retrieval(only: list[str] | None = None) -> tuple[dict, str]:
    """Command integration. The question file stays independent of execution requests and scores."""
    questions = json.loads(QUESTIONS.read_text(encoding="utf-8"))["questions"]
    if only is not None:
        if not only:
            raise ValueError("--only needs at least one question id")
        unknown = set(only) - {q["id"] for q in questions}
        if unknown:
            raise ValueError("Unknown question ids: " + ", ".join(sorted(unknown)))
        questions = [q for q in questions if q["id"] in only]
    values = {**dotenv_values(ENV_PATH), **os.environ}
    dataset = Path(values.get("LI_DATASET_DIR") or DATASET_DIR)
    state = Path(values.get("LI_KNOWLEDGE_BASE_STATE") or knowledge_base.STATE_FILE)
    name = await check_knowledge_base(dataset, state)
    if name is None:
        raise ValueError(NOT_BUILT)
    reader = reader_settings(replace(ServerSettings.from_env(), database=name))
    async with embedding_service() as (embedder, usage), reranker_service() as (reranker, rerank_usage):
        async with open_knowledge_base(reader, dataset=dataset, embedder=embedder, reranker=reranker) as kb:
            report = await evaluate_retrieval(kb, questions)
    report["embedding_usage"] = asdict(usage)
    report["rerank_usage"] = asdict(rerank_usage)
    policy = VerdictPolicy()
    report["configuration"] = {"embedding_model": EMBEDDING_MODEL, "rrf_k": RRF_K,
                               "dense_limit": LIMIT, "keyword_limit": LIMIT, "fused_limit": LIMIT,
                               "none_enabled": policy.none_enabled, "min_similarity": policy.min_similarity,
                               "min_relevance": policy.min_relevance, "reranker": reranker is not None,
                               "reranker_model": reranker.model if reranker else None,
                               "reranker_keep": reranker.top_n if reranker else None,
                               "source_fingerprint": source_fingerprint(dataset)}
    files = [QUESTIONS, REQUESTS, Path(__file__), Path(__file__).with_name("scoring.py"),
             Path(__file__).with_name("run.py")]
    files += sorted(Path(knowledge_base.__file__).parent.glob("*.py"))
    digest = hashlib.sha256(json.dumps(report["configuration"], sort_keys=True).encode())
    for path in files:
        digest.update(path.name.encode())
        digest.update(path.read_bytes())
    return report, "retrieval-" + digest.hexdigest()[:12]
