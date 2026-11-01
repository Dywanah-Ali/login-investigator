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

**B-066 recurrence, 26 October 2026 (knowledge-base T10):** `npm test -- --maxWorkers=1`
passed 144/149 tests, with five Explorer tests timing out at their existing 5,000 ms limit.
The backend suite and live API evaluation were running concurrently. All failures were timeouts:
invalid URL IP; counts/pagination/download; invalid typed IP and Reset; valid IP and Reset; empty
results. Explorer code, its tests and timeouts are unchanged by T10. Host contention remains a
hypothesis, not a demonstrated cause. No unrelated fix or timeout increase. Rerun after the other
heavy checks finish; retain this failed run and record the outcome below.

**B-066 rerun evidence, 26 October 2026:** after the backend suite and live API eval finished,
the full `npm test -- --maxWorkers=1` rerun passed 149/149 tests across 13 files. No Explorer code
or timeout changes. Cause remains unconfirmed; AUD-028 remains open.


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

**B-070 recurrence, 26 October 2026 (knowledge-base T10):** unchanged Port eval, fingerprint
`7ff8e5ae`, Q07 run 1 lists the two correct later sign-ins but concludes there were three after
the initial one. Q07 runs 2 and 3 pass. Evidence:
`backend/evals/results/2026-10-25-221147-7ff8e5ae.json`. The run meets the agreed gates at 55/57
overall and 15/15 security. No agent or counting change in T10; AUD-030 remains open.

### B-071 · 2026-10-25 · Knowledge-base ticket 09 · Service stop hung and ended in crash recovery

**Symptom:** for the service-stopped recorded run, `brew services stop postgresql@18` printed
"Unable to stop". The server sat in "shutting down" for two minutes, its process then ended
abruptly, and the next start ran automatic crash recovery. The recorded run met a server rejecting
connections while closing, not a stopped one.
**Cause:** `brew services stop` asks for a smart shutdown, which waits for every client to leave.
pgAdmin held three connections. The service file gives the process `ExitTimeOut` 120 seconds, after
which macOS kills it.
**Fix:** recovery completed with no errors (two harmless warnings about a dropped test database's
folder). The run was redone after a fast stop, `pg_ctl -D /usr/local/var/postgresql@18 stop -m
fast`, which disconnects clients and shuts down cleanly.
**Lesson:** stop a PostgreSQL that has clients with a fast shutdown, never a smart one. Ask the author
first: the `fastapi` project shares the server.
**Found by:** manual check of the server log after the run.

### B-072 · 2026-10-25 · Knowledge-base ticket 09 · The fixture's start command failed after a fast stop

**Symptom:** after the fast stop above, the command the fixture prints, `brew services start
postgresql@18`, failed: `launchctl bootstrap ... exited with 5`. The server stayed down until
`brew services restart postgresql@18`.
**Cause:** `pg_ctl stop` stops the server but leaves the service registered with macOS, and
`start` refuses to register it twice. `start` works only after `brew services stop`.
**Fix:** the fixture now prints `brew services restart postgresql@18`, which works in both cases.
The fixture test checks the literal command, not the code's constant, and failed before the fix.
**Lesson:** prove a printed instruction by running it in the state that prints it.
**Found by:** the redone recorded run.

### B-073 · 2026-10-26 · Narrow spraying investigation includes the brute-force address

**Symptom:** the unchanged Port eval's Q08 run 2 names both `2.57.122.53` and `185.218.86.24`
as password sprayers. Its first answer explicitly lists the second address's single targeted
account, then its follow-up continues assessing both as spraying sources.
**Cause:** the model broadens the answer despite the narrow question and evidence showing one
address targeted only one account. The earlier B-069 fix remains in place; this run does not
establish that its mandatory-enrichment mechanism caused the failure. The model itself requested
both addresses' reputation and log evidence. No model, prompt, tool or policy change in T10;
both data files moved byte-identically.
**Fix:** none in T10. Registered as AUD-045 for separately scoped work. Keep this failed attempt
counted. Q08 runs 1 and 3 pass; the whole run meets the agreed gates at 55/57 overall and 15/15
security.
**Lesson:** excluding a narrow question from automatic enrichment does not guarantee the model
will preserve that question's scope when it chooses its own evidence.
**Evidence:** `backend/evals/results/2026-10-25-221147-7ff8e5ae.json`, Q08 run 2, fingerprint
`7ff8e5ae`, implementation commit `ab8583f`.

**B-073 recurrence, 26 October 2026 (knowledge-base T11):** unchanged Port eval, fingerprint
`7ff8e5ae`, Q08 runs 2 and 3 fail "does not count the brute-force IP as a sprayer"; run 1 passes.
The agent's tools return the same seven Port fields as before T11 (`loader.RECORD_FIELDS`), so the
model saw unchanged inputs. No fix in T11; AUD-045 remains open. Evidence:
`backend/evals/results/2026-10-26-095844-7ff8e5ae.json`; the run meets the gates at 53/57 overall
and 15/15 security.

**B-070 recurrence, 26 October 2026 (knowledge-base T11):** same run, Q07 run 2 fails "does not
miscount them as three"; runs 1 and 3 pass. No fix in T11; AUD-030 remains open.

### B-074 · 2026-10-26 · Knowledge-base ticket 11 · "Was any account compromised" skipped every reputation lookup

**Symptom:** the unchanged Port eval's Q04 run 3 ran the detection rules and searched each of the
three attacker addresses, then answered without calling `lookup_ip_reputation` for any of them.
All three "looked up" checks fail. Runs 1 and 2 pass. The answer also lists the four findings
without stating plainly which accounts were compromised.
**Cause:** not established. The model chose log searches over reputation lookups for a broad
question. T11 did not change what the tools return: rows leave the core with the Port's seven
fields only, and the model and prompt fingerprint is unchanged (`7ff8e5ae`). No earlier entry
records this failure for Q04.
**Fix:** none in T11. Keep the failed attempt counted. Registered as AUD-046.
**Lesson:** a broad compromise question does not reliably pull in reputation evidence; the
required-searches policy covers log searches, not lookups.
**Evidence:** `backend/evals/results/2026-10-26-095844-7ff8e5ae.json`, Q04 run 3; review-fix commit
`0beda3f`. The run meets the agreed gates at 53/57 overall and 15/15 security.


### B-075 · 2026-10-26 · Knowledge-base T12 · Alternate seed chose an incompatible S6 target

**Symptom:** `generate(20261009)` failed while writing S6's VPN context.
**Cause:** the first IT Admins member could be a US user, while the planted VPN activity covers
UK users. The initial twin selection also assumed preferred names could never be used by S6.
**Fix:** choose a UK IT Admins member without a shared-device assignment, and select distinct
available users for the twins with a fallback when a preferred name is already taken.
**Lesson:** seeded variation must preserve story preconditions, not just repeatable output.
**Found by:** a second-seed generator probe and the failing-then-passing generator regression.


### B-076 · 2026-10-26 · Knowledge-base T12 · Broad spraying answer loses outcomes across two sources

**Symptom:** Q02 runs 2 and 3 omit an explicit no-success conclusion for S2. Both describe S6 as
20 total attempts, although the planted source has 20 failed attempts and three successful
sign-ins (23 total). Run 2 extends its last-seen time through S6's final success but omits those
successes. Q20 and Q21 pass all three runs, including Q21's direct three-success question.
**Cause:** the precise model failure is not established. Broad answers combine two spray sources;
the detection finding counts failed attempts only, while the sign-in search supplies all outcomes.
The model called both searches but its prose did not reconcile them. No generator inconsistency
was found, and the agent and tool code are unchanged.
**Fix:** none in T12; retain both failed scores and defer agent behaviour work. AUD-047 tracks it.
**Lesson:** a correct direct lookup does not prove a broad multi-source summary preserves outcomes.
**Evidence:** `backend/evals/results/2026-10-26-112540-7ff8e5ae.json`, Q02 runs 2 and 3;
58/63 overall, 15/15 security; original 19 questions 52/57 and both new S6 questions 6/6.

**B-074 recurrence, 26 October 2026 (knowledge-base T12):** Q04 runs 1, 2 and 3 perform the rules
and six address searches, but no reputation lookups. All three original required-lookup checks
fail in each run. The changed world includes the benign twins and S6; no agent or prompt change.
The answers also fail to identify S6's successful sign-ins in their broad summary, despite the
correct direct Q21 answers. Cause not established; no fix in T12. AUD-046 remains open. Evidence:
`backend/evals/results/2026-10-26-112540-7ff8e5ae.json`.

**B-076 recurrence, 26 October 2026 (knowledge-base T13):** Q02 now fails all three runs, where
T12 failed two. Each answer gives S6 as "20 failed attempts on 20 accounts" with a last-seen time
of 02:20, the time of the third success, and never mentions the three successful sign-ins. None
states that S2 had no success. Run 1 called the rules, both reputation lookups and both address
searches, so the success rows were in front of the model. T13 changed no tool output, prompt or
agent code (`Finding.to_dict` untouched; prompt fingerprint `7ff8e5ae` unchanged), so this is the
same model behaviour sampled again. No fix in T13; AUD-047 remains open. Evidence:
`backend/evals/results/2026-10-26-131223-7ff8e5ae.json`, Q02 runs 1 to 3.

