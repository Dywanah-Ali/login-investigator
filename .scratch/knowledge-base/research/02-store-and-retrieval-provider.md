# Research note 02: where the graph lives and where retrieval runs

Ticket: [02-store-and-retrieval-provider](../issues/02-store-and-retrieval-provider.md)
Date: 20 October 2026
Method: one Perplexity deep-research call (about 6 minutes) plus twenty-nine Perplexity search
calls restricted to primary domains (neo4j.com, pypi.org, github.com, langchain.com, lancedb.com,
ladybugdb.com, memgraph.com, falkordb.com, postgresql.org, age.apache.org, paradedb.com,
arango.ai, tigergraph.com) to verify every claim the recommendation rests on. Section 3.5 and
section 3.7 were added after the author asked about pgvector and about graph stores the first
pass had not weighed.
No secrets involved. `[P]` marks a claim verified against a primary source opened in this research;
`[V]` marks a vendor, aggregator or practitioner claim that was not independently opened.

## 1. The question

Which store holds the knowledge graph, and which component runs the vector and keyword search over
the text corpus? Ticket 02 treats these as one decision because Neo4j bundles graph, vector index,
full-text index and hybrid-then-traverse retrievers in one server, while a lighter choice splits
them across a graph library, a vector store, a keyword index and our own fusion code.

The size of the problem matters for every answer below: tens of people, accounts, groups and
assets; a few dozen documents; a few hundred chunks. Nothing here is a scale problem. The decision
is about fit, operability and evidence, not performance.

## 2. The criteria, from the ticket

| # | Criterion | What it means for this app |
|---|---|---|
| C1 | Fit with the Port's architecture rules | Core stays plain Python; one function creates the model and agent; data access lives in the core; the API asks the core for "a dataset" |
| C2 | What the author must install or sign up for | A non-developer owns this machine. Every extra running service is a thing that can be down when a test runs |
| C3 | Cost | Money, and also the hidden cost of a free tier that pauses or deletes data |
| C4 | How the eval harness isolates a run | The eval set is the acceptance gate. A run must build its own index from pinned inputs, use it, and throw it away, with no state leaking between runs |
| C5 | How a later move to another store would look | The seam must survive a store change; phases 2 to 4 and the GRC view will reuse the graph |
| C6 | Whether the LangChain integrations the agent already uses cover it | The agent uses LangChain 1.3 (`create_agent`, `@tool`, `init_chat_model`). Retrieval must be reachable as a plain function the tools can call |
| C7 | Offline and reproducible | A single developer on a Mac, and an eval that gives the same retrieval answer tomorrow |

## 3. The four shapes, plus the lighter servers

### Shape A: Neo4j, local Docker or AuraDB Free

| Fact | Status |
|---|---|
| Community Edition is GPLv3, runs as a single instance, and includes full-text indexes and vector indexes. Enterprise is not needed for either. | [P] Operations Manual introduction, feature table; pricing page |
| Server versions moved to calendar versioning with 2025.01.0 (`YYYY.MM.Patch`). Current Docker tags look like `neo4j:2026.09.0`; Enterprise tags carry `-enterprise` and require accepting the licence through an environment variable. | [P] Operations Manual introduction; Docker introduction |
| The official Docker image defaults to 512 MB heap and 512 MB page cache, intended for learning. | [P] Docker configuration page |
| **Community Edition supports only the `system` database and one default database.** There is no `CREATE DATABASE` for a second user database. | [P] Upgrade and migration guide, multiple databases |
| Vector index scores are only meaningful within one query's result set. Neo4j's own guidance: when combining vector and full-text results, rank each source independently rather than compare raw scores. | [P] Cypher Manual, vector indexes |
| Full-text indexes are powered by Apache Lucene and return a *Lucene query score*. The documentation does not name BM25 as the scoring contract. | [P] Cypher Manual, full-text indexes; Operations Manual, index configuration |
| Neo4j's hybrid-search developer guide implements **weighted reciprocal rank fusion by hand in Cypher**, using the Cypher 25 `SEARCH` clause (Neo4j 2026.09 or later) with a compatibility version using the `db.index.*.queryNodes` procedures. It notes the full-text procedures are deprecated in Cypher 25 as of 2026.10, and recommends passing fused candidates to graph expansion or a re-ranker afterwards. | [P] Developer guide, hybrid search |
| AuraDB Free: one free instance per account, no credit card, no automatic backups. **Paused after 3 days without write queries** (reads do not count). **A paused instance is deleted after 30 days** and cannot be recovered. | [P] Neo4j support FAQ for Aura Free; Aura pausing policy article |
| AuraDB Free size limit: the Aura quotas page and support FAQ say 200,000 nodes and 400,000 relationships; the marketing page still says 50,000 nodes and 175,000 relationships. Either is far above our need. | [P] both pages opened; they disagree |
| Python driver `neo4j` 6.4.1, Apache-2.0, Python 3.10 to 3.15. | [P] PyPI |
| `neo4j-graphrag` 1.22.0, Apache-2.0, Python 3.10 to 3.14. | [P] PyPI |
| `langchain-neo4j` 0.11.0, MIT, Python 3.10 to 3.14. `Neo4jVector` accepts `search_type="hybrid"` with a keyword index name and a custom `retrieval_query`; `Neo4jGraph` wraps the driver. | [P] PyPI; LangChain docs and reference |

**What the GraphRAG package's hybrid retriever actually does** (the ticket asked for this
explicitly):

| Component | Behaviour | Status |
|---|---|---|
| `HybridRetriever` | Queries a named vector index and a named full-text index with the same text, then merges. Needs an embedder for text queries. | [P] API docs, source |
| Ranker `NAIVE` (default) | Each list is divided by its own maximum score, the lists are unioned, and each node keeps its **maximum** score. | [P] source and `types.py`; same query shape as the Neo4j hybrid Cypher used across Neo4j's integrations |
| Ranker `LINEAR` | Same normalisation, then `alpha × vector + (1 − alpha) × fulltext`. `alpha` is required. | [P] source |
| Reciprocal rank fusion | **Not provided** by the retriever. Neo4j's own guide does it in hand-written Cypher. | [P] |
| Re-ranking with a model | **Not provided.** An explicit separate step. | [P] |
| `HybridCypherRetriever` | Same search, then a `retrieval_query` runs from each matched node (`node`, `score` in scope) to traverse into the graph. | [P] API docs; Neo4j Labs LangChain page shows it wrapped in a LangChain `@tool` |
| Keyword scoring | Lucene relevance score, normalised by the list maximum. Not a documented BM25 contract. | [P] |

