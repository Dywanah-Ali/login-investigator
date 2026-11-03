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

- [x] Before build, tell the author the Model line, obtain confirmation and record the model used.
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
- 2026-11-03 — Model line told to the author (standard: Opus 5.5 or Sol 6.1). Author
  confirmed Claude Opus 5.5 for this build session. Build started under `/implement T54`.
- 2026-11-03 — Author ruling: screening trials run in fixed-evidence mode. The complete
  model-visible case file goes in the investigator's first message; no tools are offered in
  scored screening or A/B/C trials. Records mark the mode `fixed_evidence`, so no screening
  result is presented as tool or retrieval evidence. The tool request/result/final-answer
  round trip is exercised only in the six compatibility sessions. Injection obedience in
  O1-12-D is assessed from claimed actions and stated conclusions under the approved rubric.
- 2026-11-03 — Checkpoint 1 built (`backend/evals/comparison/`): frozen fixtures with separate
  gold, run bundle, rotated runner with recorded retries/deadlines/recovery, A/B/C designs,
  compatibility tool loop, labels, blinded batches, label sheets and selection report.
  71 offline tests, clean types and lint; a dry-run adapter exercised every command at no cost.
- 2026-11-03 — Langfuse documentation check (get-api-docs). Context Hub `langfuse/observability`
  covers SDK v3.14.5 (March 2026) and is stale for Cloud v4. Official docs consulted:
  [OpenTelemetry integration](https://langfuse.com/integrations/native/opentelemetry),
  [v4 migration](https://langfuse.com/integrations/native/opentelemetry/migration-to-v4),
  [OTel experiments](https://langfuse.com/integrations/native/opentelemetry/experiments.md),
  [public API](https://langfuse.com/docs/api-and-data-platform/features/public-api.md) and
  OpenAPI spec mirrors. Behaviour checked: legacy ingestion for traces/observations sunsets on
  Cloud on 16 November 2026; traces go to `POST /api/public/otel/v1/traces` (OTLP HTTP/JSON or
  protobuf, Basic auth, `x-langfuse-ingestion-version: 4`) with `langfuse.observation.*` and
  `langfuse.experiment.*` attributes on every span; re-sending a span ID can create duplicates,
  so each trial must be exported once; scores go to the Scores API with an idempotent ID;
  datasets via `POST /api/public/v2/datasets` and `POST /api/public/dataset-items` (upsert by
  item ID). Not established by the docs: whether historical span timestamps are honoured, the
  long-term status of `POST /api/public/scores`, payload limits. Only a live upload proves them.
- 2026-11-03 — Author ruling: the mirror sends saved records itself as OTLP HTTP/JSON plus
  REST calls through the existing `requests` dependency, not through the Langfuse SDK. Every
  timestamp and ID comes from the run bundle; each trial's trace is sent once, tracked locally.
  Checkpoint 2 test points approved: the mirror against a fake destination, and label export.
- 2026-11-03 — Checkpoint 2 built: `mirror.py` (OTLP/JSON traces with experiment links,
  dataset and items, idempotent scores, send-once status per trial, masking `mask-1`, switch
  `LI_LANGFUSE`), numbered label exports with drift checks, and operator commands for labels,
  revisions, notes, effort, reruns, selection, trace view and mirror. Admin manual section 8
  added; every command run as written on fresh dry runs, refusals included (B-146 fixed).
- 2026-11-03 — Two-axis review. Fixed: unassessed critical errors now count as unscored, not
  absent, in eligibility and in the assistant-note gate; critical flags are initial-once with
  explicit revisions; repeated offline checks are not re-recorded; batch numbers are never
  reused after a crash and the review mapping lives in the event log; interrupted trials are
  mirrored; usage fields a provider omits stay unknown; the code-version record covers the
  core, data and locks; O1-12-D gold gained its Alternatives addition (fixture version
  `f903b7f47620`); missing commands added. Open items, including two that need the author's
  ruling, are in AUD-077. Checkpoint 3 not started: no paid adapter, no live upload.
- 2026-11-03 — Verification at commit. Comparison suite 93 passed; Pyright 0 errors; Ruff
  clean on the whole backend; frontend 150 passed and typecheck clean. Full backend suite
  (sandboxed): 724 passed, 6 failed, 31 errors. All 37 come from one cause: the sandbox
  denies the Docker socket, so Neo4j test containers cannot start (`GraphUnavailable: Neo4j
  container operation failed`). Affected files: test_paired_lifecycle, test_graph_version,
  test_graph_verification, test_native_inspection, test_api_startup, test_browser_access,
  test_eval_retrieval, test_evaluation_version, test_kb_agent, test_knowledge_graph. None
  imports the comparison package. The author chose to commit with this gap recorded; those
  files are NOT re-verified and the next session reruns them first, with Docker reachable.
