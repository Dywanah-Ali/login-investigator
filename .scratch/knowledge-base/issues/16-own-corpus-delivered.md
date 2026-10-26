# 16: The own corpus delivered and checked

Type: task (human)
Status: ready-for-human
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

- [ ] The author runs the Codex session with the brief as its only input; the date is recorded here.
- [ ] 27 documents sit in the own corpus folder.
- [ ] The consistency script passes on them; its report is saved with this ticket.
- [ ] Nothing in the corpus names a real company or person.
- [ ] The author reads the documents for feel; a dated line records it, with any rewrites asked for.
- [ ] The script's length report is compared with the planned chunk sizes per kind; any change to the
      chunking settings is recorded here for the build (ticket 17).

## Comments

- 2026-10-26, author's S4 ruling: the corpus grows from 27 to 28 own documents, adding one incident record for Olivia's unexpected authentication approval. Follow the S4 evidence requirements in the spec: distinguish sign-in observations, her later statement and responder assessment; align UTC times; preserve unknowns. Use the document ID reserved by T12. Do not describe the event as prompt flooding, phishing-proxy compromise or token theft without supporting evidence.

- 2026-10-26, superseding the S4 ruling above: the author deferred the expanded authentication-attack story as premature for this phase. Restore the 27-document plan; no additional S4 incident record or email, web or SIEM evidence is required. S4's authentication explanation is open again on T12.

- 2026-10-26, final S4 ruling: the question is settled as intentional uncertainty, not a missing incident story. Keep the 27-document plan. Do not invent Olivia statements or S4-specific proof of authorisation, compromise or an authentication-attack mechanism. See the spec's S4 ruling.
