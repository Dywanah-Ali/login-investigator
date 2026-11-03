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

from evals.comparison import __main__ as cli
from evals.comparison import (
    http_stream,
    mirror,
    openrouter,
    plans,
    records,
    roles,
    runner,
)
from evals.comparison.adapters import AdapterError, ModelRequest

KEY = "fake-openrouter-key-only-for-tests"
CONFIG = plans.SCREENING_CONFIGS[-1]


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


@pytest.mark.parametrize("config", plans.SCREENING_CONFIGS, ids=lambda c: c.config_id)
def test_each_requested_configuration_has_no_caps_fallback_or_remote_memory(config):
    original = config.to_dict()
    body = openrouter.request_body(request(config))
    assert config.to_dict() == original
    assert body["model"] == config.model
    assert body["provider"] == {"only": [config.provider], "order": [config.provider],
                                "allow_fallbacks": False, "require_parameters": True}
    assert body["service_tier"] == "default" and body["store"] is False
    assert body["reasoning"]["effort"] == config.reasoning["effort"]
    assert not {"max_output_tokens", "max_tokens", "max_completion_tokens", "previous_response_id",
                "models", "max_tool_calls"} & body.keys()
    for name, value in config.sampling.items():
        assert body[name] == value
    if config.provider == "anthropic":
        assert body["reasoning"] == {"enabled": True, "effort": "medium"}
    if config.config_id in ("gpt-6-luna", "gpt-6.1-sol"):
        assert body["reasoning"]["mode"] == "standard"
        assert body["reasoning"]["context"] == "all_turns"


def test_unapproved_service_and_fallback_settings_are_refused():
    for config in (replace(CONFIG, allow_fallbacks=True), replace(CONFIG, service_tier="priority")):
        with pytest.raises(ValueError):
            openrouter.request_body(request(config))


def test_upstream_debug_is_requested_only_for_tool_compatibility():
    assert "debug" not in openrouter.request_body(request())
    body = openrouter.request_body(request(tools=[roles.COMPATIBILITY_TOOL]))
    assert body["debug"] == {"echo_upstream_body": True}


def test_upstream_debug_is_saved_redacted_and_never_replayed_as_model_input():
    debug = {"echo_upstream_body": {"reasoning_effort": "medium", "secret": KEY}}
    fake = FakeTransport([{"debug": debug},
                          {"type": "response.completed", "response": completed()}])
    response = openrouter.OpenRouterAdapter(KEY, transport=fake).complete(
        request(tools=[roles.COMPATIBILITY_TOOL]))
    assert response.continuation is not None
    assert response.continuation["debug_events"] == [
        {"echo_upstream_body": {"reasoning_effort": "medium", "secret": "[REDACTED]"}}]
    body = openrouter.request_body(request(messages=[
        {"role": "assistant", "content": response.text, "continuation": response.continuation}]))
    assert body["input"] == completed()["output"]
    assert "debug_events" not in json.dumps(body) and KEY not in json.dumps(response.continuation)
    assert mirror.mask({"continuation": response.continuation, "cost": 0.001}) == {"cost": 0.001}


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


