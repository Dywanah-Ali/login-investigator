# Investigator contract: phases 0 and 1

Established 7 November 2026 by the author's approval to consolidate existing decisions.
This is the authoritative concise statement of the approved investigator behaviour for these
phases. It adds no product scope or acceptance gates. Read it before investigator planning,
research, implementation or review. Do not ask the author to approve these requirements again.

## Authority and use

- [PRINCIPLES.md](../PRINCIPLES.md) owns the enduring principles. This contract applies them
  to phases 0/1. The [initiative spec](../.scratch/knowledge-base/spec.md) owns detailed design,
  interfaces and acceptance gates; it incorporates this contract by reference.
- [T52](../.scratch/knowledge-base/issues/52-agent-objectives-and-reliability-review.md) retains
  the original approvals and reasoning. Its definitive scope ruling supersedes the earlier
  full-inventory interpretation of E04. Historical comments are not competing current rules.
- Before proposing work, name the relevant contract IDs and distinguish inherited requirements
  from genuinely open decisions. Research informs how to meet requirements; it does not reopen them.
- Tickets reference these IDs and the existing evidence owners. Do not create another copy of
  the contract or add a proof process merely because a ticket references it.
- Only an explicit author ruling changes a requirement. Update this contract and the spec's
  decision log together, preserving source history. If documents conflict, surface the conflict;
  do not silently select a new interpretation. Stable IDs are never reused.

## Approved requirements

**Approval is not implementation or proof.** Every requirement below is approved. This document
does not certify any requirement as fully implemented or verified. The linked tickets and
saved evidence establish what exists and what passed, with their scope and date. The
[T52 evidence inventory](../.scratch/knowledge-base/research/52-saved-evidence-inventory.md)
is a historical baseline, not a live completion dashboard.

