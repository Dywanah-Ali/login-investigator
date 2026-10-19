# Parity closing evidence

Ticket: [19](../.scratch/v2-port/issues/19-parity-closing.md). Review date: 2026-10-18.
Status: ticket 19 resolved by author acceptance on 19 October 2026, P-110. Remaining same-case next-day check waived for the course demo. Nothing pushed.

## Automated evidence

| Gate | Evidence | Result |
| --- | --- | --- |
| Cross-screen filters | `backend/tests/test_api_dashboard.py`: `test_a_filter_change_updates_every_screen_consistently`, two filter combinations through Overview, Alerts and Explorer | Passed |
| Cross-screen empty view | `test_an_empty_filter_returns_clear_empty_data_on_all_three_screens`; existing empty-message component tests in all three page test files | Passed |
| Cross-screen reset | `test_reset_restores_the_whole_log_on_all_three_screens`, after both narrowed and empty views | Passed |
| Copied tests | Twelve v1 test files byte-identical, plus v1's original boundary test retained in the extended file; `tests/conftest.py` unchanged; 254 original cases independently collected | Verified against frozen v1, read-only |
| Backend | `cd backend && uv run pytest -q && uv run pyright` | 374 passed in 142.85 seconds; Pyright zero errors, warnings or information messages |
| Frontend | `npm test`, `npm run typecheck`, `npm run build`, `npm run lint` | 134 tests pass, type check and build pass; lint has six existing warnings |
| Agent and pass bar | Accepted ticket 18 result: `backend/evals/results/2026-10-17-185622-35d4d98f.json` | 56/57 overall, 15/15 security, zero live reputation lookups |
| Saved benchmark verification | Recomputed every successful record's checks with the unchanged grader, compared the full summary, checked 19 questions each have three runs and prompt fingerprint `35d4d98f` | Identical; failed stream retained; no model calls or evidence files changed |
| Eval inputs and history | `questions.json`, `ground_truth.json`, `scoring.py` byte-identical to v1; `backend/evals/results/summary.md` retains v1's rows before v2's | Verified |
| Clean-clone startup | Independent local clone of `9d28987`, new virtual environment and `node_modules`, `uv sync`, example environment, `npm ci`, README server commands | Both servers start; direct and proxied dataset/Overview/Alerts/Explorer replies match; 1,856 rows; four frontend routes serve the app; missing-key Investigation is 503 |
| Repository scan | All 1,084 Git objects, including unreachable objects, plus tracked working files | Passed with the author-approved fake test-key exception, 18 October 2026; see classification below |

Ticket 19 adds API replay tests, acceptance documentation and the author-approved Overview
Alerts-card styling and Alerts caption cleanup. The backend application, agent and benchmark inputs remain unchanged, so
the accepted ticket 18 model run remains the agent evidence.

### Repository scan classification

No value from either locally configured API key was found in any Git object. No private-key
header was found. Supplementary scans also check AbuseIPDB-shaped 80-character hex keys,
GitHub tokens and AWS access-key patterns. The provider-key pattern matched one deliberately fake constant in
`backend/tests/test_api_errors.py`. This is the fixture that proves exception text cannot leak.
The literal pattern exists, so an unqualified claim of zero pattern matches would be false.
Author's ruling, 18 October 2026: accepted. The author approved keeping the fake test key
and recording the explicit exception. No real key value is permitted. See prompt P-035.

No author name was found in tracked working files or stored blob/commit objects. Personal-path
matches in historical test blobs use the placeholder `someone`. Email-shaped bytes in the bundled
DejaVu font are binary false positives. All historical commit email matches are GitHub noreply addresses or the assistant bot's noreply address; no personal email was found.
The scan prints object IDs and counts instead of key values or personal information.

### Clean-start details

Port 8000 was already occupied by another service. Used the README's documented alternate-port
configuration: API on 63621 and `LI_API_URL=http://127.0.0.1:63621` for the frontend. The frontend
started on its default port, accessed at the README's `http://localhost:5173`. The initial probe
incorrectly used the IPv4 address for Vite's localhost listener; corrected and passed (B-042).
The corrected complete verifier also exited successfully after the original address probe timed out.
The HTTP route check covers `/`, `/alerts`, `/explorer` and `/investigator`; it does not prove
visual appearance. No configured key was copied into the clone. Temporary servers are stopped
after verification. The clone verifies startup before the approved Overview styling change; that change does not
alter setup, dependencies or server startup.

### Existing concerns

- B-041 remains unresolved: one failed or incomplete stream in the accepted benchmark. It is
  counted as failed. The run still meets the agreed target.
- B-017 remains unresolved: clean `npm ci` reports seven high-severity dependency advisories.
- Six existing lint warnings remain: two table/library compatibility warnings, three shared
  component export warnings and one mobile-hook state/effect warning.
- The production build retains its bundle-size warning: the main JavaScript chunk is about
  1,081 kB before gzip and 330 kB after gzip.

No unrelated dependency or application change is included in this ticket.

