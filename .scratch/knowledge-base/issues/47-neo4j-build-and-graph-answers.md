# 47: Build the Neo4j graph and preserve its answers

Type: build
Status: resolved
Blocked by: 46
Blocks: 48
Phase: 0
Model: strongest (Fable 5.1 or Astra)
Rigour: Tier 3

## What to build

An isolated build command captures one source snapshot, prepares a matching PostgreSQL/Neo4j
version, verifies it and returns the existing account, group, asset, radius and dated-peer
answers through the named core operations. The working application's current build remains
available until the integration and acceptance tickets complete.

## Decisions implemented

- T46's Neo4j Community target, explicit development security limitation, data ownership and
  versioned-build design. Source files remain authoritative; PostgreSQL owns passage text,
  metadata and search data. Neo4j stores stable passage references and mention relationships.
- Keep PostgreSQL organisation reference tables for independent reconciliation and existing
  consumers. Preserve source IDs, deterministic results, snapshot permission qualification and
  the distinction between shared-address context and exposure.
- Fixed parameterised queries, named core operations and unchanged tool/result contracts.
  No application API/UI feature, free-form model query or retrieval redesign is added.

## Checkpoint 1: contain graph-specific details

- [x] Before implementation, present this ticket's Model line, obtain author confirmation and
      record the selected model under Comments. T46's confirmation does not cover this ticket.
- [x] Refactor the current graph operations behind a small core interface without changing
      their results. Establish meaningful existing-behaviour tests before replacing traversal.
      Keep framework and storage-native objects out of returned domain records.

## Checkpoint 2: build and open one isolated version

- [x] Capture immutable source inputs and a build identity/fingerprint. Build fresh PostgreSQL
      and Neo4j resources from that snapshot; do not mutate or publish the active application
      version. Pin runtime/driver versions and document only behaviours used by this ticket.
- [x] Neo4j contains organisation records, typed relationships, observation timestamps and
      passage references. It does not duplicate passage text/search metadata. Match exact
      chunk IDs and mentions to PostgreSQL, including chunks with no mentions.
- [x] Independent integrity checks derive expected identities, attributes, edges and timestamps
      from sources without using the importer's transform. Corrupt valid endpoints, attributes,
      timestamps and passage references to demonstrate refusal; counts alone cannot pass.
- [x] Writable preparation is isolated. The serving graph rejects data/schema writes and tested
      attempts to change access mode, including after restart. Builder credentials are retired
      before serving and absent from serving configuration. Explicitly retain the known Community
      administrative-access limitation; PostgreSQL keeps its restricted reader role.
- [x] A completion marker is published only after all preparation/checks succeed. Unique
      per-run databases, volumes, snapshots and state files isolate tests; failures clean only
      their own resources. Missing service prerequisites fail loudly with actionable instructions.

## Checkpoint 3: preserve complete graph answers

- [x] Account lookup accepts existing identifiers/case conventions and preserves found/not-found
      output. Group/asset walks, radius and finding walks return the same exact IDs, attributes,
      paths and ordering as the existing contracts and frozen gold.
- [x] Verify S6 independently against its frozen answer key. Include a positive device-peer
      witness, failed-login exclusions, empty devices, user-selected dates on both peer sides,
      inclusive start/exclusive end, out-of-coverage requests and snapshot permission wording.
- [x] Network waits have explicit timeouts and a defined error surface. Retain synchronous core
      graph operations for tool callers; document the off-event-loop integration required by T48.
      Each query owns its session; callers share the driver lifetime, not mutable query state.
- [x] Demonstrate the complete command-to-query path on a disposable full dataset with offline
      embeddings. Record preparation, query latency and resource measurements without inventing
      a capacity target or claiming a speed improvement over NetworkX.
- [x] Relevant backend/frontend safety checks and type checks pass; run the required two-axis
      code review and triage every finding. Any agent-behaviour change needs the agreed eval gates.
      Update and test adopted manual commands in the admin manual. Log bugs and unresolved concerns.

## Boundaries and handoff

No working-application switch, automatic old-build deletion, phase 1 features, golden-answer
changes or production deployment. The experimental scripts are evidence, not production code
to copy unreviewed. Keep the existing implementation usable until T49 accepts the replacement.
T48 consumes the verified build/core operations; T25/T27 remain blocked by T49.

## Inputs

- [T46 ruling](46-graph-store-architecture-review.md), [current spec](../spec.md).
- [Proof and its limits](../research/46-parity-and-pair-proof.md).
- [Security evidence](../research/46-community-read-only-feasibility.md).
- [Impact inventory](../research/46-impact-inventory.md).

## Comments

- 2026-10-30 — Author confirmed Astra for T47 in the session's model-confirmation prompt.
  Claimed under the implement workflow. Tests use the already approved spec door 2
  (named knowledge-base core operations and integrity/security checks) and the ticket's
  isolated build-command boundary. Existing API/tool contracts remain unchanged.

- 2026-10-30 — Created using `to-tickets` after the author's approval of the consolidated
  three-ticket design. No implementation or model confirmation for this ticket yet.

