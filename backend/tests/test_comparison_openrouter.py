"""T54 checkpoint 3 adapter checks. All credentials and remote responses are fake.

The elapsed-deadline test uses a silent spawned worker, never an external HTTP service.
The transport is tested against a fake Requests session, including redirects and retries.
"""

from __future__ import annotations

import json
import multiprocessing
import time
from dataclasses import replace

import pytest

from evals.comparison import http_stream, openrouter
from evals.comparison.adapters import AdapterError, ModelConfig, ModelRequest

KEY = "fake-openrouter-key-only-for-tests"
CONFIG = ModelConfig('test', 'Test', 'openai/gpt-6.1-sol', 'openai', {'effort': 'medium'})


def request(config=CONFIG, messages=None, tools=None):
    return ModelRequest(config, messages or [{"role": "system", "content": "A system prompt"},
                                            {"role": "user", "content": "A question"}], 180, tools)


def completed(**overrides):
    return {"id": "gen-test-1", "status": "completed", "model": CONFIG.model,
            "provider": "OpenAI", "service_tier": "default",
            "output": [{"type": "message", "role": "assistant", "id": "msg-1",
                        "content": [{"type": "output_text", "text": "Assessment [L1]."}]}],
            "usage": {"input_tokens": 10, "output_tokens": 7, "cost": 0.001,
                      "output_tokens_details": {"reasoning_tokens": 4},
                      "input_tokens_details": {"cached_tokens": 3}}, **overrides}


class FakeTransport:
    def __init__(self, events):
        self.events = events
        self.calls = []
        self.closed = False

    def __call__(self, url, key, body, timeout):
        self.calls.append((url, key, body, timeout))
        try:
            for event in self.events:
                if isinstance(event, BaseException):
                    raise event
                yield event
        finally:
            self.closed = True




def test_unapproved_service_and_fallback_settings_are_refused():
    for config in (replace(CONFIG, allow_fallbacks=True), replace(CONFIG, service_tier="priority")):
        with pytest.raises(ValueError):
            openrouter.request_body(request(config))






@pytest.mark.parametrize("data", [completed(status="failed", error={"code": "invalid_request"}),
                                 completed(output="malformed")])
def test_upstream_debug_survives_failed_or_malformed_response(data):
    fake = FakeTransport([{"debug": {"echo_upstream_body": {"reasoning_effort": "medium"}}},
                          {"type": "response.failed" if data.get("error") else "response.completed",
                           "response": data}])
    with pytest.raises(AdapterError) as caught:
        openrouter.OpenRouterAdapter(KEY, transport=fake).complete(request())
    assert caught.value.details is not None
    assert caught.value.details["continuation"]["debug_events"] == [
        {"echo_upstream_body": {"reasoning_effort": "medium"}}]


def test_response_usage_identity_and_full_continuation_are_preserved():
    data = completed()
    fake = FakeTransport([{"type": "response.completed", "response": data}])
    response = openrouter.OpenRouterAdapter(KEY, transport=fake).complete(request())
    assert fake.closed and len(fake.calls) == 1
    assert fake.calls[0][:2] == (openrouter.ENDPOINT, KEY)
    assert fake.calls[0][3] == 180
    assert response.text == "Assessment [L1]."
    assert response.usage == {"input": 10, "output": 7, "reasoning": 4, "cache_read": 3,
                              "raw": data["usage"]}
    assert response.cost_usd == 0.001 and response.generation_id == "gen-test-1"
    assert response.provider_reported == "OpenAI" and response.model_reported == CONFIG.model
    assert response.continuation == {"output": data["output"]}
    assert response.settings_reported == {"service_tier": "default"}


@pytest.mark.parametrize("usage,expected", [
    (None, None), ({}, {"input": None, "output": None, "reasoning": None,
                       "cache_read": None, "raw": {}}),
    ({"output_tokens": 0, "cost": 0}, {"input": None, "output": 0, "reasoning": None,
                                        "cache_read": None, "raw": {"output_tokens": 0, "cost": 0}}),
])
def test_missing_usage_is_unknown_and_reported_zero_is_zero(usage, expected):
    fake = FakeTransport([{"type": "response.completed", "response": completed(usage=usage)}])
    response = openrouter.OpenRouterAdapter(KEY, transport=fake).complete(request())
    assert response.usage == expected
    assert response.cost_usd == (0 if usage and "cost" in usage else None)


