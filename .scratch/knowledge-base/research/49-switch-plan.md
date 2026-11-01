# T49 development migration plan

Status: completed on 1 November 2026 after author acceptance, checks and reviews.

## Measured evidence

| Operation | Seconds |
| --- | ---: |
| Archived baseline readiness | 21.861 |
| Legacy-to-paired interruption | 21.235 |
| Paired update interruption | 13.442 |
| Paired rollback interruption | 14.642 |
| Unavailable graph startup refusal | 8.839 |
| Stopped graph recovery including app readiness | 59.896 |

[Rehearsal evidence](49-lifecycle-measurements.json) records exact saved-evidence reopening,
account lookup, S6 radius and stored-vector document self-retrieval for both versions. These
are sequential local observations, not upper bounds. The first archived cold start under two
concurrent evaluation builds exceeded 120 seconds before readiness. Separate import measurements
were 92.431 seconds for the archived environment and 16.502 seconds for the current environment.
B-126 retains that failed attempt. The successful rehearsal used a 300-second measurement
ceiling without changing application or database timeouts.

[Preparation and exact graph parity](49-preparation.json) identifies candidate
`3d58516ccfe84f74ade0ee255607fe19` and retained rollback pair
`eb6c7d59d40d4a94b87633593ae8649f`. Both use the checked source fingerprint
`e928c8dc54a9747896a58215fb06886664a601a3ea0c8de690af6ed3515f3afa`.

[Live Port evaluation](../../../backend/evals/results/2026-11-01-104006-806272-13987838.json)
passes 60/63 correctness and 15/15 security. All three Q04 Amelia-attribution failures remain
recorded under B-105/AUD-066. [Live retrieval evaluation](../../../backend/evals/results/2026-11-01-103813-673055-retrieval-7d7cff5dcc5c.json)
exactly matches the previous eight-question baseline for checks, graph paths/records, fused
and kept passage order and first-gold rank. [Comparison](49-retrieval-comparison.json) preserves
K04/K05/K06 as known failures; this is regression evidence, not a passing KB retrieval gate.

After author acceptance, retire the obsolete engine, complete the final full suite and independent
reviews, and only then change the working selection. No additional paid evaluation is authorized.

## What changes

Replace the legacy application's PostgreSQL-only selection with the verified paired selection.
Neo4j serves graph queries. PostgreSQL keeps passage content, metadata, embeddings and search.
The selected immutable source snapshot supplies every reader. SQLite investigations stay in
place. No source dataset, historical database or retained walkthrough graph is removed.

## Before selection

- Pin baseline code at `13f5fdd` and preserve its archive, lockfile, legacy pointer and immutable
  source under ignored `backend/.graph-versions/t49/legacy-recovery/`.
- Prepare two independent pairs from the same checked original live passage vectors.
  Compare all 320 passage records and vectors, 50 accounts, ten findings and 40 dated radii.
  Check frozen S6 gold independently. Save identities in `49-preparation.json`.
- Rehearse the original implementation and paired application on port 8012 with a separate
  pointer and copied SQLite memory. Reopen saved account evidence after each restart.
  Verify lookup, S6 radius and document self-retrieval using the existing live stored vector.
  This last check tests real retrieval plumbing without buying another query embedding.
- Run the approved 63 Port cases and all eight frozen retrieval questions against isolated
  copies of the candidate. Existing retrieval failures remain explicit.
- Complete backend/frontend/type/lint checks and review evidence.

## First selection and startup

After the author's measured-plan acceptance, verify `.knowledge-base.json` still has SHA-256
`09412e45a833a4a780144c7342506e3f480527b8855b410e88ac9889c4c2d993`.
Validate the candidate and rollback pair through `open_version`. Copy the prepared paired
selection into a sibling temporary file and rename it onto the working pointer. This initial
format transition is a one-time migration step; the ordinary selector deliberately refuses to
silently overwrite a legacy pointer. The existing legacy pointer remains in the recovery bundle.

Start the backend with its usual default pointer and original SQLite memory. Verify overview,
login source, lookup/S6 graph answers, document retrieval and reopened saved investigations.
Record actual readiness. No application server was listening at the initial inventory, so the
rehearsal provides the measured restart interruption rather than assuming an existing service.

## Rollback and recovery

Normal paired rollback, from `backend/`:

```sh
uv run python -m scripts.select_graph_version --state-file .knowledge-base.json --rollback
uv run uvicorn api.app:create_app --factory --port 8000
```

Stop the serving process before the restart command. Selection validates the retained previous
pair and changes only what the next process opens. Neither complete pair is deleted.

For a failure affecting the new implementation itself, stop it and run the retained baseline
code with its own pinned environment, preserved legacy pointer and source snapshot. Keep the
same SQLite memory path. The rehearsal proves that archived code can start and reopen evidence.
This recovery option remains available after NetworkX is removed from the current environment.
Use the original `.env` settings through the process environment; never print or copy credentials
into this plan. Restoring the old pointer alone is insufficient once the current code rejects it.

For a stopped graph service, start only the container named in that pair's completion marker,
wait for its readiness and restart the application. Do not remove volumes or rebuild over a
snapshot. An unavailable or mixed pair must refuse startup.

## Acceptance limits

Community serving retains administrative powers. This remains the explicit development
exception under AUD-068. Local timings are observations, not availability guarantees.
T45/AUD-062 retrieval gaps and T26's blocker remain. T25/T27 release only after T49 closes on
all required evidence. No production deployment or GitHub push is included.

## Completion

[Working activation](49-working-activation.json) passed with 28.140-second readiness, identical
overview and all 25 saved investigations. Both retained pairs were verified before selection.
The normal backend remains on port 8000. [Final verification](49-verification.json) separates
full-run findings from passing affected reruns. [Exact archived recovery](49-manual-recovery.json),
[native inspection](49-native-inspection.json), [offline operator smoke](49-command-result.json)
and [active fake-model storage probe](49-active-storage-probe.json) pass. B-134 preserves the
first harness import failure before selection; the reviewed correction preceded successful use.
Both recovery routes and the author's walkthrough pair remain retained. No extra paid run,
production claim, v1 change or GitHub push occurred.
