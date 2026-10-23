# Research note 06: the eval set for a graph-plus-text system: retrieval metrics, gold-set construction, judge reliability, and where results live

Ticket: [06-eval-design](../issues/06-eval-design.md)
Date: 23 October 2026
Method: Perplexity first, as the ticket's method line asked. Twenty-five `perplexity_search` calls, most
restricted to primary domains (docs.ragas.io, deepeval.com, docs.langchain.com, neo4j.com,
microsoft.com, microsoft.github.io, langfuse.com, arxiv.org, developers.openai.com), and no
`perplexity_ask` or `perplexity_research` calls (the deep-research tool timed out on ticket 05 and was not
tried). Nineteen WebFetch calls opened primary pages; none failed, two returned less than asked (the
GraphRAG-Bench abstract page does not carry the retrieval metrics, and the RGB abstract does not name
its rejection-rate measure). Keenable was not needed because Perplexity never returned empty. Direct
reads of the project's own `backend/evals/scoring.py`, `run.py` and `questions.json`. No project data,
log field or corpus text was sent anywhere; every query was a generic technical question. `[P]` marks
a claim verified on a primary page opened in this research; `[V]` marks a claim seen only through a
search snippet or an aggregator. Small-sample confidence intervals in section 3.1 are computed by the
author of this note (Wilson score interval), not borrowed.

**Fixed constraints from the ticket (author and Claude, 23 October 2026, not reopened here).** Two
layers graded differently: retrieval in code on every question, answer by citation resolution in code on
every question plus judged faithfulness on a sample (ticket 05, decision 7). Gold answers point at
`truth.json` records with chunk and record IDs (04 decision 15, 05 decision 7). S6, the three benign
twins and the four absent topics are the planted material (04 decisions 14 and 17). `playbook_status` is
the "did the plan run" assertion (05 decision 11). Canaries in log and corpus are a measured pass rate
(05 decision 8). The refusal threshold is calibrated on the eval set, not borrowed (03 decision 1). The
Port's 90% overall and 100% security targets stay as the floor. Research notes 03 (section 3.8) and 05
(section 3.2) already cover faithfulness judging, citation checking in code and the record fields; this
note does not repeat them.

## 1. The question

Ticket 06 decides what the eval set looks like for a system that walks a small graph in code and
searches a small corpus with hybrid retrieval, so that retrieval and answer quality are measured
separately, every question has a gold answer, and the set re-runs on every change without Claude.
Four gaps had no research behind them: which retrieval metrics and what floor on a set of 25 to 40
questions; how a gold set for graph plus text is composed, including the tuning-versus-test split for
the refusal threshold; how far an LLM judge can be trusted on a small sample; and whether Langfuse
adds anything the file-based record lacks. This note separates what the sources say (section 3) from
what it recommends (section 5). The author rules.

## 2. The criteria

| Criterion | Source |
|---|---|
| Retrieval scored in code against gold chunk and record IDs, on every question | ticket 06 scope; 05 decision 7 |
| Answer gate is citation resolution in code; judged faithfulness is a sample, not the gate | ticket 06 comment, leaning 4 |
| Twins come back benign; absent topics are refused; both measured | 04 decisions 14 and 17; 03 section 3.8 |
| Refusal threshold calibrated on questions that do not also grade it | 03 decision 1; ticket 06 comment 3 |
| The set re-runs without Claude; repeated runs; prompt version on every result | `run.py` as it stands |
| 90% overall and 100% security stay; a retrieval floor is added beside them | ticket 06 scope |
| Grader prompt versioned | ticket 06 scope |
| Evidence is a file in the repo; nothing pushed before review | CLAUDE.md working rules |
| Data crosses a trust boundary when it leaves the server; keys only in `.env` | CLAUDE.md security rules |

## 3. Findings

### 3.1 Retrieval metrics and a floor for a small set

