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
