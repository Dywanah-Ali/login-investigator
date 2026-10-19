# 19: Parity closing

**What to build:** the proof that the Port is done. Every row of the acceptance gate in the spec is
ticked with named evidence, the cross-screen checks pass through the API, a fresh clone starts from
the README, and the author closes the manual checklist and the eight-step scenario with a dated ruling.

**Blocked by:** 14 (Alerts), 15 (Log explorer), 17 (Investigator screen), 18 (Eval set in API mode).

**Status:** resolved

Spec: [spec.md](../spec.md), "Testing Decisions" (the gate table and the eight-step scenario).
Decisions: ticket 08.

- [x] API replay tests that need every screen: a filter change updates every screen consistently; an empty filter gives a clear message on all three; reset restores the whole log
  - Evidence: four added cases in `backend/tests/test_api_dashboard.py`, 50 dashboard tests pass; all three frontend empty-message tests pass.
- [x] Full automated set green: pytest (copied, adapted, boundary, API), Vitest, the eval API mode run from ticket 18
  - Evidence, 18 October: 374 pytest, 114 Vitest, both type checks and frontend build pass. Accepted T18 benchmark regraded unchanged: 56/57 overall, 15/15 security. Existing warnings listed in `docs/parity-closing.md`.
- [x] Fresh clone: both servers start from the README's two commands in a clean folder
  - Evidence: independent local clone of `9d28987`, new dependency folders, README setup and alternate API-port configuration. Direct/proxied replies match, four frontend routes load, missing-key Investigation is 503. Initial verifier address bug retained as B-042.
- [x] A scan of every git object finds no real key value or key pattern, except the explicitly approved fake test key; no personal name or email in any file
  - Evidence: all 1,084 objects scanned; classification in `docs/parity-closing.md`. Author approved the fake test-key exception on 18 October 2026, prompt P-035.