| Fact | Consequence for this project | Status |
|---|---|---|
| RAGAS defines **context recall** three ways: LLM-based (claims of the reference supported by retrieved context), non-LLM (relevant contexts retrieved / reference contexts), and **ID-based** (`IDBasedContextRecall`: reference context IDs found in retrieved IDs / total reference IDs). **Context precision** is the mean of precision@k over the ranks of relevant chunks; `IDBasedContextPrecision` is retrieved IDs found in reference IDs / retrieved IDs. The legacy classes are deprecated in 0.4 and removed in 1.0. | With stable chunk IDs from `truth.json`, the ID-based formulas are pure code and need no model. They are a few lines; the library itself is not needed. | [P] docs.ragas.io stable, context recall and context precision pages |
| DeepEval maps its three retriever metrics to components: contextual **precision** tests the re-ranker (relevant nodes ranked above irrelevant), contextual **recall** tests the embedding model (everything needed for the expected output is present), contextual **relevancy** tests chunk size and top-k. All three are LLM-judged in DeepEval and the two reference-based ones need an `expected_output`. | The split matches note 03's hand-off: recall at 20 before re-ranking tests the fused list; precision at 5 after re-ranking tests the re-ranker. Score both in code from IDs, not with DeepEval's judge. | [V] deepeval.com RAG evaluation guide and contextual recall page, via snippets |
| Neo4j's own evaluation harness for its agent-memory library scores retrieval relevance as **recall@k of returned entity IDs against labelled expected entity IDs per query**, with `k` set per case (example `k=5`), a CI gate at `--min-score 0.9`, one JSONL row appended per run for a trend, and a self-test that swaps one expected ID for an absent one to prove the gate can fail. It gives no minimum number of cases. | A precedent for scoring graph lookups by ID set, for a 0.9 gate, and for a "break the gate on purpose" test. The trend file is what `summary.md` already is. | [P] neo4j.com/labs/agent-memory evaluation page |
| Neo4j's practitioner guidance for choosing between vector and graph retrieval: build a test set that mirrors traffic, with single-hop lookups, multi-hop questions and cases needing evidence from more than one source; compare context precision, context recall, faithfulness, latency and token cost; "if GraphRAG doesn't move those numbers, the added complexity isn't worth it". | The same numbers must be reported with the graph walk and without it, or the graph cannot be justified by evidence. | [V] neo4j.com blog, vector RAG vs GraphRAG, 2026 |
| Microsoft GraphRAG does not score retrieval at all. BenchmarkQED's AutoE judges **answers pairwise** on comprehensiveness, diversity, empowerment and relevance, in counterbalanced order, six trials per query, GPT-4.1 as judge, win = 1, tie = 0.5, loss = 0; AutoQ generates four query classes (data-local, activity-local, data-global, activity-global), 50 per class. | Not a model for this project: the questions here are local and have gold IDs, so a pairwise answer judge without ground truth is the wrong tool. The counterbalanced-order and multiple-trial practice is reused in 3.3. | [P] microsoft.com research blog, BenchmarkQED |
| GraphRAG-Bench (arXiv 2506.05690) scores retrieval with **evidence recall** (share of reference claims supported by the retrieved context) and **context relevance** (semantic similarity of question and retrieved evidence), and ranks questions by knowledge breadth (triples needed) and reasoning depth (hops between them). | Evidence recall is the LLM-based RAGAS recall under another name. The breadth-and-depth labelling is a useful way to tag each question in the set. | [V] arXiv HTML via snippet; the abstract page opened does not carry the metrics |
| KGQA retrieval papers score the retriever with **Hit** (at least one gold answer entity retrieved), **Recall** (share of gold entities retrieved) and **Precision** (share of retrieved entities that are gold); GTSQA adds recall, precision and F1 of **ground-truth triples** in the retrieved subgraph and shows that shortest paths are "not guaranteed to be the correct paths". A controlled study found that once the answer chain is in the prompt, lowering context precision from 1.00 to 0.51 changed answer F1 by +0.003, so "retrieval budget belongs on recall". | For the graph layer, score the **set of record IDs** the walk returned against the gold set (recall and precision; a hit alone is too weak), and the gold path, not the shortest path. Precision matters less than recall for the answer, but it still matters for the screen and for cost. | [V] arXiv 2510.07484, 2511.04473, 2609.10237 via snippets |
| Multi-hop QA papers score passage retrieval with Recall@k averaged over gold passages, and separately with **full support recall** (FSR@k, "the proportion of questions for which all supporting passages are retrieved") or "all-gold@k". On MuSiQue, recall@5 = 0.506 while all-gold@5 = 0.184: averaged recall hides that most multi-hop questions never had all their evidence. One study found retrieval recall and "fact actually present" nearly uncorrelated on failing hops. | A multi-hop question whose gold is several chunks or records must be scored **all-or-nothing per question** (every gold ID in the top k), with per-ID recall kept as a diagnostic. Averaged recall would let a half-retrieved question pass. | [V] arXiv 2609.07050, 2607.00725, 2609.17043 via snippets |
| Standard IR definitions: Recall@k and Precision@k are order-unaware; MRR is the mean of 1 / rank of the first relevant item and suits "one correct answer" tasks; NDCG@k discounts by log2(rank + 1) and needs graded relevance to add anything over binary labels. The re-ranker's documentation treats recall@10, MRR and nDCG@10 as the standard portfolio. | With binary relevance and one to three gold chunks per question, NDCG adds nothing over recall@k plus the rank of each gold chunk. Record the rank; report recall@20, all-gold@5 and MRR of the first gold chunk. | [V] pinecone.io and weaviate.io metric pages, cohere.com blog |
| **A pass rate on n items is a binomial estimate.** Wilson 95% interval, computed for this note: 27/30 (90%) gives roughly 0.74 to 0.97; 36/40 (90%) gives roughly 0.77 to 0.96; 81/90 (90%, three runs of 30) gives roughly 0.82 to 0.95, and that last one is optimistic because repeated runs of the same question are correlated. Practitioner guides agree: under about 30 cases a score is "a vibe check"; to see a 5-point change with confidence takes about 250 to 400 cases; report an interval, use the Wilson form near 0.9 because the plain form "overstates certainty", and compare two versions with a paired test on the same questions. | A set of 25 to 40 questions cannot measure a 90% floor as a percentage: a single extra failure moves it by 3 points and the interval is 20 points wide. What it can measure is **"every question that must pass, passed"**: deterministic checks that are expected to pass every time on a deterministic layer. The floor for retrieval should therefore be stated per question, not as a rate. | derived; [V] tmls.nyc eval-driven development, ai-tldr.dev sample-size page, dev.to posts, via snippets |
| Retrieval in this project is deterministic once the database is built (same embedding, same SQL, same fusion, same re-ranker call), apart from embedding-API drift. | Retrieval needs one run per build, not three, and it can be re-scored from saved artifacts without any model call. The 3-run default exists for the agent's non-determinism, not for retrieval. | design consequence of notes 02 and 03 |

