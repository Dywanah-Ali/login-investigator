# 23: Clean disconnect handling for streamed answers

**Status:** resolved
**Blocked by:** 16 (resolved)

## Scope

The author approved T16 on 16 October 2026 and authorised investigating a targeted B-014 fix
before T17. Normal disconnection must finish without a server error while preserving cleanup.
Frontend warnings remain separate. No change to the API contract or core behaviour.

## Findings

- Installed FastAPI: 0.143.1. The delivery task writes to a closed queue under backpressure.
- Upstream discussion: https://github.com/fastapi/fastapi/discussions/15725
- Proposed upstream fix was closed without merging: https://github.com/fastapi/fastapi/pull/15824
- Latest listed release 0.143.2 changes frontend fallback checks, not this queue handling:
  https://fastapi.tiangolo.com/release-notes/#01432

## Approach

Use a guard only on the ask route. It must see a successful SSE response and a real HTTP
disconnect before recognising a resource-close exception from FastAPI's keepalive task.
All other errors and unexpected siblings in exception groups must propagate. Do not patch
installed dependencies or filter application-wide logs. If FastAPI internals change, an unmatched
exception continues to surface rather than being hidden. Remove the guard when a verified
upstream fix passes the same strict regression test.

## Acceptance

- [x] Both fast and backpressured disconnects exit cleanly, with no error log or accepted exception
- [x] Core closes before request release; a follow-up is accepted
- [x] Similar exceptions from other code, before disconnect, before SSE starts, or mixed with other failures remain visible
- [x] Existing stream payloads and errors remain unchanged
- [x] Targeted tests, full backend tests and type check pass

## Comments

2026-10-16: use the already agreed API seam. Strengthen the existing real-model-fixture ASGI
regression first; no test will tolerate the known exception after the fix.


## Implementation

- `api/sse_disconnect.py`: full-lifetime route guard. Matching depends on an observed disconnect,
  status 200 with SSE content type, resource-close exception type, and the framework's keepalive
  traceback origin. It never matches exception message text.
- Only `POST /api/investigations/{id}/ask` opts in through `route_class_override`.
- `tests/test_api_investigations.py`: removed the accepted-exception escape hatch. Both fast and
  slow-reader cases now require clean return, no error log, immediate core closure and an accepted
  follow-up. The stronger test reproduced B-014 before the guard was installed.
- `tests/test_api_sse_disconnect.py`: gets the actual upstream exception via an unguarded FastAPI
  endpoint, then checks eight refusal cases through ASGI. This includes unknown origins, errors
  before disconnect or response start, non-SSE or unsuccessful responses, and mixed resource and
  nonresource failures. Unexpected failures still log and do not expose their text to the client.
- Targeted checks: both real disconnect cases and all eight refusal cases passed; Pyright clean.
- No dependency, core, frontend or API contract changes.

## Standards review

No documented-standard breaches or actionable smell findings. The guard is confined to the API
layer and the ask route. It wraps delivery and cleanup; unknown failures and mixed siblings remain
visible. Dependence on FastAPI's internal function name is deliberate and fails visibly after a
rename. Review used `git diff a6e5131...105596c`.


## Spec review

No findings. The guard matches the ticket's scope and preserves the API contract's cancellation
behaviour. It requires successful SSE plus actual disconnect before recognising the framework
origin. Full-lifetime cleanup is preserved, including under backpressure. No frontend changes,
dependency patches, or global logging filters were introduced. Review used
`git diff a6e5131...105596c`.

Review totals: Standards 0 findings; Spec 0 findings.

## Final evidence, 16 October 2026

- Full backend suite: **351 passed**. Pyright: **0 errors, 0 warnings**.
- Strict real Investigation disconnect cases: both passed, with no tolerated exception or error log.
- Guard refusal cases: eight passed, preserving unexpected failures and their server logging.
- `git diff --check`: clean.
- Frontend unchanged; no frontend tests rerun for this backend-only follow-up. Existing warnings
  and bundle-size work remain separate.
- The source-origin match is deliberately temporary. New framework origins remain visible until
  reviewed. Remove the guard only after the same strict regression passes on an upstream fix.
- Implementation committed locally as `105596c`; evidence recorded in a follow-up commit.

Next: author reviews ticket 23, then T17 is the build frontier. Nothing pushed.


## Answer

2026-10-16: the author approved the completed work: "ok T23 is approved".
The passing checks and independent reviews above, together with this approval, close ticket 23.
T17, Investigator screen, is next. The temporary guard's removal condition remains documented.
Nothing pushed.
