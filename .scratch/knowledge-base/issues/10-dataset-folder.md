# 10: The dataset folder

Type: build (prefactor)
Status: resolved
Blocked by: none
Phase: 0

## What to build

The app's setting names a dataset folder instead of a single log file. The regenerated world will
live in the folder called `default`; this ticket moves the Port's current log into it and makes
everything that reads the log read it from there. Nothing the analyst sees changes. This prepares
the ground so tickets 11 and 12 only add to the folder.

## Decisions implemented

- T04 d13 (one folder per dataset); [spec ruling] the regenerated world is the dataset folder
  `default`, the setting names a folder and replaces the log-path setting, the old log file is
  retired; API contract change 5 (the setting part).
- [spec ruling] the Port's ground-truth file stays, in its current shape, beside `truth.json`.
- User story 56.

## Acceptance criteria

- [x] The dataset setting names a folder; the old log-path setting is removed; `env.example` and the
      API contract's configuration section are updated.
- [x] The generator writes the log into `default`; the log file at its old place is removed.
- [x] The folder has a README naming the seed. The ATT&CK version is added to it in ticket 14.
- [x] The Port's ground-truth file is written beside the log in `default` and the Port's scorer reads
      it from there. If moving it would change the frozen Port exam, it stays where it is and the
      reason is recorded here.
- [x] A missing or invalid dataset folder behaves as today's invalid log does; the startup tests
      prove it.
- [x] The eval runner's isolation works the same way with a folder.
- [x] The backend tests, the frontend tests and the Port's eval pass unchanged.
- [x] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged.

## Comments

### 2026-10-26 — Implementation started

Testing at the spec's agreed doors 1 (generator), 4 (API startup and dataset responses), and 6
(eval runner). Review baseline: `ec2acec26d3f17d5f0ee3daaf97608c42c85dcd5`. This ticket relocates
the existing files without changing their contents or the Port's questions and grading rules.

### 2026-10-26 — Implementation and review

Implementation commit: `ab8583f`. `LI_DATASET_DIR` replaces `LI_LOG_PATH`; its default is
`backend/data/datasets/default`. Startup passes that folder's `logins.csv` through the existing
core loader. The generator's default paths, the Port scorer's answer-key path, the frontend's
security-test fixture, and the eval's dirty-input tracking follow the move. The generator command
was run and wrote 1,856 rows plus the answer key at the new paths. Git records both as 100%
identical renames. The Port question file and scoring checks are unchanged; its historical note
still names the old answer-key location because the question file is frozen.

TDD evidence: the two settings checks failed before the setting changed, then passed. Five API
validation checks failed before startup used the folder, then passed. The missing-folder test
now covers an absent folder, an empty folder and a file supplied as a folder. The existing runner
test now starts a real child with a one-row alternate dataset and proves it retains that dataset
while deleting temporary memory. Focused checks: 61 passed, then 113 passed. Initial Pyright:
0 errors, 0 warnings. Frontend typecheck passed.

#### Standards review

Separate read-only reviewer inspected `git diff ec2acec...ab8583f`. No documented-standard
violations or actionable smells. Core loading stays at its existing seam, routes are unchanged,
client errors are fixed text, and the frontend change only redirects its security-test fixture.
Repeated literal paths in tests independently check the documented location.

#### Spec review

Separate read-only reviewer inspected the same diff against this ticket and the relevant spec
sections. No findings. Folder selection, removal of the old setting, unchanged file moves,
generator/scorer paths, the seed README, error responses and runner isolation are covered.
No scope creep. Full-suite and live eval evidence still pending at review time.

Review summary: Standards 0 findings; Spec 0 findings. No review concerns to register.

### 2026-10-26 — Full verification

- `cd backend && uv run pytest -q`: 423 passed. New invalid-folder cases account for the increase
  from ticket 09's 421 tests.
- `cd backend && uv run pyright`: 0 errors, 0 warnings, 0 information messages, including a final
  run after the runner-isolation test update.
- `cd frontend && npm run typecheck`: passed.
- `cd backend && uv run python -m evals.run --mode api --label 'T10 dataset folder relocation; unchanged Port exam'`:
  55/57 overall (96%, target at least 90%); 15/15 security (100%, target 100%). No run errors or
  live reputation lookups. Result: `backend/evals/results/2026-10-25-221147-7ff8e5ae.json`;
  commit `ab8583f`; prompt fingerprint `7ff8e5ae`, unchanged from the Port.
- Failed eval attempts remain counted: Q07 run 1 repeats B-070/AUD-030's prose count error;
  Q08 run 2 includes the brute-force address as a sprayer, recorded as B-073/AUD-045. No agent
  fixes in this folder-move scope. The existing gates pass despite those two failures.
- First frontend suite: 144/149 passed, with five Explorer timeouts. B-066/AUD-028 record the
  recurrence under concurrent checks. Full rerun after the backend suite and live eval finished:
  `npm test -- --maxWorkers=1`, 149/149 passed across 13 files. No code or timeout change; the
  original failed run remains recorded and its cause remains unconfirmed.


## Answer

Resolved on 26 October 2026. The app selects a dataset folder and all existing readers follow
its log's new default location. No analyst-facing behavior, log contents, answer-key contents,
Port questions or scoring checks changed.

| Criterion | Evidence |
| --- | --- |
| Folder setting replaces log-path setting | `api/settings.py`, `backend/env.example`, `docs/api-contract.md`; settings tests pass |
| Generator writes default folder; old log retired | Generator command wrote 1,856 rows to `data/datasets/default/logins.csv`; Git records a 100% identical rename |
| Seed README | `backend/data/datasets/default/README.md`, seed `20261008` |
| Port answer key colocated; exam preserved | 100% identical `ground_truth.json` rename; scorer loads the new path; frozen questions and scoring checks unchanged |
| Invalid-folder behavior | Startup tests cover missing folder, empty folder, file instead of folder, invalid CSV and hostile row; same fixed errors |
| Eval isolation | Real child reads a one-row alternate dataset; temporary memory is removed, dataset retained; full API eval uses isolated memory |
| Safety net | 423 backend tests; final 149 frontend tests; Port eval 55/57 overall and 15/15 security, both gates met |
| Typecheck and review | Pyright and frontend typecheck pass; separate Standards and Spec reviewers each report 0 findings |

Known gaps retained outside scope: Explorer timeout recurrence B-066/AUD-028, count error
B-070/AUD-030, and narrow spraying answer B-073/AUD-045. No unresolved T10 review findings.
Implementation commit `ab8583f`; evidence and closure recorded in a follow-up local commit.
Nothing pushed. The frontier is 11, 13 and 14; first by number is 11.

### 2026-10-26 — Author confirmation

After the backend restart guidance and suggested web-app check, the author reported "i think we
are good" and explicitly requested T10 be marked resolved. Author acceptance recorded; status
remains resolved. Next ticket by number is 11.
