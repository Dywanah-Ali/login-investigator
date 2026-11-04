# 56: Retire temporary comparison integration and keep a minimal evaluation foundation

Type: design, then build
Status: ready-for-agent
Blocked by: 54
Phase: supporting foundation for later operational evaluation
Rigour: Tier 3

## Scope

Author approved this direction on 4 November 2026 and recorded it in T54. T54's upload and
visual familiarisation are now accepted. This is a separate follow-up, not more comparison
upload work. No implementation has started.

Review temporary evaluation-platform/comparison code for retirement or archival. Replace
it with the bare minimum foundation needed for later operational agent evaluation, using
the official Langfuse SDK where it supplies the needed platform functions. The current
custom HTTP connector is not a required architecture. Agree the exact minimal scope with
the author before building; expand only once the agent evaluation scope is settled.

Preserve comparison results, originals and decisions. Account for the possible second model
comparison after tools are built before removing its tooling. Do not build full operational
evaluations, routine model-comparison operations or automated remote reconciliation here.

## Acceptance criteria

- [ ] Identify what to retire/archive and the minimum SDK-based foundation; author agrees scope.
- [ ] Preserve historical evidence and decisions; document the disposition of possible future
      comparison tooling before removal.
- [ ] Implement only the agreed minimum, with relevant documentation, focused checks and review.
- [ ] Leave full agent evaluation requirements/integration to later agreed operational scope.

## Comments

- 2026-11-04 — Split from T54 upon author acceptance of the familiarisation upload. Direction
  already approved; exact foundation design and implementation remain pending. No cleanup,
  dependency change, new paid run or further upload performed by opening this ticket.