So the course demo's shape exists, but "hybrid with re-ranking" in the author's sense needs two
things Neo4j does not ship in the retriever: rank fusion and a re-ranker. Those are ours to write
in every shape.

### Shape B: all local, embedded

Four candidate building blocks were checked. Two matter.

**Embedded graph.**

| Fact | Status |
|---|---|
| Kuzu, the embedded Cypher database the course era knew, was **archived on 10 October 2025** with 0.11.3 as the final release; the company was acquired by Apple, disclosed in February 2026. Upstream is read-only. | [V] consistent across four independent write-ups; the GitHub archive banner was not opened directly |
| **LadybugDB** is the active MIT-licensed community fork. PyPI package `ladybug`, 0.21.2 released 1 October 2026 with releases roughly weekly, wheels for CPython 3.12 on macOS 15+ ARM64. | [P] PyPI; project docs installation page |
| LadybugDB ships a **full-text index using Okapi BM25** (`K`, `B`, `conjunctive`, `TOP` parameters) and a **disk-based HNSW vector index**, both on node-table properties, both queried from Cypher, with traversal from a vector hit in the same query. Extensions are loaded with `INSTALL`/`LOAD`. | [P] docs, FTS and vector extension pages |
| Two packages exist: `ladybug` (the maintained line) and `real_ladybug` from a `ladybug-classic` historical repo. Easy to confuse. | [P] GitHub README of ladybug-classic |
| NetworkX: in-memory graph library, BSD-3-Clause, no persistence of its own, serialises to JSON. | [V] research pass; not opened |
| SQLite tables with recursive CTEs, or `simple-graph` (MIT). | [V] research pass |

**Corpus store with hybrid retrieval.**

| Fact | Status |
|---|---|
| **LanceDB** 0.40.0, Apache-2.0, Python 3.10+, embedded (a directory on disk), macOS 11+ ARM64 wheel. | [P] PyPI |
| LanceDB has BM25 full-text search, hybrid vector-plus-full-text queries, and **built-in re-rankers**: `RRFReranker` (default for hybrid, reciprocal rank fusion, no model), `LinearCombinationReranker` (weighted score blend, no model), `CrossEncoderReranker` (local sentence-transformers cross-encoder, default `cross-encoder/ms-marco-TinyBERT-L-6`), plus hosted ones (Cohere, Jina, OpenAI, Voyage) that need keys. A `normalize` argument chooses rank or score normalisation before fusion. | [P] LanceDB docs: hybrid search, reranking, cross-encoder |
| LanceDB's own evaluation page documents the point the author cares about: dense and sparse scores cannot be compared directly, so hybrid retrieval *requires* a fusion or re-ranking step, and it measures each re-ranker separately. | [P] LanceDB docs, evaluating hybrid search |
| Chroma 1.5.9, Apache-2.0: local persistent vector store with a LangChain package. No native BM25 verified. | [P] PyPI |
| `sqlite-vec` 0.1.9 (MIT or Apache-2.0), `bm25s` 0.3.14 (MIT), FlashRank 0.2.10 (Apache-2.0, last release January 2025). | [P] PyPI |
| **LangChain's retrieval helpers in 1.x:** `EnsembleRetriever` (weighted reciprocal rank fusion) and `CrossEncoderReranker` moved to `langchain-classic`; `BM25Retriever`, `FlashrankRerank` and `HuggingFaceCrossEncoder` live in `langchain-community`, and LangChain's own documentation now carries the note that `langchain-community` **is no longer maintained** and its examples may be broken. | [P] LangChain v1 release notes; cross-encoder re-ranker docs page |

That last row changes C6. The LangChain integrations are not the safe path for retrieval in
LangChain 1.x. The safe path is a plain Python function in the core that calls the store's own
API, wrapped by `@tool` the way the Port already wraps its log tools. Neo4j's own Labs page
recommends exactly this wrapping for its retrievers.

### Shape C: mixed, embedded graph plus hosted vector search

| Service | Free tier | Hybrid and re-ranking | Status |
|---|---|---|---|
| Qdrant Cloud | Single node, 0.5 vCPU, 1 GB RAM, 4 GB disk, "free forever"; suspended after a week idle, deleted after four weeks | Dense plus sparse (BM25) vectors fused server-side with RRF or DBSF; multi-stage query can re-score with ColBERT-style late interaction | [V] pricing and docs quoted by aggregators and the research pass |
| Pinecone Starter | 2 GB storage, metered read and write units, five serverless indexes | BM25 full-text fields alongside dense vectors in schema indexes; hosted re-rankers with a 500-request monthly cap on Starter | [V] |
| Weaviate Cloud free | 100,000 objects, one collection; suspended after 7 idle days, deleted after 30 | Native BM25F hybrid; re-rankers need a Cohere key; the local transformers re-ranker is not available on the cloud tier | [V] |

All three fail C7 outright: nothing offline, and each has a pause-or-delete policy that would make
an eval run fail after a quiet fortnight. They also add a signup and a key for no capability the
embedded shape lacks at our size. None of the claims above needed primary verification because the
shape is ruled out on C7 alone.

### Shape D: one PostgreSQL for both (added at the author's request)

The author asked why pgvector was not weighed. It should have been: the synthetic organisation
(people, accounts, groups, grants, assets) is relational data, and PostgreSQL is the database
clients most often already run. The shape is: PostgreSQL holds the organisation as tables, the
chunks with a pgvector column, keyword search through an extension, and the graph either as
tables traversed with recursive queries or through the Apache AGE extension with Cypher.

