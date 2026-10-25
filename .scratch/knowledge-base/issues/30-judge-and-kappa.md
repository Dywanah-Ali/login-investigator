# 30: The faithfulness judge and kappa

Type: build
Status: ready-for-agent
Blocked by: 29
Phase: 0

## What to build

A faithfulness judge from another model family checks whether each claim in a sample of answers is
backed by the retrieved context. It reports a rate with its interval as a smoke alarm and never
fails a run. Once the author has labelled answers, the runner reports how far the judge agrees with
the author.

## Decisions implemented

- T06 d6 (a stronger model from another family through OpenRouter; binary per claim with fixed
  steps; reason before verdict; markdown stripped first; three trials with majority; about ten
  answers per run; every verdict and reason stored; reported with its interval; never a gate in
  phase 1; judge prompt and model hashed into the fingerprint; agreement as Cohen's kappa computed in
  code).
- T07 d8 (the judge's reason stays off the screen).
- User story 80. Spec door 6.

## Acceptance criteria

- [ ] The judge model is chosen and recorded with its reason under this ticket's Answer.
- [ ] The judge grades each claim pass or fail with fixed steps, reason before verdict, on text with
      markdown stripped.
- [ ] Three trials per claim with a majority; about ten answers per run; every verdict and reason
      stored in the run file.
- [ ] The rate is reported with its interval and never fails a run.
- [ ] The judge prompt and model are hashed into the fingerprint.
- [ ] Cohen's kappa is computed in code; a test checks it on known values.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and Codex reviews the change.

## Comments
