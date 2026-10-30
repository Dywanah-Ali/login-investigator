# 48: Integrate updates, rollback and native graph inspection

Type: build
Status: resolved
Blocked by: 47
Blocks: 49
Phase: 0
Model: strongest (Fable 5.1 or Astra)
Rigour: Tier 3

## What to build

A separately configured application instance investigates one coherent source snapshot using
its matching PostgreSQL and Neo4j builds. The operator can prepare an update, select it for
restart, return to the previous complete version and inspect the graph in Neo4j Browser.
Saved investigations keep their original evidence through these changes.

## Decisions implemented

T46's complete-version activation/rollback, stable public contracts and native inspection
replacement for Gephi. Preserve the in-app Graph tab's planned saved-artifact behaviour;
Neo4j Browser is an operator inspection tool, not a new analyst screen.

## Checkpoint 1: coherent application startup and queries

- [x] Present the strongest Model line and obtain/record the author's confirmation before coding.
- [x] Open one knowledge-base context per backend process owning the PostgreSQL pool and Neo4j
      driver. Validate the chosen source snapshot, pair identity/readiness, independent graph
      integrity and serving protection before accepting requests. Close both clients after
      normal shutdown and any partial startup failure.
- [x] All login analysis, alerts, agent log tools, graph operations and retrieval use the same
      selected snapshot. Editing working inputs does not change the published version; tampering
      with the selected snapshot or selecting mismatched stores fails closed with fixed errors.
      Preserve the existing no-build startup behaviour.
- [x] Existing tool names, inputs, briefings, artifacts and stable IDs stay compatible. Database
      waits at asynchronous call sites run off the event loop. Test bounded timeouts, unavailable
      services, cancellation and concurrent investigations without mutable-state leakage.
- [x] Saved investigations and original artifacts survive close/reopen and version changes
      without querying the replacement graph to reconstruct old evidence. Preserve report
      downloads. No SQLite retention or memory migration is introduced.

## Checkpoint 2: updates and rollback

- [x] Prepare and validate a complete replacement while the old version remains selected.
      Publish a credential-free pointer only for a matching ready pair and source snapshot.
      Adopt it on a planned restart; do not add live hot-switching.
- [x] Refuse mixed stores, missing/false completion records and changed source snapshots.
      Inject failure during build/publication and verify the previous selection is intact.
      Exercise missing PostgreSQL and graph service cases and failure after partial startup.
- [x] Retain the previous pair plus its source snapshot. An explicit rollback restores that
      coherent version through restart, including login evidence, graph and document retrieval.
      Recovery must not erase saved investigations or overwrite the original working source files.
- [x] Test failure cleanup and isolation from the working application, including uniquely named
      resources/state for tests and evaluations. Record limitations of local pointer atomicity;
      do not imply distributed or power-loss guarantees without evidence.
- [x] Measure actual application restart interruption and recovery steps. Present the measured
      maintenance window for author acceptance before T49 switches the working application.
      No automatic pruning or retention policy is added; AUD-057 remains separately tracked.

## Checkpoint 3: native graph inspection

- [x] Provide saved/tested Browser queries for the organisation and a finding's neighbourhood.
      Match the same core walk's exact node/edge identities, including device peers and
      shared-address context; independent Browser logic must not silently redefine the radius.
- [x] Identify the connected build and source version. Verify styling and node/result limits
      so a truncated display cannot be mistaken for the full result. Use the read-only serving
      graph and document the accepted Community administrative limitation.
- [x] Explain that passage nodes are references and Browser does not automatically fetch text
      from PostgreSQL. No GEXF file or alternative portable graph export is promised.
- [x] Record the author's live walkthrough of organisation and finding views. Only after that
      acceptance retire the Gephi command and its format-specific tests/manual instructions.
      Preserve historical T20 evidence and the future in-app Graph tab scope.
- [x] Update the admin manual for every adopted build, inspection, activation, rollback and
      recovery task, and test its commands exactly as written. Secrets remain outside outputs.
- [x] Relevant safety net/type checks pass; required two-axis review is triaged. Run agreed
      eval gates for any agent-behaviour change. Record all bugs and remaining concerns.

