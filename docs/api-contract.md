# API contract — Login Investigator v2

Decided in [The API contract](../.scratch/v2-port/issues/09-api-contract.md) on 14 October 2026.
This is v2's central document: every endpoint has its input and output shape here before it is
built. The spec links to it; changes go through the spec's decisions log.

Shapes are written as JSON with a type note. `Timestamp` is the log's format `YYYY-MM-DDTHH:MM:SSZ`
(UTC). `Date` is `YYYY-MM-DD`. `Investigation` is the term from `GLOSSARY.md`; its ID is v1's
random thread id.

## Ground rules

| Rule | How the contract keeps it |
|---|---|
| The API is thin | Every route validates input, calls one or two core functions, shapes the reply. No analysis in routes |
| One endpoint per screen | Each dashboard screen has one endpoint that returns everything it shows. The API serves screens, not tables (author's decision, 14 Oct) |
| Only what the screen needs leaves the server | Each reply lists its fields here. Nothing else is sent. Log fields are raw values in lists meant for table cells |
| Log fields are data, never instructions | The API never formats a log field into a sentence. Messages are fixed text written in code |
| Plain dates in, raw numbers and lists out | The core resolves dates (end plus one day, whole log by default). The frontend formats, counts and cuts names |
| Errors never echo input | An error message names the field, never the value typed |
| The core is asked for "a dataset" | The API holds one `Dataset` (frame, findings on the whole log, facts) loaded from a configured path. No upload endpoint |

## Base path and configuration

All routes sit under `/api`. In development Vite proxies `/api` to FastAPI; in tests the FastAPI
test client calls the app directly.

Configuration comes from environment variables, so the eval runner can isolate a run:

| Variable | Default | Used for |
|---|---|---|
| `LI_LOG_PATH` | `backend/data/logins.csv` | The dataset the core loads at startup |
| `LI_MEMORY_PATH` | `backend/memory/investigations.sqlite` | The `SqliteSaver` memory and the investigations table, one file |
| `LI_REPUTATION_DIR` | `backend/data/ip_reputation` | Saved AbuseIPDB responses |
| `OPENROUTER_API_KEY` | none | The model. Missing: see "Agent unavailable" |
| `ABUSEIPDB_API_KEY` | none | Live reputation lookups. Missing: the tool reports an error, as in v1 |
| port | uvicorn's `--port` | The eval runner picks a free port |

Startup: load the log once, run the rules once on the whole log, open the memory once, build the
agent once. These are the seams from v1 (`loader.load_log`, `rules.detect_all`,
`investigations.open_memory`, `agent.make_model` and `agent.build_agent`), each called in exactly
one place.

## Shared filter parameters

The three dashboard endpoints and the CSV download take the same query parameters. All optional.
Missing or empty means "all", for every parameter (author's ruling, ticket 12). They mirror the URL search parameters of the frontend (ticket 07).

| Parameter | Type | Meaning | Invalid |
|---|---|---|---|
| `from` | Date | First day, inclusive | not a date, or after `to` |
| `to` | Date | Last day, inclusive. The core adds one day to make the window `[from, to + 1 day)` | not a date |
| `outcome` | `success` or `failure` | | any other value |
| `country` | two capital letters | Matched without regard to case, as the core does | |
| `user` | text | Matched without regard to case, as the core does | |
| `ip` | IP address | Explorer and CSV only | not an IP address (message never echoes it) |

Validation lives at the boundary: a bad value is a 422 before the core is called. A single date
(`from` without `to`, or equal values) means that one day, as v1's picker did. `to` without `from`
runs from the start of the log to the end of that day (ticket 11). Core: `dashboard.date_window`.

## Endpoints

### Dataset facts

`GET /api/dataset`

The facts the shell and the filter toolbar need. The frontend never hard-codes them.

```json
{
  "captured_at": "2026-10-08T09:00:00Z",   // Timestamp; the app treats this as "today"
  "label": "Synthetic data",                // fixed text for the badge
  "first_date": "2026-10-01",               // Date: earliest log day
  "last_date": "2026-10-08",                // Date: latest log day
  "countries": ["DE", "GB", "RU"],          // sorted, distinct
  "users": ["alice.k", "bob.m"],            // sorted, distinct usernames as they appear in the log
  "row_count": 1856                         // int
}
```

Core: a new `dataset_facts(df)` function (ticket 01). `captured_at` is `generator.CAPTURED_AT`.

### Overview

`GET /api/overview?<filters>`

```json
{
  "summary": {                               // from search.summarize(rows)
    "total": 1856, "successes": 1700, "failures": 156,
    "distinct_users": 41, "distinct_ips": 37, "distinct_countries": 6,
    "first_seen": "2026-10-01T09:02:57Z", "last_seen": "2026-10-08T08:59:40Z"
  },
  "alert_count": 5,                          // len(alerts_for_view)
  "hourly": [                                // stats.hourly_counts(rows); hours with no events are absent
    {"hour": "2026-10-01T09:00:00Z", "outcome": "success", "events": 12}
  ],
  "top_failed_ips": [                        // stats.top_failed_ips(rows), ten rows at most
    {"source_ip": "198.51.100.7", "failures": 40, "accounts": 12}
  ]
}
```

Not sent: the summary's `sample` and `truncated` (agent-only fields). Failed share is computed in
the frontend from `failures` and `total`.

Empty view (no rows match): `summary.total` is 0, `hourly` and `top_failed_ips` are `[]`,
`alert_count` is 0. The frontend shows the empty state. Not an error.

### Alerts

`GET /api/alerts?<filters>`

Findings with at least one event among the filtered rows, sorted newest first by `last_seen` then
`rule`, by the core (ticket 01: `alerts_for_view`).

```json
{
  "alerts": [
    {
      "rule": "brute_force",                 // rule key; the title comes from /api/rules
      "summary": "...",                      // written by the core from counts, not log text
      "ips": ["198.51.100.7"],               // full list; the frontend cuts to three
      "users": ["alice.k", "bob.m"],
      "event_count": 23, "failure_count": 22, "success_count": 1,
      "first_seen": "2026-10-07T23:10:00Z", "last_seen": "2026-10-08T00:05:00Z",
      "evidence": [                          // log rows, at most 20: the first and last when more
        {"timestamp_utc": "2026-10-07T23:10:00Z", "username": "alice.k", "source_ip": "198.51.100.7",
         "country": "RU", "outcome": "failure", "failure_reason": "bad_password", "user_agent": "..."}
      ],
      "evidence_shown": 20
    }
  ]
}
```

This is `Finding.to_dict()` unchanged, minus nothing: the side panel needs the evidence, so it
travels with the list and the panel makes no second request. The per-rule counts line, the "and N
more" cut and the "Showing 20 of 23 events" caption are frontend presentation from these numbers.

"Open in Log explorer" is a frontend link built from `ips[0]`, `first_seen` and `last_seen`
(dates only): `/explorer?ip=…&from=…&to=…`. No API involvement.

"Investigate" (author's ruling, 14 Oct: kept, frontend only, the one agreed exception to "no new
behaviour"): a frontend link to `/investigator?ask=<question>`. The Investigator puts the question
in the input box; the user presses send. Proposed wording, built from the alert's fields:
`Investigate the <rule title> alert: <first IP> against <first user> from <first_seen> to
<last_seen> UTC.` Covered by a frontend test. No API involvement.

### Rules guide

`GET /api/rules`

```json
{
  "rules": [
    {"rule": "brute_force", "title": "Brute force", "fires_when": "...", "assumption": "..."}
  ],
  "general_assumptions": ["...", "..."]
}
```

Straight from `rules.RULE_GUIDE` and `rules.GENERAL_ASSUMPTIONS`. Serves both the rule titles for
the alerts table and the "How these rules work" text. Fixed text, cacheable by the frontend for the
session.

### Log explorer

`GET /api/explorer?<filters>` (includes `ip`)

```json
{
  "summary": { "...": "as in /api/overview" },
  "rows": [                                  // every matching row, newest first; no cap, no paging
    {"timestamp_utc": "...", "username": "...", "source_ip": "...", "country": "...",
     "outcome": "...", "failure_reason": "", "user_agent": "..."}
  ]
}
```

The log has 1,856 rows, so the whole match is sent and paged in the frontend (ticket 07). Server
paging is a later change behind the same core search if a dataset ever grows.

### CSV download

`GET /api/explorer.csv?<filters>` (includes `ip`)

`text/csv`, `Content-Disposition: attachment; filename="login-investigator-rows.csv"`. The body is
`search.export_csv(rows)` on the same filtered rows, so file and table come from one core search.
Formula-looking values keep v1's leading apostrophe.

### Investigations: list

`GET /api/investigations`

```json
{
  "investigations": [                         // newest first, the full list; paging is frontend
    {"id": "9f1c…", "started_at": "2026-10-14T10:02:11Z", "first_question": "Anything suspicious last night?"}
  ]
}
```

`first_question` is the analyst's own text, already shortened to 200 characters by the core. It is
shown in the list as text content only.

### Investigations: start

`POST /api/investigations`

Request `{"question": "Anything suspicious last night?"}` (1 to 2,000 characters after trimming;
empty is a 422).

Response `201`:

```json
{"id": "9f1c…", "started_at": "2026-10-14T10:02:11Z", "first_question": "Anything suspicious last night?"}
```

Creates the record only (`investigations.start`). The client then calls **ask** with the same
question. Two steps, as v1 does (author's decision, 14 Oct). If the ask fails, the record exists
with no turns, as in v1.

### Investigations: reopen

`GET /api/investigations/{id}`

```json
{
  "id": "9f1c…",
  "started_at": "2026-10-14T10:02:11Z",
  "first_question": "…",
  "turns": [
    {
      "question": "Anything suspicious last night?",
      "answer": "…",                          // the agent's text as stored; the frontend renders
                                              // it through the allowlist markdown renderer
      "tools": [ { "…": "ToolView, see below" } ],
      "report": null                          // or an IncidentReport, see below
    }
  ],
  "report_offer": "Write the incident report" // or "Update the incident report", or null
}
```

`turns` is `agent.history()`; `report_offer` is `agent.report_request(turns)` (ticket 01: the
core decides, the API carries it). Unknown `id`: 404.

The answer is sent as stored. v1's `as_plain_text` stripping was a display fix for a plain-text
widget; v2 renders through the allowlist renderer (ticket 07), so the markers are rendered or
shown harmlessly.

**ToolView** (one per tool call, `tool_views.describe` run in the API, since the frontend never
reaches the core):

```json
{
  "title": "Detection rules",               // fixed text from the core's TITLES
  "asked": "…",                             // written by the core from the call's arguments
  "found": "…",                             // written by the core from the result
  "columns": ["Rule", "Summary", "IP addresses", "Users", "Events", "First seen (UTC)", "Last seen (UTC)"],
  "rows": [ {"Rule": "Brute force", "…": "…"} ],   // null when the core returns no table
  "raw": "{\n \"source\": …"               // the tool's result, pretty-printed JSON or the raw text
}
```

`columns` keeps the table's column order. `rows` is the pandas table as records; `null` when the
core gives none. Log values inside `asked`, `found` and `rows` are shown as text content or table
cells only.

**IncidentReport** is `agent.IncidentReport` as JSON, unchanged:

```json
{
  "title": "…", "severity": "high",          // none | low | medium | high | critical
  "summary": "…", "attacker_ips": ["…"], "affected_users": ["…"],
  "timeline": [{"time_utc": "…", "event": "…"}],
  "evidence": ["…"], "recommended_next_steps": ["…"],
  "number": 1                                // added by the API: the report's position in the
                                             // Investigation (1 for the first), for the PDF link
}
```

### Investigations: ask

`POST /api/investigations/{id}/ask`

Request `{"question": "…"}` (1 to 2,000 characters; empty is a 422). Unknown `id`: 404. Agent
unavailable: 503 (below). These are normal JSON replies, before any streaming starts.

Response: `text/event-stream` (SSE over POST, ticket 06), read with `fetch` and a stream reader,
aborted on unmount. Events, each with a JSON `data` field:

| event | data | Meaning |
|---|---|---|
| `tool` | `{"name": "search_logins"}` | A tool is starting. The frontend maps the name to its progress words |
| `text` | `{"text": "…"}` | A piece of the answer, appended in order |
| `error` | `{"code": "agent_failed", "message": "The agent stopped before it finished."}` | The answer stopped. The stream ends after it |
| `done` | `{}` | The answer is complete and stored |

After `done` or `error` the frontend fetches **reopen** to redraw the turn from memory with its
tool calls and the new `report_offer`, exactly as v1 reruns from memory. The `done` event carries
nothing, so there is one source of truth for a finished turn. A second ask on the same `id` while
one is streaming is refused with 409 `busy`; the frontend locks the input anyway.

Closing the tab mid-answer: the server stops advancing the core's generator; the memory holds
whatever the model had stored. Same as v1.

### Investigations: write or update the report

`POST /api/investigations/{id}/report`

Request `{"request": "Write the incident report"}` or `"Update the incident report"`, exactly the
text the **reopen** reply offered. Any other text: 422. A request that does not match the current
`report_offer` (nothing new since the last report, or no turns yet): 409 `not_offered`, as v1
ignores a stale click. Unknown `id`: 404. Agent unavailable: 503.

Response `200`: the `IncidentReport` above, including `number`. Not streamed; the report writer
is one structured-output call of several seconds. The frontend shows "Writing the incident
report…" meanwhile.

The eval runner's `REPORT` turn maps to this endpoint with `"Write the incident report"`.

### Investigations: report PDF

`GET /api/investigations/{id}/reports/{number}.pdf`

`application/pdf`, `Content-Disposition: attachment; filename="<report_pdf.file_name(id, number)>"`.
Built on request by `report_pdf.build` from the `number`-th report stored in the Investigation.
Unknown `id` or `number`: 404. Needs no model, so it works with the agent unavailable.

## Errors

One shape for every error reply, including validation, replacing FastAPI's default `detail`:

```json
{"error": {"code": "invalid_filter", "message": "from is not a date (YYYY-MM-DD)."}}
```

| Status | code | When |
|---|---|---|
| 404 | `not_found` | Unknown investigation id or report number, or an unknown path |
| 405 | `method_not_allowed` | A known path called with a method it does not take |
| 409 | `busy` | An ask is already streaming on this investigation |
| 409 | `not_offered` | A report request that does not match the current offer |
| 422 | `invalid_filter`, `invalid_question`, `invalid_request` | A parameter or body failed validation. The message names the field, never its value |
| 500 | `log_invalid` | The dataset failed to load at startup (`LogValidationError`); every dataset endpoint returns this with fixed text: `The log failed validation. The server log lists the problems.`, or `The configured log file was not found.` for a missing file. The loader's own message is logged on the server and never sent: it quotes bad rows' raw log values, and for a missing file the server's full path (ticket 13; bug log B-003, B-008) |
| 500 | `internal_error` | An unexpected failure. Message: `The server hit an unexpected error.` The exception is logged on the server |
| any other | `http_error` | Any other refusal by the framework itself. Message: `The request failed.` |
| 503 | `agent_unavailable` | `OPENROUTER_API_KEY` is not set. Message: `OPENROUTER_API_KEY is not set. Copy env.example to .env and add the key.` Dashboard endpoints keep working (author's decision, 14 Oct) |

Mid-stream failures use the `error` event with the same `{code, message}` object. Messages are
fixed text; the exception's own text is logged on the server and never sent, as in v1.

A tool failure inside the agent (a bad IP, a missing AbuseIPDB key, a network error) is not an API
error: the tool returns its `{"error": …}` result to the model as in v1, and it shows in the
ToolView's `found` line as `Error: …`.

## What the eval runner's API mode drives

1. Start the server with `LI_MEMORY_PATH` pointing at a temporary file, `ABUSEIPDB_API_KEY` unset,
   on a free port.
2. `POST /api/investigations` with the first turn.
3. `POST /api/investigations/{id}/ask` for each question turn, reading the stream to the end.
4. `POST /api/investigations/{id}/report` for a `REPORT` turn.
5. `GET /api/investigations/{id}` and score the last turn with the unchanged grader.

## Not in this contract

- Delete or rename an Investigation (v1 has neither).
- Upload a dataset (the seam is the configured path and the one `Dataset` object).
- Authentication (single user, as v1).
- Server-side paging (the whole match fits).
