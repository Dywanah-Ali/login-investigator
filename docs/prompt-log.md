# Prompt Log

The key prompts given to Claude Code while building v2, in order. Each entry gives the author's
prompt verbatim, its purpose, what came back, and what changed next. These may go into course
submissions.

## Entry format

```
### P-001 · 2026-10-14 · Ticket NN Title

**Prompt:**
> the author's prompt, verbatim

**Purpose:** why the prompt was given.
**Result:** what came back.
**Next:** what changed next.
```

## Entries

### P-001 · 2026-10-14 · Ticket 10 Repository foundation

**Prompt:**
> /mp-implement .scratch/v2-port/issues/10-repository-foundation.md

**Purpose:** first build prompt of v2. Build the repository the slices stand on: git, the agreed
layout, v1's core, data, tests and evals copied, and v1's tests passing.
**Result:** repository initialised with a backend uv project and an empty frontend placeholder. v1's
core, data, evals and core and agent tests copied with relative paths preserved; Streamlit and
Plotly dropped from the backend's dependencies. 254 copied tests pass on Python 3.12, not the 259
the spec expected (B-001). The core boundary test now also forbids FastAPI and Starlette.
**Next:** the author reviews the first commit; then ticket 11, the logic moved into the core.

### P-002 · 2026-10-14 · Ticket 10 Repository foundation

**Prompt:**
> "The test-count box is unticked until you rule. It should read 254, not 259. The same 259 appears in the spec, in tickets 08 and 11, and in the map, so one correction should cover all four places." double check from the source pls if u can

**Purpose:** the author challenged the claim before ruling on it, asking for proof from v1 itself.
**Result:** a fresh export of v1's last commit collected 290 tests, 254 outside the two screen
files. The 259 was traced to a subtraction of screen test functions from collected tests. The first
bug log entry had the wrong cause and was corrected. The author then approved the change ("approved").
**Next:** 259 became 254 in the spec, tickets 08, 10 and 11 and the map, with a decisions log row.
Ticket 10 closed with all nine boxes ticked.

### P-003 · 2026-10-14 · Ticket 11 Core: the logic that moved from the screens

**Prompt:**
> /mp-implement

then "go" to the proposed branch, and "ok go ahead" to the proposed test points.

**Purpose:** build the frontier ticket. No ticket was named, so the agent picked ticket 11, stated it,
proposed a branch and the three test points, and waited for the author each time.
**Result:** a new core module `views.py` with `date_window`, `dataset_facts` and `alerts_for_view`,
built test-first with ten tests. The Report offer needed no work: v1 had already moved it into the
core, with tests. The contract left `to` alone undefined; it now runs from the start of the log,
with a decisions log row. A two-axis review found two tests recomputing their expected values; both
fixed. Full suite: 267 passed.
**Next:** the author reviews ticket 11; then ticket 12, the API foundation.

### P-004 · 2026-10-14 · Tickets 20 and 21: the module name and a type checker

**Prompt:**
> approved.
>
> then lets work on those two issues "The project has no type checker set up. I ran one just for this check. The new file is clean. It found 3 type errors in v1's copied generator.py, which this ticket must not touch. Your call whether that becomes a ticket.
> The new file is named views.py and sits beside tool_views.py, which does a different job. A clearer name would be dashboard.py. I kept the name because ticket 03 called these "view functions"."

**Purpose:** close ticket 11 and act on two of its concerns.
**Result:** ticket 11 closed and merged into `main` locally. Measuring the whole backend showed 61
type errors under Pyright, not 3, all in v1's copied code, and 2 in the new module that mypy had
missed. Three options were put to the author, who chose Pyright with a "not yet checked" list.
Ticket 20 renamed `views.py` to `dashboard.py`. Ticket 21 added Pyright, listed 14 copied files as
not yet checked, and fixed the new module. Pyright: 0 errors; a deliberate error fails it. Full
suite: 267 passed.
**Next:** the author reviews tickets 20 and 21; then ticket 12, the API foundation.

### P-005 · 2026-10-14 · Ticket 12 API foundation and the Overview endpoint

**Prompt:**
> /mp-implement 12

then, before approving the test points, a question on one of them:

> explain to me this pls "For seam 2, the test counts calls to the core's open_memory and build_agent while sending several requests. This is the one place a test watches a collaborator, because "exactly once" is the requirement itself."

then "yes go ahead".