- 2026-10-30 — Neo4j Python driver 6.1.0: Context Hub `neo4j/package` and
  [official driver API](https://neo4j.com/docs/api/python-driver/current/api.html);
  checked per-call sessions, plain result consumption, connection/acquisition and query
  timeouts, explicit driver cleanup and parameterised queries. Official current docs now
  identify 6.4; the used configuration and Query APIs were also checked in installed 6.1.0
  source. Runtime remains 2026.10.1; reuse T46's same-version Community read-only/security
  documentation, with serving/restart checks rerun in T47 rather than assuming proof parity.
- 2026-10-30 — SQLAlchemy 2.1.6: Context Hub covers 2.0.50, so checked the
  [official 2.1 async reference](https://docs.sqlalchemy.org/en/21/orm/extensions/asyncio.html)
  for Core `AsyncConnection.execute`, transaction contexts and `AsyncEngine.dispose`.
  PostgreSQL access continues through the existing psycopg-backed engine.
- 2026-10-30 — Two-axis review: standards found partial-Docker-failure cleanup;
  spec found that issue plus cancellation ownership and configured-reader propagation.
  All three are being corrected and independently rechecked. B-111/B-112 retain the findings.
  B-110 records restart address refresh. Frontend first run: 149 pass, one unchanged
  Explorer interaction timeout (B-113); types clean, six existing AUD-009 lint warnings.
- 2026-10-30 — B-113 affected-file rerun passed all 8 Explorer tests without changes
  (30.53 seconds). Initial timeout remains recorded; no frontend implementation changed.
  Both reviewers rechecked fixes and report no remaining code findings; live regression
  tests and the final full safety net still determine closure.

- 2026-10-30 — Documented command passed from the repository root with `--offline --dispose`.
  Evidence: [command result](../research/47-command-result.json). Preparation 279.539 seconds;
  five account lookups, median 53.750 ms (first call 1,973.069 ms); container memory 679.8 MiB.
  Offline vectors only; no provider call, capacity claim or application switch. The command
  disposed its newly created pair. Restart binding refresh passed in this run.
- 2026-10-30 — The real-container unknown-ownership recovery test passed (1 test, 25.60 seconds).
  Configured reader separation test passed (1 test, 4.52 seconds). Both review axes confirmed
  the code fixes; final full suites are running. Baseline focused graph/agent tests passed
  38 before the seam change and 39 after it plus snapshot coverage.
- 2026-10-30 — Final full frontend rerun: 150/150 tests passed in 38.97 seconds.
  Frontend types passed. The six existing lint warnings remain: incompatible-library in
  alerts-table and explorer-table; set-state-in-effect in use-mobile; only-export-components
  in button, badge and sidebar. No frontend code changed. B-113/AUD-069 retains the first timeout.

- 2026-10-30 — Final focused graph/version suite passed all 7 tests in 709.79 seconds.
  It includes complete account/finding parity and frozen S6 gold, dated coverage, immutable
  snapshot and pair-mismatch refusal, reference-only independent corruption checks,
  positive device/failed-login/empty-device witnesses, failed embedding cleanup and real Docker
  cancellation at both preparation and sealing. The two subsequently added boundary tests
  (unknown ownership recovery and configured-reader rejection) also passed separately;
  the full suite includes all nine new tests plus the existing safety net.

- 2026-10-30 — Final safety net: **686 backend tests passed** in 786.87 seconds, with no
  teardown errors; **150 frontend tests passed**; both type checks clean. No agent prompt,
  tool result or active application behaviour changed, so no paid live agent eval was run.
  Exact new-versus-existing graph answers and existing agent tests are included in the safety net.
  `git diff --check` and staged whitespace checks pass. Model: author-confirmed Astra.

## Answer

T47 is resolved. The existing application now reaches its unchanged NetworkX operations through
`GraphQueries`. An isolated command captures read-only source files, creates a unique PostgreSQL
and Neo4j pair, independently verifies exact source records and passage references, retires graph
builder credentials, tests serving protection across restart, verifies the configured PostgreSQL
reader, and writes a credential-free completion marker. No active pointer is switched.

The Neo4j implementation returns the same complete account, group, asset, finding-walk, radius
and dated-peer results. Tests retain S6's frozen gold and positive/negative login witnesses.
Cancellation waits for resource ownership to settle; ambiguous Docker failures preserve recovery
state until cleanup can be confirmed. Graph queries have bounded sessions and fixed public errors.

Evidence: 686 backend and 150 frontend passes, clean types, the documented offline command and
[its measurements](../research/47-command-result.json), and the cleared
[two-axis review](../reviews/47-code-review-2026-10-30.md). Bugs B-108 through B-113 retain iterations.
AUD-069 records the initial Explorer timeout despite clean reruns; six AUD-009 lint warnings remain.
Community administrative access and observed runtime defaults remain under AUD-068.

T48 consumes these verified operations for paired application lifecycle, off-event-loop calling,
rollback and native inspection. T49 still gates application migration acceptance and T25/T27.
Offline versions are labelled as such and are not retrieval acceptance evidence. No production
readiness, capacity guarantee or measured application interruption is claimed.
