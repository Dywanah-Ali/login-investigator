# Spec: the v2 Port

Status: ready-for-agent
Written: 14 October 2026, from the wayfinder map `map.md` and its nine resolved tickets.
Source of truth for scope from this point on. The API contract lives in `docs/api-contract.md` and
is part of this spec by reference. Terms (Port, Parity, Investigation, Turn, Report offer, Dataset)
are defined in the root `GLOSSARY.md`.

## Problem Statement

The Login Investigator v1 is a Streamlit app: a dashboard over a synthetic sign-in log, with an
in-app LangChain agent that investigates it. Later course weeks will add features (RAG, a knowledge
graph, tracing, eval platforms, log upload) in directions not yet fixed. Streamlit cannot grow in
those directions: screens call Python directly, memory lives in the browser session, there is no
written boundary between what is shown and what is computed, and there is no way to drive the app
from outside without the screens.

The analyst wants the same four screens and the same agent, but in a shell that later features can
plug into, and that can be inspected, repeated and handed over.

## Solution

Move v1 into a new shell without changing what it does. A FastAPI backend serves the existing Python
core through a written API contract. A React frontend built from official shadcn/ui pieces on Vite
shows the same four screens: Overview, Alerts, Log explorer, Investigator. The agent, its three
read-only tools, its memory and its incident report are kept as v1 built them.

The Port is accepted only when Parity is proven: the copied core tests, API tests that replay the
old screen tests, the v1 eval set run through the real API, frontend tests for the logic that moved
to the browser, and a manual checklist and the eight-step scenario closed by the author's dated
ruling.

## User Stories

**The analyst, dashboards**

1. As an analyst, I want an Overview with four KPI tiles, sign-ins per hour and top source IPs by
   failed sign-ins, so that I can spot a spike of failed logins overnight at a glance.
2. As an analyst, I want a filter toolbar (date range, outcome, country, user) on the Overview,
   Alerts and Log explorer, so that I can narrow every dashboard screen to the same view.
3. As an analyst, I want a change of filter to update every dashboard screen consistently, so that
   the numbers on one screen never contradict another.
4. As an analyst, I want the filter state carried in the page address, so that I can reload, share
   or bookmark a view and land on the same screen.
5. As an analyst, I want the date pickers, country and user lists to offer only the values the log
   holds, so that I never type a value the data cannot match.
6. As an analyst, I want a filter that matches nothing to show a clear message instead of an empty
   chart or an error, so that I know the filter is the cause.
7. As an analyst, I want a reset that restores the whole log, so that I can start over.
8. As an analyst, I want the "Synthetic data" label and the log's capture date visible on every
   screen, so that I never mistake the data for a real environment.
9. As an analyst, I want every metric to say what it counts in its label, so that I do not have to
   guess what a number means.
10. As an analyst, I want the Alerts screen to list every finding the detection rules produce for the
    filtered view, newest first, so that the latest attack is at the top.
11. As an analyst, I want every planted scenario S1 to S4 to appear on the Alerts screen, so that I
    can trust the rules catch what they claim.
12. As an analyst, I want to click an alert and see its evidence rows in a side panel, so that the
    list stays in place while I look at the detail.
13. As an analyst, I want the alert to show at most three IPs or users and then "and N more", so
    that the table stays readable.
14. As an analyst, I want "Open in Log explorer" on an alert to jump to the explorer with that IP and
    time window already applied, so that I can see the raw rows in one click.
15. As an analyst, I want "Investigate" on an alert to open the Investigator with a prepared question
    in the input box, so that I can hand the alert to the agent without retyping its facts.
16. As an analyst, I want a "How these rules work" section listing each rule, when it fires and its
    assumptions, so that I understand what an alert means.
17. As an analyst, I want the Log explorer to add an IP search on top of the shared filters, so that
    I can pull every row for one address.
18. As an analyst, I want a badly formed IP refused with a message that names the field and never
    repeats what I typed, so that bad input cannot be reflected back as content.
19. As an analyst, I want the explorer's five count tiles and a paged table of every matching row,
    newest first, so that I can browse the raw log.
20. As an analyst, I want a CSV download of exactly the rows in the table, so that file and screen
    never disagree.

**The analyst, Investigator**

21. As an analyst, I want to start a new Investigation with a question, so that one line of inquiry
    gets its own ID.
