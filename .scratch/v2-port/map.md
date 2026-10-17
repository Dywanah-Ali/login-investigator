# Map: v2-port

Label: wayfinder:map

## Destination

Every decision the short v2 spec (formerly "PRD", renamed by the author on 14 October 2026) needs is
made and recorded in a ticket. The spec itself is written
outside this map, as its first hand-off. It covers the same behaviour in a new shell, the API
contract, and the seams.

## Notes

- **Domain.** Read `GLOSSARY.md` first. Key terms: **Port**, **Parity**, **Investigation**. Starting
  input: `docs/migration-brief.md`.
- **Facts about v1** found while charting live in [v1-facts.md](v1-facts.md). Read the part a
  ticket needs, not the whole file.
- **Skills.** Grilling tickets call `mp-grilling` and `mp-domain-modeling`. Prototype tickets call
  `mp-prototype`. Research tickets call `mp-research`.
- **v1 access.** v1 is at `../login-investigator`, read-only. `.claude/settings.local.json` adds it
  as a working directory and denies every Edit and Write inside it. Never change v1.
- **Interviews.** Questions to the author go through the AskUserQuestion tool, up to four per call,
  recommended option first.
- **Screens.** Agreed inside this map: pick the template, then agree how each of the four screens
  maps onto it, with rough prototypes. No UI code before that.
