# 54: Isolated comparison runner and early Langfuse recording

Type: build
Status: claimed
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


- 2026-11-03 (author testing-policy ruling) — Author rejected full backend/frontend runs
  for every change and directed proportional testing. AGENTS.md and CLAUDE.md now require
  focused tests for affected behaviour/seams and relevant static checks for routine work;
  full app suites only for major/cross-cutting app changes or explicit request. The spec
  decisions log records this procedural change. Agent-behaviour eval thresholds remain.
  For this isolated comparison adapter, the 143 comparison tests, backend type/lint checks,
  frozen-fixture check and two-axis review are the relevant evidence. No application graph
  or UI code changed. B-149/AUD-078 remain separate and open; the failed full run is retained,
  not reclassified as passing. Diagnostic-only retry interrupted after the author challenged
  the scope; partial private diagnostics retained. No graph fix approved or built. No model
  compatibility session, screening answer or live Langfuse upload has started. This ruling
  does not authorise paid calls. Next is isolated comparison readiness and explicit execution go.
- 2026-11-03 (close for fresh session) — Diagnostic interruption completed: exit 2 after
  1025.39 s, partial evidence only. No running containers afterward. No further graph repair
  or full-suite rerun under this isolated comparison scope. Public unauthenticated catalogue
  reads returned HTTP 200 and exactly one matching approved provider endpoint for all six
  configurations; saved in `research/54-public-route-preflight.json`. No inference or keys used.
  Native output ceilings advertised: Qwen 235929, gpt-oss 117964, DeepSeek 393216, Luna/Haiku/Sol
  128000 tokens each. These are provider ceilings, not evaluation-imposed caps or proof of
  effective defaults; adapter still omits output caps. Runtime/native settings remain the
  purpose of compatibility sessions. No paid call or Langfuse upload authorised or performed.
  Next session should request one bounded execution go for the six initial compatibility
  sessions under the settled US$25 plan; do not reopen settled model/case/scoring decisions.
