# Improvement audit register

Created: 18 October 2026. Last reviewed: 19 October 2026.

This is the maintained register of improvements, unresolved concerns and future capabilities
identified during the project review. It records what needs attention, why, and the evidence
needed to close it. It is a documentation audit of the conversation and repository records,
not a fresh security assessment or a new round of research.

Recording an item does not authorise implementation. The agreed spec and implementation tickets
still control scope. Ticket 19 is resolved by author acceptance on 19 October 2026, P-110.
Ticket 26 is unblocked but not started. Remaining items are optional future work and do not
block the accepted course demo.

## Maintenance rules

- Add new findings here during future reviews. Keep stable IDs and never reuse them.
- Distinguish author-approved direction, proposed work, unresolved defects and future ideas.
- Link the original prompt, bug or ticket. Do not copy secrets or personal configuration details.
- Before building, agree scope and acceptance with the author and create or link a local ticket.
- Update status, date and evidence when an item changes. Preserve prior decisions in the change log.
- Close items only on relevant evidence and author review. Keep closed entries for traceability.
- Bug details remain in [the bug log](../bug-log.md). Build prompts remain in
  [the prompt log](../prompt-log.md). Do not use this register as a competing spec or bug log.
- Review this register at session start alongside the map. Read the entries relevant to the work.

Priorities below are suggested planning order, not security severity scores or promised dates.
High means investigate first because correctness or security may be affected. Medium means a
useful product or maintenance improvement. Low means refinement. Unranked means design is needed.

## Open register

| ID | Item | Status | Suggested priority | Source |
| --- | --- | --- | --- | --- |
| AUD-001 | Filter Alerts by rule | Closed: author approved live review | Medium | P-038, P-044, P-115, P-116; ticket 26 |
| AUD-002 | Add default rule severity to Alerts | Closed: author approved live review, Option A | Medium | P-044, P-114 to P-116; tickets 25 and 26 |
| AUD-003 | Let the user define the report's scope after a branching conversation | Deferred by author, design needed | Medium | P-056 |
| AUD-004 | Expand investigation tools and evidence capabilities | Deferred by author, scope needed | Unranked | P-052 |
| AUD-005 | Distinguish attempted attacks from suspected compromise in answers | Open concern, cause not investigated | High | B-056; P-055 |
| AUD-006 | Review frontend dependency advisories | Open maintenance concern | High | B-017 |
| AUD-007 | Investigate incomplete answer streams | Open reliability concern | High | B-041; ticket 18 |
| AUD-008 | Correct stale Alerts presentation prose in API contract | Open documentation concern | Low | B-047 |
| AUD-009 | Resolve existing frontend lint warnings | Open maintenance concern | Medium | Parity evidence |
| AUD-010 | Review frontend bundle size | Open performance concern | Low | Parity evidence |
| AUD-011 | Extend backend type checking to copied files | Deferred until after Parity | Medium | Ticket 21; backend configuration |
| AUD-012 | Align editor Python environment with command-line checks | Previously recorded, current state unverified | Low | Ticket 21 comments |
| AUD-013 | Decide and configure project Python linting | Previously recorded, current state unverified | Low | Ticket 21 comments |
| AUD-014 | Automate agreed project checks | Previously recorded, current state unverified | Medium | Ticket 21 comments |
| AUD-020 | Distinguish whole-investigation recall from the latest account focus | Author clarified missing accounts; narrowing observed, cause partly inferred | Medium | P-058/P-059; B-060 |
| AUD-021 | Report prompt-injection evidence consistently | Open defect against existing instructions | High | B-057; P-058 |
| AUD-022 | Ensure required investigation searches are completed | Closed: author approved | High | B-058; P-058 |
| AUD-023 | Enforce chronological report timelines | Closed for new reports: author approved | Medium | B-059; P-058 |
| AUD-024 | Provide an in-app theme selector | Accepted in author theme review; Alerts header adjustment tracked separately | Medium | B-061; P-061 to P-063 |
| AUD-025 | Distinguish Alerts header from selected alert in both themes | Closed: author approved | Low | B-063; P-063/P-064 |
| AUD-026 | Review Investigation history navigation against v1 | Closed: author approved | Medium | B-064; P-073 |
| AUD-027 | Keep tool-progress activity observable during fast event bursts | Closed: author approved current behaviour | Medium | B-065; P-082 |
| AUD-028 | Explorer test timeout during concurrent checks | Rerun passed, cause unresolved | Medium | B-066; P-086 |
| AUD-029 | Correlate end-to-end scenario rulings with the saved Investigation | Closed: consolidated case verified and approved | High | B-067; P-100/P-107 |
| AUD-030 | Exclude the initial event from later-sign-in prose totals | Open counting defect | High | B-070; P-107 final benchmark |

