# 16: Investigations API

**What to build:** everything the Investigator screen and the eval runner need from the server,
without a browser. A tester can start an Investigation, ask a question and read the answer as it
streams, reopen it with every Turn and its tool views, request the report when it is offered, and
download the PDF. The dashboards keep working when the model key is missing.

**Blocked by:** 12 (API foundation and the Overview endpoint).

**Status:** claimed

Spec: [spec.md](../spec.md), "The API" and "The stream". Contract: investigations (list, start, reopen,
ask, report, PDF), errors. Decisions: ticket 06, findings under `research/`.

- [ ] List (full, newest first), start (201 with the ID; create only), reopen (Turns with tool views and reports, plus the core's Report offer; 404 when unknown)
- [ ] Ask: SSE over POST with FastAPI's event-source response; events `tool`, `text`, `error`, `done` with the contract's data; `done` carries nothing; failures before the first byte are normal 404, 422 or 503 replies; a second ask while one streams is 409 `busy`
- [ ] Tool views shaped by the core's describe function run in the API: title, asked, found, column order, rows or null, raw
- [ ] Report: the request text must equal the current Report offer, else 409 `not_offered`; not streamed; the reply includes the report's number
- [ ] PDF by ID and number with the contract's headers; works without a model key
- [ ] Missing model key: Investigation endpoints answer 503 `agent_unavailable` with the contract's fixed message; dashboard endpoints unaffected
- [ ] One agent per process; memory per Investigation ID in the one SQLite file at the configured path; an Investigation survives a server restart
- [ ] Mid-stream failure sends the `error` event with fixed text; exception text is logged, never sent
- [ ] API tests for every point above, using the copied agent test fixtures for the model

## Comments

2026-10-16: implementation started with the implement and tdd skills. The agreed seam is
the HTTP API, using the copied fake model and a temporary real SQLite file. Review baseline:
`cc3c113`. No UI work or spec changes.