**Purpose:** build the frontier ticket. The agent proposed a branch and two seams to test at (the
HTTP API, and startup seen from outside); the author asked why one test watches the core's
functions before approving.
**Result:** a new `backend/api/` package with settings, startup, the one error shape, the shared
filters and three endpoints, built test-first in six slices. FastAPI's default 422 was shown to copy
a hostile value back to the client before the custom handler replaced it. The two-axis review found
two real bugs, both fixed test-first: a number sent as a date gave a confident empty view (B-002),
and a missing log file sent the server's full path to the client (B-003). 26 API tests; full suite
293 passed; Pyright clean; the core unchanged.
**Next:** the author reviews the branch and rules on the open points in ticket 12's comments.

### P-006 · 2026-10-14 · Ticket 12 API foundation and the Overview endpoint

**Prompt:**
> ok lets go through the 4 points 1 at a time, be simple for me to understand pls

**Purpose:** rule on the four open points of ticket 12, each explained in plain words with the
options, one question at a time.
**Result:** all four recommendations chosen. The three extra error codes and the missing-file text
were written into the contract. An empty filter box now means "all" for every filter, built
test-first. The agent's tools ignoring the log and reputation settings became ticket 22, which now
blocks ticket 18. Each ruling has a row in the spec's decisions log. Full suite: 294 passed.
**Next:** the author reviews ticket 12 for approval.

### P-007 · 2026-10-14 · Ticket 13 Frontend shell and the Overview screen

**Prompt:**
> /mp-implement 13

then, asked to rule on the chart component's raw HTML, the author stopped the question to ask:

> what is the impact of ur recommendation for this one ?

then "ok i agree with ur recommendation then".

**Purpose:** build the frontier ticket. The agent proposed five test points (failed share, singular
or plural counts, the filters in the address, the Overview drawn with a fake API reply, and a scan
for raw HTML) and the author chose all five. Before ruling on the chart conflict, the author asked
what the recommended option would change.
**Result:** a new `frontend/` Vite app: React Router with four routes, the dashboard-01 shell,
KPI cards and chart component, the filter toolbar with its state in the address, one empty state,
fixed error text. The scan test caught the official chart component using raw HTML (B-004); the
author chose a one-line change over an exception. The two-axis review found a date label printing
"undefined" (B-005) and a filter value the analyst could not see (B-006), both fixed test-first. 36
frontend tests; backend 294 passed; Pyright and the frontend type check clean. A real run proved the
proxy path from the browser address to FastAPI.
**Next:** the author reviews the branch and rules on the open points in ticket 13's comments.

### P-008 · 2026-10-14 · Ticket 13 Frontend shell and the Overview screen

**Prompt:**
> HERE "I didn't look at the screen in a browser, because of your no-screenshots ruling" u can take screenshots to analyse and verify no problem, that rule just meant for not keeping screenshots as evidences
>
> pls run the open rulling one at a time

then, while ruling 2 was being asked:

> can u apply ur recommendation now? i guess there is no need to a new ticket. what do u think ?

**Purpose:** correct the agent's reading of the screenshots ruling, look at the running screen,
and rule on ticket 13's five open points one question at a time.
**Result:** the look found the top IPs chart hiding every second label, the top IP included
(B-007), and the date picker marking the reader's date as today; both fixed and looked at again.
Rulings: (1) the log-field rule reworded to "plain text in tables, chart labels and picker
options"; (2) reading the loader showed the API quoting raw log values into its `log_invalid`
message (B-008); the agent agreed no new ticket was needed, since only the API changes, and fixed
it test-first; (3) four unasked behaviours kept; (4) the prototype accepted as the label reference,
against the recommendation to check v1's code; (5) six unused fields trimmed from the replies.
Backend 295 passed, frontend 36, both type checks clean.
**Next:** the author reviews ticket 13 for approval.

### P-009 · 2026-10-15 · Ticket 14 Alerts, end to end

**Prompt:**
> good morning
> /mp-implement  14

**Purpose:** build the frontier ticket: the alerts endpoint and the Alerts screen.
**Result:** before any test, the author agreed five test points and ruled severity out of the
ticket, since v1's alerts carry none. `GET /api/alerts` sends the core's findings unchanged. The
screen has v1's seven columns on the tasks example's table, the counts line, the side panel with
evidence, "Open in Log explorer" and "Investigate", and "How these rules work". TanStack Table was
pinned to version 8, the version the official example uses. A look at the running screen confirmed
the table, the panel and the guide. The two-axis review found a selection that outlived a filter
change (B-009), fixed test-first, and v1's "Select an alert" hint missing, restored. Backend 304
passed, frontend 57, both type checks clean.
**Next:** the author rules on the open points in ticket 14's comments, then reviews for approval.

