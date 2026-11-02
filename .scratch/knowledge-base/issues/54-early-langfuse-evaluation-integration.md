# 54: Isolated comparison runner and early Langfuse recording

Type: build
Status: ready-for-agent
Blocked by: 52
Phase: 0
Model: standard (Opus 5.5 or Sol 6.1)
Rigour: Tier 3

## What to build

Author approved on 2 November 2026: this ticket owns both the isolated comparison runner
and reusable Langfuse recording. It follows T52 and does not depend on T29's full application
exam. Use [T52's approved record contract](52-agent-objectives-and-reliability-review.md#approved-runner-ownership-and-record-contract--2-november-2026)
and the [comparison protocol](../research/52-objective1-comparison-protocol.md).

Support separate compatibility, six-model screening and A/B/C architecture-calibration
modes through one local record contract. Reuse suitable existing evaluation utilities;
keep experimental results separate from the working application's acceptance gates.
T29 owns those exams, T30 the advisory judge, and T31 application/full-exam tracing.

Local evidence is authoritative. Save before upload, remove secrets before persistence,
mask all outbound records and export human labels explicitly. Runtime evaluation never
reads from Langfuse. No production specialist or application model migration is included.

## Delivery checkpoints

1. Build the frozen synthetic fixtures, isolated runner and local records from T52's
   approved cases, role responsibilities, scoring and selection policy. Materialise IDs,
   hashes and role prompts as implementation work; do not reopen those policy approvals.
   Verify using fake models.
2. Add the Langfuse mirror and blinded label workflow; verify against a fake destination.
3. After readiness and execution authorisation, run compatibility sessions and model screening.
   Reconcile genuine scored screening evidence with Langfuse and obtain author inspection.

Implementation readiness precedes live verification; the ticket is not resolved merely
because the runner can start. A real scored screening result can satisfy the live mirror
criterion; a transport probe cannot. The later twelve-answer A/B/C calibration reuses this
runner after provisional model selection and its separate budget/readiness decisions.
It need not block T54 closure. The 189-answer stage remains unapproved.

## Approved screening policy

- Six configurations, four cases, three passes: 72 scheduled attempts; inspect setup after 24.
- One case at a time, rotating model order, fresh memory and frozen evidence/settings.
- For a single-login question without an alert, use 24 hours before/after that login's
  timestamp, clipped to available records with coverage gaps stated. Expansion remains
  analyst-controlled. Preserve alert-relative and O1-06/O1-09 diagnostic windows.
- Three minutes per request and ten minutes per complete case, including retries/backoff.
- No evaluation-imposed token, model/tool-call or retry count caps. Preserve every attempt.
- Six separate initial compatibility sessions before scoring; diagnose failures first.
- Version setup fixes and rerun only affected comparisons; retain original results.
- Select the provisional A/B/C model only after all three passes. Eligibility requires
  twelve completed trials, no designated critical errors and no applicable zero scores.
  Compare quality case by case; similar quality is decided by cost, then speed. If none
  qualifies, diagnose rather than automatically promoting the least-bad candidate.
- Track actual costs against a US$25 planning budget, reviewing at US$15 and after 24 results.
  No reservations or worst-case billing gate. Unknown charges remain unknown, not zero.
  Architecture calibration and paid scoring models are outside this budget.

T52 is resolved. This ticket is next in the author-approved delivery order. Its model
confirmation, implementation checks and live-execution readiness requirements still apply;
closure of T52 does not authorise an immediate paid run.

## Acceptance criteria

- [ ] Before build, tell the author the Model line, obtain confirmation and record the model used.
- [ ] Verify the implementation against resolved T52's approved cases, roles, scoring,
      selection policy and nine-group record contract without changing application gates.
      Fixture IDs/hashes and concrete role prompts are this ticket's build work.
- [ ] Runner modes implement the approved screening policy and isolated A/B/C designs.
      Fixtures, prompts, rubric, settings and execution order are versioned; gold stays out
      of model input and every trial has fresh memory.
- [ ] Save setup, evidence, configuration, per-request history, tool/role activity, case
      outcomes, resources, assessments and mirror/review status with stable linked IDs.
      Numeric 0/1/2, N/A and unscored are distinct; critical errors remain separate.
- [ ] Persist request starts before dispatch and outcomes incrementally. Preserve partial
      and failed attempts, retry lineage and repair versions. Recovery never silently
      repeats an unresolved billed request. Missing usage/cost stays explicitly unknown;
      settlement updates cannot double-charge the same request in summaries.
- [ ] Mirror saved experiments, inputs, intermediate role outputs, final answers, versions,
      scores, timing and available usage/cost. No upload retry repeats inference.
- [ ] Off by default behind one environment switch; keys load only when enabled and never enter
      results. Mask every outbound record. Runtime evaluation never reads from Langfuse.
- [ ] Save local results before upload; report upload failure visibly and preserve local evidence.
- [ ] Export versioned human labels explicitly. Blinded answer review hides model/design
      identity, settings, costs, timing and revealing traces. Separate process/security
      review retains required trace access and states its blinding limitation.
- [ ] For screening, support the author as primary scorer with Codex preparing/recording.
      Save initial human scores before assistant discussion/suggestions; retain revisions
      and reasons. Support small review batches and measured review effort. No second human
      or paid judge is required; do not present Codex assistance as independent human agreement.
- [ ] Selection reporting applies the approved eligibility rule and retains per-case
      profiles, failures and selection rationale. N/A and unscored cannot be mistaken for
      failed/passing scores. No candidate is eliminated at the first-pass setup checkpoint.
- [ ] Implement the approved four-case grading rules: O1-02 needs no invented attack
      hypothesis; O1-09/O1-12-D inherit O1-06's complete criteria and critical errors plus
      their coverage/injection obligations. Quoting injection text is not obedience.
- [ ] Offline tests cover fresh state, schedule identity, request/tool/retry lineage,
      deadlines, interruption/recovery, missing usage, cost deduplication, gold isolation,
      score fidelity, blind views, disabled/enabled mirror, masking, local-first persistence,
      upload failures and label export. Deterministic rescoring needs no model calls.
- [ ] An authorised scored screening result is visible remotely and reconciles locally;
      record the author's inspection. A transport probe alone is not live evaluation evidence.
- [ ] Update the admin manual and test its commands. Standing regression, type-check and
      two-axis review requirements pass.

## Remaining ownership

T31 retains application tracing and the two existing exam files' datasets, experiments and
scores through T29. Reuse this integration. AUD-036 stays open until the original full closure
evidence, including retrieval-layer fields, exists. Early screening/calibration does not close it.
No paid run, model choice, larger trial or permanent specialist adoption is authorised here.

## Comments

- 2026-11-02 — Author approved the delivery split and sequence above. No implementation yet.
- 2026-11-02 — Langfuse hosted documentation; SDK version not selected. Official
  [evaluation concepts](https://langfuse.com/docs/evaluation/core-concepts) and
  [offline evaluation](https://langfuse.com/docs/evaluation/get-started/offline), via web search:
  checked experiments, traces and scoring concepts for planning. Before coding, follow
  get-api-docs and verify installed SDK compatibility and the required APIs.
- 2026-11-02 — Author approved expanding T54 to own the comparison runner and Langfuse
  recording together, with T52's nine-group record contract and three delivery checkpoints.
  Genuine screening evidence may establish live integration before architecture calibration.
  T29/T30/T31 retain their stated scopes. No build or paid run performed.
- 2026-11-02 — Author approved primary human scoring with Codex preparing blinded reviews,
  recording labels and assisting after initial scoring. Revisions remain visible; review in
  small batches. No second human/paid judge required for screening. T30 remains unchanged.
- 2026-11-02 — Author approved quality-first provisional-model selection: twelve completed
  trials, no critical errors/zero scores, case-level quality comparison, then cost/speed
  for similar quality. No qualifying model means diagnosis, not automatic promotion.
- 2026-11-02 — Author approved the remaining screening grading applications. Written
  rules for all four cases are settled; scorer/fixture verification remains this ticket's work.
- 2026-11-02 — Author approved direct-event window anchoring on the single login timestamp,
  24 hours before/after, clipped to available records with missing coverage stated. No change
  to alert-relative or O1-06/O1-09 windows. Narrow screening policy checks are settled;
  broader T52 closure still blocks build.
