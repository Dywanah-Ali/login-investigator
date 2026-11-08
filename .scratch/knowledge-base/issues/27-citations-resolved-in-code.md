# 27: Citations resolved in code

Type: build
Status: ready-for-agent
Blocked by: 24, 49
Phase: 0
Model: strongest (Fable 5.1 or Astra)

## What to build

Every factual claim in the agent's answer carries a short tag, L1, G1 or D1, and code checks each tag
against the investigation's saved artifacts after the model answers. A tag that points at nothing
sends the model back once with a correction; a second failure marks the answer unverified. One
resolver does this, and the same resolver later feeds the evidence panel and the eval's `cites`
check, so screen and exam cannot disagree.

## Decisions implemented

- T05 d6 and T07 d6 (short per-answer labels L, G and D, numbered per answer, resolved in code),
  T05 R4 (the per-turn light gate), T05 d9 (the after-model hook part: citations resolve; a question
  that named a finding ID is not answered uncited; one jump back, counted in one state field).
- Spec "One resolver" (T07 and T08 hand-offs).
- T05 conditions and AUD-041: structured answer (text plus a list of labels) or parsed prose, decided
  here.
- User stories 25, 27. Spec door 3.

## Acceptance criteria

- [ ] Resolving a label proves reference validity only. Do not label claim support as
      verified by this check. Preserve original referenced evidence for T33/T37 and reopen;
      later rebuilds must not substitute fresh evidence behind an existing citation.

- [ ] Before any build work starts, the builder tells the author this ticket's `Model:` line and
      asks the author to set that model. The build starts only after the author confirms, and a
      dated line under Comments records the model used.
- [ ] Structured answer or parsed prose is decided; the decision and its reason are recorded under
      this ticket's Answer and in AUD-041.
- [ ] Labels L, G and D are numbered per answer and resolved against the investigation's artifacts
      after the model answers.
- [ ] An unresolved label sends the model back once with a correction, counted in one state field;
      a second failure keeps the answer and marks it unverified.
- [ ] A question that named a finding ID is never answered uncited.
- [ ] One resolver function returns the resolved records for a turn; it is the function tickets 29,
      33 and 37 call.
- [ ] Agent tests use the fake model; the Port's eval passes.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged.

## Comments

- 2026-11-08 — Approved T45 ticket split: this ticket remains the sole citation resolver owner.
  Align evidence adapters with T57's shared source-bound contract; T60 integrates this resolver
  against actual worker/package evidence. Existing independent build prerequisites remain.
  T60 proves original-evidence reopen compatibility; T33/T35 retain presentation/download scope.

- 2026-10-30 — Author-approved architecture review: hold integration with saved graph evidence
  until T46 settles the foundation and contract impact. If migration is chosen, T46 must add
  the required migration blockers before it closes.

- 2026-10-30 — T46 resolved with an approved migration. T49 now blocks this ticket until
  the replacement is accepted. Existing saved-evidence contracts remain part of its gate.
