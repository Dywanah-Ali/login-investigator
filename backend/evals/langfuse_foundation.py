"""Optional Langfuse connection. The application does not use it until T31.

Own one session per public key per process, for the lifetime of the command/server.
The SDK caches clients by public key; changing projects/settings requires a fresh process.
The native SDK is exposed directly. Explicitly redact score/API payloads before calling it;
the export hook below covers trace attributes, not arbitrary REST API calls.
"""
from __future__ import annotations

import os
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from typing import TYPE_CHECKING
from urllib.parse import urlsplit

from evals.privacy import SECRET_ENV, redact

if TYPE_CHECKING:
    import httpx
    from langfuse import Langfuse
    from opentelemetry.sdk.trace.export import SpanExporter


@contextmanager
def session(env: Mapping[str, str] = os.environ, *,
            span_exporter: SpanExporter | None = None,
            httpx_client: httpx.Client | None = None) -> Iterator[Langfuse | None]:
    """Own SDK, exporter and HTTP lifetimes. Disabled mode reads only the switch.

    Optional transports are for offline checks. Exiting always closes supplied resources.
    SDK export errors are logged by the SDK; successful shutdown is not a delivery receipt.
    """
    switch = env.get('LI_LANGFUSE', '').strip().lower()
    if switch not in ('', 'off', 'on'):
        raise ValueError('LI_LANGFUSE must be on or off')
    if switch != 'on':
        yield None
        return
    names = ('LANGFUSE_PUBLIC_KEY', 'LANGFUSE_SECRET_KEY', 'LANGFUSE_BASE_URL')
    if any(not env.get(name, '').strip() for name in names):
        raise ValueError('Langfuse enabled: set LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY and LANGFUSE_BASE_URL')
    url = env['LANGFUSE_BASE_URL'].strip().rstrip('/')
    parsed = urlsplit(url)
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError('LANGFUSE_BASE_URL must be an HTTPS destination without credentials, query or fragment')

    import httpx
    from langfuse import Langfuse
    from langfuse.types import MaskOtelSpansParams, MaskOtelSpansResult, OtelSpanPatch
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider

    secrets = [env[name] for name in SECRET_ENV if env.get(name)]

    def mask_spans(*, params: MaskOtelSpansParams) -> MaskOtelSpansResult:
        return MaskOtelSpansResult(span_patches={
            identifier: OtelSpanPatch(
                delete_attributes=tuple(span.attributes),
                set_attributes=redact(dict(span.attributes), secrets),
            ) for identifier, span in params.spans.items()
        })

    # Dedicated provider keeps unrelated application telemetry out of this connection.
    provider = TracerProvider(resource=Resource({'service.name': 'login-investigator-evaluation'}))
    transport = httpx_client if httpx_client is not None else httpx.Client(timeout=15, trust_env=False)
    client = None
    try:
        client = Langfuse(public_key=env['LANGFUSE_PUBLIC_KEY'], secret_key=env['LANGFUSE_SECRET_KEY'],
                          base_url=url, httpx_client=transport, tracer_provider=provider,
                          span_exporter=span_exporter, mask_otel_spans=mask_spans,
                          tracing_enabled=True, environment='evaluation', sample_rate=1.0)
        yield client
    finally:
        try:
            if client is not None:
                client.shutdown()
        finally:
            try:
                provider.shutdown()
            finally:
                transport.close()