22. As an analyst, I want to see the agent's progress while it works, with a line naming the tool it
    is running, so that I know it has not stalled.
23. As an analyst, I want the answer to appear as it is written, so that I can read while the agent
    finishes.
24. As an analyst, I want the input locked while the agent answers, so that I cannot send two
    questions into one Turn.
25. As an analyst, I want a "Tools used" panel under each answer with what was asked, what was found,
    a table of rows and the raw result behind a switch, so that I can check the agent's claims.
26. As an analyst, I want a follow-up question answered from memory of the Investigation so far, so
    that I do not repeat context.
27. As an analyst, I want the report button to appear only when a report would add something new,
    with "Write" or "Update" wording chosen by the core, so that stale clicks are impossible.
28. As an analyst, I want the incident report shown as a card with fixed fields (title, severity,
    summary, attacker IPs, affected users, timeline, evidence, next steps), so that every report has
    the same shape.
29. As an analyst, I want to download any report of an Investigation as a PDF, so that I can file it.
30. As an analyst, I want a list of past Investigations (newest three, three more per click, the
    open one always shown), so that I can reopen one and continue it the next day.
31. As an analyst, I want a reopened Investigation to show every Turn with its tools and reports, so
    that nothing is lost between sessions or server restarts.
32. As an analyst, I want starter questions and a scope note in an empty Investigation, so that I
    know what the agent can do.
33. As an analyst, I want an AI note by the input, so that I am reminded the answers come from a
    model.
34. As an analyst, I want the agent to ignore instruction-like text planted in log fields, so that
    the data cannot steer it.
35. As an analyst, I want the agent to decline when asked to block an IP and recommend instead, so
    that it stays read-only.
36. As an analyst, I want an agent failure to show a fixed message and never the exception text, so
    that nothing internal leaks to the screen.
37. As an analyst, I want the dashboards to keep working when the model key is missing, with only
    the Investigator reporting the missing setting by name, so that a failure stays inside the part
    it belongs to.

**The author and reviewers**

38. As the author, I want both servers to start from the README on a fresh clone with two commands,
    so that a reviewer's first ten minutes succeed.
39. As the author, I want every endpoint's input and output written in one contract before it is
    built, so that frontend and backend can be reviewed against the same page.
40. As the author, I want the core to stay plain Python with no FastAPI or Streamlit import, proven
    by a test, so that screens, API and agent tools can never disagree about what the data means.
41. As the author, I want the v1 core tests copied unchanged and passing, so that I know the core did
    not change in the move.
42. As the author, I want the v1 eval set run through the real API with the same pass bar, so that
    Parity is proven on the path a real user takes, not only in the kitchen.
43. As the author, I want v1's eval history carried into v2's results table, so that a regression
    against v1 is visible at a glance.
44. As the author, I want a test that feeds injection strings through the answer renderer and asserts
    no link, image, script or raw HTML survives, so that the renderer's safety is a test and not a
    convention.
45. As the author, I want the frontend small, conventional and composed of official pieces only, so
    that I can review code I did not write.
46. As the author, I want no personal name or email in any file and no key in git history, so that
    the repo can go public.
47. As the author, I want every bug and every build prompt logged as they happen, so that the work
    can be inspected and used in course submissions.

**Future course weeks (seams only, no features)**

48. As a future week adding RAG, I want the agent's tool list to come from one place, so that a new
    tool is one line.
49. As a future week adding tracing, I want the model and agent created in exactly one function, so
    that a hook is one change.
50. As a future week adding a knowledge graph, I want all data access in the core and never in a
    route, so that a second store plugs in beside the first.
51. As a future week running eval platforms, I want the evals to call the core or the API and never
    the screens, so that any platform can drive them.
52. As a future week adding log upload, I want the API to ask the core for "a dataset" from a
    configured source, so that a dataset per user is a change in one place.

## Implementation Decisions

Each decision names the ticket that made it.

**Scope and method**

- Same behaviour in a new shell. v2 does nothing v1 does not, with one agreed exception: the
  "Investigate" link on an alert, frontend only, by the author's ruling (ticket 09).
