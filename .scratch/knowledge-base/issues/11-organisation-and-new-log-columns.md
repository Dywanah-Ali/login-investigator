# 11: The organisation and the two new log columns

Type: build
Status: ready-for-agent
Blocked by: 10
Phase: 0

## What to build

The seeded generator draws an organisation around the Port's 50 users and writes it as tables in the
`default` dataset folder: departments, privilege groups, memberships, assets with sensitivity and
owner, grants, a device register with assignments, and a networks table with the VPN pool. The log
gains a device ID and an MFA result per row. The Port's stories, rules and screens behave exactly as
before.

## Decisions implemented

- T04 d1 (one generator, extended; Port's seed, window, users, offices, home addresses, decoys and
  S1 to S5 kept exactly), T04 d2 to d5 (the organisation), T04 d4 and d7 (the two new columns),
  T05 d15 (the four rules do not read them), T05 d5 (graph record IDs are the IDs the generator
  writes).
- User stories 4, 52 to 55.

## Acceptance criteria

- [ ] The Port's rows keep their values in every old column; a test compares them with the rows
      before this ticket.
- [ ] The generator writes the tables people, groups, memberships, assets, grants, devices, device
      assignments and networks into `default`.
- [ ] Six departments; IT Admins, Finance Approvers and HR Data Owners with 3 to 5 members each; ten
      assets with sensitivity and owner as T04 d3 lists; one laptop per user plus two shared machines
      used by three users each across a department; a four-address VPN pool handed out in turn.
- [ ] Every record carries an ID written by the generator, the same on every run.
- [ ] The log gains `device_id` and `mfa_result` (`pass`, `fail`, `none`, `denied`; `denied` reserved
      and unused); the loader's column list comes from the generator.
- [ ] A test proves the tables and the log agree: every user is in people, every filled-in
      `device_id` is in the register and assigned to that user or a shared machine they use.
- [ ] `device_id` is empty on every attacker row and on every employee sign-in from a phone, and
      on no other row (spec rulings, 26 October 2026).
- [ ] The API replies do not change: the new columns are not returned to the screen unless the
      contract says so.
- [ ] The four rules' logic and tests are unchanged; the Port's eval passes.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged.

## Comments

- 2026-10-26, author's ruling before the build: unregistered devices leave `device_id` empty. The
  ticket's first wording would have put the victim's own laptop on attacker rows. Attacker rows are
  empty, and so is a small seeded share of ordinary employee rows (personal or public devices), so an
  empty value is a clue and never proof, as in real sign-in logs. Recorded in the spec's decisions log.
- 2026-10-26, author's ruling at the build: this ticket writes the four VPN pool addresses into the
  networks table in their hand-out order and adds no log rows. The VPN sign-ins are new rows, so they
  move to ticket 12 with S6 and the twins, where whole-log counts may change.
- 2026-10-26, author's ruling at the build, amending the first comment: measured, 124 of the 1,616
  employee rows (7.7%) come from a phone and the register holds no phones. The empty employee rows
  are exactly those phone sign-ins, with no further random share.
