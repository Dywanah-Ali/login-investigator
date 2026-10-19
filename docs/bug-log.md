# Bug Log

Bugs found while building v2, logged when they are found. Real problems are kept, not cleaned away.
v1's bug log stays in the v1 repository; this log starts again at B-001.

## Entry format

```
### B-001 · 2026-10-14 · Ticket 10 Repository foundation

**Symptom:** what went wrong, as seen.
**Cause:** why it happened.
**Fix:** what changed.
**Lesson:** what to remember next time.
**Found by:** test, eval, manual check, or review. Related prompt: P-00X.
```

## Entries

### B-001 · 2026-10-14 · Ticket 10 Repository foundation

**Symptom:** the spec and ticket 10 expect 259 core and agent tests. The copied tests collect 254.
**Cause:** the planning count, not the copy. `.scratch/v2-port/v1-facts.md` records that v1 collects
290 tests, and that the screen files hold 13 and 18 test functions. 290 minus 31 gives 259. But 290
counts collected tests, and `test_app.py` is parametrised: its 13 functions collect as 18 tests. The
subtraction mixed functions with collected tests. Collected per file, the screen files hold 36 (18
and 18), which leaves 254. Rechecked on a fresh export of v1's last commit: 290 collected, 254 outside
the two screen files.
**Fix:** none to the code. The author approved the correction on 2026-10-14. 259 became 254 in the
spec, tickets 08, 10 and 11 and the map, with a row in the spec's decisions log.
**Lesson:** subtract like from like. A count that becomes an acceptance gate should come from the
tool's own output for exactly the set it describes.
**Found by:** test run of the copied suite, checked against a collect-only run of a scratch copy of
v1. Related prompt: P-001.

### B-002 · 2026-10-14 · Ticket 12 API foundation and the Overview endpoint

**Symptom:** `GET /api/overview?from=1759708800` answered 200 with an empty view, as if nothing had
happened. `from=2026-10-06T00:00:00` was also accepted. The contract allows only `YYYY-MM-DD`.
**Cause:** the `from` and `to` parameters were typed as Python dates, and FastAPI's validator is
lenient. It reads a number as a Unix time (here 6 October 2025) and accepts a date with a time.
**Fix:** the parameters are read as text and checked against exactly `YYYY-MM-DD` before they become
dates (`api/filters.py`, `_date`). Three cases added to the validation test.
**Lesson:** never let broken input become a confident claim. A lenient parser turns a wrong input
into a plausible answer, which is worse than an error. At a trust boundary, check the exact format
the contract names.
**Found by:** the spec review of the first build commit, reproduced through the test client before
the fix. Related prompt: P-005.

### B-003 · 2026-10-14 · Ticket 12 API foundation and the Overview endpoint

**Symptom:** with `LI_LOG_PATH` pointing at a missing file, `GET /api/dataset` answered 500
`log_invalid` with the message `Log file not found: /full/path/to/logins.csv`. On the author's
machine the path holds the account's username.
**Cause:** the contract sends the loader's message to the client. The loader's other messages name
only the file, but its missing-file message holds the full path.
**Fix:** the API sends fixed text, "The configured log file was not found.", when the file is
missing, and logs the loader's message on the server. The loader is unchanged. A test checks the
path does not appear in the reply.
**Lesson:** "the loader's message is safe" was checked for row problems but not for every message.
Data crosses a trust boundary when it leaves the server, so check each message that can cross it.
**Found by:** the spec review of the first build commit, reproduced through the test client before
the fix. Related prompt: P-005.

### B-004 · 2026-10-14 · Ticket 13 Frontend shell and the Overview screen

**Symptom:** the scan test for raw HTML failed on its first run. It named
`src/components/ui/chart.tsx`, the official shadcn chart component the ticket requires.
**Cause:** two rules in the ticket met head on. The official component writes its chart colours
into the page with `dangerouslySetInnerHTML`, and the repository rule forbids it everywhere. The
text it wrote came only from our own colour settings, so nothing was exposed. The rule was still
broken as written.
**Fix:** by the author's ruling (option A of three), `ChartStyle` passes the same CSS as a text
child of the style element. The chart looks the same. A comment in the file marks the change. If
the component is ever reinstalled, the scan test fails at once.
**Lesson:** an "official piece" is not the same as a piece that meets our rules. Scan what a
template brings in before trusting it, and let a test hold an absolute rule.
**Found by:** test (the repository-rules scan, written before the change). Related prompt: P-007.

### B-005 · 2026-10-14 · Ticket 13 Frontend shell and the Overview screen

**Symptom:** with `?from=2026-13-45` in the address, the toolbar's date button read
"45 undefined 2026". The API refused the date with a 422, but the toolbar still showed it as a date.
**Cause:** the toolbar checked only the shape `YYYY-MM-DD`. Month 13 has no name, so the label
printed "undefined", and JavaScript's `new Date` quietly rolled day 45 into the next month.
**Fix:** one `parseDate` in `lib/format.ts` accepts a date only when it reads back unchanged, and
the toolbar's own copy of the date helpers is gone. Anything else shows as the whole log. A screen
test reproduced the label first.
**Lesson:** the same lesson as B-002, on the other side of the boundary. A lenient parser turns a
broken input into a confident-looking answer. Check the value, not just its shape.
**Found by:** the standards review of the first build commit, reproduced by a screen test before
the fix. Related prompt: P-007.

### B-006 · 2026-10-14 · Ticket 13 Frontend shell and the Overview screen

**Symptom:** with `?user=nobody` in the address, the Overview showed the empty state, but the User
box in the toolbar was blank. The analyst could not see which filter emptied the view.
**Cause:** the pickers list only the dataset's values. A value in the address that is not among
them matched no item, so the box drew nothing.
**Fix:** a value the dataset does not hold is added to its own box, so it shows. It still matches
nothing, so the screen keeps its empty state. A screen test reproduced the blank box first.
**Lesson:** the address can say anything, not only what the pickers offer. Every filter that shapes
the view must be visible on it.
**Found by:** both reviews of the first build commit, reproduced by a screen test before the fix.
Related prompt: P-007.

### B-007 · 2026-10-14 · Ticket 13 Frontend shell and the Overview screen

**Symptom:** on the running Overview, the top source IPs chart named only every second bar. The
top IP of all, with 150 failed sign-ins, had no label.
**Cause:** Recharts drops axis labels it judges too crowded, by default. Ten bars in a short chart
were enough to trigger it. The screen tests could not see it, because the test browser draws no
charts.
**Fix:** the IP axis shows every label (`interval={0}` in `top-ips-chart.tsx`). Checked on the
running screen: all ten IPs named. In the same look, the date picker marked the reader's own date
as "today"; it now marks the log's last day, as the contract says.
**Lesson:** a test that reads text cannot judge a picture. A screen is not done until someone has
looked at it running.
**Found by:** manual check in the browser, after the author clarified that screenshots may be used
to look, only never as evidence. Related prompt: P-007.

### B-008 · 2026-10-14 · Ticket 13 Frontend shell and the Overview screen

**Symptom:** a log row whose `source_ip` was `<script>alert(1)</script>` made every dataset
endpoint answer 500 `log_invalid` with the message `bad.csv failed validation with 1 problem(s):
- line 2, column 'source_ip': '<script>alert(1)</script>' is not a valid IP address`.
**Cause:** the API forwarded the loader's message, and the loader quotes each bad row's raw values.
The contract had judged the message safe because it "names row problems, not secrets". That was
true of secrets but not of log fields, which the contract's own ground rules keep out of sentences.
**Fix:** by the author's ruling, the API sends fixed text for every cause (`api/services.py`,
`start`): "The log failed validation. The server log lists the problems." The full message stays in
the server log. The loader is unchanged. A test plants the hostile value and checks it is absent.
The frontend already showed fixed text, so the screen was never affected.
**Lesson:** the second time for this one message (after B-003). "Safe" was checked against one
danger at a time. Check a message that crosses the trust boundary against every rule, including
"log fields are data, never sentences".
**Found by:** reading the loader while preparing ruling 2 of ticket 13's review, then reproduced by
a test before the fix. Related prompt: P-008.

### B-009 · 2026-10-15 · Ticket 14 Alerts, end to end

**Symptom:** with an alert's side panel open, a change of address under it (the browser's Back or
Forward button) reloaded the list for the new filters, but the panel stayed open on the old alert,
which might not be in the new view at all.
**Cause:** the selected alert was kept as page state and nothing cleared it when the filters
changed. v1 had guarded this on purpose by giving its table a key that changed with the list.
**Fix:** a selection now remembers the filters it was made under, and counts only while they still
hold (`pages/alerts.tsx`). A screen test opens the panel, changes the address and checks the panel
has closed; it failed before the fix.
**Lesson:** when a v1 line carries a comment saying why it exists, the reason travels with the port
even when the mechanism does not. Streamlit's widget key was dropped as an artefact; the guard it
gave was not an artefact.
**Found by:** the Spec axis of the two-axis review, which quoted v1's comment. Reproduced by a test
before the fix. Related prompt: P-009.

