# 20: The Gephi export

Type: build
Status: resolved
Blocked by: 13, 19
Phase: 0
Model: standard (Opus 5.5 or Sol 6.1)

## What to build

A script writes the whole graph, or one finding's neighbourhood, as a GEXF file that the author opens
in Gephi Lite to inspect the synthetic organisation by eye. There is no download endpoint.

## Decisions implemented

- T08 d9 (GEXF export by a script calling one core function, colour by node type, no endpoint, two
  tests, the author's look; attribute names never `id`, `label` or `pid`).
- User story 70. Spec door 2.

## Acceptance criteria

- [x] Before any build work starts, the builder tells the author this ticket's `Model:` line and
      asks the author to set that model. The build starts only after the author confirms, and a
      dated line under Comments records the model used.
- [x] A script calls one core function that sets colour by node type and writes the whole graph, or
      one finding's neighbourhood by finding ID, as GEXF.
- [x] No API endpoint serves the file.
- [x] Test: the file is written, read back, and its node and edge counts per type match the
      integrity check's.
- [x] Test: no attribute is named `id`, `label` or `pid`.
- [x] The author opens the whole-graph file in Gephi Lite; a dated line records the look.
- [x] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged.

## Comments

Blocked by 13 as well as 19: the neighbourhood export is chosen by finding ID. This edge was added
while writing the ticket, after the author approved the breakdown.

- 2026-10-28, Claude: the author confirmed the model is set. Model used: Claude Opus 5.5, matching
  the ticket's standard line.

- 2026-10-28 — Claude: NetworkX 3.6.1; documentation: Context Hub `networkx/package` (no GEXF
  coverage), then [write_gexf — NetworkX 3.6.1 documentation](https://networkx.org/documentation/stable/reference/readwrite/generated/networkx.readwrite.gexf.write_gexf.html),
  via Keenable; checked: `viz` colour as node data, and the warning that `id`, `pid` and `label`
  are consumed as GEXF metadata rather than written as attributes. The page does not cover
  multigraphs or value types, so the installed `networkx/readwrite/gexf.py` source was read as
  alternative evidence (not a documentation lookup): multigraph keys are written as the attribute
  `networkx_key` and read back as edge keys; `start`, `end`, `parents`, `spells`, `slices` and
  `viz` are also consumed on nodes, and `weight` and `type` on edges; `None` and tuples raise
  `TypeError`; a list is treated as dynamic `(value, start, end)` data.

- 2026-10-28, Claude: build complete; the author's Gephi Lite look is pending.
  - **Shape.** `knowledge_base/gexf.py` holds `write_gexf`, `finding_neighbourhood` and
    `NODE_COLOURS`. `KnowledgeBase.export_gexf(path, finding_id=None)` is the one core function.
    `scripts/export_graph.py` opens the published knowledge base as the read-only role, after the
    app's staleness check, and calls it. `check_graph_integrity` now returns `GraphCounts`, the
    per-type node and relationship counts it derives from the sources, so the read-back test
    compares against the check's own counts, not against the graph it exported.
  - **Builder's choices for the author to confirm or overrule.**
    1. *Neighbourhood* means the finding's radius walk, as T08's prototype describes it ("one
       neighbourhood (S6's radius) to compare with the panel's drawing"): the accounts reached,
       their groups and assets, device peers and shared-address accounts, organisation nodes only,
       with only the edges the walk used. No chunks, no `assigned_device` edges.
    2. A finding that reaches no account (a spray with no success) is refused, not written as an
       empty file.
    3. The refused attribute names are every name NetworkX's writer consumes or renames, not only
       `id`, `label` and `pid`. A future column named `type` or `start` would stop the export
       loudly instead of vanishing from the file.
    4. Values the writer cannot hold are converted: login times become comma-joined text, chunk
       metadata becomes JSON, an empty value is left out.
    5. An output path inside the dataset folder is refused (B-096): the file would change the
       folder's fingerprint and make the build stale.
  - **Latent.** Neighbourhood edges carry all their login times. No period is passed today, so this
    equals the walk's period; a future period option must filter them.
  - **Tests** (`tests/test_graph_export.py`, 10): whole graph and S6 neighbourhood read back, counts
    per type equal to the integrity check's, colours per type, no `id`/`label`/`pid` declared and
    the wider set absent except the writer's own `networkx_key`; S6's neighbourhood equal to the
    answer key's nodes and edges; reserved names refused on nodes and edges with no file written;
    the device-peer branch; the script's success, unknown finding, dataset-folder and nothing-built
    refusals; no API module mentions the export.
  - **Live export** from `li_kb_fe13d09e32f4`: whole graph 490 nodes and 583 edges, equal to
    T19's live reader evidence; S6 neighbourhood (`F-password-spraying-d06a7545`) 55 nodes and 64
    edges. Files: `.scratch/knowledge-base/evidence/20-graph.gexf` (898 KB) and
    `20-s6-neighbourhood.gexf` (65 KB).
  - **Safety net.** 622 backend tests passed in 226 s; pyright 0 errors; frontend 149 passed,
    typecheck exit 0, lint exit 0 with the six existing AUD-009 warnings (frontend untouched). The
    Port's API eval was not run: no agent, tool or prompt changed.
  - **Review.** Two-axis review triaged in
    [reviews/20-code-review-2026-10-28.md](../reviews/20-code-review-2026-10-28.md): six Standards
    points and one Spec point fixed; the rest kept with reasons or recorded above.

- 2026-10-28, Claude: the author's first look at the S6 neighbourhood in Gephi Lite showed every
  node grey (B-097). Cause: Gephi Lite ignores a `viz:color` with an alpha value
  ([gephi-lite issue #307](https://github.com/gephi/gephi-lite/issues/307), read via Keenable),
  and NetworkX always writes one. Reproduced with an alpha-free copy, which the author saw in
  colour. `write_gexf` now removes the alpha between NetworkX's own writer steps; a test asserts
  every colour has only `r`, `g` and `b`. Both live files regenerated: whole graph still 490
  nodes and 583 edges, no alpha; the S6 file is byte-identical to the copy the author saw.

- 2026-10-28, the author's look in Gephi Lite (recorded by Claude): after the B-097 fix the
  colours show by node type. The author found the S6 neighbourhood file readable and the
  whole-graph file `20-graph.gexf` too busy: 320 of its 490 nodes and 257 of its 583 edges are
  chunks and their `mentions` links. **Author's ruling:** keep the whole-graph file complete, as
  decision 9 asks, and hide chunks with Gephi Lite's filter on `entity_type` when a clean view
  of the organisation is wanted. No code change; no organisation-only option.

- 2026-10-28, **author's ruling:** the five builder's choices above (neighbourhood as the radius
  walk with organisation nodes only; refusal of a finding that reaches no account; the wider
  reserved-name set; text and JSON conversion with empty values left out; refusal of an output
  inside the dataset folder) are accepted as written. T20 resolved. Every acceptance criterion has
  its evidence above; the full backend suite passed again after B-097, 622 tests in 189 s.
  Nothing pushed. Next frontier: ticket 21; ticket 24 is also unblocked.
