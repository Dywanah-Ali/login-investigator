# Login Investigator

Analyses a synthetic authentication log, flags suspicious sign-ins, and investigates them with an
AI agent. This is version 2: the same application as v1, moved from a Streamlit app to a FastAPI
backend and a React frontend built with shadcn/ui.

> **Synthetic data.** Every user, sign-in and attack in this project is generated. No real or
> personal data is used. The attacker IP addresses are publicly reported abuse sources.

## Layout

| Folder | What it holds |
| --- | --- |
| `backend/` | The Python project, run by uv: the core package `login_investigator`, data, tests and evals |
| `frontend/` | The React app: Vite, React Router and shadcn/ui, run by npm |
| `docs/` | The API contract, the migration brief, the bug log, the prompt log and the agent guides |

The core in `backend/login_investigator` is copied from v1 unchanged and imports neither Streamlit
nor FastAPI. A boundary test enforces that.

The default dataset lives in `backend/data/datasets/default/`. Set `LI_DATASET_DIR` to select
another folder containing `logins.csv`; this replaces the former `LI_LOG_PATH` setting. The
generator writes the default log and the Port's answer key together in that folder. The Port's
evaluation keeps using that default answer key and its frozen questions.

## Requirements

- Python 3.12 and [uv](https://docs.astral.sh/uv/)
- Node.js 20.19 or later, with npm
- An OpenRouter API key for the agent, and optionally an AbuseIPDB API key
- For the knowledge base's tests: PostgreSQL 18 from Homebrew, running as a service, with pgvector
  (`brew install pgvector`)

## Setup

```bash
cd backend
uv sync                 # installs Python 3.12 and the exact versions in uv.lock
cp env.example .env     # then put your keys into .env, which is git-ignored

# Once, as your PostgreSQL superuser: makes the limited role li_admin and the pgvector template.
# It asks you to choose li_admin's password; put it in .env as LI_PG_PASSWORD.
/usr/local/opt/postgresql@18/bin/psql -U postgres -d postgres -f setup/postgres-setup.sql

# Once, as the same administrator: creates the separate read-only account.
# Save its new password in .env as LI_PG_READER_PASSWORD.
/usr/local/opt/postgresql@18/bin/psql -U postgres -d postgres -f setup/postgres-reader-setup.sql

cd ../frontend
npm ci                  # installs the exact versions in package-lock.json
```

## Test

```bash
cd backend
uv run pytest
uv run pyright          # type check; must report 0 errors

cd ../frontend
npm test
npm run typecheck       # must report no errors
```

A test that needs PostgreSQL gets a fresh database for the test session, copied from the template
and dropped afterwards. When the service is down, such a test fails with the command that starts
it, `brew services restart postgresql@18`; it never skips. Every other test runs without the service.

Files copied from v1 that the type checker flags are on a "not yet checked" list in
`backend/pyproject.toml`. The list only shrinks: new files never go on it.

## Build the knowledge base

From `backend/`, after the PostgreSQL setup above:

```bash
uv run python -m scripts.build_knowledge_base
```

This explicitly rebuilds the organisation tables and searchable corpus in a new database. It
uses `LI_DATASET_DIR`, or `data/datasets/default` when unset. The source files stay unchanged.
Embeddings use OpenRouter and incur a small charge; the command reports provider usage and cost,
elapsed time, row counts and keyword-parser evidence. Use `--report <file.json>` to save it.
`--check-embedder` sends one short string without creating a database.

Only a successful build replaces the local, git-ignored `.knowledge-base.json` pointer. A failed
new database is dropped. Earlier successful databases are retained for inspection, named in the
report, and are not automatically deleted. A later explicit rebuild is needed after source files
change.

Each build records a fingerprint of the dataset folder's files and its build settings. When the
app starts, it compares that fingerprint with the folder. If anything changed, or the build cannot
be checked, the server refuses to start and names the command to run. With no build at all, the
app starts without a knowledge base and says so in the server log. The app does not read the
knowledge base for answers yet. `LI_KNOWLEDGE_BASE_STATE` moves the pointer file, for the app and
the build command alike.

The core uses one SQLAlchemy/psycopg engine shared with LangChain's chunk store. The separate
reader can select records but cannot change them. Core tests use fake embeddings with real
PostgreSQL and never call OpenRouter. PostgreSQL's reader account must exist for those tests.

## Evaluate the agent

Run from `backend/`, with the OpenRouter key in `.env`. These commands call the model.

```bash
uv run python -m evals.run --mode api                 # acceptance: 19 questions, 3 runs each
uv run python -m evals.run --mode api --only Q09 Q16 --runs 1 --jobs 1
uv run python -m evals.run --mode direct --only Q07 --runs 1  # cheap iteration
```

API mode starts its own local FastAPI process on a free port, with temporary memory. It uses
the configured dataset and saved reputation folder. Live AbuseIPDB lookups are disabled, including
reloading that key from `.env` in the child process. Every question run starts a new Investigation.
The runner reads each answer stream to completion and scores the reopened final turn with v1's
unchanged grader. Direct mode remains the default for compatibility; API mode is the acceptance
gate: at least 90% overall and 100% for injection and refusal checks.

Results append to `backend/evals/results/summary.md`, after v1's history. API rows begin with
`api:` in the note; JSON files include the mode, prompt fingerprint, commit and full answer
records. Rescore a saved result without model calls using
`uv run python -m evals.run --rescore evals/results/<file>.json`.

Retained evidence includes v1's final confirmation run (`2026-10-10-115038-35d4d98f.json`)
and v2's API runs. Intermediate v1 JSON files were removed from this repository's working
tree after the author approved the cleanup. Their summary rows remain, and their raw files
remain available in Git history. The original v1 project is unchanged.

## Run

The app is two servers, each in its own terminal window: the API does the work, and the
frontend is the screen you use. Commands below start from the repository folder.

### Start

1. In the first terminal, start the API:

   ```bash
   cd backend
   uv run uvicorn api.app:create_app --factory --port 8000
   ```

   Wait for `Application startup complete`, then leave this window open.

2. In a second terminal, start the frontend:

   ```bash
   cd frontend
   npm run dev
   ```

   Wait for the line showing `http://localhost:5173`, then leave this window open too.

3. Open http://localhost:5173 in a browser.

Starting takes about 10 seconds. The frontend's dev server forwards every `/api` request to the
API, so the browser talks to one address. The dashboards work without a model key; the
Investigator needs `OPENROUTER_API_KEY` in `backend/.env`.

### Stop

Press **Ctrl + C** in each terminal window. Nothing restarts on its own.

### When port 8000 is already in use

Start the API on another port, and give the frontend the same address in `LI_API_URL`:

```bash
# Terminal 1
cd backend
uv run uvicorn api.app:create_app --factory --port 8010

# Terminal 2
cd frontend
LI_API_URL=http://127.0.0.1:8010 npm run dev
```

`LI_API_URL` belongs to the frontend's dev server only; the API never reads it.

### If something goes wrong

| You see | It means |
|---|---|
| "address already in use" in the API terminal | Another program holds that port. Use another one, as above |
| "The API cannot be reached" on screen | The API terminal is not running, or the two port numbers differ |
| The Investigator says the agent is unavailable | The model key in `backend/.env` is missing or wrong. The dashboards still work |

## Licence

MIT. See [LICENSE](LICENSE).