### B-010 · 2026-10-16 · Ticket 15 Explorer contract summary

**Symptom:** the Explorer contract said its summary was the same as Overview, which now exposes
three fields. The agreed Explorer design needs five count tiles.
**Cause:** ticket 13 narrowed Overview's summary without expanding Explorer's shorthand reference.
**Fix:** the author approved listing Explorer's five fields explicitly in the contract. Overview
keeps its three fields. The API test pins Explorer's exact summary, including the empty view.
**Lesson:** when a contract reuses another endpoint's shape, changing that endpoint can silently
change its dependants. Spell out independently owned response shapes.
**Found by:** reading the contract against the agreed prototype before building ticket 15.
Related prompt: P-011.

### B-011 · 2026-10-16 · Ticket 15 Reset after an invalid IP draft

**Symptom:** submitting a malformed IP hid the results, then Reset left the error visible and the
table hidden. A regression test reproduced it during implementation.
**Cause:** the draft error lived across URL filter changes. Also, Reset only considered applied
filters, so an invalid draft on an otherwise unfiltered page could not enable it.
**Fix:** draft state belongs to a view keyed by its filter query. The shared toolbar accepts a draft
reset callback and treats a changed draft as a reason to enable Reset. Tests cover Reset with and
without applied filters.
**Lesson:** resetting a form must clear both applied filters and unsubmitted input errors.
**Found by:** the Explorer screen test before the fix. Related prompt: P-011.

### B-012 · 2026-10-16 · Ticket 16 test expectations

**Symptom:** the first streamed-answer test expected 50 evidence rows but received 20. Later,
the disconnect test counted all 1,000 model chunks even though HTTP delivery had stopped.
**Cause:** the tests confused the tool's maximum sample size (50) with its default (20), and
model-library buffering with the API advancing the core generator.
**Fix:** pin the default at 20 from the existing core's documented behaviour. Count advancement
of the real core generator, verify it closes after disconnect, and send a follow-up through HTTP
to prove the busy reservation is released. The model and core still run in the test.
**Lesson:** test the boundary the requirement names. A library's internal buffering is a different
boundary from HTTP delivery and core-generator advancement.
**Found by:** the new API tests during implementation. Related prompt: P-013.

### B-013 · 2026-10-16 · Ticket 16 validation messages

**Symptom:** missing or incorrectly typed question fields and invalid report requests returned a
generic validation message instead of identifying the field.
**Cause:** the existing validation handler had no mapping for the new Investigation body fields.
**Fix:** known `question` and `request` field failures get fixed field-specific messages. No input
values or arbitrary client keys are echoed. Invalid report wording uses the core's allowed requests.
**Lesson:** a safe generic error can still miss a usability requirement. Check each new body field.
**Found by:** the Spec review, then reproduced by API tests. Related prompt: P-013.

### B-014 · 2026-10-16 · FastAPI disconnect under backpressure

**Symptom:** a slow-reader disconnect can raise `BrokenResourceError` inside FastAPI's keepalive
task after the HTTP connection is already closed. The existing error handler logs the exception.
**Cause:** FastAPI 0.143.1's SSE delivery queue closes while its keepalive task is sending a buffered event.
**Fix:** no third-party patch or unrelated handler change. The regression test recognises only this
specific post-disconnect exception and still requires core closure, stopped advancement and a
successful follow-up. The limitation remains recorded for dependency maintenance.
**Lesson:** disconnects must also be checked when the delivery queues are full.
**Found by:** the added backpressure case during review. Related prompt: P-013.


**Follow-up, 16 October 2026:** after the author's approval of T16, ticket 23 addresses the
remaining noise. The stricter disconnect test failed with the original framework exception.
A route-specific guard now recognises that exception's framework origin only after an observed
HTTP disconnect and a successful SSE response. Other exceptions continue to propagate. The guard
wraps delivery and request cleanup, so it acts before the application-wide error logger. No
third-party files, dependency versions or global log filters are changed. Remove it once an
upstream fix passes the strict regression without it. Validation evidence lives in ticket 23.

### B-015 · 2026-10-16 · Ticket 16 stream ownership

**Symptom:** review found that core closure could depend on finalization if cancellation landed
while FastAPI was delivering a yielded event, instead of awaiting the next core step.
**Cause:** the core was closed in the endpoint generator's `finally`, but FastAPI's SSE producer
does not explicitly close that generator when cancelled during queue delivery.
**Fix:** a request-scoped dependency owns the core generator. It closes before the writer
reservation is released, regardless of delivery outcome. Fast and backpressured disconnect tests
require closure before the request returns and verify a follow-up is accepted.
**Lesson:** resource ownership belongs to a guaranteed request lifetime, not to eventual cleanup
of a paused generator.
**Found by:** Standards review follow-up and inspection of installed FastAPI. Related prompt: P-013.

### B-016 · 2026-10-16 · Ticket 17 test fixtures

**Symptom:** the first renderer tests failed on list whitespace and on reading the S5 fixture.
The first arrival test mistook a GET with an abort signal for a write. The report test expected
the timeline event without its displayed timestamp.
**Cause:** test expectations did not match the browser test environment or the agreed display.
Vite rewrites module URLs, so a filesystem fixture needs `import.meta.dirname` and a resolved path.
**Fix:** corrected the independent expectations, used a resolved fixture path and checked HTTP
methods explicitly. The tests retain their security and user behaviour assertions.
**Lesson:** assert what the user sees and what crosses the boundary, including normal formatting.
**Found by:** incremental Vitest runs for T17. Related prompt: P-016.

### B-017 · 2026-10-16 · Existing frontend dependency advisories

**Symptom:** installing the T17 markdown renderer reported seven high severity package advisories.
**Cause:** `npm audit --json` traces a braces stack-exhaustion advisory
(GHSA-vfj7-8cjw-p6xm) through micromatch, fast-glob, @shadcn/registry,
@ts-morph/common, ts-morph and shadcn. All seven installed versions match the pre-T17 lockfile.
**Fix:** pending separate dependency maintenance. No automatic audit fix or unrelated version
change was made in T17. The new renderer is not listed in this audit finding.
**Lesson:** package installation can reveal existing dependency risks. Check their origin before
changing versions, especially when the suggested fix crosses major versions.
**Found by:** npm installation and audit during T17. Related prompt: P-016.

### B-018 · 2026-10-16 · Ticket 17 derived screen state

**Symptom:** the first full lint run found two new state-setting-effect warnings in the
Investigator hook.
**Cause:** the hook reset history and copied the prepared question inside effects. This added
extra renders and made it harder to tell which address a result belonged to.
**Fix:** tag history with its Investigation ID and derive loading from that match, as the
existing API hook does. Tag the input with its prepared question and derive its initial text.
The focused screen tests, TypeScript and lint pass with only the six existing warnings.
**Lesson:** tie asynchronous results to their request identity instead of clearing them later.
**Found by:** T17 full validation. Related prompt: P-016.

### B-019 · 2026-10-16 · Ticket 17 navigation during an active operation

**Symptom:** browser history could switch Investigation IDs during an answer or report. The old
operation could then replace the selected history and leave the new screen loading indefinitely.
**Cause:** disabled screen buttons prevented normal selection, but request ownership followed the
component lifetime only. Changing a query parameter does not unmount that component.
**Fix:** bind the active controller to the Investigation ID and cancel it when that ID is left.
Creation transfers ownership to the new ID before changing the address, preserving create-then-ask.
Asks and reports share the same begin/finish lifecycle. Aborted operations cannot redraw history.
**Lesson:** asynchronous work belongs to the selected resource as well as to the screen lifetime.
**Found by:** both independent reviews. The new browser-navigation regression failed before the fix.
Related prompt: P-016.

**B-019 validation iteration:** after extracting shared lifecycle handling, TypeScript correctly
rejected mutation of a ref it had already narrowed to null before the helper call. The helper now
returns the active operation object. Creation transfers ownership through that object directly.
Focused screen tests, TypeScript and lint then passed.

### B-020 · 2026-10-16 · Ticket 17 stale local preview

**Symptom:** the existing frontend served the new screen, but `/api/investigations` returned 404.
**Cause:** the API behind that preview was started before the Investigation routes were built.
Frontend hot reload does not refresh a separately running backend process.
**Fix:** started an isolated API on port 8002 with temporary memory and a Vite preview on 5174.
Existing servers were left alone. The current API returns the expected 503 missing-model-key
response, confirming the route exists and the failure is configuration rather than routing.
**Lesson:** verify both sides of the frontend/API boundary when preparing a review preview.
**Found by:** read-only local preview smoke checks. Related prompt: P-016.

### B-021 · 2026-10-16 · Interrupted preview shutdown

