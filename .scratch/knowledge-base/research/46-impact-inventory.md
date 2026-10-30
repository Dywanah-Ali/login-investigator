# T46: migration impact inventory

Date: 2026-10-30. Read-only inspection of repository sources. No application changes or
test runs. This is an impact inventory, not an approved migration design.

The named core functions provide useful boundaries, but the implementation exposes NetworkX
objects in several places. Replacing the engine is therefore more than changing a connection.
Public evidence and tool contracts can largely stay stable if storage-specific objects remain
inside the core.

The [current spec](../spec.md#the-store-and-the-build-t02-t03) and [T46](../issues/46-graph-store-architecture-review.md)
allow Community's administrative powers during this development evaluation only. Graph-data
write prevention, isolated writable builds and PostgreSQL reader separation still apply.
Permissions, recovery, availability, monitoring and cost remain a production-readiness gate.
No migration has been selected.

## Existing contracts and conditional migration work

| Area | What exists and must be preserved | Impact if migration is chosen |
|---|---|---|
| Source ownership and build | [`build_knowledge_base`](../../../backend/login_investigator/knowledge_base/__init__.py) loads organisation tables, chunks, vectors and mentions into a fresh PostgreSQL database; it records the source fingerprint last and grants the reader access. Files remain the source of truth. | Add a separately writable graph build. Decide explicitly which graph records are copied and which store owns each representation. The current graph includes chunk content/metadata as well as organisation nodes and mentions; omitting them would change integrity/export contracts. Keep retrieval and PostgreSQL permissions intact. |
| Publication and rollback | `rebuild_knowledge_base` in the same module publishes a credential-free pointer by atomic file replacement only after success. Failed new databases are dropped; the previous database is retained. | Publish a complete graph/PostgreSQL pair with a shared build identity. An interrupted graph import or PostgreSQL build must not publish half a pair. Define graph resource retention, cleanup and return to the previous matching pair. Two independent successful writes are not an atomic publication protocol. |
| Integrity | [`integrity.py`](../../../backend/login_investigator/knowledge_base/integrity.py) independently reads PostgreSQL records and CSV login observations, checking exact IDs, attributes, relationships and timestamps. It does not reuse the graph builder's transform. | Read candidate graph records through a new storage boundary while retaining independent source-derived expectations. Count equality alone is insufficient. Preserve corruption tests for valid-but-swapped endpoints and changed attributes, plus legitimate unmentioned chunks and unused networks. |
| Startup and lifetime | [`open_current_knowledge_base` / `open_knowledge_base`](../../../backend/login_investigator/knowledge_base/__init__.py) verify freshness, build/check/freeze the NetworkX graph and own the PostgreSQL pool. [`api/app.py`](../../../backend/api/app.py) opens this once before constructing services, closes it on shutdown and releases it if later startup fails. No build starts the app without knowledge-base tools; an uncheckable existing build prevents startup. | Own both storage clients for one backend lifetime. Check build-pair identity, graph availability, graph-data protection and source freshness before accepting requests. Preserve fixed public errors and cleanup after partial startup. Keep restart-based adoption unless the author explicitly changes it. |
| Graph construction | [`graph.py`](../../../backend/login_investigator/knowledge_base/graph.py) constructs typed edges from organisation tables and successful logins; observed timestamps are sorted and deduplicated. Failed logins and external addresses do not create the same edges. | Move this representation into the graph importer without changing evidence meaning. Keep stable entity IDs and typed relationships independent of database-generated IDs. Preserve the distinction between assigned devices and observed device use. |
| Named query functions | [`KnowledgeBase`](../../../backend/login_investigator/knowledge_base/__init__.py) exposes `lookup_account`, `account_groups`, `finding_radius`, `finding_walk`, `search_corpus` and `export_gexf`. [`radius.py`](../../../backend/login_investigator/knowledge_base/radius.py) defines the returned records, paths and period semantics. | Put fixed parameterised graph queries behind these named operations. Preserve exact account matching, deterministic order, date filtering on both sides of peer matches, exclusive end bounds, permission-snapshot qualification and shared-address context outside exposure counts. `KnowledgeBase.graph` and the optional NetworkX argument to integrity are implementation coupling to remove or contain, not public API requirements. |
| Agent tools | [`knowledge_tools.py`](../../../backend/login_investigator/knowledge_tools.py) implements the synchronous lookup tool with content plus an artifact. [`tools.py`](../../../backend/login_investigator/tools.py) registers it centrally; [`agent.py`](../../../backend/login_investigator/agent.py) receives the prepared core. | Preserve tool name, input, briefing and artifact shape. T25's peers/search tools, T26's package and T27's citations are planned work, not already-delivered adapters to migrate. Their blockers must reflect any approved migration. No free-form model-written Cypher. |
| IDs, memory and citations | [`rules.py`](../../../backend/login_investigator/rules.py) derives finding IDs from defining fields; [`chunking.py`](../../../backend/login_investigator/knowledge_base/chunking.py) creates document/section chunk IDs. Graph IDs come from source records. Lookup artifacts have `schema_version: 1`, basis, account, groups and paths. [`tool_evidence.py`](../../../backend/login_investigator/tool_evidence.py) fences content and keeps saved artifacts outside model input. | Preserve source IDs and JSON values. Do not expose Neo4j identity objects as evidence IDs. Saved evidence must survive reopening without querying the new graph. SQLite retention/migration remains outside this ticket. The planned single citation resolver and screen graph projection must consume saved artifacts, not the current database. See [spec IDs/tools/API sections](../spec.md#the-ids-t05). |
| Export and future screen projection | [`gexf.py`](../../../backend/login_investigator/knowledge_base/gexf.py) uses NetworkX for whole-graph and finding-neighbourhood export, including typed colours, reserved-attribute refusal and Gephi colour compatibility. [`export_graph.py`](../../../backend/scripts/export_graph.py) checks the published build first. | A graph database does not replace this export format. One possible seam is a record/path snapshot converted to NetworkX only for export; that is a proposal, not a decision. Preserve neighbourhood semantics, null/list metadata handling and refusal to write inside the dataset. The future Graph tab/API projection remains artifact-based under [the spec](../spec.md#api-contract-changes-t05-t07-t08), not a live graph browser. |

## Synchronous and asynchronous boundary

Today's graph queries are synchronous in-memory operations. PostgreSQL search and opening are
asynchronous. The agent itself streams synchronously, and
[`api/investigation_routes.py`](../../../backend/api/investigation_routes.py) advances that stream
in a worker thread. A remote graph adds network waits to currently local method calls.

This requires an explicit implementation choice, not an automatic conversion of the whole app:

- Preserve synchronous graph methods with a compatible client boundary, or make graph methods
  asynchronous and adapt the tools/agent execution path deliberately. Neither option is selected.
- [`evals/retrieval.py`](../../../backend/evals/retrieval.py) is asynchronous but invokes
  `account_groups` and `finding_walk` synchronously today. A blocking network call there needs
  deliberate handling; a coroutine cannot simply replace the current returned `GraphWalk`.
- The export command is asynchronous around a synchronous `export_gexf`. Startup, tools, direct
  evaluations and export must agree on client ownership, timeout/error handling and shutdown.
  Avoid unreviewed event-loop bridges inside the core.
- Preserve stream cancellation and investigation concurrency behaviour. Separate requests may
  share the core lifetime, but per-query mutable state must not leak between them. Driver/session
  sharing rules need official documentation when implementation is scoped.

## Verification and operations affected

| Surface | Existing evidence/contracts to carry forward |
|---|---|
| Database isolation | [`postgres_fixture.py`](../../../backend/tests/postgres_fixture.py) creates a fresh session database and fails rather than skips if PostgreSQL is unavailable. [`test_knowledge_base.py`](../../../backend/tests/test_knowledge_base.py) adds disposable builds and fake embeddings. Add separately named graph resources per run, failure cleanup and proof that tests never touch the active pair. Preserve PostgreSQL write-refusal checks. |
| Query parity | [`test_knowledge_graph.py`](../../../backend/tests/test_knowledge_graph.py) covers exact S6 answers, dated peers and address observations. [`test_eval_knowledge_base_questions.py`](../../../backend/tests/test_eval_knowledge_base_questions.py) validates frozen gold. Preserve source-derived expectations rather than rewriting gold to match a new query. |
| Lifecycle and artifacts | [`test_api_startup.py`](../../../backend/tests/test_api_startup.py) and [`test_kb_agent.py`](../../../backend/tests/test_kb_agent.py) check startup refusal, reuse, restart adoption, cleanup, saved-artifact recovery and model-input exclusion. Extend these to both clients without weakening those behaviours. |
| Export and retrieval | [`test_graph_export.py`](../../../backend/tests/test_graph_export.py) checks read-back identities/counts and neighbourhoods. [`test_eval_retrieval.py`](../../../backend/tests/test_eval_retrieval.py) and [`evals/retrieval.py`](../../../backend/evals/retrieval.py) enforce integrity before retrieval and compare exact graph records/paths. Include graph version/build/configuration in reproducibility evidence. Keep T45's missing-document-candidate concern separate. |
| Deployment/configuration | [`backend/env.example`](../../../backend/env.example), [`api/settings.py`](../../../backend/api/settings.py), the knowledge-base state pointer and [`backend/pyproject.toml`](../../../backend/pyproject.toml) currently express the existing dependencies/settings. Any migration needs graph connection/build settings, secret separation, service start/stop, resource limits, failure diagnostics and a pinned runtime. The disposable experiment does not constitute a deployment design. |
| Manual tasks | [`docs/admin-manual.md`](../../../docs/admin-manual.md) has graph export, direct retrieval and saved-evidence measurement commands. Update affected prerequisites/refusals and add adopted build, activation, rollback and recovery tasks in its fixed shape. Test commands as written. Do not present research-probe commands as supported administration prematurely. |
| Safety net | Retain backend/frontend tests and type checks. Verify API and tool output compatibility against [`docs/api-contract.md`](../../../docs/api-contract.md). Any agent-behaviour change requires the existing evaluation gates; do not treat parity of graph counts as an agent regression test. |

## Decisions needed before migration tickets

1. Graph-record ownership and chunk/mention representation across the two stores.
2. Stable paired-build identity and activation/rollback lifecycle.
3. Synchronous versus asynchronous query boundary and error/cancellation behaviour.
4. Export representation and whether NetworkX remains solely as an export utility.
5. Explicit development limitations, production-readiness owner and implementation blockers.

No unavoidable HTTP or saved-artifact schema change was identified in this bounded inspection.
Internal call signatures and publication/configuration formats will need attention. Their final
shape depends on the author's engine ruling and the remaining proof evidence.
