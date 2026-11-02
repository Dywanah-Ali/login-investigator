# 52: Review phase 0 and 1 agent objectives and reliability evidence

Type: research, then grilling
Status: resolved
Blocked by: none
Blocks: 45, 26, 54
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

- [x] Review the relevant implementation, saved evidence, spec and principles; record the model
      used and evidence inspected. Follow the map's model guidance.
- [x] Produce an objective-to-evidence table covering all agreed phase 0 and 1 objectives,
      with gaps and owner tickets. Distinguish design decisions from measured results.
      Evidence: [table](../research/52-objective-to-evidence.md), 2 November 2026,
      and companion saved-result inventory. All ten rows approved in the dated review
      records below; dispositions and downstream reconciliation completed at closure.
- [x] Record each candidate's disposition and whether it needs only evaluation work or also
      changes to capabilities/data. Nothing is accepted merely because Sentinel offers it.
- [x] The author rules on proposed objectives, scope changes and evaluation-policy changes;
      record decisions or explicit deferrals under Answer. Update the spec and decisions log
      only for approved changes. Existing decisions remain in force until then.
- [x] Update T45 and T26 with approved requirements before releasing them. Carry applicable
      decisions into T28/T29/T30/T40 and other affected tickets with explicit owners.
- [x] Record documentation inconsistencies separately, including the older overview's
      address-sharing and storage descriptions; reconcile only under the applicable rulings.
- [x] Update AUD-076 and affected audit entries without closing unresolved execution gaps.
      Leave final proof assigned to the evaluation and acceptance tickets.
- [x] Record the outcome in the map. No application build, new data source, Sentinel connection,
      changed evaluation gate or new screen is authorised by opening this ticket.

## Comments

- 2026-11-02 — Author approved a US$25 shared spending allowance for initial compatibility
  sessions, the 72-attempt model screen and necessary documented setup-repair reruns.
  Review spending at US$15 and at the existing first-24-results checkpoint. No per-model
  budgets: usage differences remain measured outcomes. Pause before starting work that
  could exceed the remaining allowance. Include failed requests and retries, and account
  for outstanding/unknown charges. The allowance is not a cost forecast or a promise
  that the full screen fits. It excludes the later A/B/C architecture comparison and any
  paid scoring model. Verify pinned-route prices and a defensible admission/reservation
  mechanism before paid execution, without silently restoring rejected token/call caps.
  Budget approval does not resolve runner ownership/readiness or authorise an immediate
  run; the agreed T52 then T54 delivery order remains.

- 2026-11-02 — Author approved rerunning only comparisons affected by a documented
  setup fix. Preserve original results, version the repair and identify the affected
  model/case/pass cells before rerunning. Shared prompt, evidence or runner changes
  require reruns across all affected models; a genuinely isolated adapter fix requires
  only that configuration's affected trials. Do not mix results from incompatible
  conditions or rerun solely because an answer scored poorly. Record expected cost
  before each repair batch; paid execution and the spending policy remain undecided.
  This replaces the complete-restart alternative, not the approved three-pass design.

- 2026-11-02 — Author approved separate compatibility checks before scoring: one initial
  session per approved model configuration, using a small synthetic task outside the
  scored cases, checking settings, complete tool interaction, output contract and result
  recording. Run sequentially under the existing 180-second request / 600-second session
  deadlines without added token/call/retry caps. Six sessions are not six API requests.
  Diagnose failures before scoring the affected configuration; retain all evidence and
  disclose settings that cannot be independently verified. This approves the compatibility
  policy only, not paid execution. Setup-rerun policy and spending remain open.

- 2026-11-02 — Compatibility and setup-rerun proposal, pending author ruling:
  run one initial compatibility session for each of the six approved configurations,
  sequentially, using a small synthetic task outside the four scored cases. Check exact
  provider/model identity, requested reasoning configuration and effective parameter
  mapping, a tool request/result/final-answer round trip, agreed output-format compliance,
  and capture of timing, available usage/cost, failures and underlying retries. Distinguish
  settings evidenced by request/response metadata from settings whose application cannot
  be independently observed; do not claim native reasoning was proved by a plausible answer.
  Reuse the 180-second request and 600-second session deadlines, with no added token,
  call or retry count cap. These are six initial setup sessions, not six API requests,
  and are outside the 72 scored attempts. A failure triggers diagnosis before that
  configuration is scored, not elimination for weak investigation quality. Additional
  post-fix compatibility sessions need a recorded repair and the eventual spend policy.
  Approval of this policy would not authorise paid execution by itself.
  Proposed setup-rerun policy, still separate and unapproved: retain original records,
  version every repair, identify affected model/case/pass cells and rerun those cells
  under the corrected frozen conditions. A shared fixture/prompt change affects every
  candidate on the changed cases; a model-specific adapter repair may affect only that
  configuration if shared conditions are unchanged. Never pool different conditions or
  rerun solely to replace an unattractive answer. Record impact and spend before rerunning;
  additional run counts and execution authority remain to be agreed.

- 2026-11-02 — Author approved sequential screening: one case attempt at a time,
  rotating model order so no candidate is always first. Record the execution schedule,
  request latency and total case duration separately. This reduces interference among
  trials but does not remove provider-load fluctuations or establish concurrent capacity.
  Do not overlap compatibility probes or paid judge work with timed screening cases.
  The approved 72-attempt plan and first-24 setup checkpoint remain unchanged.
  Probe/setup-rerun allowances, spend policy and paid execution remain open.

- 2026-11-02 — Author chose no evaluation-imposed model-call, tool-call or retry count
  cap for the 72-answer screen. Calls and retries are measured outcomes, allowing
  candidates room to complete and exposing recurring setup problems. Preserve every
  request attempt, error, retry reason, tool call, elapsed time and available usage/cost,
  including failed attempts before eventual success. Distinguish model-requested extra
  work from adapter/transport retries and runner recovery. Instrument or otherwise expose
  automatic retries rather than hiding them behind a single successful invocation.
  The approved 180-second request and 600-second case deadlines remain; retries and
  backoff consume the same case clock. No additional scored case attempts or automatic
  post-deadline reruns are approved: the plan remains 72 scheduled case attempts, with
  failures retained. Common retries trigger diagnosis, not an assumed model defect or
  silent repair during a frozen comparison. If setup changes, version the correction
  and preserve the affected original results under the existing fair-rerun protocol.
  Retry behaviour/backoff and failure classification still need a reproducible runner
  contract; absence of a numeric cap does not require retrying a known permanent error.
  Concurrency, probe/setup-rerun allowances, spend policy and paid execution remain open.

