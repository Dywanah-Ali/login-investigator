# 06: The eval set for a graph-plus-text system

Type: research, then grilling (retyped 23 October 2026; see the first comment)
Status: claimed
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

- [ ] Layers, question types, thresholds and grader decided.
- [ ] Runner integration decided.
- [ ] Decision recorded here under `## Answer`.

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
