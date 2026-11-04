"""Offline SDK smoke check: python -m evals.foundation_check. No .env is read."""
from __future__ import annotations

import json
import uuid

import httpx
from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult

from evals.langfuse_foundation import session
from evals.privacy import redact


class LocalExporter(SpanExporter):
    """Fake destination collecting final exported attributes without network access."""

    def __init__(self):
        self.attributes: list[dict] = []
        self.closed = False

    def export(self, spans):
        self.attributes.extend(dict(span.attributes or {}) for span in spans)
        return SpanExportResult.SUCCESS

    def shutdown(self):
        self.closed = True


def check() -> dict:
    secret = 'synthetic-secret-for-local-check'
    payloads: list[dict] = []

    def receive(request: httpx.Request) -> httpx.Response:
        payloads.append(json.loads(request.content))
        return httpx.Response(202, json={'message': 'Accepted'})

    exporter = LocalExporter()
    transport = httpx.Client(transport=httpx.MockTransport(receive))
    env = {'LI_LANGFUSE': 'on', 'LANGFUSE_PUBLIC_KEY': f'local-{uuid.uuid4().hex}',
           'LANGFUSE_SECRET_KEY': secret, 'LANGFUSE_BASE_URL': 'https://example.invalid'}
    with session({}) as disabled:
        if disabled is not None:
            raise RuntimeError('disabled check created a client')
    with session(env, span_exporter=exporter, httpx_client=transport) as client:
        if client is None:
            raise RuntimeError('enabled check did not create a client')
        with client.start_as_current_observation(name='foundation-check', input=secret) as span:
            span.update(output='synthetic answer', metadata={'secret_probe': secret})
            # Score/API payloads do not pass through the trace masking hook.
            client.create_score(name='synthetic-check', value=1, data_type='BOOLEAN',
                                trace_id=span.trace_id, comment=redact(secret, [secret]))
    encoded = json.dumps([exporter.attributes, payloads])
    if (len(exporter.attributes) != 1 or not payloads or secret in encoded
            or '[REDACTED]' not in encoded or not exporter.closed or not transport.is_closed):
        raise RuntimeError('local SDK export/masking/lifecycle check failed')
    return {'local_check': 'passed', 'observations': 1, 'score_batches': len(payloads),
            'destination': 'in-memory fake', 'remote_delivery_verified': False}


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