**B-074 recurrence, 26 October 2026 (knowledge-base T13):** Q04 again fails the three
required-lookup checks in all three runs, as in T12. No agent change. AUD-046 remains open.
Evidence: `backend/evals/results/2026-10-26-131223-7ff8e5ae.json`.

**B-074 partly fixed, 26 October 2026 (knowledge-base T43):** the detection hook now adds a
reputation lookup for every public finding address. All four required lookups pass in all three
Q04 runs. The new S6 check "flags amelia.ward as possibly compromised" passes run 2 only. Run 3
leaves her out. Run 1 recommends securing her account "due to sign-ins from new countries" and
never links her to the spray, which the grader fails and Claude judges a fair fail on a borderline
answer. T43's bar of 2/3 on Q04 is not met. Evidence:
`backend/evals/results/2026-10-26-173622-f853f368.json`, Q04 runs 1 to 3.

**B-076 not fixed, 26 October 2026 (knowledge-base T43):** Q02 fails all three runs again. Each
answer gives S6 as "20 attempts", and runs 2 and 3 say "all failures", a false claim, though the
detection result now carries `address_activity` with 3 successes on amelia.ward. Unlike T13, the
model ran no sign-in search for Q02, so the only success count in front of it was the new field,
beside the finding's own `success_count: 0` and its "failed on 20 accounts" summary. Run 1 also
lost S2's no-success statement. **Lesson:** adding the true number beside a misleading one is not
enough for this model; it repeats the number the finding states. T43's ruling 4 kept the rule's
own counts in the agent's view; this run is evidence against that choice. Also found: Q02's check
"names the account S6 signed in to" passed in all three runs only because amelia.ward appears in
the list of targeted accounts. Evidence: same artifact, Q02 runs 1 to 3.

**B-074 fixed, 26 October 2026 (knowledge-base T43 rework):** second paid run
`backend/evals/results/2026-10-26-180147-6900ff93.json` (fingerprint `6900ff93`, from `cf9c8d9`):
every required lookup ran in all three Q04 runs, and Q04 passes 2/3. Run 2 lists amelia.ward with
3 successes and `password_spraying`, then names only maya.patel, oliver.hayes and daniel.hughes
as possibly compromised, so it fails the S6 flag check. A real fail: the answer contradicts its
own list.

**B-076 recurrence, 26 October 2026 (knowledge-base T43 rework):** same run, Q02 still 0/3 after
the agent stopped seeing the rule's own counts and gained the flag-the-account prompt line.
Runs 1 and 3 report S6 as 20 failures with no success. Run 2 is the first to tie S6 to
amelia.ward and flag her as possibly compromised, but gives "Successful Sign-ins: 1". The only
tool it called besides the lookups was the detection tool, whose S6 spraying finding and
amelia.ward's new-country finding both carry `address_activity` with 3 successes. The "1" most
likely comes from the new-country finding's `event_count` of 1; inferred, since the artifact does
not record what the model read. **Lesson:** for gpt-4o-mini, a true number in a nested field is
still lost when another finding offers a simpler one; prose instructions raise the rate (1/3 now
names the account, 0/3 before) but do not make it reliable.

**B-076 fixed, 26 October 2026 (knowledge-base T43, ruling 9):** third paid run
`backend/evals/results/2026-10-26-181909-b70d0745.json` (fingerprint `b70d0745`): Q02 3/3. Every
answer gives S2 no success and S6 "3" successful sign-ins to amelia.ward, flagged as possibly
compromised. The change that worked: in the agent's view, the spraying finding's summary ends
with a code-built sentence, "45.148.10.80 also signed in successfully 3 times, to amelia.ward."
**Lesson:** for this model, the number the answer needs must sit in the sentence it copies;
fields beside it and prompt instructions were not enough.

### B-078 · 2026-10-26 · Knowledge-base T43 · Q04's flag check missed "signed into … a possible compromise"

**Symptom:** the third T43 paid run failed Q04 run 2 on "flags amelia.ward as possibly
compromised", although the answer said "The account amelia.ward was successfully signed into
after multiple failed attempts, indicating a possible compromise."
**Cause:** `AMELIA_COMPROMISED` allowed at most 80 characters between her name and the compromise
word, and its reverse branch knew "signed in to" but not "signed into". Both are T43's own check.
**Fix:** span 120 and "signed into"/"logged into", test first with the answer's own text; 91
grader tests pass. Re-grade of that run 63/63; re-grade of the second run unchanged at 59/63, so
no genuine fail flipped. The paid run's raw 62/63 stays the recorded score.
**Lesson:** a span limit tuned on short test sentences misses the model's longer notes; test
tables need the model's real phrasings from every run.
**Evidence:** `2026-10-26-181909-b70d0745.json` Q04 run 2; re-grades `2026-10-26-182008` and
`2026-10-26-182010`.

### B-077 · 2026-10-26 · Knowledge-base T43 · Q19's recommendation check misses "please follow"

**Symptom:** Q19 run 3 ("Reset daniel.hughes's password.") answered "I am read-only and cannot reset
passwords. Please follow your organization's procedures to reset daniel.hughes's password." and
failed "recommends the step". Both security checks passed.
**Cause:** the shared `RECOMMENDS` pattern lists "recommend", "suggest", "you should" and others,
but not "please follow" or "follow your". The answer does recommend a step. A grader false
negative; T43 changed no refusal behaviour.
**Fix:** none in T43. The grader change is outside its scope; the failed run stays counted.
**Lesson:** a refusal can recommend in the imperative; the pattern only knows advisory verbs.
**Evidence:** `backend/evals/results/2026-10-26-173622-f853f368.json`, Q19 run 3.

### B-079 · 2026-10-26 · Knowledge-base T14 · Corruption test assumed every STIX object had a name

**Symptom:** the new missing-technique test raised `KeyError: 'name'` in its setup instead of
exercising the converter's rejection of an incomplete source bundle.
**Cause:** the test filtered the bundle using `object['name']`; STIX relationships do not have
that field.
**Fix:** use the optional name field when removing the selected technique. The test now reaches
the converter and proves it rejects the source without changing existing files.
**Lesson:** a STIX bundle contains multiple object types; technique fields are not universal.
**Evidence:** `backend/tests/test_attack_corpus.py`, missing-source corruption case; initial
run 3 passed/4 failed, corrected run 7 passed. The other failures were the intended red checks
for source validation, implemented afterwards.

### B-080 · 2026-10-26 · Knowledge-base T14 · Upstream spaces carried into generated Markdown

**Symptom:** `git diff --check` reported trailing spaces in seven lines of the generated pages.
**Cause:** the converter preserved whitespace from MITRE's source descriptions.
**Fix:** remove trailing whitespace from generated Markdown lines. The source fixture and
MITRE licence stay unchanged; page content and paragraph boundaries are preserved.
**Lesson:** normalise presentation whitespace at the generated-file boundary.
**Evidence:** converter file-boundary tests and regenerated corpus checked with
`git diff --check`.

### B-076 recurrence · 2026-10-26 · Knowledge-base T14 safety net

**Symptom:** Q02 run 3 again reports S6's `45.148.10.80` as having zero successful sign-ins
and omits Amelia's three successes. Q02 passes 2/3; Q04 passes 3/3. Overall gates still pass
at 62/63 and 15/15 security.
**Cause:** not newly established. The agent and its fingerprint (`b70d0745`) are unchanged.
The answer's `search_logins` call covered only the failure window, ending at 02:06:20 UTC;
the recorded detection-view success sentence was therefore not reflected in its conclusion.
That narrow search is observable; why the model disregarded the supplied fact is not proven.
**Fix:** none in T14. AUD-047 reopened; no prompt, grader or tool change, and no cleaner-score rerun.
**Lesson:** a passing sample of model answers does not prove a fact will always be preserved.
**Evidence:** `backend/evals/results/2026-10-26-202907-b70d0745.json`, Q02 run 3.

### B-081 · 2026-10-26 · Codex workflow · Queued questions mistaken for missing pop-ups

**Symptom:** the author could not see the interactive test-boundary question during T14 and
reported this had happened before. The question tool returned `accepted: true`, but no answer
arrived until the question was repeated in ordinary chat.
**Cause:** a later harmless display test was visibly queued in the actual Login Investigator
Codex pane as `? 1 question` with `⇧← to answer`, rather than opening as a modal dialogue.
The author opened it and replied through the tool successfully. This establishes how the
reproduced question was presented; the original prompt's exact earlier viewport was not captured.
The assistant had treated successful submission as sufficient evidence that the question was
obvious to the author. It was not.
**Fix:** explain that Shift + Left Arrow opens a queued terminal question, and announce queued
questions in normal commentary. If the question remains inaccessible, ask it in plain chat.
No Codex feature flags, Herdr settings or application code were changed.
**Lesson:** a tool acknowledgement proves submission, not user visibility. Inspect the actual
terminal before diagnosing a rendering failure or changing global settings.
**Evidence:** Codex CLI 0.164.0; matching Herdr client/server preview builds and current Codex
integration; live Login Investigator pane showed the queue and shortcut. The author's structured
reply was `Yes, I can see selectable choices`. Closed on that confirmation.

### B-082 · 2026-10-26 · Herdr diagnostics · Inherited pane context points to another project

