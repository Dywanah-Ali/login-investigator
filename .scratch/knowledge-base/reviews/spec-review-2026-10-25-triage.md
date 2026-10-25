# Triage of Codex's spec review, 25 October 2026

- **Review triaged:** `spec-review-2026-10-25-codex.md`, against `spec.md` at commit `8a678d8`.
- **Triaged by:** Claude, in a fresh session, so the spec's author did not judge findings alone.
- **Method:** each finding checked against the source it cites (tickets, research notes, map,
  glossary, register) and, for code claims, the real files.

## Verdicts

"Fix" means the spec lost or misstated what its source says. "Ruling" means the fix changes an
agreed decision, so the author decides.

| ID | Verdict | Kind | Evidence |
|---|---|---|---|
| R1 | Agree; major rather than blocker, since the fix stays inside the check | Ruling | Ticket 06 comment of 24 October 2026 prescribes counts only |
| R2 | Agree | Ruling | Spec lines 626–627 and 640–641 against lines 468, 629, 637–639 |
| R3 | Agree | Fix (restore T06 d9's re-score and re-run clauses), plus a ruling on the new acceptance condition | T06 d9; research note 03, section 3.7, stage A |
| R4 | Agree, and wider: every user has a laptop link, so the allowed list protects nobody | Ruling, with N1 | Ticket 06 comment, line 122; T04 d2 |
| R5 | Agree | Fix | Map, Notes, evaluation stance |
| R6 | Agree | Ruling | AUD-036 closes on one eval run visible in Langfuse |
| R7 | Agree | Fix | T06 d6, Cohen's kappa once labels exist |
| R8 | Agree | Fix | Ticket 04, conditions, line 95 |
| R9 | Agree; recommend phase 1 | Ruling | Ticket 05 hand-offs, lines 95–98, against spec ruling 6 |
| R10 | Agree; the ruling stands but its recorded reason is wrong | Fix, including the decisions-log reason | `backend/evals/scoring.py:44` reads only S5's text; `:144` reads patterns from the question file |
| R11 | Partly: the spec says two things (story 66 refuses to start; API change 5 joins the startup failures, which today start with an error) | Ruling | `backend/api/services.py:58–67`; `backend/tests/test_api_startup.py:71–78` |
| R12 | Agree | Fix | `backend/login_investigator/reputation.py:57` |
| R13 | Agree | Fix | `GLOSSARY.md`: Investigation avoids "Conversation"; no Dataset entry |
| N1 | New, found in triage: "used address" edges (T08 d6) have no source table in the integrity check; every network node is lonely and fails the check on day one | Ruling, with R1 and R4 | Ticket 06 comment, line 118 lists three link tables only; T08 d6 and its `graph` draft |

Not covered by Codex: the `fold:` prefix and `members` for collapsed graph nodes, which the spec
put in front of Codex at review. Still open.

## Author's rulings

| # | Findings | Ruling | Reason |
|---|---|---|---|
| 1 | R1, R4, N1 | Option A. The integrity check compares identities, not only counts: every edge must match its source row by both ends and type. "Used address" edges are built from the log and checked against the log. A chunk may have zero `mentions` edges when its text names no entity, as long as its edges equal the extracted mention set. No isolated node is allowed for people, groups, assets and devices. | Standard reconciliation practice: a count is necessary but not sufficient (data-migration guides; knowledge-graph testing guides call counts a tripwire). The log is already the truth for who signed in from where, so a second copy could drift. |
| 2 | R2 | Option A. The gold items choose the checks: gold chunk IDs get the two document-retrieval checks; gold record IDs get the exact-set graph check; a mixed question gets both. A say-no question may carry an empty gold evidence set, but must state its expected verdict and keeps every other applicable check. The provenance line stays mandatory. | The marking follows what the question contains, so no type label has to be kept in step with the gold items. |
| 3 | R3 | Option A. A retrieval setting can win the on-versus-off comparison only if the say-no checks also pass with it. If the re-ranker off cannot produce `none` correctly, it stays on and the reason is recorded. Separately, as a fix: T06 d9's re-scoring of the tuning file with the remaining score source, and its re-run per phase and when the corpus changes shape, are restored. | With the re-ranker off, the empty-result rule never fires on a non-empty corpus, so a tie going to off would silently remove the refusal path. The verdict is computed in code, so the check costs no model call. |
| 4 | R6 | Option A. Deterministic checks with a fake Langfuse destination, at the existing doors: the JSON result written before any upload, an upload failure reported loudly in the summary, the masking hook applied, human labels returning only through the export script. One real eval run visible in Langfuse is the live acceptance evidence, as AUD-036's closure says. No new door. | Switched-off tests prove the app works without Langfuse, not that each promise made about it holds when it is on. |
| 5 | R9 | Option A. The core computes the finding ID in phase 0; the Alerts reply gains `finding_id` in phase 1, with the screen column that shows it. The build table moves to match. | Spec ruling 6 puts API additions in phase 1; nothing in phase 0 reads the field, and the API returns only what a screen needs. |
| 6 | R11 | Option A. A stale database stops the server from starting, with one fixed message naming the build command. The spec's comparison to today's invalid-log behaviour is removed, and API change 5 is reworded so it no longer reads as the start-with-an-error pattern. | Keeps spec ruling 8 and user story 66. The simplest guarantee that nothing answers from an old world; the start-with-an-error pattern would need every endpoint to know whether it is safe to answer. |

## Lesson

The integrity check was added to ticket 06 on 24 October 2026 after the ticket's research, and was
designed in conversation with no check against practice. A build item added after a ticket's
research needs a quick check against practice before it is agreed.
