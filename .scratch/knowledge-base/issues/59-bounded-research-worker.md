# 59: Execute a bounded research assignment

Type: build
Proof type: AI judgement
Rigour: Tier 3
Status: ready-for-agent
Blocked by: 25, 57
Phase: 0

## What to build

A valid research assignment runs through an isolated worker and returns actual evidence,
relevance observations and honest gaps, with every assigned task and subject accounted for.
The worker selects permitted tools and bounded follow-ups; it never owns the overall verdict.
This slice is verifiable through the worker entry point before T60 connects it to public chat.

Author approved this ownership on 8 November 2026 through to-tickets. T45 is the parent design;
IC-02 and IC-05–11 are inherited. Planning approval is not build release.
Select the build model under the map's model guidance before implementation.

## Acceptance criteria

- [ ] Build the worker with create_agent behind the central construction seam, with isolated
      per-invocation state and tools from the central role/task registry. Consume T57/T25
      capabilities without rebuilding collection, ranking, catalogue or exact-reference reading.
      No persistent cross-call worker memory, extra supervisor or new agent service.
- [ ] Retain the dispatched assignment as authority. Bind every call to permitted task/subject,
      time and source scope. Research can refine an assigned search, not add subjects/intents,
      broaden history or investigate a newly discovered lead without a new authorised assignment.
- [ ] Enforce task-required work from trusted capability definitions independently of model tool
      choice. T26 alone composes full-investigation obligations. Code assembles receipts, original
      evidence and completion states; the model supplies selections and separate observations.
- [ ] Return exactly one outcome per assigned task and subject, distinguishing complete/partial/
      not-completed and found/no-match/failed/unavailable/omitted operations. Validate all
      evidence and observation references against actual retrieval results. Preserve valid partial
      evidence when another operation fails; never infer success from fluent prose.
- [ ] Preserve supporting and competing evidence, conditions and provenance through deduplication
      and delivery. Keep five per search with no second combined-five cap. Bound tool calls,
      exact reads, retries, model calls and context; disclose material omissions. Completion
      does not certify semantic sufficiency. No unbounded repair or reading of discarded hits.
- [ ] Implement the selected research teaching cases: in-assignment tool selection and inspection,
      failed/missing retrieval, supporting/competing evidence and source-linked gaps. Keep exam
      answers out of examples. Existing evaluations assess semantic value; fake models do not.
- [ ] Expose lifecycle outcomes needed by T60: cancellation stops child work, partial failures
      are retained, replay respects assignment/source identity and late results cannot silently
      attach to a different request. T60 owns application writer locks and public stream routing.
- [ ] Verify the worker end to end with controlled tools/models: invalid or missing task results,
      scope escape, stale references, multi-subject partial outcomes, malicious evidence, competing
      passage retention, budget stops and cancellation. Record candidate and delivered identities
      for T29's existing gates; tool execution is not proof of interpretation quality.
- [ ] Run focused checks, relevant types/lint, one scoped review and applicable existing agent
      evaluations. Reuse T45's framework research after checking version/behaviour applicability.
      No independent duplicate acceptance campaign or new gate. Document changed operator tasks.

## Comments

- 2026-11-08 — Approved handoff. Can proceed independently of T26 after T25/T57. T26 is the
  deterministic package owner; this worker supplements its baseline without erasing misses.
  T60 consumes both. No implementation or inference occurred during planning.