**Symptom:** interrupting the old T17 preview with the terminal stop signal logged
`KeyboardInterrupt` and a lifespan `CancelledError` during shutdown.
**Cause:** the stop interrupted Uvicorn's running event loop and its lifespan receiver. This
occurred during the explicit preview restart, not during an Investigation request.
**Fix:** no application change. The preview restarted successfully on the same port and completed
its live request. A separate shutdown investigation is warranted only if normal shutdown also
fails or leaves resources behind; neither was established by this interrupted stop.
**Lesson:** distinguish forced process interruption noise from failures in serving requests.
**Found by:** the requested T17 configuration check and basic live smoke. Related prompt: P-017.

### B-022 · 2026-10-16 · Live smoke tool-count assumption

**Symptom:** the temporary live frontend test stopped on multiple elements labelled "Asked".
**Cause:** the test assumed exactly one tool call. The agent correctly used two calls to examine
successful and failed sign-ins separately. The live answer and saved-history redraw had passed.
**Fix:** accept one or more evidence entries. Reused the saved Investigation to finish the tool
panel and reopening checks, without another model request. The corrected smoke passed.
**Lesson:** agent smoke tests should check observable capabilities without fixing the tool count.
**Found by:** the basic live frontend smoke. Related prompt: P-017.

### B-023 · 2026-10-16 · T17 differed from the approved Investigator layout

**Symptom:** the author compared the built Investigator with the approved ticket 07 prototype.
History was on the right, the question and answer occupied full-width rows, the composer was a
large stacked form, and the whole chat was enclosed in a card. The approved design places history
on the left inside the page, compact chat bubbles to its right, and Send beside the question.
**Cause:** implementation and review checked the textual "second column" requirement without
checking its placement in the approved prototype. Only the message components were used, omitting
the bubble and message-scroller components named in ticket 07.
**Fix:** restored the 240-pixel left history column, compact selected history entries, right-side
chat, speaker-aligned bubbles, inline composer and AI note below it. Added the official bubble
and message-scroller components, with the required provider, automatic scrolling and a scroll-to-end
control. Tool panels and report cards now use compact spacing. Behaviour, safe rendering and the
API contract remain unchanged.
**Iteration:** the first focused run caught a missing MessageScroller provider. Added its provider
keyed by Investigation ID and stable message IDs; all focused screen/renderer tests then passed.
**Lesson:** a visual approval includes placement and proportions. Compare the saved prototype
alongside the written spec before claiming a screen is ready for review.
**Found by:** the author's screenshot and approved artifact link. Related prompt: P-018.

### B-024 · 2026-10-16 · Send appeared inactive on the original preview address

**Symptom:** the author could type a new question and enable Send on port 5173, but clicking did
not start an Investigation. The author confirmed the address was `/investigator` on port 5173.
**Cause:** the old Vite process on 5173 still proxied to an API without the Investigation routes.
A read-only check returned 404 `not_found` on 5173 and a valid list on 5174. The newer preview was
working, but supplying a second address had left the original author-facing address broken.
This is the same preview-version issue observed in B-020, now confirmed on the author's path.
**Fix:** verified the 5173 process belonged to this workspace, stopped only that Vite process,
and restarted it with `LI_API_URL=http://127.0.0.1:8002`. Both previews now use the current API.
No application or secret-file change. Added a permanent component regression for manually typing
into a new Investigation; this screen suite now runs under StrictMode like the real app.
**Validation:** typed-question component regression passed before any application change. A live
full React screen smoke passed through 5174, then passed through repaired 5173: question displayed,
input locked, live answer saved, report offer appeared and input unlocked. Each live smoke used
one short question. Temporary live tests were removed from the normal suite afterward.
**Lesson:** repair and verify the address the author is actually using. A second working preview
is not a fix for the first one.
**Found by:** the author's first T17 review comment. Related prompt: P-019.

### B-025 · 2026-10-16 · Missing tool-call count

**Symptom:** the author saw "Tools used" without the number of calls for that answer.
**Cause:** the collapsible trigger omitted the length of the answer's ToolView list, although the
approved prototype includes a count.
**Fix:** the trigger now says `Tools used (N)`. It counts calls, including repeated calls to the
same tool, rather than distinct tool names. The existing no-tools behaviour is unchanged.
**Validation:** the one-call evidence test and new repeated-call test failed before the fix and
passed afterward. Counts come from saved history, so they also appear when reopening an Investigation.
**Lesson:** evidence summaries should expose the amount of work behind the answer before opening
its details.
**Found by:** the author's next T17 review comments and screenshot. Related prompt: P-020.

### B-026 · 2026-10-16 · New report did not scroll to its end

**Symptom:** generating a report could leave the viewport at an earlier answer. The author had
to scroll down or use the central scroll-to-end arrow to see the report.
**Cause:** the scroller's automatic following respects manual scrolling. Report completion did
not explicitly request the end of the content, so a reader who had left the bottom could miss it.
**Fix:** a component inside the existing scroller provider observes the number of saved reports.
When it increases, it calls the scroller's public `scrollToEnd` action. This also restores normal
bottom-following while the new report settles in layout. The observation resets per Investigation.
Later unrelated renders and opening tool evidence do not repeatedly force the reader downward.
**Validation:** the report-flow screen test supplies overflowing DOM geometry, scrolls upward,
then completes the report request. It reproduced a scroll position of 0 before the fix and reaches
1300 afterward for 1600 pixels of content in a 300-pixel viewport. Scrolling up afterward and
opening evidence keeps the reader's chosen position.
**Iteration:** scroll heights alone initially produced a false green because other rectangles
remained zero in the DOM test environment. Supplying matching item and viewport rectangles made
the test reproduce the real overflow and fail before implementation.
**Lesson:** explicit actions should reveal their results. Scroll tests need consistent layout
geometry to distinguish automatic following from deliberate result reveal.
**Found by:** the author's report-generation review. Related prompt: P-020.

### B-027 · 2026-10-16 · User and agent messages looked too similar

**Symptom:** the author could not clearly distinguish the user's prompt from the agent's answer
by its background. Both appeared grey in the dark-theme screenshot.
**Cause:** the user bubble's tinted variant derives its colour from the primary token. Both
primary theme values have zero chroma, so tinting them still produces grey.
**Fix:** user messages now have a dedicated soft rose background and contrasting text for each
theme. Agent messages retain their neutral surface. Visible "You" and "Investigator" labels,
accessible group names and existing right/left alignment also distinguish speakers.
**Validation:** focused screen tests pass. Calculated normal-text contrast using the installed
Tailwind palette and default composited surfaces is about 13.02:1 light and 11.97:1 dark, above
WCAG's 4.5:1 threshold. Browser appearance remains for the author's review.
**Lesson:** a tint cannot add a hue to a neutral token. Message roles need deliberate, readable
surfaces and cues beyond colour alone.
**Found by:** the author's next T17 visual review comments. Related prompt: P-021.

### B-028 · 2026-10-16 · Empty-chat guidance sat outside the chat window

**Symptom:** the role description and preset prompts sat above the input outside the message
viewport. The empty viewport collapsed, so there was no clear place to begin an Investigation.
**Cause:** the guidance was rendered after the scroller instead of within its empty content, and
the empty scroller used automatic height.
**Fix:** a single welcome region inside the stable-height viewport groups a heading, the original
read-only scope description and three wrapping starter cards. It disappears on Send. The composer
and AI note remain directly below. Empty-state scrolling starts at the top; active chat retains
end-following and the explicit report-reveal behaviour.
**Validation:** a new screen regression failed before the change because the scope and starters
were absent from the viewport. It now passes and confirms starter selection only fills the input.
Existing tests still verify the scope disappears after answering and report scrolling is preserved.
**Lesson:** put empty-state guidance where the future content belongs, keeping the input easy to
find. The supporting first-party research is saved in `research/17-chat-empty-state.md` under the
v2-port effort.
**Found by:** the author's request to research and apply a better layout. Related prompt: P-021.

### B-029 · 2026-10-16 · Initial question briefly appeared twice

**Symptom:** starting a new Investigation from a starter question or typed text briefly showed
two user-question bubbles. The duplication disappeared after the answer finished.
**Cause:** create-then-ask updates the URL with the new Investigation ID. The ID-loading effect
then reopened that Investigation while its first ask was streaming. The core may already have
saved the human question, so the screen rendered it from both saved history and the live draft.
The final refresh removed the draft, explaining why the duplicate later disappeared.
**Fix:** the ID-loading effect skips reopening an Investigation already owned by the active
operation. The new Investigation's live draft remains the source during the answer. The existing
finish/error refresh then loads saved history and replaces the draft together. Genuine repeated
questions are not filtered or deduplicated by their text.
**Validation:** typed and starter screen regressions reproduced two bubbles before the fix and
pass afterward, checking one question during streaming and one after the saved-history handover.
Live partial answer rendering is retained. Existing navigation, error, report-scroll and rendering
guards pass in the focused screen suite.
**Iteration:** the initial regression held a viewport node across the provider's ID-keyed remount,
which tested detached DOM. It now waits for the selected Investigation and queries the current
viewport, reproducing the actual duplicate before implementation.
**Lesson:** do not mix a live draft with a checkpoint read of the same unfinished work. Creating
and reopening an Investigation are different lifecycle events, even when both change the address.
**Found by:** the author's T17 screenshot and review. Related prompt: P-022.

