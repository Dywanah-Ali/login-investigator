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

Added by knowledge-base ticket 22.

### What it is for

Check whether corpus search finds every required passage in its top 20 and whether graph walks
return exactly the expected records and paths. This uses T21's eight questions. It does not ask
the agent to write an answer or judge the benign twins. Run it after each knowledge-base build.

### Before you start

PostgreSQL must be running, the published knowledge base must match the dataset, and the reader
password and `OPENROUTER_API_KEY` must be set in `backend/.env`. The command uses real query
embeddings and therefore makes a small paid request per text question. It does not rebuild the
database or embed the documents again.

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
graph paths, the integrity check, embedding usage and configuration fingerprint.
`backend/evals/results/retrieval-summary.md` keeps its history separate from the Port exam.

Every applicable check must pass for a question. A required passage outside the top 20 fails.
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
behaviour, not a reason to change their answer key. T23 adds the separate re-ranking stage.
