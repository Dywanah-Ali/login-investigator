# 41: The on-versus-off comparisons

Type: build
Status: ready-for-agent
Blocked by: 39, 40
Phase: 1
Model: strongest if budget allows (Fable 5.1 or Astra), otherwise standard (Opus 5.5 or Sol 6.1)

## What to build

The re-ranker and BM25 each earn their place by measurement. Each runs on and off over the retrieval
layer on the same questions; a switch stays on only if it helps, a tie goes to off, and no setting
wins if refusal stops working with it.

## Decisions implemented

- T06 d9 (on-versus-off over the retrieval layer; a switch stays on only if it passes more questions
  on the second retrieval check, or the same number with better first-gold ranks; a tie goes to off;
  recorded at phase 1's close).
- [review ruling 3] a setting wins only if the say-no checks pass with it, verdicts included; if the
  re-ranker off cannot give `none` where needed, it stays on and the reason is recorded.
- T02 d3 (BM25 only if the comparison says so). BM25 is built as a switchable keyword leg for the
  comparison and kept only if it wins.
- User story 79.
- T45 closing decision 4 (8 November 2026): retain the current PostgreSQL baseline initially
  and validate focused searches. Record matching/query-construction differences between
  variants so their effect is not misattributed to BM25 scoring. Earlier acceptance failures
  must be resolved before acceptance; this comparison does not waive phase-0 requirements.


## Acceptance criteria

- [ ] Use T45's approved 8 November path/stage records without changing the switch/refusal
      comparison rule. Keep question/source/budget configuration comparable and record candidate
      admission separately from delivered evidence. The legacy corpus-only top-20 diagnostic
      cannot stand in for the graph-assisted pipeline's delivery result.

- [ ] Before any build work starts, the builder tells the author this ticket's `Model:` line and
      asks the author to set that model. The build starts only after the author confirms, and a
      dated line under Comments records the model used.
- [ ] BM25 exists as a switchable keyword leg; its build is recorded.
- [ ] The re-ranker and BM25 each run on and off over the retrieval layer on the full question set.
- [ ] Each result applies the T06 d9 rule and the refusal condition; ticket 39's off-threshold is
      used for the re-ranker-off runs.
- [ ] The outcome per switch and its reason are written as decisions-log rows in the spec.
- [ ] A switch that loses is left off, and the code path that serves it is either kept behind the
      switch or removed, with the choice recorded.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged.

## Comments

- 2026-11-08 — T58 owns the initial combined retrieval implementation, including explicit
  reranker-off/failure handling. This ticket retains measured switch/BM25 comparison and refusal
  requirements. Reuse its stage receipts and report budget/matching differences. A later
  comparison cannot waive an earlier failed phase-0 acceptance path.
