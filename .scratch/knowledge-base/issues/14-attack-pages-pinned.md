# 14: The ATT&CK pages at a pinned version

Type: build
Status: claimed
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

- [ ] The script fetches the STIX bundle at the pinned version and assembles each page from its
      linked objects.
- [ ] Each page is Markdown with the T04 d12 front matter, including the pinned version.
- [ ] MITRE's licence sits beside the pages; the dataset README names the ATT&CK version.
- [ ] A second run writes identical files.
- [ ] Only the script reaches the network; its tests run on a small saved sample of the bundle.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
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