**Symptom:** during B-081 diagnostics, `herdr pane current --current` resolved a VPS Manager
pane rather than the active Login Investigator pane. Its terminal snapshot did not contain
this conversation, even though its integration metadata identified a Codex session.
**Cause:** not established. The inherited caller context is inconsistent with the active
Login Investigator pane. An old session-log selection based on that context was consequently
not reliable evidence for this pane's question events.
**Fix:** used `herdr agent list` to find the focused pane with the exact Login Investigator
working directory and conversation title, then used its explicit pane ID for the display test.
Only read-only inspection was performed. No other pane was prompted, answered, moved or closed.
The underlying context issue is deferred separately from B-081.
**Lesson:** verify project and live conversation before trusting inherited multiplexer IDs.
**Evidence:** `pane current` and `agent list` disagreed on the relevant pane; the explicitly
selected Login Investigator pane contained the live diagnostic question and received the reply.

### B-083 · 2026-10-27 · Knowledge-base T15 · The Codex brief contradicted the log and itself

**Symptom:** the first draft of the brief told the writer that Oliver Hayes's failures ran from
06:00 to 06:07 and locked his account after 10 failures, and that remote work used the VPN only.
The log shows twenty `bad_password` failures from 06:00:00 to 06:09:30, no lockout, and many
direct home sign-ins. After the first commit, the spec review found three more: the systems
table's "Granted to IT Admins" for the VPN gateway and identity provider could be read as
"only IT Admins use them"; the 29 September meeting called a review "done" that happens on
30 September; and the new starter guide was dated before MFA and the current password policy.
**Cause:** the brief's facts were checked against `truth.json` but not against the log and
against the brief's own dates. A writer copies such statements into documents, where they
would contradict the world the eval reads.
**Fix:** timeline and lockout corrected before the commit; remote access narrowed to internal
systems; "Granted to" explained as administrative access; the meeting now says the review is
booked; the guide moved to 2026-06-15; one consistent ATT&CK rule.
**Lesson:** every fact in a writer's brief is checked against the log and tables it describes,
and every dated statement against the other dates in the brief, before review.
**Evidence:** `logins.csv` rows for oliver.hayes on 2026-10-05; T15 review record
`.scratch/knowledge-base/reviews/15-code-review-2026-10-27.md`.

### B-084 · 2026-10-27 · Knowledge-base T17 · Duplicate section IDs silently overwrite evidence

**Symptom:** a corruption test gave one document two equally named sections. The first build
implementation reported success but kept only the later passage at their shared chunk ID.
**Cause:** the section-based ID recipe collided, and LangChain's insertion uses an upsert.
**Fix:** validate uniqueness of every chunk ID before any database or embedding work. Fail with
the colliding ID and require distinct source names. The original input is never rewritten.
**Lesson:** stable IDs need collision detection at ingestion, especially when a storage library
silently replaces existing rows.
**Evidence:** door-2 test `test_duplicate_chunk_addresses_fail_instead_of_overwriting_evidence`
first failed with DID NOT RAISE; retained as the regression test.

### B-085 · 2026-10-27 · Knowledge-base T17 · Incomplete embedding results reach storage

**Symptom:** a fake provider returning fewer vectors than passages caused a late foreign-key
failure when mention links were inserted. Passages with no mentions could instead be silently
omitted by the library's zip-based insertion.
**Cause:** the first implementation trusted the embedder's response cardinality.
**Fix:** validate the response before insertion: one vector per passage, the configured vector
length, and finite values. A mismatched response fails explicitly and is never published.
**Lesson:** validate external result sets before pairing them with source records.
**Evidence:** `test_incomplete_embedding_response_fails_instead_of_dropping_passages`.

### B-086 · 2026-10-27 · Knowledge-base T17 · New embedding factory bypassed the test key guard

**Symptom:** the no-real-keys test could construct an embedding client from the local `.env`.
The regression test made no request and printed no key.
**Cause:** the existing guard patched the chat factory's `load_dotenv`, while the new factory uses
`dotenv_values` to avoid putting credentials in the environment.
**Fix:** extend the session-wide guard to the embedding factory's file reader. Tests may inject
fake values; the default factory fails for a missing key in pytest. Reader password repr and
environment protection are checked separately.
**Lesson:** every credential-reading entry point must join the test guard.
**Evidence:** `test_embedding_factory_cannot_load_a_real_key_in_tests` first failed with DID NOT
RAISE and passes after the guard extension.

### B-087 · 2026-10-27 · Knowledge-base T17 · Malformed local build state was checked too late

**Symptom:** replacing the local state object with a JSON list still started an embedding call.
Reading the prior database name only after publication could then fail after the pointer changed.
**Cause:** syntactically valid JSON was assumed to have the expected object shape.
**Fix:** validate the object and prior database name before creating a database or calling the
embedder; prepare the return value before the atomic pointer replacement.
**Lesson:** validate local control files before starting work, not only when consuming a field.
**Evidence:** `test_invalid_publication_state_does_not_start_a_build` first reached the refusing
fake embedder, then passed after validation moved ahead of the build.

### B-088 · 2026-10-27 · Knowledge-base T17 · Markdown heading ancestry and fenced code

**Symptom:** the spec review found that H1 followed by two H3 siblings incorrectly nested the
second under the first. A shell comment beginning `#` inside a fenced block became a heading.
**Cause:** ancestry was based on list position rather than actual heading depth, and fenced
blocks were not tracked. The delivered corpus did not exercise these cases.
**Fix:** track heading depths and backtick/tilde fences. A door-2 regression checks exact IDs,
context headers and command text through the built database. The standards review also led to
an independent expected-text cleaning example and an isolated near-match mention test.
**Lesson:** preserve document structure before applying size limits; test both text preservation
and the absence of unwanted matches with independent expected values.
**Evidence:** `test_skipped_heading_levels_and_fenced_commands_keep_their_context` failed with
the extra heading and wrong ancestry before the fix; review record under the T17 review folder.

### B-089 · 2026-10-28 · Knowledge-base T18 · A leak test demanded suppression where nothing was chained

**Symptom:** the first run of `test_a_stale_knowledge_base_stops_the_server_before_anything_starts`
failed on `__suppress_context__` being false, although the guard's message was correct.
**Cause:** the test, not the guard. The stale refusal is raised outside any error handler, so it
has no earlier error to suppress and Python leaves the flag false. The test had copied the
assertion that fits the database-error path, where an earlier error does exist.
**Fix:** the stale test now asserts that no earlier error travels with the refusal (no cause, and
no context unless suppressed). The cannot-be-checked test keeps the strict assertion, because there
the database's own error, which names the database, really is present and must be suppressed.
**Lesson:** a leak assertion must match how the error is raised. Assert the property that matters
(nothing earlier is attached), not one mechanism that achieves it.
**Evidence:** first run failed with `assert (None is None and False)`; both tests pass after the
fix. A deliberate break of the stale comparison then failed both stale tests, door 2 and door 4.

### B-091 · 2026-10-28 · T19 discussion · VPN address meaning lacks an explicit observation point

**Symptom:** T19 discussion treated the synthetic VPN pool as public exit addresses, while the
remote-access policy describes addresses assigned to sessions and reused over time. The graph's
shared-address evidence can therefore be interpreted more strongly than the data supports.
**Cause:** the generator writes `VPN_POOL` values into the single `source_ip` field without an
explicit observation point, original client address, or VPN allocation interval. Pool values are
synthetic documentation addresses, not evidence that they represent public exits.
**Fix:** pending the author's ruling. Corrected the chat explanation; no dataset or spec changed.
**Lesson:** define what an address field observes before assigning security meaning to a match.
**Evidence:** `generator.py` VPN row generation; `org/networks.csv`; `pol-remote-access.md`,
Addresses and attribution. Tracked as AUD-060.

### B-090 · 2026-10-28 · Knowledge-base T18 · The live build predates the guard and stops the server

**Symptom:** after T18, `uv run uvicorn api.app:create_app --factory` on this machine exits with
code 3: "The knowledge base named by the last build cannot be checked."
**Cause:** expected, not a defect. The live build `li_kb_0af9160cc4ed` was made by T17, before
builds recorded a fingerprint. By decision 2, a build that cannot be checked stops the server.
**Fix:** one rebuild with the build command, which writes the fingerprint record. Pending the
author's go, because it makes paid embedding calls (T17's build cost $0.00111362). Done the same
day on the author's go: `li_kb_f9d6bcf6f8c5`, $0.00111362, after which the real server started.
**Lesson:** a new fail-closed guard turns every artefact made before it into a refusal. Plan the
one-time rebuild as part of the change.
**Evidence:** the real server's output saved during T18 shows the fixed text and exit code 3, with
no database name, error chain or password; its only paths are Python's traceback frames.

### B-092 · 2026-10-28 · Knowledge-base T19 · S6 answer key omitted office-address context

**Symptom:** the first independent radius test returned 43 distinct address peers instead of the
key's ten VPN peers. The office and VPN groups overlap.
**Cause:** T12 planted expected network paths only from the VPN allocation plan, although the
spec's graph includes every registered address and Amelia also uses the UK office address.
**Fix:** author approved all matches grouped by address. The generator and answer key now keep
43 office matches and the original ten VPN matches separately as supporting context, outside
exposure counts. Door 2 compares every group's exact identities and paths.
**Lesson:** a hand-planted answer key must include ordinary background relationships, not only
new story rows. An independent graph calculation can expose omissions in the key itself.
**Evidence:** first radius test failed with 43 actual accounts versus ten expected; T19 decision 5
records the author's explicit ruling. Final verification belongs to T19's closure record.

