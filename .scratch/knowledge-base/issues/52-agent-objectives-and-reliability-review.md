# 52: Review phase 0 and 1 agent objectives and reliability evidence

Type: research, then grilling
Status: ready-for-agent
Blocked by: none
Blocks: 45, 26
Phase: 0, with decisions covering phases 0 and 1
Model: strongest (Fable 5.1 or Astra)
Rigour: Tier 3

## Question

Do the agent, graph, document retrieval, evidence presentation and evaluations together prove
that the investigator can fulfil its agreed phase 0 and 1 objectives? Which bounded additions
would improve that purpose using the existing foundation, and what would each require?

Opened by the author's ruling on 1 November 2026 after the Sentinel research discussion.
Take this after completing T51, before T45 and T26 (revised order, 1 November 2026). Existing decisions remain the baseline;
the review confirms their coverage and identifies gaps without automatically reopening them.
This ticket produces decisions, not application code or certification of unfinished work.
T25, T27 and T51 remain independently available.

## What to decide

1. **Objectives and boundaries.** Confirm what the analyst should receive: an explanation of
   the login, potential impact, supporting and clearing evidence, and remaining uncertainty.
   Treat this wording as a proposal. Preserve PRINCIPLES.md: code owns facts, the model
   interprets, the analyst owns the final verdict. Separate observed activity from potential
   reach, and missing evidence from evidence that an event did not happen.
2. **Objective-to-evidence mapping.** For each objective record the analyst question, required
   data, core/tool behaviour, expected answer, evaluation evidence, current implementation
   status, gaps and owner ticket. Distinguish intended, implemented, tested and demonstrated.
   Inspect relevant saved runs and implementation; a resolved ticket alone is not proof.
3. **Reliability coverage.** Assess graph correctness, retrieval coverage, evidence surviving
   ranking and package limits, tool selection, playbook execution, claim support, uncertainty,
   saved/displayed evidence and security boundaries. Distinguish citation resolution and gold-ID
   coverage from whether a claim is actually supported. Review the advisory judge's limits
   without silently changing its agreed role or any acceptance threshold.
4. **Evaluation design.** Identify analyst-led questions, independently reviewed expected
   answers, competing explanations, unsupported premises, missing evidence and potential-reach
   overclaims that would expose weaknesses. Map existing coverage before adding cases. Separate
   evaluation-only work from changes to tools, retrieval, data, prompts or screens. Do not
   weaken gold answers or gates to accommodate current failures.
5. **Bounded Sentinel-inspired candidates.** Assess reverse asset-exposure questions, account
   investigation completeness and useful statements of unresolved evidence. Compare behavioural
   baselines and endpoint evidence as candidates that may require new data. Each candidate gets
   retain-existing / propose-addition / defer, with investigative value, prerequisites, evidence
   needed and an owner. Sentinel is inspiration, not a contract or an integration requirement.
6. **Handoffs and proof.** Carry approved objectives into T45's retrieval decisions and T26's
   package requirements, then T28, T29, T30 and T40 as applicable. Identify impacts on other
   tickets explicitly. Final runtime reliability remains to be demonstrated through the later
   evaluation and acceptance tickets, including T42.

## Inputs

- [Principles](../../../PRINCIPLES.md).
- [Current spec](../spec.md): purpose, agent/playbook, graph, eval and testing sections;
  latest decisions take precedence over older overview wording.
- T05 and T06 decisions; T21 to T24 implementation and evidence; T49/T50 accepted graph state.
- T25 to T30, T39 to T42 and [T45](45-compound-question-retrieval-design.md).
- [Sentinel tools research](../research/sentinel-tools-inspiration.md) and
  [Sentinel Memory research](../research/sentinel-memory-mcp.md).
- Improvement register: AUD-062, AUD-064, AUD-066 and AUD-076. Existing retrieval gaps remain open.

## Acceptance criteria

- [ ] Review the relevant implementation, saved evidence, spec and principles; record the model
      used and evidence inspected. Follow the map's model guidance.
- [ ] Produce an objective-to-evidence table covering all agreed phase 0 and 1 objectives,
      with gaps and owner tickets. Distinguish design decisions from measured results.
- [ ] Record each candidate's disposition and whether it needs only evaluation work or also
      changes to capabilities/data. Nothing is accepted merely because Sentinel offers it.
- [ ] The author rules on proposed objectives, scope changes and evaluation-policy changes;
      record decisions or explicit deferrals under Answer. Update the spec and decisions log
      only for approved changes. Existing decisions remain in force until then.
- [ ] Update T45 and T26 with approved requirements before releasing them. Carry applicable
      decisions into T28/T29/T30/T40 and other affected tickets with explicit owners.
- [ ] Record documentation inconsistencies separately, including the older overview's
      address-sharing and storage descriptions; reconcile only under the applicable rulings.
- [ ] Update AUD-076 and affected audit entries without closing unresolved execution gaps.
      Leave final proof assigned to the evaluation and acceptance tickets.
- [ ] Record the outcome in the map. No application build, new data source, Sentinel connection,
      changed evaluation gate or new screen is authorised by opening this ticket.

## Comments

- 2026-11-01 — Author approved creating this as the next decision ticket, blocking T45 and T26.
  T25, T27 and T51 stay independent. The review should confirm the agent and its ecosystem's
  reliability and consider bounded additions for phases 0 and 1, while reusing the foundation
  where justified. Small implementation impact is a hypothesis to check, not an acceptance rule.

- 2026-11-01 — Author revised the work order: finish T51 first, then take this review.
  T51 provides the cleaned answer key and verified active pair as the review baseline.
  This changes priority only; T52 remains unblocked and still blocks T45 and T26.
