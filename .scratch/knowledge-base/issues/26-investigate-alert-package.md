# 26: The investigation tool and its package

Type: build
Proof type: AI judgement
Rigour: Tier 3
Status: ready-for-agent
Blocked by: 13, 25, 45, 50, 52, 57
Phase: 0
Model: strongest (Fable 5.1 or Astra)

## T52 scope handoff — 2 November 2026

Author confirmed reliable login investigation as the sole phase-0/1 objective, with bounded
account-impact and directly connected activity context. Standalone full inventory, exhaustive
permission-path presentation and reverse asset exposure are deferred. This supersedes broader
product-scope wording below. See [spec Current scope ruling](../spec.md#current-scope-ruling--t52-2-november-2026).
Detailed criteria below carry the approved T52 boundaries. Open design decisions remain
explicit; this reconciliation does not release T52 or authorise implementation.
Existing source code, questions, gold and thresholds are not changed or waived by this note.

## What to build

T45 ruling, 8 November 2026: full-investigation activation is retained parent workflow state
established before research dispatch, not inferred only from a model's call to this tool.
The shared core procedure supplies required obligations. Preserve this package's code-built
baseline clearing/aggravating searches and shared retrieval core; research follow-ups supplement
the baseline. The T45 full-procedure obligation table maps the inherited evidence requirements.
Author-approved ownership, 8 November 2026: this ticket owns the single shared procedure
definition and deterministic package. T57 supplies activity/account/connected evidence, T25
supplies documentary interfaces over T58, T59 supplies supplementary research, T60 activates
and enforces the procedure before dispatch, and T28 consumes it at the report gate. No
duplicate playbook or implementation authorisation follows from this handoff.

The analyst asks the agent to investigate a finding by its ID, and `investigate_alert` runs playbook
steps 2 to 6 in code and returns one package: account context, bounded potential impact,
involved-device peers, clearing documents and aggravating documents. Each section has its
evidence status and citations. Code supplies facts and check outcomes; the model assesses
the evidence and the analyst retains the verdict. It reports
progress per internal step, so the screen can later stack the steps while they run.

## Decisions implemented

- T05 d1 (`investigate_alert(finding_id)`), T05 d2 and d3 (one package with a named section per step,
  computed and ordered in code; spray and brute-force targets as a section, empty for other rules),
  T05 R5 (clearing and aggravating searches built in code from the finding's record, never from the
  chat; the radius from the one radius function of ticket 19), T05 d12 (package caps), T05 d13
  (parallel tool calls stay on).
- T05 d2 and T07 d4 (progress per internal step through the Port's custom stream).
- User stories 9, 15 to 19, 22, 23. Spec doors 2 and 3.

## Acceptance criteria

- [ ] Own the one core procedure definition used by T60 activation/enforcement, T28 report
      completion and T29 evaluation. Compose trusted T57/T25 task obligations; do not duplicate
      the procedure in model prompts, hooks or workers. Expose code-derived required work and
      status through the shared contract before parent integration.
- [ ] Verify the package from a resolved finding or login event through collection, baseline
      search and assembled evidence, without requiring prior model-selected tools. T57 owns
      reusable deterministic relevance/device rules and exact identity; this ticket selects
      and records their procedure use. Code-built baseline misses remain visible after research.

- [ ] Preserve the code-built baseline's own candidate and delivered-evidence records under
      T45's approved 8 November path-specific gate. Later research recovery must not hide a
      baseline package miss. Use independently resolved case identity, not expected passages
      as query inputs; preserve original gold and source bindings. T29 owns application proof.

- [ ] Before any build work starts, the builder tells the author this ticket's `Model:` line and
      asks the author to set that model. The build starts only after the author confirms, and a
      dated line under Comments records the model used.
- [ ] `investigate_alert` finds the finding by its ID; an unknown ID returns plain content saying so.
- [ ] For an alert, omitted bounds use alert start minus 24 hours through alert end plus
      24 hours. Direct single-login investigation uses its timestamp ±24 hours. Clip to
      available records and disclose requested/effective bounds and coverage gaps. Explicit
      bounds reach the shared core; expanding history requires the analyst's decision. Test
      both defaults, explicit bounds and clipping. The generic core's all-record default
      must not silently become the package default. Permissions remain a snapshot.
- [ ] Device context selects devices involved in the suspicious activity, with dated peer
      records in the agreed window. Record the selection basis and omissions. Do not include
      every device used by the account merely because it appears in the window. No
      address-sharing context; same-source login activity remains distinct.
- [ ] The five named sections have code-built facts, evidence status and citations in a fixed
      order. A targets section is filled for spray and brute force and empty otherwise.
      Triggering/surrounding counts and outcomes come from code, not model arithmetic.
- [ ] Account context includes recorded owner/role and relevant privileged or sensitive
      access with supporting paths. Missing role evidence is explicit. Role is not a
      behavioural baseline; permissions never imply observed asset access.
- [ ] Before build, record the package input/output shape and use of T57
      deterministic relevance/device-selection rules under Answer, aligned with T45. Any new
      scope choice needs the author's ruling. Standalone inventory and exhaustive path presentation are deferred.
- [ ] The clearing and aggravating searches are built from the finding's record; a test proves the
      chat text does not reach them.
- [ ] Keep the package a thin coordinator over the same core account, graph and search
      functions used by narrow tools. Do not duplicate retrieval logic or introduce a model
      investigator inside the tool. No prior narrow-tool calls or model-supplied tool outputs
      are required to assemble the package.
- [ ] Save each internal step's inputs, outputs, evidence IDs and failure status in the artifact,
      under existing security/persistence rules. Independently verify component behaviour and
      package assembly/selection/caps. Use controlled missing-document and failed-step cases
      to distinguish retrieval misses from assembly omissions; do not add new gold or thresholds.
- [ ] Reuse the shared graph operations and retain their exact S6 regression against
      `truth.json`. Test the bounded package selection separately with supporting record/path
      IDs and stated omissions. Do not assert that a selected subset equals the full radius,
      or change existing gold to make that assertion pass.
- [ ] Caps hold: five chunks per search; selected impact and peer evidence is paged with
      `truncated` flags and its complete returned lists preserved in the artifact. Distinguish
      relevance selection from truncation. Full returned evidence is not a promise of full
      reachable inventory. T45 defines preservation requirements and downstream verification
      ownership; implementation/evaluation tickets test that required evidence survives selection and caps.
- [ ] Empty, unavailable, failed and omitted checks remain distinct in content and artifacts.
      Tests include controlled missing coverage and failed checks without inventing telemetry.
- [ ] Bounded next-investigation guidance names the uncertainty addressed, its case evidence
      and approved practice source, and distinguishes external checks from app actions.
      T45's 8 November approved source table defines the initial three-runbook passage set and
      its mixed-content restrictions. Consume the extensible approved-source catalogue with
      T25 as catalogue/reader owner and T58 as ranking owner. T59 supplies later supplementary
      research, not a dependency of baseline assembly. Adding supported runbooks must not
      require new tool/agent branches. Source eligibility does not change mandatory procedure steps.
      Recommendations must never be recorded as completed checks.
- [ ] Each internal step emits start, end or error through the Port's custom stream; a test proves
      the order. The API event itself ships in ticket 36.
- [ ] Parallel tool calls stay on.
- [ ] Agent tests use the fake model; the Port's eval passes.
- [ ] Apply the current proportional-testing and proof rules: focused affected-behaviour tests,
      relevant types/lint, one scoped review and applicable existing agent evaluations. Fake-model
      tests prove plumbing; evaluation proves model behaviour. Older standing safety-net wording
      does not require full suites after every edit or an extra review campaign. Record third-party
      documentation/version checks and test any changed admin commands.

## Comments

- 2026-11-08 — Author approved T26 ownership of the shared core procedure and deterministic
  package in the seven-slice plan. T28 no longer builds a second procedure definition.
  T60 owns activation/integration; T29 owns application proof. IC-01–11 remain inherited.

- 2026-11-08 — Author approved research-only exposure of investigative retrieval tools in
  T45. Code still enforces required checks through shared core functions. This does not move
  deterministic package duties into model judgement. Full-procedure dispatch and final interface
  ownership remain T45 decisions before build; no direct chat retrieval exception is implied.

- 2026-11-08 — Author approved keeping T45 as decisions only, followed by scoped LangGraph
  orchestration research and the agreed design review before two additional build tickets are
  defined. This ticket retains deterministic package ownership pending explicit reconciliation.
  The proposed orchestration ticket must coordinate this capability without duplicating it or
  transferring factual/check duties to model judgement. Final responsibilities and dependencies
  must be reconciled before build; this note does not adopt a new coordinator architecture.

- 2026-11-03 — Author approved the coordinator boundary after discussing overlap with
  narrow tools and troubleshooting. Reuse shared core functions; retain step-level evidence;
  test components and assembly separately. T29 owns separate application evidence for collection,
  assembly and model interpretation. See spec "Investigation coordinator boundary". Documentation
  only; no build release, specialist adoption or T54 change.

- 2026-11-01 — T25 gate ruling: address-sharing context is removed everywhere. T50 removes it
  from the radius and answer key first, so this ticket now also waits for T50.

- 2026-11-01 — Author: wait for [T52](52-agent-objectives-and-reliability-review.md), the
  phase 0 and 1 objectives and reliability review. Carry its approved requirements into this
  ticket before work starts; existing requirements remain in force until explicitly amended.

- 2026-11-02 — Author approved this ticket as the integration owner for E06 guidance,
  using sources selected in T45 and approved by the author before use. No build authorised
  by the ownership ruling; existing design and dependency requirements remain.