### AUD-001: Rule filter

The author wants to focus the Alerts table on a rule such as Brute force. Offer All rules and
only the four existing categories. Compose with existing filters, preserve meaningful URL state,
reset paging and handle empty results. No additional detectors are approved by this item.

Implementation and closure belong to
[ticket 26](../../.scratch/v2-port/issues/26-alert-rule-filter-default-severity.md).
Its API contract and screen treatment must be agreed before implementation.

### AUD-002: Default rule severity

The author approved these review-priority defaults following
[research ticket 25](../../.scratch/v2-port/issues/25-login-alert-severity.md):

| Rule | Approved default |
| --- | --- |
| Brute force | Medium |
| Password spraying | Medium |
| Success after repeated failures | High |
| Sign-in from a new country | Low |

Use visible severity words and an agreed accessible colour treatment. The core owns the policy;
the API supplies it to the screen. These defaults are project choices, not industry-mandated
scores or proof of compromise. A failure-only finding does not establish that no related success
occurred elsewhere. The existing report assesses the investigation differently. Agree the
explanation for differences, particularly Low new-country alerts versus the report's current
Medium criterion, before shipping. Do not silently alter the report prompt or grader.

Closure uses ticket 26's checks and author review. Evidence is in the
[research note](../../.scratch/v2-port/research/25-login-alert-severity.md).

20 October 2026: the author chose Option A (P-114) and approved the
[design note](../../.scratch/v2-port/research/26-design-note.md) (P-115). Built on branch
`ticket-26-rule-filter-severity` with 413 backend and 149 frontend tests passing. AUD-001 and
AUD-002 close on the author's live review.

Closed 20 October 2026: the author reviewed the live screen and approved (P-116). Merged into
`main` locally; not pushed.

### AUD-003: Report scope and user intent

The current report was accepted in live review. The author noted that a conversation may explore
several directions before a report is needed. A future report should be guided by what the user
actually wants it to cover, rather than assuming every conversational branch belongs in it.

Design questions remain: how the user specifies the subject, time window, relevant findings and
intended audience; when clarification is useful; and how scope is shown before generation.
These are questions to settle, not approved fields or a prescribed new popup flow.

Proposed closure evidence: a conversation covering multiple subjects produces a report about the
selected subject; excluded branches are not mixed into its conclusions; claims remain grounded;
the saved report and PDF agree. Agree the interaction and API contract before implementation.
No current report-schema, prompt or generation change is authorised by this entry.

### AUD-004: Richer investigation tools

The author accepts tool output within today's implemented capabilities and wants richer insight
in the future. More capability needs stronger evidence, not just more confident prose. The
specific new searches, correlations, data sources or detectors have not been selected.

First identify concrete investigation questions that today's tools cannot answer. Then agree
inputs, outputs, limitations and meaningful evaluation cases for each selected capability.
Keep core logic independent of screens and preserve the read-only tool boundary.
Perplexity is a Codex development research tool. Adding it to the application's investigator is
not approved. The current log lacks context such as MFA, asset criticality and post-login activity;
do not imply those facts can be inferred from the existing fields.

### AUD-005: Compromise wording

The supplied answer to “Was any account compromised this week?” opened with an affirmative about
suspicious activity and mixed failed attacks with successful sign-ins. This can leave the user
unclear about attempted attacks versus suspected account access. See B-056 for the exact concern.

Investigate the cause before choosing a fix. Proposed acceptance: answers distinguish failed
attempts, observed successful access and remaining uncertainty. Reputation is supporting context,
not sufficient proof that a session was attacker-controlled. Changes to prompts or evidence
interpretation need regression checks and explicit evaluation review. No fix has been made.

### AUD-006: Dependency advisories