### P-010 · 2026-10-15 · Ticket 14 Alerts, end to end

**Prompt:**
> lets me see the live alerts page first before i answer the 3 open point

then, on the pager question:

> why u recommend that? what will happen when have 1000s of alerts ?

then, with a screenshot of the agreed prototype:

> u know what i hopped? i hoped the alerts page layout look exactly like the prototype. the alert details page is set. not sliding from the side. i hopped it will be there by default populated with the alert details when the user clicks the alert in the main alerts table. then i asked myself how that alerts details blocks would look when the whole page loads for the first time. then i thought maybe the most recent alert details by default populate it

and

> yes and before go. pls make the the populate of the alert's details side block with the details of the alert smooth. like a bit of progesional animation.

**Purpose:** look at the live screen before ruling, test the reasoning behind a recommendation,
and bring the screen in line with the prototype the author had in mind.
**Result:** three rulings: severity is checked on the report card; the Alerts table reuses ticket
15's pager; the glossary gains Finding. The author's question about thousands of alerts changed the
agent's recommendation from "leave the pager out" to "reuse ticket 15's": a pager fixes the drawing,
while the reply's size needs server paging, which stays out of scope. After seeing the screen, the
author replaced the sliding panel with a fixed details panel showing the newest alert by default,
with a short entry animation. Built test-first: five screen tests changed before the code. Looked at
in the browser. Frontend 58 passed, type check clean.
**Next:** the author looks at the new panel, then reviews ticket 14 for approval.

### P-011 · 2026-10-16 · Ticket 15 Log explorer, end to end

**Prompts, in order:**
> hello codex [$implement](<local implement skill>) 15

The local skill path above is redacted to avoid recording a personal filesystem path.

> tell me what is T15 is about pls first

> do u have access to the design of the layout ?

> OK u can start

Asked whether to correct the Explorer contract to list its five count fields, the author answered:

> Yes, list the five Explorer counts (Recommended)

**Purpose:** implement ticket 15 using the agreed layout, first explaining its scope and confirming
access to the design reference.
**Result:** implemented. The Explorer and CSV routes share one filtered core search;
IP validation runs at both boundaries. The screen has five supporting tiles, a paged log table and
CSV download. Alerts reuses the pager and its quiet surface is shared with the count tiles. The
contract correction was approved before being recorded. Tests caught and fixed the Reset iteration
in B-011.
**Validation:** backend 323 passed, frontend 90 passed, both type checks clean, production build passed. Standards review found one small pager-label duplication, fixed; Spec review found no gaps. Lint and bundle-size warnings are recorded in ticket 15.
**Next:** the author reviews the live screen before ticket 15 is resolved. Nothing pushed.


### P-012 · 2026-10-16 · Ticket 15 visual approval

**Prompt:**
> the layout is very good

**Purpose:** the author's review of the live Explorer layout, the remaining acceptance check.
**Result:** visual approval recorded in ticket 15. Ticket resolved and the map updated. No
application code changed. The passing automated checks from P-011 remain the evidence.
**Next:** ticket 16, Investigations API, when the author gives the go. Nothing pushed.

### P-013 · 2026-10-16 · Ticket 16 Investigations API

**Prompts, in order:**
> what is T16 is about?

> ok Go

> [$implement](<local implement skill>) 16

The local skill path above is redacted to avoid recording a personal filesystem path.

**Purpose:** explain ticket 16, then implement its server endpoints using the implement skill,
with test-first work at the agreed HTTP seam, code review and a local commit.
**Result:** Investigation list, create, reopen, streamed ask, report and PDF endpoints built.
History is kept in the configured SQLite file. A saved-history core reader lets PDF downloads
work without a model. Per-Investigation writer reservations prevent overlapping asks and reports.
Validation and failures return fixed messages. No UI, spec changes or pushes.
**Iterations:** B-012 records the sample-size and disconnect-test corrections. The sandbox blocked
uv's default cache; checks use a temporary cache directory instead.
**Validation:** backend 343 passed; frontend 90 passed; both type checks clean; production build
passed. Standards and Spec reviewers confirmed the fixes. B-013 and B-015 record the validation
and lifetime fixes; B-014 records the FastAPI disconnect limitation. Existing frontend warnings
remain. Work committed locally; nothing pushed.
**Next:** ticket 16 is ready for the author's review. Ticket 17 follows approval.

