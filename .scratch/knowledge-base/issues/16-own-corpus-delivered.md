# 16: The own corpus delivered and checked

Type: task (human)
Status: resolved
Blocked by: 15
Phase: 0

## What to build

The author runs a standalone Codex session that writes the 27 own documents from the brief alone, so
the writer never knows the exam. The documents land in the own corpus folder of the `default`
dataset, the consistency script passes on them, and the author reads them for feel. The chunk sizes
planned per document kind are confirmed against the real lengths.

## Decisions implemented

- T04 d10, d11 and d16 (the documents, their traits, the standalone writer and the script).
- T03 d3 (chunk sizes per kind, note 03 section 3.2, confirmed against the real corpus here).
- User stories 60 to 62.

## Acceptance criteria

- [x] The author runs the Codex session with the brief as its only input; the date is recorded here.
      Evidence: 2026-10-27, a standalone Codex session in an empty folder outside the repo that
      held only a byte-identical copy of `codex-brief.md`. That copy is filed unchanged as
      `evidence/16-codex-writer-brief-2026-10-27.md` (SHA-256 `cfeb869f…b22a545`), identical to
      `codex-brief.md` at commit `5161357`. The writer's folder was emptied on 2026-10-27.
- [x] 27 documents sit in the own corpus folder.
      Evidence: 2026-10-27, copied to `backend/data/datasets/default/corpus/own/`; `diff -r` against
      the writer's folder reports no difference.
- [x] The consistency script passes on them; its report is saved with this ticket.
      Evidence: 2026-10-27, `python -m scripts.check_corpus` exit 0, "Passed: 27 documents,
      0 errors". Report under "Checker report, 2026-10-27" below.
- [x] Nothing in the corpus names a real company or person.
      Evidence: 2026-10-27 scan of the own documents, under "Real names scan, 2026-10-27" below.
      Scope: the 27 own documents. The ATT&CK pages are MITRE's published text and name real
      threat groups and publishers by design (T14).
- [x] The author reads the documents for feel; a dated line records it, with any rewrites asked for.
      Evidence: 2026-10-27, the author approved the 27 own documents with no rewrites asked for.
      The phrase "within the recorded minute window" in `rec-helpdesk-reset` stays as written.
- [x] The script's length report is compared with the planned chunk sizes per kind; any change to the
      chunking settings is recorded here for the build (ticket 17).
      Evidence: 2026-10-27, "Length comparison with note 03 section 3.2" below, with the author's
      rulings P1 to P4c; written to the spec and to ticket 17's criteria.

## Comments

- 2026-10-26, author's S4 ruling: the corpus grows from 27 to 28 own documents, adding one incident record for Olivia's unexpected authentication approval. Follow the S4 evidence requirements in the spec: distinguish sign-in observations, her later statement and responder assessment; align UTC times; preserve unknowns. Use the document ID reserved by T12. Do not describe the event as prompt flooding, phishing-proxy compromise or token theft without supporting evidence.

- 2026-10-26, superseding the S4 ruling above: the author deferred the expanded authentication-attack story as premature for this phase. Restore the 27-document plan; no additional S4 incident record or email, web or SIEM evidence is required. S4's authentication explanation is open again on T12.

- 2026-10-26, final S4 ruling: the question is settled as intentional uncertainty, not a missing incident story. Keep the 27-document plan. Do not invent Olivia statements or S4-specific proof of authorisation, compromise or an authentication-attack mechanism. See the spec's S4 ruling.

- 2026-10-27, Claude: read-only spot check of the 27 delivered files, still outside the repo.
  Names match the brief's list; owners are only the five teams; one superseded document
  (`pol-password-2024`), replaced by `pol-password`; no technique ID in
  `run-password-spray-response`; the leaver only in `reg-shared-devices`; the instruction-like
  paragraph in `mtg-change-board-2026-09-24`; no hidden users, backup, retention or IP address
  found; about 13,300 words, each document near its planned range. `rec-helpdesk-reset` matches
  the log's timeline and `reg-mfa-exceptions` holds exactly the two exceptions. One feel note for
  the author's read: the helpdesk ticket's phrase "within the recorded minute window" reads like
  the brief, not an analyst. Not yet done: copying into `corpus/own/`, the checker run and report,
  the author's read, the length comparison.

- 2026-10-27, Claude: copied the 27 files into `corpus/own/`, ran the checker, scanned for real
  names, measured section lengths in tokens. Results below. The backend suite still passes, 555
  tests. Open: the author's read.

### Checker report, 2026-10-27

`uv run --directory backend python -m scripts.check_corpus`, exit 0.

| Document | Kind | Words | Sections | Longest section |
|---|---|---|---|---|
| eml-helpdesk-hours | email | 207 | 3 | 91 |
| eml-helpdesk-self-service | email | 219 | 3 | 96 |
| eml-mfa-rollout | email | 275 | 3 | 173 |
| eml-office-move | email | 224 | 3 | 96 |
| eml-phishing-awareness | email | 386 | 4 | 145 |
| gde-incident-communication | guidance | 522 | 5 | 166 |
| gde-new-starter | guidance | 633 | 6 | 128 |
| mtg-change-board-2026-09-24 | meeting | 419 | 6 | 90 |
| mtg-security-2026-09-08 | meeting | 307 | 4 | 103 |
| mtg-security-2026-09-15 | meeting | 326 | 4 | 126 |
| mtg-security-2026-09-22 | meeting | 330 | 5 | 91 |
| mtg-security-2026-09-29 | meeting | 324 | 4 | 132 |
| pol-acceptable-use | policy | 813 | 7 | 153 |
| pol-access-control | policy | 815 | 7 | 183 |
| pol-mfa | policy | 700 | 6 | 146 |
| pol-password-2024 | policy | 616 | 5 | 153 |
| pol-password | policy | 690 | 6 | 153 |
| pol-remote-access | policy | 712 | 6 | 143 |
| rec-approved-travel | record | 246 | 3 | 103 |
| rec-helpdesk-reset | record | 300 | 3 | 151 |
| rec-laptop-handover | record | 245 | 4 | 75 |
| reg-mfa-exceptions | register | 300 | 3 | 109 |
| reg-shared-devices | register | 293 | 3 | 101 |
| run-compromised-account-response | runbook | 689 | 3 | 504 |
| run-device-onboarding | runbook | 620 | 4 | 236 |
| run-new-country-sign-in | runbook | 595 | 3 | 418 |
| run-password-spray-response | runbook | 629 | 3 | 470 |