- 2026-11-03 (Codex offline build) — Author said "Ok lets go" after the stated next step
  of finishing adapter documentation and implementing/testing offline. Proceeding on that
  scope; paid inference and live Langfuse uploads remain unauthorised in this session.
  OpenRouter v1 documentation completed via official Responses
  [tool calling](https://openrouter.ai/docs/api_reference/responses/tool-calling),
  [error handling](https://openrouter.ai/docs/api_reference/responses/error-handling),
  [streaming](https://openrouter.ai/docs/api_reference/streaming),
  [reasoning preservation](https://openrouter.ai/docs/guides/best-practices/reasoning-tokens),
  [service tiers](https://openrouter.ai/docs/guides/features/service-tiers).
  Checked tool call IDs/output items, complete ordered reasoning replay, failed/incomplete
  results, SSE framing, explicit standard tier (`default`) and optional usage fields.
  Requests 2.34.2: official [timeouts](https://requests.readthedocs.io/en/latest/user/quickstart/#timeouts)
  explain inactivity rather than total duration, so transport needs a separate elapsed deadline.
  Context Hub lacked OpenRouter coverage as recorded below. Native adaptive-effort mapping
  and route/settings identity remain compatibility checks, not proven by these documents.
- 2026-11-03 — Codex: OpenRouter v1 [router metadata](https://openrouter.ai/docs/guides/features/router-metadata),
  official docs via web; checked `X-OpenRouter-Metadata: enabled`, selected-provider fields,
  optional pipeline/retry evidence and absent metadata on cache hits. Adapter requests and
  retains returned metadata without inferring native settings. The response-schema URL found
  in search (`docs/api/api-reference/responses/create-responses`) could not be fetched; no
  claim of reviewing that schema. Official Responses guides supply the shapes used here.
  Requests 2.34.2 [developer interface](https://requests.readthedocs.io/en/latest/api/), via
  official web docs: checked Session `trust_env`, streaming `iter_lines` decoding, redirects
  and default HTTPAdapter retries (zero). No package changes.
- 2026-11-03 (Codex offline checkpoint-3 result) — Built `openrouter.py` and `http_stream.py`
  behind the existing adapter seam. Exact credential-free wire inputs persist before dispatch;
  Responses output items replay intact; request worker enforces elapsed deadline and stops
  before retry; failures retain partials, known costs and sanitized provider artifacts.
  Standard service maps to `default`; requested providers have no fallback. Qwen/gpt-oss use
  the exact `deepinfra/bf16` routes already identified in approved T52 research, not new hosts.
  Anthropic's adaptive intent maps to unified enabled/effort; native application remains
  unverified. No evaluation-imposed output, retry or call count cap added.
  CLI live runs require explicit paid flag and bound; first-pass completion/review gates later
  screening. Related paid bundles share the US$15 pause; pauses occur between trials, so this
  is no hard billing ceiling. Explicit linked repairs can run alone. Admin manual updated;
  live examples tested using fake credentials/responses, not real dispatch.
  Comparison suite: 143 passed in 122.09 s; final compatibility-record wording check: two
  passed. Frozen fixtures current; backend Ruff clean; Pyright zero; frontend types clean.
  [Two-axis review](../reviews/54-checkpoint3-offline-review-2026-11-03.md) has zero remaining
  findings on either axis after B-148 fixes. Full regression results follow below. No paid
  request, real credential authentication, live upload, application model/agent change, exam
  gold/threshold change, commit or push. Remaining unchecked criteria stay unchecked.
- 2026-11-03 (regression attempt) — Full backend outside sandbox, `pytest -q -x`: 137 passed,
  one setup error in 392.02 s. `test_a_matching_knowledge_base_starts_the_server_as_before`
  failed at `docker image inspect neo4j:2026.10.1`, the B-147 recurrence, before the comparison
  test files. Announced and attempted the handoff's reversible retag workaround; Docker's
  image-tag API returned HTTP 500. No Docker restart/download or stored-build change.
  Full backend acceptance remains incomplete, not a comparison-code failure or pass.
  An offline fixture command also hit the sandbox's uv-cache denial; the same command with
  access to the existing cache passed. No dependency change. Frontend full/focused failures
  and the final bounded-concurrency rerun are retained below and in B-066/AUD-028.
- 2026-11-03 (final frontend/check state) — Initial full frontend 149/150 and focused Explorer
  7/8 retained the known five-second Reset timeout. Final full one-worker rerun passed 150/150
  in 277.21 s without frontend or timeout changes; chart-size warnings remain. AUD-028/AUD-069
  and B-066 retain all iterations. Final read-only Docker inspection finds the same image by
  ID and no running containers; the name repair failed as recorded above. No test process
  from this session remains. Comparison/fixture/type/lint/review checks pass; full backend
  acceptance remains incomplete at the B-147 environment failure. T54 remains claimed with
  its three live/final criteria unticked. No paid inference or live Langfuse upload authorised.
- 2026-11-03 (B-147 investigation) — Author reopened Docker troubleshooting. Read-only
  checks reproduced changing short-name resolution without a retag, plus engine-call timeouts.
  Local logs tie cached short-name 404s to the five-minute idle VM stop and show canonical-name
  lookup waking the VM. Resource Saver/cache is a hypothesis pending controlled verification.
  Desktop 4.76.0, Engine/CLI 29.5.2/API 1.54. Author confirmed no prior restart/settings change,
  then asked whether to restart. Recommended ordinary Desktop restart; waiting for author to
  confirm the engine is running before name checks and the failed test. Full details B-147.
- 2026-11-03 (post-update Docker check) — Author installed the pending Desktop update.
  Verified Desktop 4.98.0, Engine/CLI 29.9.2/API 1.56. Original image ID, short name and
  canonical name all resolve to the same existing image. The previously failing
  `test_api_startup.py::test_a_matching_knowledge_base_starts_the_server_as_before` passed
  in 225.89 s with fake embeddings and a temporary graph. Sampled container state/logs showed
  normal startup, no OOM kill and expected negative authentication check. No new retag,
  image-store switch or application setting change. Admin manual section 4 includes the
  read-only checks, tested as written. Full backend regression now running; no paid inference
  or live Langfuse upload. Immediate recovery is not an idle-cycle durability claim.
- 2026-11-03 (post-update full regression) — 149 passed, one failure in 1435.63 s. Full startup
  tests passed; Browser fixed-address rollback failed at `rollback_version` with
  `PAIR_UNCHECKABLE` (871.91 s for that call). B-149 retains this distinct observation; it is
  not yet established as AUD-072's readiness timeout. Narrow local Docker trace captured 63
  lifecycle events, zero OOM events; watcher stopped and final Docker check found no running
  containers. No image lookup recurrence. Full backend acceptance remains incomplete.
  Next is one diagnostic-only focused retry capturing suppressed exception context before
  cleanup, without altering application code, retry policy, readiness limits or public errors.
- 2026-11-03 — Codex diagnostic lookup: neo4j Python 6.1.0; Context Hub `neo4j/package`
  matches the installed pin, checked scoped sessions and exception handling. Official
  [API exception reference](https://neo4j.com/docs/api/python-driver/current/api.html)
  is rolling 6.4; consulted only the longstanding exception code/driver-error fields.
  Diagnostic wrapper will use Python exception context and selected non-secret fields,
  not change driver execution or add retries. The comparison's paid execution remains gated.
- 2026-11-03 (Codex checkpoint-3 intake) — Author confirmed GPT-6.1 Sol for this session
  and confirmed this session is the sole editor. OpenRouter key presence checked without
  displaying its value; author reports sufficient account credit. Author created the
  `login-investigator-v2` Langfuse project and saved its public key, secret key and base URL
  in ignored `backend/.env`; all three have values, not yet authenticated. `LI_LANGFUSE`
  is not on. Author reconfirmed US$25 planning budget, reviews at US$15 and after 24 results.
  No paid OpenRouter call or live Langfuse upload is authorised until a separate explicit
  execution go in this session. Documentation checks and offline adapter/fake tests are allowed.
  Startup inspection found B-147 recurring: image-name lookup fails while image-ID lookup
  succeeds; no repair performed. No paid adapter implemented during intake.
- 2026-11-03 — Codex: OpenRouter HTTP API v1 (existing requests lock 2.34.2);
  get-api-docs lookup: Context Hub search for `openrouter` returned no entries, so opened
  official [Responses overview](https://openrouter.ai/docs/api_reference/responses/overview),
  [provider routing](https://openrouter.ai/docs/guides/routing/provider-selection) and
  [reasoning](https://openrouter.ai/docs/guides/best-practices/reasoning-tokens).
  Checked: stateless full-history requests, rejection of store:true/previous_response_id,
  provider-only routing with fallbacks disabled and require_parameters, reasoning settings
  and billed incomplete outputs. Initial overview/tool-calling URLs with `api-reference`
  failed; the overview resolved via the official routing page to `api_reference`.
  This is an initial documentation check, not adapter/runtime compatibility evidence;
  detailed tool-continuation, usage and deadline documentation remains before implementation.
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

- 2026-11-03 — Codex: author explicitly authorised the six paid compatibility sessions
  with “Ok lets go” after the bounded next-step request. Screening and live Langfuse
  upload remain separate gates. Existing provider/settings/budget approvals retained.
  Frozen fixtures checked current; live bundle created at
  `backend/evals/comparison/runs/compat-live`. Execute one slot at a time and inspect
  saved tool/output/identity/settings/cost evidence before proceeding.

- 2026-11-03 — Codex: six authorised initial paid sessions completed in `compat-live`, one
  slot at a time. All six tool round trips passed; five output contracts passed. gpt-oss
  returned correct fact 7 with `【CMP-1】` instead of the explicitly requested `[CMP-1]`.
  Original failure retained as B-150/AUD-079; no favourable rerun or check/prompt change.
  Fourteen requests, two rate-limit retries recovered, known cost US$0.001584 and two
  unknown-cost HTTP 429 responses. Provider identities/returned settings recorded with
  native-mapping limitations. All 64 artifact references verified; fourteen requests closed;
  six full output replays checked; configured credentials absent from saved bundle.
  See [live report](../research/54-live-compatibility-2026-11-03.md). Admin compatibility
  commands now have live evidence. No application suites repeated. No screening or live
  Langfuse upload authorised/performed; review readiness gaps before the next execution go.

- 2026-11-03 — Codex readiness repair plan: author asked to resolve the reported readiness
  gaps. Preserve `compat-live`; clarify ordinary ASCII citation delimiters in the shared
  connection-check prompt only, without changing the literal check, scored role prompts,
  cases, rubric or requested model settings. Capture OpenRouter's documented upstream debug
  body locally on tool-bearing compatibility requests. Repeat all six configurations once
  in a separately versioned bundle because the connection-check setup is shared; link it
  to the originals and include original costs. This is a bounded compatibility repair,
  not screening authorisation or repeated attempts to select a favourable answer.
- 2026-11-03 — Documentation: Context Hub search `openrouter` returned no entries.
  OpenRouter API v1 official [OpenAPI schema](https://openrouter.ai/openapi.json), fetched
  to a temporary file: checked ResponsesRequest.debug, ChatDebugOptions.echo_upstream_body
  and DebugEvent.debug.echo_upstream_body. The upstream body appears in an initial stream
  chunk. Official [reasoning mapping](https://openrouter.ai/docs/guides/best-practices/reasoning-tokens)
  and [pricing](https://openrouter.ai/pricing) reviewed via web: native Claude adaptive
  intent, reasoning preservation, and failed-attempt model-token billing. Actual transformed
  requests remain to be checked. Requests 2.34.2 transport documentation from the earlier
  checkpoint-3 note still applies; transport implementation is unchanged. Official OpenAI
  [reasoning](https://developers.openai.com/api/docs/guides/reasoning),
  [Luna](https://developers.openai.com/api/docs/models/gpt-6-luna) and
  [Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol) reviewed for native medium
  effort/standard mode/Responses tool support. Owner docs for
  [Haiku](https://platform.claude.com/docs/en/models/haiku-5-5/overview),
  [Qwen](https://huggingface.co/Qwen/Qwen3.8-27B) and
  [DeepSeek](https://api-docs.deepseek.com/guides/thinking_mode/) reviewed for matching
  controls. The generated SDK/reference URLs returned 404 on direct opening; the public
  OpenAPI schema supplies the diagnostic contract instead. No dependency change.
- 2026-11-03 — Additional provider documentation: DeepInfra's official
  [reasoning contract](https://docs.deepinfra.com/chat/reasoning) accepts the `reasoning`
  object as an alternative to `reasoning_effort`, with equivalent effort values. Its
  [chat reference](https://docs.deepinfra.com/api-reference/chat-completions/openai-chat-completions)
  and [overview](https://docs.deepinfra.com/chat/overview) confirm the field and describe
  standard service when the tier is omitted. This matches the transformed Qwen/gpt-oss/
  DeepSeek requests; it is not a request for new providers or settings.

- 2026-11-03 — Codex readiness result: `compat-readiness-1` completes all six tool/citation
  contracts under one shared clarified prompt (`28b2667c34b4`) and adapter v2. Twelve upstream
  bodies confirm native fields, including Haiku adaptive/medium, Qwen sampling and DeepInfra
  reasoning controls. B-151 records downstream limits hidden by normalized null fields.
  Seventy-five focused tests passed in 39.79 s; focused Pyright clean; focused Ruff initially
  found a test import-layout issue, corrected and rerun clean. Live evidence: 62 artifact
  references hash-checked, thirteen requests terminal, six fresh memory IDs, six exact ordered
  output replays and twelve upstream bodies verified, configured credentials absent.
  Known repair charge US$0.001556; combined US$0.003140. Three combined engine_overloaded
  HTTP 429 rejections classified under published nonbilling policy in append-only notes.
  Raw missing costs remain unknown; no invented measured zero or account reconciliation.
  Original failed gpt-oss answer retained; no scored role prompt/check/gold/config change.
  [Resolution report](../research/54-readiness-resolution-2026-11-03.md) and linked JSON
  record the evidence. Admin instructions updated and compatibility commands live-tested.
  `screen-live` created with 72 frozen slots and zero request events, ready for a separate
  first-24 paid execution go. No screening, labels, selection or live Langfuse upload occurred.
  AUD-079 ready for author review; T54 remains claimed. No graph/application-suite detour.

- 2026-11-03 — Author approved the first 24 paid screening answers after readiness resolution,
  with an inspection after the first answer. Approval: “Approved. go ahead”. Use both
  compatibility bundles in cost context; stop after slot 24 for the setup checkpoint.
  This authorises neither later passes nor a live Langfuse upload. No settings, cases,
  rubric or scored prompts change. Author remains the initial blinded scorer.

- 2026-11-03 — Billing lookup documentation: OpenRouter API v1 official
  [generation metadata](https://openrouter.ai/docs/api/api-reference/generations/get-generation),
  opened via web. Checked authenticated GET `/api/v1/generation?id=...`, generation identity,
  `total_cost`, cancellation and finish fields. Context Hub’s lack of OpenRouter coverage
  and the existing Requests 2.34.2 documentation still apply. A read-only lookup for the
  first screening timeout returned HTTP 200 and a reported charge; no inference repeated.
  Save its settlement after the live runner stops to avoid concurrent bundle writers.

- 2026-11-03 — First paid screening round finished: 24 final answers, six per case,
  no manually scheduled reruns, and no slot after 24 started. Wall time 1162.393 s.
  First-answer setup inspection passed before continuation. All case inputs/prompts/pins/
  settings and source hashes match; 24 fresh memory IDs; 151 artifact references checked;
  configured secrets absent. Twenty-seven request records are terminal: 24 completed,
  two upstream 429 capacity errors and one elapsed timeout, all three recovered by policy.
  Timeout charge US$0.000426477 obtained by authenticated generation metadata and attached
  once after the runner stopped. Known screen cost US$0.107868; combined US$0.111008.
  Five rejection charges across all paid bundles remain numerically unknown with policy
  dispositions; no invoice total claimed. B-152 records the operational evidence.
  No application suites or inference reruns for billing/checks.
- 2026-11-03 — Setup checkpoint found B-153/AUD-080: one answer uses spaced/grouped/ranged
  citations that the version-1 parser ignores. Offline `[ D999 ]` and `[D1; D999]` also
  evade resolution while `[D999]` is detected. All recognized references resolve, but
  coverage is incomplete. Original checks/outputs preserved; no parser, prompt, gold,
  rubric or human score changed. New check version and local recheck proposed, not built.
  First blinded batch has six answers, no detected identity mentions and blank labels.
  [Checkpoint](../research/54-first24-setup-checkpoint-2026-11-03.md) and linked JSON retain
  evidence. Two rounds remain, 48 answers; all human scores are unscored. No selection
  or live Langfuse upload. Author asked to finish records and continue in a fresh session.
  T54 stays claimed; pick up with parser coverage before a separate later-pass go.

- 2026-11-03 — Author approved the proposed bounded B-153 parser repair and offline
  recheck. Plan: reference-resolution/2 accepts whitespace, comma/semicolon groups and
  ascending same-prefix ranges with full endpoints, using ASCII hyphen, Unicode hyphen,
  nonbreaking hyphen, en dash or minus. Keep explicit unknown references visible even
  inside unsupported groups; report unsupported reference-like brackets separately. Bound
  range expansion to 1000 references and report larger, reversed, mixed-prefix or padded
  ranges as unsupported rather than silently accepting them. Preserve original answers and
  v1 checks; append v2 checks only. Focused assessment/dependency tests and type/lint checks,
  then offline recheck of the 24 saved answers. No third-party API/library changes, paid
  inference, prompt/rubric/gold/score changes or live uploads. T54 remains claimed.

- 2026-11-03 — B-153 bounded repair verified: `reference-resolution/2` plus visible local
  command warnings. All 55 current assessment tests covered by the 53-test file run and
  focused follow-ups (two updated/new tests, then one command test); focused Ruff/Pyright
  clean. One import-order lint iteration corrected. Offline recheck appended 24 v2 events;
  all 24 v1 checks, original 135 events and 152 other bundle files unchanged. Recheck is
  idempotent. Thirteen answers gain recognized references; former zero-count answer now
  has 37 occurrences; zero unresolved references. Two answers retain five unsupported
  status-reference brackets with explanatory prose, explicit refs checked, no score implied.
  [Checkpoint addendum](../research/54-first24-setup-checkpoint-2026-11-03.md) and
  [v2 evidence](../research/54-citation-parser-v2-evidence.json) record grammar, tests,
  limits and source hash change. Frozen manifest preserved; disclose parser/command-only
  package hash change at later setup review. Admin live command tested. No paid run,
  prompt/rubric/gold/answer/score change or live upload. AUD-080 awaits author checkpoint
  disposition; T54 remains claimed. Two paid rounds (48 answers) still need separate go.

- 2026-11-03 — Author explicitly authorised the remaining 48 paid screening answers after
  the parser-repair summary, retained two syntax warnings, and clarification that the 48
  still awaited explicit go. First-24 setup checkpoint disposed to proceed with these
  warnings retained; no scoring implication. Scope: resume original slots 25–72 in
  `screen-live`, both compatibility bundles included in cost context, unchanged model
  settings/prompts/cases/rubric/retries/limits, `--after-setup-review`, no spending-review
  override. Check-only package source change is recorded by the v2 evidence and verified
  at preflight; frozen manifest retained. No linked reruns or live Langfuse upload approved.
  AUD-080 closes for the bounded parser repair and this checkpoint disposition, without
  universal grammar, entailment or answer-quality claims. Record final execution evidence
  after the runner stops; author remains initial blinded scorer. T54 stays claimed.

- 2026-11-03 — Author requested stopping after round 3 and its housekeeping, with a fresh
  session next. Clarification confirmed “round 4” means blinded human scoring, following
  the agreed three-round screen. Finish paid slots through 72, reconcile available billing,
  locally check saved evidence/citations, update records and write the fixed session handoff.
  Stop before human scoring, model selection or live Langfuse upload. No extra paid round.

- 2026-11-03 — Billing reconciliation documentation reuse: OpenRouter API v1 and Requests
  2.34.2; reuse the official generation-metadata and Requests timeout/developer-interface
  documentation checked in this ticket earlier today. Same authenticated GET
  `/api/v1/generation?id=...`, same generation identity / total_cost / finish / cancellation
  fields, unchanged installed Requests and transport semantics. Context Hub's previously
  documented lack of OpenRouter coverage still applies. Read-only lookup after runner
  exit; no inference replay. Preserve streamed-usage unknowns independently of receipts.

- 2026-11-03 — Original screening collection complete. Authorised slots 25–72 ran with
  both compatibility cost contexts and setup-review confirmation; no spending override.
  Exit 0: all 72 original trials closed, 71 answers and one `no_answer` (slot 64;
  B-155/AUD-081). Later-round elapsed 2847.102 s. Total screen requests 96, 24 retries:
  72 completed transports, 20 HTTP 429, one streamed rate-limit error and three timeouts.
  Rounds 2–3 added 18 HTTP 429, one streamed failure and two timeouts. Two new timeout
  charges US$0.002126992 / US$0.001812412 settled once from authenticated receipts;
  both native metadata cancelled true, finish fields null. Two other generation lookups
  returned 404 (empty response / streamed failure); costs unknown. Screen known
  US$0.278057, combined US$0.281197; 22 screen / 25 combined numeric charges unknown.
  Streamed usage remains unknown for 25 screen requests. No invoice-total claim.
- 2026-11-03 — Final local checks: 47 new v2 checks, 71 total; zero unresolved refs;
  eight answers retain unsupported syntax warnings, without scores. All 485 event
  artifact references verified; 159-event original prefix and all 152 original files
  preserved; 72 fresh memories; every request matches frozen input/prompt/pins/settings.
  No linked rerun, label, assistant note, selection or live upload. Batch 1 and labels
  unchanged. [Checkpoint completion addendum](../research/54-first24-setup-checkpoint-2026-11-03.md)
  and [final evidence](../research/54-complete-screen-evidence.json) retain evidence.
  B-154 records the corrected continuation example, live-tested. Initial cache permission
  startup failed before dispatch, then authorised execution succeeded. Temporary monitor
  import-path issue corrected with PYTHONPATH; no application code/test-suite detour.
  Author-requested stop: handoff then fresh-session blinded human scoring. T54 claimed.

- 2026-11-03 — Author requested committing all current work locally. Reviewed/staged all
  33 changed/new repository files; configured-secret/key-like/home-path scan clear;
  secrets, paid run bundles and handoff remain ignored. Git identity uses handle/noreply.
  Staged whitespace check newly includes the previously untracked raw Docker event log:
  it reports the log's original trailing spaces. Preserve this diagnostic evidence exactly;
  all other staged files pass the whitespace check. No application change/test rerun for
  this commit-only action, no push. Existing quality/billing gaps remain in their records.
