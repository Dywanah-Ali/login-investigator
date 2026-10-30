# T46: graph parity and matching-build proof

Date: 2026-10-30. Disposable research only; no application migration or engine ruling.

## Result

The candidate preserved the current graph and named-query answers on the tested datasets.
A small publication coordinator accepted matching PostgreSQL/Neo4j builds, refused mixed
or incomplete pairs, and returned to a retained previous pair. A fresh graph rebuilt from
retained PostgreSQL records plus source login observations passed the same parity checks.

This establishes feasibility for these boundaries. It does not make the candidate a supported
application adapter, production deployment or capacity benchmark.

## Reproduction and evidence

From the repository root, with Docker and the configured local PostgreSQL server running:

```sh
uv run --project backend --frozen --with neo4j==6.1.0 .scratch/knowledge-base/research/46-parity-pair-probe.py
```

Expected-failure cleanup check, same directory and prerequisites:

```sh
uv run --project backend --frozen --with neo4j==6.1.0 .scratch/knowledge-base/research/46-parity-pair-probe.py --fail-after-pg
```

The second command intentionally exits 1 after creating a fresh PostgreSQL build, before
graph creation or publication. Its `finally` block removes that database and temporary files.
These are research commands, not adopted admin procedures.

- [Candidate queries and importer](t46_graph_candidate.py).
- [Probe orchestration](46-parity-pair-probe.py).
- [Successful run ff605c4bbc](46-parity-pair-result-ff605c4bbc.json): 38 named checks, exit 0.
- [Injected failure ac601a07d9](46-parity-pair-result-ac601a07d9.json): no published pair,
  expected exit 1, cleanup successful.
