"""SDK lifecycle and outbound behavior; all destinations and credentials are fake."""
import socket
from collections.abc import Mapping

import pytest

from evals.langfuse_foundation import session


def test_disabled_does_not_read_keys_or_open_connections(monkeypatch):
    class SwitchOnly(Mapping):
        def __getitem__(self, key):
            assert key == 'LI_LANGFUSE'
            return 'off'
        def __iter__(self):
            return iter(['LI_LANGFUSE'])
        def __len__(self):
            return 1

    def forbidden(*args, **kwargs):
        raise AssertionError('network used while disabled')
    monkeypatch.setattr(socket.socket, 'connect', forbidden)
    with session(SwitchOnly()) as client:
        assert client is None


@pytest.mark.parametrize("secret", ['fake-sensitive-secret-12345', 'short', 'fake-quote"secret\\value'])
def test_real_sdk_exports_masked_observation_and_score_and_closes_resources(secret):
    import json
    import uuid

    import httpx
    from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult

    from evals.privacy import redact

    class Collector(SpanExporter):
        def __init__(self):
            self.spans = []
            self.closed = False
        def export(self, spans):
            self.spans.extend(spans)
            return SpanExportResult.SUCCESS
        def shutdown(self):
            self.closed = True

    requests = []
    def receive(request):
        requests.append(json.loads(request.content))
        return httpx.Response(202, json={'message': 'Accepted'})
    destination = httpx.Client(transport=httpx.MockTransport(receive))
    collector = Collector()
    env = {'LI_LANGFUSE': 'on', 'LANGFUSE_PUBLIC_KEY': 'test-' + uuid.uuid4().hex,
           'LANGFUSE_SECRET_KEY': secret, 'LANGFUSE_BASE_URL': 'https://example.invalid'}
    with session(env, span_exporter=collector, httpx_client=destination) as client:
        assert client is not None
        with client.start_as_current_observation(name='foundation-check', input=secret) as span:
            span.update(output={'answer': secret}, metadata={'note': secret})
            client.create_score(name='synthetic-check', value=1, data_type='BOOLEAN',
                                trace_id=span.trace_id, comment=redact(secret, [secret]))
    assert collector.closed
    assert destination.is_closed
    assert len(collector.spans) == 1
    payload = json.dumps(dict(collector.spans[0].attributes))
    assert secret not in payload and '[REDACTED]' in payload
    attrs = collector.spans[0].attributes
    assert attrs['langfuse.observation.input'] == '[REDACTED]'
    assert json.loads(attrs['langfuse.observation.output']) == {'answer': '[REDACTED]'}
    assert json.loads(attrs['langfuse.observation.metadata.note']) == '[REDACTED]'
    assert requests and secret not in json.dumps(requests)
    assert '[REDACTED]' in json.dumps(requests)
    assert requests[0][0]['name'] == 'synthetic-check'
    assert requests[0][0]['dataType'] == 'BOOLEAN'
    assert requests[0][0]['value'] == 1
    assert requests[0][0]['traceId'] == span.trace_id


def test_export_failure_is_logged_and_shutdown_still_closes(caplog):
    import logging
    import uuid

    import httpx

    from evals.foundation_check import LocalExporter

    class FailingExporter(LocalExporter):
        def export(self, spans):
            raise OSError('synthetic destination unavailable')

    exporter = FailingExporter()
    transport = httpx.Client(transport=httpx.MockTransport(lambda r: httpx.Response(500)))
    env = {'LI_LANGFUSE': 'on', 'LANGFUSE_PUBLIC_KEY': 'test-' + uuid.uuid4().hex,
           'LANGFUSE_SECRET_KEY': 'fake-secret-value', 'LANGFUSE_BASE_URL': 'https://example.invalid'}
    with caplog.at_level(logging.ERROR):
        with session(env, span_exporter=exporter, httpx_client=transport) as client:
            assert client is not None
            with client.start_as_current_observation(name='failure-probe'):
                pass
    assert exporter.closed and transport.is_closed
    assert 'synthetic destination unavailable' in caplog.text
