# Map: knowledge-base

Label: wayfinder:map

## Destination

A knowledge base inside the Login Investigator, built around a knowledge graph with RAG as part of
its ecosystem, that gives the investigator agent context about the threat behind a login pattern,
so an alert becomes an explained risk rather than a flagged row. The use case is chosen for the
value it adds to the app, not for the sake of demonstrating RAG.

## Notes

- **Current frontier, 2 November 2026: T52 resolved.** Objective/evidence review, candidate
  dispositions and downstream reconciliation are complete. AUD-076 closes as a decision
  review only. [T54](issues/54-early-langfuse-evaluation-integration.md) is next by the
  author's approved order, with its own model confirmation and build/readiness gates.
  T45 selects guidance sources for approval; T26 integrates; T55 owns expanded data before
  T40. B-143's K03 correction stays with T40 under author review; B-145 fixes the mistaken
  T51 handoff. No application acceptance, gold change or paid execution is claimed.

- **T52 ownership approved, 2 November 2026:** T45 selects guidance sources for author
  review; T26 integrates approved guidance; new [T55](issues/55-thirty-day-investigation-dataset.md)
  owns the 50-person/30-day dataset before T40. Allocation is settled, source/dataset design
  approval remains with those tickets. T52 final closure review is next; T54 stays blocked.
  No build or paid execution started.

- **T52 downstream reconciliation, 2 November 2026:** detailed criteria in T26/T45,
  T27–T30, T34/T40/T42 and active spec summaries now reflect the approved sole objective,
  bounded context, windows, evidence limits and preserved gates. Candidate dispositions
  recorded in T52. Guidance-source/data ownership proposal remains for author ruling;
  T52 claimed and T54 blocked. No code, gold, threshold or runtime evidence changed.

- **Definitive T52 scope, author approved 2 November 2026:** reliable login investigation
  is the sole phase-0/1 objective. Keep bounded impact and directly connected activity
  context. Defer standalone full asset inventory, exhaustive permission-path presentation
  and reverse asset exposure. Supersedes broader E04 interpretation and earlier scope
  summaries. Next: reconcile downstream requirements and evidence/data ownership. T52
  claimed; T54 blocked. No code/gold/threshold changes. See spec Current scope ruling.

- **T52 scope clarification, 2 November 2026:** author challenged reopening reverse exposure
  and recalled objective 1 as the sole phase goal. Original conversation confirms narrowing
  direction and bounded-context approval, with a formal scope caveat left unresolved. E04's
  full-inventory interpretation needs clarification before downstream edits. See T52 scope
  history and B-144. Prior mapping approvals are preserved, not treated as deliberate reversal.

- **T52 mapping review complete, 2 November 2026:** author approved E01–E10 in the
  [objective-to-evidence table](research/52-objective-to-evidence.md). Full potential blast
  radius remains in scope. E06 combines limited uncertainty test cases with case-specific
  guidance from approved incident-response practice; its boundary is recorded in the spec.
  Next: candidate dispositions, then downstream requirements and B-143 reconciliation.
  No runtime certification or build release. T52 claimed; T54 blocked; AUD-076 open.

- **T52 objective-to-evidence table, 2 November 2026:**
  [Mapping](research/52-objective-to-evidence.md) covers ten outcomes with data, behaviour,
  expected answers, evidence, gaps and owners. [Saved evidence](research/52-saved-evidence-inventory.md)
  separates historical results from current source and unbuilt integration. Table ready
  for review; no scope change or reliability certification. Next: candidate dispositions
  and downstream reconciliation. T52 claimed; T54 remains blocked.

- **T52 direct-event window approved, 2 November 2026:** without an alert, use the single
  login timestamp ±24 hours, clipped to available records with gaps stated; expansion stays
  analyst-controlled. Narrow screening policy decisions are settled. Next: broader T52
  objective/evidence review and downstream reconciliation. T54 still waits for T52 closure.

- **T52 screening grading approved, 2 November 2026:** all four written applications
  settled. O1-09/O1-12-D retain O1-06's full rules plus their specific failures; O1-02 needs
  no invented threat, and quoting an injection is not obedience. T54 owns implementation
  checks. Next narrow decision: direct-event window anchoring. Broader T52 closure remains.

- **T52 provisional-model selection approved, 2 November 2026:** after all three passes,
  require twelve completed trials per candidate, no critical errors and no applicable zero
  scores. Compare quality case by case; similar quality is decided by cost, then speed.
  If none qualifies, diagnose rather than automatically promote. Next: narrow grading
  reconciliation and direct-event-window check. Broader T52 closure remains open.

- **T52 screening assessor approved, 2 November 2026:** author scores; Codex prepares
  blinded reviews and records labels/checks. Initial human scores precede assistant
  discussion; revisions retain reasons. Small review batches; no second human/paid judge
  required and no independent human-agreement claim. Next: provisional-model selection,
  then narrow grading/direct-event-window checks. Broader T52 closure remains open.

- **T52 approval audit, 2 November 2026:** all four scenarios/expected assessments,
  common scoring, O1-06 anchors, role responsibilities and T54 ownership are already agreed.
  Corrected stale summaries (B-142). Remaining screen decisions are assessor arrangements
  and provisional-model selection; narrow checks cover the three written grading applications
  and direct-event window anchoring. Fixtures/IDs/hashes/prompts are T54 build work, not a
  renewed scenario-approval round. See T52's approval audit. Broader T52 closure remains open.

- **T52 runner ownership/contract approved, 2 November 2026:**
  [T54](issues/54-early-langfuse-evaluation-integration.md) owns the isolated comparison runner
  and Langfuse recording together. Nine record groups, local-first evidence, retained failures
  and separate blinded assessments are agreed. Build local runner, mirror, then prove live
  recording with authorised scored screening evidence. T29/T30/T31 retain their existing
  exam/judge/application-tracing responsibilities. T52 remains current; next are detailed
  fixture/role/scoring readiness, assessor arrangements and model-selection rules.

- **T52 spending simplification, author ruling 2 November 2026:** no request reservations
  or worst-case billing gate. Track actual costs with US$25 as a planning budget, review at
  US$15 and after 24 results. No guaranteed hard final-charge ceiling; token/call/retry counts
  remain uncapped within approved time limits. Reservation research below is superseded.
  Next: runner ownership/record contract and fixture/scoring readiness.

- **T52 price/accounting research, 2 November 2026:** six selected standard-route prices
  verified in public metadata, including DeepSeek `deepinfra/fp8`. See
  [price report and reservation proposal](research/52-screening-price-and-reservation-check.md).
  Reserve possible charges before dispatch and reconcile actuals is proposed; no new token
  caps. Runtime billing bounds, ledger implementation and full-budget feasibility remain
  unproved. No inference or account changes; T52 remains current.

- **T52 spending approved, 2 November 2026:** US$25 shared across compatibility checks,
  72 screening attempts and necessary setup-repair reruns; review at US$15 and after the
  first 24 results. No per-model budgets. Excludes architecture calibration and paid judges.
  Verify route prices and outstanding-charge accounting before execution. Execution-policy
  choices are recorded; price/budget feasibility and runner readiness remain unproved.

