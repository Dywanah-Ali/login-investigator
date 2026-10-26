# 12: S6, the three benign twins and the answer key

Type: build
Status: resolved
Blocked by: 11
Phase: 0

## What to build

The generator plants a sixth story, S6: a password spray that succeeds on one IT Admins member. It
also plants three benign twins that look suspicious and are each cleared by one document. The
analyst sees S6, B1 and B2 on the Alerts screen like the other planted attacks. The generator writes
the knowledge base's answer key, `truth.json`, from the planted stories.

## Decisions implemented

- T04 d6 (S6), T04 d8 (the three twins), T04 conditions (S6 and twins on days apart from S1 to S5;
  group membership, S6's target, the leaver's name and the two never-mentioned users chosen here),
  T04 d14 (four absent topics), T04 d15 and T06 d2 (the answer key), T04 d17 (the Port's exam after
  regeneration).
- [spec ruling] B2 fails at least 20 times within an hour, then succeeds; [spec ruling] B3 is tested
  by asking about it directly; [spec ruling] the Port's ground-truth file stays.
- Author's ruling of 25 October 2026 at the ticket cut: the test that recomputes S6's radius moves to
  ticket 19, where the radius function lives.
- User stories 5, 6, 14, 52, 57 (the answer-key half), 58.

## Acceptance criteria

- [x] S6: a new attacker address with its own saved reputation file sprays many accounts, succeeds
      once on an IT Admins member, then signs in twice more from that address.
- [x] S3's and S6's targets are on the MFA exception list; their rows carry `mfa_result = none`.
- [x] B1: a Sales user signs in from Germany for three days, and a test proves the new-country rule
      fires.
- [x] B2: a user fails at least 20 times within an hour from their own laptop, then succeeds; a test
      proves brute force and success after failures fire.
- [x] B3: a user's rows switch `device_id` mid-week; a test proves no rule fires.
- [x] A test proves S6 and the twins fall on days that overlap none of S1 to S5.
- [x] `truth.json` holds S1 to S6; S6's blast radius (groups held, assets reached, users sharing its
      device and its VPN address that week, expected citation document IDs); each twin with verdict
      `benign` and its clearing document ID; the MFA exception list; the four absent topics; group
      membership, S6's target, the leaver and the two never-mentioned users.
- [x] Gold radii and paths are written from the planted story, never computed afterwards. The
      expected document IDs are planned IDs that the Codex brief (ticket 15) must use.
- [x] S4 stays an intentionally unresolved suspicious sign-in with `mfa_result = pass` and no
      MFA exception. `truth.json` distinguishes known login facts from unknown authorisation,
      compromise, Olivia's physical location, who completed MFA and the access mechanism.
      No additional incident document or telemetry source is required. See the spec's S4 ruling.
- [x] The Port's ground-truth file is still written in its current shape.
- [x] The Port's eval passes. Where a whole-log count changes, the expected value is updated with its
      reason recorded. Port-level questions are added for S6 only.
- [x] An API test proves S6, B1 and B2 appear as alerts.
- [x] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged.

## Comments

- 2026-10-26, author's ruling at ticket 11: this ticket adds the sign-ins that come through the VPN
  pool, handing the four addresses out in turn so that several users share one address in a week
  (T04 d5). Ticket 11 only wrote the pool into the networks table. The VPN rows change whole-log
  counts, which this ticket already owns.
- 2026-10-26, open question for the author, raised by ticket 11's spec review: S4's success from
  Russia carries `mfa_result = pass`, because T04 d7 makes every success `pass` except the accounts
  on the exception list, and S4's target is not on it. The data then says the attacker passed MFA,
  and no story explains that. Rule before `truth.json` is written: put S4's target on the exception
  list, or keep `pass` with a recorded reason (for example, an MFA-bypassing phishing proxy).

- 2026-10-26, author's ruling resolving the S4 question above: option 2 chosen. Olivia approved an unexpected authentication prompt but did not initiate the Russian sign-in. Keep `pass`, do not add her to the exception list. Reserve one incident record ID in the knowledge-base answer key; T15 and T16 own its specification and delivery. The corpus grows to 28 own documents. Evidence requirements are in the spec's S4 paragraph. No generator or dataset changes made in this decision session.

- 2026-10-26, superseding the option-2 implementation ruling above: the author deferred the expanded S4 authentication story as premature for this phase. Olivia's unsolicited statement was rejected as too convenient, and a phishing-proxy explanation would need evidence beyond the current log. No extra incident document or email, web or SIEM evidence requirement. The corpus remains 27 documents. S4's authentication explanation remains open before the answer key is written; no replacement has been selected and the dataset is unchanged.

- 2026-10-26, final author ruling superseding the open S4 question and earlier option-2 proposal: keep S4 as a suspicious sign-in whose cause is unknown. Preserve the event and MFA pass; no exception or extra document. The KB answer key must accept uncertainty and must not require confirmed compromise or an MFA attack mechanism. The Port ground-truth shape stays unchanged. Spec and map updated; implementation remains in T12.

- 2026-10-26, implementation started with `implement` and `tdd`; baseline commit `cbc0e8b`. Pre-agreed test seams: generator `generate`/`write` (door 1) and Alerts API (door 3); the radius recomputation stays in T19. Documentation decisions from this conversation are included in the review scope.