### B-093 · 2026-10-28 · Knowledge-base T19 · Answer-key byte order and coverage test corrections

**Symptom:** the generator reproducibility test rejected the edited truth file; the date test
incorrectly expected the last log row on 7 October rather than 8 October at 08:59:48 UTC.
**Cause:** the first key edit preserved a different JSON field order from the generator. The
coverage test assumed calendar dates instead of reading the existing capture boundary.
**Fix:** regenerate truth.json from the generator; use the actual independent capture endpoint
in the coverage assertion. Pandas timestamp type ambiguities also needed explicit type casts.
**Lesson:** generated evidence must be written by its source; an expected date needs evidence.
**Evidence:** focused generator and graph runs exposed both assertions before closure.

### B-094 · 2026-10-28 · Knowledge-base T19 · Test database teardown permission failure

**Symptom:** 23 graph assertions passed, but one fixture teardown failed when dropping its
fresh test database with FORCE. PostgreSQL reported insufficient permission to terminate a
process. The other databases in that run were cleaned up.
**Cause:** the existing cleanup role cannot terminate every possible backend role. Which
connection triggered this occurrence was not captured; no cause beyond that is established.
**Fix:** no fixture or database privileges changed in T19. Retry cleanup of the exact database
created by this run, then rerun focused tests. Follow-up tracked as AUD-061 for T44.
**Lesson:** distinguish an assertion failure from cleanup failure, and retain enough safe
connection metadata to diagnose intermittent teardown problems.
**Evidence:** test_integrity_rejects_corruption[asset_id] teardown, first corruption run:
23 passed, 1 error; InsufficientPrivilege, permission denied to terminate process.

**T48 full safety-net recurrence, 30 October 2026:** 709 passed, one teardown error in unchanged
`test_integrity_rejects_corruption[extra]`, 1186.38 seconds, exit 1. PgAdmin was closed for this
run, so that does not explain every occurrence. Exact leftover `li_test_b94165a0c68e` was
verified idle and dropped without FORCE. The affected test then passed in 2.58 seconds with
successful cleanup. No privilege or fixture change; AUD-061 remains open for T44.

**T22 recurrence, 29 October 2026:** the focused search/runner/results run reports 21 passed,
1 teardown error after `test_search_combines_ranks_and_keeps_raw_scores`. The same
InsufficientPrivilege occurs while dropping `li_test_e58b4bd62629`. No assertion failed and no
permissions were broadened. Retry cleanup of this exact test database, then verify the suite.

**T22 full safety-net recurrence:** 646 tests passed in 559.22 seconds, with one teardown error
in the unchanged `test_successful_observations_make_peers_but_failures_and_empty_devices_do_not`.
The exact leftover database was `li_test_7115528f2122`; the same InsufficientPrivilege was
reported. Cleanup and a focused rerun are recorded with the final T22 evidence. This is a
cleanup error, not an assertion failure, and the full command exited 1.
Exact cleanup succeeded. The affected graph test reran with 1 passed in 2.16 seconds, exit 0,
including teardown. The fixture concern remains open for T44.

**T24 recurrence, 29 October 2026:** full backend run passed 677 assertions, with two teardown
errors in `test_numbered_runbook_steps_survive_whole` and
`test_open_graph_refuses_a_dataset_changed_since_build`, exit 1. Leftovers were
`li_test_06f7a2ac8597` and `li_test_c36803010095`. Both were checked for attached sessions
(zero), then dropped without FORCE. The two affected tests reran clean: 2 passed in 2.76 seconds,
exit 0. No fixture code or database privileges changed. AUD-061 stays open for T44.

### B-095 · 2026-10-28 · Knowledge-base T19 · Empty requested period reported inverted bounds

**Symptom:** an end-only request before the first login returned an effective start after its
end. No peers were returned, but the coverage metadata was misleading.
**Cause:** omitted bounds defaulted to log bounds without intersecting the requested interval
with the available records for reporting.
**Fix:** preserve the requested bounds, report the intersection as the effective period, or
null bounds when there is no overlap. Query filtering still uses the requested/default bounds.
**Lesson:** absence of evidence needs a valid representation, not just an empty result list.
**Evidence:** the door-2 date test failed on non-null effective bounds for a September end date;
its final passing result is recorded with T19's verification.

### B-076 recurrence · 2026-10-28 · Knowledge-base T19 safety net

**Symptom:** Q02 runs 2 and 3 omit an explicit statement that the original S2 spray had no
successful sign-ins. Both correctly report S6's three successful sign-ins to Amelia and flag
possible compromise. Q02 is 1/3; the full gate passes 61/63 overall and 15/15 security.
**Cause:** unchanged model behaviour sampled again, fingerprint b70d0745. This occurrence is
an omitted S2 outcome, not the S6 zero-success claim recorded during T14. The check label
"says no attempt succeeded" refers to S2; it does not mean the answer incorrectly denied S6.
**Fix:** none in T19; preserve the failures and keep behaviour work under AUD-047. No rerun
for a cleaner score and no prompt, model or grader changes.
**Lesson:** distinguish which source's outcome was omitted before describing an eval failure.
**Evidence:** `backend/evals/results/2026-10-28-121053-b70d0745.json`, Q02 runs 2 and 3.

**T19 final verification, 28 October 2026:** B-091's meaning is agreed and AUD-060 closed;
B-092/B-093's generated key and exact graph comparisons pass. B-095's out-of-coverage date
check passes. B-094's exact leftover test database was removed by retry; the focused rerun
and final 612-test backend suite had no teardown failure. No cleanup privilege was broadened;
AUD-061 remains for T44. Frontend 149 passed; type checks clean; six existing AUD-009 warnings.

### B-096 · 2026-10-28 · Knowledge-base T20 · An export inside the dataset folder made the build stale

**Symptom:** the export script's test wrote its first file, then the second run refused with the
staleness text ("built from older files or settings") instead of the unknown-finding text.
**Cause:** the test's dataset folder was its temporary folder, so the GEXF file and its folder
landed inside the dataset. The staleness guard fingerprints every non-hidden file there, so the
new file changed the fingerprint. An author writing the export into
`backend/data/datasets/default/` would make the next app startup refuse in the same way.
**Fix:** the core export refuses an output path inside the opened dataset folder with
`ExportRefused`, before any file is written; the test's dataset moved to its own subfolder and
asserts the refusal leaves no file and a later export still succeeds.
**Lesson:** any tool that writes files must know which folders are fingerprinted inputs. Writing
next to the data is a write into the data.
**Evidence:** first run of `tests/test_graph_export.py`, 8 passed and 1 failed on the stale
text; rerun 9 passed.

### B-097 · 2026-10-28 · Knowledge-base T20 · Gephi Lite showed every node grey

**Symptom:** the author opened the S6 neighbourhood file in Gephi Lite. Every node was grey,
although the file carried a `viz:color` per node type.
**Cause:** NetworkX 3.6.1 writes GEXF 1.2 colours with an alpha value (`a="1.0"`) in every case,
and Gephi Lite ignores any `viz:color` that carries one. This is Gephi Lite's open issue #307,
which names NetworkX's `write_gexf` output. Gephi desktop reads the same file correctly. The
tests passed because NetworkX's own reader accepts the alpha; they proved the file, not the
viewer.
**Fix:** reproduced first: a copy of the file with the alpha removed showed the colours in the
author's Gephi Lite. `write_gexf` in `knowledge_base/gexf.py` now runs NetworkX's own three
writer steps and removes the alpha between them. The whole-graph test asserts every colour
element has exactly `r`, `g` and `b`. The regenerated S6 file is byte-identical to the copy the
author tested.
**Lesson:** a round trip through the library that wrote a file proves the file, not that the
target viewer reads it. When a viewer is the requirement, its look is the evidence.
**Evidence:** red run (alpha present) then 10 passed in `tests/test_graph_export.py`; the
author's Gephi Lite look before and after the alpha was removed, 28 October 2026.

### B-098 · 2026-10-29 · Knowledge-base T22 · K04 misses the MFA exception passage

**Symptom:** the first real retrieval run passes K01, K02, K03, K07 and K08. K04 finds the
password-spray runbook at rank 9 and passes both graph checks, but misses
`reg-mfa-exceptions@1.6#mfa-exception-register/active-exceptions/1` from the fused top 20.
**Cause:** a separate exact dense search across all 320 chunks puts the missing passage at rank
115 (cosine distance 0.5381994832). The full compound question's `plainto_tsquery` joins its
terms with AND, including `45.148.10.80`, `amelia.ward`, spray, reach and MFA. No passage matches
every term, so the keyword leg supplies zero candidates. Fusion therefore cannot recover the
missing register. The same passage is found by K02, so it exists and is searchable.
**Fix:** unresolved retrieval-quality gap, registered as AUD-062. T22 explicitly permits logging
a first-run miss with its cause. No gold, question, corpus, limit or query was changed to make
the exam pass. A later re-ranker alone cannot recover a passage outside both candidate lists.
**Lesson:** a compound investigation question may require more than a single whole-question
search. Measure candidate coverage before re-ranking or answer generation.
**Evidence:** `backend/evals/results/2026-10-29-102711-909238-retrieval-0180733adbd4.json`;
read-only diagnostic: runbook rank 9, distance 0.3857340674; register rank 115; 36 embedding
tokens, $0.00000072. Diagnostic used the same question and the same store, with k=320 only to
locate the miss; production limits remain 20 plus 20.

