# Map: knowledge-base

Label: wayfinder:map

## Destination

A knowledge base inside the Login Investigator, built around a knowledge graph with RAG as part of
its ecosystem, that gives the investigator agent context about the threat behind a login pattern,
so an alert becomes an explained risk rather than a flagged row. The use case is chosen for the
value it adds to the app, not for the sake of demonstrating RAG.

## Notes

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

<!-- one line per resolved ticket: [title](link): gist -->

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
line holds its edges. **The frontier is tickets 18 and 19**, which have no unresolved blockers; one session
works at a time, so first by number wins.

Ticket 43 was opened on 26 October 2026 by the author's ruling, to restore the Port eval's margin
(Q02 and Q04, AUD-046 and AUD-047) before T14. It is taken ahead of the frontier by that ruling,
and is resolved (see Build tickets resolved). T14 to T17 have since resolved; the frontier
is tickets 18 and 19. Ticket 18, the staleness guard, is next by number.

### Model per ticket (author's ruling, 27 October 2026)

Each build ticket from 17 to 42 carries a `Model:` line under its `Phase:` line. The strongest
models (Fable 5.1 for Claude, Astra for Codex) take the tickets where one wrong choice spreads into
every later ticket; the standard models (Opus 5.5, Sol 6.1) take the rest.

| Model | Tickets | Reason |
|---|---|---|
| Strongest | 17, 19, 22, 24, 26, 27, 28, 29 | Load-bearing seams: the build, the graph, fusion, the tool pattern and fence, the package, the resolver, the playbook hooks and the eval gate |
| Strongest if budget allows | 30, 37, 41 | Judge design, the hardest frontend drawing, the BM25 leg and an honest on-versus-off call |
| Standard | 18, 20, 21, 23, 25, 31 to 36, 38 to 40 | Standard build work on seams the strongest tickets set |
| None | 42 | The author's ticket |

The line advises; it is not a gate. Each of tickets 17 to 41 carries a first acceptance criterion:
before any build work starts, the builder tells the author the ticket's `Model:` line, waits for the
author to confirm the model is set, and records the model used in a dated comment. The independence idea (eval questions in 21 and 40 written by
the other family from the retrieval builder) was proposed and is not ruled.

### Build tickets resolved

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
- The graph integrity check (tables and chunk links against the built NetworkX graph): a phase 0
  build item, recorded in ticket 06's comments on 24 October 2026; the GEXF export test compares
  against it (ticket 08, decision 9).
- The spec for phases 0 and 1: written, [spec.md](spec.md). The build tickets: cut, 09 to 42 under
  `issues/`.

## Out of scope

- Any change to the Port's behaviour that the use case does not require.
- Any change to v1.
- The bootcamp's deliverables (project document, demo video, submission).