## Author's live review

Current review app: `http://localhost:5174`, with the configured API on port 8010.
These two development servers are left running for the author; temporary clone servers are stopped.

Run this only after the automated gate passes. Use the normal configured application from the
README. The clean clone intentionally has no model key and cannot complete the agent scenario.
Record each ruling here with its date. No browser automation or screenshots are required or used.
An unchecked item is pending, never an inferred pass from a code inspection.

### Visual hierarchy

| Screen | Agreed leading element | Author's dated ruling |
| --- | --- | --- |
| Overview | Alerts metric draws attention through its count and small status icon; card background stays quiet | Approved 18 October 2026: overall page accepted, then updated card approved (P-037) |
| Alerts | Alerts table; details panel supports the selection | Approved 18 October 2026: author said "ok good lets move on to the explorer page" (P-045) |
| Log explorer | Rows table; count tiles support it | Approved 18 October 2026 after caption cleanup (P-047) |
| Investigator | Chat; past Investigations and tool evidence support it | Approved 19 October 2026, P-108: consolidated case and PDF reviewed; required searches, ordered report and chat-leading layout accepted. Earlier scoped rulings retained below |

### Presence checklist

For the Overview's metric labels, chart titles and empty message, compare with
`.scratch/v2-port/research/07-screens-prototype.html`, as already agreed. The failed share rounds
halves up and navigation preserves filters. Check the other presence items against frozen v1.

- [x] Synthetic-data label is visible at desktop and narrow widths; capture timestamp
  8 October 2026, 09:00 UTC is visible on desktop and intentionally hidden on narrow screens.
  Author approved this responsive behaviour on 19 October 2026, P-081.
- [x] Metric labels, chart titles and displayed figures match their agreed reference. Author
  approved after Reset on 19 October 2026, P-080: 1,856 attempts, 308 failed (16.6%), 57 usernames,
  five alerts; titles Sign-in attempts per hour and Top source IPs by failed sign-ins. Prototype
  figures are illustrative; these figures describe the current dataset.
- [x] Empty-state messages are clear on Overview, Alerts and Log explorer. Tested User
  `daniel.hughes` with Country `RU`, using available picker options. Filters carry between pages
  and Reset restores data. Author approved 18 October 2026, P-065.
- [x] An empty Investigation shows the scope note and all three starter questions.
  Author approved 19 October 2026, P-076.
- [x] The input shows the AI note. Author approved its visibility and readability
  19 October 2026, P-077.
- [x] Tool progress reflects actual execution in one changing line: checking detection rules,
  searching the sign-in log and looking up IP reputation, combined when types overlap. Author
  approved this direction in P-086. Fast cached calls can finish before a browser frame; the live
  review checks truthful current activity, not a mandatory visible dwell for every tool. Automated
  burst and lifecycle checks cover the event handling. Author approved the current behaviour
  after the multi-IP test on 19 October 2026, P-092, accepting brief cached-call visibility.
- [x] Input and Send are locked while the answer is being generated and usable afterwards.
  Author checked both transitions and approved 18 October 2026, P-068.
- [x] The report card shows its severity label and colour. Author approved the saved report's
  readable Critical severity label and red colour cue on 19 October 2026, P-078. Existing
  component tests cover all five values; this live ruling covers the displayed Critical report.
- [x] Both Overview charts and their bars, titles, axis labels and legends are legible in
  Light and Dark. Author approved 19 October 2026, P-079.
- [x] User-facing error messages hide exception text. Four targeted component tests cover fixed
  messages for server, filter, log and unreachable failures. Author approved the live connection
  message on 18 October 2026 (P-067) during a controlled backend stop/restart. No raw error shown.
  Backend restored; proxied Overview returns 200 and the ten saved Investigation IDs are unchanged.

Presence ruling and date: complete, 19 October 2026. Each item has its scoped author ruling
above, dated 18 or 19 October. P-092 closes the final progress item; it does not close the scenario.

### Eight-step live scenario

Use a new Investigation. The agent already anchors relative times to the dataset capture date,
8 October 2026. Use the scenario wording as written.

1. [x] Open the Overview and see the overnight spike. Reset-view hourly chart approved
   19 October 2026, P-093.
2. [x] Ask “Anything suspicious last night?” in the consolidated case
   `ba63f90e8f6f465a9633817b8c898abb`. Verified P-107 and accepted P-108, 19 October 2026.
3. [x] Confirm brute force from 185.218.86.24 against daniel.hughes. Earlier manual ruling
   P-095; verified in the consolidated case and accepted P-108.
4. [x] Confirm an actual IP search and one success after the failures. Consolidated case
   performs search_logins for 185.218.86.24 with the 02:32:20 UTC success; P-108 approval.
5. [x] Confirm reputation score, country and owner. Earlier saved-field check P-097;
   consolidated case includes the attacker reputation lookup, accepted P-108.
6. [x] Exact unnamed follow-up identifies Daniel and both later GB sign-ins, with a fresh user
   search in the same consolidated case. P-107 saved evidence and P-108 approval.
