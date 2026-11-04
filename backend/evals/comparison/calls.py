"""Record one model request. Scheduling, roles, retries and scoring belong to future callers."""
from __future__ import annotations

import json
import re
import time
from collections.abc import Callable
from dataclasses import asdict

from evals.comparison.adapters import Adapter, AdapterError, ModelRequest, ModelResponse
from evals.comparison.records import RunBundle


def record_call(bundle: RunBundle, adapter: Adapter, request: ModelRequest, *,
                request_id: str, clock: Callable[[], float] = time.monotonic) -> ModelResponse:
    """Persist start before dispatch and outcome before return/raise. Never retry implicitly.

    IDs identify attempts, including failed ones. A caller must use a new ID for another
    attempt. The returned response retains tool continuation data for a caller to use.
    """
    if not re.fullmatch(r'[A-Za-z0-9_-]+', request_id):
        raise ValueError('request_id must contain only letters, digits, underscores or hyphens')
    if any(e.get('request_id') == request_id for e in bundle.events()):
        raise ValueError('request_id already recorded; use a new ID for a new attempt')
    input_ref = bundle.write_artifact(f'inputs/{request_id}.json', json.dumps(asdict(request)))
    bundle.append('request_started', request_id=request_id, input=input_ref)
    started = clock()
    try:
        response = adapter.complete(request)
    except AdapterError as error:
        answer = bundle.write_artifact(f'answers/{request_id}.txt', error.partial_text)
        bundle.append('request_finished', request_id=request_id, status=error.kind,
                      elapsed_s=clock() - started, answer=answer, usage=error.usage,
                      cost_usd=error.cost_usd, generation_id=error.generation_id)
        raise
    except BaseException:
        # Cancellation/unexpected failure may follow a billed request. Never guess a charge
        # or persist arbitrary exception text that could contain credentials.
        bundle.append('request_unresolved', request_id=request_id,
                      elapsed_s=clock() - started, reason='call interrupted; outcome unknown')
        raise
    answer = bundle.write_artifact(f'answers/{request_id}.txt', response.text)
    bundle.append('request_finished', request_id=request_id,
                  status='completed' if response.text or response.tool_calls else 'no_answer',
                  elapsed_s=clock() - started, answer=answer, usage=response.usage,
                  cost_usd=response.cost_usd, generation_id=response.generation_id,
                  model_reported=response.model_reported, provider_reported=response.provider_reported)
    return response
