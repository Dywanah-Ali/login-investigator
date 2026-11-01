# 49: Verify and complete the Neo4j migration

Type: build
Status: resolved
Blocked by: 48
Blocks: 25, 27
Phase: 0
Model: strongest (Fable 5.1 or Astra)
Rigour: Tier 3

## What to build

Complete the verified transition to Neo4j in the working application, with an accepted
maintenance window and a tested route back. Remove obsolete NetworkX query/export paths
after the new behaviour is accepted, then release the held integration tickets.

## Decisions implemented

T46's approved architecture and three-ticket sequence. This gate accepts the development
deployment; it is not production readiness. T45's retrieval-design work and its T26 blocker
remain separate.

## Checkpoint 1: review the integrated evidence

- [x] Present this strongest Model line and obtain/record author confirmation before work.
- [x] T47/T48 have evidence for reference-only passage nodes, independent corruption checks,
      exact graph answers, protected serving, complete source/store identity, update/rollback,
      saved evidence, bounded failures, concurrency/cancellation and native Browser inspection.
      Unproven research assumptions cannot count as completed implementation checks.
- [x] Full backend/frontend tests, type checks and required lint checks pass; report existing
      noise explicitly. Required two-axis review findings are fixed or dispositioned with evidence.
- [x] Run the agreed live Port eval and graph/retrieval regression evidence on the candidate.
      Preserve frozen gold and acceptance thresholds. Compare graph results exactly and verify
      no new retrieval regressions; existing T45/AUD-062 gaps remain open and cannot be called
      a passing knowledge-base retrieval gate. Any changed agent behaviour must meet its gates.
- [x] Confirm native inspection replaces the Gephi operator workflow with the author's recorded
      walkthrough. No removal of the planned in-app saved-evidence Graph tab is implied.

## Checkpoint 2: switch with a tested recovery route

- [x] The author accepts measured restart interruption and the concrete switch/rollback plan
      before changing the working application's selected build. Retain the prior verified
      implementation/build/source configuration needed to return if the switch fails.
- [x] Build/validate the selected matching version and perform the planned restart. Verify an
      actual lookup/investigation, graph answer, document retrieval and reopening saved evidence
      against the intended version. Do not touch v1 or push to GitHub.
- [x] Demonstrate rollback/recovery in the agreed safe environment, record commands and elapsed
      time, and verify the same source version across all readers. Never delete the previous
      working version as a side effect of acceptance.
- [x] Remove obsolete NetworkX query/GEXF paths and the dependency if no remaining application
      use needs it; research/historical evidence stays. Re-run checks affected by that removal.
      Do not maintain two permanent graph engines or ship experimental scripts as production code.
- [x] Admin manual commands for the final state are tested as written, including prerequisites,
      failure messages, read-only serving, inspection, activation, rollback and recovery.

## Checkpoint 3: close the implementation hold

- [x] Record final architecture, versions, measurements, remaining limitations and acceptance
      evidence in this ticket, the map and AUD-067. Close AUD-067 only when the migration and
      parity evidence actually satisfy it.
- [x] Release T25/T27 through this ticket's resolved status only after all required evidence
      passes. Keep T45's T26 blocker and other unrelated parked concerns unchanged.
- [x] Keep AUD-068 open as the explicit pre-production gate covering permissions, recovery,
      availability, monitoring and cost. Record Community's retained administrative powers;
      an Enterprise installation alone does not close that gate.

## Boundaries

No production deployment, Enterprise purchase, new retention policy, evidence-store redesign,
retrieval-gap waiver or expansion beyond phases 0 and 1. Approval to create this ticket did
not start implementation or approve paid model runs beyond the project's existing rules.

## Inputs

- [T46 ruling](46-graph-store-architecture-review.md).
- [T47](47-neo4j-build-and-graph-answers.md), [T48](48-paired-lifecycle-and-native-inspection.md).
- [Current spec](../spec.md), [proof and limits](../research/46-parity-and-pair-proof.md).