7. [x] Report has every fixed field and chronological order; reopened report matches returned
   report; PDF opens with matching title/sections. Consolidated case/PDF accepted P-108.
8. [x] Waived by the author on 19 October 2026, P-110: next-day reopening and continuation of
   this same consolidated case. This additional check was not performed.
   Prior next-day acceptance P-071 for case `872227a3ca7948748f7b4f1ec57ee6c3` is retained as
   separate persistence evidence, not a substitute for this one-case sequence.

Scenario ruling and date: steps 1–7 accepted 19 October 2026, P-108. The author accepted
the complete demo scope on the same date, P-110, waiving the additional next-day check.
The author explicitly accepted review of the prepared consolidated case and its PDF; execution
was performed through the live API under P-107. Earlier mismatched rulings remain in the history.

### Final acceptance

- [x] Author's final approval on 19 October 2026, P-110, including the explicit demo-scope waiver.
Nothing has been pushed. Pushing is outside this ticket's verification work.


## Overview review adjustment, 18 October 2026

The author said the page was good overall and requested a stronger Alerts-card cue. Agreed:
green count and subtle check icon at zero; amber count and bell icon above zero; quiet background.
Existing findings-in-this-view wording stays. Decision recorded in the spec, prompt P-036,
and bug B-043. Author approved the updated card on 18 October 2026: "its good. approved"
(P-037). Overview review accepted; other screens and the live scenario remain open.

Live review examples verified against the API: whole log has five alerts;
`http://localhost:5174/?country=GB` has 1,434 sign-ins and zero alerts.


## Alerts review feedback, 18 October 2026

Author requested removing per-rule counts above the table and the rows/page-size caption below.
Only the total remains above it; paging navigation stays. Decision in the spec, P-038 and B-044.
The rule filter and default-severity follow-up are approved for after Parity in ticket 26.
Author accepted the current Alerts page on 18 October 2026, prompt P-045.


## Explorer review feedback, 18 October 2026

Author requested a row-count-only footer and removal of the sampling sentence. Recorded in the
spec and prompt P-046. Paging, newest-first ordering and CSV behaviour stay the same. The author
also asked for an opinion on severity; no severity or event colouring is added by this cleanup.
Author approved the updated Explorer on 18 October 2026 (P-047) and moved to Investigator review.


## Investigator first-use review, 18 October 2026

Author's ruling (P-048): "the investigator page before starting any investigations and without
prior history of investigations is functionly looking stable and reliable". Accepted as feedback
on the initial empty layout only. It does not establish that answering, streaming, tool evidence,
follow-ups, reports, PDF or reopening work in the live app. Those checks remain pending.
No screenshot artifact is used to close the gate; the author's dated wording is the ruling.

## Investigator progress adjustment, 18 October 2026

Author found the external tool-progress line easy to miss and requested an in-chat placement
(P-049). Status now follows the active question/answer inside the chat viewport, including
in-chat report-generation progress. Existing words and input locking remain. B-049 records the
issue and fix. Author accepted the improved placement on 18 October 2026 (P-050). Live scenario remains open.


## Investigator keyboard adjustment, 18 October 2026

Author requested Enter to send and Shift + Enter for a newline (P-050). Enter now submits the
existing form, preserving send guards and input-method composition. B-050 records the cause
and fix. Author accepted Enter/Shift + Enter behaviour on 18 October 2026 (P-051). Live evidence and scenario checks remain open.

## Tool evidence and expansion review, 18 October 2026

Author accepted tool outputs within the capabilities defined in the code, leaving richer
investigation features for future work (P-052). They requested smoother panel expansion and
authorised implementation after confirmation. The panel now uses observed answer pace, as the
report reveal does, to guide bounded height/fade motion. Reduced-motion users get immediate
access. The report's text reveal and all evidence fields remain intact. B-052 records the issue.
Live animation confirmation, report/PDF and persistence checks remain pending.

## Tool-expansion visibility follow-up, 18 October 2026

Author could not judge the opening animation because the expanded content was below view and
required the jump arrow (P-053). Added scoped following of the chosen panel's bottom during
opening, cancelling on manual interaction, close or unmount. Later messages are not the target;
reduced motion reveals once. B-054/B-055 record the bug and the test-strengthening iteration.
The author's visual ruling on the visible reveal still remains open.


## Tool-expansion visibility accepted, 18 October 2026

Author's ruling, verbatim: "all good now. thankx code. what is next ?" (P-054). Accepted the
updated Tools used animation and its scoped scroll-follow behaviour. The author's earlier
tool-evidence acceptance remains limited to implemented capabilities. Next manual check is
follow-up memory in the same Investigation. Report, PDF and reopening remain pending.


## Follow-up conversation reviewed, 18 October 2026

