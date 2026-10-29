# 45: Retrieval for compound questions, in chat and in the package

Type: research, then grilling
Status: ready-for-agent
Blocked by: none
Blocks: 26, and the initiative's retrieval gate (AUD-062's closure)
Phase: 0
Model: strongest (Fable 5.1 or Astra)

Opened by the author's ruling of 29 October 2026, after T23. The retrieval-design work parked at
T23 is significant enough for its own ticket. This is a decision ticket: it produces rulings,
not code. Whatever it decides is built in a later ticket, or folded into T26 by ruling.

## Question

How does the knowledge base find every passage a compound question needs, such as K04 ("what
happened in S6, and what does it reach"), when the evidence sits in different documents?

The question has two paths, and the answer may differ for each:

1. **The chat path.** The analyst can ask anything; the app cannot force a style of question.
   The model reads the question and writes the search through `search_corpus(question, ...)`
   (spec, T05 d1). It may send one long search or several focused ones; nothing in code
   decides. T22 showed one long search losing K04's MFA register: the keyword leg returns
   nothing when every term must match, and the register falls to dense rank 115.
2. **The package path.** `investigate_alert` builds its clearing and aggravating searches in code
   from the finding's record, never from the chat (spec, T05 R5). Here the search templates
   decide coverage, and text cannot steer them. That protection stays.

## What to decide

1. **What K04's gate measures.** The analyst's raw question, the package's code-built searches,
   or both, each as its own check. The original questions and gold stay unchanged; a change to
   what a gate measures is a spec change and needs the author's ruling.
2. **The chat path.** Where splitting a compound question belongs, if anywhere: in the model's
   instructions or a focused skill, in `search_corpus` itself as a guard against a long
   question, or nowhere until the stronger-model comparison (AUD-031, P-03). The architecture is
   not shaped around the current model's weaknesses (P-03).
3. **The package path.** Which searches T26 must build from a finding so that every playbook
   step's evidence is covered, and how that coverage is tested.
4. **Keeping what was found.** Whether evidence already retrieved for one need can be lost when
   results are merged or cut to five, and what protects it. T22's experiments showed both risks.
5. **The keyword leg.** Whether all-terms-must-match keyword search is right for long questions,
   or whether T41's BM25 comparison settles it.

## Inputs (research already done, none of it adopted)

- [Retrieval recovery research](../research/22-investigation-retrieval-recovery.md):
  decomposition, sufficiency, omitted needs, bounded recovery, preserved access and scope.
- [Fixed-budget experiment](../research/22-retrieval-experiment-results.md): focused queries
  keep both K04 passages; a broad route with equal fusion drops the register to rank 25; a
  human-chosen retry restores it. Recovery used human knowledge of the gold.
- [Evidence checklist design and offline replay](../research/22-evidence-checklist-design.md):
  fair turns recover K04 from saved lists but fail in two of six route orders and under a
  five-passage cap.
- T22's focused-query probe (T22 ticket, follow-up exploration): human-written queries find
  the register at rank 7 or 2 and the runbook at 1.
- T23's live runs: the re-ranker keeps K04's runbook at rank 1; the register is never scored,
  because it is not among the fused 20 (AUD-062 note).
- AUD-062 (the gap), AUD-064 (kept-5 check and calibration), B-098, P-03 in `PRINCIPLES.md`.

## Acceptance criteria

- [ ] Before any work starts, the agent tells the author this ticket's `Model:` line and waits
      for the author to confirm the model is set; a dated comment records it.
- [ ] Research uses the Perplexity and Keenable tools and checks material claims against primary
      sources; findings saved as a research note in `../research/`.
- [ ] Each of the five decisions above has a ruling recorded under the Answer, or an explicit
      deferral with its reason and owner ticket.
- [ ] Any change to what a gate measures, or to the spec, is proposed first, ruled by the author,
      and recorded in the spec's decisions log.
- [ ] T26's criteria are updated to match the package-path ruling before T26 is built.
- [ ] AUD-062 is updated with the rulings. It closes only on the evidence its own entry demands.

## Comments

- 2026-10-29 — Author: open this as its own ticket, a decision ticket that blocks T26. T24 and
  T25 proceed meanwhile. The chat path matters because the analyst can ask anything; a user
  guide cannot guarantee how questions are asked.