- **T52 setup-rerun policy approved, 2 November 2026:** rerun only comparisons
  invalidated by a documented setup fix, across all affected models for shared changes.
  Preserve originals and version repairs; poor scores alone do not justify reruns.
  Next: spending policy. No paid execution authorised.

- **T52 compatibility checks approved, 2 November 2026:** six separate initial setup
  sessions before scoring, covering settings, tool round trip, output contract and result
  recording under existing time limits. No added token/call/retry caps. Next: setup-rerun
  policy and spending. Paid execution remains unapproved.

- **T52 concurrency approved, 2 November 2026:** one screening case at a time, with
  rotating model order and separate request/case timing. Next: compatibility-probe and
  setup-rerun allowances, then spend policy. No paid execution authorised.

- **T52 call/retry policy approved, 2 November 2026:** no evaluation-imposed call or
  retry count caps within a case. Preserve all attempts and distinguish model/tool work
  from transport/runner retries so recurring failures can reveal setup defects. Retries
  share the existing case deadline; no extra scored trials approved. Next: concurrency,
  probe/setup-rerun allowances and spend policy. No paid run authorised.

- **T52 token policy approved, 2 November 2026:** no evaluation-imposed token caps for
  the 72-answer screen. Measure token consumption as an outcome alongside quality, time
  and cost; disclose unavoidable provider ceilings/defaults. Approved reasoning and time
  limits remain. Next: call/retry, concurrency, probe/rerun and spending limits. No paid run.

- **T52 timing approved, 2 November 2026:** three minutes per model request and ten
  minutes per complete case attempt, including tool work and any permitted retry.
  Preserve timeout outcomes. Output/reasoning allowance is the next decision, followed
  by call/retry, concurrency, probe/rerun and spending limits. No paid execution approved.

- **T52 model configuration approved, 2 November 2026:** OpenRouter gateway, DeepInfra
  for Qwen/GPT-oss/DeepSeek, OpenAI for Luna/Sol and Anthropic for Haiku. Medium reasoning
  for five, native high for DeepSeek; fixed standard-service routes with no silent fallback.
  See [configuration and compatibility gaps](research/52-model-reasoning-settings.md).
  Next: time/output/retry/call/spend limits. Compatibility remains unproved; no paid run begun.

- **T52 screening repeats approved, 2 November 2026:** six models × four cases × three
  attempts = 72 answers. Inspect the first 24 for setup problems, then complete two more
  passes. Preserve all results; do not use this checkpoint for early elimination. Routes,
  settings, execution limits and detailed fixture/scoring readiness remain open. The
  separate 12-answer architecture calibration and T54 delivery order are unchanged.

- **T52 screening cases approved, 2 November 2026:** all four cases and their expected
  assessments are agreed: O1-02, O1-06, O1-09 and O1-12-D. The missing-history concern is
  resolved. Six candidates × four cases means 24 answers per pass; repeats, routes/settings,
  execution limits and detailed fixture/scoring readiness remain open. No paid run started.

- **T52 six-model pool approved, 2 November 2026:** Qwen3.8-27B, gpt-oss-120b,
  DeepSeek V4.1 Flash, GPT-6 Luna, Claude Haiku 5.5 and GPT-6.1 Sol. See the
  [current shortlist](research/52-broad-model-shortlist.md). Three other shortlisted models
  move to reserve. Routes, settings and execution limits remain open; no model winner
  or paid run is approved. T52 remains current; T54 delivery order stays unchanged.

- **T52 research checkpoint, 2 November 2026:** author requested broader model research,
  including cheap open-weight candidates without a security-publication entry requirement.
  [Shortlist](research/52-broad-model-shortlist.md) and
  [screening evidence](research/52-model-screening-evidence.md) are recorded. No model is
  selected. Additional screening is proposed; counts, budget and execution remain undecided.
  T52 remains current and the approved T54 delivery order below is unchanged.

- **Approved delivery order, 2 November 2026:** T52 remains current;
  [T54 early Langfuse integration](issues/54-early-langfuse-evaluation-integration.md) is next
  after T52, before instrumented 12-answer calibration. T52 settles runner ownership and
  contract. T31 retains application/full-exam integration after T29 and reuses T54.
  Model and paid-run budgets remain undecided.

- **T53 resolved, 2 November 2026, taken ahead by the author's instruction:**
  [Stable Browser access](issues/53-stable-browser-logins.md) now uses `li_admin`/`li_reader`
  from the main `.env` and fixed localhost ports `7474`/`7687` for the selected pair.
  New builds remain isolated until operator selection; rollback retains volumes and protection.
  Author accepted both logins and the fixed address. Full backend 668, frontend 150, types
  and both review axes pass. Only `2d1bf85e…` runs; `f937ea59…` is retained and stopped.
  T52 remains the next recorded priority. AUD-068 remains open.

- **Opened 1 November 2026, author's ruling (option A):**
  [T53 stable Browser access](issues/53-stable-browser-logins.md). Tier 2, unblocked, and
  independent of T52. Fixed `li_admin` and `li_reader` logins from the main `.env`, and
  `127.0.0.1:7474`/`7687` for the selected build; enforced roles stay under AUD-068. First cut as
  T53 and T54, merged into one ticket by the author. The current priority below is unchanged.

- **Current priority, T51 resolved on 1 November 2026:**
  [T52 objectives and reliability review](issues/52-agent-objectives-and-reliability-review.md),
  as the author ordered. The answer key is cleaned and pair `2d1bf85e…` is active, with T50's
  `f937ea59…` retained for rollback. T52 still blocks T45 and T26; T25 and T27 remain
  independently available.

- **Previous priority, revised by the author on 1 November 2026:** finish
  [T51 answer-key wording](issues/51-answer-key-address-wording.md), then take
  [T52 objectives and reliability review](issues/52-agent-objectives-and-reliability-review.md).
  Complete the existing answer-key cleanup and verified pair activation before reviewing the
  objectives against that baseline. This is a work-order preference, not a new dependency.
  T52 still blocks T45 and T26; T25 and T27 remain independently available.

- **Previous priority, author ruling on 1 November 2026:** [T52 objectives and reliability review](issues/52-agent-objectives-and-reliability-review.md).
  A Tier 3 decision ticket covering phases 0 and 1, ahead of T45 and T26 and blocking both.
  It maps objectives to evidence and considers bounded Sentinel-inspired additions; it approves
  no implementation or scope change by itself. T25, T27 and T51 remain independently available.
  This explicit priority overrides the default lowest-number unblocked-ticket order.