Author considers memory stable and reliable and supplied a three-question conversation (P-055).
Accepted as the author's live conversation-continuity ruling. The named-account follow-up returned
both expected subsequent successful GB sign-ins: 198.51.100.20 at 07:23:26 UTC and 203.0.113.10
at 08:45:37 UTC on 8 October. This matches ground truth S3. The username was repeated, so this
sample alone does not isolate unnamed-reference recall or persistence after reopening.
The opening answer also conflates suspicious activity with the question of compromise; B-056
records that answer-quality concern without changing the prompt or application during this review.
Next: generate and review the incident report in this same Investigation. Report/PDF and reopening
remain pending. Ticket 19 remains open.

## Current report accepted; future scope enhancement, 18 October 2026

Author says the report is good (P-056). Record acceptance of the current live report reviewed by
the author. A future enhancement should let report content follow the user's intent when a long
conversation explores different directions. Deferred as AUD-003 in the maintained
[improvement audit register](audit/improvement-register.md). No report implementation changed.
PDF download/opening and saved-Investigation reopening remain pending. Ticket 19 remains open.


## PDF accepted, 18 October 2026

After being asked to download and open the PDF, compare its content with the report and check
for clipped text, the author replied “ok it is good” (P-057). Record the PDF download, opening
and presentation as accepted in this manual review. Saved-Investigation reopening and continuation
remain pending. This ruling does not close the whole presence checklist or ticket 19.

## Suspected history mixing investigated, 18 October 2026

At the author's request (P-060), traced selection from URL ID to API case ID and checkpoint thread
configuration. Compared the three live histories with the repeated recap question: each contains
Daniel's details locally before its recap. An offline real-route/agent/checkpointer probe across
three temporary cases captured seven question-model inputs and two report inputs, including
interleaving and restart, without cross-case marker leakage. Three existing backend checks and
two frontend navigation checks pass. See the [diagnosis](audit/conversation-isolation-2026-10-18.md).
This establishes separation in the tested flow, not a blanket semantic memory guarantee. Recap
scope remains AUD-020/B-060. No paid call, live-history write or application change. Earlier pending
next-day/manual scenario and newly identified defects are not closed by these checks.

## Theme selector added for review, 18 October 2026

Author corrected the review instruction: there was no in-app switch (P-061, B-061). They authorised
standard theme selection. The shared header now offers Light, Dark and System, with System as the
default and a saved local preference. Existing colour tokens remain; explicit choices override
OS changes and System follows them. The selector supports keyboard access, storage fallback and
cross-tab updates. A startup script sets the initial appearance before first paint. The capture
timestamp hides on narrow screens to preserve header space; the synthetic-data badge remains.
Spec decision recorded before implementation; AUD-024 tracks author review. B-062 preserves the
initial test-command/context correction. Both-theme readability remains a manual pending ruling.

Theme validation: 13 new interaction/startup cases pass; all 134 frontend tests pass. Type check,
lint and production build pass. Lint has only the same six existing warnings; build retains its
bundle-size warning (about 1,084 kB main JavaScript, 330 kB gzip). Final focused tests cover the
small header title/responsive refinements. The running dev server serves the new startup script
and header module. Author's live theme review still pending; no inferred visual pass.

## Initial theme feedback, 18 October 2026

Author replied “so far so good” after the theme-control handoff (P-062). Record positive initial
feedback on the selector. Full four-screen readability in both themes is not yet explicitly ruled
on. Other pending manual/scenario checks remain open. No application change.

## Theme review feedback and Alerts header adjustment, 18 October 2026

Author requested a darker Alerts header to distinguish it from the selected row and said
“other than that all good” (P-063). Record acceptance of the other reviewed theme appearance,
with this one adjustment outstanding. The header now darkens its existing muted token in each
theme and keeps that tone on hover. The selected row and its accent are unchanged. B-063 and
AUD-025 retain the issue. Final confirmation of the adjusted header remains pending; this feedback
does not close unrelated checklist items or the next-day scenario.

## Alerts header tone accepted, 18 October 2026

Author replied “good” to the adjusted header (P-064). Record approval of the final Alerts header
tone and close AUD-025/B-063. Together with P-063, the requested theme-appearance adjustment is
accepted. This does not close unrelated manual presence checks or the next-day scenario.


## Empty views and reset accepted, 18 October 2026

After checking Overview, the author was asked to visit Alerts and Log explorer, verify filter
carry-over and empty messages, then Reset to restore normal data. They replied “all good” (P-065).
Record this dated acceptance and close the corresponding presence-checklist item. The actual
filter combination was User daniel.hughes and Country RU; direct API reads also returned zero
matches on all three endpoints. The dated verbal ruling is the evidence, not a saved screenshot.
Other unchecked items and final Parity acceptance remain open.


## Connection-error message accepted, 18 October 2026

P-066 authorised the next safe-error check. Verified the local API listener belonged to this
project, captured the ten saved Investigation IDs and stopped only that listener. Frontend stayed
running and its API proxy returned 502. Asked the author to reload Overview and inspect the fixed
connection message without technical details. Restarted the API after the short review window;
author answered “yes” (P-067). Record the live error presentation as accepted.