### P-014 · 2026-10-16 · T16 approval and targeted disconnect follow-up

**Prompts, in order:**
> "FastAPI can log an internal error after a slow-reader disconnect. Cleanup still passes. Existing frontend warnings remain." should we fix that for completnes ? or maybe it has some kind of impact ?

> T16 is reviewed and approved.
> u can go with Investigating a targeted disconnect fix first. Keep frontend cleanup as separate work

**Purpose:** assess the warnings' impact, record the author's T16 approval and investigate a
narrow B-014 fix before building the Investigator screen. Frontend cleanup remains separate.
**Result:** T16 resolved and the map updated. Ticket 23 records upstream research and the fix.
No released fix was identified in the latest listed patch notes. A guard on the ask route handles
only known FastAPI keepalive queue closure after confirmed disconnection from a successful SSE
response. It leaves unknown failures visible, including unexpected exception-group siblings.
**Iterations:** strengthening the real disconnect test reproduced B-014 before implementation;
afterward it requires clean completion and no error log instead of accepting the exception.
**Validation:** full backend suite 351 passed, Pyright clean. Both independent review axes found
no issues. Strict disconnect cases pass without accepted exceptions or error logs; eight guard
refusal cases preserve genuine failures. Frontend unchanged. Committed locally; nothing pushed.
**Next:** finish evidence for ticket 23, then return to the T17 frontier after review.


### P-015 · 2026-10-16 · Ticket 23 approval

**Prompt:**
> ok T23 is approved

**Purpose:** record the author's approval of the targeted disconnect fix.
**Result:** ticket 23 marked resolved and the wayfinder map updated. No application code changed.
**Validation:** documentation diff checked; the existing 351 passing backend tests, clean Pyright
and independent reviews remain the evidence. No test rerun needed for this status-only update.
**Next:** ticket 17, Investigator screen, when the author gives the go. Nothing pushed.

### P-016 · 2026-10-16 · Ticket 17 Investigator screen

**Prompt:**
> [$implement](<local implement skill>) T17

The local skill path above is redacted to avoid recording a personal filesystem path.

**Purpose:** implement the agreed Investigator screen using test-first slices at T17's frontend
seams, independent Standards and Spec reviews, and local commits.
**Result:** the Investigator route now has saved Investigation selection, paged history,
prepared questions, create-then-ask streaming, progress words, locked input, saved-history redraw,
plain tool evidence with optional raw JSON, report offers, fixed-field reports and numbered PDF
links. Official shadcn message components were fetched from its registry. `react-markdown` is
used in one allowlist component, with visible non-clickable link addresses and no images or HTML.
**Iterations:** B-016 records fixture corrections, B-017 existing dependency advisories, and B-018
the derived-state correction. The core, API contract and frozen v1 are unchanged.
**Review:** Standards flagged the initially missing prompt record and repeated lifecycle cleanup.
Both were corrected. Both reviewers identified the browser-navigation race, now logged as B-019
and fixed with answer/report regressions. Standards and Spec re-reviews are clear.
**Validation:** backend 351 passed and Pyright clean. Final frontend suite 103 passed; TypeScript
clean; production build passed. Lint reports only six existing warnings. The large bundle warning
and seven existing dependency advisories remain separate work. No existing dependency versions
changed. `git diff --check` clean.
**Preview:** the older local API lacked the Investigation routes. A fresh isolated preview at
http://127.0.0.1:5174/investigator serves the screen and fixed missing-key response. Live agent
review needs `OPENROUTER_API_KEY` configured in `.env`. B-020 records the stale-preview iteration.
**Next:** T17 is ready for the author's live screen and visual hierarchy review before resolution.
Work committed locally. Nothing pushed.

### P-017 · 2026-10-16 · Key setup verification and basic live frontend smoke

**Prompt:**
> done.
> pls check without openning the .env file.
> then do basic agent fronend test. as i guess comprehensive test will be executed later anyways

