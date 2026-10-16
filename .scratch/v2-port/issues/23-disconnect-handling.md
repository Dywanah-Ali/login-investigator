# 23: Clean disconnect handling for streamed answers

**Status:** claimed
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

- [ ] Both fast and backpressured disconnects exit cleanly, with no error log or accepted exception
- [ ] Core closes before request release; a follow-up is accepted
- [ ] Similar exceptions from other code, before disconnect, before SSE starts, or mixed with other failures remain visible
- [ ] Existing stream payloads and errors remain unchanged
- [ ] Targeted tests, full backend tests and type check pass

## Comments

2026-10-16: use the already agreed API seam. Strengthen the existing real-model-fixture ASGI
regression first; no test will tolerate the known exception after the fix.
