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
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged.

## Comments

### 2026-10-26 — Implementation

Tested at the core rules door (`rules.detect_all` and the rule functions, door 2's prior art: the
core tests for rules). Review baseline: `1264d9a`.

**The recipe, fixed by this ticket.** The eval's answer key and the agent's investigation tool
depend on it; changing any line below changes every ID.

| Part | Rule |
| --- | --- |
| Form | `F-<rule slug>-<hash8>` |
| Rule slug | The rule's key with each `_` replaced by `-`: `brute-force`, `password-spraying`, `success-after-failures`, `new-country` |
| Hashed fields, in order | rule key (with underscores, e.g. `brute_force`), users, addresses, first seen, last seen |
| Users and addresses | The finding's own tuples: unique values sorted, usernames as written in the log (case kept) |
| Times | `YYYY-MM-DDTHH:MM:SSZ` in UTC, the same text the finding's dictionary shows |
| Serialisation | A JSON array, no spaces (`separators=(",", ":")`), non-ASCII kept as is, encoded UTF-8 |
| Hash | SHA-256 of those bytes; the first eight lowercase hexadecimal characters |

Worked example, pinned by a test with its value computed outside Python by `shasum -a 256`:
`["brute_force",["u1"],["1.2.3.4"],"2026-10-01T00:00:00Z","2026-10-01T00:19:00Z"]` gives
`F-brute-force-abd70cbf`.

Choices made at build time:

- **A computed property, not a stored field.** `Finding.finding_id` is worked out from the
  finding's own fields each time it is asked for, so the ID can never disagree with the content it
  names. No rule constructs it and the four rules' logic is untouched.
- **Kept out of `Finding.to_dict()`.** That dictionary is both the Alerts reply and the agent's
  detection tool output, so leaving the ID out keeps the API and the agent's view unchanged, as
  this ticket requires. Ticket 32 adds it to the Alerts reply; ticket 26's tool reads the property.
- **The hash reads the full rule key, the prefix shows the slug.** The slug is only presentation;
  the hashed text uses the key the code already uses everywhere.
- **Kebab-case slugs, full words.** Readable in a question the analyst sends ("Investigate finding
  F-password-spraying-d06a7545"), at the cost of length. The hash is always the last eight
  characters after the final `-`, so the ID splits unambiguously.

Known limit: times are hashed to the second, the log's own resolution. Two findings of the same
rule over the same users and addresses that start and end in the same seconds would share an ID.
The uniqueness test guards the `default` dataset; a later dataset with sub-second times would need
the recipe revisited.

The ten IDs on the `default` dataset:

| ID | First seen (UTC) | Address | Users |
| --- | --- | --- | --- |
| `F-new-country-f2ec8467` | 2026-10-02 08:17 | 203.0.113.70 | 1 |
| `F-brute-force-4d4fd1ab` | 2026-10-05 06:00 | 198.51.100.30 | 1 |
| `F-success-after-failures-cc1083a7` | 2026-10-05 06:00 | 198.51.100.30 | 1 |
| `F-password-spraying-4a90a716` | 2026-10-06 03:04 | 2.57.122.53 | 35 |
| `F-new-country-830a45a8` | 2026-10-06 13:47 | 91.142.73.116 | 1 |
| `F-password-spraying-d06a7545` | 2026-10-07 02:00 | 45.148.10.80 | 20 |
| `F-new-country-1ef7362b` | 2026-10-07 02:10 | 45.148.10.80 | 1 |
| `F-brute-force-0ce5e14e` | 2026-10-08 01:12 | 185.218.86.24 | 1 |
| `F-success-after-failures-9a4beef6` | 2026-10-08 01:32 | 185.218.86.24 | 1 |
| `F-new-country-4a3d5d22` | 2026-10-08 02:32 | 185.218.86.24 | 1 |

TDD evidence: the shape test failed with `AttributeError` before the property existed, then
passed. The recipe, row-order, cross-process (two children with `PYTHONHASHSEED` 1 and 2) and
uniqueness tests passed on first run, because the first cycle had already built the recipe; the
recipe test's expected value comes from an independent tool, so it still guards the recipe.
Focused checks: rules, Alerts API and tool tests 126 passed; Pyright on the changed files 0
errors, 0 warnings.
