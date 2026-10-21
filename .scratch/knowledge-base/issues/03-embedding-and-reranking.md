# 03: Embedding model, keyword search and re-ranker

Type: research
Status: resolved
Blocked by: 02

## Question

Which embedding model, which keyword method and which re-ranker does the retrieval stack use at
sensible defaults, so that tuning follows measurement rather than guesswork?

## Scope

- Embedding model: candidates reachable through OpenRouter or a local model; dimension and chunk
  size matched together; cost per run of the eval set.
- Keyword method: BM25 or the store's full-text index, per the answer to ticket 02.
- Fusion and re-ranking: reciprocal rank fusion as the default fusion; whether a cross-encoder
  re-ranker is worth its latency for a corpus of a few dozen documents; what runs locally.
- Chunking defaults for policy, runbook, ATT&CK and incident documents.
- Metadata filters (added by the author, 21 October 2026): which fields the retriever can filter
  on, how a filter combines with the hybrid search, and when the agent should narrow before
  searching. Ticket 04 chooses the exact fields with the corpus; this ticket sets the mechanism
  and the defaults.
- Record the "I don't know" path: what retrieval returns when nothing scores well, and how the
  agent must answer.
- Save one cited note at `../research/03-embedding-and-reranking.md`.

## Acceptance

- [x] Defaults recommended for embedding, chunking, keyword, fusion, re-ranking and metadata
      filtering, with reasons. Evidence: research note 03, section 5.
- [x] The refusal path designed before the happy path. Evidence: research note 03, section 3.7;
      grilling question 1 was the refusal path.
- [x] Findings presented to the author; the choice is recorded here under `## Answer`.

## Answer

Grilled and ruled by the author on 21 October 2026, one question at a time. Seven decisions.

| # | Decision |
|---|---|
| 1 | **Refusal path: three verdicts, computed in code.** The corpus search tool returns `none`, `weak` or `found` with the chunks, from recorded scores, before the model sees anything. The threshold between them is calibrated on the eval set (Cohere's borderline-pairs procedure, 30 to 50 pairs) **before** the `none` rule is switched on; until then the system answers and the eval shows how often it should have refused. The system prompt is a second lock, never the only one. The screen shows a refusal as a result with the closest misses beneath it (ticket 07). |
| 2 | **Embeddings: `openai/text-embedding-3-small` through OpenRouter at 1,536 dimensions**, via `OpenAIEmbeddings` with `check_embedding_ctx_length=False`. Model name and vector length in one configuration place; a change is a rebuild. **No local models** (author's ruling during the research). |
| 3 | **Chunking: structure first, with a context header.** Cut at Markdown headings, then by token size only inside an over-long section; overlap never crosses a section. Every chunk starts with the document title and section path (plus technique or incident ID). Sizes per document kind as in note 03 section 3.2 are hypotheses that ticket 04 confirms against the real corpus. ATT&CK content is loaded from the STIX bundle, assembled from several linked objects, with MITRE's licence notice in the corpus folder. |
| 4 | **Exact identifiers are labels, not prose.** Single-value identifiers (technique ID, incident ID) are typed columns on the chunk; lists (accounts and hosts a chunk mentions) live in a `chunk_mentions_entity` link table that also feeds the NetworkX `mentions` edges (ticket 02, decision 7). Word search stays PostgreSQL's built-in ranking for prose (ticket 02, decision 3); phase 0 records `ts_debug` output for one technique ID, hostname, IP and email. |
| 5 | **Re-ranker on, behind a switch; the eval decides.** `cohere/rerank-v3.5` through OpenRouter's rerank endpoint, our own document compressor behind the `ContextualCompressionRetriever` seam, 20 candidates re-ordered, best 5 kept. The eval runs with and without it; the default ships whichever wins on precision at 5 and the refusal metrics. Its score drives decision 1's verdict. Cohere Rerank 5 is a watch item (AUD-035). |
| 6 | **Metadata filtering: typed columns, filters before both legs, typed tool options.** Shared labels every chunk has (document type, technique ID, incident ID, version, effective date) are typed, filterable columns. Per-kind details live in the JSON column and travel with results for citations; a field is promoted to a column only when filtering on it proves necessary. Filters apply inside both the vector and keyword queries before their limits, and vector search stays exact (no approximate index) in phases 0 and 1. The agent chooses typed options on the tool; the code builds the filter; the model never writes one. Exact field list per document kind is ticket 04's. |
| 7 | **Fusion: our reciprocal rank fusion, and the three library traps become spec conditions with tests.** k = 60, equal legs, 20 + 20 candidates, 1-based ranks, every candidate's dense rank, keyword rank, raw cosine distance, raw `ts_rank_cd` and fused score recorded (ticket 02, decision 10). Traps, each with a test: the fusion function is set explicitly (the library default is weighted sum); `primary_top_k` and `secondary_top_k` are set explicitly (library default 4); a fresh `HybridSearchConfig` is built per call (the library writes the first query into a reused config), proven by a two-question regression test. |

Conditions carried into the spec (note 03, section 7): `langchain-postgres` 0.0.19,
`langchain-text-splitters` and `tiktoken` pinned; the embedder flag with a one-string test through
OpenRouter; the three trap tests; `ts_debug` outputs recorded in phase 0; refusal stage B off
until the calibration set exists; one OpenRouter key for chat, embeddings and re-ranking, in `.env`.

Hand-offs: ticket 04 (final metadata columns per kind, the link table, corpus folder format with
the ATT&CK notice, techniques in scope, canary questions, chunk sizes against real documents),
ticket 05 (tool signatures with typed filter options, the structured result with verdict, prompt
wording for `none` and `weak`), ticket 06 (record fields, threshold calibration, penalty-aware
scoring, with-and-without re-ranker comparison, Langfuse decision AUD-036), ticket 07 (how the
three verdicts and the closest misses look).

## Comments

- 2026-10-21, Claude: claimed. Scope widened by the author to include metadata filters. Research
  honours ticket 02's decisions: PostgreSQL store through `langchain-postgres`, built-in keyword
  ranking first, reciprocal rank fusion through our own score-keeping function, re-ranker through
  `langchain-classic`, embeddings local or through OpenRouter, Intel Mac.
- 2026-10-21, author: **no local models.** Ruled during the research. Embeddings and re-ranking
  go through OpenRouter.
- 2026-10-21, Claude: research done. Note at
  [../research/03-embedding-and-reranking.md](../research/03-embedding-and-reranking.md).
  Recommendation, seven defaults (note section 5): `openai/text-embedding-3-small` via OpenRouter
  at 1,536 dimensions; structure-first chunking with a context header on every chunk and sizes per
  document kind; PostgreSQL built-in ranking kept, identifiers moved to metadata; our reciprocal
  rank fusion with k = 60 and 20 + 20 candidates; `cohere/rerank-v3.5` through OpenRouter's rerank
  endpoint, 20 to 5, switchable; typed filter columns plus an entity link table, filters applied
  before both legs, typed tool parameters; a refusal path that computes a `none` / `weak` /
  `found` verdict in code from recorded scores, with the re-ranker threshold calibrated on the
  eval set before it is switched on. Three implementation traps found in the LangChain source and
  carried as spec conditions. Awaiting the grilling that records the choice.
