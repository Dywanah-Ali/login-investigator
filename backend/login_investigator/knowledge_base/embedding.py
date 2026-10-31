"""The one embedding factory; OpenRouter usage receipts measure the live build's cost."""

import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass

import httpx
from dotenv import dotenv_values
from langchain_openai import OpenAIEmbeddings
from pydantic import SecretStr

from login_investigator.postgres import ENV_PATH

from .schema import EMBEDDING_MODEL, VECTOR_SIZE


@dataclass
class EmbeddingUsage:
    requests: int = 0
    tokens: int = 0
    cost_usd: float | None = 0.0

    async def record_response(self, response: httpx.Response) -> None:
        if not response.is_success:
            return
        await response.aread()
        usage = response.json().get("usage", {})
        self.requests += 1
        self.tokens += int(usage.get("prompt_tokens", usage.get("total_tokens", 0)))
        cost = usage.get("cost")
        if cost is None or self.cost_usd is None:
            self.cost_usd = None
        else:
            self.cost_usd += float(cost)


@asynccontextmanager
async def embedding_service() -> AsyncIterator[tuple[OpenAIEmbeddings, EmbeddingUsage]]:
    """Do not put the key in environment, logs, repr or a saved report."""
    key = os.environ.get("OPENROUTER_API_KEY") or dotenv_values(ENV_PATH).get("OPENROUTER_API_KEY")
    if not key:
        raise ValueError("Set OPENROUTER_API_KEY in backend/.env")
    usage = EmbeddingUsage()
    with httpx.Client() as sync_client:
        async with httpx.AsyncClient(event_hooks={"response": [usage.record_response]}) as async_client:
            yield OpenAIEmbeddings(
                model=EMBEDDING_MODEL, dimensions=VECTOR_SIZE,
                api_key=SecretStr(key), base_url="https://openrouter.ai/api/v1",
                check_embedding_ctx_length=False, chunk_size=64, max_retries=2,
                timeout=60, http_client=sync_client, http_async_client=async_client,
            ), usage
