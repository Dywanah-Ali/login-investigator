# Admin manual

Tasks the author runs by hand: what each one is for, the exact commands, and what to do when it
refuses. One section per task. When a ticket adds a task an administrator runs, it adds a
section here in the same shape: **What it is for**, **Before you start**, **Run it**, **Open or
check the result**, **When it refuses**.

Commands are written to run from the repository root. In Claude Code, put `!` in front of a
command to run it in the session.

## Contents

1. [Export the knowledge graph and open it in Gephi Lite](#1-export-the-knowledge-graph-and-open-it-in-gephi-lite)
2. [Check retrieval without the agent](#2-check-retrieval-without-the-agent)
3. [Measure saved account-lookup evidence](#3-measure-saved-account-lookup-evidence)
4. [Verify an isolated Neo4j graph version](#4-verify-an-isolated-neo4j-graph-version)
5. [Select, restart and roll back a paired graph version](#5-select-restart-and-roll-back-a-paired-graph-version)

---

## 1. Export the knowledge graph and open it in Gephi Lite

Added 28 October 2026 by knowledge-base ticket 20.

### What it is for

A builder's wall chart: a file you open in Gephi Lite to inspect the synthetic organisation by
eye. It is not the analyst's view; the app's own Graph tab (phase 1) draws only the walk the
agent made. The export writes either the **whole graph** or **one finding's walk**: the accounts
the finding reached, their groups and assets, and the people who share a device or an address
with them.

### Before you start

| Need | How to tell |
|---|---|
| PostgreSQL running | The script refuses with the start command if it is not |
| A built knowledge base that matches the dataset | The script refuses with the rebuild command if it is missing or stale |
| The reader password in `backend/.env` | Already set up; the script refuses with a setup message if not |

### Run it

Whole graph:

```
uv run --directory backend python -m scripts.export_graph --output ~/Downloads/graph.gexf
```

One finding's walk, here S6:

```
uv run --directory backend python -m scripts.export_graph --finding-id F-password-spraying-d06a7545 --output ~/Downloads/s6.gexf
```

`--output` is required; the file goes exactly where it says. Any normal folder works.
**Never save into the dataset folder** (`backend/data/datasets/default/`): a new file there makes
the knowledge base stale and the app refuses to start (bug B-096). The script refuses that
location.

A success prints `Wrote <path>`.

**Finding IDs.** The app does not show them yet; the Alerts panel gains a finding ID column in
knowledge-base ticket 32. The IDs on the `default` dataset (from ticket 13) are below. They are
made from the log, so they change if the log is regenerated.

| Finding ID | First seen (UTC) | Address | Users |
|---|---|---|---|
| `F-new-country-f2ec8467` | 2026-10-02 08:17 | 203.0.113.70 | 1 |
| `F-brute-force-4d4fd1ab` | 2026-10-05 06:00 | 198.51.100.30 | 1 |
| `F-success-after-failures-cc1083a7` | 2026-10-05 06:00 | 198.51.100.30 | 1 |
| `F-password-spraying-4a90a716` | 2026-10-06 03:04 | 2.57.122.53 | 35 |
| `F-new-country-830a45a8` | 2026-10-06 13:47 | 91.142.73.116 | 1 |
| `F-password-spraying-d06a7545` (S6) | 2026-10-07 02:00 | 45.148.10.80 | 20 |
| `F-new-country-1ef7362b` | 2026-10-07 02:10 | 45.148.10.80 | 1 |
| `F-brute-force-0ce5e14e` | 2026-10-08 01:12 | 185.218.86.24 | 1 |
| `F-success-after-failures-9a4beef6` | 2026-10-08 01:32 | 185.218.86.24 | 1 |
| `F-new-country-4a3d5d22` | 2026-10-08 02:32 | 185.218.86.24 | 1 |

### Open the result in Gephi Lite

1. Open [Gephi Lite](https://gephi.org/gephi-lite/) in the browser.
2. Choose to open a local file and select the `.gexf` file.
   - To jump to a folder, press **Cmd + Shift + G** and paste its path.
   - A folder whose name starts with a dot (such as `.scratch`) is hidden on a Mac. Press
     **Cmd + Shift + .** in the file picker to show hidden items.
3. Nodes are coloured by type:

   | Colour | Node type |
   |---|---|
   | Blue | person |
   | Orange | group |
   | Red | asset |
   | Green | device |
   | Purple | network address |
   | Grey | document chunk |

4. **The whole graph is busy**: 320 of its 490 nodes are document chunks. For a clean view of the
   organisation, add a filter on `entity_type` in the Filters panel and leave out `chunk` (the
   author's ruling, 28 October 2026). A layout such as ForceAtlas 2 spreads the nodes apart.

Click a node to see its attributes, such as `department` or `sensitivity`. A `used_address` or
`used_device` edge carries its successful sign-in times in `times`.

### When it refuses

Every refusal starts with `Export refused:` and leaves no file.

| Message says | What to do |
|---|---|
| no knowledge base has been built | Build it: `uv run --directory backend python -m scripts.build_knowledge_base` (costs about $0.001 in embeddings) |
| built from older files or settings | The dataset changed since the build. Rebuild with the same command |
| PostgreSQL is not answering | Start PostgreSQL with the command the message gives |
| cannot be checked | Check the reader's login in `backend/.env`, or rebuild |
| No finding has this ID | Check the ID against the table above; the log may have been regenerated |
| The finding reaches no account | Expected for a spray with no successful sign-in, such as `F-password-spraying-4a90a716`: there is no walk to draw |
| outside the dataset folder | Choose another `--output` folder |

`Export failed (<ErrorName>)` means an unexpected error. Its details are hidden on purpose,
because database errors can carry hosts and credentials. Ask Claude or Codex to investigate.

**Colours all grey?** The file was written before the B-097 fix (28 October 2026): Gephi Lite
ignores colours that carry a transparency value. Export it again.

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
