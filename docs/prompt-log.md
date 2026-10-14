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

### P-004 · 2026-10-14 · Tickets 20 and 21: the module name and a type checker

**Prompt:**
> approved.
>
> then lets work on those two issues "The project has no type checker set up. I ran one just for this check. The new file is clean. It found 3 type errors in v1's copied generator.py, which this ticket must not touch. Your call whether that becomes a ticket.
> The new file is named views.py and sits beside tool_views.py, which does a different job. A clearer name would be dashboard.py. I kept the name because ticket 03 called these "view functions"."

**Purpose:** close ticket 11 and act on two of its concerns.
**Result:** ticket 11 closed and merged into `main` locally. Measuring the whole backend showed 61
type errors under Pyright, not 3, all in v1's copied code, and 2 in the new module that mypy had
missed. Three options were put to the author, who chose Pyright with a "not yet checked" list.
Ticket 20 renamed `views.py` to `dashboard.py`. Ticket 21 added Pyright, listed 14 copied files as
not yet checked, and fixed the new module. Pyright: 0 errors; a deliberate error fails it. Full
suite: 267 passed.
**Next:** the author reviews tickets 20 and 21; then ticket 12, the API foundation.

### P-005 · 2026-10-14 · Ticket 12 API foundation and the Overview endpoint

**Prompt:**
> /mp-implement 12

then, before approving the test points, a question on one of them:

> explain to me this pls "For seam 2, the test counts calls to the core's open_memory and build_agent while sending several requests. This is the one place a test watches a collaborator, because "exactly once" is the requirement itself."

then "yes go ahead".

**Purpose:** build the frontier ticket. The agent proposed a branch and two seams to test at (the
HTTP API, and startup seen from outside); the author asked why one test watches the core's
functions before approving.
**Result:** a new `backend/api/` package with settings, startup, the one error shape, the shared
filters and three endpoints, built test-first in six slices. FastAPI's default 422 was shown to copy
a hostile value back to the client before the custom handler replaced it. The two-axis review found
two real bugs, both fixed test-first: a number sent as a date gave a confident empty view (B-002),
and a missing log file sent the server's full path to the client (B-003). 26 API tests; full suite
293 passed; Pyright clean; the core unchanged.
**Next:** the author reviews the branch and rules on the open points in ticket 12's comments.

### P-006 · 2026-10-14 · Ticket 12 API foundation and the Overview endpoint

**Prompt:**
> ok lets go through the 4 points 1 at a time, be simple for me to understand pls

**Purpose:** rule on the four open points of ticket 12, each explained in plain words with the
options, one question at a time.
**Result:** all four recommendations chosen. The three extra error codes and the missing-file text
were written into the contract. An empty filter box now means "all" for every filter, built
test-first. The agent's tools ignoring the log and reputation settings became ticket 22, which now
blocks ticket 18. Each ruling has a row in the spec's decisions log. Full suite: 294 passed.
**Next:** the author reviews ticket 12 for approval.
