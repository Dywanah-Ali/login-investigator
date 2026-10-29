"""The re-ranker behind its switch (T03 d5). Scores order evidence; until T39 they decide nothing."""

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator, Mapping, Sequence
from contextlib import asynccontextmanager
from dataclasses import dataclass
import math
import os
from pathlib import Path

import httpx
from dotenv import dotenv_values
from langchain_core.callbacks import Callbacks
from langchain_core.documents import Document
from langchain_core.documents.compressor import BaseDocumentCompressor
from pydantic import ConfigDict, SecretStr

from login_investigator.postgres import ENV_PATH

RERANK_MODEL = "cohere/rerank-v3.5"
KEEP = 5
SWITCH_NAME = "LI_RERANKER"
KEY_NAME = "OPENROUTER_API_KEY"
RERANK_URL = "https://openrouter.ai/api/v1/rerank"


class RerankerUnavailable(RuntimeError):
    """Fixed text only: the request behind an HTTP error carries the key in its headers."""


@dataclass(frozen=True)
class Ranking:
    scores: list[float]  # one per document, in input order
    kept: list[int]  # input positions of the best `top_n`, best first


class Reranker(BaseDocumentCompressor, ABC):
    """LangChain's compressor slot, without the legacy compression-retriever wrapper.

    Search and the compressor share `arank`, the one place the best `top_n` are chosen. Search
    also records the scores of the documents not kept.
    """
    top_n: int = KEEP

    @abstractmethod
    async def ascore(self, query: str, texts: list[str]) -> list[float]:
        """One relevance score per text, in input order."""

    async def arank(self, documents: Sequence[Document], query: str) -> Ranking:
        """Equal scores keep input order, which for search is the fused order."""
        if not documents:
            return Ranking([], [])
        scores = await self.ascore(query, [document.page_content for document in documents])
        if len(scores) != len(documents) or not all(isinstance(s, float) and math.isfinite(s) for s in scores):
            raise ValueError("The re-ranker must return one finite score per candidate")
        order = sorted(range(len(documents)), key=lambda index: -scores[index])
        return Ranking(scores, order[:self.top_n])

    def compress_documents(self, documents: Sequence[Document], query: str,
                           callbacks: Callbacks | None = None) -> Sequence[Document]:
        raise NotImplementedError("The knowledge base is async; use acompress_documents")

    async def acompress_documents(self, documents: Sequence[Document], query: str,
                                  callbacks: Callbacks | None = None) -> Sequence[Document]:
        ranking = await self.arank(documents, query)
        return [Document(page_content=documents[index].page_content, id=documents[index].id,
                         metadata={**documents[index].metadata, "relevance_score": ranking.scores[index]})
                for index in ranking.kept]


@dataclass
class RerankUsage:
    requests: int = 0
    search_units: int = 0
    tokens: int = 0
    cost_usd: float | None = 0.0

    async def record_response(self, response: httpx.Response) -> None:
        if not response.is_success:
            return
        await response.aread()
        self.requests += 1
        # Provider text must never fail the search or reach a message; unreadable usage is unknown.
        try:
            usage = response.json().get("usage") or {}
            search_units = int(usage.get("search_units", 0))
            tokens = int(usage.get("total_tokens", 0))
            cost = None if usage.get("cost") is None else float(usage["cost"])
        except (AttributeError, TypeError, ValueError):
            self.cost_usd = None
            return
        self.search_units += search_units
        self.tokens += tokens
        if cost is None or self.cost_usd is None:
            self.cost_usd = None
        else:
            self.cost_usd += cost


class OpenRouterReranker(Reranker):
    """Cohere's re-ranker through OpenRouter. Asks for every score, never the provider's cut."""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    api_key: SecretStr
    client: httpx.AsyncClient
    model: str = RERANK_MODEL

    async def ascore(self, query: str, texts: list[str]) -> list[float]:
        try:
            response = await self.client.post(RERANK_URL, headers={
                "Authorization": f"Bearer {self.api_key.get_secret_value()}",
            }, json={"model": self.model, "query": query, "documents": texts, "top_n": len(texts)})
            response.raise_for_status()
        except httpx.HTTPStatusError as error:
            raise RerankerUnavailable(
                f"The re-ranker call failed with HTTP {error.response.status_code}") from None
        except httpx.HTTPError:
            raise RerankerUnavailable("The re-ranker could not be reached") from None
        scores: dict[int, float] = {}
        try:
            for result in response.json()["results"]:
                index, value = result["index"], result["relevance_score"]
                if type(index) is not int or not 0 <= index < len(texts) or index in scores:
                    raise ValueError
                if isinstance(value, bool) or not isinstance(value, int | float):
                    raise ValueError
                scores[index] = float(value)
        except (KeyError, TypeError, ValueError):
            scores = {}
        if len(scores) != len(texts):
            raise ValueError("The re-ranker reply must score every candidate exactly once")
        return [scores[index] for index in range(len(texts))]


def _settings(environ: Mapping[str, str], env_file: Path | None) -> dict[str, str | None]:
    # Read at call time, so the test run's guard can point the default away from the real file.
    # An empty environment value counts as unset, as in the embedding factory's key lookup.
    return {**dotenv_values(env_file or ENV_PATH), **{name: v for name, v in environ.items() if v}}


def _enabled(values: Mapping[str, str | None]) -> bool:
    value = (values.get(SWITCH_NAME) or "on").strip().lower()
    if value not in {"on", "off"}:
        raise ValueError(f"{SWITCH_NAME} must be on or off")
    return value == "on"


def reranker_enabled(environ: Mapping[str, str] = os.environ, env_file: Path | None = None) -> bool:
    """The environment first, then `.env`, then on (T03 d5). Never echoes the value read."""
    return _enabled(_settings(environ, env_file))


@asynccontextmanager
async def reranker_service(
    environ: Mapping[str, str] = os.environ, env_file: Path | None = None,
    *, transport: httpx.AsyncBaseTransport | None = None,
) -> AsyncIterator[tuple[OpenRouterReranker | None, RerankUsage]]:
    """The one re-ranker factory. Switched off, it hands in none and search keeps the fused 20.

    Do not put the key in the environment, logs, repr or a saved report.
    """
    usage = RerankUsage()
    values = _settings(environ, env_file)
    if not _enabled(values):
        yield None, usage
        return
    key = values.get(KEY_NAME)
    if not key:
        raise ValueError(f"Set {KEY_NAME} in backend/.env")
    async with httpx.AsyncClient(transport=transport, timeout=60,
                                 event_hooks={"response": [usage.record_response]}) as client:
        yield OpenRouterReranker(api_key=SecretStr(key), client=client), usage