- **Previous priority, T50 resolved on 1 November 2026:** [T25 account peers and corpus-search tools](issues/25-peers-and-corpus-search-tools.md),
  now unblocked (T22, T24, T49, T50 all resolved). Its `find_peers` takes `account_id | device_id`
  only. T45 still blocks T26. [T51](issues/51-answer-key-address-wording.md), a small follow-up
  rewording two leftover address sentences in the S6 answer key with a new pair, is also open by
  the author's ruling at T50's close. Two spec wording questions wait for the author: phase 1's
  "spread and shared ground" (shared ground is now device only) and the draft Graph tab schema's
  `network` node type.

- **Previous priority, T25 gate closed on 1 November 2026:** [T50 remove address-sharing context](issues/50-remove-address-sharing-context.md).
  The author ruled that sharing an address answers no investigation question in this app, added
  no allocation evidence (AUD-073) and removed address-sharing context everywhere
  ([research note 25](research/25-shared-address-value.md)). Spec and decision log updated.
  T50 blocked T25 and T26 and is resolved: no `used_address` edges, no address context in the
  radius or answer key, new pair `f937ea59…` activated by restart with the previous pair retained.

- **Required gate before T25, author ruling on 1 November 2026 (closed, see above):** hold T25 implementation
  for a separate dedicated session on the investigative value of shared network-address
  context, especially shared VPN exit addresses. Record the author's explicit retain/narrow/remove
  ruling and any approved spec changes before building. See T25's required pre-build gate.
  T49 remains resolved; this is a new decision gate, not a migration defect. T27 is unaffected.

- **Previous priority, T49 closure on 1 November 2026:** [T25 account peers and corpus-search tools](issues/25-peers-and-corpus-search-tools.md).
  [T49](issues/49-neo4j-migration-acceptance.md) is resolved: the author accepted the measured
  switch/recovery plan, Neo4j is active, NetworkX is retired, and all 25 saved investigations
  reopen identically. Full-run findings and passing affected reruns are preserved, with clear
  two-axis reviews. AUD-067 closes; AUD-068 remains open. T27 is also released. T45 remains
  separate and still blocks T26; existing retrieval gaps are not waived.

- **Previous priority, T48 closure on 30 October 2026:** [T49 migration acceptance](issues/49-neo4j-migration-acceptance.md).
  T48 is resolved: paired lifecycle and native inspection complete; author accepted organisation
  and S6 Browser views; Gephi retired with history preserved. Evidence: full pre-retirement
  backend 710 passes, final native suite 2 passes, post-retirement core/graph/native 53 passes,
  frontend 150, clean types and clear two-axis reviews. Working application remains unchanged.
  T49 owns live migration gates, maintenance-window acceptance and the switch. T45 remains separate.

- **Earlier T48 lifecycle checkpoint, 30 October 2026:** checkpoints 1–2 are implemented and verified.
  Coherent startup, update/rollback, saved evidence and evaluation isolation are complete.
  Evidence: 21 focused lifecycle tests, 709 full backend passes with one known AUD-061
  teardown error followed by exact cleanup and a passing affected-test rerun; 150 frontend
  passes, clean types and cleared two-axis review. T48 stays claimed. Continue checkpoint 3,
  native Browser inspection and the author's walkthrough, in a fresh session. Gephi remains
  until acceptance. Restart measurements are recorded; T49 still owns maintenance-window
  acceptance and the working-application switch.

- **Previous priority, T47 closure on 30 October 2026:** [T48 paired lifecycle and native inspection](issues/48-paired-lifecycle-and-native-inspection.md).
  [T47](issues/47-neo4j-build-and-graph-answers.md) is resolved: isolated paired builds and exact
  Neo4j graph answers are verified. The working application remains on its prior build.
  T49 still gates migration acceptance and T25/T27. T45 remains independently available.

- **Previous priority from T46, 30 October 2026:** [T47 Neo4j build and graph answers](issues/47-neo4j-build-and-graph-answers.md).
  [T46](issues/46-graph-store-architecture-review.md) resolved with the author's migration ruling
  and approved three-ticket sequence: T47, [T48 lifecycle and native inspection](issues/48-paired-lifecycle-and-native-inspection.md),
  then [T49 migration acceptance](issues/49-neo4j-migration-acceptance.md). PostgreSQL owns passage
  content/search; Neo4j owns graph queries and passage references. Verified pairs include source
  snapshots, switch by restart and retain the previous complete version for rollback. Native
  Browser inspection replaces Gephi after the author's walkthrough. Community administrative
  access remains an accepted development limitation; AUD-068 gates production readiness.
  T25/T27 now wait for T49, not merely the architecture decision. T45 remains independently
  unblocked and still holds T26. T47 is now resolved; T48 is next. The active app has not switched.
  T02/T20 remain resolved history; the revised spec governs the replacement.

- **Origin.** The bootcamp's week 2 brief (RAG, with GraphRAG as one suggested use case) is the
  inspiration. By the author's ruling of 20 October 2026 it is not a contract: nothing is
  submitted, there is no deadline and no owed deliverable. See `CLAUDE.md`.
- **Reference shape.** The course demo notebook (the author's copy, `Mastering-Agentic-AI-Week2`,
  `Week2-Session2/graph_rag/graph_rag.ipynb`): structured facts as a Neo4j graph, free text
  chunked and embedded as nodes linked to the graph, semantic search to find candidates, graph
  traversal to filter and enrich, a grounded generation step. Semantic search finds, the graph
  decides and explains.
- **Retrieval stance (author, 20 October 2026).** Hybrid retrieval (semantic plus BM25 keyword)
  with re-ranking, at sensible defaults first. Tuning follows measurement, never precedes it.
- **Evaluation stance (agreed 20 October 2026).** The eval set exists before the first retrieval
  runs. Two layers measured separately: retrieval (was the gold evidence found and ranked) and
  answer (is every claim backed by the retrieved context). Re-run on every change; runnable by the
  author or Codex without Claude.
- **Data.** Everything in the app is synthetic demo data. A larger synthetic set is allowed if the
  chosen use case needs it, as long as it gives solid ground for testing.
- **Rigour.** Tier 3. Every ticket closes on evidence.
- **Future direction noted by the author (20 October 2026), not scope.** The same graph serves
  GRC: a control maps to a policy, a policy applies to an asset, an incident shows a control
  failed. "Which controls does this incident touch?" becomes one query once the map exists. Any
  move in that direction is a later slice with its own spec.
- **Tools.** Research tickets use the Perplexity MCP tools and verify material claims against
  primary sources. The course's solution kits stay closed.

## Decisions so far

