# Migration Brief — Login Investigator v2

Written 14 October 2026, at the end of a planning chat held in the original workspace. It is the
starting input for `/mp-wayfinder` in this workspace. **Read it before charting the map.** Treat the
"Decided" section as settled; treat "Open questions" as the first candidate tickets.

The original app lives in the sibling folder `../login-investigator`. That repo is submitted course
work and is public. It stays frozen: nothing in this effort changes it.

## Why this effort exists

The Login Investigator is a course project that grows every week of a bootcamp. Week 1 shipped a
Streamlit app: a dashboard over a synthetic authentication log, plus an in-app LangChain agent that
investigates it. Future weeks will add features in directions not yet fixed (see "Seams").

Before those features arrive, the app moves off Streamlit to a frontend and an API layer that can
grow in several directions. This effort plans that move. It does not build the future features.

## Decided

| Decision | Detail |
|---|---|
| New stack | FastAPI as the API layer; React with shadcn/ui as the frontend |
| Separate workspace | The new version is built here, in `login-investigator-v2`. The old repo stays frozen as course evidence |
| Same behaviour, new shell | v2 first reproduces what v1 does. New features come later, on top |
| Rigour tier | Tier 3 (a new system that future work will depend on) |
| Planning method | `/mp-wayfinder` replaces the separate elicit step. Its grilling names the destination |
| PRD is short | One or two pages, written after wayfinder, once the decisions are made. It covers: same behaviour in a new shell, the API contract, and the seams |
| Build the seams, not the features | Prepare plug-in points for likely future features. Do not build those features now |
| Screens are designed with the author | No UI code before the screens and the template are agreed (a rule carried over from v1) |

## What carries over from v1

v1 was built with a strict two-layer design: `login_investigator/` is plain Python with no Streamlit
import (checked 14 Oct), and `app/` only displays. That design is why this move is cheap.

| Part | v1 location | Size | In v2 |
|---|---|---|---|
| Core logic: loader, rules, search, stats, reputation, PDF report, investigations | `login_investigator/` | about 1,000 lines | Copied as is |
| Agent and its three read-only tools | `login_investigator/agent.py`, `tools.py`, `tool_views.py` | about 600 lines | Copied; session handling adapts to the API |
| Data generator and the synthetic CSV | `login_investigator/generator.py`, `data/` | | Copied |
| Saved AbuseIPDB responses | `data/ip_reputation/` | six files | Copied |
| Tests | `tests/` | 290 tests | Core and agent tests copied; screen tests replaced |
| Eval set | `evals/` | gold answers, code-only grader | Copied; becomes the proof that v2 behaves like v1 |
| Product and design decisions | `docs/PRD.md`, `docs/ui-design.md`, `docs/bug-log.md` | | Read as input, not copied blindly |

## What gets rebuilt

| Part | v1 | v2 |
|---|---|---|
| Screens | Streamlit, about 760 lines in `app/` | React with shadcn/ui |
| API layer | Does not exist; screens call Python directly | New FastAPI layer between the core and the screens |
| Charts | Plotly in Python (`app/charts.py`) | A JavaScript chart library; shadcn/ui ships one |

## What Streamlit did silently

These are the jobs Streamlit performed without being asked. Each one becomes explicit work in v2,
and is where most of the hidden effort sits.

1. **Memory per user.** Streamlit kept one agent per browser session in `st.session_state`, with
   conversation memory in `SqliteSaver`. FastAPI keeps nothing between requests, so v2 must track
   each conversation by an ID.
2. **The contract.** v1 screens call Python functions directly. In v2, screen and server talk only
   through JSON. Every endpoint needs a written input and output shape. This contract becomes the
   central document of v2.
3. **Live agent replies.** v1 shows a progress line while the agent works. Streaming the agent's
   progress and answer over an API needs its own design.
4. **Charts and filter state.** The shared sidebar filters (date range, outcome, country, user, plus
   the IP box) live in `app/shared.py` today. In v2 they move to the frontend and are sent with each
   request.

## Seams for future features

The likely direction of later weeks, and the plug-in point each needs. Preparing the seam is in
scope. Building the feature is out of scope.

| Likely future feature | What it will need | Seam to prepare now |
|---|---|---|
| RAG over documents | A document store, a retriever, new agent tools | The agent takes its tool list from one place, not three fixed tools |
| Knowledge graph | A second store, tools that query it | Data access sits in the core, never inside API routes |
| LangSmith or Langfuse tracing | A hook on every model call | The model and agent are created in exactly one function |
| Eval platforms | Running the eval set against the real app | Evals call the core or the API, never the screens |
| Uploading your own logs | An upload endpoint, a dataset per user | The API asks the core for "a dataset", not one fixed CSV |

## UI starting point

The four screens and their content were agreed in v1 (`../login-investigator/docs/ui-design.md`). v2
keeps the content and changes the shell. The app is two common shapes joined: an admin dashboard and
an AI chat.

| v1 screen | Common pattern | Candidate shadcn/ui starting point (from memory, to verify) |
|---|---|---|
| Overview | KPI cards and charts | The official dashboard block |
| Alerts | Table of findings with severity | The data table pattern |
| Log explorer | Filterable, searchable table | The "tasks" table example |
| Investigator | AI chat with history | An AI chatbot template built on shadcn/ui |
| Navigation | Sidebar app shell | The official sidebar blocks |

Choosing the template is a decision with the author: look at two or three candidates, then pick one.

Security rules from v1 that the new frontend must keep:

- Log fields appear only inside tables, never as formatted text. Some rows carry planted prompt
  injection.
- The agent's answers and the report card render with links and images switched off, so an injected
  image link cannot carry data out.

## Constraints carried over

- Python 3.12 and uv for the backend. pytest for tests.
- LangChain as in v1: `init_chat_model`, `@tool`, `create_agent` with a checkpointer, structured
  output. Model gpt-4o-mini at temperature 0 through OpenRouter.
- Keys only in a git-ignored `.env`. Log and API fields are untrusted data, never instructions.
- The repo may become public: no personal names, emails or other personal information in files.

Whether the course's "LangChain only as taught" rule still binds v2 is not yet decided.

## Open questions

Candidate first tickets for the wayfinder map.

1. Which shadcn/ui template or blocks to start from (research, then a prototype to compare).
2. Frontend framework: Next.js or a plain Vite React app.
3. The API contract: which endpoints, and the JSON shape of each.
4. How conversations and agent memory are tracked per user without Streamlit's session.
5. How the agent's progress and answer stream to the browser.
6. Repo layout: one repo holding backend and frontend, or two.
7. How v2 proves it behaves like v1 (eval set and core tests as the acceptance gate).
8. Whether course constraints from v1 still apply to v2.

## Known risk

The project gains a second language (TypeScript) and toolchain (Node). The author is not a
developer and will mostly read and review the frontend code rather than write it. Plans should keep
the frontend simple and conventional so it stays reviewable.

## Next steps in this workspace

1. The author reads this brief and corrects anything summarised wrong.
2. Run `/mp-setup-matt-pocock-skills` here to set up the issue tracker.
3. Run `/mp-wayfinder` and tell it to read this brief first.
4. After the map is clear, write the short PRD.
