# 19: The graph, its integrity check and the S6 radius test

Type: build
Status: ready-for-agent
Blocked by: 12, 17
Phase: 0
Model: strongest (Fable 5.1 or Astra)

## What to build

The knowledge-base door in the core opens a dataset's knowledge base and builds the graph in
NetworkX from the database's tables, with chunks as nodes joined by `mentions` edges and the
`used address` edges drawn from the log. An integrity check runs every time the graph is built and
fails on the first mismatch. One core function computes a finding's blast radius, and a test proves
it gives exactly the S6 radius written in `truth.json`.

## Decisions implemented

- T02 d2 (walked in NetworkX, built in memory, named traversal functions), T02 d7 (chunks as nodes
  with `mentions` edges).
- [review ruling 1] `used address` edges come from the log, one per distinct user and address pair
  for addresses in the networks table, never copied into a table; the integrity check compares
  identities, not only counts; a chunk may have no `mentions` edge; no isolated person, group, asset
  or device.
- T05 R5 (code walks, the agent reads: one radius function, shared by the tool and the answer-key
  test). The hop-by-hop walk is a phase 4 seam, not built.
- T06 comment of 24 October 2026 (the integrity check).
- Author's ruling of 25 October 2026 at the ticket cut: the answer-key radius test lives here, at
  door 2, instead of at the generator's door.
- User stories 57, 69. Spec door 2.

## Acceptance criteria

- [ ] One function opens a dataset's knowledge base; the graph is built in NetworkX from the tables,
      with chunk nodes and `mentions` edges.
- [ ] `used address` edges are drawn from the log. The row filter (for example, successful sign-ins
      only) is fixed here and written beside the radius in `truth.json`.
- [ ] The integrity check reads its sources with its own code and checks every row of the spec's
      table: node ID sets per type, the node attributes a walk reads, link edge sets by source,
      target and type, the `used address` set from the log with the same filter, chunk node IDs, and
      each chunk's `mentions` edges including an empty set. No person, group, asset or device is
      isolated.
- [ ] Corruption tests: each check fails when its input is broken once; swapping two valid link
      endpoints without changing any count fails; changing an attribute a walk reads fails; a chunk
      naming no entity passes; an unused network address passes.
- [ ] One core function computes a finding's radius, already joined: groups held, assets reached,
      peers by device and by network address that week.
- [ ] A test recomputes S6's radius from the tables through that function and matches `truth.json`
      exactly.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged.

## Comments

- 2026-10-26, consequence of the author's ruling at ticket 11: `device_id` is empty on attacker rows
  and on employee sign-ins from a phone. An empty value is not a device: it makes no device edge,
  and rows with an empty device are never peers of each other by device.