Recovery: proxied Overview returned 200 with 1,856 rows. All ten saved Investigation IDs matched
the pre-stop list. Four targeted Overview error-message tests passed; ten unrelated tests were
skipped. No model call, live-history write or application edit was needed. Other pending presence
items and the next-day scenario remain open.


## Input locking accepted, 18 October 2026

The author was asked to send “Summarise the evidence so far” in an existing Investigation,
confirm that typing and sending were unavailable during the answer, then confirm both worked
when it finished. They replied “all good” (P-068). Record the dated acceptance for input locking
and unlocking only. Other unchecked presence/scenario items and final Parity approval remain open.

## Next-day reopening reviewed, 19 October 2026

The author supplied two inline views of yesterday's selected Investigation, titled
“Which IP addresses attacked us, and how bad are they?”. The earlier report is visible,
followed by today's question “What were the two later GB sign-ins for Daniel?” and a completed
answer. Both returned events match S3: 198.51.100.20 at 07:23:26 UTC and 203.0.113.10 at
08:45:37 UTC on 8 October 2026. One tool call is indicated; its contents are not expanded.
The API and frontend were restarted before this review. No screenshot artifact is saved or
used to close the gate. Explicit author acceptance of next-day reopening and continuation is
requested and remains pending. The named-account question does not isolate unnamed-reference
recall. The already recorded timeline-order defect B-059 remains visible in the old report;
this review does not resolve it. Ticket 19 and the other manual checks remain open.


## Next-day reopening accepted, 19 October 2026

The author explicitly replied “approved” (P-071) to the reopening and continuation check.
Closed scenario step 8 for Investigation `872227a3ca7948748f7b4f1ec57ee6c3`, started
18 October 2026 at 09:29 UTC. A read-only lookup matched the unique displayed first question
and start time to this ID. Yesterday's messages/report were retained and today's named-account
continuation returned both expected GB sign-ins after the server restart. This scoped approval
does not close unnamed-reference recall, other presence/scenario checks or existing audit concerns.


## History navigation correction ready for review, 19 October 2026

P-074 confirms v1-style arrow expansion/collapse. Restored the list as recorded in B-064/AUD-026:
three at a time, continuous prefix around older selections, collapse preserving selection,
accessible arrow controls and reduced-motion-aware reveal. All 136 frontend tests and build/type
check pass. Six existing lint warnings and bundle-size warning remain. Live visual acceptance
of this correction is pending. Existing next-day recovery acceptance is unchanged.


## History navigation accepted, 19 October 2026

Author replied “yes all good” after testing both restored arrows (P-075). Closed B-064/AUD-026
with this live ruling and the 136 passing frontend tests plus build/type check from P-074.
This closes the history-navigation correction only; other unchecked presence/scenario items
and final acceptance remain open. No further application change or repeated tests.


## Empty Investigation scope and starters accepted, 19 October 2026

Author replied “approved” after the explicit check of New investigation's read-only scope
explanation and all three starter questions (P-076). Closed only that presence item.
No application change, model call or repeated tests. Other unchecked gates remain open.


## AI note accepted, 19 October 2026

Author replied “approved” to the explicit visibility/readability check of the AI note below
the question box (P-077). Closed only that presence item. No application change, model call
or repeated tests. Other unchecked gates remain open.


## Report severity display accepted, 19 October 2026

Author replied “approved” to the saved report's readable Critical severity label and clear red
colour cue (P-078). Closed that presence item. This approves presentation, not the report's
severity reasoning or the separately recorded answer-quality concerns. No application change,
model call or repeated tests. Other unchecked gates remain open.


## Chart readability accepted, 19 October 2026

Author replied “approved” to the explicit check of both Overview charts in Light and Dark,
including bars, titles, axis labels and legends (P-079). Closed that presence item. No application
change, model call or repeated tests. Other unchecked gates remain open.


## Overview labels and figures accepted, 19 October 2026

Author replied “approved” after the explicit Reset check of all four metric labels and values,
failed share and both chart titles (P-080). Closed that presence item. No application change,
model call or repeated tests. Other unchecked gates remain open.


## Synthetic-data header accepted, 19 October 2026

Author replied “approved” to the explicit responsive-header check (P-081): synthetic-data label
on both screen sizes, capture timestamp 8 October 2026, 09:00 UTC on desktop, hidden on narrow
screens as agreed. Closed that presence item. No application change, model call or repeated tests.
Per-tool progress wording, remaining scenario rulings and final acceptance remain open.


## Execution-based tool progress ready for review, 19 October 2026

Author approved the researched single-line approach (P-086). Spec decision and API contract were
recorded before implementation. LangChain's per-invocation inline callbacks now publish typed
custom start/end/error signals through the existing synchronous stream, alongside model text.
Progress reflects execution rather than model requests. Only allowlisted name, opaque call ID
and phase cross the progress boundary. Inputs, outputs and raw errors are excluded.

