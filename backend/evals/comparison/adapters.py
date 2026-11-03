"""The one seam between the runner and a model. The runner never imports a provider SDK.

An adapter sends one request and returns one response, or raises `AdapterError`. It never retries
by itself: every retry is the runner's, so each attempt is recorded (T52 call/retry policy). The
OpenRouter adapter lives in `openrouter.py`; fake models exercise this seam offline.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field


@dataclass(frozen=True)
class ModelConfig:
    """One approved configuration. `label` is private: blinded views never show it."""

    config_id: str
    label: str
    model: str
    provider: str
    reasoning: dict
    sampling: dict = field(default_factory=dict)
    service_tier: str = "standard"
    allow_fallbacks: bool = False
    notes: str = ""

    def to_dict(self) -> dict:
        return {"config_id": self.config_id, "label": self.label, "model": self.model,
                "provider": self.provider, "reasoning": self.reasoning, "sampling": self.sampling,
                "service_tier": self.service_tier, "allow_fallbacks": self.allow_fallbacks,
                "notes": self.notes}


@dataclass(frozen=True)
class ModelRequest:
    config: ModelConfig
    messages: list[dict]
    timeout_s: float
    tools: list[dict] | None = None


@dataclass(frozen=True)
class ModelResponse:
    text: str
    tool_calls: list[dict] = field(default_factory=list)  # {"id", "name", "arguments"}
    usage: dict | None = None  # input, output, reasoning, cache_read; None when not reported
    cost_usd: float | None = None
    generation_id: str | None = None
    model_reported: str | None = None
    provider_reported: str | None = None
    finish_reason: str | None = None
    settings_reported: dict | None = None
    continuation: dict | None = None  # provider data needed to continue a conversation


class AdapterError(Exception):
    """`kind` is `transient` (may be retried), `permanent` (never retried) or `timeout`."""

    def __init__(self, kind: str, message: str, *, partial_text: str = "",
                 usage: dict | None = None, cost_usd: float | None = None,
                 generation_id: str | None = None, details: dict | None = None):
        super().__init__(message)
        if kind not in ("transient", "permanent", "timeout"):
            raise ValueError(f"unknown adapter error kind {kind!r}")
        self.kind = kind
        self.partial_text = partial_text
        self.usage = usage
        self.cost_usd = cost_usd
        self.generation_id = generation_id
        self.details = details


class Adapter:
    name = "abstract"
    version = "0"

    def request_details(self, request: ModelRequest) -> dict | None:
        """Credential-free wire representation, when an adapter has one."""
        return None

    def complete(self, request: ModelRequest) -> ModelResponse:
        raise NotImplementedError


class FakeClock:
    """A monotonic clock for tests. Fake adapters and the runner's sleep advance it."""

    def __init__(self, start: float = 1000.0):
        self.now = start

    def __call__(self) -> float:
        return self.now

    def advance(self, seconds: float) -> None:
        self.now += seconds


Script = Callable[[ModelRequest, int], ModelResponse | AdapterError | BaseException]


class FakeAdapter(Adapter):
    """Answers from a script: `script(request, call_number)` returns a response, or an error to
    raise. `elapsed(request, call_number)` advances the fake clock; a request that would outlast
    its timeout raises a timeout, as a real client would."""

    name = "fake"
    version = "1"

    def __init__(self, script: Script, clock: FakeClock,
                 elapsed: Callable[[ModelRequest, int], float] = lambda r, n: 1.0):
        self.script = script
        self.clock = clock
        self.elapsed = elapsed
        self.requests: list[ModelRequest] = []

    def complete(self, request: ModelRequest) -> ModelResponse:
        number = len(self.requests)
        self.requests.append(request)
        took = self.elapsed(request, number)
        if took > request.timeout_s:
            self.clock.advance(request.timeout_s)
            raise AdapterError("timeout", f"no response within {request.timeout_s:.0f}s")
        self.clock.advance(took)
        outcome = self.script(request, number)
        if isinstance(outcome, BaseException):
            raise outcome
        return outcome
