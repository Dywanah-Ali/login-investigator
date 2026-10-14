# What proves Parity

Type: grilling
Status: resolved
Blocked by: 01
Map: [map.md](../map.md)

## Question

Parity (see `GLOSSARY.md`) is the acceptance gate for the Port. Decide exactly what evidence closes
it.

Facts to start from ([v1-facts.md](../v1-facts.md), "Proof"): the copied core tests (254 of 290)
and the eval set call the Python core directly. Copied unchanged, they pass even when the API or the
screens are broken. The 31 screen tests (`test_app.py`, `test_investigator_screen.py`) test
Streamlit and cannot be copied.

Decide:

1. **Core.** Which v1 tests are copied as they are, and whether any must change because logic moved
   in [Screen-layer logic](01-screen-layer-logic.md).
2. **API level.** How Parity is checked through the API. Candidates: the eval runner gains a mode
   that asks questions through the HTTP endpoint instead of the core; API tests that replay the
   screen tests' cases (filters, empty states, alerts S1 to S4) against the endpoints.
3. **Screens.** What replaces the 31 screen tests: API tests alone, frontend component tests, a
   browser test of the core scenario, or a manual checklist with screenshots. Weigh what the author
   can run and read.
4. **Pass bar.** The eval target v1 agreed (90% overall, 100% for injection and refusal) and whether
   v2 keeps it unchanged.

The answer is written into the PRD as the acceptance criteria of the Port.

## Comments

## Answer

Grilled with the author on 14 October 2026. Twelve questions, eleven answered with the recommended
option. One change: **no screenshots anywhere in the gate.** Manual items close on the author's
ruling, recorded with a date, as the verification gate for content allows.

**The rule.** The Port is accepted only when every criterion below is ticked with named evidence.
Automated checks run first; the manual run comes last, on a build where every automated check passes.

### The gate, by layer

| Layer | Evidence | What it proves |
|---|---|---|
| Core | The 254 v1 core and agent tests, copied unchanged | The core did not change |
| Core, moved logic | New pytest tests, adapted from the screen tests, for every piece ticket 01 moved into the core: date resolution, dataset facts, alerts for a view, report offer | The logic that left the screens still means the same |
| Core boundary | `test_core_boundary.py` extended: no Streamlit and no FastAPI import in the core | The core stays independent of both shells |
| API | pytest with FastAPI's test client, replaying the data-checking screen tests: filters change every screen consistently, an empty filter gives a clear message, S1 to S4 appear in alerts, alerts newest first, reset restores the whole log, a bad IP is refused without echoing it, memory opened once and agent built once per process | The contract behaves as v1's screens did |
| Agent | The eval set run in a new **API mode**: the runner starts its own FastAPI server on a free port, with a temporary memory file and the AbuseIPDB key removed, sends each question through the ask endpoint, reads the stream, asks for the report through the report endpoint, and scores with the unchanged grader. The direct mode stays for cheap iteration; **the API mode is the one that counts** | The agent gives the same answers through the real transport |
| Pass bar | Unchanged from v1: 90% overall, 100% for injection and refusal, 19 questions times 3 runs. Parity means meeting the target, not reproducing v1's 98% | A stable gate under model variance |
| Eval history | v1's `evals/results/summary.md` rows are copied into v2 as the first rows; v2 runs continue the table | A regression against v1 is visible at a glance |
| Frontend logic | Vitest with React Testing Library for the pieces ticket 01 placed in the frontend: three names then "N more", singular or plural counts, failed share, paging of past investigations, the explorer jump route, the bad IP message, and the markdown allowlist renderer tested with the injection strings | The logic that left Python still means the same, and the renderer cannot leak |
| Presence | A manual checklist, ticked by the author with a dated ruling: synthetic label, metric labels, empty-state messages, scope note, AI note, progress words per tool, locked input while answering, severity labels and colours, charts per theme, error messages hide exception text. No browser test tool | What v1's presence tests checked is still on screen |
| Core scenario | v1's eight-step scenario run end to end in the live v2 app by the author, closed with a dated ruling | Browser, API, agent, memory, report and PDF work together |
| Engineering | Fresh-clone start of both servers from the README; no key in git history; the core boundary test | A reviewer's first ten minutes succeed |

### Rejected

- Playwright or any browser test tool: a third toolchain the author would have to maintain.
- Raising the pass bar to v1's actual 98%: one flaky run would block the Port.
- Screenshots anywhere: the author's ruling. The project rule to take screenshots when a screen
  first works was dropped from `CLAUDE.md` the same day, at the author's request.

### Where it is written

The whole gate becomes the "Quality bar and acceptance criteria" section of the v2 PRD, in v1's
style: one checkbox per criterion, the evidence named beside it, the manual checklist in the same
section.

### Hand-offs

- [The API contract](09-api-contract.md): the API eval mode needs three endpoints it can drive
  without a browser: start an investigation, ask (stream), and write the report. The report turn of
  the eval set (`REPORT`) maps to the report endpoint. The server must accept a memory file path and
  a port from configuration, so the runner can isolate a run.
- PRD: the table above, verbatim, as the acceptance criteria. `GLOSSARY.md` Parity updated today.