## Comments

- 2026-10-30 — Created using `to-tickets` after author approval. T25/T27 explicitly wait
  for this gate; resolving the architecture decision alone cannot release them.

- 2026-10-30 — T48 resolved after the author's native Browser walkthrough and explicit acceptance.
  Gephi export command/writer/method/tests are retired; remaining NetworkX cleanup remains here.
  Native evidence and final reviews are linked from T48. The separate offline inspection pair
  is retained for the author; it is not live retrieval evidence or the selected application build.
  Maintenance-window acceptance, live migration gates and application switch remain unapproved
  and unperformed. This ticket is next, not started.

- 2026-11-01 — Author invoked the implement skill for T49 and explicitly confirmed Astra.
  Claimed on the current branch at `13f5fdd`. Tier 3 migration acceptance. Existing approved
  spec doors 2 and 4 cover core and application lifecycle checks. Working selection changes
  still require the ticket’s separate measured-plan acceptance. No paid run has started.

- 2026-11-01 — Author explicitly approved one live Port API evaluation of 21 questions,
  three runs each, and one six-question frozen knowledge-base retrieval run, using existing
  model settings. No additional paid runs are authorized by that decision. Candidate passage
  vectors will be copied from the checked existing build without embedding-provider calls.

- 2026-11-01 — Baseline checks before retirement: frontend 150 tests passed in 19.33 seconds;
  frontend and backend types pass; Ruff passes. Frontend lint exits successfully with the same
  six AUD-009 warnings. No unrelated cleanup performed.
