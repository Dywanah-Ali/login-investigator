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
