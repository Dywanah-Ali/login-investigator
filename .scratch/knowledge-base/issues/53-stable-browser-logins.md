# 53: Stable Browser access: named logins and a fixed address

Type: build
Status: resolved
Blocked by: none
Blocks: none
Phase: 0
Model: standard (Opus 5.5 or Sol 6.1)
Rigour: Tier 2

## What to build

Today every graph build creates the application's serving login with a fresh random password,
written only to that build's private `.env`, and publishes Browser and Bolt on random localhost
ports. To open Neo4j Browser the author has to find that build's file, copy a new password and
look up new ports each time a build changes or restarts. People also borrow the application's
own identity to look at the graph.

Give the author one stable way into the graph, regardless of build.

**Named logins.** Two Browser logins, `li_admin` and `li_reader`, whose passwords the author sets
once in the main `.env`. Every new build creates both users with those passwords alongside the
application's serving login, which keeps its own per-build random password and stays the only
identity the application uses. A one-off operator command adds the same two users to an existing
complete pair, so the running pair `2d1bf85e…` gains them without a rebuild.

**Fixed address.** The build the application has selected answers at `http://127.0.0.1:7474`
and `bolt://127.0.0.1:7687`. Every other retained, evaluation or rehearsal build keeps random
ports, so builds never clash. The fixed address cannot be given at build time, because a new
build starts while the selected one is still running and holding the ports. It moves at
selection time instead: selecting a build, or rolling back to the previous one, gives the fixed
address to the newly selected build and keeps every build's data volume.

Neo4j Community has no roles: every user holds full administrative powers. `li_reader` is
read-only by convention only, through Browser's read access mode. The real protection stays the
server-level read-only lock on the serving database, which applies to every user. Users live in
the separate `system` database, which that lock does not cover, so they can be added to a sealed
pair. Enforced roles remain part of the AUD-068 production review.

The work carries two levels of risk. The logins touch only users inside Neo4j and leave the
running graph working throughout. The fixed address recreates containers during selection and
rollback, where a mistake could break rollback or leave the application without its graph.
Build and verify the logins first, then the address.

## Decisions implemented

- Author's ruling, 1 November 2026: option A. Fixed, named logins for people from the main `.env`,
  and a fixed address for the selected build; enforced roles through Enterprise stay under
  AUD-068. Reason: the author needs one stable way into the graph regardless of build, and the
  serving database's server lock already prevents writes for every user.