- The course's "LangChain only as taught" rule does not bind v2. The agent nonetheless stays exactly
  as v1 builds it (prompt templates, `init_chat_model`, `@tool`, `create_agent` with a checkpointer,
  structured output, `SqliteSaver`) by choice, because Parity is the gate and the agent is proven.
  Any later move to a custom graph is a row in the decisions log below (ticket 02).
- Single user, no login, as in v1 (map).

**Repository (ticket 03)**

- One repository, a light monorepo with two independent projects and no shared tooling: a backend
  folder (the whole Python project run by uv) and a frontend folder (the Vite app run by npm), with
  docs, the glossary and the project rules at the root.
- Inside the backend, the core package is copied from v1 untouched, and the API is a separate
  package beside it, never inside it. Tests, evals and data keep v1's relative paths so the copied
  tests pass unchanged.
- Two terminals to run locally. Vite's dev proxy forwards the API path to FastAPI, so the frontend
  never holds the backend address and no cross-origin headers are needed.
- Git is initialised as the first build step. Repository name `login-investigator`, fresh history,
  first commit names v1 as the source. Nothing pushed before the author's review. Commits use the
  GitHub noreply address and the author's handle.

**Where logic lives (ticket 01)**

- The rule: logic that decides what the data means lives in the core. Logic that decides how it is
  shown lives in the frontend. The API only validates input, calls the core and shapes the reply.
  Where a screen and an agent tool compute the same fact, they call the same core function. The
  agent is never changed to match a screen.
- Moved into the core, as new functions: date resolution (end day plus one, a single date is one
  day, whole log by default); dataset facts (capture time, date bounds, countries, users, row
  count); alerts for a view (rules on the whole log, matched to the filtered rows, sorted newest
  first by last seen then rule), called by both the Overview tile and the Alerts list; the Report
  offer, returned with the Investigation.
- The screens and the agent do not share the alerts logic and never did: screens keep findings with
  at least one event among the filtered rows; the tool keeps findings overlapping a time window.
  Both are core already and both stay.
- Moved into the frontend: cutting names to three plus "and N more", singular or plural counts, the
  failed share percentage, time formats, the per-rule counts line, paging of past Investigations,
  the "Open in Log explorer" route, charts, colours per theme, empty states, locked input, progress
  words per tool, starter questions, the scope and AI notes, severity labels and colours on the
  report card.
- IP validation at both ends: the frontend checks before sending, the API refuses a bad IP with a
  422, and neither echoes the value.
- Agent tools (signatures, timestamp inputs, time-window matching) are unchanged from v1.
- Streamlit artefacts (label escaping, widget keys, reruns) go nowhere.

**The API (ticket 09, written in full in the API contract)**

- Every route sits under one base path. One endpoint per dashboard screen (overview, alerts,
  explorer), each taking the shared filters as query parameters: `from`, `to`, `outcome`,
  `country`, `user`, plus `ip` on the explorer and the CSV download. Plain dates in; the core
  resolves the window. Validation at the boundary, before the core is called.
- A dataset-facts endpoint and a rules-guide endpoint serve the facts the frontend must never
  hard-code: capture time, the "Synthetic data" label, date bounds, countries, users,
  rule titles, when each fires, and the general assumptions.
- Alerts carry the core's finding dictionary unchanged, evidence included (at most twenty rows), so
  the side panel makes no second request. The explorer returns every matching row, newest first, with
  no server paging; the CSV comes from the same core search.
- Investigations: list (full, newest first), start (create the record, return the ID as plain JSON),
  reopen (every Turn with its tool views and reports, plus the core's Report offer), ask (streamed),
  report (not streamed; the request text must equal the current offer or the reply is a conflict),
  and PDF by ID and report number. Starting is create-then-ask, two steps as in v1, so the ID arrives
  as a fact before any stream begins.
- The tool-calls panel text is produced by the core's describe function, run in the API, and shaped
  as title, asked, found, column order, rows as records (or null), and the raw result.
- One error shape for every status, replacing the framework default: an object with a code and a
  fixed message. Messages name a field, never a value. Exception text is logged on the server and
  never sent. A second ask while one streams is refused as busy. Questions are 1 to 2,000
  characters after trimming.
- A missing model key leaves every dashboard endpoint working and makes the Investigation endpoints
  answer "agent unavailable" naming the setting. A dataset that fails validation at startup makes
  every dataset endpoint return fixed text; the loader's message stays in the server log (ticket
  13).
