# 38: The Graph tab click rule

Type: build
Status: ready-for-agent
Blocked by: 37
Phase: 1
Model: standard (Opus 5.5 or Sol 6.1)

## What to build

A click on the graph ties the picture to the proof. A click on an edge switches to the Evidence tab
and lights its row and hop line; a click on a node lights every evidence row that touches it. An
edge the walk returned but the answer never cited says so, with its record ID.

## Decisions implemented

- T08 d5 (the click rule, including the uncited case: "Walked, not cited in the answer" with the
  record ID).
- API contract change 2 (an edge's `label` is the citation whose resolved records contain it, or
  `null` when uncited).
- User stories 43 to 45.

## Acceptance criteria

- [ ] Before any build work starts, the builder tells the author this ticket's `Model:` line and
      asks the author to set that model. The build starts only after the author confirms, and a
      dated line under Comments records the model used.
- [ ] A click on an edge switches to the Evidence tab and lights its row and hop line.
- [ ] A click on a node lights every evidence row that touches it.
- [ ] An uncited edge shows "Walked, not cited in the answer" with its record ID.
- [ ] Door 5 tests with the fake API cover each click, the tab switch and the uncited case.
- [ ] The author checks on S6 that every drawn edge matches a hop line or a "walked, not cited" line;
      a dated line records it.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged.

## Comments