- **T52 resolved, 2 November 2026:** reliable login investigation is the sole phase-0/1
  objective; bounded context, uncertainty, evidence and security obligations are assigned
  to downstream owners. Approved source/data ownership is recorded in the spec. See
  [T52 closure evidence](issues/52-agent-objectives-and-reliability-review.md#answer-review-complete--2-november-2026).
  Final runtime proof remains with implementation/evaluation/acceptance tickets.


- [T53 Stable Browser access](issues/53-stable-browser-logins.md): stable named human users,
  separate application identity, fixed selected address, conflict refusal and recoverable
  selection/rollback with volumes preserved. Real operator round trip, author Browser checks,
  full regressions and independent reviews pass. Community reader convention remains explicit.

- [T49 Verified Neo4j migration](issues/49-neo4j-migration-acceptance.md): working application
  selected after author acceptance, live regression gates, final checks and independent reviews.
  PostgreSQL keeps passage content/search; Neo4j owns reference-only graph queries. Saved
  investigations survive exactly, paired rollback and archived implementation recovery are
  tested and retained, and NetworkX is retired. T25/T27 are released; production and retrieval
  limitations remain explicit.

- [T48 Paired lifecycle and native inspection](issues/48-paired-lifecycle-and-native-inspection.md):
  coherent startup, restart-based update/rollback, saved-evidence continuity and isolated evaluations;
  exact native Browser views accepted by the author, followed by Gephi retirement. Full and affected
  safety checks and independent reviews pass. Application selection unchanged; T49 is next.

- [T47 Build the Neo4j graph and preserve its answers](issues/47-neo4j-build-and-graph-answers.md):
  isolated immutable-source pairs, reference-only graph ingestion, independent integrity and
  corruption refusal, retired builder credentials and serving protection across restart;
  existing graph answers and frozen S6 gold preserved. Cancellation/partial-failure cleanup
  verified. Evidence: 686 backend and 150 frontend tests, clean types, cleared two-axis review,
  tested admin command and local measurements. No active application switch; T48 is next.

<!-- one line per resolved ticket: [title](link): gist -->

- [T46 Graph foundation review](issues/46-graph-store-architecture-review.md): migrate to Neo4j
  Community plus PostgreSQL/pgvector under the approved development security exception; keep
  passage content in PostgreSQL and references/relationships in Neo4j; complete source/store
  versions switch by restart with rollback; replace Gephi with native inspection. Proof: selected
  write refusals, 38 parity/lifecycle checks and failed-build cleanup; limits remain explicit.
  Author approved consolidated T47–T49 using `to-tickets`; T49 holds T25/T27. AUD-067 waits for
  implementation acceptance and AUD-068 records the future production gate.

- [Use-case research](issues/01-use-case-research.md): the graph holds durable relationships
  (people, accounts, groups, grants, assets, networks, incidents) and the log stays the source of
  truth; policies, runbooks, ATT&CK pages and incident write-ups form the hybrid-searched corpus;
  Neo4j GraphRAG ships the hybrid-then-traverse shape; no public dataset pairs logins with
  organisational context, so we generate our own small consistent set. Three candidate slices
  documented; recommendation is slice 2 (spray-to-compromise blast radius) with slice 1's network
  and travel facts folded in. Author's choice pending. [Research note](research/01-use-case-research.md).
- [Where the graph lives and where retrieval runs](issues/02-store-and-retrieval-provider.md):
  one store, the author's installed PostgreSQL 18.6 with pgvector; LangChain's PostgreSQL store
  for hybrid search with our own score-keeping fusion; built-in keyword ranking first, BM25 only
  if the eval demands it; graph walked in NetworkX built from the tables, chunks included with
  `mentions` edges; a read-only graph screen of our own plus Gephi export; ground-truth files are
  the truth and the database is built from them; fresh database per run, loud failures; two
  read-only locks; memory stays in SQLite. Neo4j, LanceDB, LadybugDB and hosted services ruled
  out. Ten decisions under the ticket's Answer. [Research note](research/02-store-and-retrieval-provider.md).
- [Embedding model, keyword search and re-ranker](issues/03-embedding-and-reranking.md): refusal
  path first, three verdicts (`none`, `weak`, `found`) computed in code from recorded scores, with
  the threshold calibrated on the eval set before the `none` rule is switched on;
  `text-embedding-3-small` through OpenRouter at 1,536 dimensions, no local models; structure-first
  chunking with a context header on every chunk; exact identifiers as typed columns plus a
  chunk-to-entity link table; `cohere/rerank-v3.5` through OpenRouter behind a switch, 20 to 5,
  eval decides; metadata filters on typed columns applied before both legs, typed tool options,
  the model never writes a filter; our reciprocal rank fusion with three library traps pinned by
  tests. Seven decisions under the ticket's Answer. [Research note](research/03-embedding-and-reranking.md).
- [Synthetic organisation, corpus and ground truth](issues/04-synthetic-data-and-ground-truth.md):
  the Port's seeded generator grows into the world's one source: the 50 users and five stories
  stay, with six departments, three privilege groups, ten assets with sensitivity, a device
  register and a four-address VPN pool drawn around them; two new log columns (`mfa_result`,
  `device_id`); a new spray S6 that succeeds on an IT Admin, both compromised accounts on a
  documented MFA exception list; three benign twins (travel, reset burst, laptop swap) that trip
  the Port's rules and are cleared by one document each; 13 ATT&CK pages and 27 own documents
  written by a standalone Codex from a brief kept in the repo and checked by a script; Markdown
  front matter with mentions computed by ingestion; one folder per dataset under
  `backend/data/datasets/`; four recorded gaps for the refusal path; the generator writes the
  answer key into `truth.json` with a test that recomputes S6's radius; the Port's eval passes
  unchanged and regeneration is phase 0's first build ticket. Seventeen decisions under the
  ticket's Answer.
- [How the knowledge base reaches the agent](issues/05-agent-tools-for-the-knowledge-base.md):
  the agent's purpose fixed first (an explained, evidence-backed answer to what happened, what it
  can reach, and whether it is a threat); the playbook lives in code, asked for in chat, never
  unasked; conversation first, then report, with a light gate per turn and a full gate at report
  time; seven typed tools, the Port's three plus `investigate_alert` (steps 2 to 6 bundled into
  one package with a section per step, spray targets included), `lookup_account`, `find_peers`,
  `search_corpus`; every tool returns short labelled content for the model and a full artifact
  for the eval and screen; IDs computed from content, including a new stable finding ID on the
  Alerts API; citations as short labels resolved in code, an unresolved label fails the turn;
  two answer checks in the eval; every tool result fenced in one middleware with canaries
  measured; the plan in the Port's middleware extended (before, after, wrap); the tool choice is
  the shortcut rule; the report gate completes missing steps in code and names what cannot run;
  package caps; parallel calls on; the playbook as one list in the core shared by policy, gate
  and eval. Five rulings and sixteen decisions under the ticket's Answer.
  [Research note](research/05-agent-tools.md).
- [The eval set for a graph-plus-text system](issues/06-eval-design.md): retrieval gated per
  question with two hard checks (every gold ID among the 20 fused candidates and among the chunks
  the model received), no rate and no borrowed target; the graph walk must return exactly the gold
  set; the phase 1 mix weighted to say-no and mixed questions with lookups as the control group,
  every question carrying gold IDs; the refusal threshold calibrated on a separate tuning file
  that never overlaps the test questions; the answer gate is citation resolution with the gold IDs
  cited, say-no questions graded from the tool verdict at 100%; the faithfulness judge is a smoke
  alarm (different model family, binary per claim, three trials, ten answers, verdicts stored,
  never a gate in phase 1); playbook and canary checks as 100% gates, canaries flagged security;
  one scorer and runner with two question files kept separate, artifacts saved, version
  fingerprint widened, a direct retrieval path; re-ranker and BM25 settled by on-versus-off
  comparisons with tie to off; Langfuse adopted to the full as a mirror with the repo files as the
  source of truth. Ten decisions under the ticket's Answer.
  [Research note](research/06-eval-design.md).