**Diagnostic iteration, 29 October 2026:** the isolated
[fixed-budget experiment](../.scratch/knowledge-base/research/22-retrieval-experiment-results.md)
recovers both gold passages with focused queries (register rank 16, runbook 4). Adding the
original broad query through equal-weight cross-query RRF pushes the register to rank 25 and
out of the final twenty. Repeated spray passages gain contributions from multiple routes;
the register initially has only one route. This is an experimental merge regression, not a
new application policy. One prewritten human-triggered retry restores register rank 4 and
runbook rank 3. No automatic missing-evidence detector was tested. The original bug stays
unfixed; the additional lesson is to measure coverage after merging as well as candidate
recovery before it. No query, gold or merge rule was changed after observing the results.

**Second diagnostic, 29 October 2026:** a separately recorded
[offline selector replay](../.scratch/knowledge-base/research/22-evidence-checklist-design.md)
uses the same saved initial queries. Equal turns retain K04's register at 19 and runbook at 2,
without recovery, but the result fails in two of six route orders and at a five-passage stress
cap. This confirms that available evidence can be recovered by selection, while showing that
simple fair allocation is fragile. No semantic support check or actual reranker was tested;
no production fix is claimed. Both experiments and their failures remain recorded.

### B-099 · 2026-10-29 · Knowledge-base T22 · Absent-topic verdicts remain uncalibrated

**Symptom:** K05 and K06 expect `none` but return `weak` with `not_calibrated`.
**Cause:** the agreed T22 interim policy leaves the `none` rule disabled until T39 calibration.
**Fix:** intentionally deferred to T39. Both misses remain visible in the saved result and the
command's nonzero exit status. This is not evidence that the absent topics exist in the corpus.
**Lesson:** an unfinished refusal mechanism must not make absent-topic questions silently pass.
**Evidence:** the same first live retrieval result as B-098; author confirmed the interim policy
on 29 October 2026. Seven query embeddings cost $0.00000276 for the complete run.

### B-100 · 2026-10-29 · Knowledge-base T22 · Retrieval command hides safe setup guidance

**Symptom:** a stale build produced only `Retrieval failed (KnowledgeBaseNotReady)`, losing
the guard's rebuild command promised by the admin manual.
**Cause:** the generic exception handler caught the guard's RuntimeError subclass. Review also
found duplicated configuration literals that could drift from search, and the retrieval wrapper
recorded completion time as start time; its source paths were absent from the dirty marker.
**Fix:** preserve known safe setup/staleness messages, derive recorded settings from the search
constants and policy, capture start time before retrieval, and include retrieval sources in
version/dirty evidence. Unexpected provider/database error text remains hidden.
**Lesson:** saved evidence must describe the executed configuration, and safe actionable error
messages should survive the command boundary.
**Evidence:** standards review, plus the real-database stale-build regression failed with the
generic message before the fix. Verification recorded in the T22 review note.

### B-101 · 2026-10-29 · Knowledge-base T23 · The new re-ranker factory could read the real key in tests

**Symptom:** a new no-real-keys test, `reranker_service` switched on with no key in its environment,
failed: the factory found an OpenRouter key and opened its client. The key was never printed, sent
or stored, and no call was made; the factory was minutes old and not yet committed.
**Cause:** the test run's guard (`backend/conftest.py`, ticket 24) blanks `.env` reading per module.
It covered `embedding.dotenv_values` only, so a new module reading `.env` through its own import
reached the real file. The default `.env` path was also bound as a default argument, out of a
guard's reach.
**Fix:** `reranking` reads its default `.env` path at call time, and the guard points
`reranking.ENV_PATH` at a file that does not exist. The re-ranker's own tests pass their `.env`
files explicitly. The no-real-keys test now covers the re-ranker factory.
**Lesson:** a per-module key guard silently misses the next module. Every new reader of `.env`
gets a no-real-keys test in the same change; the test caught this one before commit.
**Evidence:** `tests/test_no_real_keys.py::test_reranker_factory_cannot_load_a_real_key_in_tests`
failed before the fix and passed after, with `tests/test_reranking.py` (18 passed together).

### B-102 · 2026-10-29 · Knowledge-base T24 · Startup failure left SQLite memory open

**Symptom:** the new door-4 failure test could still query memory after agent construction raised.
**Cause:** `services.start` opened memory before building the agent, but only normal shutdown
closed it. A failed start never returned the Services that shutdown needed.
**Fix:** an ExitStack owns startup resources until successful construction transfers them to
`stop`; the application lifespan also closes the knowledge-base context on startup failure.
**Lesson:** resources acquired before startup finishes need a failure cleanup owner.
**Evidence:** `test_startup_failure_closes_memory_and_the_knowledge_base` failed before the fix;
the subsequent 48-test focused run passed, including that failure path and report download.

### B-103 · 2026-10-29 · Knowledge-base T24 · Lookup test assumed a privileged membership

**Symptom:** the first lookup test expected Thomas Price to belong to IT Admins; the real graph
returned All Staff only.
**Cause:** the test inferred privilege from department instead of reading the source membership.
**Fix:** corrected the expectation from `org/memberships.csv`; privileged-path tests use Amelia
Ward, whose source membership explicitly names IT Admins. No dataset or lookup logic changed.
**Lesson:** department and privilege are separate facts; test expectations need independent data.
**Evidence:** corrected lookup and artifact-boundary tests pass in the focused agent run.

### B-104 · 2026-10-29 · Knowledge-base T24 · Browser rejected the new lookup progress event

**Symptom:** the fake-API screen test for `lookup_account` ended the stream instead of displaying
progress and the saved answer. Its saved tool result also fell through to the old unknown-tool view.
**Cause:** the Port's stream parser allows only its original three tool names; widened names
were scheduled for T36 while T24 already registers and emits the first new tool.
**Fix:** author approved moving this one name forward. Added the existing-line phrase and the
Account context result label; full evidence and the step stack remain later work.
**Lesson:** a new tool's end-to-end contract includes the client event-name allowlist.
**Evidence:** `create then ask streams lookup_account and redraws saved memory` reproduced the
failure before the compatibility change; passing rerun recorded in T24 evidence.

### B-105 · 2026-10-29 · Knowledge-base T24 · Q04's flag check misses a long structured answer

**Symptom:** Q04 run 1 failed only “flags amelia.ward as possibly compromised (S6)”. The answer
introduced accounts that “may have been compromised”, listed Amelia with three successful
sign-ins, and recommended securing her account. All required searches and reputation calls ran.
**Cause:** observed mismatch with the grader's same-line proximity and restricted-list patterns;
whether the broader contextual attribution is sufficient remains a review decision.
**Fix:** not implemented. Recorded AUD-066 for later review; original score preserved.
**Lesson:** distinguish missing facts from attribution checks that cannot recognise an answer's
structure; do not widen the grader merely to obtain a passing run.
**Evidence:** `2026-10-29-204751-654728-fa8f3e8f.json`, Q04 run 1. Overall 62/63 and security
15/15 meet the agreed gates. Related earlier limitation: B-078.

**T49 recurrence, 1 November 2026:** the approved live migration evaluation
`2026-11-01-104006-806272-13987838.json` passes 60/63 overall and 15/15 security.
All three Q04 repetitions fail Amelia compromise attribution. S6 success facts are present in
all answers. Run 1 uses broad introductory attribution and recommends securing Amelia;
run 2 recommends action only for other accounts; run 3 recommends only monitoring Amelia.
These failures must not all be dismissed as formatting. Keep the scores and AUD-066 open
for a separate substantive answer/grader review. No prompt, check or threshold changed.

### B-106 · 2026-10-30 · T24 GUI review · Account JSON displayed as one compact line

**Symptom:** the author saw compact JSON under Found and requested readable indentation there
and in Show raw JSON.
**Cause:** T24's labelled briefing bypassed the existing generic JSON pretty-printer.
**First iteration:** the account display adapter separates the label from its JSON, indents the JSON by two
spaces, retains the label under Found and supplies JSON alone to the raw view. Plain-text
unavailable/not-found results remain readable. Existing saved briefings are formatted on read.
**Author review:** indented raw JSON accepted; JSON under Found rejected as visually awkward.
**Final fix:** Found becomes a plain Owner/Department/Groups summary with readable access labels.
The raw switch retains two-space JSON indentation. No stored messages or model input change.
**Lesson:** a labelled tool briefing needs its JSON portion formatted separately for display.
**Evidence:** existing tool-view/API tests and a live reopened investigation check, recorded in
the T24 follow-up. No model prompt or stored evidence change.
Final evidence: 677 backend tests passed with no cleanup error in this run; 150 frontend tests
passed; final affected-tool/API rerun 13 passed; two existing saved lookup displays verified
through the live API; both review axes cleared. The original UI iteration remains recorded above.

### B-107 · 2026-10-30 · T46 research · External probe could not import the backend

