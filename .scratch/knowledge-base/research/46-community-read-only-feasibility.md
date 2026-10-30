# T46: Neo4j Community read-only feasibility

Research date: 2026-10-30. Scope: documentation and pinned upstream source only.
No server was installed, started or tested for this note. No active data was changed.

Subsequent author ruling, 30 October 2026: the administrative-access limitation is accepted
for development evaluation, with a separate production-readiness review. This supersedes
the recommendation below to stop solely on administrative isolation. It does not turn
Community into a least-privilege system. A subsequent disposable probe and its result file
record live evidence separately; the original source findings below remain unchanged.

## Finding

Neo4j Community offers a plausible way to prevent writes to the **data graph** through
startup configuration. That is materially different from giving the application a
**least-privilege reader identity**. The latter is not established: the inspected Community
source grants authenticated users administrative capabilities, while the system database
is explicitly exempt from database-wide read-only settings.

This is a source-backed incompatibility with the proposed requirement that serving credentials
cannot perform administrative mutations. It is **not a reproduced live failure**, and it is
not a claim that the data-graph read-only setting can necessarily be undone remotely.
The agreed security-first sequence calls for discussing this finding before the wider proof.

## Release and evidence boundaries

- The official [deployment center](https://neo4j.com/deployment-center/) lists Community
  **2026.10.1**, released **23 October 2026**, as well as the 5.26 maintenance line.
  This establishes an offered release, not a downloaded or verified local binary.
- Source inspection is pinned to the official `2026.10.1` tag, resolved through GitHub's API
  to commit [`2994b43b44f35bf6520bd2667ab181bb76a45585`](https://github.com/neo4j/neo4j/tree/2994b43b44f35bf6520bd2667ab181bb76a45585).
  The tag object is `3eef601af38c1eb8c6410b7ae60a62a18fb9c2f6`.
- Perplexity Search located the dynamic-settings documentation. Claims below were checked
  against official Neo4j documentation and the pinned Neo4j source, rather than treating
  search synthesis as evidence. Current documentation can move after this date.

## Verified facts and implications

| Question | Evidence | Implication for T46 |
|---|---|---|
| Is data-graph read-only configuration available? | The [configuration reference](https://neo4j.com/docs/operations-manual/current/configuration/configuration-settings/#config_server.databases.default_to_read_only) documents `server.databases.default_to_read_only`, `server.databases.read_only` and `server.databases.writable`; these entries are not Enterprise-only. | Startup configuration remains a valid candidate for a live data-write refusal test. |
| Does it protect the system database too? | The [database configuration documentation](https://neo4j.com/docs/operations-manual/current/database-administration/standard-databases/configuration-parameters/) explicitly excludes `system`. Pinned [`DefaultReadOnlyDatabases`](https://github.com/neo4j/neo4j/blob/2994b43b44f35bf6520bd2667ab181bb76a45585/community/common/src/main/java/org/neo4j/dbms/database/readonly/DefaultReadOnlyDatabases.java) returns writable for the system database. | Protecting the data graph does not remove administrative state changes. |
| Can a Community client simply call `dbms.setConfigValue` to undo the setting? | Both [dynamic settings](https://neo4j.com/docs/operations-manual/current/configuration/dynamic-settings/) and the [built-in procedure reference](https://neo4j.com/docs/operations-manual/current/procedures/built-in-procedures/#_dbms_setconfigvalue) mark runtime configuration changes as Enterprise-only. | Do not claim this is a Community bypass. Verify that the procedure is unavailable on the selected Community binary. |
| Can `ALTER DATABASE ... SET ACCESS READ WRITE` undo it? | The [ALTER DATABASE documentation](https://neo4j.com/docs/operations-manual/current/database-administration/standard-databases/alter-databases/) marks access-mode administration Enterprise-only. The Community runtime's supported `AlterDatabase` case is limited to changing the default query language. | Test the exact access-mode command, but documentation/source do not support treating it as an available Community bypass. Do not claim all `ALTER DATABASE` forms are unavailable. |
| Can the application receive a restricted reader role? | Neo4j describes [role-based authorization as Enterprise functionality](https://neo4j.com/docs/operations-manual/current/authentication-authorization/). Pinned [`BasicLoginContext`](https://github.com/neo4j/neo4j/blob/2994b43b44f35bf6520bd2667ab181bb76a45585/community/security/src/main/java/org/neo4j/server/security/auth/BasicLoginContext.java#L46-L59) gives successful authentication `StaticAccessMode.FULL`. | A different username alone does not establish different privileges. |
| Are administrative mutations actually represented in Community code? | [`SecurityContext`](https://github.com/neo4j/neo4j/blob/2994b43b44f35bf6520bd2667ab181bb76a45585/community/kernel-api/src/main/java/org/neo4j/internal/kernel/api/security/SecurityContext.java#L66-L80) explicitly grants administrative actions and admin-procedure execution. [`CommunityAdministrationCommandRuntime`](https://github.com/neo4j/neo4j/blob/2994b43b44f35bf6520bd2667ab181bb76a45585/community/cypher/cypher/src/main/scala/org/neo4j/cypher/internal/CommunityAdministrationCommandRuntime.scala#L331-L382) implements create, rename, alter and drop user commands. | Source predicts serving credentials can manage other users even while the data graph is read-only. This is a concrete concern beyond the absence of role-based access control. |

The `system` database is not generally open to arbitrary `MATCH`/`CREATE` queries. The relevant
mutation path is supported administrative commands, which are routed to it. The official
[authentication overview](https://neo4j.com/docs/operations-manual/current/authentication-authorization/)
describes that routing; the [user-management documentation](https://neo4j.com/docs/operations-manual/current/authentication-authorization/manage-users/)
distinguishes Community-supported commands from Enterprise-only user properties.

## Procedure allowlist is not a replacement reader role

The pinned [`ProcedureCompiler`](https://github.com/neo4j/neo4j/blob/2994b43b44f35bf6520bd2667ab181bb76a45585/community/procedure/src/main/java/org/neo4j/procedure/impl/ProcedureCompiler.java#L222-L259)
accepts procedures when `fullAccess` is true **or** their name passes the allowlist.
[`GlobalProceduresRegistry.registerProcedure`](https://github.com/neo4j/neo4j/blob/2994b43b44f35bf6520bd2667ab181bb76a45585/community/procedure/src/main/java/org/neo4j/procedure/impl/GlobalProceduresRegistry.java#L132-L138)
uses that full-access compilation path. Therefore an extension-loading allowlist must not be
assumed to suppress all registered built-in procedures. More directly, user-administration
Cypher commands are not user-defined procedures, so this configuration is not evidence that
they would be denied.

No custom security extension, protocol-filtering proxy or modified database binary has been
assessed. None is implicitly approved as a workaround.

## Smallest useful live confirmation, if chosen

Use a disposable Community 2026.10.1 instance, a synthetic graph and distinct test identities.
Set data-graph read-only in its configuration before exposing the serving instance.

1. Establish edition/version and successful reads. Attempt node/relationship creation,
   updates and deletion, plus schema changes, with the serving identity.
2. Attempt `dbms.setConfigValue` and `ALTER DATABASE ... SET ACCESS READ WRITE` with that identity;
   preserve exact errors and verify the graph remains read-only.
3. Attempt to create a disposable user, change another disposable user's password and drop
   that user. Do not use real credentials. These tests distinguish graph immutability from
   administrative isolation.
4. Repeat the relevant observations after restart. Capture which restrictions are persisted.

If user administration succeeds, record the administrative-isolation gate as failed even if
graph writes are blocked. Do not proceed to the broader parity/activation/recovery experiment
as though all security requirements passed. A change to the accepted security boundary needs
an explicit author ruling; choosing an engine does not provide that ruling.

## Licence fact

Neo4j's [legal overview](https://neo4j.com/legal-terms/) links Community Edition to GPL v3;
the pinned [repository licence](https://github.com/neo4j/neo4j/blob/2994b43b44f35bf6520bd2667ab181bb76a45585/LICENSE.txt)
is GNU GPL version 3. This identifies the licence only. No legal interpretation of a future
deployment or distribution is made here. Desktop/Enterprise developer terms are not Community
licensing evidence.

## Remaining gaps

At the original research checkpoint, no live behaviour had been verified. The subsequent
probe below covers selected enforcement and restart behaviours only. Builder handoff, graph
parity, dual-store activation, recovery, performance and capacity remain unverified. This
note does not close T46 or release T25/T27.

## Subsequent live evidence, 30 October 2026

Run from the repository root:

```sh
uv run --no-project --with neo4j==6.1.0 .scratch/knowledge-base/research/46-community-security-probe.py
```

[Probe code](46-community-security-probe.py) and [raw results](46-community-security-result.json).
Server reported Community 2026.10.1. Host: Intel macOS 15.7.8; Docker engine 29.5.2.
The container served only a dynamically allocated localhost Bolt port. It used a unique
scratch volume and two synthetic nodes joined by one relationship. The builder seeded the
graph, then the container was replaced with `server.databases.read_only=neo4j` over the same
volume. The distinct serving username is not described as least-privileged.

| Check | Initial read-only start | After restart |
|---|---|---|
| Read graph | Seeded data returned | Same data returned |
| Create/update/delete nodes or relationships; create index; write after bypass attempts | All seven rejected by server with `Neo.ClientError.General.WriteOnReadOnlyAccessDatabase` | Same |
| `dbms.setConfigValue` | Procedure not found | Same |
| `ALTER DATABASE neo4j SET ACCESS READ WRITE` | Unsupported administration command | Same |
| Create, alter and drop another disposable user | Allowed | Allowed |

All four before/after snapshots matched the baseline. The 24 recorded outcomes and cleanup
results were checked by a separate read-only assertion run. The unique container, volume
and temporary `.env` were removed. Docker Desktop remains running; the image and isolated
driver cache remain available. No application package, active build or database was changed.

This is evidence for the specific tested configuration and commands, not an exhaustive
security audit or a proof of separate builder handoff. No mutating extension was installed.
The accepted development-stage administrative limitation is now reproduced, not just inferred.
