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

## Requirements

- Python 3.12 and [uv](https://docs.astral.sh/uv/)
- Node.js 20.19 or later, with npm
- An OpenRouter API key for the agent, and optionally an AbuseIPDB API key

## Setup

```bash
cd backend
uv sync                 # installs Python 3.12 and the exact versions in uv.lock
cp env.example .env     # then put your keys into .env, which is git-ignored

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

Files copied from v1 that the type checker flags are on a "not yet checked" list in
`backend/pyproject.toml`. The list only shrinks: new files never go on it.

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
