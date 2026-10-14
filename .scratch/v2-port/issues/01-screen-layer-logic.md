# Screen-layer logic: what moves to the core, the API or the frontend

Type: grilling
Status: resolved
Blocked by: none
Map: [map.md](../map.md)

## Question

v1 keeps some logic in the Streamlit layer (`app/`), not in the core. In v2 that layer disappears.
For each piece, decide where it lives: the Python core, the API layer, or the React frontend.

The known pieces (see [v1-facts.md](../v1-facts.md), "Logic in the screen layer"):

- Date range to timestamps: the end date plus one day.
- Rules run on the whole log, then filtered to the visible rows (`findings_matching`).
- Alerts sorted newest first.
- Names cut to three, plus "and N more".
- Failed share on the Overview.
- Paging of past investigations.
- The "Open in Log explorer" jump from an alert.

Before grilling, read `app/shared.py` and the four files in `app/screens/` line by line to complete
this list. Charting only scanned them.

Decision rule to test in the grilling: logic that decides what the data means belongs in the core,
so screens, API and agent tools cannot disagree; logic that decides how it is shown may live in the
frontend. Where a piece sits decides which tests cover it, so the answer feeds
[What proves Parity](08-parity.md).

## Comments

## Answer

Grilled with the author on 14 October 2026. Ten questions, all answered with the recommended option.

**The rule.** Logic that decides what the data means lives in the core. Logic that decides how it is
shown lives in the frontend. The API only shapes responses. Addition: wherever a screen and an agent
tool already compute the same fact, they call the same core function, so they can never disagree.
The addition never works the other way: the agent is not changed to match a screen.

**Correction to the ticket's premise.** The screens and the agent do not share the alerts logic
today. The screens keep findings with at least one event among the filtered rows
(`findings_matching`), so outcome, country and user all count. The tool keeps findings overlapping a
time window only (`in_window`). Both are already core. Both stay as they are.

### Where each piece lives

| Piece | Home | Test home |
|---|---|---|
| Date range to timestamps (end plus one day, single date is one day, default whole log) | Core: the API takes plain dates, the core resolves them | pytest, adapted from `test_reset_restores_the_whole_log` and the filter tests |
| Dataset facts for the pickers: date range, countries, users, capture time | Core, exposed by the API | pytest |
| Alerts for a view: rules on the whole log, matched to the filtered rows, sorted newest first by last seen then rule | Core, one function called by the Overview tile and the Alerts list | pytest, adapted from `test_alerts_are_listed_newest_first`, `test_overview_counts_match_the_core`, `test_a_filter_change_updates_every_screen_consistently` |
| Agent tools: signatures, timestamp inputs, time-window matching | Core, unchanged from v1 | The copied tool tests and the eval set |
| Report offer (when to offer, the wording) | Core (`report_request`), returned by the API with the investigation. No stale-click guard | pytest, adapted from `test_the_report_button_waits_for_something_new` |
| IP validation on the explorer | Both: the API refuses a bad IP, the frontend shows the message and never echoes the value | pytest on the API, frontend test for the message |
| Three names and "N more", singular or plural counts, failed share as a percentage, time formats, per-rule counts line | Frontend; the API sends raw lists and numbers | Frontend unit tests |
| Past investigations paging: three, three more per click, the open one always visible; the API returns the full list | Frontend | Frontend unit tests, adapted from the three paging tests |
| "Open in Log explorer": a frontend route with IP, first and last date in the URL, from fields the alert already carries | Frontend, no API involvement | Frontend test, adapted from `test_open_in_log_explorer_points_at_the_alert` |
| Charts, colours per theme, table sizes, empty states, error messages that hide exception text, locked input while answering, starter questions, scope note, AI note, progress words per tool, severity labels and colours | Frontend | Presence tests handed to ticket 08 to keep, replace or retire |
| Memory opened once per process, agent built once | API process (an existing seam) | pytest on the API |
| Markdown escaping of labels, widget keys, reruns | Nowhere: Streamlit artefacts | None |

### Hand-offs

- [What proves Parity](08-parity.md): the test-home column above; decide the frontend test mechanism
  and the fate of the presence tests.
- [The API contract](09-api-contract.md): plain dates in, a dataset-facts response, raw lists and
  numbers out, the report offer carried with the investigation, IP validation at the boundary.
- [Repo layout](03-repo-layout.md): where the new core view functions (date resolution, alerts for a
  view) sit in the package.
