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

PostgreSQL must be running, the published knowledge base must match the dataset, and the reader
password and `OPENROUTER_API_KEY` must be set in `backend/.env`. The command uses real query
embeddings and therefore makes a small paid request per text question. It does not rebuild the
database or embed the documents again.

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

PostgreSQL must be running, the knowledge base built and fresh, and reader settings configured
in `backend/.env`. Use the default synthetic dataset, which contains Amelia Ward. Development
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

The running backend prepares its graph once at startup. After rebuilding a dataset, stop and
restart the backend with its existing launch command to adopt the new build. It checks freshness
and integrity again before accepting questions. Existing saved artifacts retain their original
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
application keeps its existing build. T48 and T49 own application integration and acceptance.

### Before you start

PostgreSQL and Docker Desktop must be running. Existing PostgreSQL builder and reader settings
must be present in `.env`. Neo4j Community 2026.10.1 must be available locally:

```
docker pull neo4j:2026.10.1
```

The graph service listens only on localhost. Its serving account retains Community administrative
powers. This is the accepted development limitation in AUD-068, not production readiness.

### Run it

From the repository root, exercise the complete command with offline embeddings and dispose
only the version this command creates:

```
uv run --directory backend python -m scripts.build_graph_version --offline --dispose --report ../.scratch/knowledge-base/research/47-command-result.json
```

Offline embeddings test graph behaviour only. They cannot support a retrieval evaluation.
The version records this mode. To retain a version for further development inspection, omit
`--dispose`. To create real embeddings, also omit `--offline`; that makes paid provider calls.
Neither form switches the active application pointer. Retained versions live under the ignored
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

## 5. Select, restart and roll back a paired graph version

Added by knowledge-base ticket 48. Native Browser inspection remains its next checkpoint.

### What it is for

Prepare a complete source snapshot with matching PostgreSQL and Neo4j stores, then select it
for a separately configured application's next restart. The running process keeps its current
version. Saved investigations and report downloads remain in the same SQLite memory file.
T49 owns switching the working application after acceptance.

### Before you start

Use section 4's PostgreSQL, Docker and reader prerequisites. Run one selection command at a time.
Keep the previous version's snapshot, database, container, volume and private `.env` together.
Do not edit a snapshot or completion marker. The default working pointer is
`backend/.knowledge-base.json`; use the separate pointer below for T48 verification.
Port 8012 must be free. No production permission or availability guarantee is implied.

### Run it

From the repository root, prepare a retained offline version:

```sh
uv run --directory backend python -m scripts.build_graph_version --offline --report .graph-versions/t48-prepared.json
```

The report's `version_file` is relative to `backend/.graph-versions/`. From `backend/`, set
the path below using that report's build ID, then select it:

```sh
LI_GRAPH_VERSION=.graph-versions/BUILD_ID/complete.json
uv run python -m scripts.select_graph_version --state-file .graph-versions/t48-selection.json --version "$LI_GRAPH_VERSION"
LI_KNOWLEDGE_BASE_STATE=.graph-versions/t48-selection.json LI_MEMORY_PATH=.graph-versions/t48-memory.sqlite uv run uvicorn api.app:create_app --factory --port 8012
```

`BUILD_ID` is a placeholder for the completed build's ID. Do not use the working app's port or
memory file. Offline vectors validate lifecycle and graph behaviour only. For a retrieval
evaluation, build without `--offline`, which makes paid embedding calls. Run the evaluator with
`LI_KNOWLEDGE_BASE_STATE` set to the source selection. Both evaluation entry points prepare their
own unique source snapshot, PostgreSQL database, Neo4j instance and selection file, then dispose
those resources when the run exits. Exact unchanged passage vectors are copied from the checked
source build so preparing the isolation does not buy the same embeddings again. Evaluation query
embeddings, re-ranking and answer-model calls retain their normal costs. Changed source/settings
or a missing stored vector refuse the copy. Offline versions refuse live evaluation evidence.
The existing no-build startup path remains available without database prerequisites.

For an update, prepare another version while the old process serves, then select its marker
using the same command. Stop the separate backend with Ctrl-C and restart with the identical
environment and command above. Selection itself does not switch an already running process.
To return to the previous complete version, run this from `backend/`, then stop and restart:

```sh
uv run python -m scripts.select_graph_version --state-file .graph-versions/t48-selection.json --rollback
```

Rollback validates the previous version before selection. It preserves the working source files
and SQLite history. Re-selecting the already selected version does not lose the rollback target.
No build is automatically removed; retained-build cleanup remains AUD-057.

### Open or check the result