## Boundaries and handoff

Demonstrate in a separately configured instance before T49 switches the working application.
No new API/UI scope, automatic deletion, Enterprise purchase or production deployment. T49
owns final acceptance, switching and removal of remaining obsolete NetworkX paths.

## Inputs

- [T46 ruling](46-graph-store-architecture-review.md), [T47](47-neo4j-build-and-graph-answers.md).
- [Current spec](../spec.md), [impact inventory](../research/46-impact-inventory.md).
- [Paired-build proof](../research/46-parity-and-pair-proof.md).

## Comments

- 2026-10-30 — Checkpoints 1–2 complete. Full backend run: 709 passed in 1186.38 seconds,
  exit 1 from one known B-094/AUD-061 teardown privilege error in unchanged
  `test_integrity_rejects_corruption[extra]`. Its exact idle leftover
  `li_test_b94165a0c68e` was dropped without FORCE; the affected test reran clean,
  1 passed in 2.58 seconds. No test assertion failed. Both type checks and whitespace
  checks pass. Frontend: 150 passed; six existing AUD-009 lint warnings remain.
  No isolated graph containers/volumes or port-8012 backend remain. No live paid agent
  eval ran because prompts, tools and answer behaviour did not change; T49 retains its
  migration evaluation gates. Checkpoint 3 and author maintenance-window acceptance
  before T49 remain open. No push or working-application switch.

- 2026-10-30 — Clean focused rerun with pgAdmin closed: 21 passed in 308.96 seconds,
  no teardown errors. Covers paired lifecycle, selection refusals and the previously affected
  retrieval integrity guard. Both type checks passed; six pre-existing frontend lint warnings
  remain. The separate frontend rerun passed all 150 tests in 28.27 seconds.
- 2026-10-30 — Independent review rechecks cleared both axes: Standards 0, Spec 0.
  The final no-build evaluation publication race was reproduced and fixed using a private
  absent pointer. Review history: `reviews/48-lifecycle-code-review-2026-10-30.md`.
  Evaluation lifecycle/entry-point checks passed 19 tests; the added no-build race check
  separately passed. Final full safety-net results are recorded in this ticket.
- 2026-10-30 — Cleanup: the author deleted `li_kb_86d2da6633c7`; absence was verified.
  After pgAdmin closed, exact owned measurement pairs `li_kb_4e514dfe0a9e` and
  `li_kb_412c292a4690`, plus failed-run pairs `li_kb_16c50c1acb04` and
  `li_kb_f8ee7ed0346f`, were verified without attached sessions and disposed with their
  graph resources and snapshots. No active or historical retained application build was
  deleted. The working pointer SHA-256 remains
  `09412e45a833a4a780144c7342506e3f480527b8855b410e88ac9889c4c2d993`.
- 2026-10-30 — The lifecycle rerun before pgAdmin closed recorded 16 passes, four failures
  and one cleanup error. Its loaded connection assertions counted unrelated pgAdmin sessions;
  the corrected assertions count only the configured reader. The update/rollback test's
  teardown also met B-094/AUD-061. Exact resources were recovered as above; a clean rerun
  with pgAdmin closed is required before checkpoint acceptance.

- 2026-10-30 — Live separate-instance measurements: initial HTTP readiness 30.463 s;
  update interruption 21.526 s; rollback 26.914 s; unavailable-graph startup refusal 11.593 s;
  graph-service recovery plus app readiness 107.595 s. Readiness checks overview and
  investigation-list responses after full preparation. No provider request was made, both
  builds used offline embeddings, and the working pointer hash stayed unchanged. Evidence:
  `research/48-lifecycle-measurements.json` and its saved harness. Author maintenance-window
  acceptance remains required before T49 switches the working application.
- 2026-10-30 — Initial independent review: Standards 1, Spec 2. Both identified independent
  PostgreSQL cleanup after graph-close failure; Spec also identified evaluation resource
  isolation. B-117/B-118 retain the findings. The evaluation lifecycle rebuilds fresh stores
  and sources using exact stored passage vectors from the checked original build, with a
  post-build fingerprint match and no fallback. Query/model calls remain unchanged. This is
  resource isolation, not new retrieval behaviour or a new embedding model.

