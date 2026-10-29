# 23: The re-ranker behind its switch

Type: build
Status: resolved
Blocked by: 22
Phase: 0
Model: standard (Opus 5.5 or Sol 6.1)

## What to build

Corpus search gains a re-ranking step behind a switch: Cohere's re-ranker re-orders the 20 fused
candidates and keeps the best 5, and its score drives the verdict. With the switch off, search
behaves as ticket 22 left it.

## Decisions implemented

- T03 d5 (`cohere/rerank-v3.5` through OpenRouter's rerank endpoint, our own document compressor
  behind LangChain's compression-retriever seam, 20 to 5, behind a switch, its score drives the
  verdict).
- T03 d1 and T06 d9 (with the re-ranker off, `none` falls back to the empty-result rule).
- [spec ruling] door 2 uses a fake re-ranker. API contract change 5 (the re-ranker switch setting).

## Acceptance criteria

- [x] Before any build work starts, the builder tells the author this ticket's `Model:` line and
      asks the author to set that model. The build starts only after the author confirms, and a
      dated line under Comments records the model used.
- [x] Our own document compressor calls the rerank endpoint behind LangChain's compression-retriever
      seam and keeps the best 5 of 20.
      Evidence: `Reranker(BaseDocumentCompressor)` and `OpenRouterReranker` in
      `knowledge_base/reranking.py`; `test_the_compressor_slot_keeps_the_best_five_of_twenty_with_their_scores`;
      the request shape in `test_every_candidate_is_scored_in_one_request_and_scores_return_in_input_order`.
- [x] One setting switches it on and off; `env.example` and the contract's configuration section
      name it.
      Evidence: `LI_RERANKER` in `backend/env.example` and `docs/api-contract.md`; the reading
      rule in `test_the_switch_reads_the_environment_then_env_file_then_defaults_to_on`.
- [x] With the switch on, the re-ranker's score drives the verdict and is recorded per candidate.
      Evidence: `test_with_the_reranker_on_its_score_drives_the_verdict` (a cosine threshold never
      judges re-ranked chunks); `test_reranker_scores_the_fused_twenty_and_search_keeps_its_best_five`.
