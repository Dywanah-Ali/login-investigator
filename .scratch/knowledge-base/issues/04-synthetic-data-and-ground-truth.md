# 04: Synthetic organisation, corpus and ground truth

Type: grilling
Status: resolved
Blocked by: 02

## Question

How is the synthetic organisation generated (people, accounts, groups, assets, devices,
networks), how does it stay consistent with the existing authentication log and its four rules,
and where does the written ground truth live so every eval question has a gold answer?

## Scope

- Size: tens of people, a handful of groups and assets, a few dozen documents. Enough to test,
  not to impress.
- Linked cases from research note 01, section 5: a spray that never succeeds; a spray followed by
  a success on a privileged account; shared device and shared network cases. Travel, service
  accounts and incidents are later phases and are not generated now, but the generator must leave
  room for them.
- Whether the existing log is kept as is and the organisation is generated to match it, or the
  log is regenerated alongside the organisation from one source of truth.
- The text corpus: which policies and runbooks are written, which ATT&CK pages are included and
  how (copied text with version, or fetched), and how documents are dated and versioned.
- Where generated data and ground truth live in the repo, and how a dataset is swapped (the API
  asks the core for "a dataset").

## Acceptance

- [x] Generation approach, size and linked cases decided and recorded. Evidence: decisions 1 to 8
      under `## Answer` (one generator, 50 users, six departments, three privilege groups, ten
      assets, devices, networks, S6, three benign twins).
- [x] Ground-truth format decided: one file that every eval question points at. Evidence:
      decisions 13 and 15 (`truth.json` inside the dataset folder, written by the generator,
      including S6's computed radius, the twins' verdicts, the MFA exceptions and the absent topics).
- [x] Relationship to the existing log decided without breaking the Port's tests and eval.
      Evidence: decisions 1, 7, 4 and 17 (the five old stories keep their rows; two new columns
      flow through the loader's `COLUMNS` import; the Port's eval must pass unchanged on the
      regenerated log before any corpus work).
- [x] Decision recorded here under `## Answer`.

## Answer

Grilled on 22 October 2026, one question at a time, after a plain-English discussion recorded in
the comments. Seventeen decisions. Each was the recommended option unless noted. Facts verified
in the repo during the grilling: the Port's log and `evals/ground_truth.json` are produced by one
seeded generator (`backend/login_investigator/generator.py`, seed 20261008, seven-day window
ending 8 October 2026 09:00 UTC, 50 users, five planted stories S1 to S5, three decoy addresses);
the Port's eval (`backend/evals/questions.json`) asserts that the Romanian spray address got into
no account; every attacker address has a saved reputation lookup under `data/ip_reputation/`;
the loader rejects any column list other than the generator's `COLUMNS`; the four rules are
brute force, password spraying, success after failures and new country.

### The world

| # | Decision | Detail |
|---|---|---|
| 1 | **Keep and extend.** The 50 users, two offices, home addresses, decoys and the five stories S1 to S5 stay exactly as generated. The organisation is drawn around them in the same generator | Names carry no meaning yet, so grouping them costs nothing. The Port's eval survives with the fewest re-pointings |
| 2 | **Six departments, three privilege groups.** Engineering, Finance, HR, Sales, Operations, IT, with the six US users spread across them. Cross-cutting: IT Admins, Finance Approvers, HR Data Owners, 3 to 5 members each. Everyone holds baseline access | Three different blast radii to test |
| 3 | **Ten assets, each with a sensitivity and an owner.** Everyone: email, intranet, file share. IT Admins: identity provider, VPN gateway, domain controller, backup server. Finance Approvers: payments system, ERP. HR Data Owners: HR system. Sensitivity is internal, confidential or restricted | Every privilege group reaches at least one restricted asset. Sensitivity leaves room for phase 4's risk score without a new table |
| 4 | **Device register and a device column.** One named laptop per user; two shared machines (a meeting-room PC and a warehouse terminal) used by three users each. Every log row carries `device_id` | "Same device, different user" becomes a fact. The shared-device case crosses a department |
| 5 | **Networks table with a VPN pool.** UK office, US office, one home address per UK user and the decoys stay as today. New: a four-address VPN pool handed out in turn, so one address is used by several users in a week | The shared-network case is true by construction |

### The stories

