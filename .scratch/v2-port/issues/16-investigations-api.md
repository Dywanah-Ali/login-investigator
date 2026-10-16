# 16: Investigations API

**What to build:** everything the Investigator screen and the eval runner need from the server,
without a browser. A tester can start an Investigation, ask a question and read the answer as it
streams, reopen it with every Turn and its tool views, request the report when it is offered, and
download the PDF. The dashboards keep working when the model key is missing.

**Blocked by:** 12 (API foundation and the Overview endpoint).

**Status:** ready-for-human

Spec: [spec.md](../spec.md), "The API" and "The stream". Contract: investigations (list, start, reopen,
ask, report, PDF), errors. Decisions: ticket 06, findings under `research/`.

- [x] List (full, newest first), start (201 with the ID; create only), reopen (Turns with tool views and reports, plus the core's Report offer; 404 when unknown)
- [x] Ask: SSE over POST with FastAPI's event-source response; events `tool`, `text`, `error`, `done` with the contract's data; `done` carries nothing; failures before the first byte are normal 404, 422 or 503 replies; a second ask while one streams is 409 `busy`
- [x] Tool views shaped by the core's describe function run in the API: title, asked, found, column order, rows or null, raw
- [x] Report: the request text must equal the current Report offer, else 409 `not_offered`; not streamed; the reply includes the report's number
- [x] PDF by ID and number with the contract's headers; works without a model key
- [x] Missing model key: Investigation endpoints answer 503 `agent_unavailable` with the contract's fixed message; dashboard endpoints unaffected
- [x] One agent per process; memory per Investigation ID in the one SQLite file at the configured path; an Investigation survives a server restart
- [x] Mid-stream failure sends the `error` event with fixed text; exception text is logged, never sent
- [x] API tests for every point above, using the copied agent test fixtures for the model

## Comments

2026-10-16: implementation started with the implement and tdd skills. The agreed seam is
the HTTP API, using the copied fake model and a temporary real SQLite file. Review baseline:
`cc3c113`. No UI work or spec changes.


### Review, 16 October 2026

Fixed point: `cc3c113`; initial implementation commit: `b73b9e0`. The implement skill's
code-review step ran Standards and Spec in separate research agents.

| Axis | Finding | Result |
|---|---|---|
| Standards | Optional duplication of report request wording | API validation now uses the core's `REPORT_REQUESTS`; reviewer confirmed resolved |
| Spec | Some body validation messages omitted the field name | Fixed messages name `question` or `request`; reviewer confirmed resolved |
| Lifecycle follow-up | Endpoint-generator finalization did not guarantee core closure before writer release | Request-scoped stream ownership closes before releasing the reservation; reviewer confirmed adequate |

No remaining material findings on either axis. B-014 records a separate FastAPI 0.143.1
post-disconnect delivery error. The slow-reader test recognises that specific exception only after
a confirmed disconnect, and still requires immediate core closure and an accepted follow-up.


### Implementation evidence, 16 October 2026

- `backend/api/investigation_routes.py`: list, start, reopen, streamed ask, structured report
  and PDF routes. Existing startup still creates exactly one model/agent and one checkpointer.
- The only core additions are model-free `agent.saved_history` for saved PDFs and the precise
  generator return annotation on `ask`. Existing agent behaviour and copied tests stay intact.
- `backend/tests/test_api_investigations.py`: 20 API cases using the copied `FakeModel`, real
  temporary SQLite and real tools. Covers record-only creation, full newest-first list, trimmed
  limits, saved Turns/tool views, null tables, report offers/updates and distinct numbered PDFs,
  restart persistence, missing key, fixed pre-stream errors, writer conflicts, independent IDs,
  failures before/after text, and both fast-reader and backpressured disconnect cleanup.
- Final backend full suite: **343 passed**. Pyright clean.
- Frontend full suite: **90 passed**. TypeScript clean. Production build passed.
- Both review axes confirmed the fixes. `git diff --check` clean. No application UI changes.

Concerns/gaps:

- B-014: FastAPI 0.143.1 may log a post-disconnect `BrokenResourceError` under backpressure.
  Core closure and writer release still pass; no client data or exception text is sent afterward.
- The existing six frontend lint warnings and approximately 920 kB minified bundle warning remain.
  No unrelated changes were made. The existing Pyright ignore list for copied v1 files remains.
- No paid model call or live-model evaluation was made. This ticket specifies fake-model API
  checks; the real API evaluation gate belongs to ticket 18.

Next: the author reviews T16. The ticket remains `ready-for-human` until that review; ticket 17
is the next build ticket after approval. Nothing pushed.