- Configuration by environment variables: log path, memory path, reputation directory, the two API
  keys, and the server port, so the eval runner can isolate a run. At startup the log is loaded
  once, the rules run once on the whole log, the memory opened once and the agent built once, each
  in exactly one place. These are the seams carried from v1.
- Investigation keeping is as in v1: a random ID per Investigation, one small list table and the
  checkpointer memory in one SQLite file, one agent per server process, memory per ID.

**The stream (ticket 06)**

- Server-Sent Events over POST, produced with FastAPI's event-source response, read in the browser
  with fetch and a stream reader, aborted when the page unmounts. The built-in EventSource class is
  not used (GET only, no body, reconnects on its own).
- Four events, each with a JSON data field: `tool` (a tool is starting, by name), `text` (a piece
  of the answer), `error` (the answer stopped; the stream ends), `done` (complete and stored,
  carries nothing). After done or error the frontend fetches the Investigation again to redraw the
  Turn from memory, so a finished Turn has one source of truth.
- Failures before the first byte are normal JSON replies (404, 422, 503). The core's synchronous
  generator is handed to the route as it is; the server stops advancing it when the tab closes.

**The frontend (tickets 05 and 07)**

- Official shadcn/ui pieces composed by hand on Vite with React Router in plain declarative mode
  (four routes, no server rendering): the dashboard-01 shell and KPI cards, the tasks table example
  (TanStack Table) for the two tables, the message components for the chat. Recharts through the
  shadcn chart component. Rejected: shadcn-admin (a trimmed fork, 12,000 of 15,000 lines deleted)
  and Next.js (a server framework with no server work).
- Shared filters in a toolbar under the page title on the three dashboard screens. The sidebar is
  navigation only. The Investigator has no toolbar and is visibly unfiltered.
- Filter state lives in the URL as search parameters and travels on every request. "Open in Log
  explorer" is therefore a plain link built from the alert's first IP and its first and last dates.
- Alert evidence shows in a fixed details panel beside the table, below it on narrow screens, with
  the evidence table, "Open in Log explorer" and "Investigate". The newest alert is shown on first
  load and after a filter change; a row click swaps the panel's content with a short fade (ticket
  14). "How these rules work" is a collapsible fed by the rules endpoint.
- Overview: four KPI cards, sign-ins per hour as stacked bars, top source IPs as horizontal bars.
  The block's interactive area chart and its period toggle are removed, since the toolbar holds the
  date range.
- Log explorer: the toolbar plus the IP box, five count tiles, a paged table, a CSV link to the API.
- Investigator: a second column with "New investigation" and the paged list; chat with the message
  components; tool events drive the progress line; a "Tools used" collapsible under each answer with
  asked and found lines, rows in a table, raw JSON behind a switch; the report as a card with fixed
  fields and a PDF link; the report button only when the Report offer says so, with its wording;
  starters and the scope line only in an empty Investigation; input locked and a progress line while
  answering; the AI note by the input.
- Newly generated reports reveal their fixed-field text gradually after validation and saving,
  at a pace approximating the latest observed answer text delivery. Use a steady fallback when
  timing is unavailable. Previously saved reports open in full. A skip control and reduced-motion
  preference show the full report immediately. This is frontend presentation; report generation
  and its API remain non-streamed, and the initial generation wait remains.
- "Investigate" on an alert links to the Investigator with a prepared question built from the
  alert's rule title, first IP, first user and time window. The user presses send.
- The frontend never reaches past the API.
- **Visual hierarchy: one element leads each screen** (ticket 14). The element the analyst works in
  keeps full contrast: normal text size, full-strength text, a shaded table header, the card
  surface. Everything that supports it steps back one level: a quieter background with no shadow,
  smaller and softer text, plain headers, fainter lines. A selection in the leading element is tied
  to its supporting panel by an accent bar on the selected row. The change is in surface and
  contrast only, never in meaning: no colour stands for a severity or an outcome by this rule.
  First use: the Alerts table leads its details panel. Planned: in the Log explorer the rows table
  leads the count tiles (ticket 15); in the Investigator the chat leads the past-Investigations
  column and the "Tools used" panels (ticket 17); the Overview is checked by eye in ticket 19. The
  quiet styling becomes one shared piece at its second use, in ticket 15. Each screen's look in the
  browser confirms that one element leads.

