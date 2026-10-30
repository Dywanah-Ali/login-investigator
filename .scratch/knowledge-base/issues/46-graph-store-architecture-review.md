# 46: Graph foundation: NetworkX or Neo4j Community with PostgreSQL

Type: research, then prototype, then grilling
Status: resolved
Blocked by: none
Blocks: 47; T25/T27 now wait for migration acceptance in T49
Phase: 0
Model: strongest (Fable 5.1 or Astra)
Rigour: Tier 3

## Question

Should Neo4j Community replace NetworkX for graph storage and queries while PostgreSQL with
pgvector keeps document retrieval, or should the current architecture remain?

The author approved opening this decision ticket on 30 October 2026 after questioning whether
T02's small, bounded graph assumption still fits the application's intended direction. This is
a serious application build, not throwaway work. Ticket count is not a graph-capacity measure;
the decision must address query needs, operating safeguards and maintainability.

T02 remains resolved as the historical decision. The author approved the replacement ruling
and revised spec on 30 October 2026. This ticket delivers the decision and scoped build tickets;
implementation is separate and has not started.

## Scope

Compare two concrete shapes:

1. Current PostgreSQL/pgvector plus a checked NetworkX graph loaded at startup.
2. Neo4j Community for relationships and graph queries, with PostgreSQL/pgvector retaining
   chunks, embeddings and keyword retrieval. Decide which records are copied into the graph,
   how chunk/entity identifiers join the stores, and who owns each representation.

First agree the intended direction with the author: expected graph questions, dataset growth,
concurrent use, rebuild frequency, acceptable downtime and operating budget. Unknown quantities
stay unknown until agreed or measured. History, attack paths and GRC inform the choice but do
not become new phase 0/1 deliverables.

Research the exact Community release, its licence and platform requirements using Perplexity
and primary documentation. Do not substitute Neo4j Desktop's Enterprise developer features or
paid service features. Follow `get-api-docs` before writing any experiment against a library.
Reassess the installed Intel Mac's compatibility rather than assuming a supported package.

## Disposable proof to agree before execution

Use synthetic inputs and isolated resources. Keep experiment code and results under this
initiative's research directory; do not change application code or the active knowledge build.
Record exact versions, commands, resource names, results and cleanup. No paid services, live
data or active-database changes are part of this ticket's proof.

| Question | Required evidence |
|---|---|
| Can serving access be enforced as read-only? | Read succeeds with application credentials. Direct attempts to create, change and delete graph data fail at the database boundary. Check whether the same credentials can undo the restriction, invoke mutating procedures or perform administrative changes. Test restart persistence. A read-routing hint or a promise in tool code is insufficient. Under the author's 30 October development-stage ruling, retained administrative capabilities are recorded as an accepted limitation for this evaluation, not a failed development gate; graph-data write prevention must still be proved. |
| Can the builder remain separate? | Demonstrate how a writable build is produced and handed to the serving process without exposing builder credentials or a writable serving window. Database-wide read-only serving is only a candidate; assess its differences from the required reader role explicitly. |
| Are the graph answers preserved? | Compare account lookup, group/asset paths and S6 blast radius with existing ground truth and NetworkX results. Include dated device peers and address-reuse context, preserving the distinction between shared addresses and exposure. Compare identifiers and paths, not just counts. |
| Can two stores describe the same world? | A shared dataset/build identity is verified before serving. Deliberately mix builds and interrupt one side of a rebuild; the candidate must refuse the mismatched pair. Demonstrate controlled activation and return to the previous matching pair. |
| Are tests and evaluations isolated? | Run a disposable build/query cycle without changing the active graph or PostgreSQL database. Show failed-run cleanup and a repeatable way to isolate concurrent runs if proposed. |
| Can we recover? | Rebuild or restore the disposable graph and verify its answers and matching PostgreSQL build. Record downtime, required source artifacts and manual steps; distinguish rebuildability from backup of irreplaceable data. |

