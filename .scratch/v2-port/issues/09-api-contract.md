# The API contract

Type: grilling
Status: resolved
Blocked by: 01, 06, 07
Map: [map.md](../map.md)

## Question

Write the API contract: every endpoint with its input and output shape, before anything is built.
This is v2's central document and goes into the PRD.

Inputs: where screen logic landed ([Screen-layer logic](01-screen-layer-logic.md)), the stream
transport ([How the agent stream reaches the browser](06-agent-stream.md)), and the agreed screens
([Map the four screens onto the template](07-map-screens.md)).

Areas the contract must cover:

- **Dashboard.** Summary counts, hourly counts, top failed IPs, findings, filtered log rows, and
  the filter values the sidebar offers (countries, users, date bounds). The shared filters travel
  with each request.
- **Investigations.** List, start, reopen (full history with turns, tool calls and reports), ask a
  question (streamed), write or update the incident report, download the report PDF. v1 keeps a
  random ID per Investigation, a small list table and the `SqliteSaver` memory in one SQLite file,
  with one agent per server process; confirm v2 keeps that.
- **Tool-calls panel.** `tool_views.describe` returns a pandas table; decide its JSON shape.
- **Metadata.** The capture date and the "Synthetic data" label, served by the API so the frontend
  never hard-codes them.
- **Errors.** One error shape, and what a tool failure or a missing key looks like to the page.
- **Trust boundary.** Only the fields the screen needs leave the server. Log fields are data.
- **Seams.** The API asks the core for "a dataset", not one fixed file, without building upload.

Resolving this ticket may graduate the remaining fog ("How the seams show in the code layout",
"Running two servers locally") or rule the map complete.

## Comments

- 14 October 2026, from [What proves Parity](08-parity.md): the eval runner's API mode drives three
  endpoints without a browser: start an investigation, ask (stream), write the report. The server
  must take its memory file path and port from configuration so the runner can isolate a run.

## Answer

Grilled with the author on 14 October 2026, one question at a time in chat at the author's request.
Four decisions, three answered with the recommended option, one overruled. The contract itself is
written at [docs/api-contract.md](../../../docs/api-contract.md), approved by the author as drafted.
The PRD links to it; later changes go through the PRD's decisions log.

### Decisions

| # | Decision | Choice | Reason |
|---|---|---|---|
| 1 | Shape of the dashboard endpoints | **One endpoint per screen**: `/api/overview`, `/api/alerts`, `/api/explorer`, each taking the shared filters | The API serves one frontend owned by the same people, so it is shaped by the screens ("backend for frontend"). One core filter call per screen; the trust-boundary rule is one assertion per reply; the parity test "a filter change updates every screen consistently" maps one to one |
| 2 | How an Investigation starts | **Create, then ask**: `POST /api/investigations` with the first question returns the ID; `POST /api/investigations/{id}/ask` streams | An ID is a fact the client needs first, so it arrives as plain JSON, not inside a stream. Same two steps as v1, same endpoints for the eval runner. Matches LangChain's hosted server (create thread, then stream a run) |
| 3 | The "Investigate" button on an alert | **Kept, frontend only** (author overruled the recommendation to drop it) | A link to the Investigator with a prepared question in the input box; the user presses send. No API involvement. The one agreed exception to "no new behaviour v1 lacks"; covered by a frontend test |
| 4 | Missing model key | **Dashboards keep working**; investigation endpoints answer 503 `agent_unavailable` naming the setting, never a value | A failure stays inside the part it belongs to, as in v1 where only the Investigator screen fails |

### Shapes settled by the contract (author approved the draft as a whole)

- Shared filters as query parameters `from`, `to`, `outcome`, `country`, `user`, plus `ip` on the
  explorer and the CSV; plain dates in, the core resolves the window; validation at the boundary
  with messages that never echo values.
- `GET /api/dataset` (capture time, "Synthetic data" label, date bounds, countries, users, row
  count); `GET /api/rules` (rule guide and general assumptions).
- Alerts carry `Finding.to_dict()` unchanged, evidence included, sorted by the core; the frontend
  cuts names, counts per rule and builds the explorer link.
- Explorer returns every matching row, newest first; CSV from the same core search.
- Investigations: list (full, newest first), start, reopen (turns with ToolViews and reports, plus
  the core's `report_offer`), ask (SSE events `tool`, `text`, `error`, `done`; `done` carries
  nothing and the frontend reloads the Investigation), report (`request` must equal the current
  offer, else 409 `not_offered`; not streamed), PDF by ID and report number.
- ToolView as `title`, `asked`, `found`, `columns`, `rows` (or null), `raw`; `describe` runs in
  the API.
- One error shape `{"error": {"code", "message"}}` for every status, FastAPI's default replaced;
  mid-stream errors use the `error` event with the same object; exception text never leaves the
  server. 409 `busy` for a second ask while one streams. Questions 1 to 2,000 characters.
- Configuration by environment: `LI_LOG_PATH`, `LI_MEMORY_PATH`, `LI_REPUTATION_DIR`, the two
  keys, and uvicorn's port, so the eval runner isolates a run. Log loaded, rules run, memory opened
  and agent built once each at startup, in one place.
- v1's investigation keeping is confirmed for v2: random ID, one list table and the memory in one
  SQLite file, one agent per server process.

### Fog cleared

Nothing remains in "Not yet specified". No new ticket. The map is complete: every decision the
PRD needs is recorded. Next hand-off: write `docs/PRD.md` outside this map, then tickets, then
`git init`.

### Hand-offs

- PRD: link `docs/api-contract.md` as the contract section; carry the "Investigate" exception into
  the scope section with the author's ruling.
- Ticket 08's gate: the API tests replay against the endpoints named here; the eval runner's API
  mode follows the five steps at the end of the contract.
- `GLOSSARY.md`: Turn, Report offer, Dataset added today.