**Purpose:** verify configuration through application behaviour without opening `.env`, then
exercise the frontend with one live question. Keep comprehensive evaluations for T18 and final
acceptance for T19.
**Result:** `.env` was not opened, printed or edited. `git check-ignore backend/.env` confirms it
is ignored. Restarted the isolated preview API on 8002. Through Vite on 5174, the Investigation
list changed from the known missing-key 503 to a valid 200 response. The live model accepted the
configuration and answered one question about sign-ins from the synthetic attack IP.
**Validation:** the real React Investigator screen ran in Vitest's DOM environment with real
HTTP through the Vite proxy and real agent/model responses. Verified input locking, an answer,
a report offer, tool evidence tables, New investigation, and reopening with identical saved
answer/evidence. No browser automation or screenshot was used. The first run's single-tool
assumption failed after the live answer succeeded; B-022 records the correction. The corrected
smoke passed using the saved answer, with no second live question. B-021 records interruption
noise when stopping the old preview. No application code changed.
**Scope:** no report generation, PDF download or reputation-service request was made. The
OpenRouter configuration is proven by the live response; the AbuseIPDB key has not been checked.
The temporary smoke file was moved out of the normal suite after testing so routine tests never
make paid calls. The smoke Investigation remains in temporary preview memory for author review.
**Next:** author reviews T17's live layout at http://127.0.0.1:5174/investigator. T17 remains
ready-for-human. No comprehensive evaluation or visual approval is claimed. Nothing pushed.

### P-018 · 2026-10-16 · Restore the approved Investigator layout