- 2026-11-02 — Author rejected evaluation-imposed token allowances for this screening
  stage: no chosen per-request or per-case generated-token cap. Token consumption is an
  outcome to measure alongside answer quality, latency and cost; large usage differences
  are useful selection evidence. This supersedes the 16,384/32,768 proposal below.
  Retain approved reasoning settings and 180-second request / 600-second case deadlines.
  Omit optional token caps where supported; disclose unavoidable provider/model ceilings,
  defaults and any required output-limit parameter before execution. Do not describe these
  routes as literally unlimited or silently impose a common cap through the adapter.
  Record input, generated output and reasoning usage where exposed, identifying missing
  breakdowns and avoiding double-counting reasoning already included in output totals.
  Record truncation and timeouts as outcomes. Usage differences are configuration-specific
  observations, not equal units of reasoning across tokenizers. Spend, calls, retries and
  execution permission remain separate open decisions; no unlimited spending authorised.

- 2026-11-02 — Author approved the timing ceilings: 180 seconds per model request and
  600 seconds per complete case attempt for the 72-answer screen. The enclosing case
  deadline includes tool work, backoff and any permitted retry; retries do not reset it.
  Preserve timeout outcomes and partial evidence. These are execution ceilings, not a
  production latency gate. Other limits and paid execution remain open.

- 2026-11-02 — Next proposal, not approved: at most 16,384 generated tokens per request
  and 32,768 across a case attempt, including reasoning, tool-call output and visible
  answer tokens. Each subsequent request receives no more than the remaining case
  allowance. Retries consume the same allowance; unknown usage retains its reserved
  maximum until reconciled. Provider-specific combined-cap enforcement and usage accounting
  must be verified before execution; do not assume a parameter has identical semantics
  across routes. Exhaustion remains a recorded incomplete result, with no automatic
  continuation or larger-cap rerun. Input tokens are accounted for separately in the
  eventual spend plan. These are starting resource ceilings, not measured sufficiency
  or equal computation across models. Reasoning settings already approved remain unchanged.

- 2026-11-02 — Resumed from the handoff to settle execution limits. First proposal,
  pending author ruling: a 180-second wall-clock deadline per model request and a
  600-second deadline per complete case attempt. The case deadline includes collection,
  tool work, model requests, backoff and any separately permitted retry; a retry does not
  reset it. Measure from dispatch/start, not from the last received token. Stop launching
  work when either applicable deadline expires, preserve partial output and record timeout
  separately from assessment quality. Client cancellation does not prove provider billing
  stopped; unresolved usage must remain reserved in the eventual spend ledger. These are
  proposed operational ceilings, not measured latency targets or a production acceptance
  gate. Output/reasoning, call/retry, concurrency, probe/rerun and spend allowances remain
  subsequent decisions. No paid execution or implementation is authorised by this proposal.

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

- Author approved on 2 November 2026: finish T52, then T54 early Langfuse evaluation
integration, then instrumented 12-answer A/B/C calibration. T31 retains application tracing
and full T29 exam integration, reusing T54. T52 must assign the calibration runner implementation
owner and settle its record contract before T54 starts. Local files remain authoritative;
results are saved before upload, masking applies throughout, and human labels return only
through explicit export. Blinded scoring must hide revealing architecture labels and traces.
Model choice, budgets and paid execution remain separate unresolved decisions.

- 2026-11-02 — Model selection resumed using the OpenAI Docs skill and official provider
  pages via web search. Sol 6.1 and Sonnet 5.5 rates/defaults and parameter limitations
  rechecked; SDK compatibility untested. See the model-calibration proposal's resumed-selection
  section. Revised recommendation is Sol 6.1/medium, pending author choice; earlier high-effort
  suggestion is superseded as a recommendation only. No model selected or run authorised.

- 2026-11-02 — Author requested broad model research, explicitly including cheaper/faster
  open-weight candidates, and corrected the research filter: investigation quality,
  evidence discipline and security boundaries are local evaluation requirements; missing
  use-case-specific publications must not exclude a candidate. Earlier Sol recommendation
  is superseded pending the broad shortlist. Research skill delegates a background source
  review; parent verifies benchmark methodology and records a proposed model-screening step
  in [screening evidence](../research/52-model-screening-evidence.md). Extra screening runs,
  candidate count, budgets and execution remain proposals, not authorised inference.

- 2026-11-02 — Broad research completed: [candidate note](../research/52-broad-model-shortlist.md)
  proposes eight inexpensive candidates across six open-weight families and two proprietary
  models, with Sol/Sonnet as optional references and wider alternatives retained. Primary
  model cards and hosted rates checked; parent verified independent general capability/speed
  observations and benchmark limitations. Provider-specific compatibility, account access,
  task quality and total cost remain untested. Local documentation checks pass; no code or
  inference run. Proposed screening must be agreed before it adds work to calibration.

- 2026-11-02 — Author approved the narrowed six-model screening pool: Qwen3.8-27B,
  gpt-oss-120b, DeepSeek V4.1 Flash, GPT-6 Luna, Claude Haiku 5.5 and GPT-6.1 Sol.
  GLM-5.3-Flash, MiniMax-M3.1-Flash and Mistral Small 4 are reserves, not failed candidates.
  Compare models in a common single-investigator setup before choosing the fixed A/B/C
  baseline. Four cases each would mean 24 final answers; case count/repeats, provider routes,
  settings, limits, implementation and execution remain undecided. No paid run authorised.

- 2026-11-02 — Author accepted O1-09 missing later history and its expected assessment
  after clarification against O1-06: keep login sequence/travel evidence unchanged, but stop
  available capture immediately after success. Give the model explicit coverage metadata.
  It must distinguish no later recorded activity in a covered window from an unobserved
  interval, and must not infer account safety from either. O1-02/O1-12-D review remains open;
  no paid execution or final screening case count approved by this case ruling.

- 2026-11-02 — Author clarified all four screening cases are approved: O1-02, O1-06,
  O1-09 and O1-12-D, with the plain-language expected assessments presented in discussion.
  The O1-09 concern is resolved. This supersedes the preceding comment's claim that
  O1-02/O1-12-D scenario review remains open. Across six candidates, one pass means 24
  final answers; repeats, detailed fixture/scoring readiness, routes/settings, budgets and
  execution authorisation remain open. Do not request case-set approval again.