**B-029 handover safeguard:** an additional failing regression found that skipping the early read
could leave a newly created record loading if its final history refresh failed. The create reply
now seeds the record's contractually empty history locally. A retained draft also prevents the
welcome screen from reappearing over it. The regression verifies one visible question/answer, a
fixed failure message, no empty-state welcome and an unlocked input after that failure.

### B-030 · 2026-10-16 · Send button sat below the prompt's centre

**Symptom:** the author saw Send aligned toward the bottom of the prompt box.
**Cause:** the composer used `items-end` to align its textarea and shorter button.
**Fix:** changed that alignment to `items-center`. Send is vertically centred beside the input.
**Lesson:** controls of different heights need explicit cross-axis alignment.
**Found by:** the author's final minor T17 review comment and screenshot. Related prompt: P-023.

### B-031 · 2026-10-16 · Gradual report reveal implementation checks

**Symptom:** early checks found a possibly undefined animation rate, a React immutability warning
for the text-budget closure in render, and an existing report-flow assertion expecting all text
immediately. The new reveal tests initially failed against the old instantaneous report card.
**Cause:** the animation frame callback needed a concrete numeric rate. The text-budget closure
was local but opaque to the React checker. The old assertion predated the author's gradual-reveal
choice. A first file-write command also used the wrong working directory and made no source edit.
**Fix:** default the optional rate before creating the frame callback; build the plain-text
preview in a separate pure helper; use the new "Show full report" control before the existing
full-field/PDF assertions. Corrected the file-write path. No checker suppression or API change.
**Validation:** progressive card tests and the measured-pace screen regression failed before
implementation and pass afterward. Text completion preserves the report's fixed fields and PDF
identity. Skip, reduced motion, plain hostile text, empty lists, old reports and unmount cleanup
are covered. Final full-suite and review evidence is recorded in ticket 17.
**Lesson:** keep animation state separate from saved data, and verify timing through user-visible
behaviour while retaining deterministic checks for the complete content.
**Found by:** TDD, TypeScript and lint during P-024's authorised gradual-report reveal.


**B-031 documentation check:** the final evidence append initially used an unavailable `python`
command. It made no edit. Retried with the installed `python3`; documentation and diff checks
completed. This was a local tooling invocation issue, with no application impact.


### B-032 · 2026-10-16 · Skill validator used Python without PyYAML

**Symptom:** the global skill validator stopped with `ModuleNotFoundError: No module named yaml`.
**Cause:** system Python did not have the validator's PyYAML dependency.
**Fix:** ran the same validator with `backend/.venv/bin/python`; it passed. No dependency changes.
**Lesson:** use an existing environment containing a tooling script's dependencies.
**Found by:** Context Hub setup, P-026. A documentation patch also failed its context check
before applying changes; retried with a separate new-file patch and explicit log appends.


### B-033 · 2026-10-17 · The agent's tools ignored the log and reputation settings

**Symptom:** with `LI_LOG_PATH` pointing at a three-row log, the Overview counted 3 sign-ins while
the agent's `search_logins` tool counted 1,856, the default log. Reproduced end to end by the first
ticket-22 test, before any fix.
**Cause:** `tools.py` loaded its own copy of the default log and called the reputation lookup with
its default folder. Only the dashboards followed the settings. Known since the ticket-12 review.
**Fix:** startup hands the loaded frame, findings and reputation folder to the tools through
`tools.use_dataset`; a failed log makes the log tools refuse instead of falling back.
**Lesson:** two readers of one dataset must receive it from one place, or nothing guarantees they
agree.
**Found by:** ticket-12 review; fixed in ticket 22, prompt P-028.

### B-034 · 2026-10-17 · Ticket 22 build: a name collision and a test-order leak

**Symptom 1:** after the first change, 14 copied tool tests failed even when run alone, with
`'function' object has no attribute 'findings'`.
**Cause 1:** the new module variable was named `_given`. `tools.py` already defines a helper
function `_given` further down, which silently replaced the variable when the module loaded.
**Fix 1:** renamed the variable `_loaded`. All 23 copied tool tests pass alone.
**Symptom 2:** run after the new test, 6 copied tool tests still failed: they saw the new test's
three-row log.
**Cause 2:** the dataset handed to the tools outlived the app that handed it over. The research
note predicted this risk of design A.
**Fix 2:** `tools.forget_dataset()` runs when the app shuts down, guarded by its own test.
**Lesson:** module-level state needs a name search before it is added, and a reset tied to the
lifetime of whatever set it.
**Found by:** TDD, ticket 22, prompt P-028.

### B-035 · 2026-10-17 · A failed startup could leave its log with the tools

**Symptom:** none seen yet; found by the spec review. If startup failed after the hand-over, for
example when the memory file could not open, the tools kept that run's log for every later test.
A second slip: an edit removed a space, leaving `memory =investigations.open_memory(...)`.
**Cause:** the hand-over sat before the memory and agent steps. A startup that fails never
reaches shutdown, so `forget_dataset` never ran. The space was lost in an exact-text edit.
**Fix:** the hand-over is now the last step of `start()`, and `services.stop()` undoes it. The
regression test `test_a_startup_that_fails_leaves_nothing_behind` was seen failing (3 rows instead
of 1,856) with the hand-over put back at its old place, then passing. Space restored.
**Lesson:** shared state set during startup goes in last, after every step that can fail.
**Found by:** two-axis review of ticket 22, prompt P-028.

### B-036 · 2026-10-17 · Tests could see the real API keys

**Symptom:** a ticket-22 test removed the AbuseIPDB key, yet after the app started it was set
again, and only the test's network guard stopped a live call. A reproduction test confirmed both
the OpenRouter and the AbuseIPDB key names were set after one app start.
**Cause:** building the model calls `load_dotenv`, which copies `.env` into the process
environment. Every API test builds the model at startup, and the keys then stayed for the rest of
the run.
**Fix, first attempt:** an automatic guard in a new `backend/conftest.py` switched off `.env`
loading and removed both key names before every test.
**Review finding:** apps shared by a whole test module (the dashboard and error tests) start
before a per-test guard. They still built a model with the real OpenRouter key and put both keys
back into the environment between tests. A probe by the spec reviewer showed it, and a new test
failed on it.
**Fix:** the guard now starts when pytest starts, before any fixture or test module, and is undone
when pytest ends. Checked again with fake keys set in the terminal. The copied v1 files are
unchanged.
**Lesson:** a test run must be sealed from real secrets by default, not by each test remembering
to remove them. A guard must start before the earliest thing it guards: in pytest, the widest
fixture scope runs first.
**Found by:** ticket 22's reputation test; fixed in ticket 24, prompt P-029. Numbered B-036
because ticket 22's branch holds B-033 to B-035.

### B-037 · 2026-10-17 · API tool evidence cannot feed the unchanged grader

**Symptom:** ticket 18 requires the unchanged grader to check tool names and exact arguments,
but the reopen endpoint returns only the ToolView presentation fields.
**Cause:** the API contract preserved readable evidence but omitted the original call metadata.
Display strings cannot reliably reconstruct arguments, especially failed calls and date filters.
**Fix:** author approved adding `name` and `args` to ToolView. Recorded in the contract and spec
before the route change. The HTTP evidence test failed without these fields, then passed with
the original call metadata returned. The API runner now feeds those fields to the unchanged grader.
**Lesson:** preserve original evidence when a consumer must verify exact actions. A readable
summary is not a replacement for the source call.
**Found by:** ticket 18 implementation, prompt P-031.

### B-038 · 2026-10-17 · First eval mode label broke the copied rescore test

**Symptom:** the copied rescore test failed because `| test |` became `| direct: test |`.
**Cause:** the first implementation prefixed every summary note with its transport mode.
**Fix:** preserve direct-mode notes exactly; prefix only API notes with `api:`. JSON records carry
an explicit `mode`, and rescore preserves that mode. All 36 unchanged scoring tests plus the
new saved-result security test pass.
**Lesson:** check compatibility through the existing interface before broadening a saved format.
**Found by:** focused tests, ticket 18, prompt P-031.

### B-039 · 2026-10-17 · Eval tests and runner use different HTTP client types

**Symptom:** Pyright reported four errors when the API runner tests passed Starlette's
TestClient to a parameter annotated as `httpx.Client`, even though the HTTP tests passed.
**Cause:** the installed Starlette test client uses HTTPX2. It is no longer a subclass of
HTTPX's Client, but provides the same HTTP operations the runner needs.
**Fix:** a small `HttpClient` protocol describes only post, get and stream. Production uses
HTTPX; HTTP API tests use Starlette's test client. Pyright passes without suppressing errors
or introducing test dependencies into production.
**Lesson:** describe the interface a boundary needs rather than claiming one specific client
implementation when multiple clients supply it.
**Found by:** type checking, ticket 18, prompt P-031.

