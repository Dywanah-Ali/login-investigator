# 11: Core: the logic that moved from the screens

**What to build:** the four pieces of meaning that v1 kept in its Streamlit layer now live in the
core, so the API, the screens and the agent tools can never disagree. Each has a pytest adapted from
the old screen test that covered it.

**Blocked by:** 10 (Repository foundation).

**Status:** resolved

Spec: [spec.md](../spec.md), "Where logic lives". Decisions: ticket 01.

- [x] Date resolution: plain `from` and `to` dates become a half-open window; the end day plus one; a single date is that one day; nothing given means the whole log. Test adapted from v1's "reset restores the whole log" and the filter tests
  - Evidence: `dashboard.date_window`; four tests in `backend/tests/test_dashboard.py`, all passing. `to` alone runs from the start of the log (spec decisions log, 14 Oct)
- [x] Dataset facts: capture time, the "Synthetic data" label, first and last log day, sorted distinct countries, sorted distinct users, row count. Test
  - Evidence: `dashboard.dataset_facts`; two tests in `test_dashboard.py`, passing. Capture time, row count and scenario users come from `evals/ground_truth.json`; the two dates, the country list and the user count (57) are hand-written values pinned from the seeded log
- [x] Alerts for a view: rules on the whole log, kept when at least one event is among the filtered rows, sorted newest first by last seen then rule. Tests adapted from "alerts are listed newest first" and "overview counts match the core"
  - Evidence: `dashboard.alerts_for_view`; four tests in `test_dashboard.py`, passing. The order test feeds the findings reversed, so the rule tie-break at 02:32:20 is really checked: without it the order fails
- [x] Report offer: the core decides "Write", "Update" or nothing from the Turns. Test adapted from "the report button waits for something new"
  - Evidence: no new code and no new test needed, so no test was adapted from the screen test; the author was told on 14 Oct before the build. v1 had already moved it into the core as `agent.report_request`, and the copied tests in `test_agent.py` (lines 190 to 208) cover no offer, "Write", nothing after a report, and "Update"; passing
- [x] The agent, its tools and every existing core function are unchanged; the 254 copied tests still pass
  - Evidence: `git diff main` shows no change under `backend/login_investigator` except the new `views.py` (now `dashboard.py`), and none in existing tests. Full suite 14 Oct: 267 passed (254 copied, 3 boundary checks from ticket 10, 10 new)
- [x] The core boundary test still passes
  - Evidence: `test_core_boundary.py`, 4 tests passing; it scans `dashboard.py` too

## Comments

2026-10-14: build done on branch `ticket-11-core-moved-logic`, test-first, three slices. Two-axis
review run (standards and spec). Fixed from it: two test assertions that recomputed their expected
value, one low-value test removed, docstrings corrected, lists made tuples as elsewhere in the core.
Kept as judgement calls for the author: the module name `views.py` sits beside `tool_views.py`.
Status `ready-for-human` until the author reviews, as for ticket 10.

2026-10-14: the author approved ("approved"). Status set to `resolved`. Two follow-ups raised by the
author from the concerns: a type checker for the project, and the name of `views.py`.

2026-10-14: ticket 20 renamed `views.py` to `dashboard.py` and `test_views.py` to
`test_dashboard.py`. The evidence lines above name the new files so they can still be checked.
