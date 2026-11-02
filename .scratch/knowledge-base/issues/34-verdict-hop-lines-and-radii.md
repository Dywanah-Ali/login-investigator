# 34: The verdict, hop lines and radii tiles

Type: build
Status: ready-for-agent
Blocked by: 26, 33
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

The answer presents an evidence-qualified assessment with bounded impact context. Supporting
paths remain one hop per line with citation tags. The analyst owns the verdict. The earlier
three-full-radius tile design needs an author-reviewed revision before UI code; it must not
imply exhaustive inventory or turn a partial explanation into whole-case clearance.

## Decisions implemented

T07 references below preserve the original design provenance. T52 narrows their scope;
the reconciled acceptance criteria govern the new screen agreement.

- T07 d2 (one hop per line), T07 d3 (radii as counts first, lists in the panel), T07 d9 (the
  five-level visual hierarchy: the verdict and "Cleared by" as the one coloured surface, red, green
  or amber; amber for "Not checked" and unverified; bordered boxes without colour for tiles and
  path; citation tags small, monospace, calm link blue; plain prose; no new colours).
- API contract change 2 (`radii` on reopen, present only where the investigation tool ran).
- User stories 18 to 22, 24, 26, 29.

## Acceptance criteria

- [ ] Before any build work starts, the builder tells the author this ticket's `Model:` line and
      asks the author to set that model. The build starts only after the author confirms, and a
      dated line under Comments records the model used.
- [ ] Agree the bounded-context screen and API projection with the author before UI code.
      Review the earlier `radii` draft explicitly. Counts/lists state selection, period and
      omissions; reopen projects saved artifacts without a fresh query. Update the contract first.
- [ ] Where the assessment shown comes from is fixed under this ticket's Answer, following ticket 27's
      answer-shape decision.
- [ ] Assessment wording follows P-02. Supporting/clearing evidence states what it explains
      and what remains unresolved. Preserve the visual hierarchy, with explicit incomplete
      and unverified states, in the author-approved screen revision.
- [ ] The path renders one hop per line, each with its tag.
- [ ] Bounded impact and involved-device context show supporting evidence and limits. Test
      selected subsets, truncation, absent role/context and partial clearing evidence.
      No full-inventory or exhaustive-path presentation is required.
- [ ] Tags are small, monospace, in the app's link blue; no new colours are added.
- [ ] The answer still renders with links and images switched off.
- [ ] Door 5 tests with the fake API cover each element.
- [ ] The author's screenshot review in light and dark mode settles the exact colours and is recorded
      as a dated line.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged.

## Comments