B-017 recorded seven high-severity package advisories in the existing frontend dependency tree.
This is a recorded install/audit result, not a claim that seven remotely exploitable application
vulnerabilities have been demonstrated. The dependency chain and advisory are preserved there.

Recheck the installed lockfile, assess actual exposure and choose supported upgrades. Avoid an
unreviewed automatic major-version update. Close with an updated audit result, relevant application
checks and a documented explanation for any residual findings.

### AUD-007: Incomplete answer stream

One of 57 benchmark attempts failed or ended without the required completion event. The benchmark
still passed at 56/57 overall and 15/15 security. The failure remains counted; its cause is unknown.

Investigate with diagnostics that do not expose credentials or raw provider details. Establish a
reproduction or evidence of cause before selecting a remedy. Validate failure handling and the
chosen remedy. Do not hide the failure through retries or rewrite the accepted benchmark history.

### AUD-008: Stale API contract prose

The contract still describes a per-rule count line removed from the Alerts page. B-047 records the
mismatch. Update the explanatory prose to match the approved screen, checking nearby examples.
The JSON response is not known to be wrong. This does not authorise removing response fields.

### AUD-009: Frontend lint warnings

The latest frontend checks retain six warnings: two table/library compatibility warnings, three
shared-component export warnings and one mobile-hook state/effect warning. Review each in a
separate maintenance change. Close on a clean relevant lint result and preserved behaviour;
do not suppress warnings simply to reduce the count.

### AUD-010: Bundle size

The latest production build warns about a main JavaScript chunk of approximately 1,081 kB before
gzip and 330 kB after gzip. This is a build warning, not a measured user-performance failure.
Measure loading and inspect dependencies before selecting splitting or other changes. Record
before/after results and check navigation and chat/report behaviour after any optimisation.

### AUD-011: Type-checking coverage

Copied files still appear on Pyright's explicit ignore list. Ticket 21 deliberately deferred their
cleanup until after Parity. The current configuration lists 13 files; ticket 21's original evidence
records 14 at that earlier point. A green current check does not mean all copied files are checked.

Work file by file. Remove an entry only when it passes checking and relevant behavioural tests.
Never extend this exception list to new code. Preserve the frozen sibling v1 project.

### AUD-012 to AUD-014: Development tooling

Ticket 21 recorded editor environment mismatch, unconfigured project Ruff and no automated check
runner. These historical observations have not been revalidated in this audit. Verify the current
state before treating them as defects or implementing changes.

| ID | Proposed closure evidence |
| --- | --- |
| AUD-012 | Editor uses the intended backend environment and agrees with the command-line checker on a representative file. |
| AUD-013 | An agreed project lint configuration has a documented command and a reviewed baseline. |
| AUD-014 | Agreed checks run automatically in the selected workflow and a deliberate failure is detected. No publishing or deployment is implied. |

### AUD-020: Answer completeness versus stored memory

Read-only review of the user-linked Investigation found five saved turns, including Daniel's
later GB sign-ins and the report. The final unnamed-account question was answered about Daniel
and the attack but omitted his later successful sign-ins. This supports account-reference recall;
it does not demonstrate loss of stored history. A general summary question does not unambiguously
require every event, so the desired completeness and the user's specific concern need clarification.

Compare saved evidence, the context supplied to the model and the requested answer scope before
choosing a fix. Do not equate a fact missing from an answer with a fact missing from storage.
No model replay, conversation mutation or comprehensive memory-reliability claim was made.

Author clarification, P-059: the missing information is the other accounts, not merely Daniel's
later sign-ins. The author reports the same Daniel-only answer in different conversation histories.
Only the linked history has been inspected; that repetition across other histories is not independently
verified. Its initial question covered all accounts, then a named Daniel follow-up narrowed focus.
The existing prompt explicitly resolves follow-ups to the last answer's single user/IP. That is a
plausible contributor, not proof of the model's internal reasoning. The shared synthetic dataset
also makes recurrence of the same prominent account plausible; recurrence alone does not prove
cross-Investigation memory leakage.

Desired review behaviour: distinguish the whole case from a specific-account follow-up. A case-wide
recap should distinguish Daniel's suspicious success, Olivia's new-country success and the 35 spray
targets whose finding contains failed attempts. Do not label every targeted account compromised.
For an ambiguous singular question, make the chosen scope explicit or clarify it rather than silently
presenting one account as the entire case. Agree wording and scope before changing the prompt.
Check isolated histories with different account subjects as well as multi-account recaps. The existing
isolation test checks storage separation, not model interpretation of this live phrasing.