The frontend maintains active calls by ID, including parallel invocations of the same tool.
It combines active tool types in one sentence, removes only a finished/failed call and returns
to Thinking or Writing the answer when none remain. Completion, stream failure and navigation
clear transient activity. Legacy core callers keep start-only Stream output, preserving the
unchanged copied tests. Prompt, tools, model, saved memory and grader are unchanged.

Validation:

- Full backend suite collected before the last HTTP privacy case: 379 passed in 261.01 seconds.
- Added HTTP tool-error privacy test: one passed separately. Thus all 380 current backend cases
  were exercised; do not describe the initial full run as collecting 380.
- Five real-framework lifecycle cases cover parallel calls, duplicate tool names, retained
  follow-up history, an unexecuted model request and handled/propagated errors.
- All 141 frontend tests pass with one worker. Tests cover same-chunk tool bursts, duplicate names,
  terminal phases, fast completion, error cleanup, malformed events and active-tool navigation.
- Build and TypeScript check pass. Lint retains six existing warnings; production bundle warning
  remains, about 1,085 kB before gzip and 331 kB after gzip.
- One Explorer test initially timed out during concurrent checks. Its one-worker rerun passed,
  as did the full one-worker suite, without Explorer code or timeout changes. B-066/AUD-028
  retain the original failure and unresolved cause.
- Restarted the verified project API on port 8010. Proxied saved-Investigations endpoint returns
  HTTP 200; all 12 saved Investigation IDs match the pre-restart snapshot. No paid model call
  or live-history mutation by Codex. Frontend remains on localhost:5174.

B-065/AUD-027 and the final tool-progress presence item await the author's live ruling. Fast
cached calls may still finish before a browser paint; no forced dwell or artificial delay was
added. The accepted model benchmark remains historical evidence, not a rerun of this adapter.
Nothing pushed.

Final backend Pyright check after all test additions: zero errors, warnings or information
messages. Documentation diff check passes. Live tool-progress approval remains pending.


## Tool-progress readability remains unsatisfactory, 19 October 2026

P-087: author reports mostly Thinking with tool labels flashing too briefly to read, including
on a four-call answer. The final presence item remains unchecked. Local warmed tools measured
median 4.07 ms detection, 13.33 ms search and 0.82 ms saved reputation, five calls each with
external fetches blocked; these are not live model/browser timings. B-065/AUD-027 retain this
failed review and proposed single-line past-tense last-activity treatment. No UI/spec change
without agreement. The lifecycle implementation's automated checks remain valid evidence of
tracking accuracy, not evidence that the live presentation is accepted.


## Live reputation lookup isolated, 19 October 2026

P-089 authorised testing the external lookup alone. One uncached public IP 1.1.1.1 request to
AbuseIPDB returned source live in 0.477 seconds. The actual core ask lifecycle path emitted
start at 0.014 seconds and end at 0.491 seconds. A fixed fake model and temporary in-memory
checkpointer avoided paid model calls and real saved-history mutation. No cache/application/UI
change. This is measured network-path evidence, not browser perceptibility or final acceptance.
The author's pause on the past-tense display proposal remains in force. B-065/AUD-027 and the
tool-progress presence item stay open.


## Multi-IP progress feedback positive, 19 October 2026

After the reputation-only four-IP test question (P-090), author replied “way better” (P-091).
Record positive readability feedback for current single-line progress. No independent response,
tool count or timing capture supplied. Further display refinement stays held. Requested explicit
approval of the current behaviour before closing the final progress presence item or B-065/AUD-027.
Other scenario checks and final acceptance remain open. No application change or call by Codex.


## Current tool progress and presence checklist accepted, 19 October 2026

Author replied “aprroved” to the explicit current single-line progress acceptance question,
including the fast-cached-call limitation (P-092). Closed B-065/AUD-027 and the last presence
item. All ten presence items now have dated author rulings. Updated the spec Presence gate and
ticket 19 accordingly. The cumulative list was rejected; the later past-tense proposal stays
unimplemented. Remaining scenario items, audit concerns and final acceptance are open.
No code change, test rerun, external lookup or model call for this acceptance update.


## Scenario overnight spike accepted, 19 October 2026

Author replied “approved” to the Reset-view hourly-chart check around early 8 October (P-093).
Closed scenario step 1 only. Steps 2–7 remain open; step 8 already has its separate next-day
ruling. No application change, repeated tests, model call or external lookup.


## Scenario opening question completed, 19 October 2026

Author replied “confirmed” to the explicit completion check for a new Investigation asking
“Anything suspicious last night?” (P-094). Closed scenario step 2 only. Findings, search,
reputation details, exact unnamed follow-up and report steps remain open. No content pass
inferred from successful completion. No code change, model call or external request by Codex.


## Scenario brute-force evidence confirmed, 19 October 2026

Author replied “confirmed” after inspecting detection evidence for brute force from
185.218.86.24 against daniel.hughes (P-095). Closed scenario step 3 only. IP search and the
post-failure success remain a separate check. No code change or call by Codex.


## Scenario IP search and subsequent success confirmed, 19 October 2026