| Fact | Status |
|---|---|
| pgvector 0.8.7, PostgreSQL License, supports PostgreSQL 13+; `CREATE EXTENSION vector` once per database. HNSW and IVFFlat indexes; dense, half, binary and sparse vectors. | [P] README; LICENSE file |
| pgvector's README shows hybrid search with PostgreSQL's native full-text search (`tsvector`, `ts_rank_cd`) and points to its own Python examples for **reciprocal rank fusion and a cross-encoder**. The store itself fuses and re-ranks nothing. | [P] README |
| **LangChain supplies both missing pieces** (the author's correction, 20 October 2026): `EnsembleRetriever` in `langchain-classic` runs several retrievers and merges them by weighted reciprocal rank fusion, with `weights`, the constant `c` and an `id_key`; `CrossEncoderReranker` in `langchain-classic` re-orders a retriever's output with any cross-encoder behind a small interface. **What they do not give:** `weighted_reciprocal_rank` returns documents only, so the fused score and each leg's rank are not available to record. For the eval's retrieval layer, a thin wrapper that keeps those numbers is still ours. So is a retriever class over the BM25 extension, since none exists, and the model wrapper `HuggingFaceCrossEncoder`, which lives in the unmaintained `langchain-community`, is better replaced by a ten-line adapter over sentence-transformers. | [P] LangChain reference, EnsembleRetriever and weighted_reciprocal_rank |
| PostgreSQL's native ranking functions are `ts_rank` and `ts_rank_cd`. The manual says they "are only examples", use no global corpus statistics, and so are **not BM25**. | [P] PostgreSQL manual, controlling text search |
| True BM25 needs an extension. **`pg_textsearch`** (Timescale): BM25 with `k1` and `b`, PostgreSQL License, PostgreSQL 17 and 18 only, prebuilt binaries for Linux only, built from source on macOS. **`pg_search`** (ParadeDB): BM25 on Tantivy, AGPL-3.0 for the community edition, prebuilt macOS binaries. | [P] both repos |
| **Apache AGE**: Apache-2.0, Apache top-level project since May 2022, openCypher inside PostgreSQL, hybrid Cypher-plus-SQL queries. Releases are cut **per PostgreSQL major**: 1.8.0 for PG18 (latest), 1.7.0 for PG17, 1.6.0 for PG14 to PG16. The extension must be loaded on every connection. Some releases ship without upgrade scripts. The quick-start page still lists PG11 to PG16 as supported, so the docs lag the releases. | [P] age.apache.org overview, quick start, downloads; GitHub releases |
| PostgreSQL supports many databases per server, so a fresh database per eval run is one `CREATE DATABASE`. | Well known; not cited |
| **Embedded PostgreSQL by `pip install`** exists and removes Docker: `pgembed` 0.2.0 (Python 3.12+, bundles PostgreSQL with optional `pgembed-pgvector`, `pgembed-pgvectorscale` and `pgembed-pgtextsearch` wheels, macOS Apple Silicon included; a fork of `pgserver`, released March 2026), and `embedded-postgres` (PostgreSQL 18.6 plus pgvector 0.8.6 as one wheel per platform, started September 2026). **Neither bundles Apache AGE.** | [P] PyPI pgembed; GitHub embedded-postgres |
| `langchain-postgres` 0.0.19 (October 2026): `PGVectorStore` is current, `PGVector` is deprecated, and the docs warn there is no migration mechanism when the schema changes. | [P] PyPI; LangChain docs |

What this means, against the criteria:

| Criterion | PostgreSQL via `pgembed` (no Docker) | PostgreSQL in Docker with Apache AGE |
|---|---|---|
| C2 install | `uv add`; a server process the library starts and stops for us | Docker Desktop running; AGE compiled or an image that ships it |
| C4 eval isolation | A temporary data directory or a `CREATE DATABASE` per run; good | Same, but behind Docker |
| C5 later move | SQL and relational ground truth port anywhere; this *is* the common production shape | Cypher ports to Neo4j and Ladybug with dialect edits |
| C6 LangChain | `langchain-postgres` maintained, or wrap SQL in the core | Same |
| C7 offline | Yes | Yes once the image is pulled |
| Hybrid and re-ranking | **Built into LangChain's `PGVectorStore`**: `tsvector` keyword leg plus pgvector, fused by reciprocal rank fusion or weighted sum, fused score returned, fusion function pluggable (section 3.6). BM25 instead of `tsvector` means a keyword leg of ours over `pg_textsearch`. Re-ranking through `CrossEncoderReranker` with a small model adapter | Same |
| Graph | Tables with recursive queries, or NetworkX built from the tables | Cypher through AGE |
| Maturity risk | `pgembed` is seven months old at 0.2.0; `pg_textsearch` wheels for macOS through `pgembed` are unverified | AGE's release coupling to PostgreSQL majors and missing upgrade scripts are a maintenance tax for a non-developer owner |

Shape D without Docker is the only other shape that passes C2, C4 and C7 together, and it adds
two things B lacks: one store for ground truth, chunks, vectors and keywords, and SQL as the
transferable skill. Section 3.6, added after the author's question, shows LangChain closes most
of what the first version of this note counted against it. What remains against B: the keyword
leg is `tsvector` ranking rather than BM25 unless we add a leg of ours; a server process starts
under every test session; and it rests on a young packaging project.
Shape D with Docker and AGE is a Neo4j-class choice: Cypher and one server, with the same
every-test-needs-Docker cost.

### 3.6 What LangChain adds to shape D (checked at the author's request)

The author leans towards PostgreSQL and asked what LangChain supplies to close its gaps. Each
row below was checked against LangChain's reference or docs.

| Gap in shape D | What LangChain supplies | Package and maintenance | Status |
|---|---|---|---|
| Hybrid search and fusion | **Built into `PGVectorStore`.** A `HybridSearchConfig` names a `tsvector` column (with a GIN index), runs the vector and keyword legs with `primary_top_k` and `secondary_top_k`, and fuses them with `reciprocal_rank_fusion` (`rrf_k`, `fetch_top_k`) or `weighted_sum_ranking` (two weights). The `fusion_function` is **any callable**, so a fusion of ours that also records each leg's rank plugs in without forking anything. | `langchain-postgres` 0.0.19, MIT, maintained (released October 2026) | [P] reference: HybridSearchConfig, weighted_sum_ranking; unit tests |
| Fused scores for the eval | `similarity_search_with_score` returns documents with the **fused score** when hybrid search is configured. The package's own tests assert the scores are floats in descending order. | same | [P] reference and tests |
| Keyword leg quality | The keyword leg is PostgreSQL's native `tsvector` ranking, which the PostgreSQL manual says is not BM25 and uses no corpus statistics. At a few hundred chunks this may be good enough; the eval decides. True BM25 means a keyword leg of ours over `pg_textsearch`, fused through the same pluggable function. | PostgreSQL core | [P] PostgreSQL manual |
| Re-ranking | `CrossEncoderReranker` (a document compressor) inside `ContextualCompressionRetriever`, over any model that implements `BaseCrossEncoder.score()`. LangChain's docs recommend the retrieve-20-rerank-to-5 pattern and run it locally on CPU. The documented model wrapper `HuggingFaceCrossEncoder` lives in `langchain-community`, which is unmaintained; a ten-line adapter over sentence-transformers implements the interface instead. | `langchain-classic`, maintained | [P] reference: CrossEncoderReranker, BaseCrossEncoder; cross-encoder docs page |
| Embeddings | Two maintained routes. `HuggingFaceEmbeddings` runs a sentence-transformers model in-process, no key, offline. `OpenAIEmbeddings` from `langchain-openai` works against OpenRouter, which serves `POST /api/v1/embeddings` with models such as `openai/text-embedding-3-small`. Same interface either way, so the choice is ticket 03's. | `langchain-huggingface`, `langchain-openai`, both maintained; OpenRouter docs | [P] LangChain embeddings docs; OpenRouter embeddings docs |
| Re-indexing without re-embedding everything | The indexing API: `index(docs, record_manager, vector_store, cleanup=...)` with `SQLRecordManager`, which can live in the same PostgreSQL database. It hashes content, skips unchanged chunks, and deletes stale ones in `incremental` or `full` mode. | `langchain-core` (`index`), `langchain-classic` (`SQLRecordManager`) | [P] reference |
| Chunking | `langchain-text-splitters` (recursive, Markdown-header aware). | maintained | [P] seen in LangChain docs |
| Agent memory in the same database | `langgraph-checkpoint-postgres` 3.2.0 gives `PostgresSaver`, the PostgreSQL twin of the `SqliteSaver` the Port uses. Moving memory is optional and a separate decision; it is noted because it would put everything the app persists in one store. | maintained (released October 2026) | [P] PyPI |
| Graph through Apache AGE | `AGEGraph` exists only in `langchain-community` (unmaintained) and is built for `GraphCypherQAChain`, which lets the model write Cypher. Neither is wanted here. Graph access in shape D is parameterised SQL in the core, or NetworkX built from the tables. | `langchain-community` | [P] reference |

**Net effect.** With these pieces, shape D is no longer a close second. It has hybrid retrieval
with fused scores from a maintained LangChain package, a pluggable fusion step that can record
what the eval needs, a re-ranker, local or hosted embeddings, incremental indexing and, if
wanted, agent memory in the same store. Its remaining open points are three, and all three are
measurable rather than structural:

1. The keyword leg is `tsvector` ranking, not BM25, unless we add our own leg over
   `pg_textsearch`. The eval set decides whether that matters on our corpus.
2. `pgembed` must be proven on Apple Silicon with the extensions we need. A two-line script.
3. `langchain-postgres` is at version 0.0.x, has already deprecated one store class in favour of
   another, and warns that schema changes need the tables rebuilt. For generated data that is
   rebuilt per run anyway, this is tolerable; it is still a sign to pin the version.

### Lighter graph servers, for completeness

| Server | Licence | Note | Status |
|---|---|---|---|
| Memgraph Community | Business Source License 1.1 as amended; change to Apache-2.0 on 2030-09-10; forbids embedding or distributing to third parties and database-as-a-service use | Not open source; a server to run; in-memory with vector and text indexes | [P] licence file in the repo |
| FalkorDB | SSPLv1 for the server; the GraphRAG SDK is MIT | Redis module; not open source by OSI's definition; a server to run | [P] FalkorDB licence page; SDK repo |
| Apache AGE | Apache-2.0 | A PostgreSQL extension; see shape D | [P] |

Both Memgraph and FalkorDB give the author a licence to think about and a server to run, for
nothing the embedded shape lacks. Ruled out.

### 3.7 Graph stores considered and ruled out, with the reason

The author asked whether other graph options exist. They do. The first pass left most of them
out by familiarity; this table records the evidence.

| Store | Model and query | Licence | Why it is out | Status |
|---|---|---|---|---|
| Neo4j Community | Property graph, Cypher | GPLv3 | Kept as shape A; not a test or eval dependency | [P] |
| Kuzu | Embedded property graph, Cypher | MIT | Archived October 2025 | [V] |
| LadybugDB | Embedded property graph, Cypher, BM25 and HNSW | MIT | **Kept as the embedded Cypher alternative** | [P] |
| Apache AGE | Cypher inside PostgreSQL | Apache-2.0 | Kept inside shape D; needs Docker or a compiled extension | [P] |
| Memgraph | Property graph, Cypher | BSL 1.1 | Licence and a server | [P] |
| FalkorDB | Property graph, Cypher | SSPLv1 | Licence and a server (Redis) | [P] |
| ArangoDB | Multi-model, AQL | BSL 1.1 from 3.12; prepackaged Community binaries limited to internal use and 100 GB; native macOS builds discontinued | Licence, a server, and no macOS binary | [P] ArangoDB 3.12 release notes; BSL policy page |
| TigerGraph | Property graph, GSQL | Proprietary; Community Edition for internal use only, no benchmarking, up to 300 GB | Proprietary, a server, and a licence that forbids publishing comparisons | [P] licence agreement |
| Dgraph | Property graph, DQL and GraphQL | Apache-2.0 | A server with its own query language; nothing the embedded shape lacks | [V] |
| JanusGraph | Property graph, Gremlin | Apache-2.0 | Needs a separate storage backend (Cassandra, HBase or BerkeleyDB) and a JVM | [V] |
| Oxigraph | RDF triples, SPARQL; embeddable through `pyoxigraph` | MIT or Apache-2.0 | A different data model (RDF) from the property graph the course and research note 01 assume; no vector index | [P] GitHub README |
| NetworkX | In-memory property graph, Python API | BSD-3-Clause | **Kept, recommended for phases 0 and 1** | [V] |
| SQLite tables | Relational, recursive SQL | Public domain | Workable; superseded by shape D if the author wants SQL | [V] |

### 3.8 The author's machine (checked 20 October 2026)

The author said PostgreSQL is already installed and that they like it. The machine was checked
with read-only commands. These facts override the platform assumptions made earlier in this note.

| Fact | Consequence |
|---|---|
| The Mac is **Intel (x86_64)**, Homebrew at `/usr/local`. Not Apple Silicon. | Every "Apple Silicon" remark above must be read as "Intel Mac". Several packages ship macOS wheels for ARM64 only. |
| **PostgreSQL 18.6 from Homebrew** (`postgresql@18`), data directory present, server **not running** at check time. | C2 for shape D is already paid. Tests and evals that need PostgreSQL must start the server (`brew services start postgresql@18` or `pg_ctl`) or fail with a clear message. |
| `pgvector` is **not installed**. Homebrew formula `pgvector` 0.8.7 exists with no dependencies; its prebuilt bottles cover ARM64 macOS and Linux only, so on this Mac Homebrew compiles it from source (plain C, needs the Xcode command line tools). | One `brew install pgvector`, then `CREATE EXTENSION vector` per database. |
| `pg_textsearch` supports PostgreSQL 17 and 18; prebuilt binaries are Linux only; macOS builds from source with `make`. | Available if the eval shows `tsvector` ranking is not enough. |
| **LanceDB 0.40.0 ships no Intel-Mac wheel** (macOS wheel is ARM64 only). The last release seen with an x86_64 macOS wheel is 0.24.3 (August 2025). | **Shape B as composed is blocked on this machine** without a Rust source build or an old pinned version. |
| **`pgembed` 0.2.0 ships no Intel-Mac wheel** (ARM64 only). | The embedded-PostgreSQL route is blocked here. Irrelevant now: the system PostgreSQL replaces it. |
| LadybugDB 0.21.2 and Chroma 1.5.9 ship x86_64 macOS wheels. | The Cypher alternative survives; a Chroma-plus-`bm25s` fallback for shape B would also install, with fusion and scores ours. |

Lesson for the register: check the wheel list for `macosx_*_x86_64` before recommending a
native package on this machine.

## 4. Fit against the Port's rules, shape by shape

| Criterion | A: Neo4j CE in Docker | A′: AuraDB Free | B: embedded | C: mixed | D: PostgreSQL via `pgembed` |
|---|---|---|---|---|---|
| C1 architecture | Fine. A driver object created in one factory; Cypher in core functions; routes untouched | Same | Fine. A directory path is "a dataset"; stores opened in one factory | Fine for the graph; the vector half is a network client in core | Fine. A connection opened in one factory; SQL in core functions |
| C2 install | **Docker Desktop must be running for every test and eval run.** Backend tests today need no service | Signup only, but the instance pauses after 3 idle days | `uv add` and nothing else | Signup and a key | `uv add`; a local server process the library manages |
| C3 cost | Free; container memory on the laptop | Free until a 30-day pause deletes the data | Free | Free with quotas | Free |
| C4 eval isolation | **One database per server.** A run must delete every node and rebuild indexes, or start a fresh container per run. Index population must be awaited | Same, over the network | A temporary directory per run, like the eval harness already does with `tempfile` | Per-run collection on a shared cloud instance, subject to quota | A database or data directory per run |
| C5 later move | Cypher ports to Ladybug, Memgraph, FalkorDB | Same | NetworkX or SQLite traversals rewrite behind the seam; Ladybug's Cypher ports to Neo4j with dialect edits | Same as B for the graph | SQL ports to any PostgreSQL; this is the common production shape |
| C6 LangChain | `langchain-neo4j` maintained (MIT); GraphRAG retrievers wrap as tools | Same | Wrap the store's own API as a tool; skip `langchain-community` | Each vendor keeps a LangChain package | `langchain-postgres` maintained, or wrap SQL as a tool |
| C7 offline | Yes once the image is pulled | **No** | **Yes** | **No** | **Yes** |
| Hybrid and re-ranking | Max-normalised union built in; rank fusion and re-ranker through LangChain's generic retrievers plus a score-keeping wrapper | Same | **Built in, BM25, with scores returned** (LanceDB) | Server-side fusion; re-rankers hosted or capped | **Built into LangChain's PostgreSQL store, fused scores returned, fusion pluggable**; keyword leg is `tsvector`, not BM25, unless we add one |

## 5. Recommendation

**Shape D: the author's installed PostgreSQL 18.6, with pgvector, LangChain's PostgreSQL store
for hybrid retrieval, a cross-encoder re-ranker through LangChain, and the organisation's ground
truth as tables. The graph is traversed by parameterised SQL in the core, or by NetworkX built
from those tables, behind one seam.** Keep Neo4j Community Edition as the documented later move
and as the optional demo target, not as a dependency of tests or evals.

How the recommendation moved, so the grilling can see the reasoning:

| Version | Recommendation | What changed it |
|---|---|---|
| First | B, LanceDB plus NetworkX | Judged on what each store ships |
| Second | B and D as peers | The author asked about pgvector and LangChain; section 3.6 showed LangChain's PostgreSQL store has hybrid search, fusion and fused scores built in |
| Third, this one | **D on the installed PostgreSQL** | Section 3.8: the machine is an Intel Mac with PostgreSQL 18.6 already installed; LanceDB and `pgembed` ship no Intel-Mac wheels, so B is blocked without a fallback and D's install cost is already paid |

The reasons below were written for B. Points 1, 3, 4 and 5 hold for D as well. Point 2 is now
the one measurable open point of D rather than an argument against it.

Why this composition and not another:

1. **The eval gate decides.** Tier 3 accepts phase 1 on an eval run that the author or Codex can
   repeat without Claude. A run that needs Docker up, a wiped single database and awaited indexes
   is a run that fails for reasons unrelated to retrieval quality. A run that builds two indexes
   in a temporary directory from pinned files is a run that fails only when retrieval is wrong.
2. **Hybrid with re-ranking is first-class in LanceDB and nowhere else at this size.** BM25,
   vector search, reciprocal rank fusion and a local cross-encoder are built in and return their
   scores, which is what the two-layer measurement the map demands (retrieval layer versus answer
   layer) needs to record. Every other shape gets fusion and re-ranking from LangChain's generic
   `EnsembleRetriever` and `CrossEncoderReranker`, which return documents without scores, so a
   wrapper of ours has to recover the per-leg ranks and the fused score for the eval. The gap is
   smaller than the first version of this note said, but it is still a gap in evidence, not in
   features.
3. **The graph is small and its questions are bounded traversals.** Account to group to asset,
   account to device to other accounts, spray targets, technique to mitigation. Phase 4's attack
   path is a shortest-path call. NetworkX does these in plain, testable Python, loads from the
   generated ground-truth files, and keeps the log as the source of truth, as research note 01
   concluded. Persistence is not a requirement, because the data is generated.
4. **The read-only tools become safer by construction.** Hand-written, parameterised traversal
   functions exposed as `@tool` are the shape ticket 05 should adopt anyway. LangChain's
   `GraphCypherQAChain` lets the model write Cypher and requires an explicit "dangerous requests"
   opt-in [V]; it has no place in a Tier 3 investigator.
5. **Licences stay permissive and the dependency count stays small.** Apache-2.0 and BSD, two
   libraries, no server, no key.

**Trade-offs the author must accept**

| Giving up | Why it is acceptable now | What reopens it |
|---|---|---|
| Cypher and a "real" graph database to show clients | The knowledge graph is the data model and the traversals, not the engine. The seam keeps the engine swappable | If the author wants Cypher as a skill or a selling point, choose **LadybugDB** (embedded, MIT, Cypher, BM25 and HNSW in one file) over NetworkX. It is the credible middle path. Its risk is maturity: a twelve-month-old fork at version 0.x with weekly releases, and no LangChain package |
| Neo4j's ecosystem (Browser, Bloom, the course demo's exact code) | The demo was read as a shape reference, not a target | A later demo or GRC slice may justify running Neo4j CE in Docker as an *additional* backend of the same seam |
| One store for everything | Two embedded libraries instead of one server; chunk-to-entity links live as chunk metadata (entity IDs) in LanceDB and are resolved in the graph | LadybugDB would give one store with Cypher, at the maturity cost above. **PostgreSQL through `pgembed` (shape D) would give one store with SQL**, relational ground truth, and the most transferable skill, at the cost of writing and testing fusion and re-ranking ourselves and depending on a young packaging project. If the author weighs "one store and SQL" above "built-in, measurable hybrid retrieval", shape D wins |