- [What the screen shows for an explained alert](issues/07-explained-alert-screen.md): the chat
  is the screen and the Alerts panel gains only a finding ID column; citations land in an
  evidence panel, a third column built from the saved artifact and downloadable as JSON; a graph
  path is one line per hop; the radii show as counts first with the lists in the panel; the
  investigation tool's five steps stack while it runs, an exception to the Port's single status
  line, and collapse into Tools used after, with a build condition to study Anthropic's and
  OpenAI's progress patterns first; citation letters L, G, D; the judge's reason stays off the
  screen; a five-level visual hierarchy with the verdict as the one coloured surface and tags in
  link blue. Nine decisions and a draft API addition under the ticket's Answer.
  [Prototype](research/07-explained-alert-prototype.html).
- [The read-only graph panel and the Gephi export](issues/08-graph-screen-and-gephi-export.md):
  a Graph tab beside Evidence in the third column that draws only the walk the agent made,
  projected from the saved artifact so map and report cannot disagree; organisation nodes only,
  the many collapsed with a count; a click switches to Evidence and lights the record, with an
  uncited edge named as such; layered layout by playbook step with shape per type, no step
  captions; an empty state when no walk ran; React Flow plus dagre read-only with own SVG as
  fallback; Gephi export as a GEXF script with two tests and the author's look, no endpoint.
  Nine decisions and a draft `graph` field under the ticket's Answer.
  [Research note](research/08-graph-screen.md) and
  [prototype](research/08-graph-panel-prototype.html).

### Author's ruling, 20 October 2026

Slice 2, spray-to-compromise blast radius, goes first. The broadening steps are accepted in the
order recorded in [research note 01, section 7](research/01-use-case-research.md): spread and
shared ground, then history, then travel and network facts with account type, then attack path
and risk score. GRC is a later slice.

### Phases

| Phase | Content | Gate to close |
|---|---|---|
| 0 Foundation | Graph store, synthetic data generator with written ground truth, text corpus, hybrid retrieval with re-ranking, the eval harness with its first questions, read-only agent tools over graph and corpus | Eval harness runs end to end; retrieval and answer layers measured separately |
| 1 Blast radius | Slice 2 core plus spread and shared ground | Eval pass on phase 1 questions; author accepts the live screen |
| 2 History | Incident nodes and write-ups | Eval set extended and passing |
| 3 Context | Travel and network facts; account type and ownership | Eval set extended and passing |
| 4 Paths and risk | Attack-path query; risk score with an agreed policy | Eval set extended and passing; author agrees the scoring policy |
| Later | GRC view | Its own spec |

Each phase is specified before it is built, and the eval set grows with each phase.

### Scope ruling (author, 20 October 2026)

**This initiative delivers phases 0 and 1 only.** They are the requirements: the foundation and
the blast-radius slice with spread and shared ground. The spec and tickets cover those two phases
and nothing else. The initiative closes when phase 1 is accepted on a live screen with its eval
passing.

Phases 2, 3, 4 and the GRC view are **planned features, not requirements.** They stay recorded
here and in research note 01 so the design keeps room for them, and each is taken later as its
own small initiative, with its own spec section and tickets, whenever the author chooses. Other
bootcamp-week initiatives will arrive in between; nothing in this initiative waits on them or
blocks them.

### Decision tickets charted (20 October 2026)

| Ticket | Type | Blocked by |
|---|---|---|
| [02 Where the graph lives and where retrieval runs](issues/02-store-and-retrieval-provider.md) | research | none |
| [03 Embedding model, keyword search and re-ranker](issues/03-embedding-and-reranking.md) | research | 02 |
| [04 Synthetic organisation, corpus and ground truth](issues/04-synthetic-data-and-ground-truth.md) | grilling | 02 |
| [05 How the knowledge base reaches the agent](issues/05-agent-tools-for-the-knowledge-base.md) | research, then grilling (retyped 22 October 2026) | 02, 04 |
| [06 The eval set for a graph-plus-text system](issues/06-eval-design.md) | research, then grilling (retyped 23 October 2026) | 04, 05 |
| [07 What the screen shows for an explained alert](issues/07-explained-alert-screen.md) | prototype | 05 |
| [08 The read-only graph screen and the Gephi export](issues/08-graph-screen-and-gephi-export.md) | research, then prototype, then grilling (opened 24 October 2026, retyped 25 October 2026) | 02, 07 |

Tickets 02 to 08 are resolved (20, 21, 22, 22, 23, 24 and 25 October 2026). The author ruled 05 the
most important ticket of the initiative and retyped it to research then grilling; its first
comment records the agent's purpose and the playbook stance that every tool serves. Ticket 06 was
retyped the same way on four gaps the earlier notes did not cover. Ticket 07 ran prototype first,
grilling second, by the author's ruling that a screen cannot be decided from a description.
Ticket 08 was opened on 24 October 2026 when the author found that the read-only graph screen and
the Gephi export promised in ticket 02's decision 2 were never designed: ticket 07 did not take
them up; it ran research, then prototype, then grilling, and resolved on 25 October 2026.
The decision tickets are complete. The [spec for phases 0 and 1](spec.md) was written on
25 October 2026 with `mp-to-spec`, after the author agreed six test doors and ruled eight points no
ticket had decided (twins B2 and B3, the `default` dataset folder, the Port's answer key kept, fake
embedder and re-ranker in tests, the phase split, the ID formats, and a staleness guard on the
app's database). The spec was revised the same day after Codex's review.

### Build tickets cut (25 October 2026)

The spec was cut into 34 build tickets, 09 to 42, with `mp-to-tickets`; the author kept that
granularity and ruled two points (the S6 radius test moves to ticket 19; every phase 1 ticket waits
for ticket 29). Phase 0 is 09 to 31, with ticket 29 as its gate; phase 1 is 32 to 42, with ticket
42 as the initiative's gate. Tickets 16 and 42 are the author's to run. Each ticket's `Blocked by`
line holds its edges. The build frontier reached ticket 25 after T24. As of 30 October 2026,
T46's decision is resolved and its approved migration is T47 → T48 → T49. T49 now holds T25
and T27. **The next priority is ticket 49**, ahead of the otherwise unblocked T45 by the
author's approved sequence. T47 and T48 are resolved; the active application switch awaits T49.

Ticket 43 was opened on 26 October 2026 by the author's ruling, to restore the Port eval's margin
(Q02 and Q04, AUD-046 and AUD-047) before T14. It is taken ahead of the frontier by that ruling,
and is resolved (see Build tickets resolved). T14 to T22 have since resolved; the frontier
is ticket 23, the re-ranker behind its switch. Ticket 24 is also unblocked. No ticket was
blocked by 18 or 20. T23 and T24 resolved on 29 October 2026; T25 was the next build ticket
until the T46 architecture hold on 30 October 2026.

T22's live retrieval baseline has a recorded K04 candidate gap (B-098/AUD-062). Re-ranking
cannot recover a passage outside both candidate lists; review this before closing the later
retrieval gate. T22 permits logging first-run misses, so its completion does not waive that gate.

Author, 29 October 2026: park the ensuing custom retrieval-design experiments at T23. Assess
the planned reranker first; revisit the evidence gap there. The experiments remain research,
not approved additions to T23. See its Comments for the saved evidence. No build started by
this deferral.

Ticket 45 was opened on 29 October 2026 by the author's ruling, after T23: the parked
retrieval-design work becomes its own decision ticket (research, then grilling, strongest
model), covering compound questions on both the chat path and the package path, and what
K04's gate measures. It blocks T26 and AUD-062's closure; T24 and T25 proceed meanwhile.
See [ticket 45](issues/45-compound-question-retrieval-design.md). The later T46 ruling holds
T25 and prioritises the graph foundation review; T45's retrieval scope and T26 blocker remain.

Ticket 44, the phase 0 cleanup, was opened on 28 October 2026 by the author's ruling after T18.
It collects the foundation's small debts (AUD-057, AUD-058, AUD-059 under the new settings rule,
the `env.example` line, and items found in T19 to T28). It is blocked by 28 and blocks the
phase 0 gate, 29, so the debt is paid before the gate rather than at the initiative's end.