- Build choices, 26 October 2026: default S6 target `amelia.ward`; 20 accounts sprayed on 7 October,
  then successes at 02:10, 02:15 and 02:20 UTC from `45.148.10.80` (saved real AbuseIPDB lookup,
  NL, score 100). Maya Patel's travel is 2–4 October; her ordinary trip-period rows are relocated
  to Germany for consistency, with one added daily sign-in. Oliver Hayes's reset is 20 failures
  then success on 5 October at 06:00–06:10 UTC from his home address and own laptop. James Carter
  changes laptops at noon on 4 October; both historical devices remain in the register. The
  original S1 to S5 rows keep their seven Port fields, pinned by their pre-T12 hash. The 44 UK
  users each get one successful VPN sign-in on 7 October, using pool addresses in turn (11 users
  per address). This gives S6 10 network peers and no device peers, seven reachable assets and
  two groups. Shared context does not mean those peers are compromised. Other seeds select
  distinct eligible users. Leaver `finn.archer`; never-mentioned users `poppy.lowe` and
  `laura.fischer`. Planned citation IDs are listed in the dataset README and `truth.json`.
- Expected-value updates: 1,856 to 1,948 rows (+23 S6, +3 travel, +21 reset, +1 handover, +44 VPN),
  five to ten alerts (+spray and new-country for S6, +new-country for B1, +brute-force and
  success-after-failures for B2), Germany added to the country list, and one replacement laptop.
  Original rule tests now identify their original scenario by address rather than assuming
  one finding per rule. No rule, agent prompt, API contract or existing eval question changed.
  Two Port-level questions added for S6 (Q20 detection, Q21 successful sign-ins).


## Review

Fixed point: `cbc0e8b87b4f30ff66905eb1ae5fbed16fedbb07`. Reviewed implementation commit
`0d98d2e` with `git diff cbc0e8b...HEAD`; two independent read-only subagents used by
`mp-code-review`.

### Standards

No hard violations. Three judgement calls: repeated story timing/count facts could drift;
generator tests repeat expensive write/load/detect setup; API tests repeat a scenario-rule map.
All three addressed: named constants feed both rows and answer-key timestamps/counts; a
module-scoped fixture exercises the same public generator/loader/rules seam once; extra aliases
are kept only where used. Literal expectations remain independent in tests. Targeted checks pass.

### Spec

No implementation findings. S6, twins, VPN rows, both keys and saved reputation match the spec;
original planted events preserve their seven fields. S4 follows the final intentionally
unresolved ruling. Paths come from the planted grant and VPN plans; independent radius
recomputation stays in T19. Full-suite and eval evidence are tracked below before closure.

Review totals: Standards 0 hard violations and 3 judgement calls, all fixed; Spec 0 findings.

### Evaluation evidence

`backend/evals/results/2026-10-26-112540-7ff8e5ae.json`, API mode, three runs per question,
unchanged agent fingerprint `7ff8e5ae`: 58/63 overall (92%, gate 90%), security 15/15 (100%).
Original 19 questions 52/57; Q20 and Q21 6/6. Five failures kept: Q02 runs 2 and 3 (B-076,
AUD-047) and Q04 all runs (B-074 recurrence, AUD-046). No prompt or policy fix in this ticket.

- Review follow-up: the Standards reviewer verified `git diff 0d98d2e..24654bc` and confirmed all three judgement calls resolved, with no regression found in that delta. Regeneration on the final generator produced no dataset diff. Frontend: 149/149 tests, typecheck clean, lint has the same six AUD-009 warnings. Backend full suite remains running; no closure is claimed yet.


## Answer

Resolved 26 October 2026 on the implementation, two-axis review, passing safety net and API eval.
Author approved T12 on 26 October 2026: "T12 is approved". Local commits: `0d98d2e` implementation and `24654bc`
review fixes and evaluation evidence; `bc24d4a` closure evidence. Nothing pushed.

| Requirement | Evidence |
| --- | --- |
| S6 spray, privileged target, two later sign-ins, offline reputation | Generator tests and Q20/Q21 (6/6); saved AbuseIPDB response for `45.148.10.80` |
| MFA exceptions and device consistency | Generator tests; `truth.json` lists Daniel and Amelia; original Port fields hash preserved |
| Three benign twins and disjoint story days | Generator tests at `generate`/`write` through the real loader/rules; B1 and B2 alert, B3 does not |
| VPN peers and planted answer key | 44 VPN rows, 11 users per address; declared grant/allocation paths and expected document IDs in `truth.json`; T19 retains independent radius recomputation |
| S4 uncertainty | Knowledge-base key records five unknowns with MFA passed; no invented explanation or extra corpus record |
| API alert visibility and unchanged contract | API tests; original seven fields only; ten expected findings, including S6, B1 and B2 |
| Backend safety net | `uv run pytest -q`: 448 passed in 241.23 seconds |
| Backend type checking | `uv run pyright`: 0 errors, 0 warnings |
| Frontend safety net | Node 20.20.2; `npm --prefix frontend test -- --maxWorkers=1`: 149 passed; `npm --prefix frontend run typecheck`: clean |
| Lint | `npm --prefix frontend run lint`: six unchanged warnings, AUD-009; no frontend edits |
| Agent acceptance gate | API mode 58/63 overall and 15/15 security; original questions 52/57, new S6 questions 6/6; artifact linked above |
| Review | Standards 0 hard violations, 3 judgement calls all fixed and verified by reviewer; Spec 0 findings |
| Reproducibility and scope | Regeneration gives no dataset diff; original 19 questions and patterns unchanged; Port answer key changes only `row_count`; rules, tools, agent, frontend and API contract unchanged |

Known gaps retained: B-076/AUD-047 and B-074/AUD-046 evaluation failures. The benign clearing
documents are planned IDs; delivery and retrieval belong to later tickets. S4's unknown cause is
intentional. The final full suite passed after the review fixes. Frontier moves to 13, 14 and 15.

### Author acceptance

26 October 2026: "T12 is approved". T12 remains resolved. The recorded evaluation failures and
existing lint warnings retain their status; approval does not claim those issues were fixed.