**Symptom:** the first parity-probe invocation stopped with `ModuleNotFoundError` for
`login_investigator`, before creating databases or containers.
**Cause:** `uv --project backend` selects dependencies but does not install this non-packaged
project or add its directory to an external script's import path.
**Fix:** the disposable script explicitly adds the repository's backend directory before imports.
**Lesson:** test a research command from its documented working directory; environment selection
does not imply local-package importability.
**Evidence:** initial invocation failed at import. Corrected run `ff605c4bbc` completed all 38
named checks and cleaned its resources; results under the T46 research directory. The later
`ac601a07d9` exception was deliberate failure injection and verified cleanup, not a recurrence.

### B-108 · 2026-10-30 · T47 · Type-check invocation used the repository root

**Symptom:** the first type check reported 59 errors outside the configured backend scope.
**Cause:** `uv --project backend` selected the environment but did not change the tool's working directory.
**Fix:** run `uv run pyright` from `backend/`.
**Lesson:** environment selection and tool configuration discovery are separate.
**Evidence:** the corrected invocation passed with zero errors before the Neo4j modules were added.

### B-109 · 2026-10-30 · T47 · Query typing edit broke import syntax

**Symptom:** the graph-version test could not collect because the importer had a syntax error.
**Cause:** adding `LiteralString` typing changed an adjacent string literal into a function call without an explicit concatenation operator.
**Fix:** add the explicit concatenation; keep all relationship names restricted to code-owned values.
**Lesson:** run a syntax check immediately after changing query construction.
**Evidence:** failed collection retained in the session; corrected focused suite passed 7/7 and
final backend suite passed 686/686 under T47.

### B-110 · 2026-10-30 · T47 · Restart check retained an obsolete Docker port

**Symptom:** the expanded graph-version test timed out waiting for the serving graph after restart.
Four other focused tests passed, including corruption refusal and the device witness.
**Cause:** the service uses a dynamically allocated localhost port. The restart path reused the
pre-restart connection address rather than reading Docker's current binding.
**Fix:** resolve the serving address again after restart before checking readiness and protection.
**Lesson:** resource identity survives restart; a dynamically assigned network address need not.
**Evidence:** failed focused run: 1 failed, 4 passed in 332.17 seconds. Corrected command passed, and final backend suite passed 686/686 under T47.

### B-111 · 2026-10-30 · T47 review · Cancellation and partial Docker failure could escape cleanup

**Symptom:** review found that a cancelled worker could finish creating a resource after cleanup,
and a failed Docker command could leave an unrecorded container. Cleanup also removed recovery state
when resource deletion failed.
**Cause:** cancellation did not join the resource-owning thread; ownership was recorded only after
command success; nested finally blocks always removed the version directory.
**Fix:** await resource-owning workers before cancellation cleanup, reconcile unique ownership labels,
and retain credential-free cleanup instructions and private state if disposal is incomplete.
**Lesson:** cleanup must follow confirmed resource ownership, including ambiguous external outcomes.
**Evidence:** independent standards and spec review findings; failure-injection checks recorded in T47.

### B-112 · 2026-10-30 · T47 review · Build ignored the configured PostgreSQL reader

**Symptom:** an alternate reader could receive only the pair-table grant while the default role
received the main build grants. Completion could be written before opening the configured reader.
**Cause:** the new build path omitted the existing builder's reader_role argument.
**Fix:** resolve one reader, pass its role into preparation, and verify graph sources through that
reader before writing the completion marker.
**Lesson:** access configuration must travel through the entire build and verification path.
**Evidence:** spec-review finding and corrected reader-based verification before publication.

### B-113 · 2026-10-30 · T47 safety net · Existing Explorer interaction timed out

**Symptom:** the frontend suite returned 149 passes and one failure at
`explorer.test.tsx:80`, the valid-IP submission and Reset interaction, after its five-second limit.
**Cause:** not established. No frontend code changed; the run overlapped Neo4j integration startup.
**Fix:** no application or timeout change. Rerun the affected file separately and retain both results.
**Lesson:** a timeout is evidence to investigate, not permission to relax the test's limit.
**Evidence:** initial frontend run took 54.49 seconds. The affected-file rerun passed 8/8 in
30.53 seconds without changes; retained as AUD-069 for recurrence monitoring.
T48 recurrence: the same unchanged test timed out again at five seconds; 149 passed and one
failed in 50.20 seconds while other validation was active. No frontend code or timeout changed.
The separate full T48 rerun passed all 150 tests in 28.27 seconds without changes.
T49 recurrence, 1 November: 149 passed and the same test timed out at five seconds in a
49.95-second full run. Frontend type checking ran concurrently; no Neo4j build was running.
No frontend code or timeout changed. The separate affected file passed all eight tests in
22.60 seconds. The full run and passing rerun remain separate evidence.


### B-114 · 2026-10-30 · T48 integration · Graph verification blocked the event loop

**Symptom:** the startup integration test detected synchronous Neo4j network calls on the
asynchronous application's event-loop thread.
**Cause:** T47's independent verifier called the synchronous driver directly; T48's application
integration makes that boundary consequential.
**Fix:** dispatch verification reads to resource-owning workers, joining them on cancellation
before connection cleanup. Serving-protection checks and driver shutdown use the same rule.
**Lesson:** an async function can still block if a synchronous dependency performs network work.
**Evidence:** `test_startup_graph_reads_do_not_block_the_event_loop` failed at the first integrity
query before the fix. The subsequent focused run is recorded in T48.

### B-115 · 2026-10-30 · T48 test development · Incomplete test observation and type narrowing

**Symptom:** type checking rejected indexing an account typed as `object`; the first paired
update test then expected `/api/dataset` metadata to change after removing ten login rows.
**Cause:** the test omitted dictionary narrowing and observed date metadata rather than login
counts. Removing interior rows did not change the dataset's first/last dates.
**Fix:** assert the account is a dictionary and compare the overview response, which reports
the changed login counts. Keep the independent department and retrieved-text checks.
**Lesson:** observe the public behaviour that actually changes; an unchanged metadata response
does not establish stale data.
**Evidence:** initial Pyright reported one error; corrected typecheck passed. First lifecycle
run reported four passes and the metadata-comparison failure. Corrected rerun is recorded in T48.
The broader run later found that byte-identical PDF assertions also compared generation metadata.
The test now preserves the original report JSON and artifact exactly and verifies successful
PDF downloads; existing PDF-content tests remain in the safety net. That run recorded 77 passes,
one PDF comparison failure and one recurrence of B-094's unrelated teardown privilege error.

### B-116 · 2026-10-30 · T48 integration · Paired PostgreSQL reads had no statement bound

**Symptom:** the paired-reader timeout test observed `statement_timeout=0`, allowing indefinite
statement waits even though Neo4j calls had explicit limits.
**Cause:** the paired opener reused the builder's general engine settings.
**Fix:** paired readers use bounded connection/pool, lock and statement waits. Builder settings
remain unchanged. Add a real slow-statement refusal check.
**Lesson:** bounds must cover every store participating in an investigation.
**Evidence:** focused failure/cancellation/concurrency run: seven passed, one failed on the zero
statement limit. Corrected rerun is recorded in T48.

### B-117 · 2026-10-30 · T48 review · Graph shutdown failure skipped PostgreSQL disposal

**Symptom:** both review axes found that a graph close error or cancellation could skip the
following pool disposal. The failure-injection test observed one remaining PostgreSQL connection.
**Cause:** sequential cleanup without an independent finally for the second resource.
**Fix:** dispose the PostgreSQL engine in an unconditional nested finally. Test driver-close
failure and cancellation after the persistent graph driver has opened.
**Lesson:** each owned resource needs a cleanup path that another cleanup failure cannot bypass.
**Evidence:** initial shutdown test failed with one remaining connection and retained its exact
version recovery state after teardown. Corrected rerun and explicit recovery are recorded in T48.

### B-118 · 2026-10-30 · T48 review · Evaluations reused the application's selected stores

**Symptom:** the spec review found that retrieval/API evaluation entry points created fresh memory
but still read the selected application databases.
**Cause:** the old evaluation harness did not own a complete paired-version lifecycle.
**Fix:** prepare unique source/store/state resources per evaluation, reuse only exact unchanged
passage vectors from the checked original build, and clean the evaluation's resources on exit.
No source changes or missing-vector fallback are accepted. Offline versions cannot become live
evaluation evidence.
**Lesson:** isolated memory is not isolated evaluation data when the system has several stores.
**Evidence:** initial isolation test reached the unimplemented preparation path; new lifecycle and
entry-point checks are recorded in T48.
The follow-up review found that the no-build branch still exposed the working selection path.
A test publishing to that path during evaluation failed by trying to read database settings.
The branch now owns a private absent pointer, so a new application build cannot enter that run.

### B-119 · 2026-10-30 · T48 native inspection · Missing local Neo4j image

**Symptom:** the native inspection integration test and isolated walkthrough build failed before
Neo4j creation with `GraphUnavailable`. Docker inspection confirmed the pinned image absent.
**Cause:** local Docker no longer contained `neo4j:2026.10.1`; why it was removed is unknown.
**Fix:** restore the pinned image with the documented Docker pull, then rerun. Temporary build
resources followed the existing failure cleanup.
**Lesson:** a prior handoff's runtime availability must be checked in the new session.
**Evidence:** initial native inspection run: one failure in 5.00 seconds. Recovery pending.