### B-040 · 2026-10-17 · Eval startup deadline too short on a busy host

**Symptom:** the first full API benchmark stopped before any question with a readiness timeout;
the preceding two-question smoke passed. No score or result file was produced for this attempt.
**Cause:** readiness was capped at 30 seconds while backend tests and type checking were also
running. The host load average was 28.18, and both Python processes were competing for CPU.
Startup imports the model stack and runs the detection rules before accepting requests.
**Fix:** allow a bounded 120 seconds for startup, still fail immediately if the child exits,
and retry the full benchmark after the competing checks finish. The same prompt and grader
remain in use. Full benchmark evidence recorded in ticket 18.
**Lesson:** account for measured startup work and host contention in readiness deadlines; do
not confuse failure to start with an agent answer that failed its checks.
**Found by:** full API benchmark attempt, ticket 18, prompt P-031.

### B-041 · 2026-10-17 · One failed stream in the full API benchmark

**Symptom:** Q02 run 2 in the full 19 x 3 API benchmark failed with
`RuntimeError: The agent stream failed or ended without done.` The other two Q02 runs passed.
The complete benchmark met the gate at 56/57 (98%) overall and 15/15 (100%) security.
**Cause:** not established. This message covers an explicit API stream error or an incomplete
stream. The child server's raw error logs are suppressed to keep provider details and keys
out of eval artifacts, so this run cannot identify the underlying exception. It is not evidence
that the model gave a wrong password-spraying answer.
**Fix/status:** unresolved. The runner correctly counted the entire run as failed; it did not
score an older saved answer or substitute a retry. No application or prompt change made for
this finding. Any follow-up needs safe diagnostics and reproduction.
**Lesson:** report transport failures separately from wrong answers while keeping both in the
overall reliability score. A passing aggregate gate does not mean every request succeeded.
**Evidence:** `backend/evals/results/2026-10-17-185622-35d4d98f.json`, Q02 run 2.
**Found by:** full API benchmark, ticket 18, prompt P-031.

### B-042 · 2026-10-18 · Clean-clone probe used a different loopback address

**Symptom:** the temporary startup verifier kept waiting for the frontend although Vite reported
ready and both servers were running.
**Cause:** the probe used `127.0.0.1`, but Vite's default localhost listener was reached through
`localhost` on this host. The README already gives the correct URL.
**Fix:** probe `http://localhost:5173`, as documented. All four frontend routes returned the app
shell; dataset, Overview, Alerts and Explorer replies matched the API through the proxy.
No application or README change was needed.
**Lesson:** verify the published address rather than assuming every loopback name uses the same
listener. Distinguish a verifier's address error from an application startup failure.
**Found by:** ticket 19 clean-clone verification, prompt P-034.

### B-043 · 2026-10-18 · Overview alert count lacked an attention cue

**Symptom:** the author found the Overview Alerts card too neutral during the final live review.
Zero alerts and findings needing review had the same visual weight.
**Cause:** all four metric counts shared one neutral presentation.
**Fix:** author approved green for zero and amber for greater than zero, with a small matching
check or bell icon. Keep the card background quiet and the existing findings-in-this-view text.
The colours indicate attention in the current filter scope, not incident severity or overall safety.
**Lesson:** a status cue should express the decision the analyst needs to make. An alert requires
review; its presence alone does not establish an incident or its severity.
**Found by:** author's Overview review in ticket 19, prompt P-036.

### B-044 · 2026-10-18 · Alerts table repeated supporting counts

**Symptom:** author found the per-rule breakdown above the table and row/page-size caption below
it unnecessary during the live Alerts review.
**Cause:** v1's per-rule counts and the shared pager's supporting caption both accompanied the
total alert count.
**Fix:** retain only the total above the Alerts table. Hide the shared pager's caption for Alerts
while retaining its navigation. Remove the unused per-rule calculation. Explorer keeps its caption.
**Lesson:** repeated counts should earn their place by helping the analyst make a decision.
Keep the primary total clear and supporting controls usable.
**Found by:** author's Alerts review in ticket 19, prompt P-038.

### B-045 · 2026-10-18 · Perplexity credential entered as an environment-variable name

**Symptom:** the new Perplexity MCP was registered but its tools were unavailable. Its bearer
credential setting held a key value instead of an environment-variable name. A diagnostic
printed that field without sanitising it, exposing the entered value in tool output.
**Cause:** setup confused the variable name with its value. The diagnostic incorrectly assumed
that a field intended for a variable name could not contain a secret.
**Fix/status:** active registration replaced with the official local Perplexity MCP server,
launched through uv with the git-ignored backend `.env`. Key values are absent from the new
registration command. Research timeout set to 600 seconds. Author instructed to rotate the
exposed Perplexity key and save its replacement as `PERPLEXITY_API_KEY` in `.env`. That variable
was not present in the file during the check. Connection and rotation remain unverified; no
research call made. No key value is written in this log.
**Lesson:** sanitise every configuration value before displaying it, including fields whose
expected type or purpose appears non-secret. Registration is separate from usable authentication.
**Found by:** MCP setup check, prompt P-040.

### B-046 · 2026-10-18 · Codex research setup referenced the application's environment

**Symptom:** author clarified that Perplexity is a research tool for Codex only, not for Login
Investigator or its in-app agent. The previous setup pointed Codex's MCP launcher at the app's `.env`.
**Cause:** credential setup reused the project environment for convenience instead of respecting
the ownership boundary between development tools and the application.
**Fix:** Codex's global MCP registration now reads `~/.codex/secrets/perplexity.env`, outside
this repository. Created that file with owner-only permissions and an empty credential entry.
No Perplexity key entry was present in the app environment, so no key needed moving. The app's
agent tools were never changed. Authentication still awaits a replacement key and connection restart.
**Lesson:** tool credentials belong to the system using them. An assistant's research integration
must not couple its secret storage or lifecycle to the application being built.
**Found by:** author's correction, prompt P-041.

### B-047 · 2026-10-18 · API-contract prose still mentions removed per-rule counts

**Symptom:** while researching alert severity, the Alerts section of `docs/api-contract.md` still
says the frontend builds a per-rule counts line, although P-038 removed that line at the author's
request. The JSON contract itself is unaffected.
**Cause:** the caption cleanup updated the screen, tests and spec but missed this explanatory
sentence in the contract document.
**Fix/status:** pending documentation follow-up. Not changed during severity research, whose
scope excludes contract changes. No application behaviour or response shape is wrong here.
**Lesson:** when removing presentation text, check descriptive API examples as well as the screen
spec for references to that text. Keep research and implementation changes distinct.
**Found by:** ticket 25 local contract review, prompt P-043.

### B-048 · 2026-10-18 · Explorer supporting captions were unnecessarily wordy

**Symptom:** author requested a plain row count instead of the newest-first/page-size caption,
and removal of "Every matching row, not a sample" during the live Explorer review.
**Cause:** implementation-oriented supporting text repeated information that did not help the
analyst browse the log.
**Fix:** shared pager summary now shows a formatted count with correct row/rows wording and a
full stop. Alerts still hides that summary. Removed the Explorer sampling sentence and kept the
CSV action aligned right. Sorting, paging and full-row results remain unchanged.
**Lesson:** explain a detail in the screen only when it helps the analyst make a decision.
**Found by:** author's Explorer review, prompt P-046.

### B-049 · 2026-10-18 · Investigator progress sat outside the chat

**Symptom:** author barely noticed the tool-progress line because it appeared below the chat box,
separate from the question and answer being watched.
**Cause:** the busy status was a sibling after the message-scroller provider instead of content
inside the chat viewport.
**Fix:** render the existing status after the active question/answer inside its message item.
When no draft exists, including the report-generation wait, show it as an in-chat progress item.
Only one accessible status is shown. Existing progress wording and busy input locking stay intact.
**Lesson:** place feedback at the user's point of attention. A technically present status can
still be ineffective when detached from the activity it describes.
**Found by:** author's live Investigator review, prompt P-049.

### B-050 · 2026-10-18 · Enter inserted a newline instead of sending a question

**Symptom:** author pressed Enter in the Investigator prompt and got a new line, contrary to the
expected chat interaction. Shift + Enter should be the explicit multiline shortcut.
**Cause:** the prompt used the textarea's default Enter behaviour without a chat keyboard handler.
**Fix:** plain Enter prevents the newline and submits the existing form. Shift + Enter retains
normal multiline input. Enter during input-method composition does not submit. Existing send
logic continues to guard empty input and busy/loading operations.
**Lesson:** choose keyboard behaviour for the task the field performs. Chat composition and
ordinary multiline editing have different submission expectations.
**Found by:** author's live Investigator review, prompt P-050.

### B-051 · 2026-10-18 · New keyboard test supplied an invalid answer-stream response

