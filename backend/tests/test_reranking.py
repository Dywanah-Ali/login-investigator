"""Door 2: the OpenRouter re-ranker and its switch, against a fake HTTP server. No real key or call."""

import asyncio
import json
from pathlib import Path

import httpx
import pytest

from login_investigator.knowledge_base.reranking import (
    RerankerUnavailable, reranker_enabled, reranker_service,
)

KEY = {"OPENROUTER_API_KEY": "test-key-not-real"}


def reply(results: list[dict], status: int = 200) -> httpx.MockTransport:
    def handle(request: httpx.Request) -> httpx.Response:
        handle.requests.append(request)  # type: ignore[attr-defined]
        return httpx.Response(status, json={
            "model": "cohere/rerank-v3.5", "results": results,
            "usage": {"cost": 0.002, "search_units": 1, "total_tokens": 42},
        })
    handle.requests = []  # type: ignore[attr-defined]
    return httpx.MockTransport(handle)


def score(transport: httpx.MockTransport, texts: list[str], tmp_path: Path):
    async def run():
        async with reranker_service(KEY, tmp_path / ".env", transport=transport) as (reranker, usage):
            assert reranker is not None
            return await reranker.ascore("which policy", texts), usage
    return asyncio.run(run())


def test_every_candidate_is_scored_in_one_request_and_scores_return_in_input_order(tmp_path: Path):
    transport = reply([{"index": 2, "relevance_score": 0.9}, {"index": 0, "relevance_score": 0.5},
                       {"index": 1, "relevance_score": 0.1}])
    scores, usage = score(transport, ["a", "b", "c"], tmp_path)
    assert scores == [0.5, 0.1, 0.9]
    [request] = transport.handler.requests  # type: ignore[attr-defined]
    assert str(request.url) == "https://openrouter.ai/api/v1/rerank"
    assert request.headers["authorization"] == "Bearer test-key-not-real"
    assert json.loads(request.content) == {"model": "cohere/rerank-v3.5", "query": "which policy",
                                           "documents": ["a", "b", "c"], "top_n": 3}
    assert (usage.requests, usage.search_units, usage.tokens, usage.cost_usd) == (1, 1, 42, 0.002)


@pytest.mark.parametrize("results", [
    [{"index": 0, "relevance_score": 0.5}],
    [{"index": 0, "relevance_score": 0.5}, {"index": 0, "relevance_score": 0.4}],
    [{"index": 0, "relevance_score": 0.5}, {"index": 2, "relevance_score": 0.4}],
    [{"index": 0, "relevance_score": 0.5}, {"index": 1}],
    [{"index": 0, "relevance_score": 0.5}, {"index": True, "relevance_score": 0.4}],
])
def test_a_reply_that_does_not_score_each_candidate_once_is_refused(results, tmp_path: Path):
    with pytest.raises(ValueError, match="score every candidate exactly once"):
        score(reply(results), ["a", "b"], tmp_path)


def test_a_failed_call_stops_with_fixed_text_that_carries_no_key_or_reply(tmp_path: Path):
    def refuse(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, text="provider echoed test-key-not-real")

    with pytest.raises(RerankerUnavailable) as caught:
        score(httpx.MockTransport(refuse), ["a"], tmp_path)
    assert str(caught.value) == "The re-ranker call failed with HTTP 500"
    assert caught.value.__cause__ is None and caught.value.__suppress_context__


def test_malformed_usage_makes_the_cost_unknown_and_never_fails_the_search(tmp_path: Path):
    def handle(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"results": [{"index": 0, "relevance_score": 0.5}],
                                         "usage": {"search_units": "provider text", "cost": "n/a"}})

    scores, usage = score(httpx.MockTransport(handle), ["a"], tmp_path)
    assert scores == [0.5]
    assert (usage.requests, usage.cost_usd) == (1, None)


def test_the_switch_reads_the_environment_then_env_file_then_defaults_to_on(tmp_path: Path):
    env_file = tmp_path / ".env"
    assert reranker_enabled({}, env_file) is True
    env_file.write_text("LI_RERANKER=off\n", encoding="utf-8")
    assert reranker_enabled({}, env_file) is False
    assert reranker_enabled({"LI_RERANKER": "on"}, env_file) is True
    env_file.write_text("LI_RERANKER=\n", encoding="utf-8")
    assert reranker_enabled({}, env_file) is True


def test_an_unknown_switch_value_is_refused_without_echoing_it(tmp_path: Path):
    with pytest.raises(ValueError) as caught:
        reranker_enabled({"LI_RERANKER": "maybe-later"}, tmp_path / ".env")
    assert str(caught.value) == "LI_RERANKER must be on or off"


def test_switched_off_the_service_hands_in_no_reranker_and_needs_no_key(tmp_path: Path):
    async def run():
        async with reranker_service({"LI_RERANKER": "off"}, tmp_path / ".env") as (reranker, usage):
            return reranker, usage.requests
    assert asyncio.run(run()) == (None, 0)


def test_switched_on_without_a_key_the_service_refuses(tmp_path: Path):
    async def run():
        async with reranker_service({}, tmp_path / ".env"):
            pass
    with pytest.raises(ValueError, match="OPENROUTER_API_KEY"):
        asyncio.run(run())
