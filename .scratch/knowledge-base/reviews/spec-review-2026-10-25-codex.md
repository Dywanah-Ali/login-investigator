# Spec review: the knowledge base, phases 0 and 1

- **Spec:** `.scratch/knowledge-base/spec.md` at commit `8a678d8`, with no uncommitted changes at review start
- **Reviewer:** codex, GPT-6
- **Date:** 2026-10-25
- **Sources read in full:** `.scratch/knowledge-base/map.md`; decision tickets `02-store-and-retrieval-provider.md`, `03-embedding-and-reranking.md`, `04-synthetic-data-and-ground-truth.md`, `05-agent-tools-for-the-knowledge-base.md`, `06-eval-design.md`, `07-explained-alert-screen.md`, `08-graph-screen-and-gephi-export.md`, including every comments section; research notes 01, 02, 03, 05, 06 and 08; the complete HTML prototypes 07 and 08. All ticket and research paths are under `.scratch/knowledge-base/`. Source comparison was independently delegated and consolidated here.
- **Repo rules read:** `AGENTS.md`, `CLAUDE.md`, `GLOSSARY.md`, `docs/agents/domain.md`, `docs/api-contract.md`; relevant entries in `docs/audit/improvement-register.md`. No ADR directory exists.
- **Code checked:** `backend/login_investigator/{generator,rules,loader,tools,reputation,agent,investigations,investigation_policy}.py`; `backend/api/{app,services}.py`; `backend/evals/{run,scoring,api_runner}.py`; `backend/evals/questions.json`; `backend/pyproject.toml`; existing generator, rules, search, stats, agent, investigation-policy, startup, investigations API, eval-scoring, eval-results, eval-question, core-boundary and key-isolation tests; frontend Alerts, Investigator and repository-rules tests. Pass 7 was independently delegated, with the three discrepant code claims rechecked during consolidation.

## Verdict

**Not ready.** The graph integrity gate can pass with incorrect relationships. Five major gaps also need resolution before their affected build tickets are cut. Most source decisions are faithfully carried forward.

| Severity | Count |
|---|---|
| blocker | 1 |
| major | 5 |
| minor | 6 |
| nit | 1 |

## Findings

Most severe first. One row per finding. Spec line numbers refer to the reviewed version above. `reopen?` identifies an accepted decision with a concrete conflict or risk, rather than a preference for a different design.

| ID | Severity | Pass | Status | Spec section |
|---|---|---|---|---|
| R1 | blocker | 4 | verified, reopen? | The graph: integrity check |
| R2 | major | 2, 4 | verified, reopen? | The eval: retrieval gate and question mix |
| R3 | major | 1, 2, 4 | verified, reopen? | Three verdicts; switches settled by measurement |
| R4 | major | 2, 4 | verified, reopen? | The graph: isolated nodes |
| R5 | major | 1, 5 | verified | Further Notes: build order |
| R6 | major | 4 | verified | Langfuse; Testing Decisions |
| R7 | minor | 1 | verified | The eval: judge |
| R8 | minor | 1 | verified | The synthetic world and the dataset |
| R9 | minor | 2 | verified, reopen? | Further Notes: phase split |
| R10 | minor | 7 | verified, reopen? | The Port's ground-truth file stays |
| R11 | minor | 7 | verified, reopen? | The staleness guard |
| R12 | minor | 7 | verified | Problem Statement |
| R13 | nit | 6 | verified | Domain vocabulary |

### R1: Counts cannot prove that graph relationships match the source

- **Spec says:** "edge count per type equals row count; both ends exist" (line 447), and "Each gate gets a break-the-gate test that corrupts one input and proves the gate fails" (line 678).
- **Source or code says:** "a silent build error would become a confident wrong answer that the gates catch only where a question happens to cross it" (`issues/06-eval-design.md`, comments, lines 106–107). The source then prescribes the same count checks, so this risk is inherited from an agreed decision.
- **Problem:** Swap two memberships between existing people while keeping both groups connected. Every node count, edge count, endpoint-existence check and isolation check still passes, but the graph grants the wrong privileges. The exact-set eval only catches this if one of its questions crosses the changed links. The integrity gate therefore can pass while the requirement it protects fails.
- **Suggested fix:** Compare source record identities, endpoints, relationship types and the attributes used by queries with the built graph, in addition to counts. Name a corruption test that swaps valid endpoints without changing counts. This strengthens the existing integrity check rather than adding another test boundary.