**Symptom:** the first keyboard test sent the correct request but found the input enabled when
it expected the live stream to keep it locked. Nineteen other Investigator checks passed.
**Cause:** the new mocked answer omitted `Content-Type: text/event-stream`. The client correctly
rejected the invalid response and ended the busy state; the test did not model the API contract.
**Fix:** give the test response the required event-stream content type, matching the existing
stream test. Keep the application's response validation intact.
**Lesson:** a realistic boundary test must include the protocol metadata needed to keep the
interaction in the state it intends to observe.
**Found by:** focused Investigator keyboard checks, prompt P-050.

### B-052 · 2026-10-18 · Tool evidence opened abruptly

**Symptom:** author accepted current tool evidence but found instant expansion inconsistent with
the chat stream and gradual report reveal.
**Cause:** the Tools used collapsible had no height/opacity animation or connection to the
answer-delivery pace already measured for reports.
**Fix:** expand the existing Radix content using its measured height and a fade, with a bounded
0.4–1.2-second duration guided by the same observed answer pace. Use 0.8 seconds when no sample
is available and a shorter closing animation. Reduced-motion preference bypasses animation.
Keep all Asked/Found text, table cells and optional raw JSON intact; opening triggers no tool call.
**Lesson:** related interactions should share a coherent rhythm without delaying access to
large evidence tables for their full reading time.
**Found by:** author's Investigator tool-evidence review, prompt P-052.

### B-053 · 2026-10-18 · Sharing observed answer pace exposed a render-time ref read

**Symptom:** tests and build passed, but lint found a new `react(refs)` warning in the first
Tools used animation implementation.
**Cause:** the measured pace was formerly an event-handler-only ref for report creation. Passing
its current value into rendered tool panels read that ref during render, so updates were not
represented as render state.
**Fix:** store observed pace in React state, updated by the existing stream measurements. Both
tool expansion and report creation consume that same value. Keep the original measurement,
bounds and fallback intact; no suppression or unrelated warning cleanup.
**Lesson:** when an event-only value becomes a rendering input, its ownership must change to
reactive state so the screen tracks it correctly.
**Found by:** frontend lint after Tools used animation, prompt P-052.
**Validation:** after the state correction, all 116 frontend tests, type check and build pass;
lint returns to the same six existing warnings. Live visual pacing remains for author review.

### B-054 · 2026-10-18 · Tool expansion grew outside the visible chat

**Symptom:** opening Tools used left the reader at the old scroll position. They had to press
the middle jump arrow to see the expanded evidence, making its animation hard to judge.
**Cause:** the scroller intentionally stops following after manual navigation. The explicit
panel expansion had no separate instruction to reveal the newly growing content.
**Fix:** follow the chosen panel's bottom within the chat viewport for its opening duration.
Move only when evidence extends below view. Cancel on wheel, touch, pointer or keyboard input,
closing or leaving. Reduced motion reveals once. Snapshot the opening duration so later answer
pace updates cannot restart following after the reader interrupts it. Later chat messages are
not the target and the outer page does not scroll.
**Lesson:** an explicit reveal action needs a scoped visibility response even when normal
background updates correctly preserve the reader's position.
**Found by:** author's live tools-expansion review, prompt P-053.

### B-055 · 2026-10-18 · First reduced-motion test did not assert the reveal target

**Symptom:** self-review found the initial reduced-motion check could pass without proving the
full panel had actually been brought into view.
**Cause:** geometry was mocked after opening and only the absence of later scroll movement was
asserted. A remount also invalidated the old element's geometry stub.
**Fix:** provide geometry before opening, including newly mounted content. Assert the exact
initial reveal position and that later growth does not follow under reduced motion. Strengthen
unmount cancellation by changing geometry after removal, so a leaked frame would move the view.
**Lesson:** a cancellation test needs an initial positive result and a later change that would
expose unintended work. A stable number alone can prove nothing.
**Found by:** review of the new Tools used checks, prompt P-053.


### B-056 · 2026-10-18 · Compromise answer does not distinguish attempts from evidence of access

**Symptom:** in the author's supplied live conversation, “Was any account compromised this week?”
received “Yes, there were accounts that experienced suspicious activity” followed by failures,
a success-after-failures finding and a new-country success. It did not clearly separate attempted
attacks from suspected account compromise. High reputation scores were also used as general concern.
**Cause:** the observed answer treats a list of suspicious findings as its response to a compromise
question. The underlying prompt/model cause has not been investigated. Tool outputs were not included
in the pasted transcript, so this record does not independently verify the reputation values.
**Fix:** pending. No prompt, detection or report-policy change made during this manual review.
**Lesson:** an answer should distinguish failed attempts, evidence of successful access and the
remaining uncertainty about who controlled the session. Reputation alone does not settle compromise.
**Found by:** review of the author's conversation, P-055.

### B-057 · 2026-10-18 · Saved investigation omitted required prompt-injection warnings

**Symptom:** the reviewed Investigation's detection evidence contains instruction-like user-agent
text at 8 October 01:33:02 and 02:27:15 UTC. Its later account-search sample also contains the
02:27:15 row. Neither the relevant answers nor the saved report flag prompt injection.
**Cause:** the tool evidence preserved the fields, but the generated outputs did not satisfy the
existing system/report instructions to identify such text. Why the model omitted it is unverified.
**Fix:** pending. No prompt change or live model replay performed during diagnosis.
**Lesson:** resisting an injected instruction and reporting its presence are separate checks.
This sample does not show the agent obeyed the injected instruction.
**Found by:** read-only review of the user-linked saved Investigation, P-058.

### B-058 · 2026-10-18 · Broad investigation skipped required per-IP sign-in searches

**Symptom:** the initial broad compromise question triggered one detection call and three IP
reputation calls. It did not call search_logins for the three finding IPs, although the existing
system prompt requires those searches before answering a broad question.
**Cause:** observed model tool selection did not follow the prescribed workflow. The prompt
states the requirement; application enforcement was not added or assessed in this review.
**Fix:** pending investigation and agreed design. No new workflow or graph implemented.
**Lesson:** a written instruction is not evidence that every required investigation step ran.
Counts from failure-only findings cannot establish the absence of related successful access.
**Found by:** saved tool-call list versus SYSTEM_PROMPT, user-linked Investigation, P-058.

### B-059 · 2026-10-18 · Saved report timeline is not chronological

**Symptom:** report 1 lists 6 October 03:04, 8 October 01:12, 8 October 02:32 and then 6 October
13:47 UTC. The IncidentReport timeline field specifies oldest first.
**Cause:** structured output accepts a list without enforcing time ordering. The report component
renders the supplied order. The saved report itself contains the wrong order.
**Fix:** pending. No saved report edited or regenerated during diagnosis.
**Lesson:** a schema description does not validate a relationship between multiple field values.
**Found by:** comparison of saved report timestamps with their sorted order, P-058.

### B-060 · 2026-10-18 · Case recap silently narrowed to the latest account

**Symptom:** a case began with an all-account compromise question and contained findings about
Daniel, Olivia and 35 password-spraying targets. After a Daniel-specific follow-up and report,
“Which account were we investigating, and what happened to it?” produced only Daniel's story.
The author expected coverage of the other accounts and reports similar Daniel-only responses in
other histories. Those other histories have not been inspected in this review.
**Cause:** the linked history retains the other-account evidence. Its most recent account-specific
focus is Daniel; the system prompt explicitly maps follow-ups to the last answer's single user/IP.
This plausibly contributes to scope narrowing, but the model's reasoning has not been established.
Singular wording is ambiguous. Shared data also makes repeated Daniel answers plausible; it is
not sufficient evidence of cross-case leakage. No hard-coded Daniel fallback was found in the
inspected agent/route code.
**Fix:** pending agreed scope policy. AUD-020 records whole-case versus focused-account recall.
**Lesson:** preserving history does not ensure the agent chooses the user's intended recap scope.
Case-wide recall should distinguish targeted accounts from suspected compromise rather than
silently discarding accounts or treating every failed attempt as successful access.
**Found by:** author's clarification of the user-linked conversation, P-059.

**B-060 investigation update, 18 October 2026 (P-060):** compared all three live histories
containing the repeated recap question. Each already contains Daniel's details in its own earlier
evidence or report. The offline real-route/agent/checkpointer probe found no cross-case marker
leakage in seven captured question-model inputs and two report inputs, including interleaving
and restart. Three existing backend checks and two frontend navigation checks pass. This supports
shared dataset recurrence and scope narrowing, rather than demonstrated history mixing. B-060
remains open for recap behaviour. See docs/audit/conversation-isolation-2026-10-18.md for evidence
and a repeatable probe. No application fix or live conversation mutation made.

### B-061 · 2026-10-18 · Theme review assumed an in-app selector that did not exist

**Symptom:** the author was asked to switch themes, but the app offered no theme control.
**Cause:** main.tsx followed only the operating-system preference. Both colour palettes existed,
but the review instruction incorrectly assumed an explicit selector was available.
**Fix:** author authorised a standard theme selector. Add Light, Dark and System in the shared
header; persist the choice locally, keep System as default and retain live system updates.
Validate storage fallback and keyboard use; apply the initial preference before the page paints.
**Lesson:** verify that a review action is actually available before asking the author to use it.
**Found by:** author's correction during manual theme review, P-061.