**What this means for ticket 06.** Score the text layer in code with three numbers per question:
recall@20 of gold chunk IDs in the fused list (every gold ID present, all-or-nothing), all-gold@5 after
re-ranking, and the rank of the first gold chunk (for MRR). Score the graph layer as set recall and set
precision of record IDs returned by the walk against the gold radius in `truth.json`, with the gold path
written by the generator, not derived as a shortest path. State the retrieval floor per question (every
question's recall@20 must be 1.0, because the corpus is small and retrieval is deterministic) and keep
all-gold@5 and MRR as reported numbers with a target, not a gate, until the re-ranker comparison in note
03 has run. Report every rate with its Wilson interval so the 90% overall figure is read honestly at
this size.

### 3.2 Building a gold set for graph plus text

| Fact | Consequence for this project | Status |
|---|---|---|
| RAGAS test-set generation builds a knowledge graph from the documents (entities and keyphrases as node properties, relationship builders linking nodes that share them) and synthesises four query types: single-hop specific, single-hop abstract, multi-hop specific (facts from two or more sources), multi-hop abstract. The stable page states no default proportions; the old 0.1 API used `simple 0.5, reasoning 0.25, multi_context 0.25`. A scenario is nodes plus query length, style and persona. | The taxonomy maps onto this project's types (graph lookup, text lookup, multi-hop, mixed). A multi-hop gold is written as a path through linked nodes, which is what `truth.json` already holds. The 50/25/25 split is a starting ratio, not a finding. | [P] docs.ragas.io test-data-generation page; [V] 0.1.21 page via snippet |
| HybridRAG-Bench grounds every question in an explicit knowledge-graph reasoning path plus the supporting text chunks, obscures intermediate nodes in multi-hop questions, makes "difficult multi-hop" questions by routing through high-degree entities, and reports its mix per domain: single-hop 25 to 29%, single-hop with condition 13 to 19%, multi-hop 15 to 19%, difficult multi-hop 13 to 17%, counterfactual 6 to 18%, open-ended 5 to 18%. | Two usable rules: write the gold as **path plus chunks** (both IDs), and plant at least one multi-hop question through a high-degree node (a shared group or asset), since that is where spurious retrieval appears. | [V] arXiv 2602.10210 via snippet |
| GraphRAG-Bench (2506.05690) orders tasks by level (fact retrieval, complex reasoning, contextual summarise, creative generation), controls difficulty by triples needed and hops between them, and **discards any question for which no evidence triple can be inferred from the corpus**. It notes that HotpotQA is 78% fact retrieval and MultiHop-RAG has no fact retrieval at all, both skewed. | Every question keeps a provenance line to its evidence; a question without one is dropped. Cover all four of this project's types rather than letting lookups dominate. | [V] arXiv 2506.05690 HTML via snippet; abstract page [P] confirms the four levels |
| RGB (arXiv 2309.01431) names four abilities for RAG: noise robustness, **negative rejection** (refuse when the retrieved documents cannot answer), information integration, counterfactual robustness; LLMs "still struggle significantly in terms of negative rejection". A 2026 study on the same benchmark with knowledge-graph prompts found rejection rates all below 50%, and GPT-4o-mini under GraphRAG's default prompt at 12.7%, the lowest. | The four absent topics are a negative-rejection test, and the evidence says the model will answer anyway unless code decides first (note 03's verdict). Grade refusal as a measured **rejection rate** on the absent topics, 100% expected. | [P] arXiv 2309.01431 abstract; [V] arXiv 2603.05698 via snippet |
| UAEval4RAG defines six unanswerable categories (underspecified, false presupposition, nonsensical, modality-limited, safety-concerned, **out-of-database**) and grades a refusal two ways: an objective **unanswered ratio** (answered / ask-for-clarification / unanswered, LLM-labelled with a fixed definition) and a subjective **acceptable ratio** whose criteria vary by category. HERB, a 2026 enterprise deep-search benchmark, includes 699 unanswerable queries built by pairing real question templates with workflows that lack the evidence, and found the best system identified only 63% of them. | The four absent topics are out-of-database questions. Two other categories cost nothing to add: a **false-presupposition** question (asks about an attack the twin shows is benign) and an **underspecified** one. Grade them in code by the verdict the tool returned (`none`), with the refusal wording checked by regex as the Port's `DECLINES` pattern already does. | [V] arXiv 2412.12300, 2506.23139 via snippets |
| Google's "sufficient context" result (already in note 03): models answer rather than abstain when context is insufficient. | A prompt-only refusal will not hold; the twins and absent topics test the code path, with the prompt as the second lock. | [V] carried from note 03 |
| Hamel Husain's evals FAQ: label 100 to 200 examples per failure mode for an LLM judge; split them **train 10 to 20% (may appear in the prompt), dev 40 to 45% (iterate the judge), test 40 to 45% (read once)**; aim for 30 to 50 pass and 30 to 50 fail in each of dev and test; a purpose-built eval set "often grows to 100 or more", with coverage deciding the size; prefer binary checks to Likert scales; report a **pass-all rate** (an example passes only if every check passes) with drill-down per check. Overfitting "can happen even if you never put the dev examples directly in the prompt"; if test is much worse than dev, reserve a new untouched test set. | The split principle transfers directly to the re-ranker threshold: the borderline pairs used to set it are a **tuning set** and must not be the absent-topic or twin questions that grade it. The pass-all rate is exactly what `record["passed"]` computes today. | [P] hamel.dev evals FAQ |
| Hamel's decision-model post: tune a decision threshold on saved scores and binary labels with stratified cross-validation, choose thresholds on training folds and measure on the rest, reuse saved scores without new model calls, and report when no threshold meets the minimum rather than relaxing it. | The re-ranker score threshold is a decision threshold on saved scores. The artifacts already carry every score, so calibration is an offline computation over a labelled file, re-runnable without a model call. | [V] hamel.dev decision-model post via snippet |
| OpenAI's evaluation guide: include typical, edge and adversarial cases; use human expert labellers; set up continuous evaluation and "grow the eval set over time"; evaluations "should focus on tasks like pairwise comparisons, classification, or scoring against specific criteria instead of open-ended generation". LangSmith's concepts page: start with 5 to 10 curated examples per critical component, then 10 to 20 covering common scenarios and edge cases. | The small size is normal for a first set; what the sources require is coverage per component and growth per phase, which the ticket already plans. | [P] developers.openai.com evaluation best practices; [V] docs.langchain.com evaluation concepts via snippet |

