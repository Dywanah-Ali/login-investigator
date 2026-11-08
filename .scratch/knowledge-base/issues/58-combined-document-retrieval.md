# 58: Rank combined graph and corpus evidence

Type: build
Proof type: AI judgement
Rigour: Tier 3
Status: ready-for-agent
Blocked by: 57
Phase: 0

## What to build

A focused documentary search returns source-bound passages from the approved combined
graph/corpus pipeline, with inspectable evidence of admission, scoring, selection and omissions.
The result is verifiable through the shared knowledge-base core without a research agent.
T25 supplies the purpose-specific interfaces and catalogue; this ticket accepts a trusted
permitted source set and does not duplicate that catalogue.

Author approved this ownership on 8 November 2026 through to-tickets. T45 is the parent design;
IC-05–07 and IC-09–11 are inherited. Planning approval is not build release.
Select the build model under the map's model guidance before implementation.

## Acceptance criteria

- [ ] Keep the existing dense/keyword fusion inside the corpus route. Admit up to 20 corpus
      candidates and 20 additional unique permitted graph-linked passages from the verified
      paired build. Deduplicate by source/version identity and preserve every discovery basis.
      Corpus discovery does not require an entity mention. No model-authored database queries.
- [ ] For graph overflow, use exact semantic ordering within the eligible linked subset with
      stable identity ties. A stopped scan cannot claim best-of-all selection or exhaustive
      coverage. Record eligibility exclusions, duplicates, unresolved references and truncation.
- [ ] Rerank the combined pool using the same focused question and retain at most five parent
      passages per search. Do not invent graph fusion scores or reserve final places per route.
      Preserve source conditions and stage receipts for T25/T26/T59 and the existing eval owners.
- [ ] Establish provider-compatible query/pair/request size checks from documentation and installed
      adapter behaviour. Unknown processing coverage remains unknown. For verified oversized
      passages, bound temporary source-linked pieces, score all pieces with the same settings,
      use the maximum score per parent and deliver the original prepared parent when selected.
      Partial scoring/delivery is explicit. No stored identity changes, hidden tail loss or
      cross-call batching adoption. A tokenizer's presence does not prove compatibility.
- [ ] Define and test bounded scan/text/work policies, reranker-disabled ordering and failure
      outcomes before relying on them. Never silently drop graph contributions, fabricate scores
      or weaken refusal rules. Routine policies are builder decisions within T45; a material
      change to scope, evidence guarantees or gates returns to the author.
- [ ] Retain PostgreSQL keyword matching initially. Diagnose focused-query candidate/delivery
      failures before acceptance; T41's later BM25 comparison cannot defer phase-0 failures.
      Preserve weak/not-calibrated and empty-result semantics pending T39 calibration.
- [ ] Verify the entire core search with isolated paired stores and fake embedder/reranker,
      including duplicate admission, overflow, source mismatch, oversized text, missing scores,
      route failure and original-content delivery. Save actual route/stage identities for the
      unchanged K04 evidence obligations; no gold-informed query hints or cross-attempt pooling.
      Component success does not certify the analyst-question or package application paths.
- [ ] T29 owns the two path-specific acceptance views; T40 extends coverage; T41 owns switch
      comparisons. Keep original questions/gold and the legacy corpus-only diagnostic, including
      historical failures. No new paid campaign or AUD-062 closure follows from this ticket cut.
- [ ] Run focused tests, relevant types/lint, one scoped review and applicable existing retrieval
      evaluations. Use proportional checks; no new proof framework. Record documentation/version
      lookups and test any changed operator commands in the admin manual.

## Comments

- 2026-11-08 — Approved handoff. Reuse T45's saved overflow and orchestration research where
  applicable, checking relevant installed versions before coding. Ranking and provider safety
  policies remain implementation work, not research-proven runtime compatibility.