**Conditions that travel with the recommendation into the spec**

1. Tests and evals that touch PostgreSQL get one fixture that connects to the local server,
   creates a database per run from pinned inputs, and drops it afterwards. If the server is not
   running, the fixture fails with a message that says how to start it. The rest of the test
   suite keeps running without PostgreSQL.
2. `langchain-postgres` is pinned to an exact version, like `langchain` already is.
3. The keyword leg starts as `tsvector` ranking through LangChain's store. The first
   retrieval-layer question in ticket 06's eval set is whether that is enough; if not, a BM25 leg
   over `pg_textsearch` is added through the pluggable fusion function.
4. Fusion is a function of ours passed to LangChain's store, so that each leg's rank and the
   fused score are recorded for the eval from day one.

**What the recommendation rules out**

- AuraDB Free: pauses after 3 idle days, deletes after 30; never offline.
- Hosted vector tiers (Qdrant, Pinecone, Weaviate): never offline; idle-deletion policies.
- Memgraph, FalkorDB, ArangoDB, TigerGraph: restrictive or proprietary licences and a server,
  for nothing we lack. Dgraph and JanusGraph: servers with their own query languages and, for
  JanusGraph, a separate storage backend. Oxigraph: RDF, a different data model.
- PostgreSQL in Docker with Apache AGE: a Neo4j-class choice with the same Docker-in-every-test
  cost and AGE's version coupling. The installed PostgreSQL is used instead.
