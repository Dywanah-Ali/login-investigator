# 29: The knowledge-base exam in the eval runner

Type: build
Status: ready-for-agent
Blocked by: 21, 28, 44
Phase: 0 (its gate)
Model: strongest (Fable 5.1 or Astra)

## What to build

The eval runner runs the knowledge-base question file beside the frozen Port file, with its own
gates and its own summary lines, never blended. Retrieval and answers are measured separately. The
first questions pass end to end. This is phase 0's gate, and every phase 1 ticket waits for it.

## Decisions implemented

- T06 d8 (two exams, one scorer; new deterministic check kinds `retrieval`, `cites`, `verdict`,
  `playbook`; a `judge` kind marked so rescoring skips it; artifacts saved; the wider fingerprint;
  the dirty-path list gains the knowledge-base paths), T06 d1 (retrieval gate, both checks), T06 d2
  (graph gate), T06 d5 (answer gate through the one resolver; say-no graded from the artifacts at
  100%), T06 d7 (playbook and canary gates at 100%, canaries flagged security), T06 hand-offs
  (Wilson intervals).
- [review ruling 2] the gold items choose the checks.
- Map, phase 0 gate. Author's ruling of 25 October 2026 at the ticket cut: phase 1 waits for this
  ticket.
- User stories 71 to 76, 81, 82. Spec door 6.

## Acceptance criteria

- [ ] Carry E01–E10 into a coverage matrix linking case, collection/retrieval check,
      interpretation check and saved evidence. Fixed-evidence T54 results cannot substitute
      for application collection, tool execution, reopen or full-exam proof.
- [ ] For `investigate_alert`, distinguish collection/retrieval evidence, package assembly
      evidence and final model interpretation. Use T26's saved step inputs, outputs, evidence IDs
      and failure states to locate a miss at its stage. Component/package checks remain with T26;
      do not infer collection success from a plausible answer or a fixed-evidence comparison.
      Retain existing exam gold and thresholds; any proposed changes require author approval.
- [ ] Retain exact graph regressions and frozen Port/knowledge-base questions and gold. Any
      proposed scope-related exam revision requires an explicit author ruling before edits;
      narrowing product scope does not waive K04 or blend screening scores into acceptance.
- [ ] Distinguish label resolution/gold citation coverage from semantic claim support.
      T30 remains advisory; record attribution failures such as AUD-066 without assuming
      all are grader defects. Preserve failed, incomplete and repaired attempts.

- [ ] Before any build work starts, the builder tells the author this ticket's `Model:` line and
      asks the author to set that model. The build starts only after the author confirms, and a
      dated line under Comments records the model used.
- [ ] The knowledge-base file runs beside the Port file, with its own gates and summary lines.
- [ ] Check kinds `retrieval`, `cites`, `verdict` and `playbook` are deterministic; `judge` is marked
      so rescoring skips it. The judge itself is ticket 30.
- [ ] A runner test proves which checks each question's gold items select.
- [ ] Implement T45's author-approved 8 November acceptance paths separately: unchanged analyst
      question and the applicable same-case code-built baseline. Every gold passage must enter
      an actual admitted pool in its path and survive delivery, including chat's interpretation
      input on the application path. Record route/first-gold ranks, retained/delivered identities
      and execution settings. No cross-path pooling or gold-informed query hints. Retain raw
      corpus-only top 20 as a diagnostic, not an additional gate. Historical failures remain.
- [ ] Answer gate: every label resolves and every gold ID is cited, through ticket 27's resolver.
      Say-no questions are graded from the artifacts first, then the wording.
- [ ] Process gates: `playbook_status` on every threat question; a canary in a log field and one in a
      corpus paragraph are never obeyed, flagged `security`, at 100%.
- [ ] A test proves every deterministic check rescores from the saved run file with no model call.
- [ ] The fingerprint covers the embedder, re-ranker, chunking settings and corpus version; the
      dirty-path list covers the knowledge-base paths.
- [ ] The summary shows Wilson intervals computed in code.
- [ ] The first questions pass end to end on a real run; the Port's eval passes; both run files are
      kept as evidence.
- [ ] The map records phase 0's gate as passed, with the run files named.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged.

## Comments

- 2026-11-08 — Approved seven-slice handoff: T57/T58/T25 prove evidence capabilities,
  T26 package/baseline assembly, T59 worker behaviour, T60 application delivery/lifecycle and
  T28 report completion. This ticket retains phase-0 acceptance for both original analyst-question
  and applicable same-case baseline paths, classified separately through collection, assembly
  and interpretation. Consume actual candidate/delivery receipts and T26's shared procedure.
  T28 transitively blocks on T60; T44 still precedes this gate. No circular dependency on this
  ticket for earlier component completion and no duplicate paid campaign are introduced.
  Classifier quality, semantic applicability, prompt examples and injection resistance require
  existing evaluation evidence; fake-model plumbing tests do not establish them.

- 2026-11-08 — Author approved the explicit T45 candidate-stage gate revision, while preserving
  original questions/gold and answer/graph/security requirements. Both new paths need their own
  evidence; a successful package does not establish application answer quality. No duplicate
  full-suite/paid campaign mandate or live run is added. AUD-062 is still open.

- 2026-11-03 — Author approved `investigate_alert` as a thin coordinator with independently
  testable shared components and saved step-level evidence. T26 implements and tests the
  components/package; this ticket evaluates the application with collection, assembly and
  interpretation distinguishable. Documentation only; T54 scope and existing gates unchanged.

- 2026-11-02 — Author-approved ownership: T54 builds the isolated model/architecture
  comparison runner and reusable recording module. T29 retains the application's Port
  and knowledge-base acceptance exams and their existing gates. Reuse suitable recording
  utilities without blending experimental scores into acceptance rates. No dependency
  on T54 is added to the local exam; T31 handles its hosted integration after both exist.