- 2026-11-01 — Documentation reuse: Neo4j Community 2026.10.1 / Python driver 6.1.0 and
  SQLAlchemy 2.1.6 remain pinned. Reuse [T47's driver and SQLAlchemy lookup](47-neo4j-build-and-graph-answers.md)
  for parameterised reads, async Core execute and explicit disposal, and [T48's lifecycle lookup](48-paired-lifecycle-and-native-inspection.md)
  for existing verified prepare/select/restart/rollback behaviour. No new third-party API is
  introduced by the migration evidence scripts.

- 2026-11-01 — Corrected the initial retrieval-count mistake before any provider call. The
  frozen file contains eight questions, K01–K08. Author explicitly approved all eight plus the
  already approved 63 Port runs. The earlier six-question description is superseded.

- 2026-11-01 — Integrated evidence reviewed: T47 records reference-only passage ingestion,
  independent corruption checks, full account/finding/date equivalence, retired builder access
  and protected restart. T48 records coherent source/store selection, paired rollback, saved
  evidence and cancellation/concurrency cleanup. Its Browser acceptance is explicit, with
  170 organisation nodes/326 relationships and S6 55 nodes/64 relationships. Native inspection
  replaced Gephi only after that acceptance. The future in-app saved-evidence Graph tab stays.
  These are implementation records, not extrapolations from T46's proof. Current migration
  candidate parity and live gates are being measured independently below.

- 2026-11-01 — Refreshed documentation through get-api-docs: Context Hub `neo4j/package`
  6.1.0 for parameterised reads, per-operation sessions and explicit driver closure. Context
  Hub's SQLAlchemy entry is 2.0.50, so used the official
  [SQLAlchemy 2.1 async reference](https://docs.sqlalchemy.org/en/21/orm/extensions/asyncio.html)
  for the installed 2.1.6 Core connection/execute and disposal behaviour.

- 2026-11-01 — TDD at approved core door 2: the new legacy-selection refusal test is red
  against the unchanged implementation. It proves the old pointer currently reaches credential
  loading, which must be refused after engine retirement. No application code has changed yet.
  Both retained live-vector pairs passed 320 exact passage rows, 50 account answers, ten
  finding radii/walks and 40 dated radii, plus unchanged S6 gold. Preparation copied vectors
  without provider calls; the working-pointer hash is unchanged.

- 2026-11-01 — Approved live retrieval run complete: `2026-11-01-103813-673055-retrieval-7d7cff5dcc5c.json`.
  Exact comparison with the last full eight-question baseline passes for every check, graph
  result, fused top-20 ordering, kept-five ordering and first-gold rank. K01/K02/K03/K07/K08
  pass; K04/K05/K06 retain their existing failures. This is no new migration regression,
  not a passing knowledge-base retrieval gate. T45/AUD-062 and refusal-calibration work remain
  open. Seven query embeddings cost $0.00000276; seven reranks cost $0.007. Candidate vectors
  were cloned without document-embedding charges. See `research/49-retrieval-comparison.json`.

- 2026-11-01 — Approved live Port gate complete: `2026-11-01-104006-806272-13987838.json`.
  Correctness 60/63 (95.2%, target 90%); security 15/15 (100%, target 100%); no execution errors.
  Q04 fails all three Amelia-attribution checks. Full answers were reviewed; two provide
  insufficient explicit attribution/action for Amelia despite retaining S6 success facts.
  B-105 and AUD-066 record the recurrence without regrading or claiming every failure is a
  formatting defect. The paid scope is complete and no rerun is authorised. Prompt/tool
  behaviour was unchanged; its byte fingerprint reflects the preceding import cleanup.

- 2026-11-01 — Sequential measured rehearsal complete. Legacy-to-pair interruption 21.235 s,
  paired update 13.442 s, rollback 14.642 s, unavailable-graph refusal 8.839 s, recovery 59.896 s.
  Archived baseline starts in 21.861 s. Saved evidence is identical after each restart; both
  pairs pass actual lookup, S6 radius and document self-retrieval using a stored live vector.
  No provider calls were made by the rehearsal. B-126 preserves the earlier 120-second cold
  readiness failure under concurrent evaluation builds. Working selection and original memory
  remain unchanged. The author is reviewing `research/49-switch-plan.md`; acceptance pending.

- 2026-11-01 — Author explicitly accepted the measured candidate and switch/rollback plan:
  “Accept and proceed. Retire the old engine, complete checks, then activate Neo4j with both
  recovery routes retained.” This authorises retirement and the working selection change after
  final checks/reviews pass. It includes the documented cold-start caveat. No further switch
  permission is required, no additional paid run is authorised, and nothing may be pushed.

- 2026-11-01 — Retirement removes the NetworkX dependency and legacy graph/query/build paths.
  Native tests now use complete pairs and independent CSV/log expectations; frozen gold is
  unchanged. Core legacy-pointer refusal is red then green. Final Ruff and Python types pass.
  Both review axes found two operator/evidence issues, fixed and independently cleared; see
  `reviews/49-code-review-2026-11-01.md`. First focused run: nine passes, seven shared fixture
  readiness errors (B-131/AUD-072). Diagnostic retry and final operational gates are pending.

- 2026-11-01 — Focused retry passes all 15 tests in 265.92 seconds, without relaxing service
  deadlines; B-131/AUD-072 remain open as an intermittent cause-unproven observation. Exact
  offline disposable admin command passes, with 192.511 seconds preparation. A distinct source
  selected through `LI_DATASET_DIR` matches the recorded fingerprint, proving restored setting
  precedence. Its resources are disposed and the working pointer is unchanged.

- 2026-11-01 — Final operator checks reuse the retained candidate. Native inspection passes
  with organisation 170 nodes/326 relationships and S6 55/64; Browser HTTP returns 200. The
  archived recovery command runs exactly as documented, starts in 34.016 seconds and reopens
  all 25 existing investigations through their original memory file. It stops cleanly and
  leaves the working pointer unchanged. `49-native-inspection.json` and `49-manual-recovery.json`
  record these checks without provider calls. The final full backend suite is now running.

- 2026-11-01 — Complete backend run: 662 passed, one failure and one teardown error in
  874.12 seconds. B-133 records a test that still assumed the legacy pointer/one-passage fixture.
  Corrected only that test to use a small complete paired source; both review axes pass the
  delta. The known AUD-061 teardown leftover was verified idle and dropped without FORCE.
  Affected module and teardown case rerun: three passed in 209.14 seconds. Types pass.
  No application code, privileges, service limits, gold or thresholds changed for this recovery.
  This is full-run evidence plus a passing affected rerun, not a wholly clean full-suite run.

- 2026-11-01 — Final frontend run: 149 passes and the unchanged Explorer five-second timeout
  in 49.95 seconds. The affected file then passes all eight tests in 22.60 seconds without code
  or timeout changes. B-113/AUD-069 remain open. Frontend types pass; lint exits zero with six
  existing AUD-009 warnings. Backend types and Ruff pass. `research/49-verification.json` keeps
  full runs and affected reruns separate. Both review axes have zero open findings.

- 2026-11-01 — First activation attempt stopped before selection because the research harness
  lacked the backend import path (B-134). Both reviewers cleared its narrow correction. The
  guarded retry validates both retained pairs, effective default state/memory paths and the
  unchanged original pointer before selection. The normal backend starts in 28.140 seconds on
  port 8000. All 25 saved investigations and the overview match exactly. Actual account lookup,
  S6 radius and document self-retrieval pass on the intended source/version without provider
  calls. See `research/49-working-activation.json`. Both recovery routes and the walkthrough
  pair remain retained; v1 was not changed.

- 2026-11-01 — The exact documented storage-probe command passes on the active pair: 50
  fake-model lookups produce 50 identical artifacts after reopening disposable memory. Real
  memory is unchanged and no provider calls are made. Evidence: `research/49-active-storage-probe.json`.

## Answer

Neo4j Community 2026.10.1 with driver 6.1.0 now serves the working application's graph.
PostgreSQL/pgvector retains passage text, metadata, vectors and search. Every reader uses the
selected immutable source snapshot. NetworkX 3.6.1, its query/integrity implementation and the
obsolete publishing command are removed from the active application. The pinned archived
baseline retains its own environment solely for implementation recovery.

Author acceptance and the measured plan are in [49-switch-plan.md](../research/49-switch-plan.md).
The accepted candidate is `3d58516ccfe84f74ade0ee255607fe19`; retained paired rollback is
`eb6c7d59d40d4a94b87633593ae8649f`. [Activation](../research/49-working-activation.json) records
28.140-second readiness and all 25 saved investigations reopened identically. The normal backend
remains running on localhost port 8000. [Rehearsal](../research/49-lifecycle-measurements.json)
records update 13.442 seconds, rollback 14.642 seconds and stopped-graph recovery 59.896 seconds.
The exact archived recovery command also passes, reopening all existing cases in 34.016 seconds.
These are local observations, not availability guarantees.

[Verification](../research/49-verification.json) preserves the non-clean full runs and successful
affected reruns: backend 662 passes plus three affected passes after a test-only correction and
known teardown cleanup; frontend 149 passes plus eight affected passes after the known timeout.
Types and required lint checks pass, with six existing frontend warnings. [Two-axis review](../reviews/49-code-review-2026-11-01.md)
has zero remaining findings. Full/native corruption, source-derived graph answers, frozen S6,
paired lifecycle and cleanup checks remain covered. Frozen gold and thresholds are unchanged.

The approved live Port run passes 60/63 correctness and 15/15 security. All eight retrieval
results exactly match the previous baseline. K04/K05/K06 still fail their existing retrieval
checks; Q04 attribution remains AUD-066. No retrieval gate is waived and no extra paid run was made.

AUD-067 closes on this development migration evidence. T25/T27 are released through this
resolved dependency. T45 still blocks T26. AUD-068 remains the explicit production gate for
Community administrative powers, permissions, recovery, availability, monitoring and cost.
AUD-061, AUD-069 and AUD-072 retain their intermittent observations and unknown causes.
Nothing was pushed to GitHub.
