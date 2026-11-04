# 56: Retire temporary comparison integration and keep a minimal evaluation foundation

Type: design, then build
Status: resolved
Blocked by: 54
Phase: supporting foundation for later operational evaluation
Rigour: Tier 3

## Scope

Author approved this direction on 4 November 2026 and recorded it in T54. T54's upload and
visual familiarisation are now accepted. This is a separate follow-up, not more comparison
upload work. Implementation was authorised through `$implement` after scope agreement.

Scope agreed through three author choices on 4 November 2026:

1. Keep a compact summary of the shortlist, reasons and limitations. Remove detailed local
   experiment results during implementation after checking the summary. Existing hosted
   Langfuse records are outside this cleanup. Preserve decision and audit history.
2. Retain reusable basics for calling candidate models and saving answers, timing and
   reported cost. Unknown cost stays unknown. Retire the old fixed cases, scoring workflow
   and design-specific machinery where they are no longer needed by those basics. Future
   comparison cases, scoring and model roles are defined later, including possible
   two-model designs. Do not build a new comparison framework here.
3. Replace the temporary uploader in T56 with a small official Langfuse SDK foundation:
   off-by-default configuration, credentials only when enabled, destination configuration,
   outbound secret filtering, client lifecycle and shutdown. Prove it locally with a
   synthetic observation and deterministic score against a fake destination. No application
   tracing or live upload is required for this foundation.

Full operational evaluations, application instrumentation, model selection execution and
automated remote reconciliation remain outside T56. T29/T30/T31 own later operational work.

**Implementation authorised, 4 November 2026:** the author invoked `$implement` after
settling scope. This is the explicit go, including local cleanup and the requested commit.
No paid model execution, live Langfuse upload or GitHub push is included.

## Acceptance criteria

- [x] Author agrees the scope: summary only, reusable basics, locally tested SDK foundation
      in T56. Evidence: the three explicit choices recorded under Author rulings below.
- [x] Author gives the separate implementation go. Evidence: explicit `$implement` invocation.
- [x] Check the compact summary against saved results before removing detailed local results;
      record what was removed and preserve decision/audit history.
- [x] Retain and verify only the reusable model-calling and answer/timing/cost-recording basics;
      remove obsolete comparison wiring and associated tests/documentation coherently.
- [x] Retire the custom uploader; select a compatible SDK version and implement the agreed
      configuration, secret filtering and lifecycle boundary without comparison dependencies.
- [x] Local checks prove disabled mode requires no keys or network; enabled mode exports a
      synthetic observation and score to a fake destination with secrets filtered; shutdown
      releases resources. Report export failures truthfully without claiming remote receipt.
- [x] Relevant focused tests, types/lint and two-axis review pass; admin manual commands are
      updated and tested as written. No full application suites or paid model runs implied.
- [x] Leave full agent evaluation requirements/integration to later agreed operational scope.

## Comments

- 2026-11-04 — Split from T54 upon author acceptance of the familiarisation upload. Direction
  already approved; exact foundation design and implementation remain pending. No cleanup,
  dependency change, new paid run or further upload performed by opening this ticket.

- 2026-11-04 — Codex claimed the scope review at the author's request. Review below is a
  proposal, not an agreed spec change or build authorisation.
