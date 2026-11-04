"""OpenRouter Responses adapter for future comparisons, independent of the application's model seam.

One invocation means one HTTP POST. No SDK retries, output caps, provider fallback or remote
conversation state. The runner owns retries and saves each attempt. Full output items are
replayed unchanged for tool/role continuations; reported settings are never called verified.
"""

from __future__ import annotations

import copy
import json
import math
from collections.abc import Callable, Generator

from evals.comparison.adapters import Adapter, AdapterError, ModelRequest, ModelResponse
from evals.comparison.http_stream import response_events
from evals.comparison.records import redact

ENDPOINT = "https://openrouter.ai/api/v1/responses"
Transport = Callable[[str, str, dict, float], Generator[dict, None, None]]


def request_body(request: ModelRequest) -> dict:
    config = request.config
    if config.allow_fallbacks or config.service_tier != "standard":
        raise ValueError("comparison requests require standard service and no fallbacks")
    reasoning = dict(config.reasoning)
    # `adaptive` is the approved native Anthropic intent, not an OpenRouter `mode` value.
    # Unified enabled+effort is forwarded; native application still needs compatibility evidence.
    if reasoning.get("mode") == "adaptive":
        if config.provider != "anthropic" or reasoning.get("enabled") is not True:
            raise ValueError("adaptive reasoning is only configured for Anthropic")
        reasoning.pop("mode")
    items = []
    for message in request.messages:
        role = message["role"]
        if role == "assistant" and message.get("continuation") is not None:
            items.extend(copy.deepcopy(message["continuation"]["output"]))
        elif role == "tool":
            items.append({"type": "function_call_output", "call_id": message["tool_call_id"],
                          "output": message["content"]})
        elif role == "assistant":
            if message.get("content"):
                items.append({"type": "message", "role": role,
                              "content": [{"type": "output_text", "text": message["content"]}]})
            for call in message.get("tool_calls", []):
                arguments = call["arguments"]
                items.append({"type": "function_call", "call_id": call["id"],
                              "name": call["name"], "arguments": (
                                  arguments if isinstance(arguments, str) else json.dumps(arguments))})
        elif role in ("system", "user"):
            items.append({"type": "message", "role": role,
                          "content": [{"type": "input_text", "text": message["content"]}]})
        else:
            raise ValueError(f"unsupported message role {role!r}")
    body = {"model": config.model, "input": items, "reasoning": reasoning,
            "provider": {"only": [config.provider], "order": [config.provider],
                         "allow_fallbacks": False, "require_parameters": True},
            "service_tier": "default", "store": False, "stream": True,
            **config.sampling}
    if request.tools:
        body.update(tools=[{"type": "function", **t["function"]} for t in request.tools],
                    tool_choice="auto", debug={"echo_upstream_body": True})
    return body


def _number(value):
    if isinstance(value, bool) or not isinstance(value, int | float):
        return None
    if isinstance(value, int):
        return value if value >= 0 else None
    return value if math.isfinite(value) and value >= 0 else None


def _usage(response: dict) -> tuple[dict | None, float | None]:
    raw = response.get("usage")
    if not isinstance(raw, dict):
        return None, None
    input_details = raw.get("input_tokens_details")
    output_details = raw.get("output_tokens_details")
    input_details = input_details if isinstance(input_details, dict) else {}
    output_details = output_details if isinstance(output_details, dict) else {}
    # Reasoning is a subset of output; never add it to the output total.
    return {"input": _number(raw.get("input_tokens")),
            "output": _number(raw.get("output_tokens")),
            "reasoning": _number(output_details.get("reasoning_tokens")),
            "cache_read": _number(input_details.get("cached_tokens")),
            "raw": copy.deepcopy(raw)}, _number(raw.get("cost"))


def _text(response: dict) -> str:
    output = response.get("output")
    if not isinstance(output, list):
        return ""
    texts = []
    for item in output:
        if not isinstance(item, dict) or item.get("type") != "message":
            continue
        content = item.get("content")
        if not isinstance(content, list):
            continue
        texts.extend(part["text"] for part in content if isinstance(part, dict)
                     and part.get("type") == "output_text" and isinstance(part.get("text"), str))
    return "".join(texts)


def _validated_output(response: dict) -> list[dict]:
    output = response.get("output")
    if not isinstance(output, list) or not all(isinstance(item, dict) for item in output):
        raise ValueError("response output must be an array of objects")
    for item in output:
        if item.get("type") == "message":
            content = item.get("content")
            if not isinstance(content, list) or not all(isinstance(p, dict) for p in content):
                raise ValueError("message content must be an array of objects")
            for part in content:
                if part.get("type") == "output_text" and not isinstance(part.get("text"), str):
                    raise ValueError("output text must be a string")
        elif item.get("type") == "function_call":
            if not all(isinstance(item.get(k), str) and item[k] for k in ("call_id", "name")):
                raise ValueError("tool call identity must be nonempty text")
            if not isinstance(item.get("arguments"), str):
                raise ValueError("tool arguments must be a JSON string")
    return output


