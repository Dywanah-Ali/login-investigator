"""Reusable request recorder, with fake provider and clock boundaries."""

import pytest

from evals.comparison import calls, records
from evals.comparison.adapters import (
    AdapterError,
    FakeAdapter,
    FakeClock,
    ModelConfig,
    ModelRequest,
    ModelResponse,
)


def test_saved_answer_timing_and_unknown_cost_survive_reopening(tmp_path):
    clock = FakeClock()
    bundle = records.RunBundle.create(tmp_path / 'run', {}, clock)
    request = ModelRequest(ModelConfig('candidate', 'Candidate', 'test/model', 'test', {}),
                           [{'role': 'user', 'content': 'Question'}], 10)
    adapter = FakeAdapter(lambda r, n: ModelResponse('Answer'), clock)
    calls.record_call(bundle, adapter, request, request_id='request-1', clock=clock)
    reopened = records.RunBundle.open(bundle.root)
    events = reopened.events()
    assert events[0]['type'] == 'request_started'
    assert reopened.read_artifact(events[1]['answer']) == 'Answer'
    assert events[1]['elapsed_s'] == 1
    assert events[1]['cost_usd'] is None
    assert records.resources(reopened)['total']['unknown_cost_requests'] == 1


def test_failure_keeps_partial_answer_and_charge_without_retry(tmp_path, monkeypatch):
    monkeypatch.setenv('OPENROUTER_API_KEY', 'fake-sensitive-key-value')
    clock = FakeClock()
    bundle = records.RunBundle.create(tmp_path / 'run', {}, clock)
    request = ModelRequest(ModelConfig('candidate', 'Candidate', 'test/model', 'test', {}), [], 10)
    def fail(r, n):
        assert bundle.events()[0]['type'] == 'request_started'
        return AdapterError('timeout', 'provider timeout', partial_text='partial fake-sensitive-key-value',
                            cost_usd=0.02)
    adapter = FakeAdapter(fail, clock)
    with pytest.raises(AdapterError):
        calls.record_call(bundle, adapter, request, request_id='r1', clock=clock)
    assert len(adapter.requests) == 1
    outcome = bundle.events()[-1]
    assert outcome['status'] == 'timeout' and outcome['cost_usd'] == 0.02
    assert bundle.read_artifact(outcome['answer']) == 'partial [REDACTED]'
    with pytest.raises(ValueError, match='already recorded'):
        calls.record_call(bundle, adapter, request, request_id='r1', clock=clock)
    assert len(adapter.requests) == 1


@pytest.mark.parametrize('secret', ['short', 'fake-quote"secret\\value'])
def test_structured_request_and_answer_remove_configured_secrets(tmp_path, monkeypatch, secret):
    import json
    monkeypatch.setenv('OPENROUTER_API_KEY', secret)
    clock = FakeClock()
    bundle = records.RunBundle.create(tmp_path / 'run', {}, clock)
    request = ModelRequest(ModelConfig('candidate', 'Candidate', 'test/model', 'test', {}),
                           [{'role': 'user', 'content': secret}], 10)
    adapter = FakeAdapter(lambda r, n: ModelResponse(secret), clock)
    calls.record_call(bundle, adapter, request, request_id='r1', clock=clock)
    events = bundle.events()
    assert json.loads(bundle.read_artifact(events[0]['input']))['messages'][0]['content'] == '[REDACTED]'
    assert bundle.read_artifact(events[1]['answer']) == '[REDACTED]'
