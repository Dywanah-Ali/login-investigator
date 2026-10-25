# 40: The full phase 1 question set

Type: build
Status: ready-for-agent
Blocked by: 29
Phase: 1

## What to build

The knowledge-base question file grows from the first handful to about 30 questions, weighted to
say-no and mixed questions, with lookups as the control group. Every question carries a provenance
line and gold IDs or an expected verdict.

## Decisions implemented

- T06 d3 (about 30 questions: about 10 say-no, namely three twins, four absent topics, two
  false-presupposition traps and one underspecified; about 12 mixed and multi-hop, at least two
  through a busy node; about 8 graph and text lookups as the control group; B3 asked about the
  laptop change directly).
- [review ruling 2] the gold items choose the checks.
- User stories 14, 71.

## Acceptance criteria

- [ ] About 30 questions with the T06 d3 mix; the actual counts are recorded.
- [ ] B3's question asks about the laptop change directly.
- [ ] Every question carries a provenance line and gold IDs or an expected verdict; ticket 21's test
      passes on the full file.
- [ ] No question overlaps the tuning file.
- [ ] The full file runs through the eval; the results are recorded per question, and every failure
      is fixed or logged in the bug log with its cause.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review has run with its findings triaged
      (`mp-code-review` in Claude Code, `code-review` in Codex).

## Comments
