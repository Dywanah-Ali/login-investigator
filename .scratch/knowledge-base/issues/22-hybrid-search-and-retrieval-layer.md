# 22: Hybrid search and the retrieval layer alone

Type: build
Status: claimed
Blocked by: 19, 21
Phase: 0
Model: strongest (Fable 5.1 or Astra)

## What to build

The knowledge-base door gains corpus search: a vector leg and a keyword leg, filtered before their
limits and fused by our own reciprocal rank fusion, returning a verdict of `none`, `weak` or `found`
with the chunks. A retrieval runner calls the search and the graph walk directly, with no model, and
checks the first questions' gold IDs on every build.

## Decisions implemented

- T02 d3 (PostgreSQL's built-in text ranking first), T02 d10 and T03 d7 (our own fusion, k = 60,
  equal legs, 20 plus 20, 1-based ranks, every score recorded, three library traps each with a
  test), T03 d6 (filters inside both legs before their limits, exact vector search, typed options),
  T03 d1 (three verdicts computed in code; the `none` rule stays off until ticket 39).
- T06 d1 (retrieval gate, first check), T06 d2 (graph gate), T06 d8 (the retrieval layer alone, with
  the integrity check as its precondition).
- User stories 72, 73, 77. Spec door 2.

## Acceptance criteria

- [ ] Before any build work starts, the builder tells the author this ticket's `Model:` line and
      asks the author to set that model. The build starts only after the author confirms, and a
      dated line under Comments records the model used.
- [ ] Search runs a vector leg and a keyword leg; filters apply inside both before their limits;
      vector search is exact with no approximate index.
- [ ] Fusion is our own, k = 60, equal legs, 20 plus 20 candidates, 1-based ranks. Each candidate
      records its dense rank, keyword rank, raw cosine distance, raw keyword score and fused score.
- [ ] Three trap tests: the fusion function is set explicitly; both candidate limits are set
      explicitly; a fresh configuration is built per call, proven by a two-question regression test.
- [ ] The verdict is computed in code from recorded scores; the `none` rule is off and its switch is
      tested.
- [ ] Door 2 tests use the fake embedder.
- [ ] The retrieval runner calls search and walk directly, runs the integrity check first, checks
      every gold chunk ID among the 20 fused candidates, records the rank of the first gold chunk,
      and checks the walk returns exactly the gold record set.
- [ ] The first real run on the first questions is recorded per question. Every miss is fixed or
      logged in the bug log with its cause.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged.

## Comments

2026-10-29 — Codex: author confirmed Astra before build work. Implementing with TDD at the
spec's agreed doors 2 (knowledge-base core) and 6 (retrieval runner). Local commit only.

2026-10-29 — Author: until calibration, return `weak` with an explicit `not_calibrated`
reason; keep the `none` rule disabled. No invented relevance threshold.

2026-10-29 — Codex: langchain-postgres 0.0.19; Context Hub search had no matching package guide.
Official [PGVectorStore how-to](https://github.com/langchain-ai/langchain-postgres/blob/main/examples/pg_vectorstore_how_to.ipynb)
read through GitHub API: per-query hybrid configuration, custom fusion callback, candidate limits,
typed-column filters. The migrated API-reference page lacks this detail. Installed 0.0.19 source
separately checked: filters precede both limits, cosine distance and ts_rank_cd reach the callback,
and query/config mutation requires a fresh config each time. Existing embedding factory reused.

2026-10-29 — Codex: first live retrieval run saved as
`backend/evals/results/2026-10-29-102711-909238-retrieval-0180733adbd4.json`.
K01/K02/K03/K07/K08 pass; K04 misses the MFA exception register (exact dense diagnostic rank
115, keyword leg empty; B-098/AUD-062); K05/K06 return the agreed uncalibrated `weak` (B-099,
T39). Both graph gates pass. No question, gold or corpus edits. Seven query embeddings:
138 tokens, $0.00000276; separate K04 diagnostic: 36 tokens, $0.00000072.

2026-10-29 — Codex: builder choices within scope: original question text feeds both search
legs; graph execution inputs live separately in `evals/retrieval_requests.json`; all candidates
and the final top 20 are saved. The existing runner gains `--layer retrieval`, shared saving
and offline rescoring; its summary is separate and has no borrowed pass-rate target. Core
verdict policy accepts an explicit cosine-similarity threshold for offline switch tests only;
no live threshold is supplied. Two supported chunks produce `found`, one produces `weak`,
and zero produces `none` only with its calibrated rule explicitly enabled, following T03's
staged design. T23 will supply re-ranker scores; T39 owns real calibration.

2026-10-29 — Codex: focused checks: 21 passed with one B-094/AUD-061 teardown recurrence.
Retried cleanup of the exact leftover database successfully; no privilege change. Typecheck
clean. Full safety net and two-axis review pending before closure.