def test_negative_nonfinite_and_boolean_usage_is_not_used_as_a_number():
    data = completed(usage={"input_tokens": True, "output_tokens": -1, "cost": float("nan")})
    fake = FakeTransport([{"type": "response.completed", "response": data}])
    response = openrouter.OpenRouterAdapter(KEY, transport=fake).complete(request())
    assert response.usage is not None
    assert response.usage["input"] is None and response.usage["output"] is None
    assert response.cost_usd is None




@pytest.mark.parametrize("event,kind", [
    ({"type": "transport.http_error", "status": 401}, "permanent"),
    ({"type": "transport.http_error", "status": 402}, "permanent"),
    ({"type": "transport.http_error", "status": 429}, "transient"),
    ({"type": "transport.http_error", "status": 503}, "transient"),
    ({"type": "transport.http_error", "status": 504}, "timeout"),
    ({"type": "transport.http_error", "status": 500,
      "body": {"error_type": "authentication"}}, "permanent"),
    ({"type": "error", "error": {"code": "rate_limit_exceeded"}}, "transient"),
    ({"type": "response.failed", "response": completed(status="failed", error={
        "code": "server_error", "message": KEY}, error_type="authentication")}, "permanent"),
])
def test_failures_are_classified_without_adapter_retries_or_echoing_keys(event, kind):
    fake = FakeTransport([event])
    with pytest.raises(AdapterError) as caught:
        openrouter.OpenRouterAdapter(KEY, transport=fake).complete(request())
    assert caught.value.kind == kind
    assert len(fake.calls) == 1 and fake.closed
    assert KEY not in str(caught.value)


@pytest.mark.parametrize("last", ["timeout", "disconnect", "incomplete", "failed"])
def test_failure_keeps_partial_output_generation_id_and_available_cost(last):
    data = completed(status=last)
    first = {"type": "response.created", "response": completed(output=[])}
    if last == "timeout":
        ending = AdapterError("timeout", "elapsed deadline")
    elif last == "disconnect":
        ending = {"type": "transport.error", "kind": "transient", "message": "disconnected"}
    else:
        ending = {"type": f"response.{last}", "response": data}
    fake = FakeTransport([first, {"type": "response.output_text.delta", "delta": "Half answer"},
                          ending])
    with pytest.raises(AdapterError) as caught:
        openrouter.OpenRouterAdapter(KEY, transport=fake).complete(request())
    assert caught.value.partial_text == ("Assessment [L1]." if last in ("incomplete", "failed")
                                         else "Half answer")
    assert caught.value.generation_id == "gen-test-1" and caught.value.cost_usd == 0.001


def test_unfinished_stream_is_not_a_success():
    fake = FakeTransport([{"type": "response.output_text.delta", "delta": "Partial"}])
    with pytest.raises(AdapterError) as caught:
        openrouter.OpenRouterAdapter(KEY, transport=fake).complete(request())
    assert caught.value.kind == "transient" and caught.value.partial_text == "Partial"
    assert caught.value.usage is None and caught.value.cost_usd is None


def test_sse_comments_multiline_and_done():
    lines = [": comment", "event: response.created", 'data: {"type":',
             'data: "response.created"}', "", "data: [DONE]", ""]
    assert list(http_stream._sse(lines)) == [{"type": "response.created"}]


@pytest.mark.parametrize("lines", [['data: {"type":"x"}'], ['data: []', ''],
                                   ['data: not-json', '']])
def test_sse_malformed_or_torn_frames_are_errors(lines):
    with pytest.raises(ValueError):
        list(http_stream._sse(lines))


