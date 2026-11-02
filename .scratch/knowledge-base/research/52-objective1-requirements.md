# T52: Objective 1 working requirements

Date: 2 November 2026. Status: working synthesis, not a replacement spec.
Source: author discussion in T52; research in `52-objective1-investigation-patterns.md`.

## Agreed boundaries

- Explain the suspicious login/pattern, supporting and competing evidence, and remaining
  uncertainty. Code owns facts; the model assesses; the analyst owns the verdict.
- Include triggering records, surrounding account activity and directly connected activity:
  other accounts targeted by the same source and accounts using involved devices.
- Default period is 24 hours before the alert begins through 24 hours after it ends,
  limited to available records. State actual coverage. Expansion needs an analyst decision
  after the agent explains why more history would help.
- Include recorded owner/role, evidenced privileged or sensitive access and relevant device
  relationships. Role is not a baseline. Missing role/privilege evidence must not be invented.
- State the most supported explanation, competing evidence and evidence that would help
  resolve uncertainty. Connections and permissions do not prove compromise or actual access.
- Distinguish empty, unavailable, failed and omitted results.

Making this the sole phase 0/1 objective remains under discussion. Full blast-radius and
reverse-exposure scope dispositions have not been approved. Existing spec requirements
remain until explicitly reconciled under T52.

## Proposed case-file structure

These seven parts support the whole objective's evidence needs. They do not fully specify
the collection workflow, model assessment or evaluation. Detailed acceptance is still pending.

1. Scope: finding, rule, subjects, requested window and actual coverage.
2. Activity: triggering records and surrounding/directly connected sequence; code-built counts.
3. Account context: identity, evidenced role/context, sensitive access and permission paths;
   identify the permission snapshot rather than asserting event-time permissions.
4. Device connections: involved-device peers with supporting records and times.
5. Documents: supporting/clearing passages, source identifiers and applicability information.
6. Limits: unavailable evidence, failed checks, no matches and truncation distinguished.
7. References: stable source links and preservation of evidence used in saved investigations.

## Proposed workflow for discussion

1. Resolve the finding and derive its subjects and agreed default period. An invalid finding
   must produce an explicit inability to investigate rather than a guessed substitute.
2. Collect triggering and surrounding login records. Compute the sequence and counts in code.
3. Collect bounded account/access/device context and preserve its source and time limitations.
4. Search for evidence supporting and weakening possible explanations. Preserve source
   applicability information; a retrieved passage is not automatically applicable evidence.
5. Check collection status and evidence references. Failed or incomplete collection must remain
   visible in the package and constrain the assessment.
6. Assess the case using the agreed interpretation rule. If additional history could help,
   propose a specific expansion with a reason and wait for the analyst before collecting it.

The sequence expresses responsibilities, not a required serial execution schedule. Existing
fixed-playbook and parallel-call decisions remain the baseline. No new autonomous planner,
framework, tool implementation or evaluation threshold is approved here.

## Remaining decisions and proof

- Author ruling, 2 November: retain a review specialist as a separate comparison candidate.
  It checks the draft assessment against the underlying case file for unsupported claims,
  missed counterevidence, false reassurance, overextended explanations and hidden limitations.
  Return specific challenges with evidence references, proposed corrections and unresolved
  concerns. No authority to change facts, expand scope or decide the analyst's verdict.
  The front investigator handles challenges and exposes unresolved disagreements. No-finding
  reviews do not certify correctness. Measure this role separately from applicability work;
  implementation, permanent adoption and changes to the advisory evaluation judge are unapproved.

- Author ruling, 2 November: include a separate evidence-applicability specialist as a
  comparison candidate against one investigator with the same evidence. Inputs are relevant
  case facts and retrieved passages; outputs are cited applicability findings, partial
  explanations, contradictions and limitations. No scope-expansion authority. The front
  investigator retains original evidence and owns synthesis. Permanent adoption requires
  measured benefit; comparison implementation and evaluation thresholds are not yet approved.

- Architecture candidate raised by author: analyst-facing orchestrator with specialist
  agents. Research requested before a ruling. The current fixed-playbook/single-agent
  application remains the baseline; neither agent count nor specialist responsibilities
  have been agreed. Parallel execution of functions is distinct from independent reasoning.