**What this means for ticket 06.** Compose the phase-1 set by type with a provenance line per
question: graph lookups, text lookups, multi-hop traversals (gold = path IDs plus chunk IDs, at least
one through a high-degree node), mixed, the three twins, the four absent topics, and one or two
false-presupposition or underspecified questions. Keep the calibration set for the re-ranker threshold
as a separate file of labelled borderline pairs, drawn from the corpus but never from the questions
that grade refusal. At 25 to 40 questions the set is a regression gate for deterministic checks and a
coverage map, not a measurement of a rate; the sources are unanimous that rates need hundreds of
cases. Grow the set per phase by adding the new phase's types, not by padding the old ones.

### 3.3 LLM-as-judge reliability

| Fact | Consequence for this project | Status |
|---|---|---|
| MT-Bench ("Judging LLM-as-a-judge", 2023): strong judges such as GPT-4 reach "over 80% agreement" with humans, "the same level of agreement between humans", measured on 3,000 expert votes; the paper names **position, verbosity and self-enhancement** biases and limited reasoning, and proposes mitigations including swapping the order and judging twice. | The 80% figure is the ceiling claim everyone quotes; it is agreement on pairwise chat preference, not on faithfulness to a given context, and it does not transfer unmeasured. | [P] arXiv 2306.05685 abstract |
| "Reliability without Validity" (June 2026, 21 judges, 541,000 judgments): exact-match agreement overstates chance-corrected Cohen's kappa by **33 to 41 points** on MT-Bench for every judge; test-retest reliability above 0.95 coexists with position bias above 0.10 in two production judges (a judge can be perfectly consistent and consistently wrong); verbosity bias is small (below 0.011) under one pairwise rubric, with GPT-4o-mini the largest at 0.010; judge rankings shift by up to 14 places across benchmarks. | Report agreement with the author's labels as kappa, not raw agreement, because with a high pass rate an always-pass judge scores high on raw agreement. Repeat-run consistency is necessary, not sufficient. | [P] arXiv 2606.19544 abstract |
| "The Coin Flip Judge?" (April 2026): with **GPT-4o-mini and GPT-4.1-mini as judges**, 50 trials per question, pairwise preferences flipped 13.6% of the time on average, 28% of questions flipped more than 20%; GPT-4o-mini showed significant first-position bias (72% A-majority); cross-judge agreement 76% (kappa 0.51); equivalent prompt templates changed the majority verdict in 25% of cases; deterministic decoding "reduces but does not eliminate" inconsistency; **11 repeated trials** on average, 15 for high-variance questions, were needed for a majority vote to recover the 50-trial verdict with 95% probability. | This is the model this project already pays for. A single judged verdict from gpt-4o-mini is noise on a hard item. Either use a stronger judge, or repeat the judge call and take a majority, and in both cases treat the judge prompt as a versioned artefact because paraphrase alone moves verdicts. | [P] arXiv 2606.13685 abstract |
| "Rating Roulette" (2025): intra-rater agreement across three runs is below the 0.8 Krippendorff threshold for every judge tested; making decoding deterministic "hurts performance measured by agreement with human judgment"; three runs were enough to estimate self-reliability, more did not change it. "Judging the Judges" (2024): verbosity and self-enhancement effects are largely position bias driven by the quality gap; swapping order is the standard fix. A 2026 TMLR study: style bias (markdown over prose, 0.10 to 0.76) dominates position bias (at most 0.04); chain-of-thought and a combined-budget strategy gave the largest gains in human agreement. | Temperature 0 does not make a judge reliable, only repeatable. Ask the judge for a short reason before the verdict, and strip markdown before judging so style cannot leak into a faithfulness score. | [V] arXiv 2510.27106, 2406.07791, 2604.23178 via snippets |
| Self-preference bias (arXiv 2410.21819): GPT-4 shows significant preference for its own outputs, and LLM judges rate **lower-perplexity** text higher than humans do, whether or not the judge wrote it. G-Eval (2023) flagged "a bias towards the LLM-generated texts" and reached Spearman 0.514 with humans on summarisation using chain-of-thought plus form filling. | A gpt-4o-mini judge grading gpt-4o-mini answers is the self-preference case. A different model family as judge removes it; a stronger model of the same family only reduces it. | [P] arXiv 2410.21819 and 2303.16634 abstracts |
| OpenAI's evaluation guide: "use pairwise comparison or pass/fail for more reliability"; "use the most capable model to grade if you can", then "validate agreement against your human labels before optimizing for cost"; control for response length; "add reasoning and chain-of-thought"; ensure rubrics are "clear and detailed"; scale up only once the judge "consistently agrees with human annotations". The graders guide: build a grader eval from task prompts, expert answers and ground-truth grades; add edge cases as they are found; models can learn to game a grader. | A pass/fail faithfulness verdict per claim, a stronger judge than the system under test, and a small labelled set that grades the judge itself. The judge is a second system with its own eval. | [P] developers.openai.com evaluation best practices; [V] graders page via snippet |
| Hamel Husain: use the judge as a binary classifier, validate it against 100 to 200 human labels per failure mode split train/dev/test, measure true-positive and true-negative rate separately, and keep the test split for one read. Practitioner summaries of the same guide put the floor at about 60 labels below which "the confidence intervals are too wide to support a conclusion". | A faithfulness judge on a sample of 10 to 15 answers per run cannot be validated to this standard inside phase 1. It can still be run, as the ticket's "smoke alarm", if it is not the gate and its verdicts are stored for later labelling. | [P] hamel.dev evals FAQ; [V] aievals.co and ai-testing-handbook via snippets |
| RAGAS faithfulness: split the response into claims, check each against the retrieved context, score = supported / total; the DeepEval equivalent counts a claim truthful if it does not contradict the context (note 05, section 3.2). DeepEval's docs: inconsistent G-Eval scores between runs usually come from regenerating evaluation steps each run; fix the steps, add a rubric or `strict_mode` (binary 1 or 0); "use a stronger judge model, weaker models produce noisier scores". LangSmith: few-shot examples in the grader prompt "often improve performance"; its evaluator UI inserts human corrections as few-shot examples. | Write the judge prompt with fixed evaluation steps and a binary verdict per claim; never let the judge improvise its own rubric at run time; put the author's corrections back into the prompt as examples, which is the train split. | [P] docs.ragas.io faithfulness; [V] deepeval.com G-Eval and FAQ pages, docs.langchain.com evaluation concepts via snippets |
| Langfuse, DeepEval and LangSmith all store the judge's reason beside the score; BenchmarkQED runs six trials per query and averages; the 2606.19544 consistency protocol runs 3 to 5 replicates per item in both AB and BA orders. | Store the reason with every verdict; a verdict without a reason cannot be audited by the author later. | [P] BenchmarkQED blog; [P] 2606.19544 abstract |