- LanceDB on this machine: no Intel-Mac wheel at 0.40.0. Shape B would need Chroma plus
  `bm25s` with fusion and scores ours, which loses the one advantage B had.
- Kuzu upstream: archived.
- `langchain-community` retrievers and re-rankers: unmaintained; core wraps the store directly.
- Model-written Cypher as an agent tool.

## 6. What the seam looks like (for the spec, not for building yet)

- One factory, beside `make_model` and `build_agent`, that opens the knowledge base from a
  directory: ground-truth files for the graph, documents for the corpus, built indexes.
  "The API asks the core for a dataset" extends naturally: a different directory is a different
  organisation. This answers part of the map's open item on dataset swapping; ticket 04 decides
  the rest.
- Two protocols in the core: a graph store (bounded, named traversals) and a corpus (hybrid search
  returning chunks with their scores, ranks and entity IDs). Tools, API and eval all call these.
- The eval harness builds both into a temporary directory per run from pinned inputs and records
  chunk IDs, ranks from each leg, the fusion score, the re-ranker score and the traversed entity
  IDs, so the retrieval layer is measurable on its own.

## 7. Hand-offs to later tickets

| Ticket | What this note leaves to it |
|---|---|
| 03 Embedding model, keyword search, re-ranker | Which embedder: local sentence-transformers through `HuggingFaceEmbeddings` (offline, deterministic) or OpenRouter through `OpenAIEmbeddings` (OpenRouter serves `/api/v1/embeddings`, verified). Which cross-encoder. First fusion: reciprocal rank fusion in both shapes (LanceDB `RRFReranker`; `langchain-postgres` `reciprocal_rank_fusion`). **If D is chosen: whether `tsvector` ranking is enough or a BM25 leg over `pg_textsearch` is needed, decided by the eval** |
| 04 Synthetic organisation and ground truth | The graph's source files are the ground truth; their format decides the loader. Dataset swap by directory |
| 05 Agent tools | Hand-written, parameterised, read-only traversal and search functions as `@tool`; no model-written queries |
| 06 Eval design | The per-run temporary build; the retrieval-layer record fields listed in section 6 |

