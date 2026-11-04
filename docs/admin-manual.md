# Admin manual

Tasks the author runs by hand: what each one is for, the exact commands, and what to do when it
refuses. One section per task. When a ticket adds a task an administrator runs, it adds a
section here in the same shape: **What it is for**, **Before you start**, **Run it**, **Open or
check the result**, **When it refuses**.

Commands are written to run from the repository root. In Claude Code, put `!` in front of a
command to run it in the session.

## Contents

1. [Retired Gephi workflow](#1-retired-gephi-workflow)
2. [Check retrieval without the agent](#2-check-retrieval-without-the-agent)
3. [Measure saved account-lookup evidence](#3-measure-saved-account-lookup-evidence)
4. [Verify an isolated Neo4j graph version](#4-verify-an-isolated-neo4j-graph-version)
5. [Select, restart and roll back a paired graph version](#5-select-restart-and-roll-back-a-paired-graph-version)
6. [Inspect a paired graph in Neo4j Browser](#6-inspect-a-paired-graph-in-neo4j-browser)
7. [Check Python code with Ruff](#7-check-python-code-with-ruff)
8. [Run, review and mirror a model comparison](#8-run-review-and-mirror-a-model-comparison)

---

## 1. Retired Gephi workflow

Retired on 30 October 2026 after the author's native Browser walkthrough and acceptance in T48.
Use [section 6: native graph inspection](#6-inspect-a-paired-graph-in-neo4j-browser).
The export command is removed. [T20's historical evidence](../.scratch/knowledge-base/issues/20-gephi-export.md)
and its bug history remain preserved.

## 2. Check retrieval without the agent

Added by knowledge-base ticket 22. The re-ranker switch added by ticket 23.

### What it is for

Check whether corpus search finds every required passage in its top 20 and whether graph walks
return exactly the expected records and paths. This uses T21's eight questions. It does not ask
the agent to write an answer or judge the benign twins. Run it after each knowledge-base build.

### Before you start

PostgreSQL and Docker Desktop must be running, with the pinned Neo4j image from section 4.
The selected complete pair and source snapshot must pass their integrity checks. The reader
password and `OPENROUTER_API_KEY` must be set in `backend/.env`. Each run creates its own
disposable PostgreSQL/Neo4j pair and source snapshot. It copies exact stored passage vectors,
so it does not buy document embeddings again. Real query embeddings make a small paid request
per text question. The run disposes only its own resources and leaves the application selection
unchanged.

The re-ranker is **on by default**. With it on, each text question makes one more small paid
request: Cohere's re-ranker, through OpenRouter, scores the 20 fused passages and the best 5 are
kept. To run without it, set `LI_RERANKER=off` in `backend/.env`, or for one run only:

```sh
LI_RERANKER=off uv run --directory backend python -m evals.run --layer retrieval
```

The setting accepts only `on` or `off`. An empty value means on.

### Run it

From the repository root:

```sh
uv run --directory backend python -m evals.run --layer retrieval
```

To check selected questions, add `--only K01 K04`. The retrieval layer runs once per question;
the answer layer's `--runs` and `--jobs` options do not change that. It calls the core directly,
so `--mode api` does not apply.

### Open or check the result

The command prints a result for each question and the saved JSON path under
`backend/evals/results/`. The JSON records all candidate ranks and scores, the fused top 20,
graph paths, the integrity check, embedding usage and configuration fingerprint. With the
re-ranker on, it also records each of the 20 candidates' re-ranker score, the 5 chunks kept,
the re-ranker usage and cost, and `"reranker": true` in the configuration.
`backend/evals/results/retrieval-summary.md` keeps its history separate from the Port exam.

Every applicable check must pass for a question. A required passage outside the fused top 20
fails. The check reads the fused 20 whether the re-ranker is on or off, so switching it does not
change a pass or fail; whether the re-ranker helps is measured separately, in ticket 41.
An extra or missing graph record or path fails. A first-gold rank of 1 means the first result
was one of the required passages; all other required passages must still appear.

To rescore a saved file without any paid call, replace `RESULT_FILE.json` with its filename:

```sh
uv run --directory backend python -m evals.run --rescore evals/results/RESULT_FILE.json
```

### When it refuses

The existing staleness guard explains a missing, stale or unreachable knowledge base. Follow its
setup or rebuild instruction. Unknown question IDs fail before connecting to the model service.
An integrity failure stops retrieval before any query is embedded.

Exit code 1 means the run completed and at least one evidence check failed. Read the saved checks.
Until T39 calibrates relevance, the search verdict is `weak` with `not_calibrated`, so the two
absent-topic questions expecting `none` are recorded as misses. This is the agreed interim
behaviour, not a reason to change their answer key. A search that finds no passage at all
returns `none` with `empty_result` (the author's T23 ruling); only a filter can cause that.

| Message says | What to do |
|---|---|
| `LI_RERANKER must be on or off` | Fix the value in `backend/.env` or the command line |
| `Set OPENROUTER_API_KEY` | Add the key to `backend/.env`, or run with `LI_RERANKER=off` |
| `The re-ranker call failed with HTTP <code>` | OpenRouter refused the call. 401 or 402: check the key and credit. 429 or 5xx: wait and run again. No result was saved |
| `The re-ranker could not be reached` | Check the network and run again. No result was saved |
| `The re-ranker reply must score every candidate exactly once` | The provider's reply was malformed. Run again; if it repeats, ask Claude or Codex to investigate |

## 3. Measure saved account-lookup evidence

Added 29 October 2026 by knowledge-base ticket 24. This is a development measurement, not
routine maintenance or a storage limit.

### What it is for

Measure how one investigation's stored evidence grows over 1, 10 and 50 repeated account
lookups. The probe uses a fake model and disposable SQLite memory. It reads the checked graph
through the read-only role, makes no paid calls and leaves real investigation memory untouched.

### Before you start

PostgreSQL and the selected pair's Neo4j service must be running, with reader settings configured
in `backend/.env`. Select a complete pair through section 5 first. Use the default synthetic
source snapshot, which contains Amelia Ward. Development
dependencies must be installed because the probe reuses the fake model from the test suite.

### Run it

```sh
uv run --directory backend python ../.scratch/knowledge-base/research/24-storage-probe.py
```

### Open or check the result

The command prints JSON: preparation time, one artifact's JSON size, checkpoint/write counts
and payload bytes, database file size at each milestone, and close/reopen time. It asserts that
all 50 artifacts survive reopening. A WAL checkpoint precedes each file-size reading.
Results are observations; changing the model's answer length or tool payload changes them.
The initial measurements and limitations are in `.scratch/knowledge-base/research/24-persistence-evidence.md`.

The running backend prepares its graph once at startup. After preparing a new paired version,
select it through section 5, then stop and restart the backend to adopt that version. It checks
the selected snapshot and both stores before accepting questions. Existing saved artifacts retain their original
evidence. There is no automatic replacement of the running graph.

### When it refuses

With no build, build the knowledge base first. For a stale or uncheckable build, follow the fixed
startup message to check the reader settings or rebuild. A failed artifact-restoration assertion
needs investigation; do not delete real saved investigations to make the probe pass.


## 4. Verify an isolated Neo4j graph version

Added 30 October 2026 by knowledge-base ticket 47.

### What it is for

Build a separate PostgreSQL/Neo4j pair from a frozen source copy, verify exact graph contents,
check graph write prevention before and after restart, then query an account. The working
application keeps its selected build until explicit selection and restart under section 5.

### Before you start

PostgreSQL and Docker Desktop must be running. Existing PostgreSQL builder and reader settings
must be present in `.env`. Also set `LI_GRAPH_ADMIN_PASSWORD` and `LI_GRAPH_READER_PASSWORD`
privately in `backend/.env` for the two human Browser logins (section 5). New builds refuse
missing or empty passwords before creating resources. Neo4j Community 2026.10.1 must be available locally:

```
docker pull neo4j:2026.10.1
```

The graph service listens only on localhost. Its serving account retains Community administrative
powers. This is the accepted development limitation in AUD-068, not production readiness.

### Run it

From the repository root, exercise the complete command with offline embeddings and dispose
only the version this command creates:

```
uv run --directory backend python -m scripts.build_graph_version --offline --dispose --report ../.scratch/knowledge-base/research/53-command-result.json
```

Offline embeddings test graph behaviour only. They cannot support a retrieval evaluation.
The version records this mode. To retain a version for further development inspection, omit
`--dispose`. To create real embeddings, also omit `--offline`; that makes paid provider calls.
The explicit `--dataset-dir` option wins over `LI_DATASET_DIR` in the environment, then `.env`,
then the bundled dataset. Neither form switches the active application pointer. Retained versions live under the ignored
`backend/.graph-versions/` directory. Each has its own PostgreSQL database and Docker volume.
No earlier build is automatically deleted.

### Open or check the result

The JSON report includes the account answer, build ID, preparation duration, five lookup timings,
and one container-memory observation. These measurements do not establish a capacity guarantee
or a speed improvement. A retained version's `complete.json` is written only after verification.
Its sibling `.env` holds serving credentials. Never copy that file into a report or ticket.

### When it refuses

A missing service produces a nonzero exit. Start Docker Desktop, confirm the pinned image exists,
and restart PostgreSQL with `brew services restart postgresql@18` if needed. Check the existing
builder and reader settings. An integrity or security failure requires diagnosis before retrying;
never bypass the verifier or edit source snapshots. Ordinary failed builds clean their own resources. If Docker is unavailable during cleanup,
the version directory is retained with `cleanup.json` naming the exact remaining resources.
Restore the unavailable service before removing those resources; retain the private state until
cleanup succeeds. Do not delete unrelated containers or databases.
The active application pointer is never changed by this command.

**Image appears present but cannot be found (B-147):** an Images-list entry can come from
Docker Desktop's cache while its Linux engine is asleep. Check the engine and image name:

```sh
docker version --format 'client={{.Client.Version}} server={{.Server.Version}}'
docker image inspect neo4j:2026.10.1 --format '{{.Id}}'
docker image inspect docker.io/library/neo4j:2026.10.1 --format '{{.Id}}'
```

Both image commands should resolve to the same ID. A 404 by name while inspect by the Images
list's exact ID succeeds can be a cache problem; it does not prove the image was deleted.
Check running workloads before an ordinary restart through Docker Desktop → Troubleshoot →
Restart Docker Desktop. Avoid data cleanup, factory reset, pruning or switching image stores
as an image-name remedy. If it recurs, capture local idle/cache log entries and the Desktop
application version separately from `docker version` (Engine/CLI). Check available Desktop
updates, then repeat the checks and the failed test. Docker documents cached operations in
[Resource Saver mode](https://docs.docker.com/desktop/use-desktop/resource-saver/).
These read-only checks passed after the author's 3 November update to Desktop 4.98.0 and
Engine/CLI 29.9.2. The original image ID and five stored containers were retained.

## 5. Select, restart and roll back a paired graph version

Added by T48; final development-migration procedure accepted under T49 on 1 November 2026.
T53 adds stable human logins and a fixed selected address, verified on 2 November 2026.

### What it is for

Adopt one verified source/PostgreSQL/Neo4j version on a planned restart. Saved investigations
and report downloads remain in the same SQLite memory file. Selection moves the selected graph
to fixed localhost ports but does not reload the backend's clients. Stop the backend before
selecting, then restart it. The previous complete pair remains available for rollback.

### Before you start

Use section 4's PostgreSQL, Docker and reader prerequisites. Run one selection command at a time.
Set `LI_GRAPH_ADMIN_PASSWORD` and `LI_GRAPH_READER_PASSWORD` privately in `backend/.env`.
Every new build requires both before creating resources. These create the stable `li_admin`
and `li_reader` Browser logins; the application keeps its separate per-build `li_serving` login.
In Community, both human logins have administrative powers. `li_reader` is read-only by
convention through Browser read access mode, not an enforced role (AUD-068). The serving
database's server-level read-only lock protects graph data for all users.
Keep each retained snapshot, PostgreSQL database, graph container/volume and private `.env`
together. Never edit a snapshot or completion marker. The default working pointer is
`backend/.knowledge-base.json`. An old PostgreSQL-only pointer is refused; restoring one also
requires the archived pre-migration code described below. No production guarantee is implied.

### Run it

Prepare and verify a complete version using section 4. A working version needs real embeddings;
its retained paid variant omits **both `--offline` and `--dispose`**. Keeping `--dispose`
would delete the new version before it could be selected. The exact offline disposable command is the tested operator
smoke check. T49's accepted working version reuses the checked original live passage vectors,
compared byte-for-value in the preparation evidence, rather than buying them again.
Offline vectors cannot support live evaluation evidence. Change into `backend/` before the
commands below. Use the report's generated build ID in place of `BUILD_ID`. Stop the current
backend with Ctrl-C, then validate/select the complete pair and restart it:

```sh
LI_GRAPH_VERSION=.graph-versions/BUILD_ID/complete.json
uv run python -m scripts.select_graph_version --state-file .knowledge-base.json --version "$LI_GRAPH_VERSION"
uv run uvicorn api.app:create_app --factory --port 8000
```

To return to the previous complete pair, stop the backend, validate/select it, then use the same
startup command. The incoming graph container must be running:

```sh
uv run python -m scripts.select_graph_version --state-file .knowledge-base.json --rollback
```

Rollback preserves source files and SQLite history. Re-selecting the already selected version
does not lose the rollback target. No build is automatically removed; retention remains AUD-057.
Selection and rollback recreate serving containers while keeping their data volumes and
read-only settings. A stopped outgoing container stays stopped. Its databases do not need to
answer to select a healthy replacement. The incoming graph receives `http://127.0.0.1:7474/browser/` and
`bolt://127.0.0.1:7687`; the outgoing graph receives random localhost ports. Other port holders
cause refusal before any changes. A failed move restores the original bindings; if recovery
itself fails, leave the backend stopped and recover the two named retained containers.
To give an existing running complete pair its human logins without a rebuild, run once
(repeating this reports existing users without resetting their passwords):

```sh
uv run python -m scripts.provision_browser_users --version-file "$LI_GRAPH_VERSION"
```

Then reselect that same version with the section 5 command to give it the fixed address.
Rollback is to a pair built by the same code rules. The current integrity check refuses any graph
with `used_address` edges (T50, 1 November 2026), so pairs built before T50, including the
retained `3d58516c…` and `eb6c7d59…`, open only under the code as of commit `012de46` or
earlier. Rolling back to one of them therefore means two steps, not one: select the retained
pair as above, and run the backend from a checkout of that earlier code. The T50 pair is
`f937ea59…`. The T51 pair `2d1bf85e…` (1 November 2026) follows the same code rules, so
rolling back from it to `f937ea59…` is the one-step rollback above.
For a separate rehearsal, add `--isolated` to selection and rollback, substitute
`.graph-versions/t49/rehearsal.json` for the state file,
port `8012` and a separate memory file. T49 used copied memory and a scripted account lookup.

Both evaluation entry points prepare unique source snapshots, PostgreSQL databases, Neo4j
instances and selection files, then dispose their own resources. Exact unchanged passage
vectors are copied from the checked selected version. Evaluation query embeddings, reranking
and answer-model calls retain their normal costs. Missing vectors, changed settings/source or
an offline version refuse live evidence. Evaluations never select their copy for the application.

### Open or check the result

Check `http://127.0.0.1:8000/api/overview` and reopen a saved investigation. The selected snapshot
supplies login analysis, alerts, graph queries and retrieval. Working-input changes wait for a
new build and restart. The credential-free pointer records current and previous completion
markers, each naming the shared identity, fingerprint and stores. Never share private `.env` files.

T49's sequential local rehearsal measured 21.235 seconds from legacy to paired readiness,
13.442 seconds for an update and 14.642 seconds for rollback. A stopped graph refused startup
in 8.839 seconds; graph restart plus application readiness took 59.896 seconds. Saved account
evidence reopened exactly after every restart. Actual lookup, S6 graph answer and document
self-retrieval passed on both pairs. These are observations, not promised limits. The first
archived cold start under concurrent evaluation builds exceeded 120 seconds; B-126 preserves it.
The author accepted the measured plan including this caveat. See
[T49 measurements](../.scratch/knowledge-base/research/49-lifecycle-measurements.json).

### When it refuses

A missing or changed snapshot, unavailable store, mixed pair, invalid marker or unverified write
protection prevents startup. The fixed error names preparing a replacement and selecting a
complete version. Restore only the services named by the retained marker, or select another
verified pair and restart. For a stopped graph, use `docker start CONTAINER_NAME`, with the exact
name from its marker, wait for readiness and restart the backend so it resolves current ports.
Never rebuild over a snapshot, remove an unrelated container, or overwrite the working sources.

A failed preparation/selection leaves the prior pointer intact. Partial startup closes both
clients. Rollback without a previous complete version refuses. The pointer replacement is a
same-directory rename, not a distributed transaction or a power-loss durability guarantee.
After such an event, restore an explicitly verified retained selection. Section 4 describes
failed-cleanup metadata; keep it until exact resource cleanup succeeds.

**Pre-migration implementation recovery:** T49 retains baseline code `13f5fdd`, its lockfile and
separate environment, original pointer and frozen source under ignored
`backend/.graph-versions/t49/legacy-recovery/`. Its archived backend `.env` is a local link to the
original `.env`; credentials are not copied into reports. The original PostgreSQL database is
retained. Stop the current backend first. From the current `backend/`, run:

```sh
LI_RECOVERY_ROOT="$PWD/.graph-versions/t49/legacy-recovery"
LI_DATASET_DIR="$LI_RECOVERY_ROOT/source" LI_KNOWLEDGE_BASE_STATE="$LI_RECOVERY_ROOT/selection.json" LI_MEMORY_PATH="$PWD/memory/investigations.sqlite" uv run --directory "$LI_RECOVERY_ROOT/code/backend" --frozen uvicorn api.app:create_app --factory --port 8000
```

This uses the old implementation and its old graph dependency in its own environment, with the
same saved investigations. It does not rewrite the new application's pointer. To leave this
recovery mode, stop it and run the current backend's ordinary startup command. The preserved
archive is a recovery copy, not a second graph engine maintained in the application.

## 6. Inspect a paired graph in Neo4j Browser

Added by T48 and accepted after the author's live walkthrough on 30 October 2026. Browser
replaces the retired Gephi workflow. It is an operator tool; the planned in-app Graph tab remains separate.

### What it is for

Inspect the organisation and the exact neighbourhood calculated by the core for each finding.
The neighbourhood includes permissions and device peers. Since T50 (1 November 2026) the graph
draws no `used_address` relationships: network nodes appear in the organisation view as facts,
reached only by passage mentions, and the finding view carries no address context.

### Before you start

Start Docker Desktop and PostgreSQL. Set the two Browser passwords in `backend/.env` as in
section 5. Use the selected pair or a complete isolated pair built with the current
`build_graph_version` command in section 4. Its serving container publishes HTTP and Bolt only
on localhost. Older pairs without an HTTP binding need a fresh build for this walkthrough.
The application selection stays unchanged. Offline embeddings are sufficient for graph inspection.
Neo4j Community retains administrative powers under AUD-068; read access mode alone is not a
permission boundary. The serving database's write protection is checked before preparation.

### Run it

For everyday access, open the selected graph using these settings:

| Setting | Value |
| --- | --- |
| Browser address to bookmark | `http://127.0.0.1:7474/browser/` |
| Connection URI | `bolt://127.0.0.1:7687` |
| Database | `neo4j` |
| Usual Browser login | `li_reader` |
| Reader password | `LI_GRAPH_READER_PASSWORD` in the main `backend/.env` |
| Administrative login | `li_admin`, using `LI_GRAPH_ADMIN_PASSWORD` from the same file |

Use this address each time. Selection and rollback move it to the selected build. Your human
login names and configured passwords stay the same. Opening Browser requires the selected
graph container to be running; it does not require rebuilding the graph, regenerating queries
or starting the application backend. Section 5 explains how to start a stopped graph.

To use saved inspection queries, open an existing inspection folder whose `inspection.json`
matches the selected build. The T53 walkthrough prepared
`backend/.graph-versions/2d1bf85ead1944709f5ab8cbd6ed4ad1/inspection-t53/` on 2 November 2026.
Use its files with the steps below while that build is selected. If the selected build changes,
prepare queries for the new build rather than reusing the previous build's parameters.

To prepare inspection files for an existing complete pair, use the `inspect_graph` command
below with that pair's build ID and a new output folder. Creating another graph is optional.
If you specifically want a separate offline inspection pair, build it from the repository root:

```sh
uv run --directory backend python -m scripts.build_graph_version --offline --report ../.graph-versions/t48-inspection-build.json
```

Use the `version_file` value from that report after `.graph-versions/` below. The command
runs inside `backend`, where retained pairs live. Choose a new output
directory each time. Replace `BUILD_ID` with the generated build ID:

```sh
uv run --directory backend python -m scripts.inspect_graph --version-file .graph-versions/BUILD_ID/complete.json --output .graph-versions/BUILD_ID/inspection
```

The command checks both stores and the source snapshot. It prepares all findings without paid
calls. Add `--finding-id F-...` to prepare just one finding. It never selects an application build.

### Open or check the result

Open `browser_url` from `inspection/inspection.json`. Connect to its `bolt_uri`, database `neo4j`,
user `li_reader`. Copy `LI_GRAPH_READER_PASSWORD` privately from the main `backend/.env` into
the login form. `li_admin` uses `LI_GRAPH_ADMIN_PASSWORD` from the same file. The application
continues using only `li_serving`. Neither human name provides enforced roles in Community;
read-only convention and the server lock are described in section 5 (AUD-068).
Do not paste credentials into queries, chat or screenshots. The report and saved queries contain
no password. The selected pair is always at `http://127.0.0.1:7474/browser/` with Bolt port
`7687`. The address moves only at operator selection or rollback. Isolated builds keep random
ports; regenerate their report after restarting them. Regenerate reports after selection too,
so their addresses match the intended build. Older complete pairs first need the section 5
one-off provisioning command.

1. Run `:access-mode read`. Run `identity.cypher` and compare both values with `inspection.json`.
2. Open Settings with the gear icon. Set Visualization node limit to `1000` and Record limit
   to `1000`. Ensure Automatically connect result nodes is off, so Browser does not add
   relationships beyond the core walk. The bundled Browser 2026.10.21 does not support `:config`.
   Increase the node limit before inspecting a result with more than 1,000 nodes. Each saved
   query returns one row containing all nodes/relationships and their counts. The graph canvas
   can still hide nodes; compare its visible counts to that row and the report. At a limit of 10,
   the T48 S6 view (then 55 nodes and 64 relationships, before T50 removed address edges)
   displayed “Initial display limit hit at 10 nodes” while its table retained the full result.
   Since T50 the S6 neighbourhood is 10 nodes and 9 relationships, and the organisation view
   170 nodes and 185 relationships. A partial canvas is not the full result. Do not expand nodes
   while comparing the exact saved neighbourhood.
3. Run `:style`, then upload `inspection.grass` and confirm Import in the preview. Node captions
   show stable IDs, whose prefixes identify their types. Zoom in to read captions. The results overview lists relationship types. Grants are red and device use
   green. All nodes currently share the `Entity` label, so node colour is uniform.
4. Paste `organisation-parameters.txt`, execute it, then execute `organisation.cypher`. Use the
   result frame’s Save and open in tab button to keep the query in the Queries sidebar. This view includes all organisation nodes and relationships,
   including isolated networks, but excludes passage references.
5. Choose a finding from `inspection.json`. Execute its `F-...-parameters.txt`, then `finding.cypher`.
   Use Save and open in tab to keep the query. Check `complete=true` and both counts against the report.
   Zero nodes means the finding reached no account under the core rules. The accompanying
   `F-...-context.json` records the period, the permissions caveat and the device peers.
6. Load the appropriate parameter file whenever changing views or reconnecting. A query against
   a different build/source returns no row; it is not a valid empty neighbourhood.

Passage nodes contain stable references only. Browser does not fetch passage text from
PostgreSQL. To inspect those references separately, run:

```cypher
MATCH (n:Entity {entity_type:'chunk'}) RETURN n.id AS passage_id ORDER BY passage_id;
```

This table has its own Browser record limit. It is not part of the organisation or finding view.
There is no portable graph export in this workflow.

### When it refuses

| Symptom | Action |
| --- | --- |
| Preparation refused | Check that both services run, the version is complete, and the output folder is new. Never edit the immutable snapshot |
| No Browser HTTP binding | Prepare a new isolated pair with the current command; do not alter the working application's selection |
| Query returns no row | Compare connection identity and reload parameters from the matching build |
| `complete=false` or counts differ | Stop the inspection and investigate; do not accept the view as complete |
| Canvas shows fewer nodes than the counts | Raise Visualization node limit in Settings, rerun, and compare again. Do not infer missing evidence from the canvas |

Retain the isolated pair for the author's walkthrough. There is no automatic removal after
inspection. Any later cleanup must identify only this pair; no global database or Docker cleanup
is part of inspection.

## 7. Check Python code with Ruff

Added for AUD-013 on 31 October 2026 after the author's lint-policy approval.

### What it is for

Check backend Python code using the project's reviewed rules. Ruff checks likely mistakes and
import ordering; Pyright remains the separate type checker. The policy keeps the pinned Ruff
defaults, explicitly includes import ordering, and relaxes twelve reviewed style preferences.
Intentional exceptions have a rule-specific comment explaining why they are allowed.

### Before you start

Run from the repository root. Install the locked development tools if needed:

```sh
uv sync --locked --directory backend
```

Ruff is pinned to 0.17.3 in `backend/pyproject.toml` and `backend/uv.lock`. VS Code should use
the backend Python environment. If its Ruff extension reports a version mismatch, use the
project's pinned tool rather than removing the version check.

### Run it

```sh
uv run --locked --directory backend ruff check .
```

This command checks without changing files. It needs no database, Docker service or API key.

### Open or check the result

`All checks passed!` and exit code 0 mean the current policy is satisfied. A warning includes
its file, line and rule code. Review the code's intent before fixing or adding an exception.
The policy is not a formatting mandate and does not establish runtime correctness.

### When it refuses

Diagnostics return exit code 1. Fix confirmed problems; use a specific explained exception for
an intentional pattern. Setup/configuration errors return exit code 2; check the locked tool
installation and configuration. Do not use blanket ignores or unsafe fixes to obtain a green
result. When checking for stale suppression comments, run the full policy: enabling only
`RUF100` can incorrectly classify comments for disabled rules as unused (B-125).

## 8. Run, review and mirror a model comparison

Added for T54 on 3 November 2026 (checkpoints 1 and 2).

### What it is for

Run T52's approved comparisons outside the working application: six compatibility sessions,
the 72-trial model screen and, later, the twelve-answer A/B/C calibration. Each run is a local
evidence bundle under `backend/evals/comparison/runs/<name>/`: a frozen `manifest.json`, an
append-only `events.jsonl` and `artifacts/`. The bundle is the original. Langfuse only ever
receives a copy, and nothing reads back from it.

The `dry-run` adapter answers every request with a fixed text, calls no model and costs nothing.
Checkpoint 3 adds `openrouter`, using the Responses API with pinned providers, standard service,
full conversation history and no evaluation-imposed output cap. Its native settings and provider
limits still need the six compatibility sessions. No live call or upload is authorised by creating
a run. The application's model is unchanged.

### Before you start

Run from the repository root with the locked tools (`uv sync --locked --directory backend`).
No database, Docker service or model key is needed. Confirm the frozen cases are current:

```sh
uv run --locked --directory backend python -m evals.comparison.fixtures --check
```

`Fixtures are frozen and current.` means the four case files, the separate gold files and their
manifest match a fresh build from the default dataset. Use `--write` only after an approved
change to a case; the new fixture version then appears in every later run's manifest.

To mirror to Langfuse, add `LI_LANGFUSE=on`, `LANGFUSE_PUBLIC_KEY` and `LANGFUSE_SECRET_KEY` to
`backend/.env` (`LANGFUSE_BASE_URL` defaults to `https://cloud.langfuse.com`). Leave
`LI_LANGFUSE` unset to keep mirroring off.

For paid execution, `OPENROUTER_API_KEY` must have a value in `backend/.env`. Obtain the author's
explicit execution go for the session first. Model confirmation and the US$25 planning budget
are separate from this go. Compatibility creation and bounded live commands were exercised
on 3 November 2026 for all six initial sessions. All tool exchanges completed; gpt-oss failed
the citation-format check. See the [live report](../.scratch/knowledge-base/research/54-live-compatibility-2026-11-03.md).
The shared compatibility repair and initial screening command also have live evidence.
The later screening command also ran on 3 November; live upload examples remain unverified.

### Run it

Create and run a compatibility run, then a screening run. Paths are relative to `backend/`:

```sh
uv run --locked --directory backend python -m evals.comparison new compatibility evals/comparison/runs/compat-dry --adapter dry-run
uv run --locked --directory backend python -m evals.comparison run evals/comparison/runs/compat-dry
uv run --locked --directory backend python -m evals.comparison new screening evals/comparison/runs/screen-dry --adapter dry-run
uv run --locked --directory backend python -m evals.comparison run evals/comparison/runs/screen-dry --until-slot 24
```

The last command stops after the first pass (24 trials), the approved setup checkpoint. Inspect
the setup, then continue with the same `run` command without `--until-slot`. A run that stops
part-way, for any reason, resumes with the same command. Trials already started are never run
again.

After explicit execution authorisation, create the separate live compatibility bundle:

```sh
uv run --locked --directory backend python -m evals.comparison new compatibility evals/comparison/runs/compat-live --adapter openrouter
uv run --locked --directory backend python -m evals.comparison run evals/comparison/runs/compat-live --execute-paid --until-slot 1
```

Creation loads no credentials and sends nothing. The second command can spend money. Review the
result, then increase `--until-slot` one at a time to 6. Check each session's tool round trip,
output contract, reported identity/settings and recording. Metadata or a plausible answer does
not prove native settings. Diagnose incompatible configurations before scoring; preserve the
original attempts and version any repairs.

The readiness repair on 3 November uses a separate bundle, `compat-readiness-1`.
Its shared connection-check prompt explicitly requires ASCII brackets, and adapter version 2
requests `debug.echo_upstream_body` on tool-bearing compatibility calls. The transformed
provider body is saved under each request's `artifacts/continuations/` reference as
`debug_events`. It is diagnostic evidence only: it is neither replayed into model input nor
included in a Langfuse mirror. Compare those native fields with the approved configuration;
the ordinary returned settings may merely echo gateway values.

The repair's creation and first bounded execution use:

```sh
uv run --locked --directory backend python -m evals.comparison new compatibility evals/comparison/runs/compat-readiness-1 --adapter openrouter
uv run --locked --directory backend python -m evals.comparison run evals/comparison/runs/compat-readiness-1 --execute-paid --until-slot 1 --cost-run evals/comparison/runs/compat-live
```

These names already contain the recorded live evidence; do not recreate or remove them.
For a future approved repair choose a fresh name, record its link to the original and repeat
all configurations affected by a shared setup change. Raise the slot bound one at a time.
Later screening must include both compatibility bundles with two `--cost-run` flags so all
known charges share the spending check. A `billing_disposition` note can explain an error's
documented billing treatment without changing an absent charge to a measured zero.

After all six configurations pass compatibility and their settings/limits have been reviewed,
create the live screen and begin with one trial:

```sh
uv run --locked --directory backend python -m evals.comparison new screening evals/comparison/runs/screen-live --adapter openrouter
uv run --locked --directory backend python -m evals.comparison run evals/comparison/runs/screen-live --execute-paid --until-slot 1 --cost-run evals/comparison/runs/compat-live --cost-run evals/comparison/runs/compat-readiness-1
```

Increase the bound as reviewed, to at most 24 before the setup checkpoint. The CLI requires
`--until-slot` for paid runs and refuses later screening slots until `--after-setup-review` is
supplied. This flag records that the review occurred; it does not perform the review.

The author approved the first 24 live screening answers on 3 November. After inspecting the
first answer's frozen input, route, recording and reference resolution, the bounded command is:

```sh
uv run --locked --directory backend python -m evals.comparison run evals/comparison/runs/screen-live --execute-paid --until-slot 24 --cost-run evals/comparison/runs/compat-live --cost-run evals/comparison/runs/compat-readiness-1
```

This stops at the setup checkpoint. Completion and resolving citations do not establish
answer quality; human labels stay blank until the author scores blinded answers.

Costs share one US$25 planning budget. `--cost-run` includes the compatibility bundle's known
cost in the spending check and is required for live screening. Repeat it for other paid bundles
sharing that budget, including any separate repair runs. The command rejects duplicate bundles.
Unknown charges stay unknown; inspect their OpenRouter records before claiming an exact total.
Before another command, review combined costs from all paid bundles. The runner pauses before
the next trial once known combined spending reaches US$15. The current trial and its retries can
cross that amount; cancellation does not establish that billing stopped. This is no hard charge
ceiling. `--after-spending-review` permits continuing only after that spending review.

After the first-24 review, the remaining two passes can use:

```sh
uv run --locked --directory backend python -m evals.comparison run evals/comparison/runs/screen-live --execute-paid --until-slot 72 --cost-run evals/comparison/runs/compat-live --cost-run evals/comparison/runs/compat-readiness-1 --after-setup-review
```

The corrected later-pass command ran on 3 November and stopped at slot 72 with exit 0:
71 saved answers and one explicit `no_answer`. It includes both compatibility bundles.
Known combined cost after two authenticated timeout settlements is US$0.281197, with
25 numeric charges still unknown across all paid bundles. The empty response and one
streamed rate-limit generation returned 404 on lookup; a 404 does not prove zero charge.
All 71 answers have v2 reference checks; eight answers retain unsupported-syntax warnings.
The author stopped here for a fresh-session blinded review. Do not rerun an empty or poor
answer to replace its original outcome. See the final checkpoint completion addendum and
B-155/AUD-081 for this run's limits.

Do not add `--after-spending-review` unless the US$15 review has occurred. Setup repairs in the
same bundle use explicit linked reruns; their slots follow the original schedule. For example,
after documenting an isolated adapter repair at the first-pass checkpoint, schedule only the
affected cells. The first linked screening rerun is slot 73:

```sh
uv run --locked --directory backend python -m evals.comparison rerun evals/comparison/runs/screen-live p1-O1-02-qwen3.8-27b-A --reason "documented adapter fix" --repair-version repair-1
uv run --locked --directory backend python -m evals.comparison run evals/comparison/runs/screen-live --execute-paid --until-slot 73 --cost-run evals/comparison/runs/compat-live --after-setup-review --reruns-only
```

`--reruns-only` skips pending original trials, so reaching slot 73 does not first spend money
on slots 25–72. The example is a command template, not permission for that repair. Shared
repairs must cover all affected configurations under T52's policy. Preserve repair versions
and originals; do not rerun a poor answer merely to replace its score.

Review in small batches. Each batch writes a blinded file and a blank label sheet:

```sh
uv run --locked --directory backend python -m evals.comparison checks evals/comparison/runs/screen-dry
uv run --locked --directory backend python -m evals.comparison review evals/comparison/runs/screen-dry --size 6
```

On 3 November the same `checks` and `review --size 6` commands ran against `screen-live`.
All 24 first-round final answers are saved; batch 1 has six items and blank labels.
The [first-round checkpoint](../.scratch/knowledge-base/research/54-first24-setup-checkpoint-2026-11-03.md)
records B-153/AUD-080: version-1 reference checks skip spaced/grouped/ranged citations.
The author-approved local repair uses `reference-resolution/2`. Recheck saved live answers:

```sh
uv run --locked --directory backend python -m evals.comparison checks evals/comparison/runs/screen-live
```

This command was tested on 3 November: 24 new checks, zero unresolved references, two answers
with unsupported citation syntax. A second run produced zero new checks. Earlier checks and
answers are preserved. The summary concerns newly appended checks only; zero new checks on
repeat does not clear earlier warnings. Inspect `deterministic_check` events with v2 in
`events.jsonl` for `unsupported_citations`. Two answers have explanatory prose inside five
status-reference brackets; their explicit refs exist, but the grammar warnings remain.
V2 accepts spaces, comma/semicolon groups and ascending same-prefix ranges with full endpoints.
Ranges allow hyphen, Unicode hyphen, nonbreaking hyphen, en dash or minus, at most 1000 refs,
with unpadded endpoints of at most nine digits. Other reference-like groups are flagged.
`citation_count` counts expanded reference occurrences, including repeats; it is not a score.
A zero unresolved count does not establish complete syntax coverage or source support.
The recheck needs no paid inference. Original manifest/source hash remains frozen; disclose
the parser/command-only source hash change at any later paid setup review.

**Latest scope correction, 4 November:** the current comparison upload is solely for
learning Langfuse. Reuse the existing connector with minimal truthful display changes.
Automated remote read-back/reconciliation and a permanent model-comparison operating
workflow are not required. Simple visual inspection is enough for this exercise. Real
operational tracing/evaluations belong to later running-app integration.

**Familiarisation upload, 4 November:** from the `backend` directory, the existing
connector sends the saved comparison without running a model:

```sh
LI_LANGFUSE=on .venv/bin/python -m evals.comparison mirror evals/comparison/runs/screen-live
```

This command enables Langfuse for that process only; `.env` stays unchanged. Use the keys
and regional address already configured there. Assistant scores have the `assistant.` name
prefix and identify the assessor in their comments. Saved score timestamps remain stable.
Human score names stay separate; reference-check comments retain syntax-warning counts.
This upload is solely familiarisation. Inspect it in the Langfuse interface; no automated
remote read-back or permanent comparison operating workflow is required. Request acceptance
is not a claim that the author has inspected the display. On 4 November the transfer completed with all 72 trial records and 1,099 scores
accepted, zero failed/unresolved latest statuses. The stock command was interrupted during
score transfer after traces completed; a temporary process-local requests Session helper
resumed the same CLI and completed it faster. The helper adds no new persistent interface.
The original command remains valid; its saved transfer statuses skip accepted records.
Author completed the visual walkthrough and accepted familiarisation on 4 November.
Open the configured Japan-region Langfuse project
and look for `t54-20261103/screen-live` or traces named `t54-screening`.

**Current screen exception, 4 November:** the author delegated all 71 assessments to
Codex. Read the [assistant assessment report](../.scratch/knowledge-base/research/54-assistant-screening-assessment-2026-11-04.md)
and `screen-live/artifacts/assistant-assessment/summary.json`. All scores are explicitly
`assessor_type=assistant`; original human sheets remain blank. The generic human workflow
below remains available, but do not import assistant judgments through `labels`, which would
record them as human. Official selection reports still consume human scores only. The familiarisation connector
now includes assistant scores explicitly (B-156/AUD-082); use the assistant report for the
comparison interpretation.
No live upload or new inference is authorised by the scoring delegation.

For blind assessment, use the supplied case evidence and assessor-only gold anchors.
Those expected findings are the marking guide. Keep candidate identity, configuration,
cost, timing and revealing traces hidden until initial scores are saved. Langfuse exposes
identity as well as expected findings, so it is not the initial blinded scoring surface.

Fill `artifacts/review/labels-batch-1.json` (the assessor's name, then a score of 0, 1, 2 or
"n/a" with a reason per criterion, and `true` or `false` with a reason per critical error).
Leave entries `null` to keep them unscored. An answer counts as scored only when every
criterion has a score and every critical error has been assessed. Then record it, export the
labels and read the report:

```sh
uv run --locked --directory backend python -m evals.comparison labels evals/comparison/runs/screen-dry evals/comparison/runs/screen-dry/artifacts/review/labels-batch-1.json
uv run --locked --directory backend python -m evals.comparison export-labels evals/comparison/runs/screen-dry
uv run --locked --directory backend python -m evals.comparison report evals/comparison/runs/screen-dry
uv run --locked --directory backend python -m evals.comparison mirror evals/comparison/runs/screen-dry
```

After the author's initial labels are saved, change a judgement only by revision, record
assistant notes, record review time, and finally record the selection. The review ID and trial
ID below are placeholders: take real ones from the batch file and the report.

```sh
uv run --locked --directory backend python -m evals.comparison revise evals/comparison/runs/screen-dry --review-id R-0000000000 --criterion facts --score 1 --reason "omits the MFA result" --assessor author
uv run --locked --directory backend python -m evals.comparison note evals/comparison/runs/screen-dry --review-id R-0000000000 --text "Support may deserve 1" --assistant codex
uv run --locked --directory backend python -m evals.comparison effort evals/comparison/runs/screen-dry --batch 1 --reviewer author --minutes 25 --answers 6
uv run --locked --directory backend python -m evals.comparison select evals/comparison/runs/screen-dry --chosen gpt-oss-120b --rationale "complete profiles on all four cases; cheaper than the other eligible model" --author author
```

Use `select --none --rationale "<diagnosis>"` when no model qualifies. For a documented setup
fix, schedule linked reruns and run them; `trace` shows one trial's full, unblinded record for
process and security review:

```sh
uv run --locked --directory backend python -m evals.comparison rerun evals/comparison/runs/screen-dry p1-O1-06-gpt-oss-120b-A --reason "case fence fixed" --repair-version repair-1
uv run --locked --directory backend python -m evals.comparison run evals/comparison/runs/screen-dry
uv run --locked --directory backend python -m evals.comparison trace evals/comparison/runs/screen-dry p1-O1-06-gpt-oss-120b-A
```

### Open or check the result

`status` (also printed after `run`) shows trial states, known cost, the number of requests
with unknown cost and retries. It prints a REVIEW POINT at US$15 known spending and once the
first 24 results exist. Unknown cost is never shown as zero.

The blinded batch is `artifacts/review/batch-<n>.json`. It shows the question, the case file,
the answer and the assessor-only anchors, and hides the model, design, settings, cost and
timing. The review-to-trial mapping is `artifacts/review/identity-map.json`: do not open it while
scoring. `blinding_limitations` lists answers that name a model or vendor in their own text.

`report` prints each model's status: `pending_run` until every scheduled trial has run,
`pending_scoring` while any completed answer has an unscored criterion, `not_eligible` with
its reasons, or `eligible`. It ranks nothing. Record the selection with its rationale.

Label exports are `artifacts/exports/labels-v<n>.json`. They are numbered, never rewritten,
and checked against the log on every export. `mirror` prints how many records were sent,
skipped, failed or left unresolved, and names each record it did not mirror.

### When it refuses

- `holds no run`: the path has no `manifest.json`. Check the path relative to `backend/`.
- `already holds a run`: a manifest is never overwritten. Choose a new run folder.
- `Fixtures are NOT current`: a case's source data or builder changed. Find out why before
  rewriting; a changed case needs the author's approval and a new fixture version.
- `REFUSED: ... Nothing was recorded.`: label errors (`n/a cannot excuse it`, `already has an
  initial label`, an unknown review ID), an assistant note before the author's initial labels,
  or an unknown trial or configuration. A refused sheet records nothing. Correct the sheet and run `labels` again. A changed judgement
  is a revision with its reason, never an edited initial label.
- `Langfuse mirroring is off`: expected while `LI_LANGFUSE` is unset. Nothing was sent.
- Paid execution without `--execute-paid` or `--until-slot`: refused before credentials load.
  Use them only after execution authorisation. A screen also requires its paid compatibility
  bundle through `--cost-run`. Passing the first 24 slots requires the recorded setup review.
- `NOT MIRRORED` with `failed`: Langfuse answered with an error, so nothing was accepted. Run
  `mirror` again later. With `unresolved`: no answer arrived, so Langfuse may hold the trace.
  Check the Langfuse project first. Use `mirror --resend-unresolved` only if the trace is
  missing, because a second copy would duplicate it.
- After an interruption, `run` reports trials marked interrupted and requests marked
  unresolved with unknown cost. They are never re-sent. A rerun is only an explicit, versioned
  repair under the approved setup-rerun policy.