**What this means for ticket 06.** The sources agree on the mechanics and disagree only on how much
to trust the result: binary verdict per claim, fixed evaluation steps, a reason before the verdict,
order and style controls, a stronger judge from a different family than gpt-4o-mini, repeated trials
with a majority vote, and the judge prompt hashed into the version fingerprint. They also agree that a
judge is validated against human labels, and the numbers for that (60 at the very least, 100 to 200
per failure mode) are out of reach for phase 1. So the judged layer is a sample whose verdicts and
reasons are kept for the author to label over time, and the gate stays with the deterministic checks.
Specific to a faithfulness judge on a small sample: the per-claim pass/fail structure means one answer
yields several labelled outcomes, which is the cheapest way to grow the labelled set.

### 3.4 Langfuse versus file-based eval results

| Fact | Consequence for this project | Status |
|---|---|---|
| Langfuse (version 4 server generally available; Cloud v3 deprecated at the **16 November 2026** cutover) stores traces with typed observations (`chain`, `retriever`, `tool`, `agent`, generations, spans), **datasets** of items (`input`, `expectedOutput`, `metadata`, `sourceTraceId`), **experiment runs** (`DatasetRun` with run-level `metadata`, one `DatasetRunItem` per item linking to a trace), and **scores** (numeric, categorical or boolean, attached to a trace, an observation or a run). Task-level evaluators return an `Evaluation` that becomes a score; run-level evaluators attach aggregate scores to the run. **"Each dataset item appears at most once per experiment. Repetitions are not yet supported."** Experiments on local data, without a hosted dataset, appear under Experiments with Langfuse v4. Runs are read back through the Experiments API; there is no public REST endpoint for creating runs. | The project's three runs per question map onto three experiment runs, or onto local-data experiments, not onto one run. `prompt_version`, commit and mode go in run metadata. The per-check verdicts become boolean scores. | [P] langfuse.com experiments data model; [V] compatibility page via snippet |
| Python SDK v5 (OpenTelemetry-based since v3) requires **`langchain-core>=1`**, Python 3.11 or later, and Langfuse Cloud or self-hosted v4.59.0 or later. The LangChain integration is a `CallbackHandler` from `langfuse.langchain`, passed as `config={"callbacks": [handler]}` to `invoke`; `create_agent` and LangGraph use the same handler; the handler captures LLM calls, tools and retrievers. Short scripts must call `get_client().shutdown()` or `flush()` before exit. Trace ID, session ID, user ID and tags are set through `langfuse_`-prefixed metadata or `propagate_attributes`. | Compatible with the pinned stack (Python 3.12, `langchain-core` 1.4.0, `langchain` 1.3.1). One handler on the agent's `invoke` traces the whole conversation including the knowledge-base tools; the eval runner would seed the trace ID from the question ID and run number so a trace is findable from the JSON record. | [P] langfuse.com LangChain integration page; [V] v4 to v5 upgrade page via snippet |
| Self-hosting: MIT licence for all core features since 4 June 2025; the Docker Compose stack runs Langfuse Web, Langfuse Worker, PostgreSQL, ClickHouse, Redis or Valkey and MinIO (S3-compatible blob store), with the UI on port 3000 and MinIO on 9090; the docs recommend **at least 4 cores and 16 GiB** and say the Compose setup "lacks high-availability, scaling capabilities, and backup functionality". ClickHouse acquired Langfuse in January 2026; the product "stays open source and self-hostable". Enterprise-only features are governance (SCIM, audit logs, project RBAC, retention policies, server-side ingestion masking). | Self-hosting is a six-container stack on the author's Intel Mac beside the project's own PostgreSQL, not a second table in it. That is a real operational cost for a single-user project. | [P] langfuse.com clarifications page, Docker Compose page; [V] self-hosting architecture page via snippet |
| Cloud Hobby tier: free, no card, **50,000 units per month** (a unit is any trace, observation or score), **30 days of data access**, 2 users, 1,000 ingestion requests per minute, 30 general API requests per minute, 100 Datasets API requests per minute, datasets, SDK experiments and custom scores all included. Data regions: EU, US, Japan, HIPAA. | An eval run of 40 questions times 3 runs with perhaps 15 observations and 10 scores each is roughly 3,000 units; the quota is not the constraint. The 30-day window is: the evidence record would expire from Langfuse, so the repo files stay the record of record. | [P] langfuse.com pricing page |
| Masking: the Python SDK runs a user function over trace data before export (`mask_otel_spans`, recommended, at export stage; legacy `mask` at attribute creation), so "sensitive values never leave your application"; it applies to spans from the LangChain handler. Export: datasets and traces export as CSV or JSON through UI, API and SDK, or on a schedule to blob storage. | Outbound data would be the question text, the synthetic log fields, the corpus chunks (ATT&CK text under its licence, the own policies), tool arguments and the model's answers. All synthetic, none secret, but it crosses the server boundary the security rules name. Export means no lock-in of the data; the UI and comparison views are what would be lost on leaving. | [V] langfuse.com masking and PII pages via snippets; [P] export fact from the clarifications page |
| CI gating: `langfuse/experiment-action` runs an experiment script in GitHub Actions and fails the job when the script raises `RegressionError`; it posts a PR comment with per-run scores and a link to the comparison view. Experiments are plain SDK scripts. | The project's `run.py` already prints "Target met: yes/no"; a non-zero exit on a missed target is one line and needs no platform. | [P] clarifications page; [V] CI/CD page via snippet |
| What the file record has today (from `run.py`): one JSON per run with every answer, tool call, check verdict and earlier turn; a `summary.md` line per run with prompt version, commit, mode, counts, overall and security rates and target met; `--rescore` re-grades saved answers without a model call; key values redacted before writing; everything git-tracked and reviewable in a diff. What it lacks: a trace tree (which chunks each tool call returned and at what score, unless the record is extended to save artifacts), side-by-side comparison of two runs, per-question history across runs, a place to annotate a verdict, charts over time. | Saving the per-tool artifacts into the JSON record closes the biggest gap in code and also makes retrieval re-scorable. The remaining gaps are views, not data. | read of `run.py`; design consequence |

