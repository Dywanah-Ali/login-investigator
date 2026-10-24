# 08: The read-only graph screen and the Gephi export

Type: research, then prototype, then grilling (retyped 25 October 2026)
Status: resolved
Blocked by: 02, 07

## Question

Ticket 02, decision 2, promised "a read-only graph screen of our own in the React frontend,
designed in ticket 07" and "export to Gephi (standard graph file from NetworkX) for free
exploration". Ticket 07 designed the explained-alert screen and never took the graph screen up;
its answer shows graph paths as text lines only. This ticket takes up the promise.

What does the analyst see on the graph screen, what slice of the graph does it show, where does it
sit in the Port's shell, and how does the app produce the Gephi file?

## Scope

- **What the screen shows.** Candidates: the neighbourhood of one finding (the blast radius of
  ticket 05's `investigate_alert`, drawn), the neighbourhood of one account or asset, or the whole
  organisation with filters. Phase 1's slice is blast radius, so the finding's neighbourhood is
  the likely first view; the others are candidates for later phases unless the prototype says
  otherwise.
- **Where it sits.** A route of its own in the Port's shell, a tab beside the evidence panel of
  ticket 07, or a link from a graph citation (G labels). The Port's shell and shadcn/ui pieces,
  as every screen so far.
- **How it is drawn.** A drawing library in React (a spec decision, with the bundle size, licence
  and maintenance checked), or an SVG of our own for a small neighbourhood. Node and edge labels
  are log and graph fields and stay plain text: never through a renderer that produces markup.
- **Read-only.** No editing, no layout saved to the server, nothing written anywhere. The files are
  the truth (ticket 02, decision 6).
- **The API contract addition.** One endpoint that returns nodes and edges for the chosen scope,
  written before the build, returning only the fields the screen needs. The payload comes from the
  same named traversal functions the agent's tools and the eval's graph gate use (ticket 06,
  decision 2), so screen, tool and exam cannot disagree.
- **The Gephi export.** A core function writing a standard file from the NetworkX graph (GEXF or
  GraphML, NetworkX writes both) for the whole dataset or one neighbourhood; whether it is a
  script, an API download or both; what evidence proves the file opens in Gephi.
- **Evidence for the gates.** What the phase 1 gate "author accepts the live screen" means for
  this screen, and whether the eval needs any check beyond ticket 06's graph gate (the leaning is
  no: the walk is already graded and the screen only draws its output).

## Acceptance

- [x] Prototype of the candidate views reviewed with the author in the browser; the view, the
      placement and the drawing approach chosen (decisions 1, 2, 8).
- [x] API contract addition drafted for the graph endpoint (the section under the Answer).
- [x] Gephi export shape decided with its evidence (decision 9).
- [x] Decision recorded here under `## Answer`.

## Comments

**2026-10-24, opened.** The author noticed, while checking ticket 02's decision 2 against ticket 06,
that the graph screen promised there was never designed. Ticket 07's question, scope and answer do
not mention it; the Gephi export appears in no ticket after 02 and in no build list. The author
chose a new ticket over reopening 07, so that 07's evidence stays intact and the screen gets its
own prototype, under the author's ruling of 24 October 2026 that a screen cannot be decided from a
description. Same order of work as ticket 07: prototype first, then the grilling with the picture
in front of the author, one question at a time with a plain heading each.

**2026-10-25, claimed and retyped.** The author asked for a short best-practice research step before
the prototype, after a mutual-understanding round. The author's picture, confirmed in that round:
the graph is a panel in the investigator screen's third column, to the right of the evidence
panel, the space the Port left empty on purpose; it appears whenever the agent's answer involved a
graph walk, full investigation or partial; it draws only the nodes and edges the walk touched, with
the walk's direction, not the whole organisation with highlights (the author's lean, to be tested
by the research); library versus own SVG is open. The Gephi export was explained as a builder's
tool, not an analyst's: one function writing the NetworkX graph to GEXF or GraphML so the whole
synthetic organisation can be inspected by eye in Gephi during phase 0. Five research questions
agreed: (1) walk-only subgraph or whole graph with highlights, as security investigation tools do
it; (2) how a small walked path is drawn well and what misleads; (3) React drawing library versus
own SVG, with bundle size, licence, maintenance and plain-text labels; (4) the shape of the
nodes-and-edges payload carrying direction and hop order; (5) GEXF versus GraphML for Gephi, script
or download, and the proof the file opens. Findings go to `research/08-graph-screen.md`.

**2026-10-25, research done.** [Research note 08](../research/08-graph-screen.md) written. Its
recommendation, for the author to rule on in the grilling: draw the walk's subgraph only, which every
investigation tool examined does (BloodHound, Neo4j Bloom, Defender XDR, Elastic); a Graph tab beside
Evidence in the third column rather than a fourth column; React Flow plus dagre in read-only mode
with own SVG as fallback; a payload that projects the saved artifact with `focus`, `type` and `step`
fields; GEXF by script with no download endpoint, proved by a write-and-read-back test and the
author opening the file in Gephi Lite. One conflict surfaced: the author's "right of the evidence
panel" would be a fourth column in a three-column shell; both are drawn in the prototype.

