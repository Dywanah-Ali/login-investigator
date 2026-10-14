# Prompt Log

The key prompts given to Claude Code while building v2, in order. Each entry gives the author's
prompt verbatim, its purpose, what came back, and what changed next. These may go into course
submissions.

## Entry format

```
### P-001 · 2026-10-14 · Ticket NN Title

**Prompt:**
> the author's prompt, verbatim

**Purpose:** why the prompt was given.
**Result:** what came back.
**Next:** what changed next.
```

## Entries

### P-001 · 2026-10-14 · Ticket 10 Repository foundation

**Prompt:**
> /mp-implement .scratch/v2-port/issues/10-repository-foundation.md

**Purpose:** first build prompt of v2. Build the repository the slices stand on: git, the agreed
layout, v1's core, data, tests and evals copied, and v1's tests passing.
**Result:** repository initialised with a backend uv project and an empty frontend placeholder. v1's
core, data, evals and core and agent tests copied with relative paths preserved; Streamlit and
Plotly dropped from the backend's dependencies. 254 copied tests pass on Python 3.12, not the 259
the spec expected (B-001). The core boundary test now also forbids FastAPI and Starlette.
**Next:** the author reviews the first commit; then ticket 11, the logic moved into the core.
