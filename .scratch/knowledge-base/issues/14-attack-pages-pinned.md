# 14: The ATT&CK pages at a pinned version

Type: build
Status: ready-for-agent
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
      under the type checker, and the two-axis code review has run with its findings triaged
      (`mp-code-review` in Claude Code, `code-review` in Codex).

## Comments