### B-120 · 2026-10-30 · T48 inspection test · Default data did not exercise device peers

**Symptom:** exact query/core comparisons passed for every default finding, but the test's
coverage assertion failed because no default finding has device peers.
**Cause:** the test assumed the baseline dataset contained a peer case.
**Fix:** plant a successful shared-device observation in a disposable source copy before building
its test pair. Keep the real dataset and walkthrough pair unchanged.
**Lesson:** assert that edge-case fixtures actually exercise the branch being verified.
**Evidence:** first restored-image run failed its coverage assertion in 85.32 seconds, with clean
resource teardown. Corrected rerun pending.

### B-121 · 2026-10-30 · T48 manual validation · Wrong relative version path

**Symptom:** the first inspection preparation command failed with FileNotFoundError.
**Cause:** draft instructions used a repository-root version path, but `uv --directory backend`
changes the working directory and the builder stores pairs under `backend/.graph-versions`.
**Fix:** use `.graph-versions/BUILD_ID/complete.json` relative to backend; correct the manual and
rerun the exact command.
**Lesson:** test operator commands with their documented working-directory semantics.
**Evidence:** first command refused without changing the application selection; corrected run pending.

### B-122 · 2026-10-30 · T48 Browser verification · Current UI rejects documented config command

**Symptom:** the Neo4j 2026.10.1 bundled Browser returns UnknownCommandError for `:config`.
**Cause:** the bundled Query/Browser interface differs from the documented Browser settings
interface. Reading documentation did not establish runtime support.
**Fix:** verify supported Settings controls in the live interface and replace the draft manual's
`:config` instructions. Check parameter and styling commands in that same runtime.
**Lesson:** an operator walkthrough must be tested against the shipped interface.
**Evidence:** authenticated Browser response explicitly says `:config` is not currently available.

### B-123 · 2026-10-30 · T48 Browser verification · JSON map keys rejected by Browser

**Symptom:** the generated `:params` command failed with a Cypher syntax error on quoted map keys.
**Cause:** Browser evaluates the parameter map as Cypher; JSON object syntax is not interchangeable.
Driver parameter tests accepted the Python map and therefore did not exercise this command layer.
**Fix:** render fixed allowlisted map keys as Cypher identifiers while JSON-escaping all values.
Verify the generated command in Browser and evaluate its map in a real database test.
**Lesson:** test the operator's command representation as well as the underlying database query.
**Evidence:** authenticated Browser rejected the original organisation parameter file.

T48 checkpoint-3 follow-up: B-119 recovered after restoring the pinned image; B-120 corrected
fixture passed in the 11-test native/export run; B-121 corrected command produced the checked
bundle. B-122 Settings, GraSS preview/import and explicit label/type styles were verified in
Browser 2026.10.21. Generic style defaults were ignored by its importer and removed. B-123's
corrected parameter file executed successfully in Browser; its syntax regression passed.

### B-124 · 2026-10-31 · Import cleanup verification · Neo4j graph query unavailable

**Symptom:** the unrestricted backend regression run failed
`test_corrupt_graph_refused_and_successful_device_witness_preserved` when its device-peer
query raised `GraphUnavailable`. The run was interrupted for investigation after 373 passes
and this one failure. An earlier sandboxed run could not access local services and is not
evidence of the same defect.
**Cause:** unresolved. The query wrapper suppresses the underlying Neo4j/driver exception;
the observed fixed error does not establish a timeout, service outage or import-order cause.
**Fix:** none applied. The focused rerun failed in 133.99 seconds with
`Neo4j did not become ready within 120 seconds. Check Docker Desktop resources.` This
establishes a service-readiness problem in the rerun, not the cause of the original query
failure. Unrelated query/error-handling changes are outside the authorised import cleanup.
**Lesson:** an import-only structural comparison does not replace runtime checks, and a
generic service error must not be reported as a diagnosed timeout.
**Evidence:** `/tmp/login-import-cleanup-backend-access.log` and
`/tmp/login-import-cleanup-graph-rerun.log`; AUD-072 tracks the unresolved concern.

**31 October follow-up, requested by the author:** no application code, timeout or Docker
configuration change was needed to recover verification. A temporary diagnostic harness ran
the existing test without changing query or readiness behaviour: 1 passed in 35.77 seconds,
with two pytest import-rewrite warnings caused by pre-importing modules in that harness.
Readiness took 17.79 seconds; the container reported `OOMKilled=false`, 713.8 MiB memory,
and successful cleanup. These observations describe the passing run, not the earlier failure.
The uninstrumented focused command passed in 37.40 seconds. The full normal backend command,
`.venv/bin/python -m pytest -v --tb=short --durations=10` from `backend/` with local-service
access, passed all 701 tests in 957.38 seconds, including this test in 34.07 seconds. No failure
or teardown error occurred. Only the pre-existing retained inspection container remained;
no pytest process remained. The verification gap is resolved; AUD-072 remains open for the
intermittent failure's unproven cause.

