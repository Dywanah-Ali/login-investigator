# 03: Embedding model, keyword search and re-ranker

Type: research
Status: open
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
- Record the "I don't know" path: what retrieval returns when nothing scores well, and how the
  agent must answer.
- Save one cited note at `../research/03-embedding-and-reranking.md`.

## Acceptance

- [ ] Defaults recommended for embedding, chunking, keyword, fusion and re-ranking, with reasons.
- [ ] The refusal path designed before the happy path.
- [ ] Findings presented to the author; the choice is recorded here under `## Answer`.

## Comments
