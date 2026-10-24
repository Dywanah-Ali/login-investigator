# 02: Where the graph lives and where retrieval runs

Type: research
Status: resolved
Blocked by: none

## Question

Which store holds the knowledge graph, and which component runs the vector and keyword search
over the text corpus? These are one decision, because Neo4j bundles graph, vector index,
full-text index and hybrid-then-traverse retrievers in one server, while a lighter choice splits
them into a graph library, a vector store, a keyword index and our own fusion code.

## Scope

- Compare at least three shapes: Neo4j (as the course demo used, local Docker or Aura free tier);
  an all-local stack (an embedded or SQLite-backed graph with a local vector store and a BM25
  library); and a mixed stack (lighter graph, hosted vector search).
- Judge on: fit with the Port's architecture rules (core stays plain Python, one place creates
  the model and agent, data access in the core); what the author must install or sign up for;
  cost; how the eval harness isolates a run; how a later move to another store would look; and
  whether the LangChain integrations the agent already uses cover it.
- Confirm what the Neo4j GraphRAG package's hybrid retriever does and does not do (Lucene score
  versus BM25, re-ranking as a separate step).
- Save one cited note at `../research/02-store-and-retrieval-provider.md` with a recommendation
  and the trade-offs, for a grilling with the author.

## Acceptance

- [x] Four shapes compared on the criteria above, with primary-source citations
  ([research note](../research/02-store-and-retrieval-provider.md), sections 3 and 4).
- [x] Recommendation stated with its trade-offs and what it rules out (note, section 5).
- [x] Findings presented to the author; the choice is recorded below under `## Answer`.

## Answer

Grilled and ruled by the author on 20 October 2026. Ten decisions.

| # | Decision |
|---|---|
| 1 | **One store: the author's installed PostgreSQL 18.6 (Homebrew, Intel Mac) with pgvector.** The organisation's ground truth, the chunks, their vectors and their keyword index live in one database. Neo4j, LanceDB, LadybugDB, Memgraph, FalkorDB, ArangoDB, TigerGraph and the hosted vector services are ruled out (note, section 3.7). Neo4j stays a documented later move behind the seam, never a test or eval dependency. |
| 2 | **Graph walks in NetworkX**, built in memory from the tables when the knowledge base opens, with named traversal functions in the core. A **read-only graph screen of our own** in the React frontend, designed in ticket 07. **Export to Gephi** (standard graph file from NetworkX) for free exploration. No live-editing graph admin: the files are the truth (decision 6). |
| 3 | **Keyword search starts with PostgreSQL's built-in text ranking** through LangChain's hybrid search. The eval set's first retrieval-layer question asks whether it finds the gold passages. BM25 (`pg_textsearch`) is added only if that fails, through the same pluggable fusion step. |
| 4 | **PostgreSQL runs as an always-on Homebrew service.** Tests and evals only connect. If it is down, the shared fixture fails at once with the exact start command. |
| 5 | **A fresh database per test session and per eval run**, built from pinned inputs and dropped afterwards. Tests that need PostgreSQL **fail loudly, never skip**. Today's tests stay service-free. |
| 6 | **The ground-truth files are the truth**, standing in for the upstream systems (HR, directory, inventory, ticketing). The loader is the sync job. The database is a build artefact, never edited by hand. Dataset swap = build from another folder into another database name and point the app at it. Full rebuild per run in phases 0 and 1; incremental sync registered as a later item. |
| 7 | **Chunks live in the table LangChain's PostgreSQL store creates**, with our metadata columns for filtering: document type, version and effective date, section, technique id, account type, mentioned entity ids. The exact fields are chosen in ticket 04 with the corpus. **Chunks are also nodes in the NetworkX graph with `mentions` edges** to entities, the same role as the demo's `PART_OF` edge. |
| 8 | **Read-only by two locks**: the agent's tools are hand-written, parameterised functions in the core (no model-written SQL or Cypher), and the agent connects with a **PostgreSQL role that can only read**. |
| 9 | **Agent memory stays in SQLite** for this initiative. The move to the PostgreSQL checkpointer is registered as a later decision. |
| 10 | **Our own score-keeping merge function is plugged into LangChain's hybrid search from day one**: reciprocal rank fusion, plus each chunk's rank in both lists and its fused score, recorded for the eval's retrieval layer. |

Conditions carried into the spec:

- `langchain-postgres` pinned to an exact version, like `langchain` is.
- Connection details live only in `.env`; `env.example` holds names.
- The first build step of phase 0 proves `brew install pgvector` compiles on the Intel Mac and
  `CREATE EXTENSION vector` works.
- Section 3.8 of the note records the machine facts this decision rests on.

Hand-offs: ticket 03 (embedder, cross-encoder, fusion parameters; BM25 only if the eval says
so), ticket 04 (ground-truth file format, metadata filter fields, loader, dataset swap by
folder), ticket 05 (hand-written read-only tools over the seam), ticket 06 (per-run database
fixture, retrieval-layer record fields), ticket 07 (graph screen).

## Comments

- 2026-10-20, Claude: research done. Note at
  [../research/02-store-and-retrieval-provider.md](../research/02-store-and-retrieval-provider.md).
  Recommendation: embedded stack, LanceDB for the corpus (BM25, vector, fusion and cross-encoder
  built in) and NetworkX for the graph, behind one core seam; Neo4j Community in Docker kept as a
  later move, not a test or eval dependency. LadybugDB named as the alternative if the author
  wants Cypher and one store. Awaiting the grilling that records the choice.
- 2026-10-20, Claude: at the author's request the note gained shape D, PostgreSQL (pgvector,
  a BM25 extension, Apache AGE, and the `pgembed` route that avoids Docker), and a table of the
  graph stores ruled out with reasons (ArangoDB, TigerGraph, Dgraph, JanusGraph, Oxigraph).
  PostgreSQL without Docker is recorded as the close second to the recommendation.
- 2026-10-20, author's correction: LangChain does ship rank fusion (`EnsembleRetriever`) and a
  re-ranker wrapper (`CrossEncoderReranker`). Note corrected: the remaining gap is that they
  return documents without scores, so a score-keeping wrapper is still ours for the eval.
- 2026-10-20, Claude: at the author's request, checked what LangChain adds to the PostgreSQL
  shape (note section 3.6). Its PostgreSQL store has hybrid search built in with reciprocal rank
  fusion, fused scores returned and a pluggable fusion function; re-ranker, local or OpenRouter
  embeddings, incremental indexing and a PostgreSQL checkpointer are all maintained packages.
  Recommendation revised: shapes B and D are peers; the author's lean decides at the grilling.
  Open points for D: `tsvector` versus BM25 keyword leg (eval decides), `pgembed` on Apple
  Silicon (two-line check), pin `langchain-postgres`.
- 2026-10-20, author: PostgreSQL is already installed on the Mac, and the author likes it.
  Claude checked the machine (note section 3.8): Intel Mac, Homebrew PostgreSQL 18.6, server
  not running, pgvector not installed; LanceDB 0.40.0 and pgembed 0.2.0 ship no Intel-Mac
  wheels. Recommendation revised to shape D on the installed PostgreSQL, with four conditions
  for the spec (per-run database fixture, pinned package, tsvector first then BM25 if the eval
  says so, fusion function of ours for scores). Awaiting the grilling.
- 2026-10-24, Claude: decision 2's graph screen and Gephi export were not taken up by ticket 07,
  which this decision named as their design ticket. They now belong to
  [ticket 08](08-graph-screen-and-gephi-export.md), opened by the author.