- [Earlier security proof](46-community-read-only-feasibility.md#subsequent-live-evidence-30-october-2026).
- [Migration impact inventory](46-impact-inventory.md).

Runtime: Neo4j Community 2026.10.1; Python driver 6.1.0; psycopg 3.3.6; existing NetworkX
3.6.1; Docker engine 29.5.2; Intel macOS 15.7.8. Existing PostgreSQL setup and application
builder were reused only for fresh `li_test_*` databases. Embeddings were deterministic
fake vectors. No retrieval-quality or paid model evaluation was performed.

## What was compared

The candidate importer independently reads PostgreSQL rows and the login CSV. It does not
import the NetworkX output. It retains all existing organisation and chunk nodes, source IDs,
typed edges and observation times. For this experiment, node attributes and chunk metadata
are also stored as JSON payloads to preserve the exact current response shape; this is not
a final Neo4j schema decision. Lookup fields and relationship times are directly queryable.

The query candidate uses fixed parameterised Cypher for memberships, granted assets and
dated peer relationships. It reuses existing result dataclasses and date normalisation.
Relationship traversal and filtering run in Neo4j. It does not give expected NetworkX
paths to the candidate query. Frozen S6 gold supplies an additional independent check.

| Dataset | Nodes | Edges | Checks |
|---|---:|---:|---|
| Original default | 490 | 583 | Exact node attributes and edges; 53 lookups including case/ID/not-found cases; all 10 detected findings' full radius results; four date/coverage windows; S6 frozen gold |
| Disposable variant | 490 | 584 | Same parity checks, plus a planted shared-device witness, failed-login and empty-device exclusions, and two half-open date-boundary cases |
| Rebuilt original | 490 | 583 | Repeated original parity and frozen-gold checks after reconstructing a new graph |

The variant copies the source folder and appends five synthetic login observations. It never
changes the original dataset or frozen gold. It tests a case absent from S6's empty device-peer
set. Shared-address matches remain context, separate from exposed accounts. Comparisons include
paths, attributes, observation timestamps and coverage wording, rather than counts alone.

## Handoff, pairing and recovery

| Question | Evidence | Limit |
|---|---|---|
| Separate writable preparation | Each graph has a unique volume and private localhost endpoint. After import, a serving identity is created, the builder identity is removed, and the writable container is stopped before the read-only serving container starts. Retired builder login is rejected; serving container environment lacks its password. | Community serving identity retains administrative powers, as explicitly accepted. This is credential retirement and instance/configuration separation, not role-based least privilege. |
| No writable published graph | Only the ready read-only instance can enter the experiment's active-pair pointer. Post-handoff graph writes are rejected. | No application process consumes this pointer yet; request-drain/restart behaviour is not implemented. |
| Shared build identity | PostgreSQL marker and Neo4j Build node must agree with expected build ID and source fingerprint; PostgreSQL's existing build fingerprint is checked too. | Markers are not independent protection against malicious modification. Full graph read-back was checked separately before serving. |
| Reject mismatched versions | B's PostgreSQL database paired with A's graph is refused. Previous active pointer remains byte-for-byte unchanged. | Tested two versions, not arbitrary distributed failures. |
| Refuse incomplete build | A false PostgreSQL completion marker prevents B's publication and preserves A's pointer. | This is explicit incomplete-state injection, not a power loss or forced process kill. |
| Activation and rollback | Publish B only after validation, then explicitly return to retained A. Pointer is changed by one file replacement. | This is local atomic publication, not a distributed transaction or a proven crash-durable deployment protocol. |
| Connection failure | Stopping B's graph makes validation refuse that pair; A remains selected. | Does not exercise an application request losing its connection midway through a query. |
| Recovery | Build a fresh A graph from A's retained PostgreSQL data plus login source, validate and activate it, repeat all original parity checks. | Demonstrates rebuildability, not backup/restore of irreplaceable data or recovery after losing both stores and source files. |
| Isolation and cleanup | Three graph volumes/containers and two PostgreSQL databases in the main run; a third PostgreSQL database in the injected-failure run. Unique names, no active-state publication, cleanup on success and injected exception. | Concurrent application load and simultaneous probe invocations were not measured. |

Independent post-run verification found all three PostgreSQL databases absent, no labelled
probe containers remaining and both temporary directories removed. Container/volume deletion
commands succeeded. Credentials were temporary `.env` files or in-process values and were not
included in output. Docker Desktop and the downloaded image remain available. Application
files, dependency manifests and active build state were not modified. Original dataset
fingerprint was checked unchanged. No full application tests or agent evaluations were run.

## Measurements and their meaning

| Measurement | Observed |
|---|---:|
| Original PostgreSQL build with fake embeddings | 6.391 seconds |
| Original graph import, after server startup | 4.318 seconds |
| Original graph preparation and handoff, including two startups | 50.145 seconds |
| Warm S6 median, original NetworkX, 10 samples | 7.803 milliseconds |
| Warm S6 median, original candidate, 10 samples | 97.517 milliseconds |
| Rebuild plus reactivation and parity/benchmark validation | 59.929 seconds |
| Serving-container memory snapshots | 714.4 MiB and 705.1 MiB |

The candidate is unoptimised and makes multiple network queries per radius. These measurements
show extra overhead on today's small graph; they do not justify a speed claim for migration.
Container memory is a point-in-time sample, excludes host Docker/PostgreSQL overhead and is
not a measured minimum requirement. Two stores add service management, credentials, failure
modes and version-pairing work. Retaining old and new graphs during preparation also needs
temporary extra resources.

The roughly 60-second recovery measurement includes proof validation; it is **not measured
analyst downtime**. An application cutover/restart test is still needed before agreeing a
maintenance-window limit. No workload size, concurrency capacity, availability target or
production operating budget has been inferred from these synthetic results.

## Remaining before a migration decision/build

- Decide final record ownership, chunk representation, synchronous/asynchronous query boundary,
  export handling and publication lifecycle using the impact inventory.
- Preserve independent corruption detection, fixed public errors and saved evidence in actual
  integration tests. The experiment is not a substitute for the application's safety net.
- Carry production permissions, availability, backup/recovery, monitoring and cost into a
  separate production-readiness gate. Community administrative powers remain a known limitation.
- Obtain the author's engine ruling and review a `to-tickets` breakdown before migration work.
  T25/T27 remain held. T45's retrieval-candidate gap is unaffected.

Iteration: first invocation failed before resource creation because the backend import root
was absent. B-107 records the correction and successful rerun. No further failures occurred
in the successful run; the later injected failure was deliberate.
