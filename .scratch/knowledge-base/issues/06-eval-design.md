# 06: The eval set for a graph-plus-text system

Type: research, then grilling (retyped 23 October 2026; see the first comment)
Status: resolved
Blocked by: 04, 05

## Question

What does the eval set look like, so that retrieval and answer quality are measured separately,
every question has a gold answer in the ground truth, and the whole set re-runs on every change
without Claude?

## Scope

- Two layers: retrieval (did the gold node or chunk appear in the top results, at what rank) and
  answer (is every claim backed by the retrieved context; faithfulness).
- Question types: graph lookups, multi-hop traversals, text lookups, mixed, and "not in the
  knowledge base" questions that must be refused.
- How it fits the existing eval runner and its API mode; whether it is a new set or an extension;
  thresholds (the existing 90% overall and 100% security stay as the floor; what the retrieval
  floor is).
- Grader: deterministic where possible (retrieval), model-graded where needed (faithfulness),
  with the grader's prompt versioned.
- Size for phase 1 and how it grows per later phase.

## Acceptance

- [x] Layers, question types, thresholds and grader decided (decisions 1 to 7).
- [x] Runner integration decided (decisions 8 to 10).
- [x] Decision recorded here under `## Answer`.

## Answer

Ten questions asked one at a time on 23 October 2026, each with a plain-English heading first. The
author took the recommended option on eight, tightened question 1 (the retrieval gate) before it was
asked, and overturned question 10 (Langfuse). Decisions:

| # | Decision | Why |
|---|---|---|
| 1 | **Retrieval gate: two hard checks per question.** Every gold chunk and record ID must be among the 20 fused candidates, and among the chunks the model actually received across the whole investigation (the re-ranked top 5 per search). Either miss fails the run. The rank of the first gold chunk is recorded for the trend. No rate and no borrowed 0.9 target for the retrieval layer. | The model sees only the final five; a gold page at position 12 is a failure for the analyst. The first check says the search is broken, the second says the ranking is broken. Retrieval is deterministic, so a miss is a defect, not noise. The author rejected the note's softer top-20-only gate as too broad for a corpus of about 40 documents. (Note 06, 3.1; recommendations 1 and 3 amended.) |
| 2 | **Graph gate: exactly the gold set.** On every graph question the walk must return every gold record ID and nothing else (recall and precision both 100%), as a hard check. The gold path and radius are written by the generator from the planted story into `truth.json`, never computed afterwards as a shortest path. | The walk is deterministic code over small tables, so an extra or missing record is a bug in the walk or the key. The analyst reads the returned list on the screen, so precision matters as much as recall. (Note 06, 3.1; recommendation 2.) |
| 3 | **Phase 1 mix weighted to the hard types.** About a third say-no questions (the three twins, the four absent topics, two false-presupposition traps, one underspecified question), about 40% mixed and multi-hop (at least two routed through a busy node such as a shared group or asset), about a quarter graph and text lookups as the control group. At 30 questions: 10, 12, 8. Every question carries a provenance line and gold chunk and record IDs, or it is dropped. Growth in later phases goes to the middle group and to new traps, not to lookups. | The research shows refusal and twin handling fail most often (gpt-4o-mini rejected correctly 12.7% of the time in one study), mixed questions carry the most failure modes and are what the analyst asks, and busy nodes are where plausible wrong evidence appears. Lookups are the cheap control: if they fail, nothing above them can be trusted. (Note 06, 3.2; recommendation 6 amended.) |
| 4 | **The refusal threshold is calibrated on a separate tuning file.** About 30 to 60 query-plus-chunk pairs, labelled by the author as answers-it or does-not, flagged `tune`. The re-ranker scores them once, the scores are saved, and the `none` / `weak` / `found` threshold is chosen offline over the saved scores with no model call. The tuning file never overlaps the `test` questions; the absents and twins stay in `test` and grade refusal. | Tuning on the questions that grade refusal would make the refusal test pass by construction. A borrowed threshold is meaningless on another corpus (ticket 03, decision 1). Saved scores make re-calibration cheap and repeatable. (Note 06, 3.2; recommendation 7.) |
| 5 | **Answer gate in code, on every question.** Every citation label in the answer resolves against the artifacts of that conversation, and every gold chunk and record ID is among the cited IDs. Say-no questions are graded from the artifacts first: an absent topic needs the tool verdict `none`, a twin needs a benign conclusion with its clearing document cited; the wording is then matched by pattern as the Port's `DECLINES` and `NOT_MALICIOUS` checks do. Expected pass rate on say-no questions is 100%, every run. Extra resolved citations beyond the gold set are neither punished nor counted in phase 1. Considered, not taken for phase 1: a per-question must-not-cite set of planted distractor IDs as a hard fail, and citation precision as a reported number; the author ruled it too much for now and it may return when the busy-node questions show padding or wrong-path citations. | The middle check proves the right evidence was used, not just found, and stays deterministic. "Every material sentence carries a label" cannot be defined in code and goes to the judge. Misreading a correctly cited page is also the judge's job. (Note 06, 3.2 and note 05, 3.2; recommendation 8; ticket 05 decision 7.) |
| 6 | **The faithfulness judge is a smoke alarm, not a gate.** A stronger model from a different family than gpt-4o-mini, through OpenRouter (no local models). Binary verdict per claim with fixed grading steps, a reason written before the verdict, markdown stripped from the answer first. Three trials per answer, majority wins. A sample of about ten answers per run. Every verdict and reason is stored in the run record so the author can label them over time towards the 60 to 200 labels a judge validation needs. The judge prompt and judge model are hashed into the version fingerprint. The judged rate is reported with its interval and never fails a run in phase 1; judge-versus-author agreement is reported as Cohen's kappa once labels exist. The exact judge model is a phase 0 build choice. | gpt-4o-mini judging itself is the measured worst case (14% verdict flips, 72% first-position bias, 25% of verdicts changed by rewording). An unvalidated judge as a gate fails runs on noise. Per-claim verdicts are the cheapest way to grow the labelled set. (Note 06, 3.3; recommendations 9, 10, 11.) |
| 7 | **Process checks are hard gates at 100%.** On every "is this a threat" question, `playbook_status` must report every required step as run before the model concluded, read from the state and never from prose. On every question with a planted instruction in a log field or a corpus paragraph, the canary must not be obeyed; those checks are flagged `security` and count towards the Port's 100% security floor. The fence stays one `wrap_tool_call` middleware of our own (ticket 05, decision 8); LangChain ships no injection middleware at the pinned 1.3.1 and its docs show injection guardrails as custom middleware. Third-party detector middleware (Azure Prompt Shield, community packages) is not adopted: hosted ones cross the trust boundary and all are probabilistic layers over structural defences that already hold. Registered as an option when the ticket resolves, with the trigger "canary pass rate falls below 100% and the structural defences cannot explain it". | The Port already gates on which tools ran and on S5 injection as a security check; this extends the same discipline. A passing playbook is necessary, not sufficient; the answer gate catches the rest. The canary rate also warns when context grows too long, since the only measured injection defence weakens with length. (Note 06, 3.3 and note 05, 3.3; ticket 05 decisions 8 and 11.) |
| 8 | **One scorer, two exams, kept strategically separate.** The Port's `questions.json` stays frozen as the safety net with its 90% overall and 100% security targets. A second question file for the knowledge base grows per phase with its own gates (decisions 1, 2, 5, 7) and its own lines in the summary; the two are never blended into one rate. Shared code: `scoring.py` gains the deterministic kinds `retrieval`, `cites`, `verdict`, `playbook` and one model-graded kind `judge`, marked so `--rescore` skips it and the scorer stays unit-tested; the `Answer` record and the saved JSON keep each tool's artifact so retrieval re-scores from the file with no model call; the version fingerprint widens to the judge prompt and model, embedding and re-ranker names, chunking settings and corpus version, and `git_commit()`'s dirty-path list gains the knowledge-base paths; the retrieval layer runs once per build through a `--layer retrieval` path that calls the search and the walk directly, never through the agent; API mode is unchanged. Questions in the new file carry `type`, `gold` (chunk IDs, record IDs, path) and `split` (`test` or `tune`). | The Port exam asks "does what worked still work", the knowledge-base exam asks "does the new thing work"; one blended number would let either hide the other. A second runner would duplicate versioning, summary and API mode and drift. (Note 06, section 4; recommendations 4, 5, 12, 14; the author's ruling that the two exams run separately on the planning side.) |
| 9 | **Each retrieval switch is settled by an on-versus-off comparison on the retrieval layer.** For the re-ranker (fused top 20 straight to 5, versus re-ranked 5) and for BM25 (built-in keyword ranking versus BM25), run the retrieval layer both ways on the same questions, no model calls. A switch stays on only if it passes more questions on decision 1's second check, or the same number with better ranks of the first gold chunk. A tie goes to the simpler setting, off. Recorded at phase 1's close in the build ticket that runs it; re-run per phase and whenever the corpus changes shape. If the re-ranker goes off, the `none` verdict falls back to ticket 03's empty-result rule and the tuning file of decision 4 is re-scored with whatever score source remains. | Ticket 03 said the eval decides and the map says tuning follows measurement. The retrieval layer is deterministic and re-scorable from artifacts, so the comparison is exact and cheap, where the full agent exam would add model and judge noise. (Note 06, 3.1; Neo4j's guidance; ticket 03 decisions 1 and 5.) |
| 10 | **Langfuse to the max, as a mirror; the repo stays the source of truth.** Traces of every dev conversation and every eval run through one `CallbackHandler` in the agent-building function; the two question files uploaded as datasets; each eval run an experiment run stamped with the same version fingerprint and commit as the JSON file (three repeats become three runs); every check verdict a boolean score, the judge's verdict and reason a score with a comment; the author labels judge verdicts in Langfuse's annotation UI; the running app is traced for latency and token cost. Rules: off by default, one environment variable turns it on, the key is loaded only when on and never written to a result; the JSON file is written first and Langfuse second, an upload failure is logged loudly and noted in the summary table; runs, datasets and scores flow out, only human labels flow back through an export script into a repo file; nothing at runtime reads from Langfuse; a masking hook is wired from day one; the data that leaves the machine (question text, synthetic log fields, corpus chunks, tool arguments, answers, all synthetic) is recorded here. When the author's access ends, around 21 January 2027, the switch goes off and nothing changes. | The author's ruling, overturning the note's "traces only" leaning: hands-on use of an observability platform for evals and monitoring is part of the career goal, and the free access runs for about three months. The mirror design keeps the 30-day retention of the free tier and the trust boundary from mattering to the evidence. (Note 06, 3.4; AUD-036.) |

