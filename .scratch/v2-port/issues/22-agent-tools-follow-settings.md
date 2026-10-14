# 22: The agent's tools follow the configured log and reputation folder

**What to build:** the agent's tools read the same log and the same saved-reputation folder as the
dashboards, as configured by `LI_LOG_PATH` and `LI_REPUTATION_DIR`. Today only the dashboards follow
those settings. The screens and the agent can never answer about different logs.

**Blocked by:** 12 (API foundation and the Overview endpoint).

**Status:** ready-for-human

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

- [ ] The author has chosen the design; the choice is in the spec's decisions log
- [ ] With `LI_LOG_PATH` set, the agent's search and rules tools read that log, the same frame the dashboards use. Test
- [ ] With `LI_REPUTATION_DIR` set, the reputation tool reads saved responses from that folder. Test
- [ ] The tools' signatures and results are unchanged; the copied agent and tool tests pass unchanged
- [ ] The "Not yet wired" note in `backend/api/settings.py` is removed
- [ ] The core boundary test still passes
