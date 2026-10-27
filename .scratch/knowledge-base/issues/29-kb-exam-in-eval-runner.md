# 29: The knowledge-base exam in the eval runner

Type: build
Status: ready-for-agent
Blocked by: 21, 28
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

- [ ] The knowledge-base file runs beside the Port file, with its own gates and summary lines.
- [ ] Check kinds `retrieval`, `cites`, `verdict` and `playbook` are deterministic; `judge` is marked
      so rescoring skips it. The judge itself is ticket 30.
- [ ] A runner test proves which checks each question's gold items select.
- [ ] Retrieval gate: every gold chunk ID among the 20 fused candidates and among the chunks the
      model received; the first-gold rank recorded.
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