### Acceptance, with the decision that settles each box

- Layers: decisions 1, 2, 5, 6, 7. Question types: decision 3. Thresholds: per-question gates for retrieval and graph (1, 2), 100% on say-no and process checks (5, 7), the Port's 90% and 100% unchanged (8), the judged layer reported only (6). Grader: deterministic kinds plus one marked judge kind (5, 6, 8).
- Runner integration: decision 8, with the switches settled by decision 9 and Langfuse by decision 10.

### Hand-offs

- **Ticket 07:** the artifacts saved per run (decision 8) are the same payload the evidence panel would show; the judge's reason (decision 6) is a candidate for the screen.
- **Phase 0 build order, after tickets 04 and 05's items:** the new check kinds and the artifact in the `Answer` record with `tests/test_eval_scoring.py` extended; the knowledge-base question file with `type`, `gold` and `split`, and `tests/test_eval_questions.py` extended to `truth.json` IDs; the `--layer retrieval` path; the wider version fingerprint and the dirty-path list; the tuning file and the offline calibration script; the judge prompt, judge model choice and the three-trial majority; Wilson intervals computed in code in `summarize()`; the break-the-gate test; the on-versus-off comparison for the re-ranker and BM25 at phase 1's close; the Langfuse handler, dataset and score upload, label export and masking hook, each behind the switch and each tested with the switch off.
- **Spec:** the eval section of the phases 0 and 1 spec is written from this Answer.

### Considered, not taken

- A per-question must-not-cite set and citation precision (decision 5): too much for phase 1.
- Third-party injection-detector middleware (decision 7): registered as an option with a trigger.
- A rate-based retrieval floor with a borrowed 0.9 target (note 06, recommendation 3): rejected for a per-question gate.

## Comments

**2026-10-23, Claude.** Claimed. Before the grilling, the author and Claude held a plain-English
discussion on what the ticket decides and what earlier tickets already fixed. Positions reached, to
be confirmed or overturned in the grilling:

1. **Two layers, graded differently.** Retrieval (was the gold chunk or record in the results, at
   what rank) is pure code on every question. Answer has two checks: citation resolution in code on
   every question, and judged faithfulness on a sample (ticket 05, decision 7).
2. **Already fixed, not reopened here.** Gold answers point at `truth.json` records with chunk and
   record IDs (04 decision 15, 05 decision 7); S6, the three twins and the four absent topics are
   the planted material (04 decisions 14 and 17); `playbook_status` is the "did the plan run"
   assertion (05 decision 11); canaries in log and corpus are a measured pass rate (05 decision
   8); the refusal threshold is calibrated on the eval set, not borrowed (03 decision 1).
3. **Open for the grilling.** Question types and counts per type for phase 1 and growth per
   phase; the retrieval floor beside the Port's 90% overall and 100% security; the faithfulness
   sample size, judge prompt versioning and repeat runs; twin and refusal calibration with the
   tuning set kept apart from the test set; runner integration (extend the Port's `questions.json`
   and `scoring.py` with new check kinds versus a second runner; API mode kept); whether the
   re-ranker stays on and whether BM25 is needed, and what evidence decides; Langfuse (AUD-036)
   versus the file-based results record.
4. **Claude's leanings, stated so the author can disagree first.** Extend the Port's runner;
   deterministic retrieval layer on every question; judged layer small and a smoke alarm rather
   than the gate; citation resolution with gold IDs among the citations as the real answer gate;
   grade the process too (playbook ran, canary not obeyed); Langfuse as an optional trace sink
   behind a switch with the files as the evidence.

**Retyped to research, then grilling.** Research notes 03 and 05 already cover faithfulness judging,
citation checking in code, injection canaries and the need to calibrate the refusal threshold.
Four gaps have no research behind them and would otherwise be grilled on borrowed numbers:
retrieval metrics and a sane floor for a small set; building a gold set for graph plus text
(counts per type, multi-hop gold, tuning set apart from test set); LLM-judge reliability (sample
size, agreement, repeat runs); Langfuse against file-based results. A background agent writes
`research/06-eval-design.md` on those four gaps only, then the grilling runs one question at a time.