- Reconcile the default window and involved-device selection with existing code/T26.
- Establish authoritative evidence for role, privilege and sensitivity selection.
- Define source-related activity selection without reintroducing removed address-sharing
  graph context or implying common control.
- Define package limits, evidence applicability and incomplete-investigation behaviour.
- Map assessment requirements to measurable evaluation cases and owner tickets.
- Carry approved requirements into the spec/decision log and affected tickets before build.

No runtime verification was performed for this note.

## Comparison and initial data readiness

Author-approved evaluation scale, 2 November: retain 50 people and target 30 days of login
history with realistic surrounding activity, varied investigation cases and competing documents.
Small diagnostic fixtures and larger realistic cases serve complementary purposes. Larger
organisation populations/volumes remain a later stress-test consideration. Row/document/case
counts have not been fixed. This target does not establish a behavioural baseline or change
the default investigation window/analyst-controlled expansion. No dataset build has been run
or approved by this target decision; spec and ticket reconciliation remain pending in T52.

Author approved comparison structure A (one investigator), B (plus applicability specialist),
C (plus reviewer), with shared cases/evidence/model/boundaries, repeated trials and final-answer
quality plus cost measures. No thresholds, implementation or combined-agent variant approved.

Inspection: `backend/evals/knowledge_base_questions.json` (eight questions), dataset `truth.json`,
README, travel approval and MFA register, corpus listing, existing injection test references,
and T40. This is a coverage assessment, not a completed evaluation or exhaustive data audit.

| Situation | Reusable material | Remaining preparation |
|---|---|---|
| Suspicious activity | S1/S3, S2 and S6; K04 combines S6 context and documents | Build case packages and explicit supported-assessment expectations |
| Legitimate explanation | B1 travel, B2 helpdesk reset, B3 laptop handover; K07/K08 cover B1/B3 | Include B2 and full event/context evidence |
| Wrong person/period | Travel approval has explicit person/date/device; K01 tests superseded policy | Craft paired applicability cases with independent expected outcomes |
| Partial explanation | Travel notice limits its own meaning; MFA register says approval does not prove actor identity | Explicit event-level cases and gold claims; potentially controlled variants |
| Unresolved/conflicting evidence | S4 has an explicitly unresolved truth entry | S4 covers uncertainty; genuine contradictory evidence needs a targeted fixture |
| Missing records/failed checks | Fixed capture boundary; absent-topic K05/K06 | Separate clipped coverage, empty result, omitted result and injected tool-failure fixtures |
| Potential vs observed access | S6 access paths and K04 | Explicit forbidden-access claims and expected uncertainty |
| Malicious evidence | S5 injection in log user_agent; existing Port security checks | Document-passage and specialist-handoff injection fixtures |

Recommendation, not a data-change ruling: reuse the synthetic world and add isolated,
versioned evaluation fixtures for controlled contrasts and failures. Keep answer keys out of
agent inputs. Review gold before trials; reserve unseen variants to limit tuning to examples.
Only extend the main generated world if later end-to-end tests require the new scenario to be
discoverable through actual retrieval/graph/log paths. Repeated trials on a few stories measure
stability, not broad generalisation. T40's larger question set is still planned.

Additional findings: explicit role evidence exists for at least Amelia in the MFA register
(emergency administrator), despite the absence of a structured role field. It cannot be
generalised to all accounts. Dataset README and K03 provenance retain old address-sharing
wording; these are documentation inconsistencies to reconcile under T52, not current graph
capabilities or evidence for the comparison. Known K04 retrieval gaps remain separate from
the proposed fixed-evidence reasoning comparison.

Further source inspection, 2 November: `org/groups.csv` explicitly marks IT Admins, Finance
Approvers and HR Data Owners as `kind=privileged`. This supports a recorded privileged-group
membership claim without a new field. It does not describe all operation-level permissions
or establish every person's job title. Access selection should use these existing facts before
proposing additional data. The expanded diagnostic specifications are in
`52-objective1-case-specifications.md` and remain draft pending author review.
