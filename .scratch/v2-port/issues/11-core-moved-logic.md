# 11: Core: the logic that moved from the screens

**What to build:** the four pieces of meaning that v1 kept in its Streamlit layer now live in the
core, so the API, the screens and the agent tools can never disagree. Each has a pytest adapted from
the old screen test that covered it.

**Blocked by:** 10 (Repository foundation).

**Status:** ready-for-agent

Spec: [spec.md](../spec.md), "Where logic lives". Decisions: ticket 01.

- [ ] Date resolution: plain `from` and `to` dates become a half-open window; the end day plus one; a single date is that one day; nothing given means the whole log. Test adapted from v1's "reset restores the whole log" and the filter tests
- [ ] Dataset facts: capture time, the "Synthetic data" label, first and last log day, sorted distinct countries, sorted distinct users, row count. Test
- [ ] Alerts for a view: rules on the whole log, kept when at least one event is among the filtered rows, sorted newest first by last seen then rule. Tests adapted from "alerts are listed newest first" and "overview counts match the core"
- [ ] Report offer: the core decides "Write", "Update" or nothing from the Turns. Test adapted from "the report button waits for something new"
- [ ] The agent, its tools and every existing core function are unchanged; the 254 copied tests still pass
- [ ] The core boundary test still passes
