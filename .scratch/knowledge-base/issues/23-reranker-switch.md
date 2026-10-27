# 23: The re-ranker behind its switch

Type: build
Status: ready-for-agent
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

- [ ] Before any build work starts, the builder tells the author this ticket's `Model:` line and
      asks the author to set that model. The build starts only after the author confirms, and a
      dated line under Comments records the model used.
- [ ] Our own document compressor calls the rerank endpoint behind LangChain's compression-retriever
      seam and keeps the best 5 of 20.
- [ ] One setting switches it on and off; `env.example` and the contract's configuration section
      name it.
- [ ] With the switch on, the re-ranker's score drives the verdict and is recorded per candidate.
- [ ] With the switch off, the verdict falls back to the empty-result rule; a test proves it.
- [ ] Door 2 tests use a fake re-ranker; one real call is recorded.
- [ ] The retrieval runner records re-ranker scores and the chunks kept.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged.

## Comments
