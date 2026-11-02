# 52: Review phase 0 and 1 agent objectives and reliability evidence

Type: research, then grilling
Status: claimed
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

- 2026-11-02 — Author chose the balanced approach for production-model selection: start
  with a capable mid-priced candidate and measure investigation quality, response time and
  cost against the same quality requirements. Sol 6.1 and Claude Sonnet 5.5 remain candidates;
  neither model nor reasoning effort/provider route is selected. This does not authorise
  extra model-comparison runs or change the agreed 12-answer calibration count.

- 2026-11-02 — Author clarified that the architecture baseline should be a realistic
  production candidate. Sol's initial proposal is not an established choice; model authoring,
  tested app roles and advisory scoring are distinct. Production lifecycle lookup found
  [GPT-4.1 shutdown on 14 January 2027](https://developers.openai.com/api/docs/deprecations).
  Research precedent remains valid, but GPT-4.1 is not recommended as a new long-lived
  baseline. Updated both model notes; production priorities/model selection remain open.

- 2026-11-02 — Completed [industry model evidence](../research/52-model-selection-industry-evidence.md)
  and [calibration model proposal](../research/52-model-calibration-proposal.md). Primary
  sources disclose GPT-4.1 in DTDA's measured production window and AIDA's fixed-model
  comparison; no universal industry model baseline found. Current provider docs identify
  OpenAI, Claude and Gemini candidates. Proposed same model/settings for all A/B/C roles,
  initially GPT-6.1 Sol/high as an unmeasured starting candidate, with Astra or other vendors
  as alternatives. Model choice/effort/provider/budget await author ruling. OpenAI Sol's
  tool-calling Responses requirement and existing OpenRouter adapter compatibility must be
  checked before implementation; model listing is not account-access proof. No API inference,
  runtime model migration, dataset change or paid run performed.

- 2026-11-02 — Author requested research into model types/choices for each A/B/C design
  before defining the calibration setup, seeking a defensible industry baseline. Compare
  explicitly disclosed security-system model choices with current provider documentation;
  distinguish an industry precedent from consensus and architecture effects from model effects.
  App model selection is separate from author-confirmed Astra used in this development session.
  No runtime-model replacement or paid call is approved by this research request.

- 2026-11-02 — Author approved the 12-answer calibration stage first: O1-02, O1-06,
  O1-09 and O1-12-D, once under each A/B/C architecture. Review evidence sufficiency,
  scoring clarity, traces, review effort and observed cost/time before deciding on the
  proposed 189-answer stage. This is not a permanent architecture selection. Case-fixture
  preparation, isolated comparison harness, model/budget and scorer arrangements remain
  to be specified; no evaluation has run.

- 2026-11-02 — Author requested remaining scoring anchors and trial/adoption design.
  Drafted [case anchors](../research/52-objective1-scoring-anchors.md) for all remaining
  families/variants, preserving O1-06's accepted anchors, and a
  [comparison protocol](../research/52-objective1-comparison-protocol.md). Proposed calibration:
  four cases once per A/B/C (12 answers); proposed exploratory stage: 21 examples three times
  per architecture (189 answers). Counts are recommendations, not approved runs. No-answer
  runs remain in denominators; N/A criteria are set in advance; independent gold/scorer
  arrangements and confirmation gates remain open. Permanent adoption needs separate held-out
  and end-to-end proof, predeclared cost/latency limits and no compensation for critical errors.
  No existing gate, app code, dataset or paid execution changed.

- 2026-11-02 — Author accepted O1-06's applied score expectations and the distinction
  between incomplete answers and critically misleading answers. Recorded acceptance in
  the scoring note. Other case anchors, assessor calibration, trial counts and pass/adoption
  rules remain open. No implementation or evaluation-policy threshold change approved.

- 2026-11-02 — Author approved the proposed scoring approach: deterministic checks where
  possible, six semantic criteria with 0/1/2/not-applicable scores, case-specific predeclared
  critical errors that cannot be averaged away, blinded architecture labels and an advisory
  model judge. Overall passing/adoption thresholds and trial counts remain open. Recorded
  the approach and drafted O1-06 anchors/critical list in
  [answer scoring](../research/52-objective1-scoring.md). Applied anchors await review;
  no evaluator or gate was changed.

- 2026-11-02 — Author requested the remaining case specifications and coverage gaps.
  Drafted [full case specifications](../research/52-objective1-case-specifications.md):
  15 families, 21 diagnostic examples including the accepted O1-06, plus seven separate
  workflow checks. Includes distinct empty/unavailable/failed/truncated states, device
  handover timing, involved-device peers and missing role information. Read original helpdesk,
  handover and shared-device documents and checked source rows/organisation tables. Existing
  groups have explicit `kind=privileged`; the draft uses that evidence without inventing
  operation-level rights. Drafts preserve current dataset/gold and require review before
  execution. Direct-event window anchoring and detailed failure handling remain proposals.
  No fixtures, model calls or application changes; `git diff --check` passes.

- 2026-11-02 — Author accepted the O1-06 representative scenario and expected assessment
  after reviewing its summary. Its format can guide the remaining case specifications.
  This acceptance does not authorise data generation, evaluator implementation, paid runs,
  architecture adoption or new evaluation thresholds. Detailed fixture consistency and
  scoring/trial design still require completion before execution.

- 2026-11-02 — Author requested review of the proposed evaluation cases and one fully
  specified representative. Reviewed coverage and recorded device/role, empty-failed-truncated,
  interactive expansion and persistence gaps in the [case list](../research/52-objective1-evaluation-cases.md).
  Drafted [O1-06 partial explanation](../research/52-case-o1-06-partial-explanation.md) using
  the actual B1 travel notice, event identity and organisation records as provenance, plus
  clearly isolated proposed synthetic changes. It defines scope, evidence, reviewer-only
  gold, forbidden claims and A/B/C execution. No fixture generated, original truth changed,
  paid calls made or adoption threshold selected. Scenario/gold await author review.

- 2026-11-02 — Author approved the small-organisation evaluation target: retain the existing
  50-person organisation and target 30 days of login history, with varied investigations,
  realistic surrounding activity and competing documents. Larger populations/volumes are a
  separate later stress-test consideration. This is a target, not measured support. The
  alert-relative default window remains 24 hours before/after; longer history supports coverage
  checks and analyst-approved expansion, not an automatically established behavioural baseline.
  Exact row/document/scenario counts and implementation remain undecided. Carry this approved
  target into the eventual T52 spec reconciliation; no dataset generation is authorised yet.

- 2026-11-02 — Author approved comparison structure A (one investigator), B (plus evidence
  applicability specialist), C (plus review specialist), with common cases/evidence/model/
  boundaries, repeated trials and quality/cost measures; combined specialists considered only
  after individual contribution. No adoption thresholds or implementation approved. Author
  asked whether current data supports this comparison before proceeding.

- 2026-11-02 — Author approved retaining the review specialist as a separate comparison
  candidate, with permanent adoption dependent on demonstrated ability to catch consequential
  errors. Input: draft assessment and underlying case file, including limitations. Output:
  specific challenged claims, evidence references, suggested corrections and unresolved
  concerns. Checks include unsupported conclusions, missed counterevidence, false reassurance,
  overextended explanations and hidden coverage failures. It cannot change facts, expand
  scope or own the analyst's verdict. The front investigator inspects challenges, revises
  where warranted and preserves unresolved disagreements with an explanation. A clean review
  is not certification. Evaluate its contribution separately from the applicability specialist;
  no implementation or change to T30's advisory evaluation judge is approved.

- 2026-11-02 — Author approved comparing a separate evidence-applicability specialist
  against one investigator using the same evidence. Candidate specialist receives relevant
  case facts and retrieved passages, assesses applicability/partial explanations/conflicts,
  and returns cited findings and limitations. It cannot expand investigation scope. The
  analyst-facing investigator retains original evidence and integrates the assessment.
  Deterministic collection, matching and calculations stay in core code where supported.
  Permanent adoption depends on measured benefit versus cost and handoff losses. This
  approves the comparison candidate, not implementation or a changed evaluation gate.

- 2026-11-02 — Completed [agent architecture comparison](../research/52-objective1-agent-architecture.md)
  with six primary sources. Google supplies a direct analyst-facing coordinator analogue;
  AIDA distinguishes reasoning roles from a non-LLM executor. Neither proves superiority
  for our login objective. Proposed comparison: existing code-enforced collection plus one
  reasoning agent versus bounded applicability/challenge specialists over shared evidence.
  Agent count, framework and implementation remain undecided. Local inspection confirms
  `agent.py::build_agent` currently has one tool-using agent with policy/fencing middleware;
  T30's proposed faithfulness judge is advisory evaluation, not a live adjudicator. Any live
  specialist/reviewer requires an explicit design ruling separate from that judge policy.

- 2026-11-02 — Author proposed specialist agents coordinated by an analyst-facing
  orchestrator after reviewing the objective 1 workflow. Explicitly a candidate, not a
  confirmed design decision. Author requested research into similar use cases before a ruling.
  Compare with the existing code-enforced playbook/single-agent design, including independent
  reasoning needs, evidence contracts, contradictory results, boundaries, security, cost and
  evaluation. Existing no-sub-agent application design remains the baseline pending ruling.

- 2026-11-02 — Bounded primary-source research completed with the research skill's
  background researcher (Astra): [objective 1 investigation patterns](../research/52-objective1-investigation-patterns.md).
  Six sources cover Microsoft, Google and Elastic; Perplexity discovery and primary-page
  verification are recorded in the note. Recommendations concern explicit scope/coverage,
  traceable evidence packages, competing explanations, missing-evidence outcomes and
  decision-quality evaluation. Vendor claims are not runtime proof for this app; no source
  establishes our exact default window or missing role/privilege semantics. Next: map the
  agreed outcomes to reusable, adaptable and unsupported local capabilities. No additional
  scope, framework, integration or evaluation-policy change approved.

- 2026-11-02 — Initial local implementation inspection (source only, no runtime proof):
  `knowledge_base/neo4j_graph.py` supplies account/group lookup, group-to-asset paths and
  time-filtered shared-device peers; `_device_peers` includes all subject devices used in
  the window, not only triggering devices. `radius.py::_period` and T26 currently default
  omitted bounds to the available log period, requiring reconciliation with the approved
  alert-relative window. `schema.py` records people/department, group kind and asset sensitivity,
  but no explicit person job-role or grant privilege-level field. Role/privilege claims need
  verified evidence or an explicit unavailable status. T26 package and T28 playbook remain
  unbuilt. These are requirements/data-fit findings, not proven defects against the old spec.

- 2026-11-02 — Author approved objective 1 context-selection rules: always include recorded
  owner/role without treating role as a behavioural baseline; include recorded privileged
  access and access to explicitly sensitive assets with supporting permission relationships;
  restrict device peers to devices involved in the suspicious activity without implying
  compromise. Distinguish empty from unavailable data and disclose omitted results.
  Author requested bounded research into similar investigation agents, including Sentinel,
  for implementation insights before assessing needs against the existing foundation.

- 2026-11-02 — Author agreed a bounded account-impact summary within objective 1:
  account owner/role, relevant privileges and sensitive access, and relevant device
  relationships, each justified by its effect on the login assessment or analyst's next
  action. Potential access must remain distinct from observed resource access. A complete
  reachable-asset inventory, every permission path and reverse asset exposure are separate
  capabilities, not required by this summary. Explicit context-selection rules remain to
  be agreed and tested. Making objective 1 the sole phase 0/1 objective is under discussion;
  this boundary agreement alone does not approve deferral of existing phase 1 requirements.

- 2026-11-02 — Author agreed objective 1's assessment rule: state the most supported
  explanation, present competing evidence, and name what would help resolve uncertainty.
  The final verdict remains with the analyst. Author requested discussion of a question
  before proceeding to objective 2; no objective 2 decisions have been made.

- 2026-11-02 — Author chose analyst-controlled expansion beyond objective 1's default
  investigation window. The agent proposes additional history with a reason and asks before
  expanding. Automatic expansion is not approved. Actual coverage and unavailable records
  must remain explicit after an approved expansion. This resolves the preceding expansion
  decision; implementation and downstream reconciliation remain pending.

- 2026-11-02 — Author agreed objective 1's surrounding-activity boundary: include all login
  records behind the triggering event/pattern; the same account's surrounding failures,
  successes and source/device changes; and directly connected activity involving other
  accounts targeted by the same source or using the same device. Connections justify inquiry,
  not a compromise verdict. Default investigation window: 24 hours before the alert begins
  through 24 hours after it ends, limited to available records, with actual coverage stated.
  Older records enter for a specific comparison; claims of unusual behaviour require a
  separately defined baseline. Automatic window expansion, its triggers and limits remain
  undecided. These are agreed review requirements; implementation/data sufficiency has not
  been checked, and downstream spec/ticket reconciliation remains pending within T52.

- 2026-11-02 — Author confirmed Astra; runtime model context also identifies gpt-6-astra.
  Author clarified the motivation for T52: login evidence is one part of incident investigation.
  The current app provides useful speed and convenience, but the author wants to explore deeper
  investigative value using the existing graph, corpus and login data within manageable scope.
  Start with an explicit purpose, analyst objectives and boundaries, then derive tools and
  evaluation requirements. Do not let available tools define the purpose. Revisit the Sentinel
  research for one or two suitable capabilities, especially the inverse path/exposure question.
  Reuse of existing foundations is a hypothesis to verify, not proof that no new capability work
  is needed. This is review direction, not approval of a candidate, spec change or implementation.

- 2026-11-02 — Codex: author started T52 and requested a conversational walkthrough.
  Initial orientation read the ticket, principles, model guidance, spec purpose/overview and
  existing Sentinel tools research. No objective, scope or evaluation-policy decision yet.
  The ticket recommends Astra; the map says this recommendation is advisory. Exact active
  model has not been independently verified. Formal evidence review remains outstanding.

- 2026-11-01 — Author approved creating this as the next decision ticket, blocking T45 and T26.
  T25, T27 and T51 stay independent. The review should confirm the agent and its ecosystem's
  reliability and consider bounded additions for phases 0 and 1, while reusing the foundation
  where justified. Small implementation impact is a hypothesis to check, not an acceptance rule.

- 2026-11-01 — Author revised the work order: finish T51 first, then take this review.
  T51 provides the cleaned answer key and verified active pair as the review baseline.
  This changes priority only; T52 remains unblocked and still blocks T45 and T26.
