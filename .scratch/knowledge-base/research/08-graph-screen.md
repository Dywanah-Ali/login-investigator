# Research note 08: the read-only graph panel and the Gephi export: what investigation tools draw, how a small walked path is drawn well, the drawing library, the payload, and the export file

Ticket: [08-graph-screen-and-gephi-export](../issues/08-graph-screen-and-gephi-export.md)
Date: 25 October 2026
Method: Keenable first, as the global rule asks (`search_web_pages`, then `fetch_page_content` on
primary pages). Thirteen searches, most restricted to primary domains (bloodhound.specterops.io,
neo4j.com, learn.microsoft.com, elastic.co, cambridge-intelligence.com, networkx.org, gephi.org,
reactflow.dev). Twenty-four page fetches; two hit Keenable's rate limit on the first try and
succeeded on the retry; none failed otherwise. Perplexity was not needed because Keenable never
returned empty. Direct reads of the project's own tickets 05 and 07 for the artifact shape and the
screen decisions. No project data, log field or corpus text was sent anywhere; every query was a
generic technical question. `[P]` marks a claim verified on a primary page opened in this research
(vendor documentation, the library's own site or repository, npm, Bundlephobia); `[V]` marks a claim
seen only through a search snippet, a community forum or an aggregator. Bundle sizes are
Bundlephobia's minified-plus-gzipped figures on 25 October 2026 and will drift.

**Fixed constraints from the tickets (not reopened here).** The graph is walked in NetworkX built
from the ground-truth tables (ticket 02, decision 2); chunks are nodes with `mentions` edges
(decision 7); the files are the truth and nothing is written back (decision 6). Every knowledge-base
tool returns short content for the model plus a full artifact saved by the checkpointer and read by
the eval and the screen (ticket 05, decision 4); graph record IDs are the ground-truth IDs
(decision 5); the radii are paged with a `truncated` flag and full lists in the artifact
(decision 12); `investigate_alert` computes the radius in one core function and returns it joined
(ticket 05, section 3). Citations land in an evidence panel, a third column right of the chat,
built from the saved artifact (ticket 07, decision 1); a graph path in the answer is one line per
hop, no drawing (decision 2); radii show as counts first (decision 3); the verdict is the one
coloured surface and the rest stays quiet (decision 9). The eval's graph gate grades the walk, not
the picture (ticket 06, decision 2). Node and edge labels are log and graph fields and stay plain
text (ticket 08 scope; security rules).

**The author's picture, confirmed on 25 October 2026 before this research.** The graph is a panel
beside the evidence panel in the investigator screen's right-hand space, drawn whenever the agent's
answer involved a graph walk, showing only the nodes and edges the walk touched with the walk's
direction. The author leans to that and asked the research to test it. The Gephi export is a
builder's tool for inspecting the whole synthetic organisation by eye during phase 0.

## 1. The question

Ticket 08 decides what the analyst sees when the agent's answer rests on a graph walk, where that
picture sits, how it is drawn, what the API returns to draw it, and how the whole graph is handed
to Gephi. Five questions were agreed with the author: (1) do investigation tools draw the result's
subgraph or the whole graph with highlights; (2) how is a small walked path drawn well and what
misleads; (3) which drawing approach fits a small read-only picture in the Port's React stack;
(4) what shape should the nodes-and-edges payload take so the picture cannot disagree with the
report; (5) GEXF or GraphML for Gephi, script or download, and what proves the file opens. This
note separates what the sources say (section 3) from what it recommends (section 5). The author
rules in the grilling, with the prototype open.

## 2. The criteria

- **Agreement with the report.** The picture is drawn from the same saved artifact the answer and
  the evidence panel use. Nothing appears on the canvas that the walk did not return.
- **Readable at panel width.** Ten to forty nodes in a column of the Port's shell, labels readable,
  direction visible, the finding's start node unmistakable.
- **Plain text only.** Every label is a string rendered as text, never as markup.
- **Read-only and stateless.** No drag that persists, no layout saved, nothing written.
- **Small cost.** Bundle size, licence, maintenance, and how much code is ours to own.
- **Evidence.** The phase 1 gate "author accepts the live screen" must mean something checkable.

## 3. What the sources say

### 3.1 Subgraph or whole graph (question 1)

Every investigation tool examined draws the result of the query, not the whole graph.

- **BloodHound** (SpecterOps). The Explore page draws "the nodes and edges that connect" the
  start node to the destination after a pathfinding search. Clicking a node "dims unrelated nodes
  and edges and highlights every path that traverses the selected node". Long node labels are
  clipped by default and shown in full on click. Multi-node Cypher results with no edges fall back
  to a table layout. `[P]`
- **Neo4j Bloom.** The scene starts empty or with a sample; a search puts the matching elements in
  the scene; "Expand" adds a node's immediate neighbours on demand, limited by a node query limit;
  "Dismiss others" removes everything not selected. `[P]` The sibling tool Neo4j Browser, by
  default, runs a second query to add every relationship that exists between the returned nodes
  ("Connect result nodes"), and users on the community forum repeatedly report that this makes the
  picture disagree with the query; the fix is to switch it off. `[V]`
- **Microsoft Defender XDR.** The incident graph "displays the entities and assets involved in the
  incident"; the analyst filters by entity type and groups similar nodes; a node's context menu
  offers "View blast radius", which draws propagation paths from that node to critical targets, and
  "Hide blast radius" returns to the incident graph. `[P]`
- **Elastic Security.** The entity details flyout shows "a collapsible graph preview centered on
  the entity" over the last 30 days; the full graph view expands relationships per node from an
  actions menu. `[P]`
- **Cambridge Intelligence** (a graph-visualisation vendor) recommends taking a shortest path
  between two nodes, filtering out everything not on it, and then switching from an organic layout
  to a sequential one to read the path. "Hairballs are healthy in the data, just don't expose them
  directly to your users." `[V]`

The pattern is consistent: the result subgraph is the picture, and the whole graph is reached by
expansion on demand, never drawn by default. The author's lean is the industry norm. Neo4j
Browser's default is the one counter-example, and it is treated as a trap by its own users.

### 3.2 Drawing a small walked path well (question 2)

Sources agree on a short list of rules for node-link pictures of ten to a few hundred nodes.

- **Layout follows structure.** Force-directed layouts suit exploration where community structure
  is the message; layered ("hierarchical", "sequential", Sugiyama) layouts suit paths, trees and
  flows that move in one direction. `[V]` Force layouts are non-deterministic unless seeded, and
  readers wrongly read meaning into absolute positions. `[V]`
- **Keep the picture stable.** Same data, same picture: fix the seed or compute positions
  deterministically, so the reader learns the map once. `[V]`
- **Colour for category, few hues.** Six to eight categorical hues at most; one high-salience hue
  reserved for alerts on well under two percent of nodes; luminance for importance. `[V]` Node
  shape as a second categorical channel costs more to decode than colour; three shapes at most.
  `[V]`
- **Edges behind nodes; small arrowheads.** Arrowheads multiply clutter; keep them small and
  outside the node perimeter, or show direction by tapering or on hover. `[V]`
- **Labels.** Label every node only while the graph is small (a few dozen nodes); keep labels
  horizontal; add a halo or outline so text reads over edges. `[V]` BloodHound clips long labels
  and reveals them on click. `[P]`
- **Collapse the periphery.** Low-degree peripheral nodes can be aggregated into one node that
  carries a count ("47 singleton interactors"). `[V]` Defender groups similar nodes behind a
  toggle. `[P]` This matches ticket 07's decision 3 (radii as counts first).
- **What misleads.** Phantom edges the query did not return (Neo4j Browser's default) `[V]`;
  position read as meaning in a force layout `[V]`; a changed picture for unchanged data `[V]`;
  colour and size encoding the same attribute `[V]`.

### 3.3 Drawing approach in React (question 3)

| Candidate | Size (min+gz) | Licence | Renders labels as | Layout | Notes |
|---|---|---|---|---|---|
| React Flow (`@xyflow/react` 12.12) | 58.6 kB `[P]` | MIT `[P]` | React components, so plain React text `[P]` | None built in; docs recommend dagre, d3-force, elkjs `[P]` | Built for editors; read-only needs dragging and connecting switched off. Keyboard focus, ARIA roles and live region built in `[P]`. |
| Cytoscape.js 3.34 | 133.6 kB `[P]` | MIT `[P]` | Canvas text | Built-in breadthfirst, dagre extension `[P]` | Graph algorithms we do not need (the walk is NetworkX's); React via `react-cytoscapejs` wrapper `[P]`. |
| Sigma.js 4 | 94.3 kB `[P]` | MIT `[P]` | WebGL text | Via graphology | Built for thousands of nodes `[P]`; Gephi Lite uses it `[V]`. |
| vis-network 10 | 115.6 kB `[P]` | Apache-2.0 or MIT `[P]` | Canvas text | Physics, hierarchical | React wrapper reported less maintained `[V]`. |
| d3-force 3 | 5.5 kB `[P]` | ISC `[P]` | n/a (layout only) | Force | Iterative; needs our own rendering. |
| `@dagrejs/dagre` 3.1 | 15.5 kB `[P]` | MIT `[P]` | n/a (layout only) | Layered, directed | 2.3 million weekly downloads, published this week `[P]`; React Flow's recommended choice for tree-like flows, "no edge routing" `[P]`. |
| Own SVG | 0 kB | ours | SVG `<text>` | Needs a layout library or hand placement | Everything ours: pan, zoom, fit, hit areas, keyboard access. |

Two observations cut across the table. First, the picture is a directed path with a start node and
a few hops, which is exactly the shape a layered layout draws well; dagre is small, MIT, maintained
and recommended by React Flow's own docs for that case. `[P]` Second, the Port's frontend is React
with shadcn/ui, and React Flow is the only candidate whose nodes are ordinary React components, so
a node label is a React string and the plain-text rule holds by construction; the canvas and WebGL
libraries also draw text rather than markup, so the rule holds there too, but styling and
accessibility live outside React. `[P]`

An earlier aggregator claim that Cytoscape.js is LGPL is wrong; its site states MIT for the core
and all first-party extensions. `[P]`

### 3.4 The payload (question 4)

There is no standard, but the de facto shape is one object with two arrays: `nodes`, each with an
`id` and attributes, and `edges`, each with `source` and `target` referencing node IDs plus
attributes. D3 names the second array `links`; Cytoscape.js nests both under a `data` key and
accepts either one `elements` array or `nodes` and `edges` arrays; React Flow takes `nodes` and
`edges` with `id`, `source`, `target`, `label` and a free `data` object. `[P]` For a directed graph
the `source` to `target` order is the direction; each edge appears once. `[V]`

Nothing in the sources carries hop order or "which step of the investigation produced this edge";
that is ours to add. Ticket 05 already fixes the inputs: the artifact holds the graph records with
their ground-truth IDs, the radius is computed in one core function and returned joined, and the
package has a section per step with `truncated` flags. The payload can therefore be a projection of
the saved artifact, not a new walk, which is the strongest form of "screen, tool and exam cannot
disagree": they read one record.

### 3.5 The Gephi export (question 5)

- **Format.** Gephi Desktop's GraphML import is "a limited set of this format": boolean, int, long,
  float, double and string attributes; no sub-graphs, no hyperedges, and no visual attributes at
  all (colour only as a string attribute, shapes not supported). `[P]` Its GEXF import carries
  typed attributes including list types, directed edges by default, and the `viz` module for
  colour, size, position and shape on nodes and edges. `[P]` Gephi Lite reads GEXF 1.2 and 1.3 and
  GraphML, writes GEXF, and names GEXF "the format of choice to exchange graphs with Gephi". `[P]`
- **NetworkX.** `write_gexf` writes a node's `viz` attribute (colour, size, position) into the
  file and warns that GEXF reserves `id`, `pid` and `label` as attribute names. `[P]`
  `write_graphml` supports int, str, float and bool values and raises an error for any other type,
  so a dict or list attribute on a node breaks the GraphML export. `[P]`
- **Opening the file without installing anything.** Gephi Lite is "Gephi in your browser": no
  installation, no server, "your data remains on your computer"; it reads a local GEXF file. `[P]`
  It targets smaller graphs (roughly ten thousand nodes) and lacks CSV import and the Preview
  export. `[V]` Gephi Desktop remains the full tool for larger work. `[P]`
- **Script or download.** No source speaks to this; it is a trust-boundary question of ours. The
  API returns only the fields the screen needs (security rules). A download endpoint for the whole
  organisation would push every table through the API for a builder's convenience.

## 4. The options

### Question 1: what the panel shows

| Option | For | Against |
|---|---|---|
| A. The walk's subgraph only (author's lean) | Industry norm (3.1); cannot invent edges; small enough to label everything | The analyst sees no context beyond the walk; expansion is a later feature |
| B. Whole organisation, walk highlighted | Context visible | 50 users plus groups, assets, devices, networks and chunks is a hairball at panel width; invites reading position as meaning; the periphery is noise the eval never graded |
| C. Subgraph plus one-hop ghost neighbours | Some context | Ghost edges are exactly Neo4j Browser's trap: the picture then shows what the walk did not return |

### Question 2: where it sits

| Option | For | Against |
|---|---|---|
| A. A tab in the third column: Evidence and Graph | One right-hand column as ticket 07 decided; the panel collapses under the chat on narrow screens the same way | The analyst flips between proof list and picture |
| B. Stacked in the third column: graph above the evidence list | Both visible | The column gets tall; the picture competes for height with the list |
| C. A fourth column right of the evidence panel (the author's words today) | Picture and list side by side | Four columns on a laptop screen leaves the chat narrow; ticket 07's shell has three |
| D. A route of its own | Room | Breaks "the chat is the screen" (ticket 05, R3); the picture leaves the answer it explains |

### Question 3: how it is drawn

| Option | For | Against |
|---|---|---|
| A. React Flow plus dagre (about 74 kB gz) | Pan, zoom, fit view, keyboard focus and ARIA built in; nodes are React components so shadcn styling and plain text come for free; MIT; the layered layout fits a path | An editor library used read-only: dragging, connecting, deleting must be switched off and tested off; two dependencies |
| B. Own SVG plus dagre (about 16 kB gz) | Smallest; nothing to switch off; full control of look | Pan, zoom, fit, hit areas and keyboard access are ours to write and test; the author reviews code rather than writes it, so more of our code is more to review |
| C. Cytoscape.js | Mature, MIT, dagre extension | Twice the size for algorithms we do not use; styling outside React |
| D. Sigma.js or vis-network | Scale | Scale we do not have; weaker React fit |

### Question 4: the payload

Decided largely by the fixed constraints; the open choice is whether the endpoint re-walks the
graph or projects the saved artifact. Projection keeps one record for screen, tool and exam.
Re-walking is simpler to build before the artifact round-trip exists but opens a second path that
could drift.

### Question 5: the export

| Option | For | Against |
|---|---|---|
| A. GEXF by script, read in Gephi Lite or Desktop | Carries colour and size; Gephi's own format; NetworkX writes it in one call; no API surface | `viz` colours must be set on the nodes before writing, a small helper |
| B. GraphML | Also opens in Gephi | No visual attributes; the writer rejects dict or list attributes, so node records need flattening first |
| C. A download endpoint | Convenience | Exposes the whole organisation through the API for a builder's task |

## 5. Recommendation

1. **Draw the walk's subgraph only** (Q1 A). Nothing on the canvas that the walk did not return.
   Context arrives later, if ever, as expansion on demand, the way every tool in 3.1 does it.
2. **A tab in the third column, Evidence and Graph** (Q2 A), unless the prototype shows that the
   picture and the list are read together often enough to justify stacking. The author's "right of
   the evidence panel" is recorded as a fourth column in the options and tested in the prototype;
   the recommendation is against it because the Port's shell has three columns and the chat pays.
3. **React Flow plus dagre, read-only** (Q3 A), with a build test that asserts nodes cannot be
   dragged, connected or deleted. Own SVG is the fallback if the bundle or the switch-off list
   proves heavier than it looks in the prototype. Layered layout left to right from the finding.
4. **The payload projects the saved artifact.** Shape: `nodes[]` with `id` (ground-truth ID),
   `type` (person, group, asset, device, network, chunk), `label` (plain string), `role` (`focus`,
   `walked`); `edges[]` with `id`, `source`, `target`, `type` (the table the edge came from), and
   `step` (the playbook step that produced it, so hop order and the step stack of ticket 07 line
   up); `truncated` counts per step mirroring ticket 05's decision 12; nothing else. The finding's
   start node is `focus`. Direction is the walk's direction.
5. **Visual rules for the prototype**, from 3.2: layered layout, deterministic positions, colour
   by node type within the hues the app already has, the focus node as the one loud element in the
   panel in line with ticket 07's hierarchy, small arrowheads, labels on every node clipped with
   the full value on hover or click, truncated groups drawn as one node with a count that opens
   the list in the evidence tab.
6. **GEXF, by script, no endpoint** (Q5 A). One core function sets `viz` colour by node type and
   writes the whole graph or one neighbourhood with `write_gexf`. Evidence: a unit test that writes
   the pinned dataset, reads it back with `read_gexf` and asserts node and edge counts by type
   against the integrity check of ticket 06; and the author opening the file in Gephi Lite in the
   browser once, recorded as the author's look, not a screenshot.
7. **The phase 1 gate for this panel** is the author's acceptance of the live panel on the three
   phase 1 question kinds (threat, benign twin, say-no) plus the two code checks above. No eval
   question is added: the walk is graded by ticket 06's graph gate and the panel only draws its
   output.

## 6. Open for the grilling

- Tab versus stack versus fourth column, with the prototype at laptop width open.
- Whether the panel appears only when a walk happened, or always with an empty state.
- Whether a click on a node highlights the hop line in the answer and the row in the evidence
  tab, or only the row.
- Whether chunks (`mentions` edges) are drawn at all in phase 1, or only the organisation nodes.
- Whether the export covers one neighbourhood as well as the whole graph in phase 0.

## Sources

Primary pages opened `[P]`: BloodHound "Search and pathfinding" and "Graph view"
(bloodhound.specterops.io); Neo4j Bloom "Scene interactions" and "Search bar" (neo4j.com/docs);
Microsoft Defender XDR "Investigate incidents", "Investigate incident cases", "Graph icons"
(learn.microsoft.com); Elastic "View entity details", "Entity relationships" (elastic.co/docs);
React Flow "Layouting overview", "Accessibility", "Edge" (reactflow.dev); Cytoscape.js home
(js.cytoscape.org); sigma.js and d3-force repositories (github.com); npm pages for `@xyflow/react`,
`cytoscape`, `vis-network`, `@dagrejs/dagre`; Bundlephobia for the same plus `sigma` and
`d3-force`; NetworkX `write_gexf` and the `graphml` module source (networkx.org); Gephi Desktop
"GEXF" and "GraphML" import pages, Gephi Lite "File formats", gephi.org/lite (gephi.org).

Secondary `[V]`: Neo4j community threads on "Connect result nodes"; Cambridge Intelligence blog
posts on large-network layouts and hairballs; visualcomplexity.com "Design principles"; GLE
"Network graph visualization for science"; knowledgegraphnavigator.com and thelinuxcode.com guides;
pkgpulse, redsurgetechnology and awesomedataviz library comparisons; Bellingcat toolkit note on
Gephi Lite.