Isolation investigation, P-060: reviewed the nine saved Investigation records and compared the
three histories containing the repeated recap question. Each already contains Daniel in its own
evidence or report before the recap. The real-route/agent/checkpointer probe captured seven model
inputs and two report inputs across three temporary cases, including alternating follow-ups and
restart. No other case's unique marker appeared. Three existing backend and two frontend navigation
checks pass. This supports shared-data recurrence and scope narrowing, not history leakage in the
tested flow. Keep this recap item open; no semantic fix was made. Details and repeatable offline
probe: [conversation isolation investigation](conversation-isolation-2026-10-18.md).

Scenario reference check, P-098 on 19 October 2026: author confirmed the exact question
“Did that user sign in from anywhere else afterwards?” identifies Daniel, returns both expected
later GB sign-ins and performs a new search in the same Investigation. This closes the scenario's
singular-reference check. AUD-020 remains open for whole-case versus recent-account recap scope.

P-105, 19 October 2026: read-only saved-result verification now establishes the exact unnamed
question in case 9f06429702864efca91a6fab8f7c1517 turn 6. It identifies Daniel and returns both
expected later GB events, grounded in the case's earlier turn-3 search. No new tool call. This
supports this singular-reference case, without resolving AUD-020's whole-case recap concern.

### AUD-021: Prompt-injection reporting

B-057 records injection-bearing tool evidence that the relevant answers and report did not flag,
despite existing instructions. This is a warning omission, not demonstrated obedience to the
injection. Investigate and agree a remedy; validate both resistance and explicit reporting using
representative evidence. Preserve original log text as untrusted data. No prompt fix is implemented.

### AUD-022: Required searches in broad investigations

B-058 records three required per-IP searches missing from the initial broad investigation. The
agent called detection and reputation tools, but did not complete the instructed sign-in searches.
Decide how much should be enforced by the workflow versus requested in the prompt. Changes to the
agent architecture need author agreement. Acceptance should check actual calls and grounded
conclusions, including success checks beyond failure-only findings.

P-107 authorises the deterministic fix. A standard before_model middleware now schedules
missing whole-IP searches for actual current-turn detection findings before another model call.
It avoids repeated completed attempts, including failures, and never interprets log text as
instructions. Existing read-only tools and create_agent remain. Offline real-agent tests and
initial overnight benchmark attempts pass; final suite/benchmark and author review pending.

P-108 closes AUD-022/B-058 after author review of the consolidated case, supported by 393
backend tests, clean Pyright and final 56/57 API benchmark with all security checks passing.
The scope-regression iteration is retained as B-069; its correction is also accepted.

### AUD-023: Chronological report timeline

B-059 records a saved timeline with an older event after newer events. Agree validation or ordering
at the appropriate core boundary and a meaningful regression case. Keep saved-report and PDF
presentation consistent. Do not silently rewrite historical reports as part of diagnosis.

P-099, 19 October 2026: author approved chronological order in the new scenario report.
This is acceptance of that instance. It does not demonstrate enforced ordering or repair the
historical saved report, so AUD-023/B-059 remain open.

P-107 authorises sorting newly generated timelines before save/return with parsed aware
timestamps. Returned card data, saved report and PDF now share that sorted list. Invalid new
timestamps refuse saving. Historical reports remain untouched. API regressions pass; full-suite
verification and final author review pending. B-059 retains the original unordered examples.

P-108 closes AUD-023/B-059 for newly generated reports after author review of the ordered
report and matching PDF. Historical reports remain unchanged. Regression evidence includes
returned/saved/PDF consistency and invalid-timestamp handling.

### AUD-024: In-app theme selection

The author found no way to switch themes when asked to review them. The original app followed
only the operating-system preference. At the author's request, add a shared header selector with
Light, Dark and System. System stays the default; a local preference persists across reloads and
pages. Explicit choices override system changes. System follows live changes. Browser storage
failure must not prevent switching during the current session.