def test_http_worker_sends_one_post_without_redirects_and_never_echoes_error_body(monkeypatch):
    calls = []
    messages = []

    class Response:
        status_code = 500

        def json(self):
            return {"id": "gen-failure", "usage": {"cost": 0.2, "output_tokens": 8},
                    "error_type": "authentication", "error": {"message": KEY}}

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

    class Session:
        trust_env = True

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def post(self, url, **kwargs):
            calls.append((url, kwargs, self.trust_env))
            return Response()

    monkeypatch.setattr(http_stream.requests, "Session", Session)
    receiving, sending = multiprocessing.Pipe(duplex=False)
    try:
        http_stream._http_worker(sending, "https://fake.invalid", KEY, {"input": "fake"}, 3)
        messages.append(receiving.recv())
    finally:
        receiving.close()
        sending.close()
    assert len(calls) == 1
    assert calls[0][1]["allow_redirects"] is False and calls[0][2] is False
    assert calls[0][1]["headers"]["X-OpenRouter-Metadata"] == "enabled"
    clean = {"id": "gen-failure", "usage": {"cost": 0.2, "output_tokens": 8},
             "error_type": "authentication", "error": {"message": "[REDACTED]"}}
    assert messages == [{"type": "transport.http_error", "status": 500,
                         "body": clean, "response": clean}]
    assert KEY not in json.dumps(messages)
    fake = FakeTransport(messages)
    with pytest.raises(AdapterError) as caught:
        openrouter.OpenRouterAdapter(KEY, transport=fake).complete(request())
    assert caught.value.cost_usd == 0.2 and caught.value.generation_id == "gen-failure"
    assert caught.value.usage is not None
    assert caught.value.usage["output"] == 8


def _silent_worker(pipe, *args):
    time.sleep(30)


def test_elapsed_deadline_stops_silent_worker_and_leaves_no_background_process(monkeypatch):
    monkeypatch.setattr(http_stream, "_http_worker", _silent_worker)
    before = {p.pid for p in multiprocessing.active_children()}
    start = time.monotonic()
    with pytest.raises(AdapterError, match="elapsed deadline") as caught:
        list(http_stream.response_events("https://fake.invalid", KEY, {}, 0.2))
    assert caught.value.kind == "timeout" and time.monotonic() - start < 3
    assert {p.pid for p in multiprocessing.active_children()} == before




def test_missing_key_prevents_dispatch():
    fake = FakeTransport([])
    with pytest.raises(AdapterError, match="paid execution is disabled"):
        openrouter.OpenRouterAdapter(transport=fake).complete(request())
    assert fake.calls == []


@pytest.mark.parametrize("output", [[None], ["bad item"], None,
                                    [{"type": "message", "content": None}],
                                    [{"type": "message", "content": [None]}],
                                    [{"type": "function_call", "call_id": None}]])
def test_malformed_nested_output_preserves_partial_and_known_charge(output):
    fake = FakeTransport([{"type": "response.output_text.delta", "delta": "Received partial"},
                          {"type": "response.completed", "response": completed(output=output)}])
    with pytest.raises(AdapterError) as caught:
        openrouter.OpenRouterAdapter(KEY, transport=fake).complete(request())
    error = caught.value
    assert error.kind == "permanent" and error.partial_text == "Received partial"
    assert error.cost_usd == 0.001 and error.generation_id == "gen-test-1"
    assert error.details is not None


def test_failure_details_keep_reason_but_remove_echoed_key():
    data = completed(status="failed", error={"code": "server_error", "message": KEY})
    fake = FakeTransport([{"type": "response.failed", "response": data}])
    with pytest.raises(AdapterError) as caught:
        openrouter.OpenRouterAdapter(KEY, transport=fake).complete(request())
    assert KEY not in json.dumps(caught.value.details)
    assert "server_error" in json.dumps(caught.value.details)










def test_model_protocol_mapping_survives_configuration_rename():
    renamed = replace(CONFIG, config_id="renamed-condition")
    assert openrouter.request_body(request(renamed))["reasoning"] == {
        "effort": "medium"}






def test_router_metadata_records_selected_provider_without_inventing_missing_identity():
    metadata = {"requested": CONFIG.model, "attempt": 1,
                "endpoints": {"available": [{"provider": "OpenAI", "selected": True}]}}
    data = completed(provider=None, openrouter_metadata=metadata)
    fake = FakeTransport([{"type": "response.completed", "response": data}])
    response = openrouter.OpenRouterAdapter(KEY, transport=fake).complete(request())
    assert response.provider_reported == "OpenAI"
    assert response.settings_reported is not None
    assert response.settings_reported["openrouter_metadata"] == metadata
    assert openrouter._provider({}) is None
