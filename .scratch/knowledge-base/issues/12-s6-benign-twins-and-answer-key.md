# 12: S6, the three benign twins and the answer key

Type: build
Status: ready-for-agent
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

- [ ] S6: a new attacker address with its own saved reputation file sprays many accounts, succeeds
      once on an IT Admins member, then signs in twice more from that address.
- [ ] S3's and S6's targets are on the MFA exception list; their rows carry `mfa_result = none`.
- [ ] B1: a Sales user signs in from Germany for three days, and a test proves the new-country rule
      fires.
- [ ] B2: a user fails at least 20 times within an hour from their own laptop, then succeeds; a test
      proves brute force and success after failures fire.
- [ ] B3: a user's rows switch `device_id` mid-week; a test proves no rule fires.
- [ ] A test proves S6 and the twins fall on days that overlap none of S1 to S5.
- [ ] `truth.json` holds S1 to S6; S6's blast radius (groups held, assets reached, users sharing its
      device and its VPN address that week, expected citation document IDs); each twin with verdict
      `benign` and its clearing document ID; the MFA exception list; the four absent topics; group
      membership, S6's target, the leaver and the two never-mentioned users.
- [ ] Gold radii and paths are written from the planted story, never computed afterwards. The
      expected document IDs are planned IDs that the Codex brief (ticket 15) must use.
- [ ] The Port's ground-truth file is still written in its current shape.
- [ ] The Port's eval passes. Where a whole-log count changes, the expected value is updated with its
      reason recorded. Port-level questions are added for S6 only.
- [ ] An API test proves S6, B1 and B2 appear as alerts.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged.

## Comments