**Security rendering (ticket 07)**

- Agent answers render through an allowlist markdown renderer: paragraphs, bold, italics, bullet
  and numbered lists, headings, inline code and code blocks. Links and images are not on the list,
  so a link shows as plain text with its address visible and is never followed, and an image is
  dropped. Raw HTML is never rendered. This is a change from v1's plain text, agreed by the author.
- The report card shows fixed fields as plain text. Log fields appear only as plain text, in table
  cells, chart labels and picker options, and never pass through any renderer that produces markup
  (ticket 13).
- Repository rules: no `dangerouslySetInnerHTML` anywhere in the frontend, and the renderer is used
  in exactly one component.
- Accepted residual risk: an answer can use headings or bold to look like part of the page. That is
  cosmetic and leaks nothing.
- Carried from v1: keys only in a git-ignored env file; log and API fields are data, never
  instructions, and the agent's system prompt says so; the memory file is git-ignored; only the
  fields the screen needs leave the server.

**Seams for future features (brief, ticket 03)**

The seams are prepared and the features are not built. All seams already exist in v1 and keep
fixed homes in the core: the tool list in one module, the single model-and-agent factory, data
access in the loader extended to answer "a dataset" from a configured source, and evals that call
the core or the API. The API process is the place where each is called once.

## Testing Decisions

**What makes a good test here.** A test grabs the system from outside at one of three doors and
checks what comes out. It never reaches inside to check how. The three doors are the HTTP API (the
main one), the core's functions (the existing door, kept for the copied tests), and the frontend's
functions and components (a small new door, needed because the browser is a different language and
holds the one security-sensitive renderer). No fourth door: no browser test tool and no screenshots,
by the author's ruling.