def _error_kind(data: dict, status: int = 0) -> str:
    if not isinstance(data, dict):
        return "permanent"
    canonical = data.get("error_type")
    error = data.get("error")
    code = error.get("code") if isinstance(error, dict) else None
    if canonical in ("authentication", "authorization", "invalid_request", "context_length_exceeded",
                     "content_filter", "insufficient_credits", "permission_denied"):
        return "permanent"
    if status in (408, 504) or canonical == "timeout":
        return "timeout"
    if (status == 429 or status >= 500 or code in ("rate_limit_exceeded", "server_error")
            or canonical in ("rate_limit", "provider_unavailable")):
        return "transient"
    return "permanent"


def _failure_details(response: dict, event: dict, key: str) -> dict:
    # Provider diagnostics are local response context; never automatically exported.
    return redact({"status": response.get("status"), "error": response.get("error"),
                   "error_type": response.get("error_type"),
                   "incomplete_details": response.get("incomplete_details"),
                   "continuation": {"response": response, "event": event}}, [key])


def _provider(response: dict) -> str | None:
    if isinstance(response.get("provider"), str):
        return response["provider"]
    metadata = response.get("openrouter_metadata")
    if not isinstance(metadata, dict) or not isinstance(metadata.get("endpoints"), dict):
        return None
    available = metadata["endpoints"].get("available")
    if not isinstance(available, list):
        return None
    selected = [item["provider"] for item in available if isinstance(item, dict)
                and item.get("selected") is True and isinstance(item.get("provider"), str)]
    return selected[0] if len(selected) == 1 else None


class OpenRouterAdapter(Adapter):
    name = "openrouter"
    version = "2"

    def __init__(self, api_key: str = "", *, transport: Transport = response_events):
        self._api_key = api_key
        self._transport = transport

    def request_details(self, request: ModelRequest) -> dict:
        """Exact credential-free wire settings saved before dispatch."""
        return {"endpoint": ENDPOINT, "body": request_body(request),
                "headers": {"X-OpenRouter-Metadata": "enabled"},
                "reasoning_mapping": "unified enabled/effort; native application unverified"}

    def complete(self, request: ModelRequest) -> ModelResponse:
        if not self._api_key:
            raise AdapterError("permanent", "OpenRouter key not loaded; paid execution is disabled")
        body = request_body(request)
        response: dict = {}
        partial = ""
        events = self._transport(ENDPOINT, self._api_key, body, request.timeout_s)
        failure_event: dict = {}
        debug_events: list[dict] = []
        try:
            for event in events:
                if not isinstance(event, dict):
                    raise TypeError("response event must be an object")
                failure_event = event
                if isinstance(event.get("debug"), dict):
                    # Upstream inputs are local diagnostic evidence, never replayed as output
                    # or automatically exported to telemetry.
                    debug_events.append(redact(event["debug"], [self._api_key]))
                kind = event.get("type")
                if kind == "response.output_text.delta":
                    partial += event.get("delta", "")
                if isinstance(event.get("response"), dict):
                    response.update(event["response"])
                if isinstance(event.get("openrouter_metadata"), dict):
                    response["openrouter_metadata"] = event["openrouter_metadata"]
                if kind in ("transport.http_error", "error", "response.failed"):
                    status = event.get("status", 0)
                    details = event.get("body") or event.get("response") or event
                    # Do not echo provider error text: it may contain credentials or input.
                    raise AdapterError(_error_kind(details, status),
                                       f"OpenRouter failure (HTTP {status})")
                if kind == "transport.error":
                    raise AdapterError(event["kind"], event["message"])
                if kind == "response.incomplete":
                    raise AdapterError("permanent", "OpenRouter returned incomplete output")
                if kind == "response.completed":
                    if response.get("status") != "completed" or response.get("error"):
                        raise AdapterError("permanent", "OpenRouter completion has a failed status")
                    output = _validated_output(response)
                    calls = [{"id": item["call_id"], "name": item["name"],
                              "arguments": item["arguments"]} for item in output
                             if item.get("type") == "function_call"]
                    usage, cost = _usage(response)
                    return ModelResponse(
                        text=_text(response), tool_calls=calls, usage=usage, cost_usd=cost,
                        generation_id=response.get("id"), model_reported=response.get("model"),
                        provider_reported=_provider(response), finish_reason="completed",
                        settings_reported={k: response[k] for k in (
                            "reasoning", "service_tier", "temperature", "top_p", "top_k",
                            "max_output_tokens", "incomplete_details", "openrouter_metadata")
                                           if k in response},
                        continuation={"output": copy.deepcopy(response.get("output", [])),
                                      **({"debug_events": debug_events} if debug_events else {})})
            raise AdapterError("transient", "OpenRouter stream ended without a completion event")
        except AdapterError as error:
            usage, cost = _usage(response)
            # Keep every available partial and charge, including failed/incomplete responses.
            error.partial_text = _text(response) or partial
            error.usage, error.cost_usd = usage, cost
            error.generation_id = response.get("id")
            error.details = _failure_details(response, failure_event, self._api_key)
            if debug_events:
                error.details["continuation"]["debug_events"] = debug_events
            raise
        except (KeyError, TypeError, ValueError):
            usage, cost = _usage(response)
            details = _failure_details(response, failure_event, self._api_key)
            if debug_events:
                details["continuation"]["debug_events"] = debug_events
            raise AdapterError("permanent", "Malformed OpenRouter response",
                               partial_text=_text(response) or partial, usage=usage, cost_usd=cost,
                               generation_id=response.get("id"),
                               details=details) from None
        finally:
            events.close()
