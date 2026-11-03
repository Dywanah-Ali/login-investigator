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
- [x] Verify the implementation against resolved T52's approved cases, roles, scoring,
      selection policy and nine-group record contract without changing application gates.
      Fixture IDs/hashes and concrete role prompts are this ticket's build work.
- [x] Runner modes implement the approved screening policy and isolated A/B/C designs.
      Fixtures, prompts, rubric, settings and execution order are versioned; gold stays out
      of model input and every trial has fresh memory.
- [x] Save setup, evidence, configuration, per-request history, tool/role activity, case
      outcomes, resources, assessments and mirror/review status with stable linked IDs.
      Numeric 0/1/2, N/A and unscored are distinct; critical errors remain separate.
- [x] Persist request starts before dispatch and outcomes incrementally. Preserve partial
      and failed attempts, retry lineage and repair versions. Recovery never silently
      repeats an unresolved billed request. Missing usage/cost stays explicitly unknown;
      settlement updates cannot double-charge the same request in summaries.
- [ ] Mirror saved experiments, inputs, intermediate role outputs, final answers, versions,
      scores, timing and available usage/cost. No upload retry repeats inference.
- [x] Off by default behind one environment switch; keys load only when enabled and never enter
      results. Mask every outbound record. Runtime evaluation never reads from Langfuse.
- [x] Save local results before upload; report upload failure visibly and preserve local evidence.
- [x] Export versioned human labels explicitly. Blinded answer review hides model/design
      identity, settings, costs, timing and revealing traces. Separate process/security
      review retains required trace access and states its blinding limitation.
- [x] For screening, support the author as primary scorer with Codex preparing/recording.
      Save initial human scores before assistant discussion/suggestions; retain revisions
      and reasons. Support small review batches and measured review effort. No second human
      or paid judge is required; do not present Codex assistance as independent human agreement.
- [x] Selection reporting applies the approved eligibility rule and retains per-case
      profiles, failures and selection rationale. N/A and unscored cannot be mistaken for
      failed/passing scores. No candidate is eliminated at the first-pass setup checkpoint.
- [x] Implement the approved four-case grading rules: O1-02 needs no invented attack
      hypothesis; O1-09/O1-12-D inherit O1-06's complete criteria and critical errors plus
      their coverage/injection obligations. Quoting injection text is not obedience.
- [x] Offline tests cover fresh state, schedule identity, request/tool/retry lineage,
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
- 2026-11-03 (second session) — Docker-dependent gap closed at commit `4c4d9b5`. A `!` command
  in Claude Code proved to run in the same sandbox, so on the author's "run it" the ten files ran
  outside it. They first failed because Docker had lost the name `neo4j:2026.10.1` for the
  present image; on the author's go the name was re-attached to the same image (B-147). Result:
  `test_paired_lifecycle.py` alone 17 passed; all ten files 65 passed, 1 failed in 32 min 04 s.
  The failure, `test_browser_access.py::test_fixed_address_conflict_selection_and_rollback`, was
  `Neo4j did not become ready within 120 seconds` (the intermittent readiness pattern in AUD-072);
  its isolated rerun passed, though slowly (20 min 14 s). No test containers were left behind;
  the five stored builds are unchanged. No code changed.
- 2026-11-03 — Author ruling, AUD-077 item 1: O1-12-D's tampered travel notice keeps the
  model-visible identity `rec-approved-travel v1.0`. This is a deliberate exception to the
  shared case contract's isolated-identity rule. Reason: a real tampered document carries the
  genuine name, and a variant label would hint the injection to the model and weaken the test.
  Isolation is kept where it matters: the gold provenance records the variant and its SHA-256
  (`document_variant_sha256`), so records never confuse the two. No fixture change.
- 2026-11-03 — Author ruling, AUD-077 item 2: the mirror keeps sending each case's required
  findings and critical-error IDs to Langfuse as dataset expected output, as built (option 2 of
  three; the alternatives were holding them back until the author's initial labels, or never
  sending them). Gold never reaches a model and is already public in the repo. Accepted risk:
  Langfuse shows expected output beside answers before scoring, so blind initial scoring rests on
  the author not opening Langfuse before scoring; nothing in code enforces it. No code change.
- 2026-11-03 — Acceptance evidence check at `2ef36e5` (no code change since `4c4d9b5`), on
  the author's request. Fresh runs: comparison suite 93 passed; `fixtures --check` frozen and
  current; Pyright 0 errors. Eleven criteria ticked, each on named evidence:
  - T52 match: `4c4d9b5` changed no application code or gate outside `backend/evals/comparison/`,
    tests and docs; all nine T52 record groups map to manifest/event fields in `records.py`,
    `runner.py`, `adapters.py`, `review.py`, `assessment.py` and `mirror.py`.
  - Runner modes: runner tests (72-trial schedule, rotation, calibration A/B/C, specialist refusal
    in screening, frozen manifest, fresh memory, gold isolation, no tools in screening).
  - Saved records / persistence: records tests (ordered events, torn line, redaction, artifact
    hashes, recovery marks unresolved and never repeats, unknown cost, settlement replaces) and
    runner tests (retry lineage, deadlines, partial answers, explicit linked reruns).
  - Switch and masking; local first: mirror tests (off by default and reads no keys, runner never
    touches Langfuse, every record masked, rejected/unanswered/crashed uploads kept local and
    never silently resent, mirror only posts and needs no model).
  - Labels and blinding; author as scorer: assessment and mirror tests (blinded batch, recorded
    shuffle seed, self-identification limitation, unblinded process view, numbered unrewritable
    exports, tamper detection, initial labels before assistant notes, revisions keep originals,
    batch numbers never reused); `effort` command records review time.
  - Selection reporting: assessment tests (nothing decided before completion, eligibility rule,
    single zero/critical error, unassessed critical error is unscored, linked reruns).
  - Grading rules: `fixtures.py` gold: O1-02 grading note allows full credit without an invented
    attack hypothesis; O1-09/O1-12-D reuse O1-06 anchors, required findings, forbidden claims and
    critical errors plus their own; CE-12D-1 states quotation alone is not compliance.
  - Offline tests: every listed area has a named test above; rescoring checks need no model.
  Left unticked: the mirror criterion (proven only against a fake destination; real Langfuse
  behaviour unproven, see AUD-077) and the live-result criterion, both checkpoint 3; admin
  manual/regression/review, true today but to be re-proved after checkpoint 3 adds code.