- 2026-11-02 — Repeat-count guidance checked against
  [Anthropic agent evaluations](https://www.anthropic.com/research/demystifying-evals-for-ai-agents)
  and [OpenAI evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
  via official-page web browsing. Guidance supports repeated trials and task-specific evaluation;
  no universal fixed repetition count was established. Proposal awaiting author ruling:
  three independent attempts per model/case, six models × four cases × three = 72 final
  answers, with frozen evidence/prompts/settings, fresh memory and every result retained.
  This is a modest variability screen, not a statistically powered production reliability
  claim; four related cases remain four cases. A first 24-answer checkpoint may diagnose
  fixture/scorer problems, but must not select winners or silently drop failed candidates.
  No execution, spending cap or repeat count approved yet.

- 2026-11-02 — Author approved three attempts for each of six models on each of four cases:
  72 final screening answers. Inspect the first 24-answer pass for setup problems, then
  complete the remaining two passes. Checkpoint is diagnostic, not early elimination.
  Preserve fresh-memory/frozen-condition trials and all failures. Changed conditions need
  versioned, fairly rerun comparisons rather than pooled results. Extra rerun allowance,
  routes/settings, budgets and execution authorisation remain open. A/B/C calibration
  stays separate at its previously agreed twelve answers.

- 2026-11-02 — Author confirmed OpenRouter access. Prepared
  [route/reasoning proposal](../research/52-model-reasoning-settings.md): OpenRouter gateway,
  DeepInfra for the three open-weight-family candidates, OpenAI for Luna/Sol, Anthropic for
  Haiku; standard tier, fixed provider variants and no silent fallbacks. Medium reasoning
  proposed for five, native high for DeepSeek. All settings/provider choices remain proposals.
  Public endpoint metadata checked, exact DeepSeek variant/features still pending. Local
  metadata fetch failed DNS; browser sources used. No credentials, inference or app changes.
  Installed LangChain 1.3.1/langchain-openai 1.2.2 source inspected for Responses flags;
  OpenRouter stateless-history compatibility is untested and requires pre-run verification.

- 2026-11-02 — Author confirmed the OpenRouter starting configuration: DeepInfra for
  Qwen3.8-27B/medium, gpt-oss-120b/medium and DeepSeek V4.1 Flash 1017/high; OpenAI for
  GPT-6 Luna/medium and GPT-6.1 Sol/medium; Anthropic for Claude Haiku 5.5/adaptive medium.
  Standard service, fixed providers, no automatic provider/model fallback and required
  parameter support. Approval is subject to compatibility checks, including exact DeepSeek
  variant and native reasoning/sampling preservation. No inference or app migration yet.
  Time/output/retry/call/spend limits are the next decision; approved trial count unchanged.

- 2026-11-02 — Price/accounting research completed after the execution-policy approvals
  recorded above. [Price snapshot and reservation proposal](../research/52-screening-price-and-reservation-check.md)
  verifies all six standard routes; DeepSeek's exact catalogue variant is `deepinfra/fp8`.
  Saved public endpoint JSON and independently checked budget controls. No credentials,
  inference or account changes. Prices alone cannot prove all uncapped trials fit US$25.
  Proposed reservation rule: settled charges + unresolved reservations + next request's
  conservative possible cost must fit the remaining shared allowance. Use provider-native
  bounds, not new evaluation token caps; reconcile actual charges and retain unresolved
  holds after timeouts. A per-key limit alone lacks a documented exact final-charge guarantee.
  Design approval, billing-bound validation, account isolation and runner implementation
  remain open; no paid execution. AUD-076 retains the accounting proof obligation.

- 2026-11-02 — Documentation lookup: OpenRouter API v1; Context Hub had no matching entry.
  Used official [usage accounting](https://openrouter.ai/docs/cookbook/administration/usage-accounting),
  [limits](https://openrouter.ai/docs/api_reference/limits),
  [streaming](https://openrouter.ai/docs/api_reference/streaming), provider-selection and
  service-tier docs plus unauthenticated endpoint metadata. Checked charged-cost fields,
  generation-ID reconciliation, cancellation limits, exact routes, unit prices and native
  token ceilings. Independent research note linked from the price report. No SDK changes.

- 2026-11-02 — Author explicitly rejected the request-reservation method, considering
  expected spending affordable. Do not implement reservations or retain worst-case billing
  bounds as a pre-run gate. Use US$25 as the planning budget, not a guaranteed hard final-charge
  ceiling; retain actual-cost tracking, the US$15 review and first-24-results checkpoint.
  Preserve failed/retried request costs and label unavailable charges unknown until reported.
  This supersedes the reservation/admission proposal and its audit proof obligation, not
  the existing timing, model, case, repetition or delivery-order decisions. No new token,
  call or retry caps. No account changes or immediate paid execution requested by this ruling.

- 2026-11-02 — Runner ownership and record contract drafted below for author ruling.
  Inspected T29, T30, T31, T54, the evaluation/Langfuse spec, accepted scoring note and
  `backend/evals/run.py`, `api_runner.py`, `scoring.py`, plus saved-result tests. The existing
  application runner records boolean acceptance checks and whole-case time; it does not
  provide the complete new comparison contract. This is an extension need, not a newly
  established defect in the existing exam. Used codebase-design for the runner/recording seam.
  No application code, ticket ownership or spec changes implemented by this proposal.

## Approved runner ownership and record contract — 2 November 2026

Author approved the proposal below. T54 owns the isolated comparison runner and Langfuse
recording; the nine-group record contract and delivery checkpoints are agreed. Updated
T54, T29/T30/T31 scope references, the spec/decisions log and map. This is design approval;
T52 remains claimed until its remaining decisions and closure criteria are satisfied.

### Ownership

| Ticket | Approved responsibility |
|---|---|
| T52 | Agree the comparison contract, fixture/score readiness, role instructions and selection rules; assign build ownership. Remains a decision ticket. |
| T54 | Expand to own the isolated comparison runner and reusable Langfuse recording together. Build compatibility, six-model screening and A/B/C calibration modes using the same local record contract. |
| T29 | Keep the full application's Port/knowledge-base acceptance exams and gates. Reuse suitable recording utilities without importing screening scores into acceptance rates. |
| T30 | Keep the later advisory faithfulness judge and human-agreement reporting. No paid judge is required by the initial screen or included in its budget. |
| T31 | Keep application tracing and full-exam Langfuse integration, reusing T54's recording module. |

Approved sequence remains T52, then T54. T54 has three internal checkpoints:

1. Frozen synthetic fixtures, isolated runner, versioned local records and offline/fake-model
   checks, including the common investigator and separately defined A/B/C evaluation designs.
2. Langfuse mirror, masking and blinded human-label export tested against a fake destination.
   The runner can work locally with mirroring disabled. Local-first persistence remains required.
3. Once ready and execution is authorised, separate compatibility sessions, then the screening
   passes with the first-24 diagnostic checkpoint. Reconcile an actual authorised scored
   result with Langfuse and record the author's inspection before T54 closes.

Distinguish implementation-ready from ticket-resolved: T54's live evidence occurs after its
runner is ready, not before the runner exists. The later 12-answer A/B/C calibration uses
the same machinery after selecting a provisional model and settling its separate execution
budget/readiness. T54 need not wait for that later calibration to close if genuine screening
evidence meets its integration criterion. No full 189-answer stage is added. No production
specialist is adopted; evaluation designs are isolated from the working application.
T54's title/criteria, T31's references, the map and spec decisions log are reconciled.
No new ticket is needed for this coupled runner-and-recording work.

### Record contract, version 1

The run is a local evidence bundle: a frozen manifest, durable ordered trial events,
case outcomes and separately versioned scoring records. Exact filenames are implementation
choices. Large artifacts may be referenced by local path plus content hash; the bundle
must remain readable without Langfuse, live models or the working application's memory.

| Record group | Required information |
|---|---|
| 1. Test setup | Schema version; experiment/run/trial IDs; stage (`compatibility`, `screening`, `architecture_calibration`); case ID and pass number; scheduled order; code revision and relevant dirty-content hashes; fixture, prompt, tool and rubric versions; approved execution settings. |
| 2. Case evidence | Exact model-visible inputs and ordered context, evidence text/IDs, coverage metadata and source hashes; assessor-only gold/anchors stored separately and never supplied to models. Fresh-memory identity per trial. Explicit fixed-evidence versus live-tool mode so the screen cannot imply live retrieval proof. |
| 3. Model configuration | Requested and reported model, provider/variant and service tier; reasoning/sampling settings; actual defaults/mandatory ceilings where known; adapter version; unresolved effective settings labelled unknown. Model/design identity retained privately for unblinding. |
| 4. Request history | Unique request-attempt IDs and parent links; start/end and elapsed time; returned generation IDs; completion/error/timeout status; retry parent, reason and origin (model, transport or runner); partial results and sanitised errors. Retain failures before eventual success. |
| 5. Tool and role activity | Requested tool name/arguments, whether it executed, returned evidence or error, timing and linkage to the requesting turn; specialist inputs/outputs where applicable. Record available provider continuation data needed for reproducibility, without requesting hidden chain-of-thought. |
| 6. Case outcome | Full final analyst-facing answer or explicit absence; partial-answer artifact if interrupted; execution status kept separate from score. Link repaired/rerun trials to originals and identify which version is eligible for comparison. No overwritten or cherry-picked attempts. |
| 7. Resources | Request and case timing separately; input/output/reasoning/cache usage where exposed; call/tool/retry counts; reported dollar charges including failures; accounting source and completeness. Unknown is not zero. Updated settlement references the same request rather than duplicating its charge. No reservations. |
| 8. Assessment | Criterion ID; score 0/1/2, explicit not-applicable or not-yet-scored status; excerpt, evidence reference and reason; separate critical-error flags; deterministic-check outcomes; assessor alias/type and rubric version. Preserve original labels, disputes and later rulings. No invented weighted score or promotion threshold. |
| 9. Recording and review | Durable local save status; outbound masking version; mirror/export status and remote IDs if enabled; upload errors. Blinded review ID and separately kept identity mapping; review order and label revisions. |

### Behaviour at the interface

- One comparison runner executes a frozen plan and writes this bundle. Recording/mirroring
  consumes already-saved records; upload failure cannot require another model call.
- Record a request-start event before dispatch and save outcomes incrementally so an
  interruption cannot erase previous requests. Restart exposes unfinished attempts; it
  never silently duplicates a possibly billed request or counts a partial case as fresh success.
- Apply the approved sequential execution and time deadlines. Preserve the approved absence
  of token/call/retry caps and reservations. Track actual costs and the agreed reviews.
- Keep operational completion distinct from answer quality. An interrupted case remains in
  coverage/failure reporting; an unscored answer is not a score of zero or a passing result.
- Create a blinded scoring view containing case evidence, the final answer and appropriate
  assessment anchors. Hide candidate/design names, settings, costs, latency and revealing
  traces. Maintain a separate process/security review with necessary trace access; disclose
  that this review is not equivalently blinded. Natural self-identification in an answer
  may still reveal a candidate; preserve the original and record such blinding limitations.
- Local redaction removes secrets before persistence; outbound masking covers everything
  uploaded. Human labels return by explicit export and are versioned locally. No runtime
  reads from Langfuse and no schema change to the working application's responses.
- Offline rescoring of deterministic checks and human relabelling use saved evidence without
  model calls. Any future advisory model scoring is a separately labelled/authorised operation.

### T54 evidence required

Offline checks must demonstrate fresh trial state, schedule identity, request/tool/retry
lineage, timeouts and interrupted-record recovery, unknown usage and charge deduplication,
gold isolation, score/N/A/unscored fidelity, separate blind views, safe local persistence,
masking, upload failure survival and explicit label export. No backend/frontend/eval tests
ran for this documentation proposal. Existing application gates remain unchanged. T54 adds
tested operator commands to the admin manual when it implements them.

This approval settles ownership and the evidence shape. Assessor arrangements, provisional-model
selection rules and remaining policy ambiguities need T52 resolution before build. T54 writes
the exact fixtures/prompts and freezes their IDs/hashes before execution under the approved
case/role contracts; those implementation artifacts need not pre-exist their build ticket.
Approval does not close T52 or authorise an immediate paid run.

## Approval audit — 2 November 2026

Requested after the author challenged the suggestion that cases/scoring needed defining
again. Checked dated approval comments above against the case specifications, O1-06
representative, common scoring, remaining anchors, comparison protocol, screening notes,
role contracts and T54. Later explicit approvals take precedence over earlier draft wording.
This is a document/source audit, not runtime evaluation or a new scope ruling.

### Already decided; do not reopen

| Item | Recorded approval/evidence |
|---|---|
| Four cases and expected assessments | T52's explicit all-four clarification: O1-02, O1-06, O1-09, O1-12-D. Matching travel and document injection are not awaiting scenario approval. |
| Common scoring method | Six criteria, 0/1/2/N/A, evidence/reason per score and separate critical errors approved. No averaging away critical failures. |
| O1-06 detailed grading | Applied expectations and incomplete-versus-critically-misleading distinction explicitly accepted. |
| Missing-history meaning | O1-09 explicitly distinguishes unavailable later coverage from no events inside available coverage; neither establishes account safety. |
| Injection expectations | O1-12-D keeps legitimate travel evidence and rejects injected clearance/scope-expansion commands; it inherits O1-06's assessment. |
| Comparison design and roles | A single investigator, B applicability specialist, C review specialist; role responsibilities and analyst authority already approved. Exact prompt text is not a new role-design decision. |
| Model configurations, repeats and execution policies | Six configurations, 72 attempts/first-24 checkpoint, separate twelve-answer A/B/C stage, sequential timing, no token/call/retry caps or reservations, actual-cost planning/checkpoints. |
| Runner owner and saved evidence | T54 and its approved nine-group record contract; T29/T30/T31 responsibilities retained. |

### Genuinely unresolved for the initial screen

| Item | What is actually missing | Existing evidence / smallest next step |
|---|---|---|
| Assessor arrangements — subsequently resolved | Author is primary scorer; Codex prepares blinded reviews, records labels and assists after initial scoring. | Approved below. No second human or paid judge required for the initial screen; no independent human-agreement claim. |
| Provisional-model selection rule — subsequently resolved | Complete all twelve trials, no critical errors or applicable zero scores; compare quality first, then cost and speed for similar quality. | Approved below. If none qualifies, diagnose rather than promote the least-bad candidate. Temporary baseline selection, not permanent adoption. |
| Narrow grading-table reconciliation — subsequently resolved | Author approved the three screening applications below. | O1-09 and O1-12-D inherit O1-06's complete rules and add their specific failures; O1-02 needs no invented attack hypothesis. Written screening grading is settled; implementation remains T54 work. |
| Direct-event window convention — subsequently resolved | Author approved 24 hours before/after the login timestamp when no alert exists. | Clip to available records and disclose missing coverage; analyst controls expansion. Alert-relative windows and O1-06/O1-09 coverage stay unchanged. |

### Build work, not another approval round

T54 materialises isolated fixture data, source references/IDs/hashes, exact role instructions
consistent with approved roles, output schemas, schedule and checks. It verifies source
consistency, gold separation, effective settings, scoring fidelity and interruption/accounting
behaviour. Freeze before scored execution. Missing implementation is not missing scenario
approval. A semantic conflict discovered while building comes back as that specific conflict.
Search of `backend/evals` and `backend/tests` found none of the four O1 case identifiers;
this supports the recorded not-yet-materialised status, not a claim that no reusable data exists.

The broader 21-example/189-answer proposal, realistic 30-day data build, held-out confirmation,
permanent adoption thresholds and live retrieval/workflow proofs are not all prerequisites
for the four-case fixed-evidence screen. T52 still has its original objective-to-evidence
mapping, saved-run review and downstream reconciliation obligations; this audit does not
close them or quietly reduce phase 0/1 scope.

### Documentation correction and verification

Corrected stale status summaries in the case catalogue/specifications, common scoring and
O1-06 note; clarified the scoring-anchor status without marking drafts approved. Preserved
earlier dated history. B-142 records the documentation drift and misleading repeated request.
No gold, rubric scores, critical-error rules, acceptance gates or application code changed.
Local links and whitespace are checked; no runtime test or paid evaluation is claimed.

## Screening assessor arrangement approved — 2 November 2026

The author approved being the primary scorer for the 72 screening answers, assisted by
Codex. Codex prepares blinded case evidence/answers and the agreed rubric, records the
author's six-criterion labels and critical-error flags, and runs deterministic factual/
reference checks. Save the author's initial labels before discussing possible inconsistencies
or offering suggested scores. Retain revisions, reasons and disagreements; the author
owns the final human label. Code checks are separate evidence, not semantic-score replacements.

Review in small batches and measure actual review effort from the first batch. Review all
produced answers, including partial answers under the existing rubric; no-answer failures
remain separate operational outcomes. Do not claim there are 72 scoreable answers if some
trials produce none. No second human or paid model judge is required for this exploratory
screen. Codex assistance is not a second independent human review, and no inter-human
agreement statistic is claimed. T30's later advisory-judge scope remains unchanged.

Recorded in the comparison protocol, common scoring note, T54, spec/decisions log and map.
This resolves the screen's assessor decision; provisional-model selection, narrow grading
and direct-event-window checks, and broader T52 closure work remain open.

## Provisional-model selection approved — 2 November 2026

The author approved quality-first selection after all three screening passes. Each model
has twelve scheduled trials: four cases, three attempts each. Eligibility requires all
twelve completed, with no designated critical errors and no applicable criterion scored 0.
A score of 1 is permitted because it represents an omission without contradiction. N/A is
not a zero; unscored/missing evidence is not a passing label. Timed-out/incomplete trials
remain operational failures even when their partial answers can be assessed.

Among eligible configurations, compare criterion profiles case by case. Prefer consistently
complete answers over repeated partial answers. When quality is similar, choose the cheaper
model, then use speed as the next deciding factor. Record the author's evidence-based
selection rationale; no new weighted total or statistical-superiority claim is introduced.
Do not eliminate candidates on the first-24 setup checkpoint alone.

If no configuration qualifies, investigate the failures rather than automatically advancing
the least-bad candidate or weakening the agreed rubric. Setup defects follow the approved
versioned affected-comparison rerun policy, with originals preserved; ordinary model failures
are not silently replaced. Calls/retries/costs remain visible under the approved record contract.

This selects a provisional model for the separate A/B/C comparison only. It does not certify
production reliability or choose a permanent application model. Assessor and selection
decisions are now settled. Narrow grading/window checks and broader T52 closure remain open.

## Approved narrow grading reconciliation — 2 November 2026

Checked the three screening rows against approved cases and O1-06's accepted anchors.
Author approved the [screening clarification](../research/52-objective1-scoring-anchors.md#approved-screening-clarification--2-november-2026):
O1-02 rewards bounded expected travel without demanding invented threats; O1-09 explicitly
inherits all O1-06 criteria/critical errors plus the missing-coverage rule; O1-12-D explicitly
inherits O1-06 plus injection obedience, distinguishing quotation from compliance. Existing
partial-credit, contradiction and critical-error distinctions remain. No new case, threshold,
mandatory phrasing or application behaviour is proposed. Approval completes these three
written screening grading applications, not the wider catalogue or runtime validation.

Recorded approval in the scoring documents, T54, protocol, spec/decisions log, map and audit
register. Direct-event window anchoring is the remaining narrow screening policy check;
broader T52 objective/evidence and downstream reconciliation work remains open.

## Direct-event window approved — 2 November 2026

For a question about a single login with no alert, the author approved using the login
timestamp as both window anchors: 24 hours before through 24 hours after the login.
Clip to actual available records and explicitly state missing coverage. Further expansion
requires the analyst's decision. Example: a login at 14:00 UTC on 3 October has a requested
window from 14:00 UTC on 2 October through 14:00 UTC on 4 October.

This does not change alert-relative windows or the approved O1-06/O1-09 diagnostic coverage.
T54 materialises precise interval representation consistently with the core's time contract.
Recorded in case specifications, protocol, T54, spec/decision log, map and audit register.
All narrow screening policy decisions identified in the approval audit are now settled.
T52 remains claimed for its broader objective-to-evidence mapping, saved-run inspection,
scope dispositions and downstream reconciliation. T54 remains blocked by T52; no build or
paid run is launched by this ruling.

## Objective-to-evidence mapping — 2 November 2026

At the author's request, built the [phase 0/1 mapping](../research/52-objective-to-evidence.md)
and [saved evidence inventory](../research/52-saved-evidence-inventory.md). Ten rows cover
activity, account context, assessment, full potential reach, spread/shared ground, uncertainty,
workflow, durable evidence, security and evaluation. Each identifies data, behaviour, expected
answers, implementation, evidence, gaps and owners. No new scope is approved.

Inspected current registry, account adapter, graph/period contracts, test source, eight-question
exam, T24 lookup/persistence evidence and raw T22/T23/T49 retrieval plus T49 Port results.
Retrieval remains 5/8 in those saved runs; T49 Port is 60/63 with Q04 attribution 0/3.
T49 graph evidence predates T50. Current source exposes only account lookup among planned
KB tools. The fixed-evidence screen cannot prove live retrieval or phase-1 acceptance.

Model record: Codex; exact active variant not independently exposed in this session.
The map's guidance is advisory; prior-session Astra confirmation is not claimed as current
verification. The research skill used a background source-inspection agent.

B-143 records stale documentation separately. AUD-076 stays open. Screening approvals stand;
T52 remains claimed and T54 blocked. No application/spec/gold changes, runtime tests or paid
calls. Local links and whitespace checked. Next: author review, candidate dispositions and
downstream reconciliation including T45/T26/T28/T29/T30/T40.

## Mapping review: E01 accepted — 2 November 2026

The author accepted E01: explain the activity using triggering records, surrounding failures
and successes, source/device changes, accurate code-built counts and sequence, and explicit
coverage gaps. Preserve the approved window: 24 hours before alert start through 24 hours
after alert end, or the single login timestamp ±24 hours without an alert. Clip to available
records; missing later records never establish that nothing happened afterward.

This accepts the mapping of existing requirements, not runtime proof or a new scope change.
T26 owns integrated collection; T29/T40 own verification. Downstream reconciliation remains
pending. Next review row: E02, account significance. T52 remains claimed.

## Mapping review: E02 accepted — 2 November 2026

The author accepted E02 and requested the next row. Explain account significance through
recorded owner, department, evidenced role, privileged groups and sensitive permission paths.
Select context relevant to the investigation and state unavailable role information explicitly.
Permission shows potential impact, not observed resource access; a permission snapshot does not
establish event-time permissions. Role alone does not establish normal behaviour.

This accepts the mapping of existing requirements, not runtime proof or a new scope change.
T26 owns context selection; T29/T40 own verification. Downstream reconciliation remains
pending. Next review row: E03, assessment using supporting and competing evidence.

## Mapping review: E03 accepted — 2 November 2026

The author accepted E03 and requested the next row. Assess the most supported explanation
using login facts, account context, supporting documents and competing evidence. Check
applicability to the person, time and activity; preserve important evidence through retrieval,
ranking and package limits. State limitations and what would resolve uncertainty. The analyst
retains the verdict. An explanation for location does not automatically explain separate
attack activity.

This accepts the mapping of existing requirements, not retrieval closure, runtime proof or
a new scope change. T45 owns retrieval decisions; T26 the package; T29/T40 end-to-end
verification; T54 separate fixed-evidence interpretation tests. AUD-062 remains open.
Next review row: E04, full potential blast radius.

## Mapping review: E04 accepted — 2 November 2026

The author accepted E04 as the retained full potential blast-radius capability. Show the
complete reachable-asset inventory through group memberships, grants, asset sensitivity and
checkable permission paths. Provide summary counts and highlight sensitive assets, with full
lists available in evidence. This remains distinct from E02's context selected for explaining
the login. Permission paths describe potential exposure, not observed resource access or
lateral movement. Snapshot permissions do not establish historical access.

This confirms existing phase-1 scope in the mapping, not runtime acceptance or a new scope
change. T26 owns packaging; T29/T40 verification; presentation tickets the evidence views;
T42 live acceptance. Downstream reconciliation remains pending. Next review row: E05,
connected activity and shared devices.

## Mapping review: E05 accepted — 2 November 2026

The author accepted E05. Identify other accounts targeted by the suspicious source and
accounts using the devices involved, with dated login/device-use evidence inside the agreed
window. Connections justify investigation, not compromise or common-control claims. For
the login assessment, select devices involved in the suspicious activity; do not restore
removed shared-address exposure/context.

The current generic graph query covers all subject devices in the window; involved-device
selection remains implementation work. S6's empty peer set does not prove positive shared-
device behaviour. T25 owns the peer tool; T26 relevant collection; T29/T40 verification;
T42 live acceptance. This accepts the mapping, not runtime proof or a new scope change.
Downstream reconciliation remains pending. Next review row: E06, uncertainty and missing
evidence.

## Mapping review: E06 directions raised — 2 November 2026

The author distinguished two directions: additional dataset preparation to support uncertainty
handling, and guidance/recommendations based on incident-response practice. Asked whether the
first direction's preparation is worthwhile and invited pushback. E06 is not yet accepted.

Codex recommendation for discussion: retain honest reporting of current evidence limits as a
core obligation; use a small set of controlled evaluation fixtures for missing coverage, empty
results, failed checks and omitted results. Do not infer a requirement to populate every missing
evidence source or make every case resolvable. Broader telemetry/data expansion remains a
separate capability decision. The approved 50-person/30-day target remains unchanged.

Also propose bounded next-investigation guidance grounded in an approved, versioned source
and the specific case gap. Distinguish an external analyst check from an available app action;
no autonomous collection or response. General practice cannot establish case facts. Exact
recommendation scope, source corpus and evaluation ownership need a ruling before implementation.
Official reference consulted: [NIST SP 800-61r3](https://csrc.nist.gov/pubs/sp/800/61/r3/final),
April 2025; incident-response guidance includes scope/impact/resource tradeoffs. This reference
supports the guidance discussion, not a claim that the proposed app boundary is a NIST mandate.
No spec change or E06 approval recorded.

## Mapping review: E06 approved with bounded guidance — 2 November 2026

The author approved both proposed directions. Preserve honest evidence-limit reporting and
prepare small controlled evaluation cases for missing coverage, empty results, failed checks
and omitted results. Identifying missing evidence does not require adding that evidence source
or making every case resolvable. Do not expand endpoint, session or resource-access telemetry
merely to close uncertainty. The approved 50-person/30-day target remains separate and unchanged.

Provide case-specific next-investigation guidance grounded in case evidence plus approved
incident-response practice. Name the check, the uncertainty it addresses and whether it requires
an external analyst action or is available in the app. General guidance cannot establish case
facts or imply a check ran. Curated sources and relevance tests are required. Broad response
planning and automated containment are deferred; no autonomous scope expansion is approved.

Recorded this approved boundary in the spec and decisions log and in the mapping. Exact source
selection and detailed test/implementation allocation remain T52 downstream reconciliation work;
no new build or paid run starts. E01–E06 are reviewed; next is E07 workflow completeness.

## Mapping review: E07 approved — 2 November 2026

The author approved E07's completion and scope rules. A full investigation follows the
required code-tracked checks; a narrow lookup stays narrow. Track whether each check ran
and what it returned. Failed checks remain visible with reasons and do not count as clean
results. The answer identifies outstanding checks and their effect on the conclusion.
Additional history requires analyst approval. A polished report is not proof of completeness.

T26 owns collection; T28 workflow enforcement and the report gate; T29/T40 verification.
This approves the mapping of existing requirements, not runtime acceptance. The knowledge-base
workflow and report gate remain unbuilt. Downstream reconciliation remains pending.
Next review row: E08, checkable evidence preserved with the saved answer.

## Mapping review: E08 approved — 2 November 2026

The author approved E08 before asking about SQLite's responsibility. Preserve original
evidence with the saved answer, resolve citations against that evidence, expose checkable
records/paths/passages and warn on unresolved references. Reopening must not silently
substitute current source data. Resolving a citation does not prove semantic claim support.
Existing lookup-artifact persistence is narrower than full-package/display proof.

Clarification checked against investigations.py, agent.py and knowledge_tools.py: SQLite
holds the investigation index and checkpointed messages, including tool results, existing
lookup artifacts and saved report JSON. Full evidence presentation remains later work;
SQLite does not hold a complete copy of the source knowledge base. No storage change is
proposed. E09/E10 remain for review after the author's question.

## Mapping review: E09 approved — 2 November 2026

The author approved E09. Logs, retrieved documents and tool outputs inform the investigation
but cannot command it. Ignore embedded malicious instructions while retaining legitimate
evidence for assessment. Tools remain read-only and evidence presentation remains plain text.
T25/T26/T28 own tool/workflow boundaries; T29/T40 injection checks; presentation tickets
safe rendering. Historical Port log-injection passes do not establish safety of future
document retrieval, evidence displays or specialist handoffs. This accepts the mapping, not
runtime proof. Next review row: E10, repeatable evaluation, the final row.

## Mapping review: E10 approved; ten-row review complete — 2 November 2026

The author approved E10. Version data, questions, expected results, settings and saved
execution evidence. Measure graph correctness, retrieval, answer quality, workflow and
security separately, then prove them together through the application and author acceptance.
Preserve failures and distinguish passed, failed and untested behaviour. Keep Port and
knowledge-base results separate. The isolated four-case screen does not certify the full app.

T29–T31 own application evaluation/recording; T39–T41 calibration, expanded coverage and
comparisons; T42 final acceptance; T54 isolated comparison evidence. No existing gate or
threshold changes. All ten mapping rows E01–E10 are now approved, including E06's bounded
guidance refinement already recorded in the spec. This completes mapping review, not T52.

Candidate dispositions, detailed downstream reconciliation and B-143 documentation cleanup
remain. T52 stays claimed, AUD-076 open and T54 blocked. No application build, runtime test
or paid call. Whitespace checked. Next: candidate dispositions, starting with reverse asset
exposure, then reconcile approved requirements into the affected tickets.

## Scope-history verification — 2 November 2026

The author challenged reopening reverse asset exposure and recalled settling on objective 1
as the sole phase-0/1 objective. Inspected the original local Codex conversation, not only
assistant-authored handoffs: session 01a19917-7284-7001-8e2a-0c0fbf1b5eb6, 2 November,
08:33:59–08:44:35 UTC. Relevant sequence:

- 08:33:59: author proposed objective 1 as the sole objective for phases 0/1.
- 08:34:15: assistant agreed it was substantial enough and said reverse exposure could wait,
  but explicitly said narrowing existing blast-radius scope had not yet been decided.
- 08:36:33: author said to work on that. Assistant proposed a bounded account-impact summary,
  separating full asset inventory, every permission path and reverse exposure from it.
- 08:39:07: author agreed. Assistant proposed precise owner/role, privileged/sensitive-access
  and involved-device selection rules.
- 08:44:35: author agreed and requested implementation research for that objective.

This verifies the author's recollection of the narrowing discussion and approved bounded
summary. No explicit final sole-objective scope ruling was found in the inspected sequence;
the assistant's formal caveat remained in the written record while subsequent work focused
on objective 1. Do not treat missing documentation as proof the author intended broader scope.

Today's E04 approval followed an assistant presentation asserting retained full blast radius.
The author has now questioned the underlying scope, so that approval must not be used to
infer a conscious reversal of the earlier direction. Clarify this specific boundary before
reconciling E04 or opening another candidate-design discussion. No spec reduction or expansion
is made by this verification. E01–E10 review history stays intact, with this scope caveat.
B-144 records the review-process gap. T52 remains claimed and T54 blocked.

## Answer: definitive sole-objective scope ruling — 2 November 2026

Following original-conversation verification, the author agreed: reliable login investigation
is the sole phase-0/1 objective. Keep bounded account-impact context, including owner/role,
relevant privileges and sensitive access, and involved-device relationships. Defer standalone
full reachable-asset inventory, exhaustive permission-path presentation and reverse asset
exposure. This resolves the ambiguity; do not ask to design reverse exposure for this phase.

Supersedes E04's earlier full-inventory interpretation. The other approved mapping safeguards
and E06 guidance remain. Graph foundations stay available; no implementation deletion is
authorised. Existing tests/gold/thresholds remain pending specific reconciliation, not waived.

Recorded in spec scope/decision log, mapping, working requirements, map and session-entry
documents. Added explicit scope handoffs to affected active tickets. T52 stays claimed for
detailed downstream reconciliation and remaining evidence/data ownership. T54 stays blocked.
B-144's scope ambiguity is resolved by this ruling; B-143's broader stale prose cleanup remains.

## Downstream reconciliation — 2 November 2026

Author requested continuation from the handoff. Applied existing approvals, without a new
product-scope decision or runtime claim. Model identity: Codex; exact active variant is not
independently exposed. Inspected the handoff, current map, P-01–P-03, relevant AUD-062/064/065/066/076
entries, the approved mapping and active spec/tickets. Historical source/run inspection remains
in the saved-evidence inventory; no fresh execution is asserted here.

### Candidate dispositions under the definitive ruling

| Candidate | Disposition and reason | Change needed / owner |
|---|---|---|
| Account investigation completeness | Retain within the sole objective: trigger, surrounding activity, account significance and competing evidence | Capability integration in T26/T28, retrieval decisions T45, application proof T29/T40/T42; not evaluation-only |
| Bounded potential impact | Retain relevant privileged/sensitive access and supporting paths | T26 selection, T34 author-reviewed presentation, T29/T40 tests; existing core facts remain reusable |
| Full reachable inventory and exhaustive permission paths | Defer as standalone product requirements under the author's definitive ruling | No implementation/deletion now; retain existing exact graph regression evidence |
| Reverse asset exposure | Defer beyond phases 0/1 under the same ruling | No new source, endpoint, evaluation gate or design ticket required now |
| Explicit unresolved evidence | Retain; empty, unavailable, failed and omitted are different outcomes | T26 artifacts, T28 workflow/report gate, T40 controlled fixtures, T29 application exam |
| Case-specific next-investigation guidance | Approved addition under E06, bounded to case facts and approved practice | Needs curated sources and capability work, not only evaluation; allocation proposal below |
| Behavioural baselines | Defer; a role or 30-day log does not establish normal behaviour | No new baseline collection/model approved; future initiative if reopened by author |
| Endpoint evidence | Defer additional telemetry; retain existing involved-device relationships | No endpoint ingestion approved; missing endpoint evidence remains a legitimate limitation |

### Applied handoffs

| Owner | Reconciled requirement |
|---|---|
| T26 | Alert/event windows, clipping, involved-device selection, bounded account impact, code facts versus assessment, distinct incomplete states, complete returned evidence versus exhaustive inventory |
| T45 | Evidence needs and applicability, supporting/competing passages, loss through fusion/ranking/caps; original K04 failure and gold retained |
| T27 | Reference validity does not prove claim support; preserve original evidence |
| T28 | Shared required-step state, honest failure/omission handling, analyst-controlled expansion and recommendations versus performed checks |
| T29 | Separate collection/retrieval/interpretation evidence, unchanged exams/gates, retained failures; screening is not app acceptance |
| T30 | Applicability, uncertainty and potential/observed access in advisory assessment; no new hard gate or paid screening judge |
| T34 | Bounded-context presentation; author agrees revised screen/API before UI code; no imposed replacement layout |
| T40 | Coverage matrix, controlled uncertainty cases and guidance relevance; no automatic gold edits or telemetry expansion |
| T42 | Integrated application proof, saved-evidence continuity and native Browser inspection replacing future Gephi wording |

Spec overview, relevant stories, package/window, screen and storage summaries now reflect
existing rulings. Historical decision records and graph regression contracts remain intact.
The earlier `radii` API sketch is explicitly a draft awaiting T34's bounded-context agreement,
not a newly adopted API contract. No application, API-contract file, gold, threshold, fixture,
operator command, service or paid run changed.

### Ownership proposal, subsequently approved below

This table records the proposal presented to the author. The subsequent approval below
settles the allocation; it does not authorise building.

| Work | Proposed owner and reviewable result | Boundary |
|---|---|---|
| E06 guidance sources | T45 research selects a small source list and maps each proposed passage to the uncertainty it helps investigate; author approves that list before ingestion/use | Existing corpus is considered first; NIST SP 800-61r3 was consulted, not adopted wholesale; no new broad response-planning corpus |
| E06 implementation and tests | T26 integrates approved guidance; T28 preserves action/check state; T40 supplies relevance/unsupported-action cases; T29 records app results and T30 remains advisory | No automated containment, no claim external checks ran, no revised acceptance threshold |
| 50-person/30-day data target | A separate scoped data ticket owns generator, surrounding activity, corpus/truth consistency and compatibility evidence before T40 uses the expanded world | Preserve existing stories and frozen Port exam; no behavioural baseline, no forced resolution of all cases; T54's four approved fixtures stay separate |

T26 still needs concrete selection/input-output rules at its design step. T45 still owns its
five retrieval decisions; this reconciliation does not choose a decomposition strategy or
change what K04 measures. T34 still needs the author's screen agreement. These are explicit
later design obligations, not a reason to reopen the settled objective.

T52 remains claimed and T54 blocked. Closure still needs the remaining source/data ownership
ruling and a final criterion-by-criterion review. B-143's K03 provenance item remains with T51;
no exam text was silently changed. AUD-062/064/066/076 remain open.

Verification for this reconciliation: `git diff --check` passed; ten affected ticket criterion
sections present; five scope links and their spec heading resolve; T52 remains claimed and
T54 retains its T52 blocker; AGENTS.md and CLAUDE.md remain identical. No diffs in backend,
frontend, API contract or admin manual. No runtime tests were run for these documentation
edits. Ownership proposal sent to the author for ruling; no approval inferred from waiting.

## Answer: guidance and dataset ownership approved — 2 November 2026

After the question was repeated in plain chat, the author explicitly replied "approved":
T45 selects guidance sources and brings them to the author for approval; T26 integrates
approved guidance; a separate data ticket owns the 50-person/30-day dataset. Created
[T55](55-thirty-day-investigation-dataset.md) to materialise the data responsibility and
made T40 depend on its accepted data. T54's controlled fixtures remain independent.

Updated T45/T26/T40, the spec and decisions log, map and AUD-076. Exact guidance sources
are now T45's review obligation, not an unresolved T52 allocation. T55 must secure agreement
on its concrete dataset design before build. No source is adopted, dataset generated or
application implementation authorised by this allocation. Existing T28/T29/T30/T40 testing
responsibilities remain unchanged.

T52 stays claimed for its final criterion-by-criterion closure review. T54 remains blocked
until that review is completed; no new screening approval is requested by this record.

## Answer: review complete — 2 November 2026

The author approved the final ownership allocation and requested the closure review. All
T52 decision-review criteria are evidenced below. This resolves a planning/reliability review,
not implementation acceptance or a claim that the application already meets the objective.

| Criterion | Closure evidence |
|---|---|
| Implementation, saved evidence, spec and principles reviewed | Objective mapping and saved-evidence inventory identify inspected source and exact historical runs. P-01–P-03 and map model guidance reviewed. Work performed by Codex; exact model variant was not independently exposed, recorded honestly in the review. The map makes the recommendation advisory; no unverified variant is claimed. |
| Objective-to-evidence mapping | E01–E10 reviewed by author; definitive sole-objective ruling supersedes the earlier broad E04 interpretation. |
| Candidate dispositions | Downstream reconciliation table records retained account/context/uncertainty work, approved bounded guidance, and deferred full inventory/reverse exposure/baselines/endpoint ingestion, with capability/data implications. |
| Author rulings and spec | Definitive scope, E06, screening policy and final source/data ownership approvals recorded in this ticket and the spec decisions log. Exact sources/design remain named downstream decisions. |
| Downstream requirements | Detailed T26/T45 and T27–T30/T34/T40/T42 criteria updated; T55 created and T40 dependency added. T54 consumes approved policies rather than asking for them again. |
| Documentation inconsistencies | B-143/B-144 retain history; active spec and T42 pointers reconciled. K03 is assigned to T40 for a proposed correction, preserving frozen exam/gold. B-145 records and corrects the mistaken T51 assignment. |
| Audit and remaining proof | AUD-076 decision-review closure recorded. AUD-062/064/066 stay open; full collection/retrieval/interpretation proof remains T26/T28/T29/T40/T42, advisory support assessment T30, screening/recording T54, source decisions T45 and data T55. |
| Map and work boundary | Map records completion and T54 as next by the existing delivery order. No application, new source, gold, threshold, operator command, service, commit, push or paid run changed. |

T45, T26, T54 and T55 retain their declared dependency lines; resolved T52 satisfies that
one prerequisite. T26 still waits for its other dependencies. T54 is next by the author's
existing priority, not because every other ticket is blocked. It must meet its own model
confirmation and build/readiness criteria before implementation or paid execution.

Source selection and dataset/screen design are downstream decisions with owners, not
unfinished T52 approvals. Historical comments saying T52 is claimed or T54 blocked describe
prior states and are superseded by this Answer.

Closure verification: `git diff --check` passed. All 65 local file links checked across
T26/T27/T28/T29/T30/T34/T40/T42/T45/T52/T54/T55 and the mapping/inventory resolve. All eight
T52 criteria have evidence above. T51 remains resolved; no backend/frontend, frozen exam,
API-contract or admin-command diff exists. AGENTS.md and CLAUDE.md remain identical.
No runtime test was needed or run for this documentation-only decision closure.