**Prompt:**
> "Concerns/gaps: Visual layout" exactly! :)
>
> [https://claude.ai/artifact/XLhRJSY2pXJ4Jz94DJzpff](https://claude.ai/artifact/XLhRJSY2pXJ4Jz94DJzpff)
>
> check the approved layout for the investigator screen (Second Column (Recommended))

The prompt included a screenshot of the approved Investigator prototype.

**Purpose:** compare the implemented screen with the approved ticket 07 layout and correct the
mismatch within T17.
**Result:** compared the supplied screenshot and the saved `07-screens-prototype.html`. The
artifact URL was inaccessible through the web tool; its identical saved source was available.
History is now the left in-page column. The chat to its right uses the official message, bubble
and message-scroller components; the outer chat card and repeated question heading are removed.
The input and Send button share one compact composer. Tool evidence and report cards use compact
spacing, with labelled severity and its accent retained. Existing behaviour and safe rendering
remain unchanged. B-023 records the mismatch and provider integration iteration.
**Validation:** focused screen/renderer tests passed. Full frontend suite: 103 passed; TypeScript
clean; lint retains only the six existing warnings. Production build and final review evidence
are recorded in T17 after completion. No model call, `.env` access or backend change was needed.
**Next:** review the corrected preview at http://127.0.0.1:5174/investigator. The author still owns
visual acceptance. Nothing pushed.

**Final evidence for P-018:** 103 frontend tests passed; TypeScript clean; lint has only the six
existing warnings; production build passed with the existing bundle warning. Standards and Spec
reviews are clear. Spec review explicitly checked the saved approved prototype this time. The
preview serves the corrected route and all new chat modules with 200 responses. No additional
model request was made. Correction committed locally as `f016aa4`. Visual acceptance remains
with the author.

### P-019 · 2026-10-16 · First review comment: new Investigation Send

**Prompts, in order:**
> first of all i cannot really start a new chat with the agent. is that expected ?

> i can write to the prompt field, send button switch to be active. but when i click nothing happens,. the prompt does not even move to the chat

> [http://127.0.0.1:5173/investigator](http://127.0.0.1:5173/investigator)

**Purpose:** handle this first review comment on its own. Diagnose and restore manually typing
and sending a new Investigation. Do not open `.env`.
**Result:** reproduced the preview mismatch through HTTP: port 5173's Investigation API returned
404, while 5174 worked. The user confirmed using 5173. Restarted only this workspace's Vite process
on 5173, pointing it at the current API on 8002. No application-code change was required.
**Validation:** component screen suite runs under the real app's StrictMode, with an added typed
question regression. The full React app with real HTTP and a short live model request passed
through 5174 before the fix, then passed at the user's repaired 5173 address. Verified immediate
question display, input locking, saved answer, report offer and unlock. Live checks use the DOM
test environment, not a browser or visual assertion. No `.env` read, screenshot or comprehensive
evaluation. Temporary paid-call tests were removed from the normal suite.
**Next:** author refreshes the original port 5173 page, then provides the next review comment.
B-024 records the cause and fix. T17 remains ready-for-human. Nothing pushed.

### P-020 · 2026-10-16 · Tool count and automatic report reveal

**Prompt:**
> Ok it works now, but two issues about the agent responses:
> 1- the count of the tools user for the query is not stated.
> 2- when i trigger "Write the incident report" the report is generated but i have to scroll downto see it, or click the middle scrolling arrow. it should scoll all the way to the end of the report to be fully visible automatically.

The prompt included a screenshot of the answer and its unnumbered Tools used toggle.

**Purpose:** record that the preview connection now works, then handle the two requested T17
response-display corrections.
**Result:** Tools used now includes its call count. A new saved report explicitly invokes the
existing scroller's public scroll-to-end action, including when the reader had scrolled upward.
Later manual scrolling remains possible. No backend, API contract or safe-renderer change.
**Iterations:** B-025 records the count omission. B-026 records the report scroll failure and the
DOM geometry correction needed to reproduce it. Test-first work stays at the agreed screen seam.
**Validation so far:** thirteen focused screen tests pass, TypeScript is clean, and lint retains
only the six existing warnings. Full frontend checks and review evidence are recorded in T17.
**Next:** author checks the count and automatic report reveal on the port 5173 preview. T17
remains ready-for-human. No `.env` access, paid model call or push for these corrections.

**Final evidence for P-020:** all 105 frontend tests pass, TypeScript is clean, lint retains the
six existing warnings and the production build passes with its existing bundle warning. Standards
and Spec reviews are clear. The correction is committed locally as `a75d1a6`. The author checks
actual browser scrolling next. Nothing pushed.

### P-021 · 2026-10-16 · Speaker distinction and researched empty chat layout

**Prompt:**
> ok thanks.
> few more comments about the chat part:
> 1- The user prompt and agent response should be distingueshed visually. give the user prompt query inside the chat window diff background color. for example a lighter version of the pinkesh color with are using in different parts of the app.
> 2- the note of the agent role and the pre-set prompts are sitting ourside the chat window. i guess there is a better layout. pls research the best practive and apply it.

The prompt included a screenshot of the scope note, starter chips and composer outside the empty
message viewport. This records the final message after the author's interrupted draft.

**Purpose:** research first-party chat/empty-state guidance, then improve the existing T17 screen
with pink user messages and better-integrated role guidance and starter questions.
**Research:** the research skill delegated a primary-source investigation. Findings and links
are saved at `.scratch/v2-port/research/17-chat-empty-state.md`: Carbon empty states and Carbon AI
Chat home-screen guidance, plus WCAG colour/contrast guidance. The chosen layout is a project
application of that guidance, not a claimed universal rule.
**Result:** user bubbles use dedicated soft rose colours for both themes, with visible speaker
labels and existing alignment. One welcome region now sits inside the stable-height empty chat
viewport with the original scope text and three wrapping starter cards. Selecting a starter still
only fills the input. The welcome disappears on Send; the composer and AI caution stay below.
**Iterations:** B-027 records the neutral-primary tint issue. B-028 records the outside-viewport
empty state and its failing-then-passing screen regression. No backend, model prompt, API contract,
answer renderer or `.env` change. No extra paid model calls.
**Validation so far:** fourteen focused screen tests pass, TypeScript is clean and lint has only
the six existing warnings. Calculated palette contrast exceeds 4.5:1 in both themes. Full frontend
and review evidence follows in T17. The author still owns visual acceptance.
**Next:** review the updated chat at http://127.0.0.1:5173/investigator. Nothing pushed.

**Final evidence for P-021:** all 106 frontend tests pass, TypeScript is clean, lint retains the
six existing warnings and production build passes with its existing bundle warning. Standards
and Spec reviews are clear, including class precedence and empty/active scrolling transitions.
Changes committed locally as `db4df51`. The author reviews the appearance next. Nothing pushed.

### P-022 · 2026-10-16 · Duplicate initial user question

**Prompt:**
> way better thanks codex.
> one comment through, one i start new chat through the pre-set 3 questions or even by typing in the prompt field. the intial query in the chat is dupicated. the duplications disappears later but still. not good for UX

The prompt included a screenshot with the same initial question in two user bubbles.

**Purpose:** reproduce and fix the temporary duplicate for both typed and preset questions.
**Result:** creating the record changes its URL, which triggered a saved-history read during the
first stream. The saved human question and live draft were both displayed. The ID-loading effect
now skips this read while that Investigation belongs to the active operation. The existing terminal
refresh hands over to saved history. No text-based filtering, API or agent change was needed.
**Iterations:** B-029 records the race, regression correction for a remounted viewport and fix.
**Validation so far:** both regressions failed with two bubbles before the fix and pass afterward.
All seventeen focused screen tests pass; TypeScript is clean and lint retains only six existing
warnings. Full frontend validation and review evidence follows in T17. No `.env` access or paid
model call was needed.
**Next:** author checks a new typed or starter question on port 5173. T17 remains ready-for-human.
Nothing pushed.

**Handover safeguard for P-022:** a further failing test reproduced a stuck loading state when
final history reload failed after skipping the initial read. The create reply now seeds the
known empty record, and a retained draft prevents the welcome from appearing over it. The test
passes with the question/answer visible once, the fixed error message and an unlocked input.

**Final evidence for P-022:** all 109 frontend tests pass; TypeScript is clean; lint retains the
six existing warnings; production build passes with its existing bundle warning. Standards and
Spec reviews are clear. Fix committed locally as `a829f31`. The author confirms the browser
behaviour next. Nothing pushed.

### P-023 · 2026-10-16 · Centre the Send button

**Prompt:**
> perfect thanks codes.
> now the last minor change we need. the send button is not vertically centered in the chat prompt. pls fix that

The prompt included a screenshot showing Send near the bottom edge of the composer.

**Purpose:** correct vertical alignment as a small, reversible presentation change.
**Result:** composer alignment changed from `items-end` to `items-center`. No behaviour or
security change. B-030 records the cause and fix. No new tests or broad rerun for a CSS alignment
change; TypeScript and diff checks provide the routine verification. Visual confirmation remains
with the author on port 5173. Nothing pushed.

### P-024 · 2026-10-16 · Requested progressive report delivery

**Prompt:**
> great thanks. i am sorry one last thing when the report is generated in just appears suddeny. would pls make it stream on the same pace as when the agent typically response to the user prompt. why it would better? it is good for the user experience. by the end of the day the report itself is an agent response

**Purpose:** make report delivery feel progressive rather than sudden.
**Inspection:** the agreed report endpoint currently returns one completed structured report.
The core invokes a structured-output chain and saves its validated result before replying. The
report card renders that saved result as fixed plain-text fields. The API contract explicitly
says reports are not streamed. Installed LangChain parsers and official reference docs were
checked to distinguish full validated output from partial structured drafts.
**Choice presented:** gradual reveal of the completed report, keeping the initial generation
wait, or genuine live structured-report streaming with an API/core flow change. Gradual reveal
was recommended for the requested UX refinement. At this inspection the author's choice was pending; no application,
API or spec change had been made yet.


**Author's choice, verbatim:**
> ok i agree with ur recommendation. however when need to keep that reveal as similar to the pace of the streaming of the agent typicall responses as possible. pls confirm first if u understand and agree with me before u take any actions.

**Author's go:**
> Go

**Decision:** confirmed understanding before making changes. The author approved gradual reveal
of a completed validated report, with a pace close to normal streamed answers. This is recorded
in the spec's frontend section and decisions log. No API/core streaming change.
**Result:** report text reveals in field order. Recent text chunk timing supplies an approximate
characters-per-second rate, excluding initial latency, tools and long pauses. Without a sufficient
sample the default is 200 characters/second; observed rates are bounded to 40–600 to avoid extreme
network bursts or stalls. This timing is local presentation state and is not persisted.
Only the report just generated animates. Past reports open fully; leaving the Investigation or
starting another action ends the visual reveal. "Show full report" skips it, and reduced-motion
preference disables it. Severity and the validated report's PDF link remain available. Saved
report data is never clipped or changed. Reveal remains plain text and respects report scrolling.
**Iterations:** B-031 records implementation/type/lint corrections and updated full-field checks.
**Validation so far:** twenty-two focused screen/report-card tests pass; TypeScript clean; lint
has only the six existing warnings. The clock-controlled screen test verifies measured pace,
older-report visibility and immediate display on reopening. Component checks cover progressive
fields, skip, reduced motion, hostile text, empty lists and cancellation on unmount.
**Next:** full frontend checks and independent reviews, then the author's pace/appearance review
at http://127.0.0.1:5173/investigator. No `.env` access, backend change, paid model call or push.


**Final evidence for P-024:** all 114 frontend tests pass across 11 files. TypeScript is clean.
Lint retains the six existing warnings; production build passes with its existing bundle warning.
Standards review: clear. Spec review: clear. Both reviewed `22e9113...3ba596c` independently.
Implementation committed locally as `3ba596c`; diff checks clean. Nothing pushed.
**Next:** the author refreshes port 5173 and generates a report to judge actual pacing and feel.
The initial generation wait remains. T17 stays ready-for-human until author acceptance.


### P-025 · 2026-10-16 · Accept the Investigator screen

**Prompt:**
> it is perfect. thanks codex :)

**Purpose:** confirm acceptance after the iterative live screen review, including gradual report reveal.
**Result:** marked T17 resolved and its visual-hierarchy checkbox complete. Updated the map to
record the dated author acceptance and move the build frontier to T18. No application edits,
new model calls or test rerun for this documentation update. T18 is not started; comprehensive
evaluations and final acceptance remain with T18 and T19 respectively. Nothing pushed.


### P-026 · 2026-10-16 · Context Hub for Codex

**Initial prompt:**
> ok install chub locally for this project environment. and install the skill for u and claude globally pls

**Verification prompt:**
> yes verify first pls

**Final scope, verbatim:**
> ok install the MCP, and the skill just for codex. claude will handle his part

**Purpose:** give Codex access to Context Hub documentation through MCP and a global companion skill.
**Result:** installed `@aisuite/chub` 0.1.4 under `tools/context-hub` with a lockfile, separate
from the application dependencies. Registered the project-local MCP entry point as `chub` in
Codex's user configuration. Installed the upstream `get-api-docs` skill globally for Codex
and adapted it to prefer MCP, use the local CLI as fallback, and respect specialized
official-documentation skills. Telemetry and external feedback are disabled.
Claude setup remains with the author. No application or spec changes.
**Evidence:** the published npm archive includes the MCP implementation, correcting the
initial README-only answer that no official server was documented. A live MCP client
connected, discovered five tools, searched public documentation (15 matches), and fetched
`openai/chat` (11,688 characters). The global skill passed the validator with the project's
Python environment after system Python lacked PyYAML. Codex reports the server enabled.
**Next:** reload Codex to expose the tools in a new session. Build frontier remains T18.
Nothing pushed.


### P-027 · 2026-10-16 · Share Context Hub across projects

**Prompt:**
> do it

**Purpose:** accept the recommendation to move Context Hub to a global installation
and update Codex's MCP registration once for all projects.
**Result:** installed `@aisuite/chub@0.1.4` globally through npm, updated Codex's
user MCP registration to the global entry point, and revised the global companion
skill to use the shared CLI fallback. Telemetry and external feedback stay disabled.
Removed the superseded project-local package and replaced its setup notes with
`docs/context-hub.md`. Claude setup remains separately managed.
**Evidence:** a live client launched the global server from a temporary directory
outside the project, discovered all five tools, searched documentation (15 matches),
and fetched `openai/chat` (11,688 characters). Skill validation passed and Codex's
registration points to the global package. No application changes or push.
**Next:** reload Codex. No per-project installation is needed. A future Node.js
version change may require reinstalling the global package and updating registration.


### P-028 · 2026-10-17 · Ticket 22: the agent's tools follow the settings

**Prompts, verbatim:**
> /mp-implement T22

> i lean toward option A as well, but this ticket is very critical so i want to do a lil research for tyhe best practice first pls

**Purpose:** close the gap where the agent's tools read the default log and reputation folder
while the dashboards follow the settings, with the design chosen on researched evidence.
**Result:** a background research agent compared five designs against the official LangChain,
LangGraph and FastAPI docs and the installed library code (`research/22-tool-data-injection.md`).
The author chose design A with guards, ruled that a failed log makes the log tools refuse, and
approved five test points. Built test-first in four slices on branch
`ticket-22-tools-follow-settings`. A two-axis review followed; the author chose to apply all six
recommended fixes. Bugs B-033, B-034 and B-035.
**Evidence:** 356 backend tests pass; Pyright 0 errors; the eval prompt fingerprint is
`35d4d98f` before and after, so the model sees the same tools.
**Next:** the author reviews ticket 22. Ticket 18 follows.
