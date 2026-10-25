# 13: The finding ID in the core

Type: build
Status: ready-for-agent
Blocked by: none
Phase: 0

## What to build

Every finding the four rules produce carries a short stable ID, made from the finding's content, so
the same log always gives the same IDs. The agent's investigation tool (ticket 26) and the eval's
answer key point at these IDs. The Alerts screen does not show it yet; that is ticket 32.

## Decisions implemented

- T05 d5 (IDs made from content, never from storage order); spec "The IDs": `F-<rule>-<hash8>`, the
  rule slug plus an eight-character hash of rule, users, addresses, first and last seen.
- [review ruling 5] the core's finding ID is phase 0; the Alerts field ships in phase 1.
- T05 d15 (the four rules' logic is untouched).
- User story 2.

## Acceptance criteria

- [ ] Every finding has a `finding_id` of the form `F-<rule>-<hash8>`.
- [ ] The exact hash fields, their order and the slug rules are fixed and written under this ticket's
      Answer.
- [ ] A test proves the same log gives the same IDs across runs and across processes.
- [ ] A test proves no two findings on the `default` dataset share an ID.
- [ ] The four rules' logic and their tests are unchanged.
- [ ] The Alerts API reply is unchanged in this ticket.
- [ ] The Port's eval passes.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and Codex reviews the change.

## Comments
