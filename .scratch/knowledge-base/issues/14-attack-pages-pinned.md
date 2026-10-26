# 14: The ATT&CK pages at a pinned version

Type: build
Status: resolved
Blocked by: 10
Phase: 0

## What to build

A script kept in the repo fetches MITRE ATT&CK's STIX bundle at one pinned version and writes the
thirteen technique and mitigation pages the corpus needs into the `default` dataset folder, with
MITRE's licence beside them. The knowledge-base build (ticket 17) can start from these pages alone.

## Decisions implemented

- T04 d9 (thirteen pages: T1110 and its four sub-techniques, T1078 with the domain-accounts
  sub-technique, T1621, T1021, and the four linked mitigations), T03 d3 (pages assembled from linked
  objects), T04 d12 (front matter fields, kind `attack`), T04 d13 (MITRE's licence in the folder,
  version in the README).
- User story 59.

## Acceptance criteria

- [x] The script fetches the STIX bundle at the pinned version and assembles each page from its
      linked objects.
- [x] Each page is Markdown with the T04 d12 front matter, including the pinned version.
      Ownership clarified by the author's ruling recorded below.
- [x] MITRE's licence sits beside the pages; the dataset README names the ATT&CK version.
- [x] A second run writes identical files.
- [x] Only the script reaches the network; its tests run on a small saved sample of the bundle.
- [x] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged.

## Comments

- 26 October 2026, Codex: claimed on the author's `$implement T14`. Baseline commit
  `bc6a3432e2ba40f8093f25dba21f8e98ed1b65a8`. Checking the official MITRE release and
  testing the saved-bundle-to-files boundary before the live download and final review.
- 26 October 2026, author: approved the test boundary in chat after the pop-up question did
  not appear. Tests observe the generated files from a saved sample, with a separate real
  download check. The author requested troubleshooting of the recurring pop-up issue after
  this ticket closes; it is separate from T14's implementation.
- 26 October 2026, implementation choices: Enterprise ATT&CK 20.0, release commit
  `20664a889568dce884a1dac0ec7b12ae3a199f51`, verified from MITRE's official GitHub API.
  Both source files have SHA-256 pins. Pages live under `default/corpus/attack/`; their IDs
  follow `attack-t1110-003`. Header `date` is the object's modification date, `version` is
  the release, and external provenance is `owner: mitre`, `department: external`, rather
  than attributing MITRE text to a synthetic employee. Detection follows strategy-to-analytic
  links. Mitigation pages describe only their links to the nine selected techniques.
- 26 October 2026, review and verification: [two-axis review](../reviews/14-code-review-2026-10-26.md).
  Standards zero findings; Spec one medium finding on the external-owner convention.
  Proposed exception awaiting the author's approval. Backend 521 passed, frontend 149 passed,
  clean backend/frontend types, 11 focused converter/core tests after whitespace cleanup.
  Port API eval `2026-10-26-202907-b70d0745.json`: 62/63 overall, 15/15 security;
  Q02 2/3 and Q04 3/3. Q02 run 3 repeats B-076; AUD-047 reopened outside this ticket.
  No agent, tool or grader changed and no cleaner-score rerun. Ticket stays claimed until
  the external-owner decision is recorded and the review finding is settled.

- 26 October 2026, closing ruling: the author approved team ownership for internal documents.
  Document responsibility is separate from login accounts; ATT&CK retains its external-publisher
  labels. Recorded in the spec's corpus section and decisions log, T04's superseding comment,
  and T15's acceptance criteria. Follow-up Spec review: finding settled, no new contradictions.

## Answer

Resolved 26 October 2026. `backend/scripts/fetch_attack.py` downloads the Enterprise ATT&CK
20.0 bundle and licence from the pinned MITRE commit, verifies both hashes, then calls the
network-free `login_investigator.attack_corpus` converter. Thirteen pages and MITRE's exact
licence are saved under `backend/data/datasets/default/corpus/attack/`. Pages assemble linked
mitigation advice, procedure examples, detection strategies and analytics with references.
The dataset README records provenance, header meanings and the regeneration command.

Evidence: 521 backend tests, 149 frontend tests, clean type checks, 11 focused converter/core
checks after whitespace normalisation, repeated real fetches with identical files, and Port
API eval `2026-10-26-202907-b70d0745.json` at 62/63 overall and 15/15 security. Two-axis review
has zero unresolved findings after the ownership ruling. B-079 and B-080 retain development
iterations. B-076/AUD-047 recurred on one model answer; logged outside T14 without changing
the agent or rerunning for a better score. No push. Ticket 17 is now unblocked.