Measure graph preparation/import time, representative query latency and resource use. Report
the dataset size and test conditions. Do not invent a capacity target or infer production
capacity from the synthetic dataset. Include the operating cost of two services and connection
failure handling, not just query syntax.

## Acceptance criteria

- [x] Before substantive research or the proof, tell the author the Model line, obtain model
      confirmation, and record it in Comments. Ticket drafting is not model confirmation.
- [x] The author agrees the target requirements and bounded proof scope before execution.
- [x] A cited comparison distinguishes verified Community features, limitations and unanswered
      questions. Existing planning concerns are rechecked rather than repeated as current facts.
- [x] Each proof question above has reproducible evidence or an explicit failed/unproven result.
      A failed security gate is a valid decision result, not permission to relax the requirement.
- [x] An impact inventory covers build/integrity checks, startup, named core functions, tools,
      stable evidence IDs, saved artifacts, citation resolution, graph projection/GEXF, tests,
      evaluation fixtures, deployment and admin tasks. Preserve the existing public contracts
      where possible; identify any unavoidable change for author review.
- [x] The author rules keep, migrate, or defer with a concrete unresolved condition. Record the
      rationale, tradeoffs, evidence and reconsideration triggers under Answer.
- [x] If migration is chosen, propose affected spec changes first, obtain the author's ruling,
      update the decisions log, and create sequenced migration tickets with rollback and parity
      gates. Add those blockers to T25/T27 before closing this ticket so a decision alone cannot
      accidentally resume builds against the old foundation.
- Not applicable: keep/defer was not selected. Migration acceptance in T49 owns the continuing hold.
- [x] Update the map and AUD-067 with the ruling. Any new manual operating task belongs in the
      admin manual and its commands must be tested as written before that task is adopted.

## Boundaries

- No model-written Cypher, autonomous graph writes or altered agent judgement policy.
- Beyond the explicitly approved migration and native-inspection replacement, no change to
  phase 0/1 acceptance, frozen gold answers, report/evidence persistence or SQLite memory.
  Storage growth (AUD-065) and compound retrieval (T45/AUD-062) remain separate concerns.
- No application migration until the architecture and resulting implementation scope are agreed.
- T45 may continue independent research; its existing block on T26 remains. T46 is the author's
  next priority, ahead of T45, while graph-dependent implementation waits.

## Inputs

- [T02 decision](02-store-and-retrieval-provider.md) and
  [planning research](../research/02-store-and-retrieval-provider.md).
