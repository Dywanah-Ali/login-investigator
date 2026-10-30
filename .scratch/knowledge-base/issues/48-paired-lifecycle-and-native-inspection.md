# 48: Integrate updates, rollback and native graph inspection

Type: build
Status: ready-for-agent
Blocked by: 47
Blocks: 49
Phase: 0
Model: strongest (Fable 5.1 or Astra)
Rigour: Tier 3

## What to build

A separately configured application instance investigates one coherent source snapshot using
its matching PostgreSQL and Neo4j builds. The operator can prepare an update, select it for
restart, return to the previous complete version and inspect the graph in Neo4j Browser.
Saved investigations keep their original evidence through these changes.

## Decisions implemented

T46's complete-version activation/rollback, stable public contracts and native inspection
replacement for Gephi. Preserve the in-app Graph tab's planned saved-artifact behaviour;
Neo4j Browser is an operator inspection tool, not a new analyst screen.

## Checkpoint 1: coherent application startup and queries

- [ ] Present the strongest Model line and obtain/record the author's confirmation before coding.
- [ ] Open one knowledge-base context per backend process owning the PostgreSQL pool and Neo4j
      driver. Validate the chosen source snapshot, pair identity/readiness, independent graph
      integrity and serving protection before accepting requests. Close both clients after
      normal shutdown and any partial startup failure.
- [ ] All login analysis, alerts, agent log tools, graph operations and retrieval use the same
      selected snapshot. Editing working inputs does not change the published version; tampering
      with the selected snapshot or selecting mismatched stores fails closed with fixed errors.
      Preserve the existing no-build startup behaviour.
- [ ] Existing tool names, inputs, briefings, artifacts and stable IDs stay compatible. Database
      waits at asynchronous call sites run off the event loop. Test bounded timeouts, unavailable
      services, cancellation and concurrent investigations without mutable-state leakage.
- [ ] Saved investigations and original artifacts survive close/reopen and version changes
      without querying the replacement graph to reconstruct old evidence. Preserve report
      downloads. No SQLite retention or memory migration is introduced.

## Checkpoint 2: updates and rollback

- [ ] Prepare and validate a complete replacement while the old version remains selected.
      Publish a credential-free pointer only for a matching ready pair and source snapshot.
      Adopt it on a planned restart; do not add live hot-switching.
- [ ] Refuse mixed stores, missing/false completion records and changed source snapshots.
      Inject failure during build/publication and verify the previous selection is intact.
      Exercise missing PostgreSQL and graph service cases and failure after partial startup.
- [ ] Retain the previous pair plus its source snapshot. An explicit rollback restores that
      coherent version through restart, including login evidence, graph and document retrieval.
      Recovery must not erase saved investigations or overwrite the original working source files.
- [ ] Test failure cleanup and isolation from the working application, including uniquely named
      resources/state for tests and evaluations. Record limitations of local pointer atomicity;
      do not imply distributed or power-loss guarantees without evidence.
- [ ] Measure actual application restart interruption and recovery steps. Present the measured
      maintenance window for author acceptance before T49 switches the working application.
      No automatic pruning or retention policy is added; AUD-057 remains separately tracked.

## Checkpoint 3: native graph inspection

- [ ] Provide saved/tested Browser queries for the organisation and a finding's neighbourhood.
      Match the same core walk's exact node/edge identities, including device peers and
      shared-address context; independent Browser logic must not silently redefine the radius.
- [ ] Identify the connected build and source version. Verify styling and node/result limits
      so a truncated display cannot be mistaken for the full result. Use the read-only serving
      graph and document the accepted Community administrative limitation.
- [ ] Explain that passage nodes are references and Browser does not automatically fetch text
      from PostgreSQL. No GEXF file or alternative portable graph export is promised.
- [ ] Record the author's live walkthrough of organisation and finding views. Only after that
      acceptance retire the Gephi command and its format-specific tests/manual instructions.
      Preserve historical T20 evidence and the future in-app Graph tab scope.
- [ ] Update the admin manual for every adopted build, inspection, activation, rollback and
      recovery task, and test its commands exactly as written. Secrets remain outside outputs.
- [ ] Relevant safety net/type checks pass; required two-axis review is triaged. Run agreed
      eval gates for any agent-behaviour change. Record all bugs and remaining concerns.

## Boundaries and handoff

Demonstrate in a separately configured instance before T49 switches the working application.
No new API/UI scope, automatic deletion, Enterprise purchase or production deployment. T49
owns final acceptance, switching and removal of remaining obsolete NetworkX paths.

## Inputs

- [T46 ruling](46-graph-store-architecture-review.md), [T47](47-neo4j-build-and-graph-answers.md).
- [Current spec](../spec.md), [impact inventory](../research/46-impact-inventory.md).
- [Paired-build proof](../research/46-parity-and-pair-proof.md).

## Comments

- 2026-10-30 — Created using `to-tickets` after author approval. Native inspection replaces
  the initially proposed GEXF-preservation work. No code or live walkthrough completed yet.