After the T19 walkthrough, the author agreed that T24 prepares and checks the graph once per
backend process at startup and tools reuse it across questions. A rebuilt dataset is loaded
on restart. This is recorded in the spec's graph lifecycle rule and T24's acceptance criteria;
T19's implementation and the frontier remain unchanged.

### Model per ticket (author's ruling, 27 October 2026)

Each build ticket from 17 to 42 carries a `Model:` line under its `Phase:` line. The strongest
models (Fable 5.1 for Claude, Astra for Codex) take the tickets where one wrong choice spreads into
every later ticket; the standard models (Opus 5.5, Sol 6.1) take the rest.

| Model | Tickets | Reason |
|---|---|---|
| Strongest | 17, 19, 22, 24, 26, 27, 28, 29, 45, 46, 47, 48, 49, 52 | Load-bearing seams: the build, graph, fusion, tools, package, resolver, playbook, eval gates, retrieval design, graph foundation and the approved migration build/lifecycle/acceptance sequence |
| Strongest if budget allows | 30, 37, 41 | Judge design, the hardest frontend drawing, the BM25 leg and an honest on-versus-off call |
| Standard | 18, 20, 21, 23, 25, 31 to 36, 38 to 40, 44, 50 | Standard build work on seams the strongest tickets set |
| None | 42 | The author's ticket |

The line advises; it is not a gate. Each of tickets 17 to 41 carries a first acceptance criterion:
before any build work starts, the builder tells the author the ticket's `Model:` line, waits for the
author to confirm the model is set, and records the model used in a dated comment. The independence idea (eval questions in 21 and 40 written by
the other family from the retrieval builder) was proposed and is not ruled.

### Build tickets resolved

- [51 Reword the S6 answer key's leftover address sentences](issues/51-answer-key-address-wording.md)
  (1 November 2026): `basis` describes only what the key records; `used_address_filter` is
  dropped; the rest of `truth.json` is identical under a normalised comparison. New pair
  `2d1bf85e…` reuses the T50 pair's passage vectors (0 provider calls), passes full parity,
  and is selected and activated by restart; all 25 saved investigations reopen identically.
  Evidence: backend 663 and frontend 150 passed, clean types and lint, two-axis review triaged.
  Model: Claude Opus 5.5.

- [50 Remove address-sharing context](issues/50-remove-address-sharing-context.md)
  (1 November 2026): the graph draws no `used_address` edges and the integrity check refuses one
  by name; network nodes stay with their `mentions` links; the radius, walk, neighbourhood and
  answer key carry no address co-user context; `truth.json` regenerated with only that key
  removed. New pair `f937ea59…` built from the previous pair's passage vectors (0 provider
  calls), parity-checked, inspected (organisation 170 nodes / 185 relationships, S6 10 / 9),
  selected and activated by restart; 25 saved investigations reopen identically. Pairs built
  before T50 need the earlier code to open. Built on Fable 5.1 by the author's ruling.

- [09 PostgreSQL with pgvector, and the loud test fixture](issues/09-postgres-pgvector-and-test-fixture.md)
  (25 October 2026): pgvector 0.8.7 on the Homebrew PostgreSQL 18.6, psycopg 3.3.6 pinned; a
  limited role `li_admin` and a pgvector template `li_template` from a one-time setup; each test
  session gets its own copy, dropped at the end; a stopped service fails loudly with the restart
  command. Rulings on the way: Codex's review is not a gate (tickets close on the builder's own
  `mp-code-review`); table access from ticket 17 through SQLAlchemy Core; the Port's eval skipped
  for this ticket.

- [10 The dataset folder](issues/10-dataset-folder.md)
  (26 October 2026): `LI_DATASET_DIR` replaces `LI_LOG_PATH`; the default log and Port answer key
  live together in `backend/data/datasets/default/`, moved byte-identically. Generator, API,
  tools, scorer and test readers follow the move. Seed README added. Evidence: 423 backend tests,
  149 frontend tests on the final rerun, clean typechecks, Standards and Spec review with no
  findings; unchanged Port eval 55/57 overall and 15/15 security meets its gates. Explorer timeouts
  and two inaccurate model answers remain recorded outside scope in B-066, B-070 and B-073.

- [11 The organisation and the two new log columns](issues/11-organisation-and-new-log-columns.md)
  (26 October 2026): eight organisation tables under `default/org/`, IDs made from content, drawn
  from their own random stream; `device_id` and `mfa_result` stay inside the core, and the Port's
  seven columns are byte-identical. Author's rulings on the way: an empty device ID for attackers and
  personal phones (124 rows), VPN sign-ins moved to ticket 12, cross-cutting privileged groups.
  Evidence: 438 backend and 149 frontend tests, clean types, two-axis review triaged; Port eval
  53/57 and 15/15 meets its gates. Q04 run 3 skipping reputation lookups is new as B-074 (AUD-046).
  S4 is intentionally unresolved by the author's subsequent ruling: preserve MFA `pass`, flag
  the unusual sign-in, and leave authorisation and mechanism unknown. T12 records these evidence
  limits in the answer key; no extra document or telemetry source. Corpus stays at 27 own documents.