- [Current spec](../spec.md): The store and the build; The graph; Testing Decisions.
- [T19](19-graph-integrity-and-radius.md), [T20's export](20-gephi-export.md), and
  [T24](24-first-agent-tool-lookup-account.md): current contracts and acceptance evidence.
- [GraphRAG deployment research](../research/graphrag-team-adoption-2026-10-30.md): examples,
  not a market-share ranking or proof of free-edition suitability.
- [Principles](../../../PRINCIPLES.md) and
  [AUD-067](../../../docs/audit/improvement-register.md#aud-067-graph-foundation-review).

## Answer

1. **Target architecture selected, 30 October 2026:** author chose Neo4j Community for graph
   queries with PostgreSQL/pgvector retained for document retrieval, subject to an agreed
   migration design and reviewed build tickets. The purpose is the intended relationship-query
   direction, not a current speed improvement. The proof preserves tested answers and supports
   paired activation/rollback; it also measures additional query/service overhead. Community's
   administrative capabilities remain an accepted development-stage limitation with a separate
   production-readiness gate. The author subsequently approved the design and T47–T49 below.
   Each implementation ticket starts separately under its model-confirmation rule. T25/T27
   remain held by T49 until migration acceptance; publishing tickets does not start coding.

2. **Passage ownership agreed, 30 October 2026:** PostgreSQL owns passage text and search
   data. Neo4j holds relationships and stable passage references, including mention links.
   The author accepted this split after the library/map explanation. The initial proposal to
   join stores for GEXF export was superseded by native inspection in ruling 4 below. The
   disposable proof's full JSON passage copies in Neo4j are not the selected implementation:
   reference-only ingestion and independent integrity need migration acceptance tests. Source
   files remain authoritative. No retrieval-quality change or frozen-gold change is approved.

3. **Update and rollback lifecycle agreed, 30 October 2026:** prepare and verify a complete
   replacement PostgreSQL/Neo4j pair before selecting it. Adopt the replacement during a
   planned application restart, preserving startup refusal on an uncheckable or mismatched
   pair. Retain the previous pair and its matching source snapshot for explicit rollback.
   Rollback selects the complete prior version and restarts; it must not mix old stores with
   newer login records or documents. Saved investigations and their evidence remain separate
   and must survive the switch. Actual interruption must be measured during integration.
   No live hot-switching or automatic old-build deletion is approved.

4. **Native inspection and consolidated build sequence approved, 30 October 2026:** replace
   the Gephi operator workflow with tested Neo4j Browser views, build identification, display
   limit checks and the author's live walkthrough. Retire GEXF-specific code only after this
   replacement is accepted; preserve historical T20 evidence. The future in-app Graph tab still
   uses saved artifacts and is not replaced by Browser. The author reduced six proposed tickets
   to three and explicitly approved publishing the revised design and sequence:
   [47 build/answers](47-neo4j-build-and-graph-answers.md) →
   [48 lifecycle/inspection](48-paired-lifecycle-and-native-inspection.md) →
   [49 acceptance/switch](49-neo4j-migration-acceptance.md).

## Agreed implementation design

- Keep the existing named core operations, fixed parameterised tools, stable source/evidence
  IDs, saved artifact contents and public contracts. Add the Neo4j implementation behind
  those operations; do not expose database-native objects to tools or screens.
- Keep synchronous graph query operations for existing synchronous tool callers. Explicitly
  run network-bound operations off the event loop at asynchronous callers such as direct
  retrieval evaluation. Own the graph driver alongside the PostgreSQL engine for one backend
  lifetime, with short-lived per-call sessions, timeouts, fixed public failures and cleanup.
  Verify cancellation and concurrent investigations during integration.
- Replace the Gephi export with native Browser inspection. Retire NetworkX query/export paths
  and remove the dependency once no application use remains. PostgreSQL owns passage content;
  compare stable references and mention edges during independent integrity reconciliation.
- Preserve PostgreSQL organisation reference tables during migration for independent checks
  and existing consumers. Source files remain authoritative; Neo4j is the graph query store.
  Removing redundant reference tables would require a separately justified change.
- Use isolated writable graph preparation followed by read-only serving and retired builder
  credentials, as in the proof. Record Community's administrative limitation explicitly.
  Pair identities include the source snapshot. Active/rollback pointers are credential-free.
- Test source-snapshot selection across login analysis, document retrieval, graph queries,
  native inspection and startup checks. A pair rollback must restore one coherent dataset without
  changing saved investigation evidence. No automatic retention/pruning policy is introduced.
- Keep production readiness explicitly gated on permissions, availability, recovery,
  monitoring and cost. An Enterprise upgrade alone is not evidence that these are configured.
- Preserve the current implementation until the replacement passes its acceptance gate;
  then remove obsolete query paths. T25/T27 remain blocked through migration completion.

## Comparison, evidence and closure limits

| Dimension | Existing PostgreSQL plus NetworkX | Selected Neo4j plus PostgreSQL |
|---|---|---|
| Graph access | In-process graph and Python traversal; one durable store | Fixed Cypher queries through a second service; native query visualisation |
| Current measured warm S6 median | 7.803 ms | 97.517 ms in the unoptimised disposable candidate |
| Write protection | Restricted PostgreSQL reader plus fixed tool code | Restricted PostgreSQL reader; Neo4j graph-data read-only serving with accepted administrative powers during development |
| Publication | One database pointer, graph prepared from it at startup | Complete source snapshot and two matching stores, restart adoption and retained rollback version |
| Operations | Fewer services; existing Gephi export for inspection | More service/resource/credential management; Browser replaces the export workflow |

The rationale is the intended relationship-query direction and native graph tooling, not a
demonstrated NetworkX capacity failure or speed improvement. See the cited
[security assessment](../research/46-community-read-only-feasibility.md),
[live comparison and limits](../research/46-parity-and-pair-proof.md),
[impact inventory](../research/46-impact-inventory.md) and
[official Browser documentation](https://neo4j.com/docs/browser/).

Every proof question has evidence or an explicit limit in the proof report: graph protection,
isolated handoff, exact answers, paired publication/rollback, isolation/failed-build cleanup and
rebuildability. Reference-only passage ingestion, application-level cutover/downtime, complete
failure/cancellation/concurrency handling and native Browser walkthrough remain implementation
acceptance work in T47–T49. A full disaster backup test and production capacity are not claimed.

Reconsider the design if those acceptance checks cannot preserve answers/evidence, the measured
operating burden or interruption is unacceptable, or production requirements/costs conflict
with the selected edition. Unknown growth and concurrency targets stay unknown until measured
or agreed. AUD-068 carries the production gate; AUD-067 stays open until T49 accepts the migration.

Closure evidence: author approved the revised design and three-ticket proposal; spec and its
decision log updated; T25/T27 depend on T49; map priority is T47. No new supported manual task
was delivered in this decision ticket. The build tickets require tested admin-manual commands
before adoption. No application code was changed by ticket publication.

## Comments

- 2026-10-30 — Author approved the revised design and consolidated three-ticket sequence.
  Published T47–T49 with `to-tickets`, updated spec/decision log and integration blockers,
  recorded AUD-068 and resolved this decision. Earlier six-ticket and GEXF-preservation
  proposals are superseded. No T47 model confirmation or application coding has begun.
- 2026-10-30 — Author questioned preserving Gephi after selecting Neo4j. Official
  [Browser documentation](https://neo4j.com/docs/browser/) confirms it ships with Community
  and visualises query results; [visualisation overview](https://neo4j.com/docs/getting-started/graph-visualization/graph-visualization/)
  documents styling and image/tabular exports; [Browser settings](https://neo4j.com/docs/browser/operations/browser-settings/)
  document node/result limits. T20's purpose was visual inspection of the organisation and
  finding neighbourhood, so Browser is a plausible replacement for that workflow. It is not
  the same as preserving GEXF files or the future in-app saved-evidence Graph tab. With the
  approved passage-reference split, Browser will not automatically display PostgreSQL passage
  text. Proposed revision: replace draft ticket 50's GEXF preservation with tested native
  inspection queries, build identification, author walkthrough and retirement of the old
  export/NetworkX dependency where unused. No removal or spec revision approved yet; ticket
  sequence remains a proposal. Verification is documentary, not a live Browser walkthrough.
- 2026-10-30 — Author selected the Neo4j target in the architecture-choice question.
  See Answer ruling 1. This supersedes earlier comments saying no engine selection exists;
  it does not approve application changes or release integration holds.

- 2026-10-30 — Parity and paired-build proof completed; see
  [evidence and limits](../research/46-parity-and-pair-proof.md) and
  [impact inventory](../research/46-impact-inventory.md). Run `ff605c4bbc`: 38 named checks,
  including full graph parity, 53 lookups and all 10 findings on original/variant/rebuilt
  graphs, dated peer cases, frozen S6 gold, read-only handoff, matching-pair activation and
  rollback. Run `ac601a07d9`: intentional failure after PostgreSQL build, no publication,
  cleanup verified. All three temporary PostgreSQL databases and graph resources removed.
  B-107 records the initial import-path failure and fix. Original warm S6 medians: NetworkX
  7.803 ms, unoptimised candidate 97.517 ms; graph preparation/handoff 50.145 s; rebuild plus
  validation 59.929 s. These are synthetic proof measurements, not capacity or analyst downtime.
  No app/dependency changes or full app/eval runs. Final schema/ownership, sync/async boundary,
  production readiness and engine ruling remain open; migration and T25/T27 release not approved.
- 2026-10-30 — Next proof documentation: reuse Neo4j Python 6.1.0 Context Hub lookup
  above for driver lifecycle and bound parameters. Psycopg installed 3.3.6, Context Hub
  `psycopg/package` 3.3.3 guide consulted for connection context commit/close, dictionary
  rows and parameter binding; only those stable APIs used. Official Cypher docs checked
  [UNWIND](https://neo4j.com/docs/cypher-manual/current/clauses/unwind/),
  [temporal functions](https://neo4j.com/docs/cypher-manual/current/functions/temporal/),
  and [paths](https://neo4j.com/docs/cypher-manual/current/patterns/variable-length-paths/)
  for batch insertion, datetime bounds and graph paths. Existing application builder APIs
  are reused without changes; offline embeddings only. Independent candidate ingestion
  reads fresh PostgreSQL rows and CSV observations rather than exporting NetworkX results.
- 2026-10-30 — Live security probe completed on Community 2026.10.1, Python driver 6.1.0
  and Docker 29.5.2. [Probe](../research/46-community-security-probe.py),
  [raw results](../research/46-community-security-result.json). Both before and after restart:
  seven graph/schema write attempts rejected with `WriteOnReadOnlyAccessDatabase`;
  `dbms.setConfigValue` absent and access-mode ALTER unsupported; create/alter/drop of
  another test user allowed. All four graph snapshots equal the seeded baseline. 24 recorded
  outcomes checked. Unique container and volume removed, temporary `.env` removed. Docker
  Desktop remains running and the downloaded image/isolated driver cache remain. No application
  dependencies or active databases changed; no application tests/evals run. This proves the
  tested data-write restrictions and confirms the accepted administrative limitation, not
  complete security or separate-builder handoff. Remaining T46 proof questions are open.
- 2026-10-30 — Neo4j Python driver 6.1.0: Context Hub `neo4j/package` and
  [official transaction documentation](https://neo4j.com/docs/python-manual/current/transactions/);
  checked driver/session lifecycle, explicit database selection and parameterised queries.
  Disposable security probe uses write-mode sessions so graph-write refusals must come from
  the server. Docker config naming follows Neo4j's documented underscore conversion;
  the current Docker configuration page timed out, so the official
  [container configuration explanation](https://neo4j.com/docs/kafka-streams/docker-streams/)
  was used for that naming rule only. Driver is isolated with `uv run --no-project --with`;
  no application dependency change. Probe syntax and `.env` ignore rule verified.
- 2026-10-30 — Author agreed to continue Community evaluation with administrative access
  treated as an explicit development-stage tradeoff. A production-readiness review must
  cover permissions, recovery, availability, monitoring and cost; Enterprise is a possible
  later upgrade, not an approved purchase or a guarantee of readiness. The spec and its
  decisions log record this conditional exception. Graph write prevention, isolated writable
  builds and all correctness/consistency proofs remain required. T25/T27 stay held and no
  engine migration is yet approved. This supersedes the earlier instruction to stop the
  evaluation solely because Community retains user-administration capabilities.
- 2026-10-30 — Author proposed separating present development needs from production
  readiness: use Community now and consider Enterprise when offering the application for
  production, alongside other operational requirements. This is a proposal under discussion,
  not yet a migration ruling or an approved spec/security exception. Codex verified the
  [official 2025–2026 Community-to-Enterprise upgrade procedure](https://neo4j.com/docs/upgrade-migration-guide/current/version-2025-2026/ce-to-ee/):
  stop, dump databases, install Enterprise and load/start. A supported edition transition
  exists; future-version compatibility, licensing cost and production configuration/testing
  remain to be assessed. No local edition upgrade was tested.
- 2026-10-30 — Security feasibility research saved in
  [46-community-read-only-feasibility.md](../research/46-community-read-only-feasibility.md).
  Perplexity discovery, official docs and Neo4j 2026.10.1 source pinned to commit
  `2994b43b44f35bf6520bd2667ab181bb76a45585` support data-graph read-only configuration
  but show administrative capabilities for Community authenticated identities and a writable
  system database. This conflicts with the proposed unprivileged-serving requirement;
  no live failure has been reproduced. Runtime `dbms.setConfigValue` is Enterprise-only,
  so it is not a demonstrated Community bypass. Discuss the finding before the broader proof;
  a minimal live confirmation is proposed. No acceptance gate beyond model/scope is ticked.
- 2026-10-30 — Codex platform preflight: `uname -m` reports x86_64; `sw_vers` reports
  macOS 15.7.8. Docker client 29.5.2 is installed but its configured local daemon socket
  is absent; `/usr/libexec/java_home -V` reports no Java runtime. No service started or
  package installed. These are setup prerequisites, not application defects.
- 2026-10-30 — Neo4j Community 2026.10.1 documentation via official web pages:
  [requirements](https://neo4j.com/docs/operations-manual/current/installation/requirements/),
  [macOS](https://neo4j.com/docs/operations-manual/current/installation/osx/),
  [Docker](https://neo4j.com/docs/operations-manual/current/docker/introduction/).
  Checked x86_64 support, macOS archive installation with Java 21 or 25, and the Community
  image tag without the Enterprise suffix. Local runtime compatibility is not yet tested.
- 2026-10-30 — Author agreed the proposed review and isolated-proof scope: shared analyst
  service, measured planned interruption, free editions first; compare the existing design
  with Neo4j Community plus PostgreSQL/pgvector against the six proof questions above.
  Start with Community database-enforced read-only feasibility; if that gate fails, discuss
  the finding before setting up the remaining experiment. Synthetic isolated resources only;
  preserve application code and active databases. Identify installation requirements before
  setup. Exact concurrency and growth remain unknown, so synthetic measurements cannot
  establish capacity for a production workload. No migration or paid service approved.
- 2026-10-30 — Author chose free editions first. Paid features require a later decision
  if a necessary safeguard is missing. Hosting costs remain a separate consideration.
- 2026-10-30 — Author accepts a brief planned maintenance window during knowledge-base
  rebuilds. Measure the interruption in the disposable proof before agreeing a numerical
  limit. This does not waive matching-build verification or read-only serving safeguards.
- 2026-10-30 — Author chose a shared analyst service, with several analysts using one
  deployment, as the operating target for the architecture review. Exact concurrency,
  availability, growth and budget remain open; this does not expand phase 0/1 deliverables.
- 2026-10-30 — Author confirmed Astra is selected for this review and authorised starting
  T46. Codex claimed the ticket. Target requirements and disposable-proof scope remain to
  be agreed before execution. If this discussion results in build tickets, the author requests
  the installed `to-tickets` skill; Codex located and read it. No migration ruling is implied.
- 2026-10-30 — Author: approved creating the architecture decision ticket and agreeing its
  scope before application changes. Preferred candidate is Neo4j Community plus PostgreSQL
  with pgvector. No engine replacement or security exception has been approved.
- 2026-10-30 — Codex: created T46, placed it ahead of T45 by the approved next-step direction,
  and held T25/T27 and their downstream work. Proof scope above is proposed for review;
  no installation, experiment, model confirmation or migration performed in ticket creation.