Author replied “confirmed” to the separate sign-in-search evidence check for 185.218.86.24,
including daniel.hughes succeeding at 02:32:20 UTC on 8 October after the failures (P-096).
Closed step 4 only. Reputation, exact unnamed follow-up and report scenario checks remain open.
No code change, repeated tests or external/model call by Codex.


## Scenario reputation fields confirmed, 19 October 2026

Author replied “confirmed” after checking score 100/100, country NL and owner
TC DATACENTER LIMITED MANAGED IP SPACE for 185.218.86.24 (P-097). These match the saved
response, read independently without an external lookup. Closed step 5 only. Exact unnamed
follow-up and report scenario checks remain open. No code change, tests or call by Codex.


## Scenario unnamed follow-up confirmed, 19 October 2026

Author replied “confirmed” to the exact unnamed follow-up check in the same Investigation
(P-098): daniel.hughes identified, both later successful GB sign-ins returned and a new sign-in
search shown. Closed step 6. This is a dated live ruling for the scenario's singular reference;
it does not close AUD-020's separate concern about whole-case multi-account recap scope.
Report/PDF scenario check and final review remain open. No code change or call by Codex.


## Scenario report accepted; PDF comparison pending, 19 October 2026

Author replied “approved” after reviewing all eight report fields against tool evidence and
checking chronological timeline order in the same scenario Investigation (P-099). Record the
report portion of step 7 as accepted; leave the step unchecked until its PDF is downloaded,
opened and compared. This new report's ruling does not fix or rewrite the historical B-059
report, or establish automatic chronological enforcement. Other audit findings remain open.
No code change, repeated tests or external/model call by Codex.


## PDF approved; aggregate scenario evidence needs correlation, 19 October 2026

Author replied “approved” to the scenario PDF download, opening, card comparison and clipping
check (P-100). Record that dated ruling and tick the report/PDF item as an author-confirmed check.
Do not close the aggregate end-to-end gate yet. Read-only inspection of default saved memory
found the three newest exact overnight-question cases each with one turn and no report. Across
all stored cases, no exact unnamed follow-up was found, and reports were present only in two
18 October cases. This does not establish loss, a failed UI action or incorrect author feedback;
the current reviewed case or runtime data location may differ. Requested the Investigation URL
to correlate the author's rulings with the right saved case. B-067/AUD-029 track this verification
gap. Prior confirmations are retained; the aggregate ruling remains pending.

The accepted next-day check also names a different prior case (872227a3ca7948748f7b4f1ec57ee6c3).
Before claiming one complete same-case eight-step scenario, resolve case identity and the scope
of the combined evidence. No quiet waiver or data mutation. No model or external reputation call.


## Linked case verified; scenario mismatches confirmed, 19 October 2026

P-101 links `90c317b74bb94e2b9d066e2515da5d1f`. Live GET through port 5174 returned 200 and
matches the default saved store. Created 19 October at 10:24:08 UTC, first question “Was any
account compromised this week?”. Two turns: initial question with detection and three reputation
lookups, then report. No sign-in search and no unnamed follow-up are saved in this case.
The report's timeline dates are 6 October, 8 October, 8 October, 6 October, so chronological
ordering is not satisfied. B-058/B-059 and AUD-022/AUD-023 record these existing defects recurring.

Case identity is established; no evidence of lost stored history or a different runtime store.
It is still unknown whether the author used a different case for the earlier confirmations.
Retained those dated rulings and report/PDF appearance acceptance, but reopened scenario steps
2, 4, 6 and 7 rather than treating this broad-case sequence as the exact overnight scenario.
B-067/AUD-029 remain open for acceptance correlation. Requested whether the follow-up used
another case and its URL. No replay, historical report edit or live-memory mutation.


## All saved cases searched for follow-up evidence, 19 October 2026

P-103 authorises finding the case across history. Read-only search covered all 16 Investigations
and 31 saved turns. Normalised exact unnamed wording was absent. Two named-account matches:

| Case | Saved question | Evidence |
| --- | --- | --- |
| 9f06429702864efca91a6fab8f7c1517, turn 3 | Did  daniel.hughes sign in from anywhere else afterwards? | One search; answer includes both expected later GB IPs and timestamps |
| 872227a3ca7948748f7b4f1ec57ee6c3, turn 4 | What were the two later GB sign-ins for Daniel? | One search; answer includes both expected later GB IPs and timestamps |

This establishes named-account follow-up evidence and identifies the related saved cases without
further manual URL hunting. The exact unnamed-reference check remains unperformed in the saved
record. B-067/AUD-029 are now narrowed to exact-scenario evidence and same-case continuity;
no history loss is demonstrated. No app/history mutation, model call or external request.


## Exact unnamed reference verified from saved result, 19 October 2026

P-105: author reports completion in the identified existing case
`9f06429702864efca91a6fab8f7c1517`. Read-only inspection verifies turn 6 has exactly
“Did that user sign in from anywhere else afterwards?”. Answer identifies daniel.hughes and
returns successful GB sign-ins at 07:23:26 UTC from 198.51.100.20 and 08:45:37 UTC from
203.0.113.10 on 8 October. Both IPs and exact timestamps are present in that case's earlier
turn-3 search result. This is grounded unnamed-reference recall within the saved conversation.