- [x] With the switch off, the verdict falls back to the empty-result rule; a test proves it.
      Evidence: `test_verdict_uses_recorded_scores_and_none_requires_an_enabled_calibrated_rule`
      (zero passages give `none` / `empty_result`, on and off, per the author's ruling).
- [x] Door 2 tests use a fake re-ranker; one real call is recorded.
      Evidence: `NumberReranker`, `BrokenReranker`, `LengthReranker`, and `httpx.MockTransport`
      for the adapter; live runs `2026-10-29-150414-681065-retrieval-0331ac624577.json` and
      `2026-10-29-151556-711492-retrieval-813793dbc769.json` (7 calls, $0.007 each).
- [x] The retrieval runner records re-ranker scores and the chunks kept.
      Evidence: `test_runner_records_reranker_scores_and_kept_chunks_and_grades_the_fused_twenty`;
      both live artifacts carry `rerank_score` on the fused 20, the kept 5, `rerank_usage` and
      the re-ranker configuration.
- [x] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged.
      Evidence: backend 666 passed with two B-094/AUD-061 teardown errors in an unchanged test
      (pytest exit 1; the first full run, before review fixes, was clean at 665); Pyright 0
      errors; frontend 149 passed, TypeScript clean, lint with the existing AUD-009 warnings;
      [review note](../reviews/23-code-review-2026-10-29.md). Port eval not run: agent, tools
      and prompts unchanged.

## Comments

- 2026-10-29 — Author: park the T22 retrieval-design discussion here. Pause further custom
  decomposition, selection, evidence-checklist and recovery experiments. Build and assess the
  already-planned reranker first, then revisit the recorded gaps without assuming those
  experimental additions are needed or approved. This is a follow-up reminder, not an expansion
  of T23's implementation scope or authorization to start it now.
  Evidence: [retrieval experiment](../research/22-retrieval-experiment-results.md) and
  [selection replay/design proposal](../research/22-evidence-checklist-design.md).
  B-098/AUD-062 remains open: reranking cannot recover K04's MFA passage when it is absent from
  the candidate list. Preserve that failure and the original gold when evaluating T23.
- 2026-10-29 — Model: author confirmed Claude Opus 5.5 is set, matching the `Model:` line, and
  gave the build go (`/implement T23`).
- 2026-10-29 — Claude: documentation checked. OpenRouter `POST /api/v1/rerank` (official API
  reference): `model`, `query`, `documents` (strings), optional `top_n`; the reply's `results`
  carry `index` and `relevance_score`, and `usage` carries `cost`, `search_units`,
  `total_tokens`. LangChain 1.3.1 / langchain-core 1.4.0 (installed): `BaseDocumentCompressor`
  is in core; `ContextualCompressionRetriever` moved to the legacy `langchain-classic` package
  (LangChain v1 migration guide), which is not installed. Context Hub has no OpenRouter rerank
  or LangChain compressor entry.
- 2026-10-29 — Author's ruling: a search that returns zero passages gives `none` with reason
  `empty_result`, with the re-ranker on or off. Non-empty results stay `weak` /
  `not_calibrated` until T39. Recorded in the spec's retrieval section and decisions log.
- 2026-10-29 — Claude: builder choices within scope; (1) to (3) were put to the author before
  build, (4) follows the spec and is reported at closure. (1) The
  re-ranker subclasses LangChain's `BaseDocumentCompressor`, the slot the compression retriever
  calls, without adding `langchain-classic`. (2) It scores all 20 fused candidates and keeps the
  best 5; every candidate's score is saved for calibration and diagnosis, at the same cost as
  asking for 5. (3) A failed re-ranker call stops the search with a clear error; it never falls
  back silently to fused order, which would change the verdict's score source unseen. (4) The
  switch defaults to on, as T03 d5 states; T41's on-versus-off comparison decides what ships.
- 2026-10-29 — Claude: B-101 found and fixed during the build. The new factory could read the
  real key from `.env` in tests, because the test guard covered the embedding module only. No
  key was printed, sent or stored. The guard now covers the re-ranker; AUD-063 records the class.
- 2026-10-29 — Claude: the retrieval scorer now reads the fused 20 from `candidates`, because
  `chunks` holds only the kept 5 with the re-ranker on. Offline rescore of T22's final artifact
  gives identical results: `2026-10-29-150344-683834-retrieval-b6941a3d42d1.json`.
- 2026-10-29 — Claude: first live runs with the re-ranker on (before and after review fixes,
  identical outcomes). The gate results equal T22's: five of eight pass; K04 still misses the MFA
  register (B-098/AUD-062); K05/K06 still `weak` (B-099, T39). The re-ranker kept every found
  required passage: K01 rank 3, K02 rank 1, K04's runbook rank 1, K07 rank 1, K08 rank 2. K06,
  an absent topic, scores 0.646 at its top, above K04's 0.516; recorded in AUD-064 for T39.
- 2026-10-29 — Claude: admin manual commands tested. The on command produced the live runs
  above; the documented `LI_RERANKER=off` command gave the same outcomes with zero re-ranker
  requests and `"reranker": false`: `2026-10-29-151808-470796-retrieval-69e31e22b772.json`.
- 2026-10-29 — Claude: two-axis review triaged; see the [review note](../reviews/23-code-review-2026-10-29.md).
  AUD-063 and AUD-064 registered.

## Answer

Corpus search gains Cohere's re-ranker (`cohere/rerank-v3.5`) through OpenRouter's rerank
endpoint, behind `LI_RERANKER` (default on). It scores the 20 fused candidates in one request,
records every score, and keeps the best 5; its score drives the verdict, which stays `weak` /
`not_calibrated` until T39. Zero passages give `none` / `empty_result`, on or off, by the
author's ruling. The re-ranker subclasses LangChain's `BaseDocumentCompressor`. A failed call
stops the search with fixed text. The retrieval gate still reads the fused 20, so switching the
re-ranker does not change a pass; T41 judges it, with the kept-5 check AUD-064 names.