- **After the map (author's decision, 14 October 2026).** The spec is written by `/mp-to-spec` at
  `.scratch/v2-port/spec.md` and carries a decisions log under Further notes. Build tickets from
  `/mp-to-tickets` go in this same folder, `issues/10-…` onward, one file per ticket.
- **Research output.** This folder is not a git repo yet, so research findings are saved under
  `research/` instead of a throwaway branch. Nothing is pushed.

### Charting decisions (14 October 2026, the author's answers)

| Topic | Decision |
|---|---|
| Destination | As above |
| Users | Single user, no login, as in v1 (v1 PRD, Out of scope) |
| Template and framework | Chosen together, in one prototype ticket, after the research ticket |
| Parity | Must include a check at the API level, such as running the eval set through the API |
| Inventory | Done during charting, in [v1-facts.md](v1-facts.md). No inventory ticket |
| Investigation keeping | v1 already answers it (random ID, list table, one SQLite file, one agent per server). The leftovers go to [The API contract](issues/09-api-contract.md) |

### Housekeeping noticed (not part of any ticket)

- `docs/agents/issue-tracker.md` pointed to `triage-labels.md`, which does not exist. Fixed 14 October 2026: the five label names are now inline.
- `docs/agents/domain.md` mentioned skills not installed here. Fixed 14 October 2026: it names `mp-grilling` and `mp-wayfinder` instead.
- The folder is not a git repository yet.

## Decisions so far

<!-- one line per resolved ticket: [title](link): gist -->

- [shadcn/ui templates and the frameworks they need](issues/04-shadcn-templates.md): shadcn/ui recommends no framework and a Vite SPA is fully supported; no template covers all four screens, the official dashboard-01 + tasks table + message components compose to about 3,000 lines with Recharts and TanStack Table, while shadcn-admin (Vite) has every screen shape at 15,000 lines and all chat templates need Next.js.
- [How the agent stream reaches the browser](issues/06-agent-stream.md): Server-Sent Events over `POST /investigations/{id}/ask` via FastAPI's `EventSourceResponse` (0.135+), read with `fetch` and a stream reader (not `EventSource`), aborted on unmount; events `text`, `tool`, `error`, `done`.

- [Pick the template and framework](issues/05-pick-template.md): official shadcn/ui pieces composed by hand (`dashboard-01` shell and Overview, tasks table example for the two tables, `message` components for the chat) on Vite + React Router declarative mode; Recharts v3 via the shadcn `chart` component. Rejected shadcn-admin (12,000 of 15,000 lines deleted) and Next.js (server framework with no server work). Prototype: [research/05-template-prototype.html](research/05-template-prototype.html).
- [Map the four screens onto the template](issues/07-map-screens.md): filters in a toolbar on the three dashboard screens, sidebar is navigation only; alert evidence in a side panel; filter state in the URL as search parameters carried on every request; past investigations in a second column inside the Investigator page; stacked bars and horizontal bars via Recharts; agent answers rendered through an allowlist markdown renderer (no links, images or raw HTML, guarded by a test with the injection strings), report as plain fixed fields, log fields only in table cells. Prototype: [research/07-screens-prototype.html](research/07-screens-prototype.html).
- [Screen-layer logic](issues/01-screen-layer-logic.md): meaning in the core (date resolution, dataset facts, alerts for a view sorted newest first, report offer), presentation in the frontend (name cutting, counts, paging, explorer jump as a route), IP validated at both ends, agent tools unchanged from v1; each piece has a test home for ticket 08.

- [Do the course rules bind v2](issues/02-course-rules.md): the rule no longer binds v2 (author's ruling); the agent nonetheless stays as v1 builds it for the Port, by choice; transport, server-lifetime agent and shared checkpointer are plain FastAPI work; any later move to a custom graph is a PRD decisions-log row.

- [Repo layout: one repo or two](issues/03-repo-layout.md): one repository, `backend/` (core copied from v1 plus a separate `api/` package) and `frontend/` (Vite) with docs at the root; seams stay in the core's `tools.py`, `agent.py` and loader; two terminals with Vite proxying to FastAPI; `git init` at the end of the wayfinder, name `login-investigator`, fresh history.

- [The API contract](issues/09-api-contract.md): written at `docs/api-contract.md`, approved by the author. One endpoint per screen (`/api/overview`, `/api/alerts`, `/api/explorer`) taking the shared filters as query parameters; create-then-ask for Investigations (`POST /api/investigations`, then `POST /api/investigations/{id}/ask` over SSE); report by request text matching the core's offer; PDF by ID and report number; `GET /api/dataset` and `GET /api/rules` for the facts the frontend must not hard-code; one error shape, no echoed input; a missing model key leaves the dashboards working and the investigation endpoints at 503; configuration by environment so the eval runner isolates a run. "Investigate" on an alert kept, frontend only, by the author's ruling.

- [What proves Parity](issues/08-parity.md): the 254 core tests copied unchanged plus adapted tests for moved logic and a boundary test that also forbids FastAPI; API tests replaying the data-checking screen tests; the eval set in a new API mode (runner starts its own server, isolated memory, no key) with the v1 target unchanged (90%, 100% security, 19 x 3) and v1's results history carried over; Vitest for the frontend logic and the allowlist renderer; a manual checklist and the eight-step scenario closed by the author's dated ruling, no screenshots and no browser tool; the three engineering checks kept. Written into the PRD as the acceptance criteria.

- [Log explorer, end to end](issues/15-log-explorer-end-to-end.md): full filtered rows and CSV share one core search; five explicit counts, IP validation at both boundaries, shared table pager and quiet supporting surface. Automated checks passed and the author approved the live layout on 16 October 2026.

- [Investigations API](issues/16-investigations-api.md): persisted Investigations, streamed answers, readable tool evidence, numbered reports and offline PDF downloads. Author reviewed and approved on 16 October 2026. B-014 is tracked separately in ticket 23.

- [Clean disconnect handling](issues/23-disconnect-handling.md): the ask route handles the known FastAPI queue-close error after a confirmed disconnect while preserving genuine failures. 351 backend tests and Pyright passed; both reviews found no issues. Author approved on 16 October 2026.

- [The agent's tools follow the settings](issues/22-agent-tools-follow-settings.md): startup hands the loaded log, findings and reputation folder to the agent's tools, so the screens and the agent read the same data; a log that fails validation makes the log tools refuse instead of falling back. Design chosen on researched evidence; 356 backend tests and Pyright passed; two-axis review fixes applied. Author approved on 17 October 2026.

- [Tests never see the real keys](issues/24-tests-never-see-real-keys.md): found during ticket 22. One guard for the whole test run switches off `.env` loading and removes both key names, so no test can spend real quota or send log IPs out; the app and eval runner still load `.env`. A spec-review hole for apps shared by a module was fixed. 359 backend tests and Pyright passed. Author chose review and merge on 17 October 2026.

- [Investigator screen](issues/17-investigator-screen.md): approved second-column layout, distinct user messages, in-chat welcome and starters, tool-call counts, stable first-question handover, centred Send and gradual report reveal matched to observed answer pace. All 114 frontend tests pass; Standards and Spec reviews clear. Author accepted the live screen on 16 October 2026.

## Not yet specified

- Nothing. The map is complete (14 October 2026): every decision the spec needs is recorded.
  Hand-offs done the same day: `spec.md` written by `/mp-to-spec`; build tickets `issues/10` to
  `issues/19` written by `/mp-to-tickets`. Tickets 10–17 are resolved. The build frontier is ticket 18, Eval runner in API mode.
  The targeted B-014 disconnect follow-up, [ticket 23](issues/23-disconnect-handling.md), is also
  resolved following the author's approval on 16 October 2026. Frontend warnings stay separate.
  Ticket 17 is resolved following the author’s live screen acceptance on 16 October 2026.
  Ticket 22, which blocked ticket 18, is resolved following the author's approval on 17 October
  2026. Ticket 24, real keys kept out of test runs, is resolved the same day.
  Ticket 18 is implemented and `ready-for-human`: the full API benchmark passed at 56/57
  (98%) overall and 15/15 (100%) security, with v1's final prompt and unchanged grader.
  370 backend tests, type checks and both reviews pass. One failed stream is retained in
  the score and logged as B-041. Author review is next; ticket 19 follows acceptance of 18.

## Out of scope

- The five future features: RAG, knowledge graph, tracing, eval platforms, log upload. Their seams
  stay in scope.
- Any change to v1.
- Any new behaviour v1 lacks. One agreed exception: the "Investigate" link on an alert, frontend
  only, by the author's ruling in [The API contract](issues/09-api-contract.md).
- Deploying or hosting v2.
