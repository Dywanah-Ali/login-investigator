# 44: Phase 0 cleanup

Type: build
Status: ready-for-agent
Blocked by: 28
Phase: 0
Model: standard (Opus 5.5 or Sol 6.1)

## What to build

One ticket that pays the foundation's small debts before the phase 0 gate (ticket 29). It
collects review concerns and inconsistencies found while phase 0 is built, so they are repaired
while the foundation is still the topic, rather than at the end of the initiative.

Opened by the author's ruling of 28 October 2026, after T18. Small items found in tickets 19 to
28 join the list below with their source; each item gets its own short ruling here before it is
built. Opening the ticket schedules the items; it does not approve a design for any of them.

## Items

| # | Item | Source | Ruling needed before build |
|---|---|---|---|
| 1 | Align every existing `LI_` setting with the settings rule: the environment first, then `.env`, then the default, read with `dotenv_values`. Covers the app's `LI_DATASET_DIR`, `LI_MEMORY_PATH`, `LI_REPUTATION_DIR` and `LI_KNOWLEDGE_BASE_STATE`, and the build command's pointer setting | AUD-059; spec, API contract change 5 (author's ruling, 28 October 2026) | None: the rule is ruled |
| 2 | Make `env.example` match what the app honours, including `LI_DATASET_DIR` and `LI_KNOWLEDGE_BASE_STATE` | Found while answering AUD-059 | None, follows item 1 |
| 3 | Bring chunking and mention code into the staleness fingerprint, or decide not to | AUD-058 | Yes: a hand-bumped recipe version, a hash of the modules' source, or leave as is |
| 4 | Reclaim superseded knowledge-base build databases, or keep manual maintenance | AUD-057 | Yes: a cleanup policy that protects the active and unrelated databases, or none |
| 5 | Candidate: a startup refusal prints Python's traceback, whose frames show source-file paths in the console; the fixed message has none | T18 spec review A2 | Yes: whether the console should show only the fixed message |

## Acceptance criteria

- [ ] Before any build work starts, the builder tells the author this ticket's `Model:` line and
      asks the author to set that model. The build starts only after the author confirms, and a
      dated line under Comments records the model used.
- [ ] Each item has a ruling recorded under this ticket's Answer before it is built.
- [ ] Item 1: one test per reading program (app, build command) pins the order: environment over
      `.env` over default. The eval and the test run stay isolated from the real build.
- [ ] Items 3 to 5: built as ruled, each with a test, or closed in the register by the ruling.
- [ ] The register entries named above are updated with closure evidence.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged.

## Comments
