# Map: knowledge-base

Label: wayfinder:map

## Destination

A knowledge base inside the Login Investigator, built around a knowledge graph with RAG as part of
its ecosystem, that gives the investigator agent context about the threat behind a login pattern,
so an alert becomes an explained risk rather than a flagged row. The use case is chosen for the
value it adds to the app, not for the sake of demonstrating RAG.

## Notes

- **Origin.** The bootcamp's week 2 brief (RAG, with GraphRAG as one suggested use case) is the
  inspiration. By the author's ruling of 20 October 2026 it is not a contract: nothing is
  submitted, there is no deadline and no owed deliverable. See `CLAUDE.md`.
- **Reference shape.** The course demo notebook (the author's copy, `Mastering-Agentic-AI-Week2`,
  `Week2-Session2/graph_rag/graph_rag.ipynb`): structured facts as a Neo4j graph, free text
  chunked and embedded as nodes linked to the graph, semantic search to find candidates, graph
  traversal to filter and enrich, a grounded generation step. Semantic search finds, the graph
  decides and explains.
- **Retrieval stance (author, 20 October 2026).** Hybrid retrieval (semantic plus BM25 keyword)
  with re-ranking, at sensible defaults first. Tuning follows measurement, never precedes it.
- **Evaluation stance (agreed 20 October 2026).** The eval set exists before the first retrieval
  runs. Two layers measured separately: retrieval (was the gold evidence found and ranked) and
  answer (is every claim backed by the retrieved context). Re-run on every change; runnable by the
  author or Codex without Claude.
- **Data.** Everything in the app is synthetic demo data. A larger synthetic set is allowed if the
  chosen use case needs it, as long as it gives solid ground for testing.
- **Rigour.** Tier 3. Every ticket closes on evidence.
- **Future direction noted by the author (20 October 2026), not scope.** The same graph serves
  GRC: a control maps to a policy, a policy applies to an asset, an incident shows a control
  failed. "Which controls does this incident touch?" becomes one query once the map exists. Any
  move in that direction is a later slice with its own spec.
- **Tools.** Research tickets use the Perplexity MCP tools and verify material claims against
  primary sources. The course's solution kits stay closed.

## Decisions so far

<!-- one line per resolved ticket: [title](link): gist -->

- [Use-case research](issues/01-use-case-research.md): the graph holds durable relationships
  (people, accounts, groups, grants, assets, networks, incidents) and the log stays the source of
  truth; policies, runbooks, ATT&CK pages and incident write-ups form the hybrid-searched corpus;
  Neo4j GraphRAG ships the hybrid-then-traverse shape; no public dataset pairs logins with
  organisational context, so we generate our own small consistent set. Three candidate slices
  documented; recommendation is slice 2 (spray-to-compromise blast radius) with slice 1's network
  and travel facts folded in. Author's choice pending. [Research note](research/01-use-case-research.md).
- [Where the graph lives and where retrieval runs](issues/02-store-and-retrieval-provider.md):
  one store, the author's installed PostgreSQL 18.6 with pgvector; LangChain's PostgreSQL store
  for hybrid search with our own score-keeping fusion; built-in keyword ranking first, BM25 only
  if the eval demands it; graph walked in NetworkX built from the tables, chunks included with
  `mentions` edges; a read-only graph screen of our own plus Gephi export; ground-truth files are
  the truth and the database is built from them; fresh database per run, loud failures; two
  read-only locks; memory stays in SQLite. Neo4j, LanceDB, LadybugDB and hosted services ruled
  out. Ten decisions under the ticket's Answer. [Research note](research/02-store-and-retrieval-provider.md).

### Author's ruling, 20 October 2026

Slice 2, spray-to-compromise blast radius, goes first. The broadening steps are accepted in the
order recorded in [research note 01, section 7](research/01-use-case-research.md): spread and
shared ground, then history, then travel and network facts with account type, then attack path
and risk score. GRC is a later slice.

### Phases

| Phase | Content | Gate to close |
|---|---|---|
| 0 Foundation | Graph store, synthetic data generator with written ground truth, text corpus, hybrid retrieval with re-ranking, the eval harness with its first questions, read-only agent tools over graph and corpus | Eval harness runs end to end; retrieval and answer layers measured separately |
| 1 Blast radius | Slice 2 core plus spread and shared ground | Eval pass on phase 1 questions; author accepts the live screen |
| 2 History | Incident nodes and write-ups | Eval set extended and passing |
| 3 Context | Travel and network facts; account type and ownership | Eval set extended and passing |
| 4 Paths and risk | Attack-path query; risk score with an agreed policy | Eval set extended and passing; author agrees the scoring policy |
| Later | GRC view | Its own spec |

Each phase is specified before it is built, and the eval set grows with each phase.

### Scope ruling (author, 20 October 2026)

**This initiative delivers phases 0 and 1 only.** They are the requirements: the foundation and
the blast-radius slice with spread and shared ground. The spec and tickets cover those two phases
and nothing else. The initiative closes when phase 1 is accepted on a live screen with its eval
passing.

Phases 2, 3, 4 and the GRC view are **planned features, not requirements.** They stay recorded
here and in research note 01 so the design keeps room for them, and each is taken later as its
own small initiative, with its own spec section and tickets, whenever the author chooses. Other
bootcamp-week initiatives will arrive in between; nothing in this initiative waits on them or
blocks them.

### Decision tickets charted (20 October 2026)

| Ticket | Type | Blocked by |
|---|---|---|
| [02 Where the graph lives and where retrieval runs](issues/02-store-and-retrieval-provider.md) | research | none |
| [03 Embedding model, keyword search and re-ranker](issues/03-embedding-and-reranking.md) | research | 02 |
| [04 Synthetic organisation, corpus and ground truth](issues/04-synthetic-data-and-ground-truth.md) | grilling | 02 |
| [05 How the knowledge base reaches the agent](issues/05-agent-tools-for-the-knowledge-base.md) | grilling | 02, 04 |
| [06 The eval set for a graph-plus-text system](issues/06-eval-design.md) | grilling | 04, 05 |
| [07 What the screen shows for an explained alert](issues/07-explained-alert-screen.md) | prototype | 05 |

Ticket 02 is resolved (20 October 2026). The frontier is tickets 03 and 04, which 02 unblocked;
03 by number first. The spec (`mp-to-spec`) follows the last resolution.

## Not yet specified

- Dataset swap: ticket 02 settled the mechanism (build from another folder into another
  database name; the app opens a dataset by name). Ticket 04 settles the folder's format.
- The spec for phases 0 and 1, after tickets 03 to 07.

## Out of scope

- Any change to the Port's behaviour that the use case does not require.
- Any change to v1.
- The bootcamp's deliverables (project document, demo video, submission).