**The acceptance gate (ticket 08, the author's rulings of 14 October 2026).** The Port is accepted
only when every row is ticked with named evidence. Automated checks run first; the manual run comes
last, on a build where every automated check passes.

| Layer | Evidence | What it proves |
|---|---|---|
| Core | The 254 v1 core and agent tests, copied unchanged | The core did not change |
| Core, moved logic | New pytest tests, adapted from the screen tests, for every piece moved into the core: date resolution, dataset facts, alerts for a view, Report offer | The logic that left the screens still means the same |
| Core boundary | The boundary test extended: no Streamlit and no FastAPI import in the core | The core stays independent of both shells |
| API | pytest with FastAPI's test client, replaying the data-checking screen tests: filters change every screen consistently, an empty filter gives a clear message, S1 to S4 appear in alerts, alerts newest first, reset restores the whole log, a bad IP is refused without echoing it, memory opened once and agent built once per process | The contract behaves as v1's screens did |
| Agent | The eval set run in a new **API mode**: the runner starts its own FastAPI server on a free port, with a temporary memory file and the AbuseIPDB key removed, sends each question through the ask endpoint, reads the stream, asks for the report through the report endpoint, and scores with the unchanged grader. The direct mode stays for cheap iteration; **the API mode is the one that counts** | The agent gives the same answers through the real transport |
| Pass bar | Unchanged from v1: 90% overall, 100% for injection and refusal, 19 questions times 3 runs. Parity means meeting the target, not reproducing v1's 98% | A stable gate under model variance |
| Eval history | v1's results summary rows are copied into v2 as the first rows; v2 runs continue the table | A regression against v1 is visible at a glance |
| Frontend logic | Vitest with React Testing Library for the pieces placed in the frontend: three names then "N more", singular or plural counts, failed share, paging of past Investigations, the explorer jump route, the "Investigate" question, the bad IP message, and the allowlist renderer fed the S5 injection strings and crafted answers (markdown links, image tags, raw HTML, javascript: URLs), asserting no anchor, image, script, iframe or raw HTML in the output | The logic that left Python still means the same, and the renderer cannot leak |
| Presence | A manual checklist, ticked by the author with a dated ruling: synthetic label, metric labels, empty-state messages, scope note, AI note, progress words per tool, locked input while answering, severity labels and colours on the report card, charts per theme, error messages hide exception text | What v1's presence tests checked is still on screen |
| Core scenario | v1's eight-step scenario run end to end in the live v2 app by the author, closed with a dated ruling | Browser, API, agent, memory, report and PDF work together |
| Engineering | Fresh-clone start of both servers from the README; no key in git history; the core boundary test | A reviewer's first ten minutes succeed |

**The eight-step scenario (from v1's PRD).** Open the Overview and see the overnight spike; ask
"Anything suspicious last night?"; the agent runs the rules and reports a brute force from one IP
against one account; it searches for that IP and finds one success after the failures; it looks the
IP up and reports score, country and owner; a follow-up ("Did that user sign in from anywhere else
afterwards?") is answered from memory plus one search; the report is written with every fixed field;
the next day the Investigation is reopened from the list and continued.

**Prior art.** v1's tests in the sibling folder: the core and agent tests are the ones copied; the
two screen test files are the source for the API replays and the frontend tests, with the test
names kept where the case is the same; the eval runner, grader and gold answers are copied and the
runner gains the API mode. v1's acceptance section is the style for the ticked list.

## Out of Scope

- The five future features: RAG, knowledge graph, tracing, eval platforms, log upload. Their seams
  stay in scope; the features do not.
- Any change to v1. It is frozen, public course work.
- Any new behaviour v1 lacks, except the "Investigate" link on an alert.
- Deleting or renaming an Investigation, uploading a dataset, authentication, server-side paging.
- A custom LangGraph graph or any change to how the agent is built.
- Deploying or hosting v2.
- Browser test tools and screenshots.

## Further Notes

- Tier 3 work. No application code before this spec is agreed; no UI code before the screens are
  agreed (done, ticket 07). Every bug goes in the bug log and every build prompt in the prompt log.
- Spec changes go through the author: propose first, then edit and add a row below.
- The prototypes that informed the screen decisions are kept under `research/` in this folder.
- The two housekeeping items noticed during charting (a missing triage-labels file, skills named in
  the domain doc that are not installed) were fixed on 14 October 2026.

### Decisions log

| Date | Decision | Reason |
|---|---|---|
| 2026-10-14 | Spec written from the completed map; "PRD" renamed "spec" | The author's naming |
| 2026-10-14 | The course rule does not bind v2; the agent stays as v1 built it by choice | Parity is the gate; the agent is proven; the factory is one place to change later |
| 2026-10-14 | "Investigate" on an alert kept, frontend only | The author overruled the recommendation to drop it |
| 2026-10-14 | Agent answers render through an allowlist markdown renderer instead of plain text | "Nothing that fetches or navigates", not "no formatting"; guarded by a test |
| 2026-10-14 | No screenshots and no browser test tool in the gate | The author's ruling; manual items close on a dated ruling |
| 2026-10-14 | Missing model key: dashboards keep working, Investigation endpoints answer 503 | A failure stays inside the part it belongs to |
| 2026-10-14 | The copied core and agent tests number 254, not 259; corrected here, in tickets 08, 10 and 11 and in the map | 259 subtracted 31 screen test functions from 290 collected tests; collected, the screen files hold 36 (bug log B-001). The author's approval |
| 2026-10-14 | `to` without `from` runs from the start of the log to the end of that day; added to the contract | The contract left it open; an absent bound means "all", as for every other filter. The author's approval (ticket 11) |
| 2026-10-14 | Pyright type-checks the backend; copied v1 files that fail today sit on a "not yet checked" list that only shrinks (ticket 21) | Green from the first day, new code fully checked, the same checker as VS Code, and v1's code unchanged until Parity is proven. The author's choice over fixing all 61 errors now or using mypy |
| 2026-10-14 | The core's `views.py` renamed `dashboard.py` (ticket 20) | It sat beside `tool_views.py`, an unrelated module, and the names suggested a link. The author's approval |
| 2026-10-14 | The contract's Errors table gains `method_not_allowed` (405), `internal_error` (500) and `http_error` (any other framework status); `not_found` also covers an unknown path (ticket 12) | "One error shape for every status" needs a code for every status the server can send, and the contract stays the full list. The author's approval |
| 2026-10-14 | A missing log file answers `log_invalid` with fixed text, not the loader's message (ticket 12, bug log B-003) | The loader's missing-file message holds the server's full path, which can name the machine's user. Data crosses a trust boundary when it leaves the server. The author's approval |
| 2026-10-14 | An empty filter parameter means "all", as a missing one does, for every filter, dates included (ticket 12) | One rule for every box; an empty date was a 422 while an empty user meant "all", and the frontend may send empty boxes. The author's approval |
| 2026-10-14 | The official chart component passes its CSS as text, not raw HTML (ticket 13, bug log B-004) | The no-raw-HTML rule stays absolute, with no exception; the scan test fails if the component is reinstalled. The author's choice of three options |
| 2026-10-14 | Log fields may appear as plain text in table cells, chart labels and picker options; the rule and the project rules reworded (ticket 13) | The danger is a log field turned into markup, not its place on screen. The agreed screens put IPs on a chart and users and countries in pickers, all as plain text. The author's approval |
| 2026-10-14 | `log_invalid` sends fixed text for every cause, not the loader's message; done in ticket 13's branch, no new ticket (bug log B-008) | The loader's row messages quote raw log values, which broke the contract's rule that the API never formats a log field into a sentence. The change sits in the API only; the core is untouched. The author's ruling |
| 2026-10-14 | The agreed screens prototype (ticket 07) is the reference for the Overview's labels, chart titles and empty-state text, not v1's code; the failed share rounds a half up; the sidebar links keep the filters (ticket 13) | v1 could not be read in that session, and the prototype was agreed as v1's content. The author chose this over a check against v1's code; ticket 19's presence check uses this reference |
| 2026-10-14 | The Overview summary sends only `total`, `failures` and `distinct_users`; the dataset facts drop `row_count` (ticket 13) | Only the fields the screen needs leave the server. No screen showed the other six, and the Log explorer has its own endpoint for its counts. The author's approval |
| 2026-10-15 | "Severity labels and colours" are checked on the report card; the Alerts screen has none (ticket 14); spec, ticket 17 and ticket 19 name the card | v1's alerts carry no severity; only the incident report does. Naming the screen lets the presence check look in the right place. The author's ruling |
| 2026-10-15 | The Alerts table pages with the Log explorer's pager, one shared piece built in ticket 15; no columns menu | v1 had no pager and the log yields five alerts, but a pager keeps the screen usable if alerts grow, and reusing ticket 15's costs almost nothing. The reply's size at scale still needs server paging, which stays out of scope. The author's ruling (ticket 14) |
| 2026-10-15 | Alert evidence moves from a sliding panel (ticket 07, decision 2) to a fixed details panel beside the table, showing the newest alert by default; its content fades in on change, with no motion when the system asks for reduced motion | The author saw the live screen and wanted the prototype's drawing: the details always in view, never covering the list. v1's "Select an alert" hint goes, since an alert is always selected. The author's ruling (ticket 14) |
| 2026-10-15 | A visual-hierarchy rule for every screen: one element leads at full contrast, supporting elements step back one level; the quiet styling is shared from its second use (ticket 15) | On the Alerts screen the table and the details panel read as equally important; stepping the panel back fixed it, and the author asked for it as practice across the app. Writing it down means each screen inherits it instead of deciding again. The author's ruling (ticket 14) |
| 2026-10-16 | Explorer summary explicitly lists `total`, `successes`, `failures`, `distinct_users` and `distinct_ips`; Overview keeps three fields | The Explorer design needs five counts. The contract still pointed to Overview after ticket 13 narrowed its summary. The author approved the correction |
| 2026-10-16 | Newly generated reports use gradual text reveal after validation and saving, approximating observed answer-delivery pace; saved reports open immediately, with skip and reduced-motion support | The author chose gradual reveal over genuine API streaming, confirmed the pace requirement, then gave "Go". Generation, saved data and the API contract stay unchanged. Ticket 17, prompt P-024 |
| 2026-10-17 | The agent's tools take the dataset the API loaded at startup through one core setter, `use_dataset`, cleared at shutdown; without it they keep v1's default file. When the configured log fails validation the two log tools return a short fixed error and the IP lookup keeps working (ticket 22) | The only design that keeps the tools' names, descriptions and arguments, the copied tests and the core's independence from the API, and the tools read the very frame the dashboards read. LangChain's runtime context breaks the copied tests or the tool schema; a tool factory changes the descriptions the model reads (research note `research/22-tool-data-injection.md`). A failure stays inside the part it belongs to. The author's choice of design and of the failed-log behaviour |