- Author's ruling, 1 November 2026: the work gets a ticket, and one ticket rather than two
  (logins and address were first cut as T53 and T54, then merged at the author's request).

## Acceptance criteria

- [x] Before any build work starts, the builder tells the author this ticket's `Model:` line and
      asks the author to set that model. A dated line under Comments records the model used.
- [x] Third-party documentation is checked first (Neo4j Cypher user management in Community
      2026.10, the Python driver behaviour used, and Docker port publishing and container
      recreation), and recorded under Comments in the issue-tracker format.

Logins:

- [x] A new build creates `li_admin` and `li_reader` with the passwords from the main `.env`.
      The serving login and its per-build random password are unchanged, and the application
      still connects only as the serving login.
- [x] A build stops before creating any container, with a clear message naming the missing
      variable, when either password is absent or empty in the main `.env`. `env.example`
      gains the two variable names only.
- [x] No password appears in command output, reports, saved queries, logs or test snapshots.
- [x] The one-off command adds both users to an existing complete pair, refuses a pair that is
      not complete or not running, and is safe to run twice: a second run reports the users as
      already present without changing them.
- [x] Evidence: the author logs in to the running pair `2d1bf85e…` in Browser as both
      `li_admin` and `li_reader`, after the one-off command.

Fixed address:

- [x] Selecting a complete build gives it the fixed address, and the previously selected build
      no longer holds it. Both builds' data volumes and recorded protection stay intact.
- [x] Rollback moves the fixed address back to the previous build in the same way.
- [x] Selection refuses with a clear message, and changes nothing, when either fixed port is
      held by something other than the outgoing selected build.
- [x] Builds that are not selected, including evaluation and rehearsal builds, keep random ports.
- [x] Evidence: the author opens `http://127.0.0.1:7474` in Browser and reaches the selected
      pair, and the inspection report records the fixed address.

Both:

- [x] The serving write-protection check passes for new builds and for the build at its fixed
      address, and the build's protection record is unchanged in shape.
- [x] The inspection report and saved instructions name `li_reader` as the Browser login.
- [x] The admin manual's sections 5 and 6 state where the two passwords live, that `li_reader`
      is read-only by convention only (AUD-068), the one-off command, and the fixed address and
      when it moves, with every command tested as written.
- [x] Backend tests, frontend tests and types pass. The builder's two-axis review is recorded.

## Comments

2026-11-02 — Final regression: complete backend suite **668 passed in 2032.92 seconds**;
no failures or teardown errors. Frontend **150 passed**, backend and frontend types clean,
backend Ruff clean. Frontend lint retains its six existing AUD-009 warnings. Both review
axes have zero remaining findings (`reviews/53-code-review-2026-11-01.md`). The working
pair alone remained running after test cleanup. Exact operator commands are being checked
before closure; no paid evaluation was required because agent behaviour is unchanged.

2026-11-02 — Author confirmed that the fixed Browser address works with Bolt port 7687.

2026-11-02 — New T53 service tests passed in the full run before the suite advanced beyond
200 checks: both new human logins, serving identity separation, eight write refusals per
human user, one-off creation/repeat/non-reset behaviour, incomplete/stopped refusal, both
port conflicts, selection, injected publication-failure recovery, rollback, missing outgoing
marker recovery, stopped outgoing preservation, and unchanged protection records.

2026-11-02 — Working pair `2d1bf85e…` reselected with the documented operator command.
Browser now serves `http://127.0.0.1:7474/browser/`, Bolt `bolt://127.0.0.1:7687`.
The backend was stopped before the move. Original selection bytes (including previous
`f937ea59…`) and both protection-record checksums remain unchanged. Both human users
authenticated after recreation and each passed all eight protection checks. Credential-free
evidence: `research/53-live-access.json`. Fresh inspection at the working pair's ignored
`inspection-t53/` reports `li_reader`, fixed ports, 170 organisation nodes / 185 relationships,
and ten findings. Author fixed-address acceptance and final full-suite result follow.

2026-11-02 — Codex verification lookup: python-dotenv installed 1.2.4; Context Hub
`python-dotenv/package` covers 1.2.2, supplemented with the official
[function reference](https://bbc2.github.io/python-dotenv/reference/); checked:
`dotenv_values` parses without mutating the environment, missing versus empty values,
and `interpolate=False` to preserve literal operator passwords.

2026-11-01 — Verification progress: service-free selection checks 4 passed; backend and
frontend types passed during implementation. Initial frontend run 148/150 with two AUD-028
Explorer timeouts; final one-worker rerun 150/150 in 76.49 seconds without frontend changes.
Initial login run authenticated both users and verified write refusal, then failed the B-137
test assertion (2 passed, 1 failed). A superseded fixed-address focused run was terminated
after review corrections; its exact two disposable pairs `e3a31059…` / `a0bc0164…` and their
databases were explicitly removed using ownership-checked disposal. It is not passing evidence.
The final full backend run follows with reviewed code and isolated test addresses.

2026-11-01 — Author: confirmed Browser access as both `li_admin` and `li_reader` on the
working `2d1bf85e…` pair after the one-off command. Codex ran that command twice; results
were `created` then `already present` for both users. No passwords were printed.

2026-11-01 — Two-axis review first pass: Standards found test-port collision with the working
service and duplicated checked-start logic. Spec found outgoing readiness blocking recovery
and failure to attempt the second restoration after the first failed. Corrections recorded
in B-138/B-139/B-140; final review and verification follow below.

2026-11-01 — Codex: author approved test boundaries at build, provisioning command and
selection/rollback interfaces. Tests use disposable pairs and fake Browser passwords from
a private temporary test file. Human Browser login and appearance remain author checks.
Operator CLI moves fixed ports by default; `--isolated` keeps rehearsal selections random.
Core/evaluation selection defaults to isolated ports so evaluations cannot take the working address.

2026-11-01 — Codex: author selected Sol 6.1 and confirmed it before build work. Author invoked
`implement T53`, taking this ticket ahead of T52 for this session. Review baseline:
`dc17f6e0f7da9d1fb984ca0f523290dbeefac7dc` on `main`.

2026-11-01 — Codex: Neo4j Community 2026.10.1; documentation:
[user management](https://neo4j.com/docs/operations-manual/current/authentication-authorization/manage-users/),
via web; checked: system-database user creation, password parameters, `IF NOT EXISTS`,
and Community users' implied administrative privileges. Current manual is rolling;
the pinned server's behaviour will also be tested locally.

2026-11-01 — Codex: neo4j Python 6.1.0; documentation: `neo4j/package` via Context Hub,
matching the installed pin; checked: parameterised queries, explicit database selection,
consumed results and scoped driver/session cleanup.

2026-11-01 — Codex: Docker Engine CLI; documentation:
[port publishing](https://docs.docker.com/engine/network/port-publishing/) and
[volumes](https://docs.docker.com/engine/storage/volumes/), via web after Context Hub search
returned SDK documentation rather than CLI coverage; checked: localhost bindings are set
at container creation and named volumes persist independently of containers.

2026-11-02 — Closure: the exact section 4 offline build/dispose command passed in 170.012
seconds and removed its unique resources (`research/53-command-result.json`). The section 5
rollback command ran twice: fixed ports moved to retained `f937ea59…`, both human identities
and eight protection checks each passed there, then fixed ports returned to `2d1bf85e…`.
The original selection bytes and both protection-file checksums match the pre-work baseline.
Both human logins authenticated against the restored current build. The older pair was
stopped cleanly (exit 0) with its volume retained. Only the current pair runs; backend remains
stopped as it was before this work. The section 6 inspection command passed at fixed ports.
Docker Engine 29.5.2 was used. All acceptance criteria have evidence; no GitHub push was made.

## Answer

Stable human logins now come from the main private `.env`, while the application retains its
separate random per-build serving identity. New builds refuse missing Browser passwords
before allocating resources. `scripts.provision_browser_users` safely adds the human users
to running complete pairs without resetting existing passwords.

Operator selection and rollback move Browser `7474` and Bolt `7687` on localhost by recreating
containers over their retained volumes. Conflict checks precede changes. Failed publication
restores original bindings; recovery handles missing/stopped outgoing pairs and attempts both
restorations. Evaluation/rehearsal selection remains isolated. Inspection names `li_reader`.
Community's administrative powers and the server read-only lock remain explicit under AUD-068.

Accepted by the author: both human Browser logins and the fixed address. Verification:
668 backend tests; 150 frontend tests; clean types and backend Ruff; zero remaining findings
on each review axis. Six existing frontend lint warnings and the separately recorded frontend
intermittent remain outside scope. No agent behaviour changed.

Evidence: [verification](../research/53-verification.json),
[backend run](../research/53-backend-tests.txt),
[live access and rollback](../research/53-live-access.json),
[operator build](../research/53-command-result.json),
[two-axis review](../reviews/53-code-review-2026-11-01.md),
and [admin manual](../../../docs/admin-manual.md), sections 4–6.