Check `http://127.0.0.1:8012/api/overview` after startup. The selected snapshot supplies login
analysis, alerts, graph operations and document retrieval. Changing working input files has no
effect until a new version is built, selected and adopted by restart.

The selection file is credential-free and records the current and previous completion-marker
paths. Each marker names the shared build identity, fingerprint, source snapshot and stores.
Do not share private `.env` files. Query/connection waits are bounded, but a complete multi-query
investigation has no single promised duration. Restart measurements are local observations;
the maintenance window needs author acceptance before T49 switches the working application.

Measured on 30 October 2026 with two isolated offline versions: initial readiness 30.463 seconds;
update interruption 21.526 seconds; rollback interruption 26.914 seconds. Readiness meant successful
overview and investigation-list HTTP responses after full startup checks. A stopped graph refused
startup in 11.593 seconds. Starting that container, waiting for readiness and restarting the app
took 107.595 seconds. No model-provider request was made. These local observations include host
load during validation and are not production limits. See T48's saved measurement evidence.

### When it refuses

A missing or changed snapshot, unavailable store, mixed pair, invalid completion record or
unverified protection prevents startup. Restore the named version's PostgreSQL and Neo4j
services, or select a different complete retained version and restart. To restart a stopped
graph container, use `docker start CONTAINER_NAME`, taking the name from that version's
completion marker. Restart the application afterward so it resolves the current localhost
port. Never rebuild into an existing snapshot or overwrite working source files for recovery.

A failed build or publication leaves the prior selection intact. A failed partial startup closes
both clients. A malformed selection or a selection file in the source snapshot is refused.
Rollback with no previous complete version refuses. Keep failed-cleanup recovery state as
described in section 4. The local pointer replacement is one same-directory rename. It does
not promise distributed atomicity or durability through power loss; restore an explicitly
verified retained selection after such an event.

## 6. Inspect a paired graph in Neo4j Browser

Added by T48 and accepted after the author's live walkthrough on 30 October 2026. Browser
replaces the retired Gephi workflow. It is an operator tool; the planned in-app Graph tab remains separate.

### What it is for

Inspect the organisation and the exact neighbourhood calculated by the core for each finding.
The neighbourhood includes permissions, device peers and shared-address context. A purple
`used_address` relationship is context, not evidence of exposure or overlapping sessions.

### Before you start

Start Docker Desktop and PostgreSQL. Use a complete isolated pair built with the current
`build_graph_version` command in section 4. Its serving container publishes HTTP and Bolt only
on localhost. Older pairs without an HTTP binding need a fresh build for this walkthrough.
The application selection stays unchanged. Offline embeddings are sufficient for graph inspection.
Neo4j Community retains administrative powers under AUD-068; read access mode alone is not a
permission boundary. The serving database's write protection is checked before preparation.

### Run it

From the repository root, first build a separate offline inspection pair:

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
user `li_serving`. Copy the password privately from this build's `.env` file into the login form.
Do not paste credentials into queries, chat or screenshots. The report and saved queries contain
no password. After a container restart, regenerate into a new output folder to refresh its
localhost ports.

1. Run `:access-mode read`. Run `identity.cypher` and compare both values with `inspection.json`.
2. Open Settings with the gear icon. Set Visualization node limit to `1000` and Record limit
   to `1000`. Ensure Automatically connect result nodes is off, so Browser does not add
   relationships beyond the core walk. The bundled Browser 2026.10.21 does not support `:config`.
   Increase the node limit before inspecting a result with more than 1,000 nodes. Each saved
   query returns one row containing all nodes/relationships and their counts. The graph canvas
   can still hide nodes; compare its visible counts to that row and the report. At a limit of 10,
   the verified S6 view displayed “Initial display limit hit at 10 nodes” while its table retained
   55 nodes and 64 relationships. A partial canvas is not the full result. Do not expand nodes
   while comparing the exact saved neighbourhood.
3. Run `:style`, then upload `inspection.grass` and confirm Import in the preview. Node captions
   show stable IDs, whose prefixes identify their types. Zoom in to read captions. The results overview lists relationship types. Grants are red, device use green and
   address use purple. All nodes currently share the `Entity` label, so node colour is uniform.
4. Paste `organisation-parameters.txt`, execute it, then execute `organisation.cypher`. Use the
   result frame’s Save and open in tab button to keep the query in the Queries sidebar. This view includes all organisation nodes and relationships,
   including isolated networks, but excludes passage references.
5. Choose a finding from `inspection.json`. Execute its `F-...-parameters.txt`, then `finding.cypher`.
   Use Save and open in tab to keep the query. Check `complete=true` and both counts against the report.
   Zero nodes means the finding reached no account under the core rules. The accompanying
   `F-...-context.json` records the period, permissions caveat and separate address context.
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
