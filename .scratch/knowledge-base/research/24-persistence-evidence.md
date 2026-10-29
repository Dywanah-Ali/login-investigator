# T24 persistence and lifecycle evidence

29 October 2026. Astra implementation. Scope: one account lookup through the existing agent,
saved evidence and application lifecycle. Broader storage design remains deferred as AUD-065.

## Artifact and persistence path

`KnowledgeBase.lookup_account` reads the prepared graph. It accepts a username or stable person
ID, returns copied account/group records and membership paths, and does not query PostgreSQL
per question. The application opens that graph using the read-only role.

The tool's successful artifact contains `schema_version: 1`, `tool: lookup_account`, a snapshot
`basis`, `status`, the account record (`person_id`, username, display name, department, country,
entity type), group records (ID, name, kind, entity type), and member-of paths as node IDs.
A missing account has `not_found`, a null account and empty groups/paths. With no build the tool
returns an unavailable status and a plain explanation. It never guesses an owner or privilege.

The model receives only the short labelled briefing: username, owner, department, and group
names/kinds. The shared tool wrapper encloses this in a source-labelled, untrusted-data fence.
The model wrapper removes artifacts from message copies, including on later turns; saved
messages retain the originals. Report transcripts use message text only.

The tool returns `(content, artifact)` using LangChain's content-and-artifact format. The artifact
lives on `ToolMessage.artifact`, inside the investigation's LangGraph message state, persisted by
SQLite checkpoints and intermediate writes. It is not a second application-owned artifact table.
Reopening through the checkpointer needs no source lookup. Existing tool views receive only the
briefing; full evidence API projection and downloads remain the later tickets' work.

Reports already persist as JSON in a named AI message. Downloads render that saved report to PDF
without calling a model. PDF bytes are not stored, so a later download can have a new generation
timestamp while retaining the report's saved content.

## Storage measurement

Command, run from repository root:

```sh
uv run --directory backend python ../.scratch/knowledge-base/research/24-storage-probe.py
```

Uses the current checked graph through the reader role, a fake model, and disposable SQLite
memory. Repeats Amelia Ward's account lookup in one investigation with distinct tool-call IDs
and short fixed answers. No paid model calls, real investigation writes or source writes.
Counts/bytes come from SQLite's checkpoint and intermediate-write tables. File size is measured
after a WAL checkpoint/truncation so it includes the persisted pages rather than omitting a WAL.
Payload byte counts exclude metadata and SQLite page/index overhead.

| Completed lookups | Checkpoints | Checkpoint payload bytes | Intermediate writes | Write payload bytes | SQLite file bytes |
|---|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 | 0 | 20,480 |
| 1 | 7 | 10,996 | 9 | 1,733 | 40,960 |
| 10 | 70 | 679,083 | 90 | 17,330 | 811,008 |
| 50 | 350 | 15,815,671 | 450 | 86,770 | 16,404,480 |

One artifact serialized as JSON: **601 bytes**. Latest saved state after 50 lookups contains 50
artifacts. Full close/reopen and latest-state retrieval took **0.0181 seconds** and preserved
all artifacts exactly. Graph preparation, including the staleness check, open and integrity
check, took **4.9589 seconds** in this run. These are single local observations, not performance
targets or a concurrency test. Concurrent development/eval activity can affect timing.

The larger file is predominantly checkpoint payload, not the standalone artifact. Keeping
earlier growing message states repeats evidence across checkpoints; keeping artifacts outside
model input does not prevent that storage growth. This supports the deferred AUD-065 review
without selecting pruning, deduplication, retention or migration now.

## Verification boundaries

- Door 3/4 tests use a fake model and real disposable memory plus PostgreSQL fixtures.
- The model observes only briefings while saved messages preserve full artifacts.
- Source lookup is disabled during the reopen proof; a later model turn still receives no artifact.
- Lifecycle tests count real graph preparation/integrity checks, exercise separate investigations,
  verify the reader's write refusal and pool cleanup, and inject integrity/startup failure.
- Rebuild test publishes a new dataset build while the app runs, confirms the old checked instance
  remains in use, then confirms restart adopts the rebuilt source.
- Existing report-download regression covers restart and reading without a model.
- Browser fake-API test covers lookup progress through stream completion and redraw.

Final suite counts, review disposition and live Port evaluation are recorded in the T24 ticket.

## Live evidence

The Port API evaluation passed its existing gates at 62/63 overall and 15/15 security:
`backend/evals/results/2026-10-29-204751-654728-fa8f3e8f.json`. Q04 run 1's compromise-attribution
check remains failed; the answer contains Amelia's three successes and an introductory possible
compromise statement. B-105/AUD-066 records the grading concern without changing its score.

A separate isolated API smoke check asked who owns Amelia Ward's account, her department and
groups. The real agent chose `lookup_account` and returned Amelia Ward, IT, All Staff (baseline)
and IT Admins (privileged). The full short answer and tool result are saved in
`24-live-lookup.json`. Its temporary API process exited and its disposable memory was removed.