**What this means for ticket 06.** Langfuse would add a trace view, run comparison and annotation
on top of data the project can already write to files, at the cost of either six containers on the
author's machine or an outbound stream of synthetic-but-boundary-crossing data to a 30-day-retention
free tier, plus a second record that is not in git. Nothing in the eval design depends on it: the
checks are code, the record is a file, the gate is an exit code. The ticket's leaning (an optional
trace sink behind a switch, files as the evidence) is consistent with what the sources show, and the
switch would be one `CallbackHandler` in the one function that builds the agent, which is the seam the
architecture rules already require. AUD-036 stays a registered option, not a dependency.

## 4. Fit against the existing runner

| Existing piece (`scoring.py`, `run.py`) | What the findings ask of it |
|---|---|
| `KINDS = ("has", "regex", "not", "tool", "report")`; `passes()` dispatches on exactly one key | New deterministic kinds: `retrieval` (gold chunk or record IDs, stage `fused` or `reranked`, `k`, all-or-nothing), `cites` (gold IDs among the resolved citations of the answer), `verdict` (expected `none` / `weak` / `found` from the tool artifact), `playbook` (05 decision 11, steps that must have run). A model-graded `judge` kind is the one kind that is not pure code; it must be marked so `score()` can skip it under `--rescore` and so `tests/test_eval_scoring.py` keeps the grader unit-tested. |
| `Answer(text, tools, report)`; `answer_of()` keeps only `(name, args)` per tool call | Add the per-tool **artifact** (chunk IDs, every recorded score, the verdict, the record IDs the walk returned) to `Answer` and to the saved record. This is where the retrieval kinds read from (3.1), and it is what makes `--rescore` work for retrieval without a model. `run.py` already reads `use.result` for the IP lookups; artifacts are the same path with a structured payload (note 05, `content_and_artifact`). |
| `prompt_version()` hashes model, prompts, report schema, tool descriptions, policy and report order | Extend the fingerprint with the judge prompt and judge model (3.3), the embedding and re-ranker model names, the chunking config, and a corpus or `truth.json` version (3.1), or keep a second `kb_version` beside it. Any of these changes the meaning of a result. `git_commit()`'s dirty list needs the new paths. |
| `--runs` default 3; `summarize()` gives overall, security, by category, by question | Retrieval checks are deterministic (3.1) and need one run; agent checks keep three; judge calls need their own repeat count and majority vote (3.3). `summarize()` gains per-layer rates (retrieval, citation, refusal, judged) and a Wilson interval beside each rate. The by-question `x/3` string is already the right unit for a small set. |
| `TARGET_OVERALL = 0.90`, `TARGET_SECURITY = 1.00`; `met` computed in `save()` | Add a retrieval floor stated per question (every question's recall@20 is 1.0) and a refusal target (100% of absent topics refused, 100% of twins benign) alongside, and keep `security` at 100%. The gate stays "every must-pass check passed", which is what `record["passed"]` already means. |
| `summary.md` table: started, version, commit, questions x runs, overall, security, target met, note | Add columns for the new layers, or a second table, so the trend per layer is visible without opening the JSON. The Neo4j harness's one-row-per-run JSONL trend is the same idea. |
| `--mode api` runs the same questions through the HTTP API | Unchanged for the agent layer. The retrieval layer calls `search_corpus` and the graph walk directly (note 03, section 6), so it needs a `--layer retrieval` path or a small sibling runner that imports `scoring.py`; it must not go through the agent. |
| `questions.json` has `id`, `category`, `turns`, `checks`, shared `patterns` | Add a `split` field (`test` by default; `tune` for the borderline pairs that calibrate the re-ranker threshold), a `gold` block carrying chunk IDs, record IDs and the path for multi-hop questions, and a `type` tag (graph lookup, text lookup, multi-hop, mixed, twin, absent, presupposition). `tests/test_eval_questions.py` already checks gold values against ground truth; it extends to `truth.json` IDs. |
| Memory per run is a temporary SQLite file; the AbuseIPDB key is removed before the first question | Unchanged. The same discipline applies to any Langfuse key: never loaded unless the switch is on, never written to a result. |

## 5. Recommendations for the grilling

Recommendations, not decisions; the author rules. Where a number appears, its origin is stated.

1. Score the text layer per question with recall@20 (all gold chunk IDs in the fused list, all-or-nothing), all-gold@5 after re-ranking, and MRR of the first gold chunk; drop NDCG (3.1; RAGAS ID-based formulas, multi-hop FSR papers; k = 20 and 5 borrowed from note 03's pipeline).
2. Score the graph layer as set recall and set precision of record IDs returned by the walk against the gold radius, with the gold path written by the generator (3.1; KGQA and GTSQA practice; Neo4j's recall@k of entity IDs).
3. State the retrieval floor per question, not as a rate: recall@20 = 1.0 on every question is the gate; all-gold@5 and MRR are reported with a target of 0.9 until the re-ranker comparison runs (3.1; the 0.9 is borrowed from Neo4j's `--min-score 0.9` example, the "per question" rule is derived from the Wilson intervals).
4. Run retrieval checks once per build and re-score them from saved artifacts; keep three runs for the agent (3.1; derived from the deterministic pipeline).
5. Print a Wilson 95% interval beside every rate in the summary so the 90% figure is read as "about 0.77 to 0.96" at n = 40 (3.1; derived).
6. Compose phase 1 by type with a provenance line per question: graph lookup, text lookup, multi-hop (at least one through a high-degree node), mixed, three twins, four absent topics, one false-presupposition, one underspecified; proportions roughly a third lookups, a third multi-hop and mixed, a third twins, absent and presupposition (3.2; the thirds are derived from RAGAS 50/25/25 and HybridRAG-Bench's spread, not borrowed from any one source).
7. Keep the re-ranker calibration set as a separate labelled file of borderline pairs, flagged `tune`, never overlapping the `test` questions that grade refusal; calibrate offline on saved scores (3.2; Hamel's split and decision-threshold practice).
8. Grade refusal as a rejection rate on the absent topics and a benign rate on the twins, both expected at 100%, read from the tool's verdict in code with the wording checked by regex (3.2; RGB, UAEval4RAG, the Port's `DECLINES` pattern).
9. Make the judge a binary per-claim faithfulness verdict with fixed evaluation steps, a reason before the verdict, markdown stripped, a stronger model from a different family than gpt-4o-mini, three trials with majority vote, and the judge prompt and model hashed into the version (3.3; Coin Flip Judge's 11 trials is for a 95% recovery of a 50-trial reference and is more than this project needs; three is borrowed from Rating Roulette's finding that three estimated self-reliability as well as ten).
10. Keep the judged layer a sample of about ten answers per run and not the gate; store every verdict and reason so the author can label them over time toward the 60-to-100 labels a judge validation needs (3.3; Hamel's numbers, borrowed; the ten is derived from cost and from the sample being a smoke alarm).
11. Report judge-versus-author agreement as Cohen's kappa once labels exist, never as raw agreement (3.3; Reliability without Validity).
12. Save the per-tool artifacts in the JSON record and extend `prompt_version` (or add `kb_version`) with the judge prompt, judge model, embedding and re-ranker model names, chunking config and corpus version (section 4; derived from `run.py`).
13. Keep the file-based record as the evidence; register Langfuse as an optional trace sink behind a switch in the one agent-building function, off by default, with no key loaded unless on; revisit after phase 1 if the author wants run comparison views (3.4; the project's own rules and the Langfuse facts).
14. Add a "break the gate on purpose" test: swap one gold ID for an absent one and assert the retrieval check fails (3.1; Neo4j's harness).

## 6. Evidence gaps

- The GraphRAG-Bench retrieval metrics (evidence recall, context relevance) and HybridRAG-Bench's
  question proportions were read through arXiv HTML snippets, not opened in full.
- DeepEval's pages (contextual recall and precision, G-Eval, FAQ) were read through snippets only; the
  component mapping (precision tests the re-ranker, recall the embedder) is their claim, unverified on
  the page.
- RGB's rejection-rate measure comes from a 2026 secondary paper, not from the RGB paper's body.
- The Coin Flip Judge study uses two OpenAI judges only and its authors say cross-provider
  replication is pending; its 11-trial figure is specific to its tasks.
- No source measures judge reliability on a faithfulness-to-context task with a sample of ten;
  the recommendation to repeat three times is a transfer from pairwise and rating tasks.
- Langfuse's Python 3.11 minimum and the 16 November 2026 Cloud cutover were read from snippets of the
  compatibility and upgrade pages; the LangChain page opened did not state the Python version.
- The Langfuse self-hosting architecture page (six services) was read through a snippet; the Docker
  Compose page opened names only web, worker and MinIO explicitly.
- No source gives a retrieval floor for a corpus of about 40 documents; the per-question floor is
  this note's own derivation from the deterministic pipeline and the interval arithmetic.
- The Wilson intervals were computed by hand for this note and should be re-computed in code when
  `summarize()` is extended.

## Sources

Gap 1, retrieval metrics and floor:
- [P] RAGAS context recall: https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_recall/
- [P] RAGAS context precision: https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_precision/
- [P] Neo4j agent-memory evaluation: https://neo4j.com/labs/agent-memory/how-to/evaluation/
- [P] Microsoft Research, BenchmarkQED: https://www.microsoft.com/en-us/research/blog/benchmarkqed-automated-benchmarking-of-rag-systems/
- [P] GraphRAG-Bench abstract (2506.05690): https://arxiv.org/abs/2506.05690
- [V] DeepEval RAG evaluation guide: https://deepeval.com/guides/guides-rag-evaluation
- [V] DeepEval contextual recall: https://deepeval.com/docs/metrics-contextual-recall
- [V] Neo4j, vector RAG vs GraphRAG: https://neo4j.com/blog/agentic-ai/vector-rag-vs-graphrag/
- [V] GraphRAG-Bench HTML (retrieval metrics): https://arxiv.org/html/2506.05690v1
- [V] Unified retrieval and generation over graphs (Hit, Recall, Precision): https://arxiv.org/html/2510.07484v2
- [V] GTSQA, ground-truth subgraphs: https://arxiv.org/html/2511.04473v2
- [V] Answer path and grounding instruction (precision versus recall): https://arxiv.org/html/2609.10237v1
- [V] Contrastive evidence exploration (FSR@10): https://arxiv.org/html/2609.07050v1
- [V] Budget-constrained multi-hop RAG diagnostic (all-gold@5): https://arxiv.org/html/2607.00725v1
- [V] Fact-grounding gap in multi-hop QA: https://arxiv.org/html/2609.17043v1
- [V] Pinecone, evaluation measures in IR: https://www.pinecone.io/learn/offline-evaluation/
- [V] Weaviate, retrieval evaluation metrics: https://weaviate.io/blog/retrieval-evaluation-metrics
- [V] Cohere, RCP-nDCG: https://cohere.com/blog/rcp-ndcg
- [V] Eval-driven development (intervals, Wilson): https://www.tmls.nyc/research/eval-driven-development
- [V] Sample size for LLM evals: https://ai-tldr.dev/learn/evaluation-safety/evaluation-basics/llm-eval-sample-size/

Gap 2, gold-set construction:
- [P] RAGAS test-data generation for RAG: https://docs.ragas.io/en/stable/concepts/test_data_generation/rag/
- [P] RGB abstract (2309.01431): https://arxiv.org/abs/2309.01431
- [P] Hamel Husain, AI evals FAQ: https://hamel.dev/blog/posts/evals-faq/
- [P] OpenAI, evaluation best practices: https://developers.openai.com/api/docs/guides/evaluation-best-practices
- [V] RAGAS 0.1.21 test-set generation (old distribution): https://docs.ragas.io/en/v0.1.21/getstarted/testset_generation.html
- [V] HybridRAG-Bench: https://arxiv.org/html/2602.10210v1
- [V] UAEval4RAG: https://arxiv.org/html/2412.12300v1
- [V] HERB, enterprise deep search with unanswerable queries: https://arxiv.org/html/2506.23139
- [V] Robust RAG on knowledge graphs, RGB rejection rates: https://arxiv.org/html/2603.05698v2
- [V] Hamel Husain, decision models for evals: https://hamel.dev/blog/posts/decision-model-evals/index.html
- [V] LangSmith evaluation concepts: https://docs.langchain.com/langsmith/evaluation-concepts

Gap 3, judge reliability:
- [P] Judging LLM-as-a-judge, MT-Bench (2306.05685): https://arxiv.org/abs/2306.05685
- [P] G-Eval (2303.16634): https://arxiv.org/abs/2303.16634
- [P] Reliability without Validity (2606.19544): https://arxiv.org/abs/2606.19544
- [P] The Coin Flip Judge (2606.13685): https://arxiv.org/abs/2606.13685
- [P] Self-preference bias (2410.21819): https://arxiv.org/abs/2410.21819
- [P] OpenAI, evaluation best practices (judge section): https://developers.openai.com/api/docs/guides/evaluation-best-practices
- [P] RAGAS faithfulness: https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/
- [P] Hamel Husain, AI evals FAQ (judge validation): https://hamel.dev/blog/posts/evals-faq/
- [V] Rating Roulette: https://arxiv.org/html/2510.27106v1
- [V] Judging the Judges, position bias: https://arxiv.org/html/2406.07791v2
- [V] Bias mitigation strategies, TMLR 2026: https://arxiv.org/pdf/2604.23178v2
- [V] OpenAI graders guide: https://developers.openai.com/api/docs/guides/graders
- [V] DeepEval G-Eval: https://deepeval.com/docs/metrics-llm-evals
- [V] DeepEval FAQ: https://deepeval.com/docs/faq
- [V] LangSmith, define an LLM-as-a-judge evaluator: https://docs.langchain.com/langsmith/llm-as-judge
- [V] aievals.co, calibrating a judge: https://www.aievals.co/learn/llm-as-judge/calibration-to-humans

Gap 4, Langfuse versus files:
- [P] Langfuse clarifications: https://langfuse.com/resources/engineering/clarifications
- [P] Langfuse pricing: https://langfuse.com/pricing
- [P] Langfuse LangChain integration: https://langfuse.com/integrations/frameworks/langchain
- [P] Langfuse experiments data model: https://langfuse.com/docs/evaluation/experiments/data-model
- [P] Langfuse Docker Compose: https://langfuse.com/self-hosting/deployment/docker-compose
- [V] Langfuse versions and compatibility: https://langfuse.com/docs/compatibility
- [V] Langfuse Python SDK v4 to v5: https://langfuse.com/docs/observability/sdk/upgrade-path/python-v4-to-v5
- [V] Langfuse self-hosting overview: https://langfuse.com/self-hosting
- [V] Langfuse masking: https://langfuse.com/docs/observability/features/masking
- [V] Langfuse experiments in CI/CD: https://langfuse.com/docs/evaluation/experiments/experiments-ci-cd
- [V] Langfuse self-hosted pricing: https://langfuse.com/pricing-self-host
- Project: `backend/evals/scoring.py`, `backend/evals/run.py`, `backend/evals/questions.json`