### B-062 · 2026-10-18 · Theme check setup used the wrong execution context

**Symptom:** the first theme-test command ran from the repository root without a package.json.
After rerunning from frontend, the suite could not collect because its file read treated Vite's
browser-transformed import.meta.url as a filesystem URL.
**Cause:** the test assumed a Node-only module URL inside jsdom/Vite. The shell invocation also
missed the documented frontend working directory.
**Fix:** run npm from frontend and import the trusted index.html as raw Vite text for the
first-paint script check. Supply the missing jsdom scrollIntoView behaviour locally for keyboard
select tests, restoring it after each check. No application validation was bypassed.
**Lesson:** boundary tests must use the execution context actually provided by the test runner.
**Found by:** focused theme-control checks, P-061.

**Theme validation for B-061/B-062:** 13 focused cases and all 134 frontend tests pass after the
setup correction. Type check, production build and lint pass, with the same six existing lint
warnings and bundle-size warning. The server serves the theme control. Live author review of
Light/Dark readability remains pending; no visual acceptance inferred from DOM tests.

### B-063 · 2026-10-18 · Alerts header blended into the selected row

**Symptom:** in the author's light and dark reviews, the column header and selected alert shared
the same background tone and were difficult to distinguish.
**Cause:** the header used bg-muted, and the shared TableRow selected state also uses bg-muted.
The shared noninteractive header row inherited body-row hover styling as well.
**Fix:** darken only this header's existing muted colour, mixing 5% black in light mode and 20%
in dark mode. Keep its row transparent on hover so the tone stays stable. Preserve column text,
selected-row background, left accent, keyboard selection and other tables.
**Lesson:** structural headers and selected data need distinct surfaces in each theme.
**Found by:** author's light/dark review, P-063. Live review of the adjusted tone remains pending.

**B-063 closed, 18 October 2026:** author approved the adjusted header with “good” (P-064).
Fourteen Alerts tests and production build/type check pass. The theme-specific header distinction
is accepted. Existing bundle warning remains separately tracked.


### B-064 · 2026-10-19 · Investigation history list differs from v1

**Symptom:** author reports investigation history is not quite like v1; exact concern awaits
clarification. Independent read-only comparison confirms no collapse control in v2 after the
list is fully expanded. v1 offers Show fewer. For an older selected case, v1 reveals a contiguous
prefix rounded to groups of three; v2 shows the newest limited entries plus the selected case.
v1 also animates newly revealed cards; v2 has no equivalent reveal animation.
**Cause:** v2 uses a numeric limit and a filter including the active ID, with only a Show three
more control. v1 uses cases_to_show plus show_fewer_cases and a constant reveal animation.
**Fix:** pending clarification and agreed screen treatment. No application code changed.
The spec explicitly covers three-at-a-time expansion and keeping the open case visible; it does
not explicitly describe collapse or animation. Do not silently change the spec.
**Lesson:** matching storage and reopening does not establish parity of history navigation.
**Found by:** author report, P-073; comparison of frozen v1 app/screens/investigator.py and
v2 frontend/src/pages/investigator.tsx. No v1 file changed.


**B-064 implementation, 19 October 2026 (P-074):** restored arrow-only expand/collapse
controls with accessible labels and hover titles. Expansion reveals three entries, or the actual
remaining count. Older selection reveals a continuous prefix in groups of three. Collapse keeps
enough entries to retain that selection; its arrow is disabled when no reduction is possible.
Newly mounted entries fade/slide for 320 milliseconds only when reduced motion is not requested.
No stored conversations or backend behaviour changed. All 136 frontend tests pass, including
three list-navigation cases; build/type check pass. Lint retains six existing warnings and build
retains the bundle-size warning. Author's live visual acceptance remains pending.


**B-064 closed, 19 October 2026:** author replied “yes all good” after testing the restored
history arrows (P-075). Live navigation correction accepted, supported by all 136 frontend
tests and passing build/type check. Existing lint and bundle warnings remain separate.


### B-065 · 2026-10-19 · Reputation progress phrase not observed although tool ran

**Symptom:** author did not see “Looking up IP reputation…” during the live presence check,
but supplied inline evidence of the saved lookup for 185.218.86.24. The presence gate stays open.
**Cause:** live timing is not captured, so the precise live event sequence is unproven. Confirmed
frontend weakness: each tool event replaces one progress string. A deterministic offline
component probe sent reputation and search events in one network chunk. Only the search phrase
was rendered; the reputation phrase was absent. The backend forwards named tool events from
model tool-call chunks; saved tool evidence alone does not prove its event was visibly painted.
**Fix:** pending author agreement on a short cumulative tool-activity list during answering.
No artificial wait or agent change proposed. No application change made during diagnosis.
**Lesson:** transient latest-event status cannot guarantee visibility of every tool in a burst.
**Validation:** temporary component diagnostic reproduces overwritten reputation wording using
real page/hook/SSE parsing, no live calls. Diagnostic removed after the run; retain a regression
case if the remedy is approved. See P-082 for run result.


**B-065 research update, 19 October 2026 (P-083 to P-085):** author rejected the cumulative
activity list and retained single changing status. Official docs distinguish model-generated
calls from execution lifecycle. Installed framework supports callbacks and native lifecycle
streams. Three offline probes passed for parallel execution, checkpoint/answer preservation
and controlled failure. Recommendation is public callbacks plus custom stream events in the
existing sync path; newer v3 API is marked experimental. Exact live timing remains unproven;
near-instant cached operations may still be imperceptible. Research note:
.scratch/v2-port/research/27-tool-progress-lifecycle.md. No implementation yet; gate stays open.


### B-066 · 2026-10-19 · Explorer test timed out during progress-change verification

**Symptom:** full frontend run passed 137 of 138 tests, but Explorer's valid-IP/Reset test
exceeded its existing five-second timeout. Backend tests, type checking and frontend build
were running concurrently. Explorer application and test code were not changed by P-086.
**Cause:** unconfirmed. Host contention is a plausible explanation, not an established cause.
**Fix:** no timeout increase or unrelated code change. Rerun the affected screen and modified
Investigator tests with one worker, then rerun the full suite with bounded concurrency.
**Lesson:** retain a timeout failure and its rerun evidence rather than treating it as a pass.
**Found by:** P-086 full frontend verification. Final rerun results to be appended.


**B-066 rerun evidence, 19 October 2026:** all 35 Explorer and Investigator tests passed with
one worker, without Explorer code or timeout changes. Cause remains unconfirmed; full-suite
bounded-concurrency rerun is in progress. AUD-028 preserves the unresolved test-reliability concern.


**B-065 implementation, 19 October 2026 (P-086):** added per-invocation inline LangChain
callbacks publishing small typed lifecycle signals through messages/custom streaming. API tool
events contain only an allowlisted name, opaque call ID and start/end/error phase. Existing
legacy callers still receive the original start-only Stream shape; copied tests stay unchanged.
The frontend tracks each active call ID, deduplicates names for a single combined phrase, removes
only the completed call and returns to Thinking/Writing the answer when none remain. Completion,
failure and navigation clear transient progress. No artificial delay or serialized tool execution.
Five real-framework offline tests cover parallel calls, duplicate names, saved follow-up, an
unexecuted request, and handled/propagated errors. HTTP privacy test and frontend burst, completion,
failure, malformed-event and navigation checks pass. Final suite evidence is in Parity closing.
Live author acceptance remains pending; near-instant cached calls can still be imperceptible.

**B-066 full rerun evidence, 19 October 2026:** all 141 frontend tests passed with one worker.
No Explorer code or timeout changes. Original timeout retained; cause remains unknown and
AUD-028 stays open for test reliability review.


**B-065 live review failed, 19 October 2026 (P-087):** author mainly sees Thinking, with only
brief flashes of tool wording, even on a response showing four tool calls. Execution tracking
passes tests, but practical readability remains unsatisfied. Do not mark this implementation
accepted. A read-only warmed-tool timing probe, five invocations each with external lookups
blocked, measured median detection 4.07 ms (3.70–7.05), search 13.33 ms (12.92–13.55) and saved
reputation 0.82 ms (0.77–1.05). These are isolated local measurements, not captured timings of
the author's live model/browser run. On the frontend, the last end event returns progress to
Thinking until answer text arrives. Tool count does not imply perceptible execution time.
Proposed refinement: retain only the most recent finished activity in past tense while the
model prepares the response, then replace it at the next tool start or first answer text.
Example: “IP reputation lookup finished. Preparing response…”. No cumulative list, fake active
status or artificial delay. Awaiting author agreement; no application change in this diagnosis.


**B-065 live external timing evidence, 19 October 2026 (P-089):** one isolated real AbuseIPDB
lookup for uncached public IP 1.1.1.1 returned source live in 0.477 seconds. The real core
agent.ask adapter with fixed fake model and temporary memory emitted start at 0.014 seconds
and end at 0.491 seconds, matching call ID. No saved-cache changes or app Investigation created.
This supports correct real-network lifecycle signals; browser perceptibility remains unverified.
One sample is not a production latency claim. Proposed past-tense display change remains held.


