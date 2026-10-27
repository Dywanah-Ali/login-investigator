# 22: Hybrid search and the retrieval layer alone

Type: build
Status: ready-for-agent
Blocked by: 19, 21
Phase: 0
Model: strongest (Fable 5.1 or Astra)

## What to build

The knowledge-base door gains corpus search: a vector leg and a keyword leg, filtered before their
limits and fused by our own reciprocal rank fusion, returning a verdict of `none`, `weak` or `found`
with the chunks. A retrieval runner calls the search and the graph walk directly, with no model, and
checks the first questions' gold IDs on every build.

## Decisions implemented

- T02 d3 (PostgreSQL's built-in text ranking first), T02 d10 and T03 d7 (our own fusion, k = 60,
  equal legs, 20 plus 20, 1-based ranks, every score recorded, three library traps each with a
  test), T03 d6 (filters inside both legs before their limits, exact vector search, typed options),
  T03 d1 (three verdicts computed in code; the `none` rule stays off until ticket 39).
- T06 d1 (retrieval gate, first check), T06 d2 (graph gate), T06 d8 (the retrieval layer alone, with
  the integrity check as its precondition).
- User stories 72, 73, 77. Spec door 2.

## Acceptance criteria

- [ ] Search runs a vector leg and a keyword leg; filters apply inside both before their limits;
      vector search is exact with no approximate index.
- [ ] Fusion is our own, k = 60, equal legs, 20 plus 20 candidates, 1-based ranks. Each candidate
      records its dense rank, keyword rank, raw cosine distance, raw keyword score and fused score.
- [ ] Three trap tests: the fusion function is set explicitly; both candidate limits are set
      explicitly; a fresh configuration is built per call, proven by a two-question regression test.
- [ ] The verdict is computed in code from recorded scores; the `none` rule is off and its switch is
      tested.
- [ ] Door 2 tests use the fake embedder.
- [ ] The retrieval runner calls search and walk directly, runs the integrity check first, checks
      every gold chunk ID among the 20 fused candidates, records the rank of the first gold chunk,
      and checks the walk returns exactly the gold record set.
- [ ] The first real run on the first questions is recorded per question. Every miss is fixed or
      logged in the bug log with its cause.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged.

## Comments
