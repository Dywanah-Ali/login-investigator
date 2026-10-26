# 13: The finding ID in the core

Type: build
Status: resolved
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

- [x] Every finding has a `finding_id` of the form `F-<rule>-<hash8>`.
- [x] The exact hash fields, their order and the slug rules are fixed and written under this ticket's
      Answer.
- [x] A test proves the same log gives the same IDs across runs and across processes.
- [x] A test proves no two findings on the `default` dataset share an ID.
- [x] The four rules' logic and their tests are unchanged.
- [x] The Alerts API reply is unchanged in this ticket.
- [x] The Port's eval passes.
- [x] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
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
errors, 0 warnings. Implementation commit: `bb231dd`.

## Review

`mp-code-review` against `1264d9a...bb231dd`, two separate read-only reviewers.

### Standards

No hard violations. One documented-standard gap and five judgement calls.

| Finding | Triage |
| --- | --- |
| The docstring points at an Answer section that did not exist yet (`docs/agents/issue-tracker.md`: resolve under `## Answer`) | Fixed: the Answer below carries the recipe |
| Mysterious Name: `defining` | Fixed: renamed `defining_fields`, the spec's own words |
| Test readability: chained `len(set(ids)) == len(ids) > 1` | Fixed: two plain asserts |
| Test readability: child script joined from escaped string literals | Fixed: a `textwrap.dedent` block |
| Duplicated Code: the two `strftime(TIMESTAMP_FORMAT)` calls appear in both `finding_id` and `to_dict` | Kept: two lines, and the pinned recipe test fails if they drift |
| Primitive Obsession (weak): the slug built inline with `replace` | Kept: four rule keys, one place that builds the slug |
| Observation: the ten `default` IDs are not pinned by a test | Kept: the IDs follow from the log and the recipe. The recipe is pinned by its test, and the log by the generator's regeneration check, so a third pin adds nothing |

### Spec

No wrong implementation and no scope creep. The reviewer re-ran the worked example through
`shasum` and recomputed all ten `default` IDs; both match. The computed property in place of a
stored field was judged acceptable, since it reads like a field and cannot drift.

| Finding | Triage |
| --- | --- |
| The recipe sits under Comments, not under an Answer | Fixed: the Answer below |
| Pending evidence: full safety net and Port eval | Done: see Verification |
| Boundary note for ticket 32: `to_dict()` feeds both the Alerts reply and the agent's detection tool, so adding the field there would change the agent's view too | Outside T13. Registered as AUD-048 for ticket 32's builder |

Review fixes re-checked: rules tests 39 passed, Pyright 0 errors, 0 warnings.

## Verification

- `uv run pytest -q` (backend): 453 passed, before and after the review fixes. That is 448 from T12
  plus the five new ID tests.
- `uv run pyright` (backend): 0 errors, 0 warnings, 0 informations.
- `npm --prefix frontend test -- --maxWorkers=1`: 149 passed across 13 files.
- `npm --prefix frontend run typecheck`: clean. The frontend lint was not re-run; no frontend file
  changed, and its six known warnings stay AUD-009.
- `uv run python -m evals.run --mode api`: **57/63 overall (90.5%, gate at least 90%) and 15/15
  security (gate 100%). Both gates met, with no spare run.** Prompt fingerprint `7ff8e5ae`,
  unchanged. Result: `backend/evals/results/2026-10-26-131223-7ff8e5ae.json`. Its summary line
  has an empty label because none was passed, and reads `bb231dd+changes` because the review fixes
  were in the working tree when the line was written. The server it ran had started on the
  implementation's code; the review fixes only rename a local variable and edit tests. The record
  is left as written.
- The six failed runs are kept as they are, and the eval was not re-run for a cleaner score:
  - Q02 fails all three runs on the same check, "says no attempt succeeded". Each answer gives S6 as
    20 failed attempts and omits its three successes. This is the B-076/AUD-047 recurrence, which
    was two runs in T12.
  - Q04 fails all three runs on the required reputation lookups. This is the B-074/AUD-046
    recurrence, the same as in T12.
  - T13 changed no tool output, prompt or agent code, so both are the unchanged model sampled
    again. All other questions pass 3/3, including the S6 questions Q20 and Q21.

## Answer

Resolved on 26 October 2026. Every finding the four rules produce now carries a content-made
`finding_id`. The same log gives the same IDs in any order and in any process. No rule, tool output,
API reply or agent behaviour changed.

**The recipe**

| Part | Rule |
| --- | --- |
| Form | `F-<rule slug>-<hash8>` |
| Rule slug | The rule's key with each `_` replaced by `-`: `brute-force`, `password-spraying`, `success-after-failures`, `new-country` |
| Hashed fields, in order | rule key (with underscores), users, addresses, first seen, last seen |
| Users and addresses | The finding's own tuples: unique values sorted, usernames as written in the log |
| Times | `YYYY-MM-DDTHH:MM:SSZ` in UTC |
| Serialisation | A JSON array, no spaces, non-ASCII kept as is, encoded UTF-8 |
| Hash | SHA-256; the first eight lowercase hexadecimal characters |

Worked example: `["brute_force",["u1"],["1.2.3.4"],"2026-10-01T00:00:00Z","2026-10-01T00:19:00Z"]`
gives `F-brute-force-abd70cbf`. The code is `Finding.finding_id` in
`backend/login_investigator/rules.py`. It is a computed property, kept out of `to_dict()`.

| Criterion | Evidence |
| --- | --- |
| Every finding has a `finding_id` of the agreed form | `test_every_finding_has_an_id_naming_its_rule` |
| Recipe fixed and written | This Answer; `test_the_id_follows_the_recipe_fixed_in_ticket_13`, with the value computed by `shasum` |
| Same IDs across runs and processes | `test_ids_do_not_depend_on_the_order_of_the_rows`; `test_the_same_log_gives_the_same_ids_in_another_process` (two children, `PYTHONHASHSEED` 1 and 2) |
| No shared ID on `default` | `test_no_two_findings_on_the_default_dataset_share_an_id`; ten distinct IDs, listed under Comments |
| Rules and their tests unchanged | The diff adds tests only; no rule body or existing test changed |
| Alerts reply unchanged | `to_dict()` untouched; `test_api_dashboard.py` pins the reply's key set and passes |
| Port eval passes | 57/63 and 15/15, both gates met |
| Safety net, types, review | 453 backend, 149 frontend, clean types; two-axis review triaged above |

Known limit, written here so a later dataset does not trip on it: times are hashed to the second.
Findings of one rule over the same users and addresses that start and end in the same seconds would
share an ID.

Retained outside scope: B-076/AUD-047 and B-074/AUD-046 recur and leave the Port eval at its gate
with no margin. AUD-048 is new, for ticket 32. Nothing pushed. The frontier is 14 and 15. T13
unblocks no ticket on its own: 20 still needs 19, 26 needs 25 and 32 needs 29.