**B-065 positive multi-IP feedback, 19 October 2026 (P-091):** author replied “way better”
after receiving the four-IP reputation-only test question. Record improved readability of the
current single-line implementation. No answer/tool-count/timing evidence was independently
inspected, so no claim about four live successful requests. Further display changes remain held.
Explicit final current-progress ruling requested before closing this finding or presence gate.


**B-065 closed, 19 October 2026:** P-092 explicitly approves the current execution-based
single-line progress after positive multi-IP feedback, accepting that fast cached calls may
be too brief to read. Closure evidence: 379 full backend tests plus one added HTTP privacy case,
141 frontend tests, both type checks/build, the isolated 0.477-second live lookup and author
review. No cumulative list or past-tense hold implemented. Future timing changes are not implied.


### B-067 · 2026-10-19 · Scenario acceptance evidence not yet matched to saved case

**Symptom:** author confirms scenario follow-up/report/PDF, but a read-only inspection of default
backend/memory/investigations.sqlite cannot correlate that sequence. Three newest exact overnight
question cases have one turn and no report. No stored case has the exact unnamed follow-up;
only two 18 October cases have reports. Next-day acceptance names a different prior case.
**Cause:** unknown. Wrong reviewed case or runtime data location is possible. This is an evidence
correlation gap, not established loss of history, failed generation or incorrect author feedback.
**Fix:** pending the author's current Investigation URL, then compare the actual live API case
and configured store. Preserve dated author rulings; hold aggregate end-to-end acceptance.
Do not silently waive same-case continuity or change stored conversations.
**Lesson:** individual manual confirmations need a shared case identity before an end-to-end
scenario can be claimed complete.
**Found by:** P-100 final-record audit. Used SQLite URI mode=ro and saved_history without model;
skipped checkpointer setup DDL on the existing read-only schema. No app/database mutation.


**B-067 identity resolved; scenario gap remains, 19 October 2026 (P-101):** linked case
90c317b74bb94e2b9d066e2515da5d1f is present in both live API (200) and default saved store.
It begins “Was any account compromised this week?” and contains only the opening answer and
report. Opening used detection plus three reputation lookups, zero sign-in searches. No unnamed
follow-up exists in this case. Report timeline dates 6 Oct → 8 Oct → 8 Oct → 6 Oct are unordered.
No evidence of storage loss or wrong runtime memory. Unknown whether other confirmations refer
to another case; requested its URL. Retained historical rulings but reopened scenario steps
2/4/6/7 for correlation/content. No stored message or report changed.

**B-058 recurrence, 19 October 2026 (P-101):** current linked broad-question case has three
reputation lookups but no required per-IP sign-in searches. Not a newly fixed issue; AUD-022 open.

**B-059 recurrence, 19 October 2026 (P-101):** current linked report also has an out-of-order
timeline, 6 Oct → 8 Oct → 8 Oct → 6 Oct. P-099 author approval is retained as history but cannot
prove chronological correctness of this stored report. AUD-023 remains open. No historical rewrite.


**B-067 complete saved-case search, 19 October 2026 (P-103):** all 16 cases and 31 turns
searched read-only. Found named-account follow-ups in 9f06429702864efca91a6fab8f7c1517 turn 3
and 872227a3ca7948748f7b4f1ec57ee6c3 turn 4. Each has one sign-in search and an answer with both
expected later GB IPs/timestamps. Exact unnamed wording absent after normalising case/whitespace/
trailing punctuation. Related history is present; gap is the exact unnamed scenario and same-case
continuity, not history loss or requiring the author to find more URLs. No mutation/replay.


**B-067 unnamed recall now evidenced, 19 October 2026 (P-105):** exact “Did that user sign in
from anywhere else afterwards?” is saved as turn 6 of 9f06429702864efca91a6fab8f7c1517. Answer
correctly names Daniel and both expected later GB IPs/timestamps. Zero new tools; both events
are already in turn-3 search evidence, verified read-only. Narrow reference/grounding gap is
resolved. The exact overnight scenario's fresh-search and same-case continuity remain open.
No new omission defect inferred from reusing known evidence for this repeated question.


**B-058 implementation, 19 October 2026 (P-107):** standard LangChain before_model middleware
collects valid IPs from actual current-turn detection ToolMessages and schedules missing
unrestricted search_logins calls before another model call. Existing completed attempts, even
failed ones, count to prevent loops. Filtered searches do not stand in for whole-IP coverage.
No prompt, tool schema or custom graph change. Six offline real-agent cases cover omitted and
existing searches, filters, failure, duplicate/invalid IPs, no findings and new-turn isolation.
Initial five cases plus all unchanged copied agent tests passed; full suite/benchmark in progress.

**B-059 implementation, 19 October 2026 (P-107):** newly generated report timelines sort by
parsed timezone-aware timestamps before save and return. Stable chronological ordering flows
through saved reports to the PDF. Invalid or timezone-free timestamps refuse saving a new
report. Existing historical reports are not reordered or rewritten. API regressions cover
returned/saved/PDF order, offset-aware comparison, original object preservation, invalid times
and historical reads. Initial API/eval compatibility group: 35 passed. Final suite pending.

### B-068 · 2026-10-19 · Search policy assumed every tool call had an ID

**Symptom:** first Pyright check of the new policy found two errors because LangChain types
allow a missing tool-call ID.
**Cause:** a dictionary comprehension inferred optional IDs as keys for a string-keyed map.
**Fix:** only add calls with an explicit string ID; unmatched tool results cannot trigger policy.
**Lesson:** correlate tool evidence by verified IDs rather than assuming a complete model chunk.
**Evidence:** updated code passes Pyright with zero errors, warnings or information messages.
No application runtime failure or live-data mutation. Part of P-107, pending final feature review.


### B-069 · 2026-10-19 · Search enforcement broadened a narrow password-spraying question

**Symptom:** first post-fix API benchmark passed 55/57 overall and all 15 security attempts,
but Q08 runs 1 and 3 counted the brute-force IP as a password sprayer. Preserved result
backend/evals/results/2026-10-19-110557-4caada27.json.
**Cause:** the first policy enriched every detection IP even for an explicitly narrow attack-type
question, adding unrelated source evidence before the model could focus its answer. Both failed
Q08 opening answers then listed the brute-force IP under the password-spraying answer. The
mechanism is confirmed; model wording remains stochastic.
**Fix:** broad enrichment now excludes explicit attack-type and literal-IP questions, leaving
those tool choices to the model as before. Narrow exclusions cover spray wording, brute force,
new-country and success-after-failure wording. No claim of universal natural-language intent
classification. Broad questions still receive all required per-IP searches.
**Lesson:** mandatory evidence completion must preserve the user's scope.
**Evidence:** three new real-framework narrow-scope regressions and all earlier policy/copied
agent tests pass (31 total). Final full suite and benchmark in progress. Earlier 390-case suite
passed before this scope refinement; it is not represented as checking the final revision.


**B-069 final evidence, 19 October 2026:** final fingerprint 7ff8e5ae API benchmark passes all
three Q08 attempts. The full run passes 56/57 overall and 15/15 security; result
backend/evals/results/2026-10-19-111011-7ff8e5ae.json. Original 55/57 run remains. Final policy
has narrow-scope regressions and clean Pyright; author review pending.

### B-070 · 2026-10-19 · Follow-up lists two later sign-ins but claims three

**Symptom:** final benchmark Q07 run 1 lists the correct two later GB sign-ins, then says there
were three successful sign-ins after the initial one. Q07 runs 2 and 3 pass.
**Cause:** observed search starts at 02:32:20 inclusively, so its count includes the initial
suspicious success. The answer failed to exclude that event when describing later sign-ins.
This is an observed grounding/counting error, not missing memory or a failed user search.
**Fix:** none in this two-fix scope. Keep the failed attempt counted. Existing system prompt
already says not to count the initial event; a robust follow-up/count design needs separate work.
**Lesson:** a correct evidence list does not guarantee a correct prose total, especially across
an inclusive search boundary.
**Evidence:** 2026-10-19-111011-7ff8e5ae.json, Q07 run 1. Unchanged grader catches it; 56/57 overall
and 15/15 security still meet the agreed threshold. The check's inherited “B-013” label refers
to v1's count bug, not this repository's different B-013 validation-message entry.


**P-108 closure, 19 October 2026:** author approves the consolidated case and PDF, required
searches, chronological new report and Investigator hierarchy. B-058 (missing required searches),
B-059 (new-report ordering), B-067 (case-correlation gap), B-068 (optional call-ID typing) and
B-069 (scope regression) are closed with the implementation/regression evidence and this ruling.
Historical report instances are preserved. Same-case next-day continuation is an acceptance
check pending 20 October, not a remaining case-identity defect. B-070's counted benchmark
failure and other unrelated open bugs remain. No app/history changes for closure.
