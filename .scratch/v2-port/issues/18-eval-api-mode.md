# 18: Eval set in API mode

**What to build:** the v1 eval set proves the agent through the real transport. The runner starts
its own server, drives the Investigation endpoints for every question and the report, scores with
the unchanged grader, and records the run in a results table that begins with v1's history.

**Blocked by:** 16 (Investigations API), 22 (The agent's tools follow the configured log and
reputation folder; author's ruling, 14 Oct). Both resolved; 22 on 17 Oct. The runner's direct mode
never hands a dataset to the tools, so it keeps reading the default log; the API mode goes
through startup and follows `LI_LOG_PATH` and `LI_REPUTATION_DIR`.

**Status:** resolved

Spec: [spec.md](../spec.md), "Testing Decisions". Contract: "What the eval runner's API mode drives".

- [x] A new API mode in the runner: starts FastAPI on a free port with a temporary memory file and the AbuseIPDB key unset; starts an Investigation; asks each question through the ask endpoint and reads the stream to the end; a `REPORT` turn goes to the report endpoint; reopens and scores the last Turn with the unchanged grader
- [x] The direct mode still works for cheap iteration; the API mode is the one that counts
- [x] Questions, gold answers and grader unchanged from v1; the scoring tests pass
- [x] v1's results summary rows copied in as the first rows of v2's table; v2 runs append
- [x] One full run recorded: 19 questions times 3 runs, with the result against the bar (90% overall, 100% injection and refusal) and the run files saved
- [x] No key printed or saved in any run file

## Comments

### 2026-10-17 · Implementation started

Author invoked `$implement T18`. Baseline: `84065b9`. Work on the current branch, as the
implement skill requests. The final v1 agent prompt is unchanged; questions, gold answers and
grader compare byte-for-byte equal. v1's summary and run files are already copied into v2.
Tests use the spec's agreed HTTP API and core function seams.

Contract gap found: ToolView returns presentation fields but not the tool name and original
arguments required by the unchanged grader. Proposed adding `name` and `args`; author approval
requested before changing the contract or implementing that part.

### 2026-10-17 · Contract addition approved

Author: "ok good. ok Approved". ToolView gains the original tool `name` and `args`.
Recorded in the API contract and spec decisions log before implementation. The grader and
agent prompts remain unchanged.

### 2026-10-17 · Implementation checks and reviews

- Paid API smoke: Q09 and Q16, one run each, 2/2 passed. Report generated and reopened;
  security 100%. Saved in `backend/evals/results/2026-10-17-184429-35d4d98f.json`.
- Prompt fingerprint remains `35d4d98f`, v1's final fingerprint.
- Backend Pyright: 0 errors. The changed eval runner is now checked, removed from the ignore list.
- Frontend type check passes; all 18 Investigator screen tests pass after the ToolView type update.
- Two-axis review of the diff from `84065b9`: Standards 0 findings; Spec 0 findings. Separate
  read-only reviewers examined the implementation. Spec reviewer also checked the 120-second
  bounded startup adjustment. Final full-run evidence will be appended below.
- First full-run attempt timed out before any questions under high host load (B-040); no
  answer was scored. Full backend suite and a subsequent full API benchmark remain to finish.

Full backend suite completed: **370 passed in 385.56 seconds**. The 67 focused backend checks
passed earlier. Full API benchmark retry started after competing checks completed.

## Evidence

### Full API benchmark · 2026-10-17

Command, from `backend/`:

```bash
uv run python -m evals.run --mode api --runs 3 --jobs 3 --label 'T18 full API benchmark, unchanged v1 prompt and grader'
```

Saved answers and checks: [full run](../../../backend/evals/results/2026-10-17-185622-35d4d98f.json).
History: [summary](../../../backend/evals/results/summary.md).

| Evidence | Result |
|---|---|
| Overall | 56/57, 98%; gate 90% met |
| Injection and refusal | 15/15 security runs, 100%; gate met |
| Live reputation lookups | 0, including earlier turns |
| Failed runs | Q02 run 2: failed or incomplete SSE stream, counted as a failure; B-041 |
| Final v1 prompt fingerprint | `35d4d98f`, unchanged |
| Questions, gold answers, grader | Byte-identical to v1 |
| v1 summary history | Exact original prefix preserved; v2 rows append |
| Run file secrets | Loaded key values absent from both saved v2 JSON files |

The failed stream's underlying cause is not established. No prompt, grader, question or threshold
was changed to improve the score. The earlier startup-only timeout produced no answers and is
preserved in B-040. The failed Q02 run remains in the benchmark; no replacement run was substituted.

### Automated and review evidence

- `uv run pytest -q`: **370 passed**, including all 36 copied eval scoring tests and direct-mode
  fake-model runs, HTTP runner tests, report/reopen, stream failures and child isolation/cleanup.
- `uv run pyright`: **0 errors**; `evals/run.py` now checked rather than ignored.
- `npm run typecheck`: passed.
- `npm test -- src/pages/investigator.test.tsx`: **18 passed**.
- Standards review: **0 findings**. Spec review: **0 findings**.
- `git diff --check`: passed. Agent core diff from `84065b9`: empty.

Implementation complete. Author approved on 17 October 2026. Nothing pushed.

## Answer

Author: "approved" (17 October 2026). Accepted implementation commit `b56a657` and the
recorded evidence: 56/57 (98%) overall, 15/15 (100%) security, unchanged v1 prompt and grader,
370 backend tests passing, clean type checks and both reviews. Ticket 18 resolved. B-041
remains an unresolved finding in the bug log. Ticket 19 is next.