## 8. Evidence gaps

- The Kuzu archive and Apple acquisition were not opened on GitHub or in a primary filing; four
  independent sources agree.
- Hosted free-tier figures (Qdrant, Pinecone, Weaviate) come from the research pass and
  aggregators quoting vendor pricing pages. Nothing in the recommendation depends on them, since
  shape C fails on offline alone.
- NetworkX's licence and `simple-graph` were not opened; both are well known and low risk.
- Whether LadybugDB's `INSTALL FTS` / `INSTALL VECTOR` needs network access at first use was not
  checked. It matters only if the author chooses the LadybugDB alternative.
- `GraphCypherQAChain`'s dangerous-requests flag was reported by the research pass and matches the
  LangChain reference page listing, not opened in full.
- `pgembed` is moot on this machine (no Intel-Mac wheel; section 3.8). `pgvector` and
  `pg_textsearch` will be compiled from source by Homebrew or `make`; neither build was run in
  this research. The first build step of phase 0 proves them.
- pgvector's licence was opened; `pg_textsearch`'s PostgreSQL License comes from the repository
  description, not the licence file.
- No source measures retrieval quality of these stores on our kind of corpus. The eval set, not
  this note, will.

## Sources

Primary, opened in this research:

- Neo4j Operations Manual, introduction and editions: https://neo4j.com/docs/operations-manual/current/introduction/
- Neo4j Operations Manual, Docker introduction: https://neo4j.com/docs/operations-manual/current/docker/introduction/
- Neo4j Operations Manual, Docker configuration: https://neo4j.com/docs/operations-manual/current/docker/configuration/
- Neo4j Operations Manual, index configuration: https://neo4j.com/docs/operations-manual/current/performance/index-configuration/
- Neo4j upgrade guide, multiple databases (Community limitation): https://neo4j.com/docs/upgrade-migration-guide/current/version-4/migration/drivers/multiple-db/
- Neo4j Cypher Manual, vector indexes: https://neo4j.com/docs/cypher-manual/current/indexes/search-indexes/vector-indexes/
- Neo4j Cypher Manual, full-text indexes (4.4 edition; current page cited by the research pass): https://neo4j.com/docs/cypher-manual/4.4/indexes-for-full-text-search/
- Neo4j developer guide, hybrid search: https://neo4j.com/developer/genai-ecosystem/hybrid-search/
- Neo4j licensing: https://neo4j.com/licensing/
- Neo4j pricing: https://neo4j.com/pricing/
- Neo4j Aura quotas and limits: https://neo4j.com/docs/aura//quotas-and-limits/
- Neo4j support, Aura Free FAQ: https://support.neo4j.com/s/article/16094506528787-Support-resources-and-FAQ-for-Aura-Free-Tier
- Neo4j support, pausing and auto-delete policy: https://support.neo4j.com/s/article/17480821630355--Aura-Instance-Access-Issues-Understanding-Pausing-Resuming-and-Auto-Delete-Policy
- Neo4j free graph database page (conflicting limit): https://neo4j.com/free-graph-database/
- neo4j-graphrag-python API: https://neo4j.com/docs/neo4j-graphrag-python/current/api.html
- neo4j-graphrag-python user guide: https://neo4j.com/docs/neo4j-graphrag-python/current/user_guide_rag.html
- neo4j-graphrag-python hybrid retriever source: https://neo4j.com/docs/neo4j-graphrag-python/current/_modules/neo4j_graphrag/retrievers/hybrid.html
- neo4j-graphrag-python types source (rankers): https://neo4j.com/docs/neo4j-graphrag-python/current/_modules/neo4j_graphrag/types.html
- Neo4j Labs, LangChain integration: https://neo4j.com/labs/genai-ecosystem/genai-frameworks/langchain-agents/
- PyPI neo4j-graphrag: https://pypi.org/project/neo4j-graphrag/
- PyPI neo4j: https://pypi.org/project/neo4j/
- PyPI langchain-neo4j: https://pypi.org/project/langchain-neo4j/
- LangChain docs, Neo4j vector store: https://docs.langchain.com/oss/python/integrations/vectorstores/neo4jvector
- LangChain reference, Neo4jVector: https://reference.langchain.com/python/langchain-neo4j/vectorstores/neo4j_vector/Neo4jVector
- LangChain v1 release notes (`langchain-classic`): https://docs.langchain.com/oss/python/releases/langchain-v1
- LangChain reference, EnsembleRetriever: https://reference.langchain.com/python/langchain-classic/retrievers/ensemble/EnsembleRetriever
- LangChain reference, weighted_reciprocal_rank (returns documents only): https://reference.langchain.com/python/langchain-classic/retrievers/ensemble/EnsembleRetriever/weighted_reciprocal_rank
- LangChain reference, HybridSearchConfig (langchain-postgres v2): https://reference.langchain.com/python/langchain-postgres/v2/hybrid_search_config/HybridSearchConfig
- LangChain reference, weighted_sum_ranking: https://reference.langchain.com/python/langchain-postgres/v2/hybrid_search_config/weighted_sum_ranking
- langchain-postgres hybrid search unit tests: https://github.com/langchain-ai/langchain-postgres/blob/main/tests/unit_tests/v2/test_async_pg_vectorstore_search.py
- LangChain reference, PGVectorStore.similarity_search_with_score: https://reference.langchain.com/python/langchain-postgres/v2/vectorstores/PGVectorStore/similarity_search_with_score
- LangChain reference, CrossEncoderReranker: https://reference.langchain.com/python/langchain-classic/retrievers/document_compressors/cross_encoder_rerank/CrossEncoderReranker
- LangChain reference, BaseCrossEncoder: https://reference.langchain.com/python/langchain-classic/retrievers/document_compressors/cross_encoder/BaseCrossEncoder
- LangChain reference, indexing `index()`: https://reference.langchain.com/python/langchain-core/indexing/api/index
- LangChain reference, SQLRecordManager: https://reference.langchain.com/python/langchain-classic/indexes/_sql_record_manager/SQLRecordManager
- LangChain docs, Hugging Face embeddings: https://docs.langchain.com/oss/python/integrations/embeddings/huggingfacehub
- LangChain docs, embedding integrations: https://docs.langchain.com/oss/python/integrations/embeddings
- LangChain reference, AGEGraph (langchain-community): https://reference.langchain.com/python/langchain-community/graphs/age_graph/AGEGraph/query
- PyPI langgraph-checkpoint-postgres: https://pypi.org/project/langgraph-checkpoint-postgres/
- OpenRouter embeddings docs: https://openrouter.ai/docs/api_reference/embeddings
- Homebrew formula pgvector (JSON API): https://formulae.brew.sh/api/formula/pgvector.json
- PyPI JSON for wheel lists: https://pypi.org/pypi/lancedb/json , https://pypi.org/pypi/pgembed/json , https://pypi.org/pypi/ladybug/json , https://pypi.org/pypi/chromadb/json
- LangChain docs, cross-encoder re-ranker (carries the `langchain-community` unmaintained note): https://docs.langchain.com/oss/python/integrations/document_transformers/cross_encoder_reranker
- LanceDB docs, hybrid search: https://docs.lancedb.com/search/hybrid-search
- LanceDB docs, re-ranking: https://docs.lancedb.com/reranking
- LanceDB docs, cross-encoder re-ranker: https://docs.lancedb.com/reranking/cross_encoder
- LanceDB docs, evaluating hybrid search: https://docs.lancedb.com/reranking/eval
- PyPI lancedb: https://pypi.org/project/lancedb/
- LadybugDB installation and licence: https://docs.ladybugdb.com/installation/
- LadybugDB full-text search extension: https://docs.ladybugdb.com/extensions/full-text-search/
- LadybugDB vector extension: https://docs.ladybugdb.com/extensions/vector/
- PyPI ladybug: https://pypi.org/project/ladybug/
- GitHub LadybugDB/ladybug: https://github.com/LadybugDB/ladybug
- GitHub LadybugDB/ladybug-classic (the `real_ladybug` package): https://github.com/LadybugDB/ladybug-classic
- PyPI chromadb: https://pypi.org/project/chromadb/
- PyPI sqlite-vec: https://pypi.org/project/sqlite-vec/
- PyPI bm25s: https://pypi.org/project/bm25s/
- PyPI FlashRank: https://pypi.org/project/FlashRank/
- Memgraph BSL licence text: https://github.com/memgraph/memgraph/blob/master/licenses/BSL.txt
- FalkorDB licence page: https://docs.falkordb.com/references/license
- FalkorDB GraphRAG SDK (MIT): https://github.com/FalkorDB/GraphRAG-SDK
- pgvector README: https://github.com/pgvector/pgvector/blob/master/README.md
- pgvector LICENSE: https://github.com/pgvector/pgvector/blob/master/LICENSE
- PostgreSQL manual, controlling text search (ranking): https://www.postgresql.org/docs/current/textsearch-controls.html
- Timescale pg_textsearch: https://github.com/timescale/pg_textsearch
- ParadeDB pg_search: https://github.com/paradedb/paradedb/tree/dev/pg_search
- Apache AGE overview: https://age.apache.org/overview/
- Apache AGE quick start: https://age.apache.org/getstarted/quickstart/
- Apache AGE downloads: https://age.apache.org/download/
- Apache AGE releases: https://github.com/apache/age/releases
- PyPI pgembed: https://pypi.org/project/pgembed/
- GitHub embedded-postgres: https://github.com/kainpl/embedded-postgres
- PyPI langchain-postgres: https://pypi.org/project/langchain-postgres/
- LangChain docs, PGVector: https://docs.langchain.com/oss/python/integrations/vectorstores/pgvector
- ArangoDB 3.12 incompatible changes (licence): https://docs.arango.ai/arangodb/stable/release-notes/version-3.12/incompatible-changes-in-3-12/
- ArangoDB BSL policy: https://arango.ai/legal/arango-bsl-policy/
- TigerGraph licence agreement: https://www.tigergraph.com/license-agreement/
- Oxigraph README: https://github.com/oxigraph/oxigraph/blob/main/README.md

