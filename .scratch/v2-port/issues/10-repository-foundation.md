# 10: Repository foundation

**What to build:** the v2 repository exists with the agreed layout, holds v1's core unchanged, and
proves it with v1's own tests. A reviewer can clone it, run the backend tests and see them pass.
No application behaviour yet; this is the ground the slices stand on.

**Blocked by:** None (can start immediately).

**Status:** resolved

Spec: [spec.md](../spec.md), "Repository" and "Scope and method". Source: v1 in the sibling folder,
read-only.

- [x] `git init` done, repository name `login-investigator`, fresh history, first commit message names v1 as the source, GitHub noreply address and the author's handle on the commit. Evidence: root commit 45275fa by the handle at the noreply address, message "Repository foundation: v2 starts from v1 of the Login Investigator". The folder is still called `login-investigator-v2` on disk; the name `login-investigator` applies when the GitHub repository is created, which waits for the author's review
- [x] Top level: a backend folder (uv project), a frontend folder (empty placeholder for now), docs, `GLOSSARY.md`, `CLAUDE.md`, a README with the two run commands to be filled in. Evidence: `backend/pyproject.toml`, `frontend/.gitkeep`, `docs/`, `GLOSSARY.md`, `CLAUDE.md`, `README.md` with a "Run" section holding two placeholder commands
- [x] The core package, data (log CSV, saved AbuseIPDB responses), tests and evals copied from v1 with relative paths preserved, so the copied tests run unchanged. Evidence: `backend/login_investigator`, `backend/data`, `backend/tests`, `backend/evals` copied byte for byte, checked with `diff -r` against v1 (only `test_core_boundary.py` differs: a new docstring and a new test; v1's test is kept unchanged); pyproject and lock carried over with Streamlit and Plotly removed
- [x] The 254 core and agent tests pass under Python 3.12 with uv, with the screen tests left behind. Evidence: `uv run pytest` in `backend/` on Python 3.12.14: 257 passed, which is v1's 254 core and agent tests plus 3 new boundary cases. The box first said 259; the real v1 count is 254, since v1 collects 290 and its two screen test files hold 36 (bug log B-001). Corrected by the author's approval on 2026-10-14, recorded in the spec's decisions log. `test_app.py` and `test_investigator_screen.py` left behind.
- [x] The core boundary test extended: no Streamlit and no FastAPI import anywhere in the core. Evidence: `backend/tests/test_core_boundary.py` keeps v1's test and adds one case each for Streamlit, FastAPI and Starlette, searching subpackages too. A planted `from fastapi import FastAPI` in a core subfolder made the FastAPI case fail; removing it made all pass
- [x] `env.example` holds names only; `.gitignore` covers `.env`, the memory file and build output. Evidence: `backend/env.example` holds two empty names; root `.gitignore` covers `.env`, `memory/` and SQLite files, `node_modules/`, `dist/`, `build/` and the local Claude settings file. v1's test `test_the_memory_file_and_its_side_files_are_git_ignored` failed before the ignore file existed and passes after
- [x] A scan of the repository finds no key, no personal name and no email. Evidence: grep over every tracked file for the author's names, email addresses, OpenRouter and OpenAI key shapes, 80-character hex keys and machine paths returned nothing. `.env` and `settings.local.json` are not tracked
- [x] `docs/bug-log.md` and `docs/prompt-log.md` exist with their headings. Evidence: both files, each with an entry format and a first entry (B-001, P-001)
- [x] Evidence named beside each box above when ticked

## Comments

2026-10-14: build done, waiting for the author's review. The first commit now exists and its box is ticked. One box stays open: the test count, which needs the author's ruling on 259 versus 254 (bug log B-001). Status is `ready-for-human` because the tracker has no `done` word.

2026-10-14: the author approved correcting 259 to 254. All nine boxes ticked with evidence. Status set to `resolved`, the tracker's closed word.