Turn 6 has zero tool calls. It reused already gathered evidence, so it does not establish a new
search in the exact overnight scenario. Do not call the lack of a redundant search a new defect
merely because this repeat question used memory. Step 6's combined fresh-search/same-scenario
condition remains open; the narrower recall gap is resolved. AUD-020's whole-case recap scope,
missing initial broad searches and report-order defects remain separate. No replay, model call,
external request or stored-history change by Codex.


## Two evidence fixes and consolidated verification, 19 October 2026

P-107 authorises fixing B-058 (missing searches) and B-059 (report order). Standard LangChain
before_model middleware now schedules missing whole-IP searches from actual current-turn
findings before continuing. Completed attempts, including failures, are not repeated. Explicit
attack-type and literal-IP questions preserve their narrow scope. New report timelines sort
by parsed aware timestamps before save/return, with the same order in the PDF. Invalid new
timestamps refuse saving. Historical reports remain unchanged. Prompts/tool schemas/grader
and frozen v1 stay unchanged; the eval fingerprint now includes policy/order source.

Retained verification iterations:

- Initial full backend suite: 390 passed before the scope refinement.
- Initial benchmark 4caada27: 55/57 overall and 15/15 security. Q08 runs 1 and 3 failed when
  automatic searches broadened a password-spraying question. B-069 records cause/correction;
  result 2026-10-19-110557-4caada27.json is preserved.
- Final narrow-scope regressions and unchanged copied agent tests: 31 passed.
- Final Pyright: zero errors, warnings or information messages.
- Final API benchmark 7ff8e5ae: 56/57 overall (98%) and 15/15 security (100%), zero live reputation
  lookups; file backend/evals/results/2026-10-19-111011-7ff8e5ae.json. Q08 now 3/3. One Q07
  attempt lists the correct two later events but claims three; B-070/AUD-030 retain it as failed.
- Consolidated review case: `ba63f90e8f6f465a9633817b8c898abb`, created 19 October. Opening exact
  overnight question performs detection, attacker-IP search with success evidence and reputation.
  Exact unnamed follow-up identifies Daniel, returns both later GB events and performs a fresh
  user search. New report has all fields and chronological order; reopened report equals returned
  report; PDF parses, title and sections match. Evidence: .scratch/v2-port/research/28-consolidated-scenario.json.
  This live case ran on 4caada27; the subsequent narrow-only exclusion leaves its broad branch
  unchanged, verified by final real-model benchmark and regressions. No second app case created.
- Final review API reloaded on 8010; proxied endpoint returns 200. All 17 IDs (the original 16
  plus the deliberately created review case) match before/after final reload.

The final backend regression run is in progress and will be appended. Frontend is unchanged
by these two fixes; its latest 141-test/build/type-check evidence remains applicable.

The strict manual scenario gate remains open for the author's consolidated-case ruling and
next-day reopening/continuation of that same case. The earlier next-day acceptance remains
valid for its different case; it cannot silently substitute for this case's full sequence.
No final acceptance, push or historical report rewrite is implied.


Final P-107 backend regression result: all 393 tests pass in 227.32 seconds on the final
scope-preserving revision. Final Pyright: zero errors, warnings or information messages.
No new frontend changes; latest 141 frontend tests/build/type-check remain supporting evidence.
Questions, grader, copied agent tests and dependency lockfiles remain unchanged. Documentation
diff check passes. Two fixes are ready for one consolidated author case/PDF/layout review;
same-case next-day continuation remains pending. Existing audit concerns and B-070 remain open.


## Consolidated case and layout accepted, 19 October 2026

Author replied “approved” (P-108) to the combined review of case
`ba63f90e8f6f465a9633817b8c898abb` and its PDF: required searches, chronological report and
Investigator layout with chat as the focus. Closed B-058/AUD-022, B-059/AUD-023 and the scoped
B-069 correction. B-067/AUD-029 case-correlation gap is resolved by the verified shared case.
All four visual-hierarchy rows and presence checks are accepted. Scenario steps 1–7 now share
the consolidated evidence and dated ruling. Only its same-case next-day continuation remains
before the final aggregate scenario and author sign-off. Ticket 19 remains ready-for-human.
Historical reports are unchanged. B-070/AUD-030 and other unrelated concerns remain open.
No code change, tests, model/reputation calls or push for this acceptance update.


## Closure, 19 October 2026

P-110 explicitly instructs closure and approves whatever remains for this course demo.
Ticket 19 is resolved. The remaining same-case next-day continuation check is waived, not
claimed as tested. All earlier evidence and review iterations are retained. Known defects
and enhancements remain in the audit register for optional future work. No additional
testing, implementation or push was required or performed for this closure. This final
ruling supersedes historical pending acceptance notes above.