### R2: Document retrieval gates also demand graph records and evidence for absent topics

- **Spec says:** "every gold chunk and record ID among the 20 fused candidates and among the chunks the model received" (lines 626–627). It also says: "Every question carries a provenance line and gold IDs, or it is dropped" (lines 640–641).
- **Source or code says:** The spec gives graph records their own identifier at line 468 and their own exact-set walk gate at line 629. It explicitly includes graph-only control questions and four absent topics at lines 637–639. `issues/06-eval-design.md`, decisions 1–3, contains the same overlapping requirements.
- **Problem:** A pure graph lookup returns graph records, not fused document chunks. An absent-topic question deliberately has no supporting document ID. Read literally, these gates either fail valid graph answers or exclude the refusal cases the eval is required to contain. The missing rule is which gate and which gold fields apply to each question type.
- **Suggested fix:** State that the two document-retrieval checks apply to gold chunk IDs, the graph check applies to gold record IDs, and mixed questions apply both. Explicitly permit an empty gold evidence set for no-evidence questions, with their expected verdict and other applicable checks still mandatory.

### R3: Turning off the re-ranker can disable the required refusal behavior

- **Spec says:** "If the re-ranker is switched off, `none` falls back to the empty-result rule" (lines 427–428). A switch stays on only if it improves retrieval passes or first-gold ranks, and "A tie goes to off" (lines 654–657).
- **Source or code says:** "an absent topic needs verdict `none`" and "100% on say-no, every run" (spec lines 631–633). `research/03-embedding-and-reranking.md`, line 193, defines the empty-result rule as "Both filtered legs return zero rows". `issues/06-eval-design.md`, decision 9, additionally requires that the tuning file is "re-scored with whatever score source remains" and comparisons "re-run per phase and whenever the corpus changes shape".
- **Problem:** Exact nearest-neighbor search over a nonempty, unfiltered corpus can return candidates even when the topic is absent. With only the empty-result refusal rule, that search cannot produce the required `none` verdict. The specified comparison can nevertheless select off because its selection criteria do not include refusal. The spec also drops the source's remaining-score calibration and repeat-comparison conditions.
- **Suggested fix:** Make passing the existing refusal gates a condition of accepting either switch configuration. Restore the calibration and comparison lifecycle hand-offs. Before accepting re-ranker off, require evidence that its remaining-score policy satisfies those gates; otherwise retain the working configuration and record why.

### R4: The isolation check rejects permitted chunks that name no entity

- **Spec says:** "Plus no isolated node outside a short allowed list (the two never-mentioned users)" (line 451).
- **Source or code says:** "Chunks are nodes too, joined to entities by `mentions` edges" (spec lines 435–436), and mentions are "found by ingestion from the text, never hand-written" (lines 361–362). The corpus permits policies, noise documents and a runbook without a technique ID (`issues/04-synthetic-data-and-ground-truth.md`, decisions 10–12).
- **Problem:** A valid chunk containing generic password guidance can mention no person, device, asset or technique. It becomes an isolated node under the specified graph model and fails the build, even though no corpus rule requires each chunk to name an entity. This is a permitted-input counterexample, not a claim that the unwritten corpus already contains such a chunk.
- **Suggested fix:** Distinguish legitimate chunks with zero extracted mentions from missing graph links. Require their actual links to match the extracted mention set, including an empty set. Keep unexpected isolation checks for organisation records where relationships are required.

### R5: The build order puts the first eval questions after retrieval

- **Spec says:** "the order is the dependency floor, not the ticket list" (line 729). Hybrid retrieval is item 8 (line 740), while the knowledge-base question file and first end-to-end questions are item 11 (line 743).
- **Source or code says:** "The eval set exists before the first retrieval runs" (`map.md`, Notes, Evaluation stance).
- **Problem:** Following the dependency floor allows retrieval to be built and run before its first agreed questions and gold evidence exist. That reverses the map's explicit evaluation stance. The later phase 1 expansion does not require delaying the initial phase 0 cases.
- **Suggested fix:** Put the first question fixtures and their gold evidence before the first retrieval run. Leave full runner integration and the phase 1 question expansion at their later positions.