| Kind | Documents | Fewest words | Most words |
|---|---|---|---|
| email | 5 | 207 | 386 |
| guidance | 2 | 522 | 633 |
| meeting | 5 | 307 | 419 |
| policy | 6 | 616 | 815 |
| record | 3 | 245 | 300 |
| register | 2 | 293 | 300 |
| runbook | 4 | 595 | 689 |

Passed: 27 documents, 0 errors

### Real names scan, 2026-10-27

- Every capitalised two-word phrase in the 27 documents was compared with `org/people.csv`. The
  only name outside the table is Finn Archer, the planned leaver, found only in
  `reg-shared-devices`. All other phrases are document titles, groups or headings.
- The only domain is `corp.example`, a reserved example domain. No vendor or product name
  (Microsoft, Okta, Google and others) appears; "authenticator app" and "teams" are generic.
- Systems named in prose match `org/assets.csv` or the brief: identity provider, VPN gateway, file
  share, payments system, ERP, HR system, the intranet's self-service reset portal, the lab
  workstation and the warehouse terminal WH-TERM-01.

These scans support, but do not replace, the author's read for AUD-055. The third AUD-055 check,
technique IDs in `run-password-spray-response`: none. Technique IDs appear in five other own
documents, which the checker validated against the plan.

### Length comparison with note 03 section 3.2, 2026-10-27

Method: each document split at `#`, `##` and `###` headings, heading kept with its text, sections
with no body skipped, tokens counted with `tiktoken` `cl100k_base`. This mirrors the planned
heading split before any size split. The counting script was a one-off in the session scratchpad,
not part of the repo.

| Kind | Planned size / overlap (tokens) | Sections | Smallest | Median | Largest | Over 350 |
|---|---|---|---|---|---|---|
| policy | 250–350 / 30–50 | 37 | 62 | 126 | 292 | 0 |
| runbook | 200–350 / 25–50 | 13 | 63 | 131 | 635 | 3 |
| email | not planned | 16 | 54 | 112 | 223 | 0 |
| guidance | not planned | 11 | 65 | 123 | 244 | 0 |
| meeting | not planned | 23 | 48 | 93 | 177 | 0 |
| record | not planned | 10 | 61 | 112 | 230 | 0 |
| register | not planned | 6 | 100 | 125 | 223 | 0 |
| ATT&CK, without `## References` | 200–350 / 20–40 | 274 | 20 | 62 | 767 | 43 |

What it shows:

1. Policies never reach the size split. Every section fits whole, and chunks will be smaller than
   the 250–350 target, median 126. The spec cuts at headings and never merges, so this is
   expected.
2. Runbooks reach the size split in three "Response steps" sections: 635, 577 and 512 tokens. Each
   numbered step is about 80 to 130 tokens. The boundary rule "a numbered step stays whole" is
   therefore live, and ticket 17 needs a test that no step is cut.
3. Five own kinds have no planned row: email, guidance, meeting, record and register. Their
   largest section is 244 tokens, so a 350 limit never fires on them.
4. The ATT&CK pages carry a `## References` section of citations that dwarfs the content: 17,282
   of T1078's 26,414 tokens. Without it, 43 of 274 sections still exceed 350. 185 of the 274
   sections are procedure examples, one short paragraph per threat group or tool. The text also
   holds 324 inline `(Citation: ...)` markers.

Also found while ruling: 224 Markdown links with web addresses and two `<code>` pairs sit in the
ATT&CK text outside the References lists.

Author's rulings, 2026-10-27, asked one at a time (recorded in the spec, "Chunking rulings at T16",
and its decisions log; carried to ticket 17's criteria):

- P1. The five unplanned own kinds take the policy row: 350 tokens, overlap 30 to 50.
- P2. Runbooks keep their row; ticket 17 adds a test that every numbered step lands whole in one
  chunk. The documents are not edited to add a heading per step: the writer wrote blind, and the
  chunker must cope with plain numbered steps.
- P3. `## References` sections of ATT&CK pages are not chunked. The files keep them; a test fails
  loudly if a future converter format lets them back in. Keeping MITRE's source links as metadata
  for provenance is registered as AUD-056, not built.
- P4a. Inline `(Citation: ...)` markers are removed from chunk text, files unchanged, under a test.
  Revised from the first proposal ("leave for the eval") because P3 removes what they point to.
- P4b. Procedure examples are packed several to a chunk, up to 350 tokens, each whole, under a
  test. This restores note 03's one chunk per field group.
- P4c. Markdown links keep their visible text and lose the address; the `<code>` tags are removed;
  files unchanged, under a test.

The author asked whether P3 is only a convenience. Claude's answer: no, production pipelines strip
references and boilerplate before indexing, and the pinned converter makes the format stable
within a version; the test covers changes between versions.
