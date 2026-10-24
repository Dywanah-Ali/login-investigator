# 08: The read-only graph screen and the Gephi export

Type: prototype, then grilling
Status: open
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

- [ ] Prototype of the candidate views reviewed with the author in the browser; the view, the
      placement and the drawing approach chosen.
- [ ] API contract addition drafted for the graph endpoint.
- [ ] Gephi export shape decided with its evidence.
- [ ] Decision recorded here under `## Answer`.

## Comments

**2026-10-24, opened.** The author noticed, while checking ticket 02's decision 2 against ticket 06,
that the graph screen promised there was never designed. Ticket 07's question, scope and answer do
not mention it; the Gephi export appears in no ticket after 02 and in no build list. The author
chose a new ticket over reopening 07, so that 07's evidence stays intact and the screen gets its
own prototype, under the author's ruling of 24 October 2026 that a screen cannot be decided from a
description. Same order of work as ticket 07: prototype first, then the grilling with the picture
in front of the author, one question at a time with a plain heading each.
