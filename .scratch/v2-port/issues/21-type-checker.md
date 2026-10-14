# 21: A type checker for the backend

**What to build:** Pyright checks the backend on one command and is green from the first day. New v2
code is fully checked. The files copied from v1 that Pyright flags today sit on a written "not yet
checked" list in the configuration; a file leaves the list only once it is clean, so the list can
only shrink. Pyright is the checker VS Code uses, so the editor and the check agree.

**Blocked by:** 20 (Rename the core's `views.py`).

**Status:** resolved

Raised by: the concerns of ticket 11, decided by the author on 14 Oct (spec decisions log).

Measured on 14 Oct with Pyright 1.1.414 in standard mode: 61 errors over `login_investigator`,
`tests` and `evals`, 44 of them in the core. Almost all come from pandas types the checker cannot
follow; a few are values that could in theory be empty. All 267 tests pass, so none breaks
behaviour today. mypy, more lenient, found 14.

- [x] Pyright pinned as a backend development dependency; settings in `pyproject.toml`; `uv run pyright` from `backend` checks `login_investigator`, `tests` and `evals`
  - Evidence: `pyright==1.1.414` in the dev group and `uv.lock`, added by `uv add`; `[tool.pyright]` in `backend/pyproject.toml`
- [x] The "not yet checked" list holds exactly the copied v1 files that fail today, each named, with a comment saying why the list exists and how a file leaves it
  - Evidence: 14 files on the list: the 15 files Pyright flagged on 14 Oct, less `dashboard.py`, which was fixed instead
- [x] `dashboard.py` and `test_dashboard.py` are checked and clean; the two errors Pyright finds in `dashboard.py` today ("not a time" values from `pd.Timestamp`) are fixed without changing behaviour
  - Evidence: `captured_at` and `date_window` now use plain UTC datetimes, which cannot be "not a time"; the search already accepted them. The ten dashboard tests pass unchanged
- [x] No copied v1 file is changed
  - Evidence: `git diff` under `login_investigator`, `tests` and `evals` shows only `dashboard.py`
- [x] `uv run pyright` reports zero errors, and a deliberate type error in a checked file makes it fail (shown once, then removed)
  - Evidence: 14 Oct, "0 errors". With `_DELIBERATE: int = "not a number"` added to `dashboard.py`: 1 error, exit code 1. The line was then removed
- [x] The README's Test section lists the check beside `uv run pytest`
  - Evidence: `README.md`, Test section
- [x] The full suite still passes (267)
  - Evidence: `uv run pytest`, 14 Oct: 267 passed

Out of scope: cleaning the v1 files on the list. Each is a later ticket, after Parity is proven.

## Comments

2026-10-14: the author approved ("approved"). Status set to `resolved`. Open, not ticketed: VS Code
does not use `backend/.venv`, so its underlines do not match `uv run pyright` yet; Ruff runs in the
editor but is not configured in the project; nothing runs the checks automatically.
