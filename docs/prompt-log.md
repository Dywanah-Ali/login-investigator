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

### P-002 · 2026-10-14 · Ticket 10 Repository foundation

**Prompt:**
> "The test-count box is unticked until you rule. It should read 254, not 259. The same 259 appears in the spec, in tickets 08 and 11, and in the map, so one correction should cover all four places." double check from the source pls if u can

**Purpose:** the author challenged the claim before ruling on it, asking for proof from v1 itself.
**Result:** a fresh export of v1's last commit collected 290 tests, 254 outside the two screen
files. The 259 was traced to a subtraction of screen test functions from collected tests. The first
bug log entry had the wrong cause and was corrected. The author then approved the change ("approved").
**Next:** 259 became 254 in the spec, tickets 08, 10 and 11 and the map, with a decisions log row.
Ticket 10 closed with all nine boxes ticked.

### P-003 · 2026-10-14 · Ticket 11 Core: the logic that moved from the screens

**Prompt:**
> /mp-implement

then "go" to the proposed branch, and "ok go ahead" to the proposed test points.

**Purpose:** build the frontier ticket. No ticket was named, so the agent picked ticket 11, stated it,
proposed a branch and the three test points, and waited for the author each time.
**Result:** a new core module `views.py` with `date_window`, `dataset_facts` and `alerts_for_view`,
built test-first with ten tests. The Report offer needed no work: v1 had already moved it into the
core, with tests. The contract left `to` alone undefined; it now runs from the start of the log,
with a decisions log row. A two-axis review found two tests recomputing their expected values; both
fixed. Full suite: 267 passed.
**Next:** the author reviews ticket 11; then ticket 12, the API foundation.