- [x] Visual hierarchy checked by eye on all four screens: one element leads each (spec, "The frontend"); the Overview's leading element decided then
- [x] The manual presence checklist ticked by the author with a dated ruling: synthetic label, metric labels, empty-state messages, scope note, AI note, progress words per tool, locked input, severity labels and colours on the report card, charts per theme, error messages hide exception text
  - Reference for the Overview (author's ruling 2026-10-14, ticket 13, point 4; spec decisions log): its metric labels, chart titles and empty-state text are checked against the agreed screens prototype (`research/07-screens-prototype.html`), not v1's code. A wording that differs from v1 but matches the prototype passes. The failed share rounds a half up, and the sidebar links keep the filters, both as decided. Every other item is checked against v1, as the gate says
- [x] Scenario accepted by the author on 19 October 2026, P-110. Steps 1–7 have evidence; the remaining same-case next-day check is explicitly waived for the course demo, not recorded as performed.
- [x] The gate table in the spec rewritten as a ticked list with the evidence named beside each box, in v1's style
  - Evidence: spec Testing Decisions. Manual rulings remain unchecked; the repository-scan exception was approved on 18 October 2026.
- [x] Bug log and prompt log maintained through closure, P-110; known issues remain documented for optional future work.
- [x] Author approved closure and all remaining acceptance items on 19 October 2026, P-110. Nothing pushed; this approval does not instruct a push.

## Comments

### 2026-10-18 · Automated gate and review handoff

Author's go: P-034. Working base `9d28987`; application code unchanged.
Evidence and the author's review sheet: [docs/parity-closing.md](../../../docs/parity-closing.md).
The 254 original checks were independently collected from twelve byte-identical copied files
plus the retained original boundary test. Full automated suite passes.

Repository scan: all 1,084 objects contain neither loaded key value; no personal information
found in tracked files. One provider-key pattern is the deliberately fake exception-leak fixture
in `test_api_errors.py`. The literal zero-pattern gate is left open pending the author's ruling;
no history rewrite or quiet exception. Commit emails are GitHub noreply or assistant-bot noreply.

The author's presence, visual-hierarchy and eight-step-scenario rulings remain pending.
The Overview's leading element is still for the author to decide. Ticket stays open.
B-041, B-017, six lint warnings and the build-size warning remain visible and unchanged.
Nothing pushed. The next step is the author's live review, one item at a time.

### 2026-10-18 · Repository-scan exception accepted

Author answered "yes" to keeping the made-up API key in the error-leak test and recording
"Scan passed. One fake test key is intentionally present." Prompt P-035 records the approval.
The scan checkbox and Engineering gate are now closed with that explicit exception.
No test fixture or Git history was changed. Visual, presence and scenario review remain open.

### 2026-10-18 · Overview Alerts-card adjustment

Author found the Overview good overall and approved an attention cue on its Alerts metric:
green zero, amber above zero, coloured count and matching subtle icon, quiet card background.
Recorded the design before implementation. `section-cards.tsx` implements it; B-043 and P-036
preserve the issue and approval. Live API confirms five alerts for the whole log and zero for GB.
The final styled card still needs the author's live confirmation; no inferred hierarchy ruling.

Validation after styling: 114 frontend tests, type check and production build pass. Lint has
only the six existing warnings. Existing bundle warning remains. Nothing pushed.


### 2026-10-18 · Overview accepted

Author's ruling, verbatim: "its good. approved" (P-037). This closes the requested Alerts-card
adjustment after the earlier acceptance of the overall Overview. Its count and subtle status
icon provide the agreed attention cue. Updated the Overview review row in the evidence sheet.
The other three screens, remaining presence checklist and eight-step scenario remain open.
No application changes or repeated tests for this documentation update. Nothing pushed.


### 2026-10-18 · Alerts caption cleanup and proposed features

Author requested keeping only the total above the Alerts table and removing its row/page-size
caption. Recorded the decision before implementation; pager navigation remains. B-044 and
P-038 record the feedback. The author asked for an opinion before any work on a rule filter
or severity column. Neither feature nor detection research is implemented by this change.
Alerts review remains open.


### 2026-10-18 · Alerts accepted; Explorer captions simplified

Author accepted the current Alerts screen and moved to Explorer (P-045). Updated the evidence
row. Rule filtering and default severity remain the approved post-Parity follow-up in ticket 26.
Explorer feedback (P-046): show only the row count in its footer and remove the sampling sentence.
Recorded the wording decision in the spec before editing. Its proposed event severity remains
an opinion request only. Explorer's final live ruling is pending.

Explorer caption validation: all 114 frontend tests, type check and build pass. Only the existing
six lint warnings and bundle-size warning remain. Final Explorer ruling stays pending.


### 2026-10-18 · Explorer accepted; Investigator review next

Author's ruling, verbatim: "ok approved now lets move to the most important one "investigator" page"
(P-047). Recorded the dated Explorer approval in the evidence sheet. Investigator layout,
remaining presence checks and eight-step live scenario remain open. No application change.


### 2026-10-18 · Investigator first-use layout accepted

Author found the initial screen, before any Investigation and without history, stable and
reliable (P-048). Recorded that scoped layout ruling. Active answering, follow-up, tool evidence,
report/PDF and persistence remain pending. No functional gate inferred from appearance alone.
Next manual step: choose "Anything suspicious last night?", send, and inspect progress, input
locking and the first answer before continuing the scenario. No model call made by Codex.

### 2026-10-18 · Investigator progress moved into the chat

Author requested moving the status from below the chat into the chat itself (P-049, B-049).
Recorded the decision before implementation. Status now follows the active draft, or appears
as a separate message item during waits without a draft, including report generation. Keep one
accessible status and the current wording/input lock. Final live confirmation remains pending.

Progress-placement validation: 114 frontend tests, type check and build pass. Existing stream
and report tests assert one status inside the chat viewport. Existing warnings remain.


### 2026-10-18 · Progress placement accepted; prompt keyboard adjusted

Author said the in-chat progress is better, then requested Enter to send and Shift + Enter for
newline (P-050). Recorded the placement acceptance and keyboard design before editing. Keyboard
submission uses the existing form and send guard; composition Enter is left to the input method.
B-050 records the issue and fix. Final live keyboard confirmation and scenario remain open.

Keyboard validation: 20 Investigator checks and all 116 frontend tests pass, including multiline
submission and input-method guards. Type check and build pass; only existing warnings remain.
Test response-header correction is preserved as B-051. Live keyboard confirmation still pending.


### 2026-10-18 · Chat keyboard accepted; answer evidence next

Author said the keyboard behaviour is good and asked for the next Investigator test (P-051).
Recorded acceptance of Enter to send and Shift + Enter for newline. Next: check the answer to
"Anything suspicious last night?" against its tool evidence. Do not mark factual answer,
follow-up, report or persistence checks passed from layout/keyboard approval.

### 2026-10-18 · Tool evidence accepted; animated expansion requested

Author accepted the current tool outputs within their defined capabilities and left richer
insight for future enhancements. This is a tool-evidence ruling, not blanket acceptance of all
agent answers or the report/PDF/persistence scenario. After confirmation, the author gave go
for smoother Tools used expansion (P-052, B-052).
Inspected the report's observed-pace text reveal. Tools now expands its full saved evidence with
a bounded height/fade animation using the same pace, a steady fallback and reduced-motion bypass.
No backend, evidence content or tool execution change. Live animation confirmation remains open.

Tools animation validation: 116 frontend tests, type check and build pass after the reactive-pace
correction logged as B-053. Only six existing lint warnings and the existing bundle warning
remain. Visual pacing still needs the author's live ruling. No paid model call made.

### 2026-10-18 · Expanded tools follow into view

Author could not assess the animation because opening evidence left it below the visible chat
(P-053). B-054 records the actual visibility bug. Added scoped following of the selected panel
for its opening interval, with a stable duration captured on open. Stop on manual interaction,
closing or unmount; reduced motion reveals once. Scroll only this chat viewport, not the outer
page or unrelated later messages. B-055 preserves a weak initial test corrected during review.
Final visual confirmation remains pending; the previous animation has not been deemed accepted.

Visibility-follow validation: 25 focused checks and all 121 frontend tests pass. Type check and
build pass. Only six existing lint warnings and the bundle warning remain. Exact selected-panel
scrolling, manual interruption, duration snapshot, close/unmount and reduced-motion reveal are
checked at the DOM boundary; final visual acceptance stays with the author.


### 2026-10-18 · Tool expansion and following accepted; memory next

Author accepted the updated tool expansion and scroll following (P-054). Recorded the dated
ruling. Next manual step: in the same Investigation, ask "Did that user sign in from anywhere
else afterwards?" without repeating the username. Ground truth S3 has two subsequent successful
GB sign-ins for the investigated account. No memory or later scenario check marked passed yet.


### 2026-10-18 · Author accepts conversation continuity; report next

P-055 supplies a live conversation and the author's memory acceptance. The named-account follow-up
matches both S3 later successful GB sign-ins. Record this scoped acceptance, without claiming that
repeating the username tests unnamed-reference recall or that reopening persistence has passed.
Opening-answer compromise wording concern recorded as B-056. No application change or model call.
Next manual step is report creation in the same Investigation; report/PDF and reopening remain open.

### 2026-10-18 · Current report accepted; maintained improvement audit created

Author accepted the current report and deferred clearer user control of report scope (P-056).
Recorded the scoped ruling in docs/parity-closing.md. Created docs/audit/improvement-register.md
and linked its maintenance rules from AGENTS.md and CLAUDE.md at the author's request. The register
collects discussed future work and unresolved concerns without expanding this ticket's scope.
PDF download/opening and reopening/continuation still need the author's ruling. Nothing pushed.


### 2026-10-18 · PDF accepted; saved Investigation next

Author accepted the downloaded/opened PDF following the content and clipping check (P-057).
Recorded the scoped ruling in docs/parity-closing.md and updated the audit register's remaining
checks. Next: refresh, reopen this Investigation from its history and continue it. The specified
next-day continuation remains a separate pending ruling. No code changed. Nothing pushed.

### 2026-10-18 · User-linked conversation diagnosis

Read-only API review (P-058) shows saved history and unnamed account recall, but no proof of blanket
memory reliability. Final summary omits later sign-ins; clarify the author's concern before a fix.
New existing-behaviour defects recorded as B-057/B-058/B-059: missing prompt-injection warnings,
skipped required IP searches and report timeline out of order. AUD-020 to AUD-023 track follow-up.
Earlier UI/report/PDF acceptances remain scoped rulings; assess these findings before final closing.
No application change, model replay or conversation mutation. Ticket 19 stays open.

### 2026-10-18 · Conversation isolation investigated

P-060 authorised diagnosis of suspected mixing across conversations. The three live histories
with the repeated recap each have Daniel in their own earlier evidence/report. Code selects
one thread by the URL/API case ID. An offline boundary probe captured seven question-model and
two report inputs across three temporary cases, including alternate follow-ups and restart,
with zero cross-case marker leaks. Three existing backend and two frontend navigation checks
pass. Evidence/probe in docs/audit/conversation-isolation-2026-10-18.md. No demonstrated mixing;
recap scope remains AUD-020/B-060. No app or live-history mutation; no paid call. Ticket stays open.

### 2026-10-18 · Theme selector requested and implemented

Author found no in-app control after being asked to review both themes and requested standard
implementation (P-061). Recorded the shared-header Light/Dark/System decision in the spec first.
Implemented on existing theme tokens and shadcn Select, with System default, persisted preference,
live OS tracking, storage fallback, tab synchronisation and startup application before paint.
No backend or dependency change. B-061/B-062 retain the missing control and test-context iteration.
AUD-024 tracks final author review. Both-theme readability is not inferred from automated checks.

Theme checks: all 134 frontend tests pass, including 13 new cases for keyboard interaction,
explicit/system modes, persistence, live OS changes, listener cleanup, blocked/invalid storage,
cross-tab sync, route changes, API failure and initial script/provider agreement. Type check,
lint and production build pass. Only six existing lint warnings and the bundle warning remain.
Live server serves the changes. Author reviews appearance next; no screenshot/automation gate.

### 2026-10-18 · Theme review accepted apart from Alerts header tone

Author said other reviewed appearance is good and requested a slightly darker Alerts header in
both themes (P-063). Applied a scoped palette-based darkening and disabled header-row hover tint,
preserving selection and other tables. B-063/AUD-025 record the adjustment. Author confirmation of
the final tone remains pending. No broader checklist/scenario acceptance inferred.

Header-tone validation: 14 existing Alerts tests pass; production build/type check pass. Existing
bundle-size warning remains. No new CSS-only test. Diff checked; live tone confirmation pending.

### 2026-10-18 · Alerts header accepted

Author approved the updated header with “good” (P-064). Closed AUD-025/B-063 with the dated visual
ruling and existing passing Alerts/build evidence. Theme appearance feedback is addressed;
unrelated manual presence/scenario checks and final author acceptance remain open.

### 2026-10-18 · Empty states, filter carry-over and Reset accepted

Author confirmed “all good” after the three-screen empty-view and reset review (P-065).
Ticked only the corresponding presence item in docs/parity-closing.md with the dated ruling.
Used available picker values User daniel.hughes and Country RU. Live API reads returned zero
matches on Overview, Alerts and Explorer. Other checklist/scenario items remain open.

### 2026-10-18 · Safe connection error accepted; backend restored

P-066 authorised the live outage check; P-067 confirmed the expected connection message without
technical details. Stopped only the verified project API listener, preserved frontend service,
then restarted the backend. Proxied Overview is 200 with 1,856 rows; the ten saved Investigation
IDs are unchanged. Four targeted Overview error-message checks pass. Ticked only the matching
presence item. Other unchecked presence/scenario items and final approval remain pending.

### 2026-10-18 · Input locking and unlocking accepted

Author confirmed “all good” after checking that the prompt and Send are disabled while answering
and usable after completion (P-068). Closed the corresponding presence item with this dated
ruling. No new code or repeated tests. Other unchecked presence/scenario items remain open.

### 2026-10-19 · Next-day continuation result supplied

After local server restart, the author supplied inline views showing yesterday's report and
a completed new answer in the same selected Investigation. Both later Daniel GB sign-ins
match S3. Recorded the observations in docs/parity-closing.md. Requested explicit author
acceptance before ticking scenario step 8. No screenshot artifact, application change or
model call by Codex. B-059's existing report timeline issue remains unresolved. Other manual
checks and final approval remain open.


### 2026-10-19 · Next-day reopening and continuation accepted

Author replied “approved” (P-071). Closed only scenario step 8 in docs/parity-closing.md,
with the saved Investigation ID verified by a read-only lookup. Remaining presence/scenario
checks, existing audit concerns and final acceptance remain open. No application change or
repeated tests. Nothing pushed.


### 2026-10-19 · History navigation concern under review

Author reports history is not quite like v1 (P-073). Read-only comparison identifies missing
collapse control, different expansion around older selected cases and absent reveal animation.
B-064/AUD-026 retain the findings. Asked whether the actual concern is the list or reopened
messages. No application/spec change; screen treatment awaits clarification. Accepted next-day
recovery remains scoped and accepted. Other manual gates stay open.


### 2026-10-19 · History arrows and list behaviour restored

P-074 confirms the differences and v1 arrow controls. Recorded the screen decision in the spec
before implementation. B-064/AUD-026 now have implementation evidence: accessible arrow-only
controls, groups of three, continuous prefix including older selected cases, collapse retaining
selection, reduced-motion-aware reveal. All 136 frontend tests and build/type check pass; six
existing lint warnings and bundle warning remain. Awaiting author live acceptance. Nothing pushed.


### 2026-10-19 · History navigation accepted

Author tested the restored history navigation and replied “yes all good” (P-075).
B-064/AUD-026 are closed with the live ruling and P-074's passing checks. Remaining presence
and scenario rulings stay open. No application change or repeated tests. Nothing pushed.


### 2026-10-19 · Empty Investigation scope and starters accepted

Author approved the read-only scope explanation and all three starter questions in a new
Investigation (P-076). Closed the corresponding presence item in docs/parity-closing.md.
Other manual gates remain open. No code change or repeated tests. Nothing pushed.


### 2026-10-19 · AI note accepted

Author approved the AI note's visibility and readability below the question box (P-077).
Closed the corresponding presence item in docs/parity-closing.md. Other manual gates remain
open. No code change or repeated tests. Nothing pushed.


### 2026-10-19 · Report severity display accepted

Author approved the saved report's Critical severity label and red colour cue (P-078).
Closed the corresponding presence item in docs/parity-closing.md. Approval covers presentation;
existing reasoning concerns and other manual gates remain open. No code change or repeated tests.
Nothing pushed.


### 2026-10-19 · Chart readability accepted

Author approved both Overview charts and labels in Light and Dark (P-079). Closed the matching
presence item. Remaining presence items: synthetic label/capture date, metric labels/titles/figures,
and per-tool progress words. Scenario and final acceptance remain open. No code change or
repeated tests. Nothing pushed.


### 2026-10-19 · Overview labels and figures accepted

Author approved the four Reset-view metrics, failed share and both chart titles (P-080).
Closed the matching presence item. Synthetic label/capture date and per-tool progress words
remain unchecked; scenario and final acceptance remain open. No code change or repeated tests.
Nothing pushed.


### 2026-10-19 · Synthetic-data header accepted

Author approved the synthetic-data label on both screen sizes and desktop capture timestamp,
with timestamp hidden on narrow screens as agreed (P-081). Closed the matching presence item.
Per-tool progress wording is the final unchecked presence item. Remaining scenario rulings
and final acceptance stay open. No code change or repeated tests. Nothing pushed.


### 2026-10-19 · Reputation progress visibility failed live review

Author reports missing reputation progress wording despite saved tool evidence (P-082).
B-065/AUD-027 record the confirmed latest-event replacement weakness and proposed cumulative
activity treatment. Exact live event timing is unknown. Per-tool progress presence remains open;
no UI/spec change pending author agreement. No model call by Codex.


### 2026-10-19 · LangChain lifecycle research completed

Author rejected cumulative activity display, retaining one changing line, and requested official
LangChain documentation (P-083 to P-085). Research note:
../research/27-tool-progress-lifecycle.md. Three offline probes confirm genuine parallel
start/end events and error reporting in installed versions. Recommended existing sync stream
with public callbacks/custom events; native v3 is experimental. No application or spec change.
Agree lifecycle contract and single-line treatment before implementation. B-065/AUD-027 and
tool-progress presence remain open. No model call or live-history write. Nothing pushed.


### 2026-10-19 · Execution-based single-line progress implemented

P-086 authorises the researched approach. Spec and API contract updated before code. Per-request
LangChain callbacks publish start/end/error through custom streaming; API sends only allowlisted
name, opaque call ID and phase. Frontend tracks active IDs, handles overlapping/duplicate names,
uses a single combined phrase, and clears completed/failed activity. Existing legacy Stream
callers and copied tests remain compatible. No prompt/model/tool/grader change.

379 backend tests passed in the full run; the final added HTTP privacy case passed separately,
covering all 380 current cases. All 141 frontend tests, build/type check pass. Six existing lint
warnings and bundle warning remain. Explorer timeout and passing reruns retained in B-066/AUD-028.
API restarted; endpoint is 200 and all 12 saved IDs are unchanged. Full evidence is in
docs/parity-closing.md. B-065/AUD-027 and tool-progress presence await live author acceptance.
No model call by Codex or push.

Final backend Pyright check after all additions: zero errors, warnings or information messages.


### 2026-10-19 · Lifecycle progress fails practical readability review

P-087: author mainly sees Thinking and unreadable tool flashes despite four tool calls. Recorded
failed live review and local warmed-tool measurements in B-065/AUD-027 and Parity evidence.
Proposed retaining only the most recently finished activity in past tense while preparing the
response, within the single line. No UI or spec change yet; author agreement pending. Final
presence/scenario gates stay open. No model call or live-history write by Codex. Nothing pushed.


### 2026-10-19 · Isolated live reputation lookup succeeds

P-088 held the proposed further UI change. P-089 requested live reputation testing alone.
One uncached 1.1.1.1 AbuseIPDB lookup took 0.477 seconds, source live, matching lifecycle
start/end events through real core ask with a fixed fake model and temporary memory.
No real Investigation/cache/UI mutation. One sample does not establish browser visibility;
B-065/AUD-027 and the presence gate remain open. No paid model call or push.


### 2026-10-19 · Multi-IP progress more readable

Author said “way better” after the four-IP reputation-only question (P-090/P-091). Recorded
positive readability feedback for current progress without claiming all four calls were live
or successful. Proposed further UI changes remain held. Explicit final progress ruling requested;
other unchecked gates and audit concerns remain open. No code change or external call by Codex.
Nothing pushed.


### 2026-10-19 · Tool progress accepted; presence checklist complete

P-092 explicitly approves current single-line progress including brief cached-call visibility.
Closed B-065/AUD-027. All ten presence items now have dated rulings in docs/parity-closing.md;
closed the corresponding ticket and spec gates. Further display proposals remain unimplemented.
Scenario steps 1–7, visual-hierarchy aggregate ruling, final log completeness and final author
review remain open. No application change, tests, model call or external request. Nothing pushed.


### 2026-10-19 · Scenario step 1 accepted

Author approved the overnight spike in Overview's Reset-view hourly chart (P-093). Closed
scenario step 1 in docs/parity-closing.md. Steps 2–7 and final aggregate rulings remain open;
step 8 is already accepted separately. No code change, tests or external/model call. Nothing pushed.


### 2026-10-19 · Scenario step 2 completed

Author confirmed the new exact-wording overnight question finished without error (P-094).
Closed only scenario step 2; findings/evidence and subsequent steps remain open. No code change,
repeated tests or model/external call by Codex. Nothing pushed.


### 2026-10-19 · Scenario step 3 confirmed

Author confirmed the detection finding identifies brute force from 185.218.86.24 against
daniel.hughes (P-095). Closed step 3 only. Steps 4–7 and final review remain open. No code
change, tests or external/model call by Codex. Nothing pushed.


### 2026-10-19 · Scenario step 4 confirmed

Author confirmed the separate IP search and successful daniel.hughes sign-in at 02:32:20 UTC
on 8 October after the failures (P-096). Closed step 4. Steps 5–7 and final review remain open.
No code change, tests or external/model call by Codex. Nothing pushed.


### 2026-10-19 · Scenario step 5 confirmed

Author confirmed the reputation score, country and network owner for 185.218.86.24 (P-097),
matching its saved response. Closed step 5. Steps 6–7 and final review remain open. No code
change, tests or external/model call by Codex. Nothing pushed.


### 2026-10-19 · Scenario step 6 confirmed

Author confirmed the exact unnamed follow-up identifies daniel.hughes, returns both expected
later GB successes and shows a new sign-in search (P-098). Closed step 6. AUD-020's whole-case
recap concern remains separate. Step 7 and final review remain open. No code change, tests or
external/model call by Codex. Nothing pushed.


### 2026-10-19 · Scenario report accepted; PDF next

Author approved all eight report fields, consistency with tool evidence and chronological
timeline in the current scenario (P-099). Step 7 remains unchecked pending this report's PDF
comparison. Historical B-059 and other audit concerns remain open. No code change, tests or
external/model call by Codex. Nothing pushed.


### 2026-10-19 · Scenario PDF approved; aggregate closure held for case correlation

P-100 approves PDF download/opening/comparison and unclipped text. Recorded the author ruling
for step 7. Read-only saved-memory inspection does not yet correlate the reviewed exact unnamed
follow-up/report sequence; requested the current URL. B-067/AUD-029 track the evidence gap,
including that next-day acceptance names a different case. No product/data-loss claim, silent
waiver or revoked author ruling. Aggregate scenario gate remains open pending correlation.
No application change, live-history mutation, model/reputation call or push.


### 2026-10-19 · Linked case differs from exact scenario

P-101 supplied case 90c317b74bb94e2b9d066e2515da5d1f. Live API/store match: weekly-compromise
opening and report, detection plus three reputation lookups, no sign-in searches or unnamed
follow-up. Report timeline is unordered. Recorded recurrences of B-058/B-059, retained dated
feedback and reopened scenario steps 2/4/6/7 for actual evidence. Asked if another case was used
for the follow-up. Aggregate gate remains open. No history loss demonstrated, no app/history
mutation or model call. Nothing pushed.


### 2026-10-19 · Relevant follow-ups found across saved history

P-103 authorises searching history. All 16 cases/31 turns inspected read-only. Found both
named-account follow-ups, each with one sign-in search and expected later GB IPs/timestamps.
Details in docs/parity-closing.md and B-067/AUD-029. Exact unnamed wording is absent; its
scenario check remains open. Related history is retained. No more manual URL hunting needed.
No model/external call, application/history mutation or push.


### 2026-10-19 · Exact unnamed recall verified; earlier evidence reused

P-105 reports completion. Read-only inspection of 9f06429702864efca91a6fab8f7c1517 turn 6
verifies exact unnamed question, Daniel and both expected later GB IPs/timestamps, all grounded
in turn-3 search. No new tool call. Narrow recall gap resolved; combined step 6 remains open
for fresh-search/exact-scenario continuity. Do not force a redundant search or claim a new bug
from this reuse. Existing initial-search/report-order concerns remain open. No code/history
mutation, model call or external request by Codex. Nothing pushed.


### 2026-10-19 · Two evidence fixes authorised

P-107 directs proceeding quickly with the two remaining issues. Implementation decision recorded
in spec before code: standard LangChain before_model middleware routes missing per-IP searches
to existing tools after detection, using current-turn results only; no repeated completed attempt
or custom graph. Sort new report timelines at the core write boundary using parsed aware ISO
times, before persistence/return. Invalid timestamps refuse saving; no historical rewrite.
Preserve tool schemas, system/report prompts, eval questions/grader and all copied tests.
Validation: real-framework offline omission/duplicate/error/history cases, report persistence/PDF
agreement, then one real-HTTP model scenario and benchmark as appropriate. No UI redesign.


### 2026-10-19 · Two fixes verified; consolidated case ready

P-107 implementation and evidence in docs/parity-closing.md. Final policy preserves explicit
narrow scope while scheduling missing broad per-IP searches. New reports sort before save/return;
PDF uses saved order; historical reports stay intact. Initial 390-case suite passed; final
revision's complete suite is finishing. Final Pyright is clean. Final API benchmark 7ff8e5ae
passes 56/57 overall and 15/15 security, with unchanged questions/grader and no live lookups.
B-069's first-run scope regression is corrected; its failed benchmark remains. B-070/AUD-030
retain the final one-off prose count error, not hidden by the pass bar.

Review case ba63f90e8f6f465a9633817b8c898abb has the full overnight → unnamed follow-up with
fresh search → sorted report → matching reopened report/PDF sequence. Evidence file:
research/28-consolidated-scenario.json. Created once; all 16 prior cases preserved. Final API
reload preserves all 17 IDs. No new UI code, tool schema, prompt or grader change. Benchmark
fingerprint includes new policy/order source. Author case/layout ruling and this same case's
next-day continuation remain open. Do not use another case's earlier next-day result silently.
Nothing pushed.


Final P-107 backend regression result: all 393 tests pass in 227.32 seconds on the final
scope-preserving revision. Final Pyright: zero errors, warnings or information messages.
No new frontend changes; latest 141 frontend tests/build/type-check remain supporting evidence.
Questions, grader, copied agent tests and dependency lockfiles remain unchanged. Documentation
diff check passes. Two fixes are ready for one consolidated author case/PDF/layout review;
same-case next-day continuation remains pending. Existing audit concerns and B-070 remain open.


### 2026-10-19 · Combined case/fixes/layout approved; next-day check remains

P-108 approves consolidated case ba63f90e8f6f465a9633817b8c898abb and PDF, including required
searches, chronological report and chat-leading layout. Closed the visual-hierarchy checkbox
and B-058/B-059/B-067/B-069 with their audit entries. Scenario steps 1–7 have the combined
case's verified evidence and author ruling. Step 8 now explicitly targets this same case on
20 October; the earlier other-case next-day approval remains separate historical evidence.
After that check, finish aggregate scenario, log completeness and final author sign-off.
Ticket stays ready-for-human. B-070 and unrelated audit items remain open. No new code/tests/
model calls or push.


## Answer

Resolved on 19 October 2026 by explicit author approval, P-110. This is a course demo.
The author accepted the remaining scope and waived the additional next-day continuation
check for consolidated case ba63f90e8f6f465a9633817b8c898abb. That check was not performed.
Earlier persistence evidence and scenario steps 1–7 remain recorded in docs/parity-closing.md.

Existing evidence: 393 backend tests, 141 frontend tests, passing type checks/build,
and API benchmark 56/57 overall with 15/15 security. No additional tests were run to close
this documentation task. Known defects and improvements remain in the bug log and audit
register, including B-070/AUD-030. They do not block the author's demo acceptance.
No further implementation started. Nothing pushed. This ruling supersedes earlier pending
acceptance notes in this ticket while retaining their history.
