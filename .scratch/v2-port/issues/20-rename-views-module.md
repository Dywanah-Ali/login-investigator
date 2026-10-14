# 20: Rename the core's `views.py` to `dashboard.py`

**What to build:** the core module made in ticket 11 gets a name that says what it holds. `views.py`
sat beside `tool_views.py`, which does an unrelated job (the agent's tool-call panel), so the two
names suggested a link that does not exist. No behaviour changes.

**Blocked by:** 11 (Core: the logic that moved from the screens).

**Status:** ready-for-human

Raised by: the standards review of ticket 11 ("Mysterious Name"), taken up by the author on 14 Oct.

- [x] `backend/login_investigator/views.py` becomes `dashboard.py`, with its history kept by git
  - Evidence: moved with `git mv`; the commit records it as a rename
- [x] `backend/tests/test_views.py` becomes `test_dashboard.py` and imports the new name
  - Evidence: same; the import line is the only change inside the file
- [x] The API contract and ticket 11's evidence name the new module. The prompt log stays as written, since it records what happened
  - Evidence: `docs/api-contract.md` line 60; ticket 11's five evidence lines, plus a comment there explaining the change
- [x] No other file names the old module
  - Evidence: `git grep` for the old names finds only ticket 11's explaining comment, and the prompt log by design
- [x] The full suite passes with the same count as before the rename (267)
  - Evidence: `uv run pytest`, 14 Oct: 267 passed
