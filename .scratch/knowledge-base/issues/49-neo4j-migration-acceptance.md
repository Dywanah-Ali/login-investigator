# 49: Verify and complete the Neo4j migration

Type: build
Status: ready-for-agent
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

- [ ] Present this strongest Model line and obtain/record author confirmation before work.
- [ ] T47/T48 have evidence for reference-only passage nodes, independent corruption checks,
      exact graph answers, protected serving, complete source/store identity, update/rollback,
      saved evidence, bounded failures, concurrency/cancellation and native Browser inspection.
      Unproven research assumptions cannot count as completed implementation checks.
- [ ] Full backend/frontend tests, type checks and required lint checks pass; report existing
      noise explicitly. Required two-axis review findings are fixed or dispositioned with evidence.
- [ ] Run the agreed live Port eval and graph/retrieval regression evidence on the candidate.
      Preserve frozen gold and acceptance thresholds. Compare graph results exactly and verify
      no new retrieval regressions; existing T45/AUD-062 gaps remain open and cannot be called
      a passing knowledge-base retrieval gate. Any changed agent behaviour must meet its gates.
- [ ] Confirm native inspection replaces the Gephi operator workflow with the author's recorded
      walkthrough. No removal of the planned in-app saved-evidence Graph tab is implied.

## Checkpoint 2: switch with a tested recovery route

- [ ] The author accepts measured restart interruption and the concrete switch/rollback plan
      before changing the working application's selected build. Retain the prior verified
      implementation/build/source configuration needed to return if the switch fails.
- [ ] Build/validate the selected matching version and perform the planned restart. Verify an
      actual lookup/investigation, graph answer, document retrieval and reopening saved evidence
      against the intended version. Do not touch v1 or push to GitHub.
- [ ] Demonstrate rollback/recovery in the agreed safe environment, record commands and elapsed
      time, and verify the same source version across all readers. Never delete the previous
      working version as a side effect of acceptance.
- [ ] Remove obsolete NetworkX query/GEXF paths and the dependency if no remaining application
      use needs it; research/historical evidence stays. Re-run checks affected by that removal.
      Do not maintain two permanent graph engines or ship experimental scripts as production code.
- [ ] Admin manual commands for the final state are tested as written, including prerequisites,
      failure messages, read-only serving, inspection, activation, rollback and recovery.

## Checkpoint 3: close the implementation hold

- [ ] Record final architecture, versions, measurements, remaining limitations and acceptance
      evidence in this ticket, the map and AUD-067. Close AUD-067 only when the migration and
      parity evidence actually satisfy it.
- [ ] Release T25/T27 through this ticket's resolved status only after all required evidence
      passes. Keep T45's T26 blocker and other unrelated parked concerns unchanged.
- [ ] Keep AUD-068 open as the explicit pre-production gate covering permissions, recovery,
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