def test_tool_round_trip_replays_ordered_reasoning_opaque_fields_and_call_ids(tmp_path):
    output = [{"type": "reasoning", "id": "rs-1", "encrypted_content": "opaque-data",
               "signature": "sig", "summary": [], "content": []},
              {"type": "function_call", "id": "fc-1", "call_id": "call-1", "name": "get_record",
               "arguments": '{"ref":"CMP-1"}'}]
    calls = []

    def transport(url, key, body, timeout):
        calls.append(body)
        assert key == KEY
        assert body["tools"] == [{"type": "function", **roles.COMPATIBILITY_TOOL["function"]}]
        if len(calls) == 1:
            assert len(body["input"]) == 2
            data = completed(output=output)
        else:
            assert body["input"][2:4] == output
            assert body["input"][4] == {"type": "function_call_output", "call_id": "call-1",
                                        "output": json.dumps({"ref": "CMP-1", "text":
                                                               roles.COMPATIBILITY_RECORDS["CMP-1"]})}
            data = completed(output=[{"type": "message", "role": "assistant", "content": [
                {"type": "output_text", "text": "The colour code is 7 [CMP-1]."}]}])
        yield {"type": "response.completed", "response": data}

    adapter = openrouter.OpenRouterAdapter(KEY, transport=transport)
    bundle = runner.new_run(tmp_path / "run", stage="compatibility", configs=[CONFIG],
                            case_ids=[], passes=1, designs=["compat"], adapter=adapter,
                            experiment_id="fake-openrouter")
    runner.Runner(bundle, adapter).run()
    checks = next(e for e in bundle.events() if e["type"] == "compatibility_checks")
    assert checks["tool_round_trip"] and checks["output_contract"]
    assert len(calls) == 2
    starts = [e for e in bundle.events() if e["type"] == "request_started"]
    assert [json.loads(bundle.read_artifact(e["wire_input"]))["body"] for e in starts] == calls
    assert KEY not in "".join(p.read_text() for p in bundle.root.rglob("*") if p.is_file())


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


def test_creating_live_manifest_does_not_load_keys_and_dispatch_requires_execution_flag(
        tmp_path, monkeypatch, capsys):
    import dotenv

    def forbidden(*args, **kwargs):
        pytest.fail("must not load credentials or call transport")

    monkeypatch.setattr(dotenv, "dotenv_values", forbidden)
    monkeypatch.setattr(openrouter.OpenRouterAdapter, "complete", forbidden)
    path = str(tmp_path / "live-plan")
    assert cli.main(["new", "compatibility", path, "--adapter", "openrouter"]) == 0
    assert cli.main(["run", path]) == 1
    assert "--execute-paid" in capsys.readouterr().err
    assert records.RunBundle.open(tmp_path / "live-plan").events() == []


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


@pytest.mark.parametrize("preparation_s,expected_calls", [(590, 1), (610, 0)])
def test_slow_wire_preparation_consumes_case_deadline(tmp_path, monkeypatch, preparation_s,
                                                    expected_calls):
    from tests.test_comparison_runner import answer, finished, make

    bundle, adapter, run = make(tmp_path, answer(), configs=[CONFIG], cases=["O1-02"], passes=1)

    def slow_details(request):
        adapter.clock.advance(preparation_s)
        return {"fake": "wire body"}

    monkeypatch.setattr(adapter, "request_details", slow_details)
    run.run()
    assert len(adapter.requests) == expected_calls
    if expected_calls:
        assert adapter.requests[0].timeout_s == 10
        event = next(e for e in bundle.events() if e["type"] == "request_finished")
        assert event["dispatch_timeout_s"] == 10
    else:
        assert next(iter(finished(bundle).values()))["status"] == "timeout"
        assert next(e for e in bundle.events() if e["type"] == "request_finished")["status"] == "timeout"


def test_spending_pause_happens_before_next_trial(tmp_path):
    from evals.comparison.adapters import ModelResponse
    from tests.test_comparison_runner import make

    bundle, adapter, run = make(tmp_path, lambda r, n: ModelResponse(text="Answer", cost_usd=15),
                                configs=[CONFIG], cases=["O1-02", "O1-06"], passes=1)
    result = run.run(stop_cost_usd=15)
    assert len(adapter.requests) == 1 and result["stop_reason"]
    assert len(records.trial_states(bundle)) == 1


def test_live_run_needs_bound_and_first_pass_review_before_loading_keys(tmp_path, monkeypatch):
    import dotenv

    def forbidden(*args, **kwargs):
        pytest.fail("must not load credentials")

    monkeypatch.setattr(dotenv, "dotenv_values", forbidden)
    path = str(tmp_path / "screen")
    assert cli.main(["new", "screening", path, "--adapter", "openrouter"]) == 0
    assert cli.main(["run", path, "--execute-paid"]) == 1
    assert cli.main(["run", path, "--execute-paid", "--until-slot", "72"]) == 1
    assert records.RunBundle.open(tmp_path / "screen").events() == []