| # | Decision | Detail |
|---|---|---|
| 6 | **S6: a second spray that succeeds.** A new attacker address (new saved reputation lookup) sprays many accounts and succeeds once on an IT Admins member, on a day that does not overlap S1 or S2, followed by two more sign-ins from the same address. S2 stays a spray that never succeeds | Widest radius. The failed-versus-worked contrast is kept and the Port's S2 eval question survives |
| 7 | **`mfa_result` column** with four values: `pass`, `fail`, `none` (not prompted), `denied` (prompt refused). Normal successes are `pass`; failures that never reached MFA are `none`. Both compromised accounts (S3's and S6's targets) sit on a documented MFA exception list, so their rows are `none`. `denied` is unused now and reserved for MFA fatigue (AUD-037) | "Why did the spray work" gets an answer with a citation |
| 8 | **Three benign twins, each cleared by one document.** B1 approved travel: a sales user signs in from Germany for three days (twins S4; cleared by a travel notice). B2 reset burst: a user fails eight times from their own laptop in ten minutes, then succeeds (twins S1; cleared by a helpdesk ticket). B3 laptop swap: a user's rows switch to a new `device_id` mid-week (cleared by an IT handover record). **Condition:** each twin must trip the Port's rules, or it is not a twin: B2 crosses the brute-force threshold and B1 counts as a new country. The scanner twin stays in AUD-038 | An investigator earns trust on the cases it refuses to flag |

### The corpus

| # | Decision | Detail |
|---|---|---|
| 9 | **Thirteen ATT&CK pages at one named version.** T1110 with its four sub-techniques (guessing, cracking, spraying, credential stuffing); T1078 Valid Accounts with the domain-accounts sub-technique; T1621 MFA request generation and T1021 Remote Services for registered future stories; the four linked mitigations (MFA, account use policies, password policies, user account management). Fetched from the STIX bundle by a script kept in the repo; the version is pinned in the dataset README and each page's front matter; MITRE's licence file sits beside the pages | "What should have stopped this" has a citation |
| 10 | **Fifteen core own documents.** Policies: access control, password, MFA, remote access and VPN, acceptable use. Runbooks: password spray response, compromised account response, new-country sign-in triage, device onboarding and replacement. Registers and records: MFA exception register, shared device register, B1's travel notice, B2's helpdesk ticket, B3's laptop handover. Plus an older, superseded version of the password policy | Every story and twin has one explaining document |
| 11 | **Twelve extra documents, mostly noise.** Author's choice over the recommended 15-file corpus: five meeting notes (four weekly security meetings, one IT change board), five emails (all-staff MFA rollout, two helpdesk notices, an office move notice, a phishing awareness mail), two guidance documents (new starter guide, incident communication template). Two meeting notes restate the MFA exceptions in different words from the register. Total: **27 files** | Distractors and near-duplicates without new stories to keep consistent |
| | **Realism traits planted inside the 27:** the superseded policy version stays in the folder; one register names a leaver who is not in the tables; one runbook describes the spray response without ever naming a technique ID; one document carries instruction-like text (the corpus twin of S5) | The mess a real corpus has |
| 12 | **Markdown with fixed front matter:** `id`, `title`, `kind` (policy, runbook, register, record, meeting, email, guidance, attack), `owner` (a username), `department`, `date`, `version`, `status` (current, superseded), `supersedes`. Mentions of users, devices, assets and technique IDs are found by ingestion from the text, never hand-written. Per-kind extras live in ticket 03's JSON column | Typed filter columns come from the header; mentions cannot drift |
| 16 | **The Codex brief lives in the repo and delivery is checked by a script.** A standalone Codex session, outside this workspace, writes the 27 files from a brief kept in this initiative's folder. The brief carries the organisation's facts, the 27-file list with headers, the traits as counted requirements, the forbidden topics (decision 14) and the format. It never mentions evals, planted stories or reasons. A consistency script validates every front matter, checks every owner and every mentioned username, device and asset against the tables (allowing the one planted leaver), checks the four absent topics stay absent and reports lengths. Humans read for feel, not facts | The writer must not know the exam |

### Ground truth and the dataset

| # | Decision | Detail |
|---|---|---|
| 13 | **One folder per dataset** under `backend/data/datasets/<name>/`: `org/` (people, groups, memberships, assets, grants, devices, device_assignments, networks, one CSV each), `logins.csv`, `truth.json`, `corpus/own/`, `corpus/attack/` with the licence file, and a `README.md` naming the generator seed and the ATT&CK version. The generator writes everything except the two corpus folders. The Port's loader is pointed at the dataset's log, with the current path kept as the `default` dataset. Swapping a dataset is naming another folder | The world travels as one unit |
| 14 | **Four recorded gaps** for the refusal path: no incident write-ups (phase 2); no document governs the backup server; no data retention policy; two named users appear in no document. Recorded in `truth.json` as absent topics; the Codex brief forbids them without saying why | A missing kind, asset, policy and people, so plausible questions with no source are tested |
| 15 | **The generator writes the answer key.** `truth.json` holds each story (S1 to S6) as the Port records them today, S6's computed blast radius (groups held, assets reached, users sharing its device and its VPN address that week, document IDs expected as citations), each twin with the verdict `benign` and its clearing document ID, the MFA exception list and the absent topics. A generator test recomputes the radius from the tables and fails if `truth.json` disagrees | Gold answers in ticket 06 point at records; a human writes only the questions |
| 17 | **The Port's exam after regeneration.** Existing Port eval questions must pass unchanged on the regenerated log; where a new story changes a whole-log count, the expected value is updated with the reason recorded. Port-level questions are added for S6 only, because the Port's rules detect it alone. Twin questions belong to ticket 06. The regeneration (generator, tables, log, truth file, loader change) is phase 0's first build ticket, and the Port's tests and eval pass on it before any corpus or retrieval work starts | The safety net stays honest and phase 0 gets a clean first gate |