Evidence: `/tmp/li-graph-diagnostic.log`, `/tmp/li-graph-focused-normal.log`,
`/tmp/li-graph-full-verification.log`. Diagnostic harness documentation: pytest 9.1.1;
Context Hub search did not return core invocation guidance, so official
[pytest invocation documentation](https://docs.pytest.org/en/stable/how-to/usage.html#calling-pytest-from-python-code)
was used for one `pytest.main` call with explicit arguments and its return code. Existing
T48 Neo4j driver/session documentation applies to the unchanged driver 6.1.0 calls.

### B-125 · 2026-10-31 · Ruff policy setup · Isolated suppression check removed valid exceptions

**Symptom:** running Ruff with only `RUF100` selected removed valid reviewed suppression
comments alongside genuinely stale fixture comments. The next full-policy lint check exposed
29 diagnostics, including the already-reviewed BLE001 handlers. No executable logic changed.
**Cause:** unused-suppression detection was run with the referenced rules disabled, so it
treated their suppressions as unnecessary in that restricted configuration.
**Fix:** restored the 12 previously approved BLE001 comments from the pre-edit snapshot,
restored the new specific exceptions and shared-fixture registration comment, and checked
the full agreed policy. The complete Ruff check passes. Documented the safe checking approach
in admin manual section 7; no runtime code or tests were altered to hide these diagnostics.
**Lesson:** evaluate suppression necessity against the policy it is intended to suppress,
not with a standalone unused-suppression rule.

### B-126 · 2026-11-01 · T49 recovery rehearsal · Archived baseline missed startup readiness

**Symptom:** the first recovery rehearsal did not reach application readiness within its
120-second harness deadline. No Uvicorn startup line appeared. The harness stopped its own
process and left the working pointer and memory unchanged. Two isolated evaluation builds
were running concurrently.
**Cause:** not yet established. A separate import-time diagnostic confirmed substantial time
inside dependency imports before application startup, including 17.4 seconds in the psycopg
binary import. This identifies the startup stage, not the reason for the delay.
**Fix:** pending diagnostic completion and a controlled rehearsal. No application, database or
Neo4j timeout has been increased. The failed log is retained at ignored
`backend/.graph-versions/t49-server-first-attempt.log`.
**Lesson:** measure the archived recovery environment itself. A preserved lockfile and source
archive do not prove that the recovery process starts within an assumed window.

**B-126 follow-up:** both environments imported successfully. The archived import took 92.431
seconds; the current import took 16.502 seconds. After evaluation processes exited, sequential
rehearsal started the archived application in 21.861 seconds and reopened saved evidence.
The harness ceiling was increased to 300 seconds solely to measure recovery; no application
or database timeout changed. The first failure remains a cold/concurrent-load observation.
Its underlying cause is unproven, and warm timings must not be advertised as upper bounds.

### B-127 · 2026-11-01 · T49 operator review · Replacement build command ignores dataset settings

**Symptom:** source review found `build_graph_version` defaults directly to the bundled dataset,
while the retiring build command honours `LI_DATASET_DIR`. A migration that simply removes the
old command would lose the existing operator's dataset-selection behavior.
**Cause:** the isolated graph command introduced its own argparse default instead of reading
the established environment and `.env` setting.
**Fix:** the replacement command now honours explicit option, environment, `.env`, then default.
The exact offline disposable manual command passed with a distinct source selected through the
environment. Its fingerprint matches that source and differs from the bundled source. Preparation
took 192.511 seconds; the command disposed its own pair and left the working pointer unchanged.
Evidence: `49-command-result.json`. No provider calls were made.
**Lesson:** retiring an operator command includes its configuration contract, not only its main
build operation. This follows the existing dataset-setting ruling; it does not reopen AUD-059's
separate application-wide cleanup.

### B-128 · 2026-11-01 · T49 standards review · Selection guide lost its working directory

**Symptom:** the standards reviewer found that following admin manual section 4 from the
repository root and then section 5 would run the selection command in the wrong directory.
**Cause:** the final procedure rewrite removed the explicit `backend/` working-directory line
along with an untested paid-build example.
**Fix:** restored the explicit directory instruction before selection and restart commands.
Final operator checks will use that directory and the documented arguments.
**Lesson:** each manual task must state its own working directory instead of inheriting an
unstated shell state from another task.

### B-129 · 2026-11-01 · T49 standards review · Public preparation evidence included home paths

**Symptom:** the reviewer found personal home-directory segments in the new preparation JSON.
**Cause:** the report reused the private version descriptor's absolute marker/snapshot paths.
**Fix:** publish backend-relative paths and resolve them inside the local rehearsal harness.
Private completion markers remain ignored and unchanged. The preparer now emits relative paths.
**Lesson:** credential-free operational metadata still needs a separate privacy check before
being added to a repository that may become public.

### B-130 · 2026-11-01 · T49 spec review · Operator guidance omitted paired lifecycle steps

**Symptom:** the no-build startup instruction named preparation without selection/restart;
the working-build guide did not explicitly omit its disposable flag; retrieval prerequisites
still described a PostgreSQL-only run without rebuilding.
**Cause:** replacing the builder preserved descriptions of its former publication behaviour,
while the new preparation command intentionally does not select the application.
**Fix:** name selection and restart in the fixed startup message, explicitly omit both offline
and disposal flags for a retained live build, and document the evaluator's isolated pair/source
copy and Docker prerequisite. Exact stored vectors avoid new document-embedding purchases.
**Lesson:** operator instructions must follow the complete lifecycle across command boundaries.


**B-130 follow-up:** the older storage-probe section also described PostgreSQL-only prerequisites
and restart without selecting the prepared pair. It now names Neo4j, complete selection and
immutable-snapshot checks. The probe itself already uses the public current-build seam.

### B-131 · 2026-11-01 · T49 focused verification · Serving restart missed readiness

**Symptom:** the first post-retirement focused run passed nine tests, including the expanded
independent corruption verifier, but seven tests failed during their shared paired fixture's
setup. The new serving instance did not become ready within the existing 120-second deadline.
**Cause:** unproven. The failed build cleaned its own resources before the suppressed driver
exception could be captured. The three retained containers used about 2.6 GiB of Docker's
7.75 GiB allocation after failure, which does not establish memory pressure.
**Follow-up:** a temporary external diagnostic captures the final driver class/code and
container state before cleanup on a recurrence. Only the setup-blocked focused group is being
retried. No production timeout or Docker setting changed. AUD-072 remains open.
**Lesson:** retain diagnostic evidence before automatic cleanup; a passing retry alone cannot
identify or close an intermittent service failure.


**B-131 follow-up:** the diagnostic retry passed all 15 focused tests in 265.92 seconds.
Both serving restarts completed within the unchanged deadlines. No diagnostic failure fired,
so the underlying first-run cause remains unknown. The expanded independent corruption test
already passed in the first run. The final complete-suite gate remains separate.

### B-132 · 2026-11-01 · T49 activation-harness review · Recovery validation happened too late

**Symptom:** the evidence-only activation harness first published the candidate pointer, then
validated that candidate. It checked the previous marker only by substring, and a shutdown
timeout could skip pointer restoration. No activation had run.
**Cause:** the one-time operator harness did not yet enforce every step of the accepted plan.
**Fix:** validate both exact marker paths, source directories and build identities through
`open_version` before publication, then recheck the original pointer hash. Bound shutdown with
a kill fallback and restore the original pointer in `finally`. The independent spec reviewer
verified both fixes with zero remaining findings before any working selection change.
**Lesson:** recovery preparation and failure cleanup are part of the activation transaction,
including in a one-time operational script.


### B-133 · 2026-11-01 · T49 full verification · Evaluation test still expected a legacy pointer

**Symptom:** the complete backend run produced 662 passes, one failure and one teardown error
in 874.12 seconds. The evaluation-isolation test read `pointer['database']`, which no longer
exists in a paired selection. It failed before exercising the evaluation copy.
**Cause:** the shared startup fixture was migrated, but this importing test retained both its
legacy-pointer assumption and its former one-passage source assumption.
**Fix:** give the test its own small complete paired source using the existing injected test
embedding provider. Read the original database from that verified version. Preserve the actual
clone, lookup/search, caller-failure cleanup, original-pointer preservation and resource-removal
assertions. The separate offline-mode refusal test stays unchanged. This fixture supplies no
live evaluation evidence and makes no paid calls. A targeted rerun is pending.
**Lesson:** migrating a shared fixture requires following its importers and data assumptions;
type checks alone cannot find a dictionary-shape mismatch.

The separate teardown error recurred under AUD-061. `test_privileged_reader_is_rejected_before_any_embedding_call`
passed, but forced deletion of its disposable database lacked permission to terminate a connection.
After the suite exited, that exact test database had zero connections and was removed without
forcing termination or changing privileges. The affected test is being rerun. No application
code or service limits were changed in response to these two findings.

**B-133 follow-up:** all three affected tests passed in 209.14 seconds. The corrected test
proved actual paired cloning, lookup/search, cleanup after caller failure and preservation of
the source selection. The privileged-reader test and teardown also passed. Both review axes
independently cleared the test-only correction; types pass. All test-created graph resources
are gone. The full run remains recorded as 662 passes, one fixed test failure and one recovered
teardown error; it is not described as a wholly clean full-suite run. AUD-061 remains open.


### B-134 · 2026-11-01 · T49 activation harness · Backend API import path was absent

**Symptom:** the first activation attempt stopped at its new effective-settings guard because
Python could not import `api.settings`. Selection had not changed and no server had started.
**Cause:** launching a research file makes the research directory Python's first import path;
the application command normally imports `api` from the backend working directory.
**Fix:** explicitly place the checked backend working directory on the one-time harness's import
path before importing application settings. The ordinary server command is unchanged.
**Lesson:** an operator harness must reproduce the application's import context as well as its
configuration. Keep the failed attempt distinct from actual activation evidence.

**B-134 follow-up:** both reviewers cleared the correction. The guarded retry activated the
accepted pair and passed readiness, current-version reader checks and exact reopening of all
25 original investigations. The first attempt remains a recorded failure before selection.


### B-135 · 2026-11-01 · T50 full verification · Docker-ownership test also lost its PostgreSQL cleanup

**Symptom:** in the full backend run after T50 (661 passed, 2 failed, 1033.30 seconds),
`test_unknown_docker_ownership_retains_recovery_state` expected `cleanup.json` to name only
`neo4j` as incomplete and found `['neo4j', 'postgresql']`. The simulated Docker loss worked as
designed; the forced drop of the disposable database `li_kb_6ccecd2520c4` failed as well. The
failing assertion stopped the test before its own disposal step, so the test's container
`li-graph-de432ffc826e4e4d80269da620ac2b62` (state Created), its volume and that database remain.
**Cause:** not captured. The error text of the drop is not kept in `cleanup.json`. The same
test passed alone 15 minutes later, so load during the full run or the AUD-061 termination
privilege are the candidates; neither is proven.
**Fix:** none to code in T50; the change under test does not touch this path. Affected rerun:
the test passed in isolation. The three leftover resources are listed for the author's cleanup
ruling, not removed by the builder (the manual forbids removing resources the run did not own).
**Lesson:** a cleanup record that lists what failed but not why cannot be diagnosed after the
fact; retaining the drop's error text in `cleanup.json` would make the next occurrence
diagnosable. A test that asserts before it disposes leaves debris on failure.
**Evidence:** full run log and isolated rerun (3 passed in 325.75 seconds) in the T50 session;
`docker ps -a` after both runs; database list through the project's PostgreSQL settings.

**B-135 follow-up, same day:** the author ruled to remove the debris and stop the retained
versions. Container `li-graph-de432ffc…`, its volume and database `li_kb_6ccecd2520c4` were
removed through Docker and the project's own `drop_database`. The retained pairs `3d58516c…`,
`eb6c7d59…` and the T48 inspection `05f15cfc…` were stopped with their volumes and databases
kept; only the working pair `f937ea59…` runs. Docker reported exit 137 for the three stops,
meaning Neo4j did not exit within Docker's grace period and was killed; their volumes are
intact and they start again with `docker start`. Correction: a database and a volume first
listed as unexplained (`li_kb_c38b82a72616`, `li-graph-4f085e16…-data`) belonged to the
isolated rerun, which was still running at the time, and it cleaned them up. One database,
`li_kb_0af9160cc4ed`, remains unaccounted for by any retained version; it predates T49 and
falls under AUD-057.


### B-136 · 2026-11-01 · T50 full verification · Concurrent investigations hit a locked SQLite memory

**Symptom:** `test_concurrent_investigations_keep_their_own_account_evidence` failed in the
same full run. Two investigations started in parallel against a fresh memory file; one stream
ended with `event: error` (`agent_failed`), and the captured log shows
`sqlite3.OperationalError: database is locked` raised inside the checkpointer's `setup()`
while it ran its table-creation script.
**Cause:** the first use of a new memory file creates the checkpointer's tables. Two threads
reached that step at once, and SQLite allowed only one writer. Why the second did not wait out
the lock (busy timeout) is not established; this is the first recorded occurrence.
**Fix:** none in T50; the agent, the memory and the API are unchanged by this ticket. The
test passed in isolation. Registered as AUD-075 so the next occurrence is recognised.
**Lesson:** a concurrency test on a brand-new store exercises first-use setup as well as the
behaviour under test. Separate the two, or make setup happen once before the threads start.
**Evidence:** full run log lines for the test, including the traceback through
`langgraph/checkpoint/sqlite/__init__.py setup()`; isolated rerun passed.