def test_related_run_cost_is_included_in_spending_pause(tmp_path):
    from tests.test_comparison_runner import answer, make

    bundle, adapter, run = make(tmp_path, answer(), configs=[CONFIG], cases=["O1-02"], passes=1)
    result = run.run(stop_cost_usd=15, prior_cost_usd=15)
    assert result["stop_reason"] and adapter.requests == []
    assert records.trial_states(bundle) == {}


def test_model_protocol_mapping_survives_configuration_rename():
    renamed = replace(CONFIG, config_id="renamed-condition")
    assert openrouter.request_body(request(renamed))["reasoning"] == {
        "effort": "medium", "mode": "standard", "context": "all_turns"}


def test_live_manual_workflow_uses_only_fake_keys_and_fake_responses(tmp_path, monkeypatch):
    import dotenv

    from evals.comparison.adapters import ModelResponse

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(dotenv, "dotenv_values", lambda *a: {"OPENROUTER_API_KEY": KEY})
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    sent = []

    def fake_complete(self, request):
        sent.append(request)
        if request.tools and request.messages[-1]["role"] != "tool":
            return ModelResponse(text="", tool_calls=[{"id": "fake-call", "name": "get_record",
                                                       "arguments": '{"ref":"CMP-1"}'}],
                                 cost_usd=0.001)
        return ModelResponse(text="The colour code is 7 [CMP-1].", cost_usd=0.001)

    monkeypatch.setattr(openrouter.OpenRouterAdapter, "complete", fake_complete)
    compat = "evals/comparison/runs/compat-live"
    screen = "evals/comparison/runs/screen-live"
    assert cli.main(["new", "compatibility", compat, "--adapter", "openrouter"]) == 0
    assert cli.main(["run", compat, "--execute-paid", "--until-slot", "1"]) == 0
    assert len(sent) == 2
    # Complete compatibility with the same documented bound mechanism, still fake.
    assert cli.main(["run", compat, "--execute-paid", "--until-slot", "6"]) == 0
    assert len(sent) == 12
    assert cli.main(["new", "screening", screen, "--adapter", "openrouter"]) == 0
    assert cli.main(["run", screen, "--execute-paid", "--until-slot", "1", "--cost-run", compat]) == 0
    assert len(sent) == 13
    assert cli.main(["run", screen, "--execute-paid", "--until-slot", "72", "--cost-run", compat,
                     "--after-setup-review"]) == 1
    assert len(sent) == 13
    assert cli.main(["run", screen, "--execute-paid", "--until-slot", "24", "--cost-run", compat]) == 0
    assert cli.main(["run", screen, "--execute-paid", "--until-slot", "72", "--cost-run", compat,
                     "--after-setup-review"]) == 0
    assert len(sent) == 84
    bundle = records.RunBundle.open(tmp_path / screen)
    event = next(e for e in bundle.events() if e["type"] == "spending_context")
    assert event["known_cost_usd"] == pytest.approx(0.012)
    assert event["unknown_cost_requests"] == 0
    assert cli.main(["run", screen, "--execute-paid", "--until-slot", "1",
                     "--cost-run", compat, "--cost-run", compat]) == 1
    compat_bundle = records.RunBundle.open(tmp_path / compat)
    original = compat_bundle.manifest["schedule"][0]["trial_id"]
    runner.schedule_rerun(compat_bundle, original, reason="fake repair", repair_version="fake-1")
    assert cli.main(["run", compat, "--execute-paid", "--until-slot", "7"]) == 0
    assert len(sent) == 86


def test_screening_repair_does_not_dispatch_unstarted_later_passes(tmp_path):
    from tests.test_comparison_runner import answer, make

    bundle, adapter, run = make(tmp_path, answer())
    run.run(until_slot=24)
    original = bundle.manifest["schedule"][0]["trial_id"]
    linked = runner.schedule_rerun(bundle, original, reason="fake adapter fix", repair_version="v2")
    result = run.run(until_slot=73, reruns_only=True)
    assert result["ran"] == [linked] and len(adapter.requests) == 25
    assert len(records.trial_states(bundle)) == 25
    assert bundle.manifest["schedule"][24]["trial_id"] not in records.trial_states(bundle)


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