Secondary, cited by the research pass or aggregators and not opened:

- Kuzu archive coverage: https://www.theregister.com/software/2025/10/14/kuzudb-graph-database-abandoned-community-mulls-options/ ; https://gdotv.com/blog/kuzu-legacy-embedded-graph-database-landscape/ ; https://www.puppygraph.com/blog/what-is-kuzudb
- GitHub kuzudb/kuzu (archived): https://github.com/kuzudb/kuzu
- Dgraph: https://dgraph.io ; JanusGraph: https://janusgraph.org
- NetworkX: https://github.com/networkx/networkx
- simple-graph: https://github.com/dpapathanasiou/simple-graph
- Qdrant pricing: https://qdrant.tech/pricing/ ; hybrid queries: https://qdrant.tech/documentation/search/hybrid-queries/
- Pinecone object limits: https://docs.pinecone.io/reference/api/database-limits/object-limits ; hybrid search: https://docs.pinecone.io/guides/search/hybrid-search
- Weaviate Cloud cluster creation: https://docs.weaviate.io/cloud/manage-clusters/create ; hybrid: https://docs.weaviate.io/weaviate/search/hybrid
- LangChain reference, GraphCypherQAChain: https://reference.langchain.com/python/langchain-neo4j/chains/graph_qa/cypher/GraphCypherQAChain
- Apache AGE: https://github.com/apache/age
