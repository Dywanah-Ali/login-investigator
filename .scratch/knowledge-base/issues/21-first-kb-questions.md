# 21: The first knowledge-base questions

Type: build
Status: resolved
Blocked by: 16, 17, 19
Phase: 0
Model: standard (Opus 5.5 or Sol 6.1)

## What to build

The knowledge base's own question file, beside the frozen Port file, starts with a first handful of
questions, each carrying its gold IDs or its expected verdict. They are written and committed before
any search runs, so the exam cannot be fitted to the results.

## Decisions implemented

- Map, evaluation stance (the eval set exists before the first retrieval runs); spec build order
  item 8 (review finding R5).
- T06 d3 (question fields: `type`, `gold`, `split`, a provenance line), T06 d8 (two files, kept
  separate).
- [review ruling 2] the gold items choose the checks; a say-no question may carry no gold IDs but
  states its expected verdict.
- User story 71.

## Acceptance criteria

- [x] Before any build work starts, the builder tells the author this ticket's `Model:` line and
      asks the author to set that model. The build starts only after the author confirms, and a
      dated line under Comments records the model used.
- [x] The question file sits beside the Port's file, which stays unchanged.
- [x] Six to ten questions, covering at least one document lookup, one graph lookup, one mixed
      question on S6, one absent topic (verdict `none`, no gold IDs) and one twin.
- [x] Every question carries `type`, `split`, a provenance line, and gold IDs or an expected verdict.
- [x] A test proves every gold chunk ID exists in a fresh build, every gold record ID exists in the
      world's files, and every question has gold IDs or a verdict.
- [x] The file is committed before ticket 22's first search run; the commit order is the evidence.
- [x] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged.

## Comments

- 2026-10-26, author's S4 ruling: S4 is intentionally unresolved. When evaluating it, accept that the unusual successful Russian-source sign-in warrants investigation, while authorisation, compromise, Olivia's physical location, who completed MFA and the attack mechanism remain unknown. Do not demand confirmed compromise or a named MFA attack; do not treat this evidence limit as a fifth absent topic or a new retrieval verdict. See the spec and T12.
- 2026-10-29, Claude: stated the `Model:` line (standard: Opus 5.5 or Sol 6.1); the author
  confirmed the model is set. Built with Claude Opus 5.5.
- 2026-10-29, Claude: documentation lookup not needed. The work codes against no third-party
  library: the test uses the standard library and the project's own build and chunker.
- 2026-10-29, Claude: build complete; the author's two rulings below are pending.
  - **Shape.** `backend/evals/knowledge_base_questions.json` holds eight questions, K01 to K08, all
    `split: test`: two document lookups (K01 current password length, where the superseded 2024
    policy says 8; K02 the MFA exception register), one graph lookup (K03 hannah.porter's groups),
    one mixed question on S6 (K04 reach plus why MFA did not stop it), two absent topics (K05 data
    retention, K06 incident write-ups) and two twins (K07 B1 travel, K08 B3 laptop swap, asked
    directly). `gold` always has `chunks`, `records` and `paths`, empty where unused. The Port's
    `questions.json` is unchanged.
  - **Test.** `backend/tests/test_eval_knowledge_base_questions.py`, 7 tests at door 6: fields and
    something to check; the kinds the ticket names; absent topics carry `none` and no gold; every
    gold record and path step is a first-column ID of an `org/*.csv` table; K04 equals
    `truth.json` S6's radius and paths; each twin's gold chunks come from its clearing document;
    every gold chunk ID exists in a fresh PostgreSQL build of `default` with the fake embedder.
    Each gold chunk's text was also read from the chunker: each holds the evidence its question
    needs (K04's runbook chunk ends at step 4, "Check MFA for each success").
  - **Evidence.** New file 7 passed; full backend suite 629 passed (622 before, plus 7); pyright
    0 errors; frontend 149 passed; two-axis review triaged in
    [the review](../reviews/21-code-review-2026-10-29.md). Port eval not run: no agent, tool or
    prompt change.
  - **For the author to rule.**
    1. *K04 carries two of S6's three expected documents.* `run-compromised-account-response` is
       left out because the question asks about reach and MFA, not next steps, and the answer gate
       demands every gold ID be cited. The alternative adds it as a third gold chunk.
    2. *Field names beyond T06 d3.* `conclusion: "benign"` on twins keeps the investigator's
       conclusion apart from the search tool's `verdict` (`none`, `weak`, `found`); `turns` and the
       top-level `note` copy the Port file's shape.
- 2026-10-29, Claude: the author ruled both points and the ticket is resolved. Questions committed
  in `aa07926`, before any search run; T22 has not started.
  1. K04 keeps two gold documents. The next-steps runbook (`run-compromised-account-response`)
     belongs to a phase 1 question that asks what to do next.
  2. `conclusion: "benign"` is accepted for twins, apart from the search tool's `verdict`. Recorded
     in the spec's decisions log.