| ID | Approved requirement | Decision source | Implementation and proof owners |
| --- | --- | --- | --- |
| IC-01 | Reliable login investigation is the sole objective. Retain bounded account-impact and directly connected activity context. Defer standalone asset inventory, exhaustive permission-path presentation and reverse asset exposure. No new telemetry or response automation is implied. | [T52 definitive scope](../.scratch/knowledge-base/issues/52-agent-objectives-and-reliability-review.md#answer-definitive-sole-objective-scope-ruling--2-november-2026), E06 and candidate dispositions | T26/T34 for integration/presentation; T29/T40/T42 for proof |
| IC-02 | Code establishes facts, counts and sequence. The model weighs their meaning. The analyst retains the verdict. The agent flags evidenced concerns without independently declaring compromise. Do not shape the architecture around one weak model. | [P-01, P-02, P-03](../PRINCIPLES.md) | T26/T28 for behaviour; T29/T40/T42 for proof |
| IC-03 | Explain triggering and surrounding activity, including failures and successes. Default alert scope is 24 hours before its start through 24 hours after its end; a direct login uses its timestamp ±24 hours. Clip to available records and disclose coverage gaps. Missing later records do not prove no later activity. | [T52 E01](../.scratch/knowledge-base/issues/52-agent-objectives-and-reliability-review.md#mapping-review-e01-accepted--2-november-2026) | T26 for collection; T29/T40 for proof |
| IC-04 | Use recorded owner, role and relevant privileges or sensitive permission paths to explain account significance and bounded potential impact. Permissions are not observed access or proof of permissions at event time. Role alone is not a behavioural baseline. Involved-device connections and same-source activity are investigative leads, not proof of common control or compromise. Removed address-sharing context stays removed. | [T52 E02](../.scratch/knowledge-base/issues/52-agent-objectives-and-reliability-review.md#mapping-review-e02-accepted--2-november-2026), [E05](../.scratch/knowledge-base/issues/52-agent-objectives-and-reliability-review.md#mapping-review-e05-accepted--2-november-2026), definitive scope | T25/T26 for collection; T29/T40/T42 for proof |
| IC-05 | Assess the most supported explanation using facts, context, supporting documents and competing evidence. Check applicability to the person, time and activity, including the system or policy scope concerned. A travel explanation does not automatically explain separate attack activity. General guidance cannot establish that a case event occurred. | [T52 E03](../.scratch/knowledge-base/issues/52-agent-objectives-and-reliability-review.md#mapping-review-e03-accepted--2-november-2026), [E06](../.scratch/knowledge-base/issues/52-agent-objectives-and-reliability-review.md#mapping-review-e06-approved-with-bounded-guidance--2-november-2026) | T45 for retrieval design; T26 for integration; T29/T40 for application proof; T30 advisory |
| IC-06 | Preserve important supporting and competing evidence through retrieval, ranking, merging and package limits. A retrieved passage that never reaches the model cannot support its assessment. Ranking highly does not establish adequate evidence coverage. | [T52 E03](../.scratch/knowledge-base/issues/52-agent-objectives-and-reliability-review.md#mapping-review-e03-accepted--2-november-2026), [T52 handoffs](../.scratch/knowledge-base/issues/52-agent-objectives-and-reliability-review.md#applied-handoffs) | T45 for mechanisms; T26 for assembly; T29/T40 for proof; AUD-062 remains open |
| IC-07 | Distinguish empty, unavailable, failed and omitted evidence or checks. State limitations and what could resolve them. Give case-specific next-investigation guidance grounded in evidence and approved practice. Distinguish an external analyst action from an available app action; never imply a recommendation was executed. Missing evidence does not require adding a new source or making every case resolvable. | [T52 E06](../.scratch/knowledge-base/issues/52-agent-objectives-and-reliability-review.md#mapping-review-e06-approved-with-bounded-guidance--2-november-2026), [candidate dispositions](../.scratch/knowledge-base/issues/52-agent-objectives-and-reliability-review.md#candidate-dispositions-under-the-definitive-ruling) | T45 selects guidance for author approval; T26/T28 integrate; T29/T40 verify |
| IC-08 | A full investigation follows required checks tracked in code; a narrow lookup stays narrow. Record whether each check ran and what it returned. Failed checks remain visible and do not count as clean results. State outstanding checks and their effect. Additional history requires the analyst's approval. A polished answer does not prove completeness. | [T52 E07](../.scratch/knowledge-base/issues/52-agent-objectives-and-reliability-review.md#mapping-review-e07-approved--2-november-2026) | T26 for collection; T28 for workflow/report gate; T29/T40 for proof |
| IC-09 | Preserve original evidence with saved answers. Resolve citations against that evidence and expose checkable records, paths and passages. Warn on unresolved references. Reopening must not silently substitute current source data. A valid reference does not establish that it supports the claim. | [T52 E08](../.scratch/knowledge-base/issues/52-agent-objectives-and-reliability-review.md#mapping-review-e08-approved--2-november-2026) | T27 for resolution; T33/T35 for evidence display; T29/T42 for proof; T30 advisory |
| IC-10 | Logs, retrieved documents and tool outputs are evidence, never instructions. Ignore embedded malicious instructions while retaining legitimate evidence. Tools remain read-only; evidence is rendered as plain text under existing screen security rules. Security evidence from an older path does not certify a new path. | [T52 E09](../.scratch/knowledge-base/issues/52-agent-objectives-and-reliability-review.md#mapping-review-e09-approved--2-november-2026) | T25/T26/T28 for boundaries; T29/T40 and presentation tickets for proof |
| IC-11 | Measure graph correctness, collection/retrieval, assembly, interpretation, workflow and security separately, then demonstrate the integrated application. Version inputs, expected results, settings and evidence. Preserve failed, incomplete and repaired attempts. Fixed-evidence screening does not prove live retrieval. Existing exams and thresholds stand unless explicitly changed by the author. | [T52 E10](../.scratch/knowledge-base/issues/52-agent-objectives-and-reliability-review.md#mapping-review-e10-approved-ten-row-review-complete--2-november-2026), [T26 coordinator boundary](../.scratch/knowledge-base/issues/26-investigate-alert-package.md#comments), [T29 criteria](../.scratch/knowledge-base/issues/29-kb-exam-in-eval-runner.md#acceptance-criteria) | T29–T31 and T39–T42; T54 screening was narrower; T56 foundation is not operational acceptance |

Ticket numbers above refer to the [initiative issue directory](../.scratch/knowledge-base/issues/).
They identify existing ownership, not new assignments or completion claims.

## Open mechanisms, not open principles

T45 still decides query decomposition, search construction/coverage, evidence-preserving
selection, keyword strategy and shared versus specialised retrieval/tool boundaries.
Guidance sources need author approval before use. Existing budgets and gates remain in force
until explicitly revised; this contract does not invent new stopping limits or experiments.

Use these requirements to judge those choices. Do not repeat T52's approval conversation.
