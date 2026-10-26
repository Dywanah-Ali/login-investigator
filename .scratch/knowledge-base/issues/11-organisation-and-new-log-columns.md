# 11: The organisation and the two new log columns

Type: build
Status: resolved
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

- [x] The Port's rows keep their values in every old column; a test compares them with the rows
      before this ticket.
- [x] The generator writes the tables people, groups, memberships, assets, grants, devices, device
      assignments and networks into `default`.
- [x] Six departments; IT Admins, Finance Approvers and HR Data Owners with 3 to 5 members each; ten
      assets with sensitivity and owner as T04 d3 lists; one laptop per user plus two shared machines
      used by three users each across a department; a four-address VPN pool handed out in turn.
- [x] Every record carries an ID written by the generator, the same on every run.
- [x] The log gains `device_id` and `mfa_result` (`pass`, `fail`, `none`, `denied`; `denied` reserved
      and unused); the loader's column list comes from the generator.
- [x] A test proves the tables and the log agree: every user is in people, every filled-in
      `device_id` is in the register and assigned to that user or a shared machine they use.
- [x] `device_id` is empty on every attacker row and on every employee sign-in from a phone, and
      on no other row (spec rulings, 26 October 2026).
- [x] The API replies do not change: the new columns are not returned to the screen unless the
      contract says so.
- [x] The four rules' logic and tests are unchanged; the Port's eval passes.
- [x] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
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
- 2026-10-26, author's ruling at the review: the privileged groups cut across departments, one
  outsider each (IT Admins from Engineering, Finance Approvers from Operations, HR Data Owners from
  Finance). Recorded in the spec's decisions log.

### 2026-10-26: Build choices made inside the ticket

Testing at the spec's agreed doors 1 (generator), 4 (API) and the loader's own tests. Review
baseline `e57d11d`.

- **Separate random streams.** The organisation and the two columns draw from their own seeded
  streams (`"<seed>:organisation"`, `"<seed>:devices"`), so the Port's stream and rows cannot shift.
- **IDs from content:** `user-<username>`, `group-<slug>`, `mem-<group>-<username>`,
  `asset-<slug>`, `grant-<group>-<asset>`, `dev-laptop-<username>`, `dev-meeting-room-pc`,
  `dev-warehouse-terminal`, `asg-<device>-<username>`, `net-<name>`, `net-home-<username>`,
  `net-vpn-1` to `net-vpn-4`.
- **Baseline access through an `All Staff` group** of kind `baseline` with all 50 members, granted
  email, intranet and file share. The three privileged groups have kind `privileged`, so a later
  radius can tell them apart.
- **Departments:** Engineering 12, Sales 10, Operations 9, Finance 7, IT 7, HR 5, each with one US
  user. Groups: IT Admins 4, Finance Approvers 4, HR Data Owners 3.
- **Sensitivity** (T04 d3 names the assets but not each level): email and intranet internal; file
  share, VPN gateway and ERP confidential; identity provider, domain controller, backup server,
  payments system and HR system restricted. Owners are drawn from the group that holds the asset;
  the baseline assets' owners from IT Admins.
- **Shared machines** stand in the UK office: the meeting-room PC is used by three people from three
  departments, the warehouse terminal by three from Operations. About 30% of their UK office
  sign-ins are made on the shared machine (34 rows).
- **Networks:** the two offices, one home per UK user, the three decoys named after the Port's own
  comments (corporate proxy, cloud egress, public resolver address), the four VPN addresses
  `203.0.113.51` to `.54`. Attacker addresses are not the organisation's networks.
- **MFA:** S3's target is on the exception list now, since the column would otherwise say the
  attacker passed MFA; ticket 12 adds S6's target. S4's `pass` is an open question on ticket 12.
- **Rows leave the core with the Port's seven fields** (`loader.RECORD_FIELDS`), at the one exit
  every screen, the CSV download and the agent's tools share (`to_records`, `export_csv`).

### 2026-10-26: Review

`mp-code-review` against `e57d11d...ce07dbb`, two separate read-only reviewers.

- **Standards: no hard violations, nine judgement calls.** Fixed in `0beda3f`: the exception list
  names `S1_TARGET` instead of repeating the text; shared machines come from the devices table, not
  from parsing an ID; the ID helpers are private; the two zips are strict; a duplicate test is
  removed; a test's unclear name is replaced. Kept: plain tuples for the group and asset lists
  (commented, the module's style); the MFA values in the generator, beside the column list the
  loader takes from it; the 124 pin, which is the author's measured ruling; the docstring layout.
- **Spec: nothing missing.** Cross-cutting groups ruled by the author and fixed in `0beda3f`. The
  consequence notes on tickets 19 and 25 gained a line in the spec's decisions log. S4's MFA `pass`
  recorded as an open question on ticket 12. Notes kept: the decoys' network names follow the
  Port's comments; only one shared machine crosses departments, which T04 d4 allows; `fail` is
  unused, which the spec allows.

## Answer

Resolved on 26 October 2026. The generator draws the organisation around the Port's 50 users and
writes eight tables under `backend/data/datasets/default/org/`. The log gains `device_id` and
`mfa_result`, which stay inside the core. The Port's stories, rules, screens and answer key are
unchanged.

| Criterion | Evidence |
| --- | --- |
| Port rows unchanged | `test_port_rows_keep_their_old_values` hashes the seven old columns against the log committed at `e57d11d` (SHA-256 `920f501f…`) |
| Eight tables, shape and IDs | Generator tests for tables, departments, cross-cutting groups, assets and grants, devices, networks, unique IDs; byte-identical files across two runs |
| Two columns and loader | `COLUMNS` ends with the two; loader refuses an unknown `mfa_result`; MFA test |
| Tables and log agree; empty devices | `test_the_tables_and_the_log_agree`, `test_device_id_is_empty_exactly_on_attacker_and_phone_rows` (124 phone rows), shared-machine test |
| API unchanged | Existing API tests pin the seven fields on Alerts evidence, Explorer rows and the CSV header; `git diff e57d11d` is empty for `docs/api-contract.md` and `frontend/` |
| Rules unchanged; Port eval | `git diff e57d11d` empty for `rules.py`, `test_rules.py`, `ground_truth.json`, `questions.json`. Eval 53/57 (93%) overall and 15/15 security, gates met, fingerprint `7ff8e5ae`: `backend/evals/results/2026-10-26-095844-7ff8e5ae.json` |
| Safety net and types | 438 backend tests; 149 frontend tests; pyright 0 errors; frontend typecheck clean |
| Review | Two-axis review above, findings triaged |

Failed eval attempts kept and recorded: Q07 run 2 (B-070, AUD-030), Q08 runs 2 and 3 (B-073,
AUD-045), Q04 run 3 skipping all reputation lookups (new B-074, AUD-046). The agent's inputs did
not change, so none is attributed to this ticket. Commits `ce07dbb` (implementation) and `0beda3f`
(review fixes); evidence in a follow-up local commit. Nothing pushed. The frontier is 12, 13 and 14.

### 2026-10-26 — Author confirmation

After the closure report, the author wrote "T11 is approved, mark it resolved". Author acceptance
recorded as general approval of the closure evidence; no itemised checks were reported. Status
remains resolved. Open for ticket 12: the author's ruling on S4's MFA `pass`.
