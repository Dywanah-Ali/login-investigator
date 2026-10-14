# Repo layout: one repo or two

Type: grilling
Status: resolved
Blocked by: none
Map: [map.md](../map.md)

## Question

v2 has a Python backend (uv, FastAPI) and a TypeScript frontend (React, shadcn/ui). Decide whether
they live in one repository or two, and what the top-level folders are.

Points to weigh:

- The author reviews rather than writes the frontend. One repo keeps the API contract next to both
  sides that depend on it.
- The repo may become public, and later course weeks build on it. The layout should still make
  sense when RAG, a knowledge graph and tracing arrive.
- The seams (one tool list, one model-and-agent factory, data access in the core, "a dataset" not one
  CSV) need a home in the folder structure.
- Course submissions may want one link to one repo.

The answer feeds "How the seams show in the code layout" and "Running two servers locally" in the
map's Not yet specified.

## Comments

### 14 October 2026, grilling with the author

**Facts found first.** v1 is one GitHub repository, `login-investigator-prototype`, with the Python
core, tests, evals and data at the top level. The v2 folder is not a git repository yet.

## Decision

1. **One repository.** Backend and frontend are two folders in the same repo. One submission link,
   one review per API change, one home for the contract, the glossary and the docs. A light
   monorepo: two independent projects, no shared tooling.
2. **Top level:**

   ```
   backend/              the whole Python project, run by uv
     login_investigator/ the core, copied from v1 untouched
     api/                the FastAPI app and routes, a separate package
     tests/ evals/ data/ as in v1, paths preserved so the copied tests pass unchanged
     pyproject.toml uv.lock env.example
   frontend/             the Vite + React app, run by npm
   docs/                 PRD, brief, contract, bug log, prompt log
   GLOSSARY.md README.md CLAUDE.md
   ```

3. **API code in a separate `api/` package** beside the core, never inside it. The rule "the core
   never imports FastAPI" is then checkable with one search of `backend/login_investigator/`.
4. **Seams have fixed homes, all in the core and all already present in v1:** the tool list in
   `tools.py`, the single model-and-agent factory in `agent.py`, data access in the core's loader,
   extended to answer "a dataset" rather than one file.
5. **Running locally: two terminals.** One command starts the API in `backend/`, one starts Vite in
   `frontend/`. Vite's dev proxy forwards API calls to FastAPI, so the frontend never holds the
   backend address and no cross-origin headers are needed. The README documents both commands.
6. **Git:** `git init` at the end of the wayfinder, as the first build step, so the first commit
   holds the agreed layout, the PRD and the copied core. Repository name `login-investigator`.
   Fresh history; the first commit message names v1 as the source. Nothing pushed before the
   author's review. GitHub noreply address and handle for commits.

Closes "How the seams show in the code layout" and "Running two servers locally" in the map.