**2026-10-25, prototype built.** [Prototype](../research/08-graph-panel-prototype.html), served
locally and checked in Chrome on four screens with no console errors. Screen 1 is ticket 07's S6
answer with the walk drawn in the right-hand space and seven option boxes: what the panel shows
(walk only, walk plus ghosts, whole organisation highlighted), where it sits (tab, stacked, fourth
column), documents drawn or not, the many collapsed or every node, what a click does, and the
drawing rules used. Screen 2 is B1's tiny walk. Screen 3 is an answer with no walk (empty state or
hidden tab). Screen 4 is the Gephi export (script only or a download too), the GEXF the file
holds, and the evidence list. The drawing is hand-placed SVG in a layered top-to-bottom layout by
playbook step; edges that skip a row are routed round the side; fans of identical edges carry one
label. Next: the grilling, one question at a time, with the prototype open.

## Answer

Resolved 25 October 2026 after a research note, a prototype review and a nine-point grilling with
the prototype open, one question at a time. The research is
[research note 08](../research/08-graph-screen.md); the prototype is
[`08-graph-panel-prototype.html`](../research/08-graph-panel-prototype.html), whose defaults show
the chosen set with the rejected options still available as buttons for the record. The author
took every recommendation and sharpened two of them (decisions 5 and 6's caption rule) from the
prototype.

**The shape.** The graph is not a screen of its own. It is a panel in the investigator's third
column, a Graph tab beside the Evidence tab of ticket 07, that draws the walk the agent made for
the answer being read. The report and the map are drawn from the same saved artifact, so the map
cannot say anything the report did not.

| # | Decision | Why |
|---|---|---|
| 1 | **The panel draws the walk only**: the nodes and edges the investigation returned, nothing else. No ghost neighbours, no whole organisation with highlights. Context beyond the walk is a later feature, as expansion on demand, never drawn by default. | Every investigation tool examined does this (BloodHound, Neo4j Bloom, Defender XDR, Elastic). Phantom edges the walk did not return are the one trap the research found, Neo4j Browser's default. |
| 2 | **A Graph tab in the third column**, beside the Evidence tab. The right-hand column stays one column; it collapses under the chat on narrow screens as ticket 07 decided. The stacked and fourth-column placements are not taken. | The author's first words were "right of the evidence panel"; the prototype showed the fourth column narrowing the chat, and the author chose the tab. The stacked placement is the fallback if flipping tabs proves tiresome on the live screen. |
| 3 | **Organisation nodes only** in phase 1: people, groups, assets, devices, networks. Document chunks and their `mentions` edges are not drawn; documents stay in the Evidence tab where their text is readable. | Documents on the map add nodes without adding a path. |
| 4 | **The many are collapsed with a count.** Restricted assets are drawn one by one; internal assets and the peers that share an address fold into one node each carrying a count. The fold follows ticket 05's `truncated` flags and ticket 07's counts-first rule. | A wide radius must not make the panel long; the four restricted assets are the point and stay visible. |
| 5 | **A click lights the record and brings it into view.** Clicking an edge switches the panel to the Evidence tab, scrolls to the row whose citation contains that record and highlights it; the hop line in the answer lights too. Clicking a node highlights every row whose citation touches that node. Clicking a collapsed node lands on the row that holds the full list. An edge the walk returned but the answer never cited shows a quiet line, "Walked, not cited in the answer", with its record ID. Clicking a label in the answer or a row in Evidence keeps ticket 07's behaviour and does not force the Graph tab open. No menu, no expansion, no drag that persists. | The author's sharpening: a highlight in a hidden tab is not a highlight. Rows and records are not one-to-one (one citation can hold four grants; one node sits in three citations), so the rule names each case. |
| 6 | **The drawing rules.** Layered layout, top to bottom in playbook order: the account, then groups, then assets, then shared devices and addresses, then peers. Positions are computed from the payload the same way every time. Shape says type: circle for a person, rounded box for a group, square for an asset, diamond for a device, pill for an address. The focus account is the one dark element, in line with ticket 07's hierarchy; restricted assets carry a small red R in the severity red. Edge labels are the relation from the source table (member of, granted, assigned, used address); fans of identical edges carry one label; edges that skip a row are routed round the side; arrowheads are small and outside the node. Every label is a plain string, clipped when long, with the full value and record ID on hover. **No step captions on the rows** (author, from the prototype): the shapes and the order carry it. A header line names the finding and the node count; a legend sits under the drawing. | From research note 08, section 3.2. The caption rule is the author's: captions made the panel busy for no added value. |
| 7 | **Empty state, never a moving tab.** The Graph tab is always present. On an answer with no graph walk it shows one quiet line: no graph was walked for this answer. | A control that moves is harder to learn than one that is sometimes quiet. |
| 8 | **React Flow plus dagre, read-only.** Nodes are our own React components, so the shapes, curves, header and legend of the prototype come back as our markup in the app's colour variables; dagre computes the layered positions. Dragging, connecting and deleting are switched off, with a test that asserts they stay off. Own SVG plus dagre is the recorded fallback if the switch-off list proves heavy in the build; Cytoscape.js, Sigma.js and vis-network are not taken. Bundle cost about 74 kB compressed, both MIT. | Pan, zoom, fit-to-view, keyboard focus and ARIA come built in; a label is a React string, so the plain-text rule holds by construction. The layered layout fits a path with a start node and a few hops. |
| 9 | **The Gephi export is a script writing GEXF, no download endpoint.** One core function sets `viz` colour by node type and writes the whole graph, or one finding's neighbourhood, with NetworkX's `write_gexf`. GraphML is not taken. Evidence: a unit test writes the pinned dataset, reads it back with `read_gexf` and asserts node and edge counts per type against the integrity check of ticket 06; a second test fails loudly on a reserved attribute name (`id`, `label`, `pid`); and the author opens the file in Gephi Lite in the browser once, recorded as the author's look with its date, never as a screenshot. | A builder's wall chart, not an analyst's map. GEXF carries colour and size; Gephi's GraphML import drops them. A download would push every table through the API for a builder's task, against the rule that the API returns only what the screen needs. |

### API contract addition (draft, for the spec)

One change to `docs/api-contract.md`, to be made when the spec is written, beside ticket 07's
additions. Nothing else in the contract moves.

**Investigations: reopen.** Each turn where a graph tool ran gains `"graph"`, projected in the API
from the saved artifact, never from the model's text and never from a fresh walk:

```json
"graph": {
  "focus": "user-0017",
  "nodes": [
    {"id": "user-0017", "type": "person", "label": "mgarcia", "sub": "IT · Operations office"},
    {"id": "group-it-admins", "type": "group", "label": "IT Admins", "sub": "4 members"},
    {"id": "asset-dc01", "type": "asset", "label": "domain controller", "sensitivity": "restricted"},
    {"id": "fold:peers:net-vpn3", "type": "person", "label": "9 peers", "count": 9,
     "members": ["user-0021", "user-0022", "…"]}
  ],
  "edges": [
    {"id": "mem-0117", "source": "user-0017", "target": "group-it-admins",
     "type": "member of", "step": 1, "label": "G1"},
    {"id": "grant-0033", "source": "group-it-admins", "target": "asset-dc01",
     "type": "granted", "step": 2, "label": "G2"},
    {"id": "net-0007", "source": "fold:peers:net-vpn3", "target": "net-vpn3",
     "type": "used address", "step": 3, "label": null}
  ]
}
```

`id` is the ground-truth record ID (ticket 05, decision 5); a folded node's `id` is prefixed
`fold:` and carries its `members`. `type` on a node is one of `person`, `group`, `asset`,
`device`, `network`; on an edge it is the relation from the source table. `step` is the playbook
step that produced the edge, which ties it to ticket 07's hop lines and step stack. `label` is the
citation label whose resolved records contain this edge, or `null` when the walk returned it and
the answer did not cite it. `label` and `sub` render as plain text only. Direction is the walk's
direction, `source` to `target`. The turn's `evidence` (ticket 07) already maps each label to its
record IDs; the frontend joins the two. No separate route: the graph travels with the turn, and
`GET /api/investigations/{id}/artifact.json` carries it with the rest.

### Considered, not taken

- Ghost neighbours and the whole organisation highlighted (decision 1).
- Stacked in the third column, a fourth column, a route of its own (decision 2).
- Documents as nodes in phase 1 (decision 3); they may return when phase 2 adds incident write-ups.
- Every node drawn (decision 4).
- A click that only highlights without switching tabs, and a click that does nothing (decision 5).
- Step captions on the rows (decision 6).
- A hidden Graph tab when there is nothing to draw (decision 7).
- Own SVG, Cytoscape.js, Sigma.js, vis-network (decision 8).
- GraphML; a download endpoint (decision 9).
- A graph endpoint that re-walks the graph instead of projecting the artifact (payload).

### Hand-offs

- **The spec (`mp-to-spec`):** the Graph tab as a shadcn piece inside ticket 07's third column;
  the `graph` field above in `docs/api-contract.md`; React Flow and dagre as new frontend
  dependencies with their licences recorded; the read-only test; the click rule of decision 5
  including the uncited case; the drawing rules of decision 6 as a named rule the build ticket
  checks with the author's screenshot review, dark mode included; the GEXF script and its two
  tests; the author's Gephi Lite look as a dated line on the build ticket.
- **Phase 0 build:** the export script and its tests, after the integrity check of ticket 06
  exists, since the test compares against it. The payload projection shares the citation resolver
  of ticket 07 and the eval's `cites` check (ticket 06, decision 5).
- **Phase 1 acceptance:** the author accepts the live Graph tab on S6, on one benign twin and on
  one answer with no walk, with every drawn edge matching a hop line or a "walked, not cited"
  line. No eval question is added: ticket 06's graph gate grades the walk and the panel only draws
  its output.