### Recorded as conditions, not decisions

- The seven-day window, the seed mechanism and the captured-at moment stay as the Port has them.
  S6 and the twins fit inside the window on days that do not overlap the old stories.
- Group membership, S6's target, the leaver's name and the two never-mentioned users are chosen
  when the tables are built and written into `truth.json`.
- Nothing in the corpus names a real company or person, and no technique text is written by
  Codex; ATT&CK text comes only from the bundle with its licence.

### Hand-offs

- **Ticket 05:** the tools read the org tables and `truth.json`'s shape; filters use the
  front-matter fields in decision 12; the knowledge base must be able to cite an exception
  register, a travel notice, a helpdesk ticket and a handover record.
- **Ticket 06:** gold answers point at `truth.json` records (decision 15); twin questions and the
  four absent topics (decision 14) are the false-positive and refusal material; Port-level S6
  questions are separate (decision 17).
- **Ticket 07:** the screen has three radii to show (groups, assets, peers by device and network)
  and a "cleared by" document for each twin.
- **Phase 0 build order:** regeneration first (decision 17), then the ATT&CK fetch script, then
  the Codex brief and the consistency script, then the corpus delivery.

### Register

AUD-037 to AUD-039 record what this ticket did not take: more attack stories, more twins, more
row signals and a longer baseline.

## Comments

**2026-10-22, Claude.** Claimed. Before the grilling, the author and Claude held a plain-English
discussion on four points. Positions reached, to be confirmed or overturned in the grilling:

1. **Log and organisation from one generator.** The Port's log is already produced by a seeded
   generator (`backend/login_investigator/generator.py`) together with `evals/ground_truth.json`.
   The organisation is added to that generator rather than fitted to the log. The author accepts
   that the Port's tests and eval set are re-pointed to the regenerated log.
2. **Scope of planted scenarios.** The Port's five stories suffice for phases 0 and 1 but not for
   a product. Ticket 04 takes the cheapest honest additions: a spray that succeeds on a
   privileged account, an MFA column, and two or three benign look-alikes that twin a planted
   attack. The rest is registered as AUD-037 to AUD-039.
3. **Who writes the corpus.** ATT&CK pages are copied from the STIX bundle with the licence
   notice. Policies and runbooks are written by a standalone Codex session outside this
   workspace, from a brief that gives the organisation's facts, the document list with metadata,
   and the realism traits as hard requirements, and withholds the eval questions, the planted
   stories and the reasons. The brief is a ticket 04 deliverable; the files are reviewed for
   consistency with the organisation before they enter the repo.
4. **Ground truth has two layers.** World truth (people, accounts, groups, grants, assets, devices,
   networks, planted stories) is produced by the generator and decided here. Gold answers per
   eval question are written by a human against the world truth and decided in ticket 06. Leaning:
   world truth as a folder of typed tables plus the log CSV plus the corpus, one folder per dataset.

**2026-10-22, Claude.** Resolved. Seventeen questions asked one at a time through the pop-up tool.
The author took the recommended option on sixteen and chose a larger corpus on question 10
(around 25 files with meeting notes and emails, settled as 27 in decision 11). Facts looked up in
the repo mid-grilling: the Port's eval asserts the S2 address got into no account; every attacker
address has a saved reputation file; the loader imports `COLUMNS` from the generator; the four
rules. Map pointer added; frontier moves to ticket 05.

**2026-10-25, Claude, while writing the spec: decision 8 corrected by two author's rulings.** The
four rules were checked against the twins. The brute-force rule needs 20 failures on one account
from one address within an hour, and success-after-failures needs 10 in the hour before a success,
so B2's eight failures would trip neither, against this decision's own condition. None of the rules
reads `device_id`, so B3 can never become an alert. The author ruled, one pop-up at a time: **B2
fails at least 20 times within an hour, then succeeds**, so it trips both rules; **B3 is tested by
asking the agent about the laptop change directly**, and passes only if the agent finds the IT
handover record and calls it benign. A fifth rule was not taken. The Answer above is unchanged; the
spec (`../spec.md`, decisions log) carries the rulings.