- 2026-10-30 — Author offered a fresh session after lifecycle checkpoints. Agreed to complete
  and verify checkpoints 1–2, then hand off checkpoint 3. No Browser service or UI work started.
  An exploratory radius-projection test passed, but its unused helper/test were removed so the
  lifecycle commit remains focused. T48 stays open; Gephi remains until native walkthrough acceptance.

- 2026-10-30 — Author confirmed T48 and that Codex is set to Astra. Implementation baseline:
  `ccf5348`. Use the agreed spec Testing Decisions doors 2, 3, 4 and 6 for core lifecycle,
  saved evidence, application startup and retrieval. Checkpoint 1 precedes update/rollback
  and native inspection. Working application selection remains untouched until T49.
- 2026-10-30 — Documentation: neo4j Python 6.1.0 via Context Hub `neo4j/package`;
  [driver concurrency](https://neo4j.com/docs/python-manual/current/concurrency/):
  one process-owned driver, per-call sessions, explicit close; synchronous network calls
  require worker dispatch at asynchronous callers. Existing T47 parameterised query and timeout
  documentation applies to the unchanged pinned driver.
- 2026-10-30 — Documentation: Python 3.12 [tasks, threads and shielding](https://docs.python.org/3.12/library/asyncio-task.html);
  checked worker dispatch and cancellation ownership. Reuse T24's FastAPI 0.143.1 lifespan
  documentation for the unchanged before-yield/after-yield lifetime, and T47's SQLAlchemy
  2.1.6 async engine documentation for explicit disposal. API contracts remain unchanged
  except documenting the already approved paired source selection.
- 2026-10-30 — Native inspection documentation: Context Hub has no Browser guide;
  checked official [Browser settings](https://neo4j.com/docs/browser/operations/browser-settings/)
  and [visual tour](https://neo4j.com/docs/browser/visual-tour/): recordLimit, maxVizNodes,
  saved queries, connection identity and read access mode. Runtime verification and the
  author's walkthrough are still required; documentation alone is not acceptance.
- 2026-10-30 — Psycopg 3.3.6: Context Hub `psycopg/package` covers 3.3.3; checked the
  stable connection keyword behaviour against PostgreSQL 18's official
  [libpq options](https://www.postgresql.org/docs/18/libpq-connect.html) and
  [statement timeout](https://www.postgresql.org/docs/18/runtime-config-client.html).
  Paired readers bound connection/pool waits to 5 seconds, lock waits to 5 seconds and statements
  to 10 seconds. Existing builders keep their prior settings. Real slow-query refusal is tested.

- 2026-10-30 — Created using `to-tickets` after author approval. Native inspection replaces
  the initially proposed GEXF-preservation work. No code or live walkthrough completed yet.

- 2026-10-30 — Checkpoint 3 resumed on the author's instruction; Astra already confirmed.
  Browser parameters are derived from the core radius, with directed device/address peer
  edges and build/source guards. The organisation view excludes passage references; those
  remain inspectable separately. New serving containers expose Browser HTTP on localhost
  only, alongside existing Bolt. Gephi remains until the author's walkthrough acceptance.
- 2026-10-30 — Documentation: Neo4j Community 2026.10.1 / driver 6.1.0; Context Hub search
  has driver coverage but no Browser guide. Reused T47/T48 driver parameter/session notes;
  checked official [Browser settings](https://neo4j.com/docs/browser/operations/browser-settings/),
  [styling](https://neo4j.com/docs/browser/operations/browser-styling/) and
  [parameters](https://neo4j.com/docs/browser/operations/query-parameters/): read access mode,
  recordLimit/maxVizNodes, GraSS captions/relationship colours and :params maps.
- 2026-10-30 — Browser verification harness: installed Playwright 1.61.1; Context Hub
  `playwright/playwright` 1.60.0 documents the reused stable Chromium/context/locator APIs.
  The harness uses a fresh browser context and never prints credentials or records login traces.
  No dependency added to the application.

- 2026-10-30 — Native inspection runtime checks: organisation 170 nodes/326 relationships;
  S6 55/64, complete TRUE and matching source/build identity. Browser 2026.10.21 settings,
  explicit GraSS import, captions and colours checked; auto-connect off. Node limit 10 produced
  an explicit truncated-canvas warning while the table retained 55/64; restoring 1000 restored
  the full graph. Record limit 1 retained the full one-row query result. Evidence:
  `research/48-native-inspection-verification.md`. Independent final reviews: Standards 0,
  Spec 0. Author live walkthrough remains pending, so Gephi is retained and T48 stays open.
- 2026-10-30 — Verification so far: native/retained-export focused suite 11 passed in 265.43 s;
  parameter syntax regression separately passed; frontend 150 passed in 44.53 s; both type
  checks pass; six existing lint warnings remain. Full backend and final native-expression
  test run pending. B-119 through B-123 retain the environment, fixture and Browser iterations.
- 2026-10-30 — Final native regression suite passed: 2 tests in 238.66 s, including live Cypher
  evaluation of generated Browser parameter syntax and exact peer/core identities. The final
  walkthrough command succeeded with output in the isolated pair's `walkthrough/` directory.
  The pair `05f15cfcb66b48aaa7e2c5cfddd116c3` is retained for the author's live acceptance.

- 2026-10-30 — Full backend safety net passed cleanly: 710 tests in 1439.60 s (23:59),
  no teardown errors. That run collected before the final parameter-syntax test was added;
  the final native suite separately passed both tests in 238.66 s. Frontend 150 passed,
  both type checks clean, six existing lint warnings. No provider calls or live agent eval:
  no prompts, tool contracts or answer behaviour changed. Final two-axis rechecks both clear.
  The author requested step-by-step Browser guidance; live walkthrough is in progress,
  with no acceptance or Gephi retirement inferred.

- 2026-10-30 — Author live walkthrough: connected to the retained inspection pair; screenshot confirms exact build/source identity. Author confirmed display limits, auto-connect off and read mode. Organisation screenshot confirms 170 nodes/326 relationships. After styling instructions, author responded positively. Finding view and explicit final native-inspection acceptance remain pending; Gephi is retained.

- 2026-10-30 — Author completed the S6 live view: graph screenshot shows the styled neighbourhood and selected UK office address; table screenshot confirms matching build/source, node_count 55, relationship_count 64 and complete TRUE. Explained shared-address context and passage-reference/PostgreSQL-text boundary. Both native views have been walked through; explicit acceptance requested before Gephi retirement.

- 2026-10-30 — Author explicitly accepted native Browser inspection as the Gephi replacement
  and instructed retirement. Removed `scripts/export_graph.py`, the GEXF writer/core export
  method and `test_graph_export.py`; replaced active manual instructions with a native-inspection
  link. Historical T20/spec/bug evidence remains. Native identity, device-peer and address-context
  coverage replaces format-specific checks. Remaining NetworkX query removal stays in T49.
  Post-retirement import/type/core regression checks and review are in progress.

- 2026-10-30 — Post-retirement checks passed: 53 knowledge-base, graph and native-inspection
  tests in 160.11 s, no failures or teardown errors. Pyright clean. Retirement review:
  Standards 0, Spec 0 after updating closure wording. Full pre-retirement backend run was
  710 clean passes; final native-expression suite separately passed 2; frontend 150, clean
  frontend types and six existing lint warnings. No further application code changed afterward.
  All T48 criteria are evidenced. T48 resolved; T49 is next. Working application pointer remains
  unchanged; no push, paid provider call or maintenance-window acceptance is implied.

## Answer

Completed paired startup, update/rollback, saved-evidence continuity and isolated evaluations in
checkpoints 1–2. Checkpoint 3 now provides core-derived native Browser inspection with exact
node/edge identities, build/source guards, verified styling and display-limit behaviour. The
author completed organisation and S6 views and explicitly accepted the replacement. Gephi's
command, writer, public export method, format-specific tests and active manual instructions are
retired; historical T20 evidence remains. The native walkthrough pair is retained separately.
T49 owns final migration evaluation, maintenance-window acceptance, working-app switch and
remaining obsolete NetworkX removal. AUD-068 remains the production-readiness gate.