Implemented using the existing shadcn/ui Select, a shared React provider and existing colour tokens.
A trusted startup script applies the saved setting before first paint. Native controls use the
matching CSS colour scheme. No new dependency or backend field. On narrow screens, the capture
timestamp is hidden to leave room for navigation, the synthetic-data badge and theme selection.
Keyboard, persistence, system updates, storage failure, tab synchronisation, navigation and startup
behaviour have focused checks. Implementation is ready for the author's live visual review;
this entry does not mark readability of every screen in both themes as accepted.

Author feedback on 18 October 2026: “so far so good” (P-062). The control works in the initial
review; this does not establish readability of every screen in both themes.

References: [shadcn/ui Vite theme pattern](https://ui.shadcn.com/docs/dark-mode/vite) and
[Tailwind dark mode and startup application](https://tailwindcss.com/docs/dark-mode).
Context Hub supplied the Tailwind v4 guide; no directly matching shadcn dark-mode entry was found.

Author review, P-063: other reviewed theme appearance is accepted. The sole remaining header-tone
adjustment is tracked separately as AUD-025. This supersedes the initial pending theme review.

### AUD-025: Alerts header tone

The author found the column header too similar to the selected alert in both themes. Darkened
only that header using the existing muted token, preserving selection cues and column text.
The noninteractive header no longer inherits the body-row hover tint. Other tables are unchanged.
Implemented as a styling-only correction. The author approved the updated header on 18 October
2026 with “good” (P-064). Closed with 14 passing Alerts tests, a passing build/type check and the
author's visual ruling. The existing bundle warning remains separate.

### AUD-026: Investigation history navigation

Author reports a difference from v1. Read-only comparison confirms missing Show fewer,
different handling of older selected cases and no equivalent list-reveal animation.
See B-064 for mechanisms and scope boundaries. Clarify the author's actual concern before
choosing a fix or changing the agreed screen design. Previously accepted next-day saved-history
recovery remains accepted; navigation parity is a separate concern.

Author confirmed the list differences and arrow controls (P-074). Implemented arrow-only expand
and collapse, continuous groups of three around the selection and reduced-motion-aware reveal.
Collapse retains the selected case and is disabled when shortening would hide it. All 136 frontend
tests, build/type check pass; six existing lint warnings and bundle warning remain. Live author
review is pending; B-064 retains implementation evidence.

Author approved with “yes all good” on 19 October 2026 (P-075). AUD-026/B-064 are closed.
No additional application changes were needed after the passing checks.

### AUD-027: Tool-progress visibility

Author did not see the reputation progress phrase despite a saved lookup. B-065 records an
offline reproduction: two tool events in one chunk overwrite the first visible status. This
is a confirmed mechanism, not a captured explanation of the author's exact live timing.
Proposed remedy: retain distinct tool-activity phrases in a short in-chat list during answering,
cleared on completion, cancellation, navigation or a new request. Agree treatment before UI edits.
Per-tool progress presence remains open in ticket 19. No model replay or application edit yet.

Author rejected the cumulative list (P-084). Retain a single changing line. Official-doc and
installed-source research plus three offline probes support genuine execution lifecycle events.
Public callbacks with custom stream events fit the existing sync path; installed v3 event
streaming is experimental. Contract and screen agreement still precede implementation. No
promise that a near-instant cached lookup's status will be perceptible. See
[research note](../../.scratch/v2-port/research/27-tool-progress-lifecycle.md), P-085 and B-065.

P-086 authorised implementation. The contract/spec were recorded before code. Per-invocation
callbacks now drive tool lifecycle events with only name, opaque ID and phase. The single-line
frontend tracks active IDs, handles overlap/duplicate tool names, and clears completed activity.
Five framework lifecycle tests, an HTTP privacy test and all 141 frontend tests pass. Final
backend-suite/type-check evidence is recorded in Parity closing. API restarted for review;
all 12 saved Investigation IDs are unchanged. Author live acceptance remains pending.

P-087: author reports mostly Thinking with brief unreadable tool flashes even for four calls.
Local warmed-tool probe confirms millisecond-scale execution; this does not capture the exact
live stream. Tracking accuracy is not accepted as sufficient readability. Proposed next step:
retain the last finished activity in past tense within the same line while preparing the response;
replace it on another tool start or first answer text. Agreement pending; no new UI code.

P-088 held that proposed refinement while discussing execution time versus dataset size.
P-089 requested an isolated live lookup. One uncached 1.1.1.1 query to AbuseIPDB returned in
0.477 seconds; the real lifecycle adapter emitted correlated start/end events. Fixed fake model
and in-memory checkpoint isolated the lookup from paid model calls and saved app history.
This is one network sample, not evidence of browser visibility. Final live presence ruling and
any further display change remain open.


P-092 explicitly approves the current single-line lifecycle display, accepting brief cached-call
visibility after the positive multi-IP test. AUD-027/B-065 are closed with the automated checks,
isolated real API timing and dated live ruling. Further display proposals remain unimplemented.
The final presence item is now accepted; the scenario and other audit findings remain separate.

### AUD-028: Explorer test timeout

One full frontend verification run timed out in the existing valid-IP/Reset Explorer test.
The other 137 tests passed. A one-worker rerun of Explorer and Investigator passed all 35 tests
without code or timeout changes to Explorer. Cause remains unconfirmed; concurrent host load is
plausible. B-066 retains the original failure and rerun evidence. The final one-worker
full-suite rerun passed all 141 tests, recorded with P-086. No unrelated application fix is authorised here.

### AUD-029: Scenario case identity and end-to-end evidence

Author approved the report and PDF, but inspected default saved memory does not yet match the
reported exact follow-up/report sequence. No data-loss or failed-execution claim is established.
Requested the current Investigation URL to check the correct live case and data location.
Next-day acceptance also identifies a different prior case. Preserve individual dated rulings,
but hold aggregate end-to-end acceptance until case identity and same-case continuity are
resolved. B-067 records the read-only observations. No mutation, model replay or implementation.

P-101 supplied `90c317b74bb94e2b9d066e2515da5d1f`. Live API and store agree: this is a
weekly-compromise case with opening answer and report, detection plus three reputation lookups,
no sign-in searches and no unnamed follow-up. Its report timeline is unordered. This also
reproduces AUD-022/B-058 and AUD-023/B-059. No history-loss evidence. Reopened scenario items
2/4/6/7 while retaining dated author feedback. Asked whether another case was used for the
follow-up. The exact overnight scenario and same-case continuity remain unproven.

P-103: searched all 16 saved cases and 31 turns. Two related named-account questions exist
in 9f06429702864efca91a6fab8f7c1517 turn 3 and 872227a3ca7948748f7b4f1ec57ee6c3 turn 4,
each with a search and the two expected later GB IPs/timestamps. Exact unnamed wording absent.
This narrows the gap to the actual unnamed-reference test and same-case scenario continuity;
the related history is present. No further manual case hunt is required from the author.

P-105: exact unnamed question now verified in the identified saved case, turn 6. Correct
account and both expected GB events, grounded in turn-3 search. Zero new tools; this verifies
recall, not a fresh-search or one-case overnight scenario. That narrower reference gap is
resolved; AUD-029 stays open for the remaining scenario conditions. No forced redundant lookup.

P-108 closes AUD-029/B-067: consolidated case ba63f90e8f6f465a9633817b8c898abb correlates
steps 1–7, exact wording, actual searches and ordered report/PDF, accepted by the author.
The same case still needs next-day continuation on 20 October as a separate acceptance gate.

### AUD-030: Later-sign-in totals

Final API benchmark 7ff8e5ae Q07 run 1 lists two correct later GB sign-ins but claims three
successful sign-ins after the initial one. Its user search starts inclusively at the initial
success, so the returned count also includes that event. Both later IPs/timestamps and the
required user search are present; this is a counting/wording defect. Keep the attempt failed.
Q07 runs 2 and 3 pass; overall 56/57 and security 15/15 meet the agreed threshold. B-070 records
exact evidence. No fix or grader change in the two-fix scope. Agree a robust boundary/counting
remedy and regression evidence before implementation.

## Longer-term capabilities already named in the spec

These are future ideas, not approved implementation work. Each needs its own scope, design and
acceptance criteria. See the [spec](../../.scratch/v2-port/spec.md), future seams and Out of Scope.

| ID | Capability | Existing architectural seam | Status |
| --- | --- | --- | --- |
| AUD-015 | Retrieval-augmented generation | Central tool list | Future idea |
| AUD-016 | Knowledge graph | Data access in the core | Future idea |
| AUD-017 | Tracing | One model/agent creation function | Future idea |
| AUD-018 | Evaluation-platform integration | Evals call core or API independently of screens | Future idea |
| AUD-019 | Log upload | Dataset abstraction at the API/core boundary | Future idea |

## Review decisions to preserve

| Topic | Decision and evidence |
| --- | --- |
| Overview attention cue | Accepted: green at zero alerts and amber above zero. Positive alerts are not automatically confirmed incidents. P-036/P-037, B-043. |
| Alerts captions | Accepted: total count only above the table; redundant footer summary removed. P-038/P-045, B-044. |
| Explorer captions and severity | Caption cleanup accepted. Keep raw events neutral. Failed does not mean malicious and successful does not mean safe. Raw-event severity was discussed, not approved. P-046/P-047, B-048. |
| Investigator initial state | Empty layout accepted. This alone does not establish functional correctness. P-048. |
| Progress and keyboard | In-chat progress, Enter to send and Shift + Enter for newline accepted. P-049 to P-051, B-049/B-050. |
| Tools evidence and reveal | Current capability accepted. Animated opening and scoped following accepted. Preserve reduced-motion handling and cancellation on manual interaction. P-052 to P-054, B-052/B-054. |
| Conversation continuity | Author accepts memory. Supplied named-account follow-up matches both expected later sign-ins. It does not isolate unnamed-reference recall or reopening persistence. P-055. |
| Current report | Author says it is good. Report-intent enhancement deferred as AUD-003. This is not a PDF or persistence ruling. P-056. |
| Research-tool boundary | Keep Codex research credentials separate from app configuration. No Perplexity tool added to the app. B-045/B-046 retain the setup iterations; never reproduce key values here. |

The deliberately fake key-shaped security-test string was accepted as a scan exception. It is not
a live credential or an outstanding product enhancement. The existing security-test boundary stays.

## Acceptance outcome

Ticket 19 closed on 19 October 2026, P-110. The author explicitly accepted the course demo
and approved the remaining scope. The additional next-day continuation check for the same
consolidated case was waived, not performed. Earlier persistence evidence remains valid
within its recorded scope. See [Parity closing](../parity-closing.md).

No mandatory acceptance checks remain. Open defects and improvement ideas keep their status
and evidence here for optional future work, including B-070/AUD-030. Closure does not claim
that these issues were fixed. Historical pending acceptance notes below are superseded.

## Change log

| Date | Change | Evidence |
| --- | --- | --- |
| 2026-10-18 | Created maintained register AUD-001 to AUD-019. Carried forward discussed enhancements, unresolved concerns and existing future seams. Recorded current report acceptance with scope enhancement deferred. | P-056; linked tickets and bug log |

| 2026-10-18 | Recorded PDF acceptance; saved-Investigation and other unclosed scenario checks remain pending. | P-057 |

| 2026-10-18 | Added AUD-020 to AUD-023 after read-only review of a user-linked Investigation. Stored history is present; answer completeness, injection reporting, required searches and timeline order need separate assessment. | P-058; B-057 to B-059 |

| 2026-10-18 | Clarified AUD-020: author means omitted accounts and repeated Daniel focus across histories. Recorded scope narrowing as B-060; other histories remain uninspected. | P-059 |

| 2026-10-18 | Investigated suspected conversation mixing. Live comparisons and model-input boundary probe found no leakage in the tested flow. AUD-020 remains open for recap scope. | P-060; conversation isolation investigation |

| 2026-10-18 | Added AUD-024 after author requested an in-app theme control. Implemented theme selection; live appearance review remains pending. | P-061; B-061/B-062 |

| 2026-10-18 | Recorded positive initial theme-control feedback. Full both-theme visual review remains open. | P-062 |

| 2026-10-18 | Author accepted other reviewed theme appearance. AUD-024 accepted; sole Alerts header-tone correction tracked as AUD-025/B-063 pending final visual confirmation. | P-063 |

| 2026-10-18 | Closed AUD-025 after author approved the adjusted Alerts header. | P-064 |

| 2026-10-19 | Recorded author acceptance of saved Investigation reopening and next-day continuation. Other manual gates and audit concerns remain open. | P-071; Parity closing step 8 |

| 2026-10-19 | Registered history-navigation differences pending author clarification. | AUD-026; B-064; P-073 |

| 2026-10-19 | Implemented author-confirmed history-list treatment; visual acceptance pending. | AUD-026; B-064; P-074; 136 frontend tests |

| 2026-10-19 | Closed AUD-026 after author accepted restored history arrows and navigation. | P-075; B-064; 136 frontend tests and build/type check |

| 2026-10-19 | Registered missed tool-progress wording and reproduced burst overwrite; UI remedy proposed. | AUD-027; B-065; P-082 |

| 2026-10-19 | Cumulative activity list rejected; researched lifecycle events for the retained single status line. No implementation yet. | AUD-027; P-083 to P-085; research note |

| 2026-10-19 | Implemented execution-based progress after P-086; registered unrelated Explorer timeout with passing isolated rerun. | AUD-027/AUD-028; B-065/B-066 |

| 2026-10-19 | Author live review rejected progress readability; measured fast local tools and proposed a truthful past-tense single-line refinement. | AUD-027; B-065; P-087 |

| 2026-10-19 | Held display refinement and tested one real external reputation lookup: 0.477 seconds, correct lifecycle events, browser visibility still unverified. | AUD-027; B-065; P-088/P-089 |

| 2026-10-19 | Author reports multi-IP progress is “way better”. Retain current implementation and hold further display changes; final explicit ruling requested. | AUD-027; B-065; P-090/P-091 |

| 2026-10-19 | Closed AUD-027/B-065 and the final presence item after explicit approval of current progress, including the cached-call limitation. | P-092; Parity closing |

| 2026-10-19 | Exact unnamed scenario follow-up passed by author ruling. AUD-020 remains open for whole-case recap scope. | P-098; Parity scenario step 6 |

| 2026-10-19 | New scenario report accepted, including chronological timeline. AUD-023/B-059 stay open for historical defect and enforcement. | P-099; Parity step 7 partial |

| 2026-10-19 | Recorded PDF approval; aggregate scenario evidence cannot yet be matched to one saved case. Requested current URL. | AUD-029; B-067; P-100 |

| 2026-10-19 | Linked case identity verified through API/store. Missing searches/follow-up and unordered report require reopening scenario evidence; existing AUD-022/AUD-023 recur. | AUD-029; B-067; P-101 |

| 2026-10-19 | Searched all saved cases: found both named-account follow-ups with correct search results; exact unnamed-reference scenario remains unproven. | AUD-029; B-067; P-103 |

| 2026-10-19 | Verified exact unnamed recall and grounding in prior search. No new tool call; exact scenario continuity/fresh-search condition remains open. | AUD-020/AUD-029; B-067; P-105 |

| 2026-10-19 | Implemented missing-search policy and new-report ordering after P-107; initial regressions/type checks pass, full benchmark pending. | AUD-022/AUD-023; B-058/B-059/B-068 |

| 2026-10-19 | Final benchmark passes 56/57, security 15/15; narrow-scope regression fixed. Registered one remaining follow-up count contradiction without hiding its failed score. | AUD-022/AUD-023/AUD-029/AUD-030; B-069/B-070; P-107 |

| 2026-10-19 | Final scope-preserving revision passes all 393 backend tests and Pyright; API benchmark 56/57 overall, 15/15 security. Two fixes ready for consolidated author review; same-case next-day continuation pending. | P-107; AUD-022/AUD-023/AUD-029; Parity evidence |

| 2026-10-19 | Author approved consolidated fixes/case/PDF/layout. Closed AUD-022/AUD-023/AUD-029; same-case next-day continuation and final sign-off remain. | P-108; Parity evidence; 393 backend tests; 56/57 API benchmark |

| 2026-10-19 | Closed ticket 19 by explicit author acceptance of the course demo; waived remaining same-case next-day check. Open defects and enhancements retained for optional future work. No further implementation started. | P-110; ticket 19 Answer; Parity closure |

| 2026-10-20 | Built AUD-001 and AUD-002 under ticket 26 after the author approved the design note with Option A. Two-axis review findings fixed; lint stays at the six AUD-009 warnings. Awaiting author live review. | P-112 to P-115; ticket 26; 413 backend, 149 frontend tests |

| 2026-10-20 | Closed AUD-001 and AUD-002 after the author's live review; ticket 26 resolved and merged locally. | P-116; ticket 26 |
