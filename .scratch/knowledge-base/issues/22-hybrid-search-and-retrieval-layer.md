# 22: Hybrid search and the retrieval layer alone

Type: build
Status: resolved
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

- [x] Before any build work starts, the builder tells the author this ticket's `Model:` line and
      asks the author to set that model. The build starts only after the author confirms, and a
      dated line under Comments records the model used.
- [x] Search runs a vector leg and a keyword leg; filters apply inside both before their limits;
      vector search is exact with no approximate index.
- [x] Fusion is our own, k = 60, equal legs, 20 plus 20 candidates, 1-based ranks. Each candidate
      records its dense rank, keyword rank, raw cosine distance, raw keyword score and fused score.
- [x] Three trap tests: the fusion function is set explicitly; both candidate limits are set
      explicitly; a fresh configuration is built per call, proven by a two-question regression test.
- [x] The verdict is computed in code from recorded scores; the `none` rule is off and its switch is
      tested.
- [x] Door 2 tests use the fake embedder.
- [x] The retrieval runner calls search and walk directly, runs the integrity check first, checks
      every gold chunk ID among the 20 fused candidates, records the rank of the first gold chunk,
      and checks the walk returns exactly the gold record set.
- [x] The first real run on the first questions is recorded per question. Every miss is fixed or
      logged in the bug log with its cause.
- [x] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged.
      Evidence: 646 backend assertions passed; the full command exited 1 on known B-094 cleanup,
      exact cleanup succeeded and the affected test reran clean (1 passed, exit 0). Frontend
      149 passed; both typechecks clean; all three review findings resolved. This records the
      recovered flaky teardown explicitly, not a clean full-suite command.

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

2026-10-29 — Codex: two-axis review found two Standards items and one Spec evidence gap,
all fixed and independently confirmed. The stale-command regression was red, then passed;
the stronger filter test also passed (2/2 focused). Pyright: 0 errors. See
[review note](../reviews/22-code-review-2026-10-29.md). The final reviewed live run is
`backend/evals/results/2026-10-29-103513-294903-retrieval-b6941a3d42d1.json`, with identical
per-question outcomes. The admin manual's live and offline-rescore commands were tested from
the repository root. Three complete live runs plus the single diagnostic total $0.000009;
offline rescore makes no model call. Full safety net pending.

2026-10-29 — Codex: final safety net: backend 646 passed, 1 existing teardown error in 559.22s
(B-094/AUD-061, full command exit 1). Cleaned only its exact leftover database and reran the
affected unchanged graph test: 1 passed in 2.16s, exit 0, including teardown. Frontend 149
passed across 13 files, exit 0. Backend Pyright and frontend TypeScript: clean. Frontend lint:
exit 0 with six existing AUD-009 warnings. No new assertion failure; the fixture concern stays
open for T44. Port live eval not run because agent behaviour, tools and prompts did not change.
Resolved on this evidence and the ticket's explicit allowance for logged retrieval misses;
the initiative retrieval gate remains unmet until the recorded gaps are addressed. Local
commits only, no push.

## Answer

Corpus search is available at `KnowledgeBase.search_corpus`, using PostgreSQL's exact vector
search and built-in keyword ranking through the pinned LangChain store. Filters precede each
20-result limit, our 1-based RRF combines them into 20, and the artifact retains every candidate's
leg ranks, raw scores and fused score. Results are uncalibrated `weak` by the author's ruling.

`uv run --directory backend python -m evals.run --layer retrieval` calls the core directly,
checks graph integrity first, grades the original T21 gold, and saves separate retrieval
evidence. A saved result can be rescored offline. The original questions and gold are unchanged.

| Question | First required passage rank | Result |
|---|---|---|
| K01 current password policy | 2 | Pass |
| K02 MFA exceptions | 3 | Pass |
| K03 Hannah's groups | Not applicable | Exact records and paths pass |
| K04 S6 mixed question | 9 | Graph passes; MFA exception register missing from top 20 |
| K05 absent retention policy | Not applicable | `weak`, expected `none`; calibration deferred |
| K06 absent incident write-up | Not applicable | `weak`, expected `none`; calibration deferred |
| K07 approved travel | 3 | Required clearing passage found |
| K08 laptop handover | 4 | Required clearing passage found |

These are retrieval checks, not agent answers or benign/threat judgements. T22 permits logged
misses; it does not waive the later initiative gate. B-098/AUD-062 tracks K04's candidate gap;
B-099 tracks the intended uncalibrated refusals until T39. A re-ranker alone cannot fix K04.
