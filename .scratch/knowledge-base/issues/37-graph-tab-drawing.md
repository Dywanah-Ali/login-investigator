# 37: The Graph tab drawing

Type: build
Status: ready-for-agent
Blocked by: 26, 33
Phase: 1

## What to build

The Graph tab draws the walk the agent made for the answer the analyst is reading, and nothing else.
It is laid out top to bottom in playbook order, with shape for type, the account under
investigation as the one dark node and restricted assets marked with a small red R. The many are
folded into one node with a count. The picture is read-only.

## Decisions implemented

- T08 d1 (the walk only, projected from the saved artifact), T08 d3 (organisation nodes only, the
  many folded with a count), T08 d4 (layered by playbook step), T08 d6 (the drawing rules: shape per
  type, dark focus node, red R, relation labels, one label per fan, side-routed row-skipping edges,
  small arrowheads, plain clipped labels with hover, no step captions, a header and a legend), T08 d7
  (the empty state), T08 d8 (React Flow plus dagre, read-only, nodes as our own components in the
  app's colour variables, own SVG plus dagre as fallback, licences recorded).
- API contract change 2 (`graph` on turns where a graph tool ran, projected through the one
  resolver). The `fold:` prefix and `members` for folded nodes are Claude's design from T08 and were
  not covered by Codex's review of the spec.
- User stories 37 to 42, 46 to 48.

## Acceptance criteria

- [ ] Reopen turns gain `graph` where a graph tool ran, projected through ticket 27's resolver; the
      API contract is updated first.
- [ ] The `fold:` naming and `members` are confirmed or changed, recorded under this ticket's Answer,
      and covered by Codex's review of this ticket.
- [ ] Door 4 test: the graph holds only nodes and edges the walk returned.
- [ ] React Flow and dagre draw the walk with every T08 d6 drawing rule; licences are recorded.
- [ ] A test proves dragging, connecting and deleting are switched off; the list of switched-off
      behaviours is recorded.
- [ ] Every label renders as plain text, clipped when long, with the full value and record ID on
      hover.
- [ ] The empty-state line shows when no walk ran.
- [ ] Door 5 tests with the fake API cover the drawing, the fold and the empty state.
- [ ] The author's screenshot review in light and dark mode settles spacing, node sizes and shades,
      recorded as a dated line.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged.

## Comments
