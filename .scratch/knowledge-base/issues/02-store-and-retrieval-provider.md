# 02: Where the graph lives and where retrieval runs

Type: research
Status: open
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

- [ ] Three shapes compared on the criteria above, with primary-source citations.
- [ ] Recommendation stated with its trade-offs and what it rules out.
- [ ] Findings presented to the author; the choice is recorded here under `## Answer`.

## Comments