- 2026-11-04 — Langfuse Python SDK not declared in `backend/pyproject.toml`; no SDK version
  selected or installed in this review. Context Hub `langfuse/observability` covers community
  SDK 3.14.5 and is unsuitable as current implementation guidance. Checked official
  [SDK overview](https://langfuse.com/docs/observability/sdk/overview),
  [masking](https://langfuse.com/docs/observability/features/masking) and
  [batching/lifecycle](https://langfuse.com/docs/observability/features/queuing-batching):
  SDK provides tracing and lifecycle operations; current Python guidance prefers
  export-stage `mask_otel_spans`. Background export means a returned trace or a completed
  flush must not be described as verified remote acceptance. Resolve SDK/platform version
  compatibility against the selected release before implementation.

## Scope review and decisions, 4 November 2026

### Author rulings during scope questions

- 2026-11-04 — Foundation: author chose **build it in T56**, replacing the temporary
  uploader with a small, locally tested official SDK foundation. Scope agreement is
  complete. Author then explicitly instructed: wait for their go on implementation.
- 2026-11-04 — Reusable tooling: author chose **reusable basics**. Retain only the useful
  mechanisms for calling candidate models and recording answers, timing and reported
  cost, preserving unknown cost as unknown. Existing fixed cases, scoring workflow and
  design-specific machinery are not retained wholesale. Define future cases, assessment
  criteria and model roles when the final comparison is agreed, including the possibility
  of two models in an agent design. Exact extraction/removal list follows settled scope;
  no code changed during this discussion.
- 2026-11-04 — Retention: author chose **summary only**. Keep a compact summary of the
  shortlist, reasons and limitations. Detailed local experiment answers, assessments,
  request records and upload receipts are to be removed during T56 implementation after
  the summary is checked. This supersedes the full-evidence preservation recommendation
  below for local experiment results. No files deleted during scope discussion. Existing
  hosted Langfuse records are outside this local cleanup decision. Align the spec and
  final acceptance criteria with this ruling when the scope questions are settled.

### Findings

1. `backend/evals/comparison/` contains 3,319 Python source lines across fourteen files.
   Only `mirror.py` implements the Langfuse transport. The remaining files implement local
   collection, fixtures, model requests, assessment and selection. Retiring the platform
   connector does not require deleting that local evidence tooling.
2. `mirror.py` constructs OTLP spans and REST dataset/score payloads, authenticates HTTP
   requests, and maintains transfer statuses. It depends on comparison fixtures, reviews,
   assessments and `RunBundle`. It is not a general application evaluation component.
3. The comparison command module imports the mirror directly. Retirement must therefore
   address command wiring and associated tests/documentation, not just remove a file.
4. Existing application exams (`evals/run.py`, `api_runner.py`, `scoring.py` and
   `retrieval.py`) do not import the comparison package or Langfuse. They can continue
   independently. The SDK is not yet a declared project dependency.
5. T29 owns the application exam, T30 the advisory judge, and T31 application tracing and
   hosted exam integration. Historical T31 wording still says to reuse T54 machinery;
   its later comments supersede that assumption. Align operative wording when the author
   agrees this scope, while retaining the dated history.

### Initial recommendation — superseded by the agreed Scope above

Retained as discussion history only. Full-result retention, freezing all tooling and the
separate source archive below were initial proposals, not the final agreed requirements.

| Area | Proposed T56 disposition |
| --- | --- |
| Original answers, events, manifests, assessments, receipts and decisions | Preserve at existing paths. Do not alter historical IDs, hashes, timestamps or uploaded records. Ignored run bundles stay local and outside commits. |
| Local comparison runner, fixtures, request adapters, assessment/selection tools and their tests | Freeze in place as historical/ad hoc tooling. Retain import paths and evidence-reading capability. No generic extraction, new candidates, consumer repairs or promise of readiness for another comparison. Reassess against the next comparison's agreed protocol when needed. |
| Custom Langfuse transport | Retire from active comparison commands. Preserve the old source in a clearly labelled archive outside active Python modules, with the source revision and restoration context. Remove active transport and tests specific only to its retired HTTP contract; retain any checks still needed by local comparison commands. |
| New shared foundation | One small SDK setup/lifecycle module: existing off-by-default switch, credentials only when enabled, explicit destination, outbound secret filtering, controlled client lifetime and shutdown. Return/use native SDK capabilities instead of inventing a new trace/score/dataset framework. No dependency on comparison cases, gold, record schema or assessor types. |
| Proof of foundation | A local synthetic smoke path using the installed real SDK with a fake destination/exporter: one observation and one deterministic score. Verify disabled mode needs no keys or network, masking reaches exported trace data and the score payload, and shutdown releases resources. Check relevant error reporting without claiming delivery from SDK enqueue/flush alone. No application agent call. |
| Operator documentation | Replace current-comparison operating instructions with a concise historical notice and retained evidence locations. Document only the new foundation's setup and smoke command in the admin manual, testing those commands as written. Align T56/T31/spec/map references after scope agreement. |

The small score smoke test proves the selected SDK can send a saved check result. It does
not define application score names, experiment grouping or acceptance gates. Secret
filtering for trace exports does not automatically cover score/dataset API payloads;
the one score used here must be filtered explicitly. Broader payload policy belongs to
the later integration that introduces those payloads.

### Explicitly later

- Application callbacks, tool/retrieval instrumentation, Port/knowledge-base dataset upload,
  experiments, bulk result mirroring and label exports: T31 after operational scope agreement.
- Application coverage, collection/assembly/interpretation checks and existing acceptance
  gates: T29. Advisory faithfulness judging and agreement measurement: T30.
- Model challengers, another comparison or architecture calibration: their separately agreed
  protocol and execution authorisation.
- Cost-settlement repair, regrouping the old experiment, remote read-back/reconciliation,
  persistent upload queues and a general evaluation-platform abstraction: excluded here.
- A live synthetic SDK smoke upload is optional and requires an explicit scope decision;
  this proposal uses local proof and does not require another Langfuse walkthrough.

### Initial proposed completion evidence — superseded by current acceptance criteria

Author-approved scope recorded first. Then: original bundle integrity preserved; retained
comparison evidence-reading commands work without the retired connector; new disabled and
enabled SDK paths pass focused checks; relevant types/lint and two-axis review pass; admin
commands tested as written. No full application suites or paid model runs are implied.

### Current next step

T56 implemented and verified at its agreed boundaries. Application integration remains
later T29/T30/T31 scope; future model comparison still needs its own design and execution go.

- Implementation note: agreed test seams are model calling/local records and SDK setup/export/shutdown against fake destinations. Review baseline is `c9bc8e4388843e1f4ae066d36e02aaad979b55e6`. The explicitly invoked implement workflow requests one full-suite run at the end and a local commit.

- 2026-11-04 — SDK lookup: Langfuse 5.1.0 pinned; official Python reference and masking/
  batching documentation above checked for constructor injection, export-stage masking,
  native score creation and shutdown. Installed source confirms cached resources per public
  key, background score queue and separate tracing-provider shutdown. Context Hub 3.14.5
  entry remains unsuitable for implementation. No current application integration added.
- 2026-11-04 — Retention executed after checking summary against saved event/assessment
  counts and known screen cost: removed five run bundles containing 1,004 files, nine
  workflow modules, frozen fixtures and four workflow test files. Retained compact report
  at `research/54-assistant-screening-assessment-2026-11-04.md`; historical decisions and
  audit research remain. Hosted records untouched. Source remains recoverable from Git.
- 2026-11-04 — B-159 records one stale-test-reference failure after shared redaction
  extraction. Initial helper invocation also needed `PYTHONPATH=.`; no results deleted
  before its corrected verification succeeded. One file-write command used the wrong
  working-directory prefix and was corrected; no unintended files were created.

- Final focused command (as documented in admin manual): 56 passed in 3.20 seconds;
  targeted Pyright zero errors/warnings and Ruff clean. Locked dependency setup and local
  SDK smoke command both passed. The smoke reports one observation, one score batch,
  in-memory destination and no remote-delivery claim. Both independent review axes have
  zero remaining findings after corrections; see `reviews/56-code-review-2026-11-04.md`.
- Full frontend: 141 passed / 9 timeouts, 93.52 seconds. Affected four files then passed
  with one worker, 72/72 in 99.44 seconds. B-161 and AUD-028/AUD-069 retain the failed full
  result and unproven cause. Chart-dimension warnings remain. No frontend change made.

- Full backend run interrupted after 148 passes in 633.59 seconds. This is an incomplete
  suite, not a full pass. The generic implement skill was applied too broadly: T56 needs
  focused tooling checks under the project's proportional-testing rule. After the author
  questioned the graph container, the run was stopped with SIGINT. Pytest exited 130;
  Docker inventory confirmed no containers from this session remained. Five older exited
  graph containers were left untouched. No graph repair or configuration change made.
- Final SDK test after strengthening score payload assertions: 5 passed in 4.61 seconds.
  The earlier 56-test focused pass covers all affected files; final change added assertions
  only. No second full application run was attempted.

## Answer

Implemented the agreed retirement and minimal foundation. The compact T54 summary was
verified before deleting its five local run bundles. Removed fixed comparison workflow,
fixtures, scorer/selector and custom HTTP uploader. Kept model-request adapters and durable
local records, with a single-call recorder for answer/timing/reported cost. No candidates,
case schedule or multi-model design is selected by this tooling.

Langfuse 5.1.0 is pinned. The small optional SDK session provides explicit destination,
off-by-default configuration, secret filtering and cleanup. A local fake-destination smoke
check exercises a real SDK observation and score. SDK trace filtering and explicit API
payload filtering are documented separately. Existing application exams remain independent.

Evidence: 56 focused passes; final SDK assertion check 5 passes; targeted Pyright and Ruff
clean; documented setup and smoke commands tested; both review axes zero remaining findings.
B-159/B-160 retain corrected iterations. Broad verification limits are explicit: backend
interrupted at 148 passes; frontend full run 141 passes/9 timeouts, affected four files
subsequently 72/72 with one worker. B-161 and the audit register preserve the unresolved cause.

No live model execution, Langfuse upload, hosted-record deletion, or GitHub push occurred.
