# Small retrieval experiment: frozen protocol

Frozen before live retrieval: 2026-10-29T11:34:57.326520+00:00.

Author authorized the proposed small experiment with “ok lets go”. This is an isolated diagnostic, not an application spec change. T23 and the original gold remain untouched.

## Comparison

- Twelve cases: seven existing document questions and five fresh diagnostic variations. The corpus and component evidence were already inspected. These are not an independent held-out dataset.
- Compare original question, handwritten focused queries, and focused queries plus original question. Use unchanged search, no filters, 20 candidates per query; combine lists with equal-weight RRF k=60, ties by chunk ID. Keep only 20 final passages.
- Identical query strings are executed once and reused across arms. Record actual physical embedding cost separately from the logical work of each arm. No claim of equal total search work, equal context tokens or production latency.
- No reranker or answer model. Coverage means the exact predeclared gold passages survived the final cap. No claim of answer safety or end-to-end success. Graph K03 is excluded; K04 measures its document needs only.
- Two absent-topic cases have no positive gold; their coverage is null, never vacuously passed. Record weak/not_calibrated as the existing behavior, without enabling refusal.
- False-premise and wrong-period cases require evidence that challenges the question. Retrieving that evidence does not prove an agent will interpret it correctly.
- Deliberately omit one need from N03 focused search. Retain the original full question in the broad arm.
- After initial results, inspect missing evidence and write a separate human recovery decision file. Allow at most one prewritten alternative query per case. Add it to focused+broad and recompute the same capped fusion. Gold may inform human review; this is not an automatic coverage detector. No post-result edits to queries, gold or merger.
- Record regressions as well as recoveries. Do not change a failed result by changing the experiment afterwards.

## Verification

Preflight validates all required passage IDs against locally rebuilt chunks, fixture integrity, stable fusion, deduplication and the 20-passage cap. Live calls reuse the project knowledge-base and embedding wrappers as the reader. No new third-party API behavior is introduced.

## Frozen inputs

- `22-retrieval-experiment-cases.json` SHA-256: `12256ea70d0332bbd4a0dd29218c9a01d3f88fff1663e1da523ac6ec73fac614`
- `22-retrieval-experiment.py` SHA-256: `2b76e8c3da44b16f4d74f45f22d73a0bbf5aa1777684ad686ce6ecf296683a1d`
