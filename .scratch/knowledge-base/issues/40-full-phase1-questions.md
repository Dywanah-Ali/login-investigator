# 40: The full phase 1 question set

Type: build
Status: ready-for-agent
Blocked by: 29, 55
Phase: 1
Model: standard (Opus 5.5 or Sol 6.1)

## T52 scope handoff — 2 November 2026

Author confirmed reliable login investigation as the sole phase-0/1 objective, with bounded
account-impact and directly connected activity context. Standalone full inventory, exhaustive
permission-path presentation and reverse asset exposure are deferred. This supersedes broader
product-scope wording below. See [spec Current scope ruling](../spec.md#current-scope-ruling--t52-2-november-2026).
Detailed criteria below carry the approved T52 boundaries. Open design decisions remain
explicit; this reconciliation does not release T52 or authorise implementation.
Existing source code, questions, gold and thresholds are not changed or waived by this note.

## What to build

The knowledge-base question file grows from the first handful to about 30 questions, weighted to
say-no and mixed questions, with lookups as the control group. Every question carries a provenance
line and gold IDs or an expected verdict.

## Decisions implemented

- T06 d3 (about 30 questions: about 10 say-no, namely three twins, four absent topics, two
  false-presupposition traps and one underspecified; about 12 mixed and multi-hop, at least two
  through a busy node; about 8 graph and text lookups as the control group; B3 asked about the
  laptop change directly).
- [review ruling 2] the gold items choose the checks.
- User stories 14, 71.

## Acceptance criteria

- [ ] Review K03's obsolete address-reuse provenance under B-143/B-145. Obtain the author's
      ruling on the exact correction before editing the frozen exam; preserve its clean
      account-control purpose and gold. T51 is resolved and does not own this work.

- [ ] Map the expanded cases to the sole login-investigation objective and E01–E10.
      Include controlled missing coverage, empty results, failed checks and omissions,
      partial/competing explanations and potential-access overclaims. Do not add telemetry
      merely to resolve every case. Record overlap with existing cases before adding new ones.
- [ ] Preserve original questions/gold/gates. Propose any necessary revision individually
      for author approval before changing them. Keep exact graph tests even where the
      product answer presents bounded context. K04's missing MFA evidence stays a failure.
      Apply the already-approved T45 8 November candidate-stage revision: measure each actual
      pipeline path separately; retain corpus-only fused top 20 as a diagnostic. This is the
      explicit exception to the earlier candidate-stage rule, not permission for other changes.
- [ ] Test bounded guidance against approved sources and the uncertainty in each case;
      distinguish external analyst checks from available app actions and performed checks.
- [ ] The 50-person/30-day dataset target remains approved but unbuilt;
      generator/data ownership is now assigned to T55 by the author. T55 supplies accepted
      data before this ticket uses it. Small uncertainty fixtures do not replace that
      target or establish a baseline.

- [ ] Before any build work starts, the builder tells the author this ticket's `Model:` line and
      asks the author to set that model. The build starts only after the author confirms, and a
      dated line under Comments records the model used.
- [ ] About 30 questions with the T06 d3 mix; the actual counts are recorded.
- [ ] B3's question asks about the laptop change directly.
- [ ] Every question carries a provenance line and gold IDs or an expected verdict; ticket 21's test
      passes on the full file.
- [ ] No question overlaps the tuning file.
- [ ] The full file runs through the eval; the results are recorded per question, and every failure
      is fixed or logged in the bug log with its cause.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged.

## Comments

- 2026-11-08 — Approved T45 split retains this ticket's expanded application coverage and
  T55 dependency. Consume T57–T60/T25/T26 stage and scope records through T29. Include the
  approved role-example/classification and supporting/competing evidence behaviours in existing
  coverage mapping; first identify overlap. No new campaign, gold rewrite or threshold change.

- 2026-10-26, author's S4 ruling: S4 is intentionally unresolved. When evaluating it, accept that the unusual successful Russian-source sign-in warrants investigation, while authorisation, compromise, Olivia's physical location, who completed MFA and the attack mechanism remain unknown. Do not demand confirmed compromise or a named MFA attack; do not treat this evidence limit as a fifth absent topic or a new retrieval verdict. See the spec and T12.

- 2026-11-02 — T52 closure assigns B-143's remaining K03 provenance review here. T51
  changed the generated answer key only and explicitly left the exam untouched. Propose
  removal/rewording of K03's obsolete address-reuse sentence for author approval before
  editing the frozen question file; preserve the clean-control intent and existing gold.
  B-145 records the corrected owner. This does not waive any retrieval gate.
