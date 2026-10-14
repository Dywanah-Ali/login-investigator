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
**Cause:** the planning count, not the copy. v1 collects 290 tests. Its two screen test files hold
36 of them (18 each), which leaves 254. The 259 was never measured by running pytest.
**Fix:** none to the code. The evidence on ticket 10 names 254, and a spec correction is proposed to
the author, since spec changes go through the author. The same 259 appears in ticket 08, ticket 11
and the map, so the correction covers all four.
**Lesson:** a number that becomes an acceptance gate must come from running the tool, not from
counting by hand.
**Found by:** test run of the copied suite, checked against a collect-only run of a scratch copy of
v1. Related prompt: P-001.
