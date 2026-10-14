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

## Run

Two terminals, one per server.

```bash
# Terminal 1: the API, on port 8000
cd backend
uv run uvicorn api.app:create_app --factory --port 8000

# Terminal 2: the frontend, then open http://localhost:5173
cd frontend
npm run dev
```

The frontend's dev server forwards every `/api` request to the API on port 8000, so the browser
talks to one address. The dashboards work without a model key.