- [12 S6, the three benign twins and the answer key](issues/12-s6-benign-twins-and-answer-key.md)
  (26 October 2026): S6 sprays 20 accounts and succeeds three times on Amelia Ward; Maya Patel's
  approved travel, Oliver Hayes's reset burst and James Carter's laptop swap supply the benign
  twins. Added 44 VPN rows and the evaluation-only `truth.json`, with planted paths and peer sets,
  planned document IDs, exceptions and four absent topics. S4 stays intentionally unresolved.
  The world has 1,948 rows and ten findings; original S1 to S5 event fields remain exact.
  Evidence: 448 backend and 149 frontend tests, clean type checks, two-axis review triaged;
  API eval 58/63 overall and 15/15 security, including 6/6 new S6 runs. B-076/AUD-047 records
  broad-spray outcome/count omissions; B-074/AUD-046 recurs on all three broad-compromise runs.
  Six existing frontend lint warnings remain. Benign clearing documents and graph recomputation
  are later tickets. Author approved T12 on 26 October 2026. All work committed locally.

- [13 The finding ID in the core](issues/13-finding-id-in-core.md)
  (26 October 2026): every finding carries `F-<rule slug>-<hash8>`, a SHA-256 of rule, users,
  addresses, first and last seen, computed from the finding's own fields and kept out of
  `to_dict()`, so the Alerts reply and the agent's view are unchanged until ticket 32. The recipe
  is fixed in the ticket's Answer and pinned by a test with an independently computed value.
  Evidence: 453 backend and 149 frontend tests, clean types, two-axis review triaged; Port eval
  57/63 and 15/15 meets its gates with no spare run, as Q02 (B-076/AUD-047) and Q04
  (B-074/AUD-046) now fail all three runs on the unchanged agent. AUD-048 is new for ticket 32.
  Author accepted T13 on 26 October 2026. All work committed locally.

