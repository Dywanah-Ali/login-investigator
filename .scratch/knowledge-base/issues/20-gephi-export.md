# 20: The Gephi export

Type: build
Status: ready-for-agent
Blocked by: 13, 19
Phase: 0

## What to build

A script writes the whole graph, or one finding's neighbourhood, as a GEXF file that the author opens
in Gephi Lite to inspect the synthetic organisation by eye. There is no download endpoint.

## Decisions implemented

- T08 d9 (GEXF export by a script calling one core function, colour by node type, no endpoint, two
  tests, the author's look; attribute names never `id`, `label` or `pid`).
- User story 70. Spec door 2.

## Acceptance criteria

- [ ] A script calls one core function that sets colour by node type and writes the whole graph, or
      one finding's neighbourhood by finding ID, as GEXF.
- [ ] No API endpoint serves the file.
- [ ] Test: the file is written, read back, and its node and edge counts per type match the
      integrity check's.
- [ ] Test: no attribute is named `id`, `label` or `pid`.
- [ ] The author opens the whole-graph file in Gephi Lite; a dated line records the look.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged.

## Comments

Blocked by 13 as well as 19: the neighbourhood export is chosen by finding ID. This edge was added
while writing the ticket, after the author approved the breakdown.
