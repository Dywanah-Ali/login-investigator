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