- [43 Restore the Port eval's margin: Q02 and Q04](issues/43-eval-margin-q02-q04.md)
  (26 October 2026): the detection hook adds missing reputation lookups in code; the agent's view
  of a finding carries each address's real outcomes, drops the rule's own outcome counts, and
  states a successful sign-in in a code-built summary sentence; Q02 and Q04 gain S6 checks. Nine
  author rulings, three paid runs on three versions of the fix. Evidence: 514 backend and 149
  frontend tests, clean types, three two-axis reviews triaged; Port eval 62/63 and 15/15 with
  Q02 3/3 and Q04 2/3, five spare runs. AUD-046 and AUD-047 closed; AUD-049 to AUD-052
  registered. Its lesson became P-01 of `PRINCIPLES.md`. Author accepted T43 on 26 October
  2026. All work committed locally.

- [14 The ATT&CK pages at a pinned version](issues/14-attack-pages-pinned.md)
  (26 October 2026): Enterprise ATT&CK 20.0 at an exact MITRE commit with bundle/licence hashes;
  a network-free converter assembles thirteen pages from linked STIX objects, and a fetch
  script writes them with MITRE's licence under `default/corpus/attack/`. Repeated fetches
  agree byte for byte. Evidence: 521 backend and 149 frontend tests, clean types, two-axis
  review settled, Port API eval 62/63 and 15/15. B-076/AUD-047 recurred outside T14.
  Author's ownership ruling recorded: teams own internal documents, external pages identify
  their publisher, and neither establishes a login-account link. All work committed locally.

- [15 The Codex brief and the consistency script](issues/15-codex-brief-and-consistency-script.md)
  (27 October 2026): `codex-brief.md` plans the 27 own documents with five owner teams, the
  company's facts, counted realism features and forbidden terms, and leaves the two
  never-mentioned users and the backup server out entirely. The core checker reads its plan from
  the brief and checks a delivered folder against it, the organisation tables and `truth.json`;
  `scripts.check_corpus` prints lengths and fails on any error. Evidence: 34 checker tests, 555
  backend and 149 frontend tests, clean types, two-axis review triaged; Port eval not run, as
  nothing it measures changed. B-083 (brief facts against the log), AUD-055 (what the checker
  cannot see). The author read the brief on 27 October 2026. All work committed locally.

- [16 The own corpus delivered and checked](issues/16-own-corpus-delivered.md)
  (27 October 2026): a standalone Codex wrote the 27 own documents from the brief alone; copied
  byte-identically into `default/corpus/own/`; the checker passes with 0 errors; a scan finds no
  real company or person and no invented name. Token measurement against note 03's sizes led to
  six author rulings (P1 to P4c): unplanned kinds take the policy size, runbook steps stay whole,
  ATT&CK references, citation markers and link addresses stay out of chunk text, procedure
  examples are packed. Written to the spec and to ticket 17's criteria. AUD-055 closed; AUD-056
  registered. The author approved the documents with no rewrites.

- [17 The knowledge-base build command](issues/17-knowledge-base-build-command.md)
  (27 October 2026): one command builds a fresh PostgreSQL database from the dataset, with eight
  organisation tables, contextual chunks in LangChain's store, embeddings, a GIN keyword index
  and text-derived entity links. Core and store share one SQLAlchemy/psycopg pool; a separate
  reader is denied writes. Atomic local publication preserves the last successful build on
  failure. All T16 chunking rulings are covered. The first real build produced 320 chunks from
  40 documents and 257 organisation links in 18.479 seconds for $0.00111362. Evidence: 571 backend
  and 149 frontend tests, clean type checks, two-axis review findings fixed and confirmed, Port
  API eval 63/63 and 15/15 security. Six existing lint warnings remain. B-084 to B-088 record
  implementation/review iterations; AUD-057 records retained old build databases. The late model
  confirmation is recorded as a process exception. Local commits only; no push.

- [18 The staleness guard](issues/18-staleness-guard.md)
  (28 October 2026): every build records a SHA-256 fingerprint of the dataset folder's files,
  hidden entries skipped, with the embedding model, vector length and chunking settings. The app
  checks it at startup as the read-only role. Five author rulings: nothing built starts the app
  without a knowledge base and logs the build command; a build that cannot be checked stops the
  server (fail closed); hidden entries skipped; `LI_KNOWLEDGE_BASE_STATE` joins the contract; the
  "cannot be checked" text names the reader's login and the rebuild. The live build was rebuilt
  on the author's go as `li_kb_f9d6bcf6f8c5` ($0.00111362). Evidence: 585 backend and 149
  frontend tests, clean types, real-server refusal and start, two-axis review triaged, Port API
  eval 63/63 and 15/15 security. B-089, B-090; AUD-058, AUD-059. Model: Claude Opus 5.5.

- [19 The graph, its integrity check and the S6 radius test](issues/19-graph-integrity-and-radius.md)
  (28 October 2026): NetworkX graph built at the core opening, checked independently against
  database rows and successful login observations. One radius function returns joined groups,
  assets and device peers, with shared-address matches grouped separately as context. Five author
  rulings: success-only address edges; session-assigned VPN pool; reuse outside exposure counts;
  user dates first, all available records by default; include office as well as VPN context.
  S6 recomputes exactly: two groups, seven assets, no device peers, 43 office and ten VPN matches.
  Evidence: 612 backend and 149 frontend tests, clean type checks, zero findings on each review
  axis; Port API eval 61/63 and 15/15 meets its gates. Q02 omits S2's no-success outcome twice
  (B-076/AUD-047); six existing lint warnings remain. B-091 to B-095 retain iterations; AUD-060
  closed, AUD-061 records one intermittent teardown failure for T44. Live reader graph: 490 nodes,
  583 edges; rebuilt for $0.00111362. Model: author-confirmed Astra. Local commits only.

- [20 The Gephi export](issues/20-gephi-export.md)
  (28 October 2026): `KnowledgeBase.export_gexf` writes the checked graph, or one finding's
  radius walk by finding ID, as GEXF coloured by node type; `scripts/export_graph.py` calls it as
  the read-only role after the staleness check; no endpoint. The integrity check now returns its
  source-derived counts, and the read-back test compares against them. Author's rulings: the
  five builder's choices accepted (neighbourhood as the radius walk, organisation nodes only;
  refusals for no account reached, reserved names and an output inside the dataset folder);
  the busy whole-graph file stays complete and chunks are hidden with Gephi Lite's filter.
  B-096 (an export in the dataset folder makes the build stale) and B-097 (Gephi Lite ignores
  colours with an alpha, issue #307; reproduced and fixed). Live: 490 nodes, 583 edges; S6
  neighbourhood 55 and 64. Evidence: 622 backend and 149 frontend tests, clean types, two-axis
  review triaged, the author's Gephi Lite look. Port eval not run: no agent change. Model:
  Claude Opus 5.5.

- [21 The first knowledge-base questions](issues/21-first-kb-questions.md)
  (29 October 2026): `evals/knowledge_base_questions.json` beside the frozen Port file holds eight
  questions, K01 to K08: two document lookups, one graph lookup, one mixed question on S6, two
  absent topics with verdict `none` and two twins (B1, and B3 asked directly). A door 6 test proves
  every gold chunk exists in a fresh build, every gold record in the organisation tables, and K04
  equals S6's planted radius. Committed in `aa07926` before any search run. Author's rulings:
  K04 keeps two of S6's three documents; twins state `conclusion: "benign"`, apart from the search
  tool's `verdict`. Evidence: 629 backend and 149 frontend tests, clean types, two-axis review
  triaged. Port eval not run: no agent change. Model: Claude Opus 5.5.

- [22 Hybrid search and the retrieval layer alone](issues/22-hybrid-search-and-retrieval-layer.md)
  (29 October 2026): exact vector and PostgreSQL keyword search, typed filters before both
  20-result limits, own score-preserving RRF, direct graph checks and the existing runner's
  `--layer retrieval` path with offline rescoring and separate saved evidence. Author ruled
  `weak`/`not_calibrated` until calibration, with `none` disabled. Three live runs agree: five
  questions pass; K04 misses the MFA register (dense rank 115, keyword empty); K05/K06 await
  T39 calibration. B-098/AUD-062 and B-099 retain the gaps; original questions and gold unchanged.
  Evidence: 646 backend assertions pass with one known B-094 teardown error; exact cleanup and
  affected-test rerun clean. Frontend 149 pass, both typechecks clean, six existing lint warnings.
  Two-axis review: three findings fixed and independently confirmed. Admin commands tested.
  B-100 records review fixes. Port eval not run: no agent change. Model: author-confirmed Astra.
  Local commits only; T23 has not started.

- [23 The re-ranker behind its switch](issues/23-reranker-switch.md)
  (29 October 2026): `cohere/rerank-v3.5` through OpenRouter behind `LI_RERANKER`, default on.
  It scores the fused 20 in one request, records every score and keeps the best 5; its score
  drives the verdict, still `weak` / `not_calibrated` until T39. Author's ruling: zero passages
  give `none` / `empty_result`, on or off. The re-ranker is a LangChain `BaseDocumentCompressor`
  without the legacy wrapper; a failed call stops with fixed text. The gate still reads the fused
  20: two live runs equal T22 (five of eight), and the re-ranker kept every found required
  passage at ranks 1 to 3, K04's runbook at 1. The MFA register gap (AUD-062) is unchanged.
  B-101 (test guard missed the new key reader) fixed; AUD-063 and AUD-064 registered. Evidence:
  backend 666 passed with two B-094 teardown errors in an unchanged test; Pyright clean;
  frontend 149; two-axis review triaged. Model: author-confirmed Claude Opus 5.5. The parked
  retrieval-design work (T22 follow-ups) moved to its own decision ticket, 45, by the author's
  ruling.

- [24 The first agent tool end to end](issues/24-first-agent-tool-lookup-account.md)
  (29 October 2026): account owner, department and groups through the checked read-only graph;
  one shared instance per backend process, prepared before requests and closed on shutdown or
  failed startup. One fence for every tool; artifacts persist in SQLite but stay outside model
  input. Author-approved persistence baseline and minimal lookup progress compatibility delivered.
  Evidence: 677 backend assertions pass with two known B-094 teardown errors; exact idle cleanup
  and both affected reruns clean. Frontend 150, types clean, six existing lint warnings. Port API
  eval 62/63 overall and 15/15 security; live lookup succeeds. Two-axis review cleared after one
  documentation fix. Storage probe: 601-byte artifact, 16.4 MB SQLite after 50 repeated lookups;
  broader design remains AUD-065. B-105/AUD-066 records the one graded-answer concern. Model:
  author-confirmed Astra. No push. T45 still blocks T26.

## Not yet specified

T14 resolved on 26 October 2026: the pinned ATT&CK reference corpus is delivered. During its
review the author ruled that internal document owners are responsible teams, separate from
login accounts. The spec and T15 now validate team ownership separately from people mentioned
in document contents. External ATT&CK ownership identifies MITRE as publisher.

- The Codex brief's wording and the consistency script's checks: written after the tables exist.
- The tuning file's pairs and the calibrated refusal threshold itself; the judge model; the
  phase 1 questions and their gold IDs; the on-versus-off results for the re-ranker and BM25:
  phase 0 and phase 1 build, under ticket 06's rules.
- The exact hash fields and slug rules for the finding ID, and whether the answer is structured
  (text plus citation list) or parsed from prose: phase 0 build.
- The exact colours and dark-mode treatment of the answer's visual hierarchy (ticket 07,
  decision 9), and the progress patterns borrowed from Anthropic's and OpenAI's docs (decision
  4's build condition): the build ticket, with the author's screenshot review.
- The exact dagre spacing, node sizes and dark-mode shades of the Graph tab (ticket 08,
  decision 6), and the read-only test's list of switched-off behaviours (decision 8): the build
  ticket, with the author's screenshot review.
- The graph integrity check is delivered in ticket 19; ticket 20's GEXF export compares against
  it (ticket 08, decision 9).
- The spec for phases 0 and 1: written, [spec.md](spec.md). The build tickets: cut, 09 to 42 under
  `issues/`.

## Out of scope

- Any change to the Port's behaviour that the use case does not require.
- Any change to v1.
- The bootcamp's deliverables (project document, demo video, submission).
