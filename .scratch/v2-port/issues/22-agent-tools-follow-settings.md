# 22: The agent's tools follow the configured log and reputation folder

**What to build:** the agent's tools read the same log and the same saved-reputation folder as the
dashboards, as configured by `LI_LOG_PATH` and `LI_REPUTATION_DIR`. Today only the dashboards follow
those settings. The screens and the agent can never answer about different logs.

**Blocked by:** 12 (API foundation and the Overview endpoint).

**Status:** ready-for-human (build done 2026-10-17, waiting for the author's review)

Raised by: the review of ticket 12, decided by the author on 14 Oct: a ticket of its own, done
before ticket 18 (the eval runner's API mode), which is now blocked by this one.

The gap: `tools.py` loads the log through `load_log()` with its default path and calls
`reputation.lookup` with its default folder, each cached for the process. The API loads the log from
`Settings.log_path` once at startup. With the default settings both read the same file, so nothing
is wrong today; the gap opens only when a setting is changed, and nothing warns.

Why it waits for a design ruling: the fix changes `tools.py`, a core file, and the spec keeps the
core unchanged until Parity is proven. The design must keep the tools' signatures and results
exactly as v1's (spec: "Agent tools are unchanged from v1"), so the copied agent tests and the eval
set still prove Parity. Options to put to the author, for example: the tools take the dataset from
the one place the API loads it; or the core reads the same environment variables. Decide before
building.

- [x] The author has chosen the design; the choice is in the spec's decisions log
  - Evidence: 2026-10-17 decisions-log row. Design A, a core setter called once at startup, with
    three guards: cleared at shutdown, a test that the tools share the startup load, no silent
    fallback. Research: `research/22-tool-data-injection.md`
- [x] When the configured log fails validation, the two log tools return a short fixed error and the IP lookup still works; they never fall back to the default file. Test (added 2026-10-17 by the author's ruling)
  - Evidence: `test_a_log_that_fails_validation_is_refused_never_replaced_by_the_default`
- [x] The tools share the dashboards' startup load instead of loading their own copy, and the data is cleared when the app stops or fails to start. Test (added 2026-10-17, the guards of design A)
  - Reworded 2026-10-17. It first asked for an `is` identity check. The author chose to test from
    outside instead, because an identity check reads private helpers: ruling at the agreement of
    the test points. The frame is the very same object; the findings are the same `Finding`
    objects in a new tuple.
  - Evidence: `test_the_search_and_rules_tools_read_the_configured_log` counts the tools' own
    loader and rules calls during the run: none. `test_after_shutdown_the_tools_read_the_default_log_again`
    and `test_a_startup_that_fails_leaves_nothing_behind`; the second was seen failing against
    the old ordering (B-035)
- [x] With `LI_LOG_PATH` set, the agent's search and rules tools read that log, the same frame the dashboards use. Test
  - Evidence: `test_the_search_and_rules_tools_read_the_configured_log`: tools and Overview agree
    on 3 sign-ins, 1 failure and 0 findings; the default log has 1,856 rows and 5 findings. It
    failed with 1,856 before the fix (B-033)
- [x] With `LI_REPUTATION_DIR` set, the reputation tool reads saved responses from that folder. Test
  - Evidence: `test_the_reputation_tool_reads_the_configured_folder`; before the fix it tried a
    live call, which the test refuses
- [x] The tools' signatures and results are unchanged; the copied agent and tool tests pass unchanged
  - Evidence: the three tool functions are untouched in the diff; the eval prompt fingerprint is
    `35d4d98f` before and after; `test_tools.py` and `test_agent.py` pass unchanged
- [x] The "Not yet wired" note in `backend/api/settings.py` is removed
  - Evidence: the module docstring now says both readers follow the same settings
- [x] The core boundary test still passes
  - Evidence: full backend suite 356 passed; Pyright 0 errors

2026-10-17: build done on branch `ticket-22-tools-follow-settings`, test-first, four slices, then
a two-axis review. Review fixes applied by the author's choice: hand-over moved to the end of
startup with a matching `services.stop()`, neutral error text, one helper for the repeated
branches, types on the new code, the zero-load check, and this reworded box. Left as notes: an
agent answer still running during shutdown would fall back to the default log for its remaining
tool calls (low risk under a graceful shutdown); with a broken log and a bad time window, the
window error is returned first. `tools.py` stays on Pyright's "not yet checked" list; checked
alone, it shows only v1's three old errors, none in the new code. Status `ready-for-human` until
the author reviews.