### R6: Langfuse has requirements but no named proof for its enabled behavior

- **Spec says:** "The JSON file is written first; an upload failure is logged loudly and noted in the summary" and "A masking hook is wired from day one" (lines 666–668). The build order only names "each part tested with the switch off" (line 744).
- **Source or code says:** User stories 83–85 require traces, upload-failure reporting and human-label export. `docs/audit/improvement-register.md`, AUD-036, says the adopted integration "closes on one eval run visible in Langfuse". The six test doors at spec lines 683–690 name no enabled-upload, masking, failure-ordering or label-export checks.
- **Problem:** Switch-off tests prove that the app works without Langfuse. They cannot prove that enabling it produces the promised mirror, preserves the local result on failure, applies masking or exports labels. The audit's live closure evidence is also absent from the acceptance list.
- **Suggested fix:** Assign deterministic enabled-handler, upload-order, failure, masking and export checks to the existing test doors using a fake destination. Add the already-agreed visible eval run as the live acceptance evidence. No additional test door is needed.

### R7: The agreed judge agreement report is missing

- **Spec says:** "Reported with its interval, never failing a run in phase 1" (lines 647–648).
- **Source or code says:** "judge-versus-author agreement is reported as Cohen's kappa once labels exist" (`issues/06-eval-design.md`, decision 6, line 45).
- **Problem:** The spec retains storage and export of the author's labels but drops the agreed conditional agreement report. A ticket built solely from the spec would have no obligation to implement it.
- **Suggested fix:** Restore the conditional kappa report and assign its deterministic calculation to the eval-runner test door. The judge remains advisory.

### R8: The scenario scheduling condition was narrowed

- **Spec says:** S6 runs "on a day that overlaps neither S1 nor S2" (line 311); the twins are described without a scheduling condition at lines 314–317.
- **Source or code says:** "S6 and the twins fit inside the window on days that do not overlap the old stories" (`issues/04-synthetic-data-and-ground-truth.md`, conditions, lines 94–95).
- **Problem:** The source constrains all new stories against the old scenario days. The spec retains only part of that constraint for S6, with no recorded ruling relaxing the rest.
- **Suggested fix:** Restore the full scheduling condition beside the new stories and check it at the generator test door.

### R9: The Alerts API addition belongs to two different phases

- **Spec says:** "The finding ID in the core and the Alerts reply" is phase 0 (line 735), but "Phase 1 adds the API additions" (line 751).
- **Source or code says:** The decisions log records "API additions and screens in phase 1, everything else in phase 0" (line 776). The earlier source places the Alerts field in phase 0 (`issues/05-agent-tools-for-the-knowledge-base.md`, hand-offs, lines 95–98).
- **Problem:** The latest ruling and the build table disagree. The exception is small, but ticket authors would assign the same API change to different phases.
- **Suggested fix:** Align the table with the latest ruling by keeping core IDs in phase 0 and the Alerts field in phase 1, or have the author explicitly record the early Alerts-field exception.

### R10: The reason for retaining the Port answer key names the wrong consumer

- **Spec says:** "The Port's scorer reads its own ground-truth file for names such as `$S2_IP`" (lines 336–337).
- **Source or code says:** `backend/evals/scoring.py:143–147` reads substitutions from the question file using `patterns = document["patterns"]`. Its ground-truth read at lines 43–45 extracts `scenarios.S5.text` for injection grading.
- **Problem:** Keeping the file is justified, but the stated mechanism is inaccurate. A builder following this rationale could update the wrong source of eval expectations.
- **Suggested fix:** Keep the ruling. Describe the actual ground-truth consumers, including injection grading, and distinguish them from question-file pattern substitutions.

### R11: Invalid logs do not currently stop server startup

