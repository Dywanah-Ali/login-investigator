# 39: Calibration and the `none` rule

Type: build
Status: ready-for-agent
Blocked by: 23, 29
Phase: 1

## What to build

The refusal threshold is chosen from evidence, not guessed. The author labels a separate tuning file
of query and chunk pairs; the re-ranker scores them once; the threshold is chosen offline from the
saved scores. Then the `none` rule is switched on, so the agent says plainly when the knowledge base
has nothing on a question.

## Decisions implemented

- T06 d4 (a separate tuning file of 30 to 60 pairs labelled by the author, scored once by the
  re-ranker, scores saved, threshold chosen offline, never overlapping the test questions), T03 d1
  (the `none` rule off until calibrated), T06 d9 (with the re-ranker off, the tuning file is
  re-scored with the remaining score source).
- User stories 28, 78.

## Acceptance criteria

- [ ] The tuning file holds 30 to 60 query and chunk pairs, each with `split: tune`, labelled by the
      author; a dated line records the labelling.
- [ ] A test proves no tuning pair overlaps a test question.
- [ ] The re-ranker scores the pairs once and the scores are saved.
- [ ] The threshold is chosen offline from the saved scores; the method and the value are recorded
      under this ticket's Answer.
- [ ] The tuning file is also re-scored with the score source left when the re-ranker is off, and
      that threshold is recorded for ticket 41.
- [ ] The `none` rule is switched on; the say-no checks on the first questions pass.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and Codex reviews the change.

## Comments