- **Spec says:** "startup fails loudly ... in the same way a log that fails validation is refused today" (lines 387–389).
- **Source or code says:** `backend/api/services.py:58–67` catches log validation failure, stores an endpoint error and continues opening memory. `backend/tests/test_api_startup.py:71–78` proves dataset endpoints return 500 while `/api/rules` returns 200.
- **Problem:** The new startup-refusal ruling is clear, but its comparison to existing behavior is misleading. Reusing the old behavior literally would leave the server running.
- **Suggested fix:** Keep the new startup refusal and remove the claim that it follows the existing invalid-log startup mechanism.

### R12: Existing reputation lookups also support live requests

- **Spec says:** "The agent can see only the sign-in log and saved IP reputation lookups" (lines 18–19).
- **Source or code says:** `backend/login_investigator/reputation.py:54–58` uses an available key to call `_fetch(...)` when no saved response exists, returning `source="live"`.
- **Problem:** The current-capability description unnecessarily excludes an existing path.
- **Suggested fix:** Remove "saved" from this sentence.

### R13: The spec drifts from the glossary's Investigation vocabulary

- **Spec says:** "the same evidence and graph payload for the whole conversation" (lines 576–577), with similar domain usage throughout. Its header also says Dataset is defined in the root glossary (lines 8–9).
- **Source or code says:** `GLOSSARY.md`, Investigation, defines the persisted line of inquiry and explicitly lists "Conversation, thread, chat, session" under "Avoid". The current glossary has no Dataset entry.
- **Problem:** The spec uses an avoided synonym for the persisted domain object and overstates the glossary's contents. References to the chat as a screen are not the problem.
- **Suggested fix:** Use Investigation when referring to the saved domain object. Remove Dataset from the existing-definition claim or identify it as a term awaiting definition.

## Checked and found clean

1. Faithful to sources: PostgreSQL, NetworkX, read-only roles, SQLite memory, retrieval settings, fusion traps, corpus counts, blind writer brief, seven tools, artifacts, middleware, screen choices and export requirements are carried forward. Explicit B2, B3, dataset-folder, answer-key and ID-precedence rulings correctly supersede earlier text. Source omissions are listed above.
2. Consistent with itself: Story counts, tool counts, corpus size, citation letters, scope boundaries, stable-ID precedence and screen placement agree. Graph/eval rules and the API phase exception are the specific inconsistencies recorded above.
3. Stories against decisions: The 87 stories were mapped to the world, corpus, store, retrieval, tools, evidence/graph screens, reports, eval and observability decisions. The report can name failed steps; its completeness wording was read with that explicit exception. The advisory faithfulness judge was not misrepresented as a hard guarantee.
4. Provable: Six shared test boundaries, fake model and retrieval services, real database checks, artifact round trips, existing safety nets, model evals and dated live acceptance provide appropriate proof points. R1–R6 identify gaps in particular gates or coverage, not a need for a new testing architecture.
5. Scope: Phases 0 and 1 remain the deliverable. History, attack paths, risk scores, GRC, memory migration and incremental sync remain deferred. Required travel and handover documents for twins do not silently add the later travel-analysis phase.
6. Template and repo rules: The expected major sections and user-story form are present. Core separation, thin APIs, read-only tools, plain-text data rendering, protected secrets, agreed screens and author-controlled changes are preserved. API examples come from the cited screen drafts. Domain vocabulary exceptions are in R13.
7. True to the code: Generator seed/window/users/scenarios, four rule thresholds, column validation, the three-tool tuple, model/agent factories, existing middleware and streaming, SQLite memory, eval targets, runner isolation, fingerprint extension points and cited prior-art tests were checked. Only the three local descriptive inaccuracies in R10–R12 were found in those claims.

## Questions for the author

None requiring additional information to complete this review. Findings marked `reopen?` identify proposed corrections to accepted decisions and remain for the author's ruling. No spec changes were made.

## Not reviewed

No implementation was changed or executed. No backend/frontend test suite, paid eval, database build, live service or browser acceptance run was performed. Prototype source was read, but visual approval was not repeated. External vendor claims, pricing, retirement dates and package behavior were not independently revalidated because no finding depends on a new external fact. Course solution kits were not opened.

Only this review file was written. The spec, tickets, map, glossary, audit register and code remain unchanged under the review skill's read-only boundary.
