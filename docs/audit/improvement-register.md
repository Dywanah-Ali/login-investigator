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
| AUD-012 | Align editor Python environment with command-line checks | Closed: backend import verified and author confirmed Pylance warning cleared, 31 October 2026 | Low | Ticket 21 comments; author editor check |
| AUD-013 | Decide and configure project Python linting | Closed: author-approved policy, pinned tool, reviewed baseline and tested commands, 31 October 2026 | Low | Ticket 21 comments; tooling ticket 01 |
| AUD-014 | Automate agreed project checks | Previously recorded, current state unverified | Medium | Ticket 21 comments |
| AUD-020 | Distinguish whole-investigation recall from the latest account focus | Author clarified missing accounts; narrowing observed, cause partly inferred | Medium | P-058/P-059; B-060 |
| AUD-021 | Report prompt-injection evidence consistently | Open defect against existing instructions | High | B-057; P-058 |
| AUD-022 | Ensure required investigation searches are completed | Closed: author approved | High | B-058; P-058 |
| AUD-023 | Enforce chronological report timelines | Closed for new reports: author approved | Medium | B-059; P-058 |
| AUD-024 | Provide an in-app theme selector | Accepted in author theme review; Alerts header adjustment tracked separately | Medium | B-061; P-061 to P-063 |
| AUD-025 | Distinguish Alerts header from selected alert in both themes | Closed: author approved | Low | B-063; P-063/P-064 |
| AUD-026 | Review Investigation history navigation against v1 | Closed: author approved | Medium | B-064; P-073 |
| AUD-027 | Keep tool-progress activity observable during fast event bursts | Closed: author approved current behaviour. Exception recorded 24 October 2026: the knowledge base's investigation tool stacks its five steps while running (ticket 07, decision 4); the Port's tools keep the single line | Medium | B-065; P-082; knowledge-base ticket 07 |
| AUD-028 | Explorer test timeout during concurrent checks | Reruns passed; recurring timeouts, cause unresolved | Medium | B-066; P-086; knowledge-base T10 |
| AUD-029 | Correlate end-to-end scenario rulings with the saved Investigation | Closed: consolidated case verified and approved | High | B-067; P-100/P-107 |
| AUD-030 | Exclude the initial event from later-sign-in prose totals | Open counting defect | High | B-070; P-107 final benchmark |
| AUD-031 | Replace gpt-4o-mini before its retirement on 14 January 2027 | Open, deadline-bound; no model chosen | High | P-121; OpenRouter service notice |
| AUD-032 | Move the agent's conversation memory from SQLite to the PostgreSQL checkpointer | Open, parked by the author; not in the knowledge-base initiative's scope | Low | Knowledge-base ticket 02, decision 9 |
| AUD-033 | Incremental sync of the knowledge base instead of a full rebuild per run | Open, future; phases 0 and 1 rebuild in full; trigger to reopen: a full rebuild takes too long or costs too much to run per change | Low | Knowledge-base ticket 02, decision 6 |
| AUD-034 | Check Intel-Mac wheels before recommending a native Python package | Open, process lesson; applied once in research note 03 (section 3.1) | Medium | Knowledge-base research note 02, section 3.8 |
| AUD-035 | Evaluate Cohere Rerank 5 (calibrated relevance scores) as a replacement for `rerank-v3.5` once OpenRouter serves it | Open, watch item; swap gated by the eval set | Low | Knowledge-base research note 03, section 3.5 |
| AUD-036 | Langfuse as the trace and eval-result store for the knowledge base; the author's three months of free access run 21 October 2026 to about 21 January 2027 | Decided, 23 October 2026 (ticket 06, decision 10): adopted to the full as a mirror behind a switch, repo files stay the source of truth; closes on one eval run visible in Langfuse | Medium | Author, 21 October 2026 |
| AUD-037 | Widen the planted attack scenarios beyond the five the Port ships (impossible travel, MFA fatigue, dormant account, after-hours privileged use, credential stuffing) | Open; the spray-to-privileged-success story is taken into knowledge-base ticket 04, the rest stays future | High | Author and Claude, 22 October 2026 |
| AUD-038 | Plant benign look-alikes that share a signature with an attack (travel, VPN change, new device, password reset burst, new joiner, scheduled scanner, authorised test) | Open; two or three look-alikes are taken into knowledge-base ticket 04, the rest stays future | High | Author and Claude, 22 October 2026 |
| AUD-039 | Richer log row signals (MFA result, device identifier, authentication method, target application, session identifier) and a longer baseline window | Open; the MFA column is taken into knowledge-base ticket 04, the rest stays future | High | Author and Claude, 22 October 2026 |
| AUD-040 | Structural escalation of the agent: the agent as a node in a parent graph with deterministic pre-steps, or a knowledge-base sub-agent (Dual-LLM) if the corpus ever becomes hostile | Open, future seam; knowledge-base ticket 05 chose the Port's middleware extended | Low | Knowledge-base research note 05, sections 3.1, 3.3, 3.5 |
| AUD-041 | Structured agent answer (text plus a list of citation labels) so the citation gate reads a list instead of parsing prose | Open, build-time option in phase 0 | Low | Knowledge-base ticket 05, conditions |
| AUD-042 | Injection-detector middleware (a classifier over inputs and tool results) as an added layer over the structural defences | Open, parked; trigger to reopen: the canary pass rate falls below 100% and the structural defences cannot explain it | Low | Knowledge-base ticket 06, decision 7 |
| AUD-043 | Show the faithfulness judge's reason on the screen | Open, parked; trigger to reopen: a measured agreement between the judge and the author's labels | Low | Knowledge-base ticket 07, decision 8 |
| AUD-044 | Sweep test databases left behind by a test run that was killed before its teardown | Open, parked; trigger to reopen: a leftover `li_test_` database is seen | Low | Knowledge-base ticket 09, spec review |
| AUD-045 | Preserve the attack type in a narrow spraying investigation | Open, deferred outside T10 | High | B-073; T10 Port eval Q08 run 2 |
| AUD-046 | Require reputation lookups in a broad compromise answer | Closed: knowledge-base T43, author accepted 26 October 2026 | Medium | B-074; T11 Port eval Q04 run 3 |
| AUD-047 | Preserve each spray source's success outcome and total in broad answers | Open: T14 and T19 safety-net recurrences; behaviour fix outside T19 | High | B-076; T12 Port eval Q02 runs 2 and 3; T14 Q02 run 3 |
| AUD-048 | Decide whether the finding ID reaches the agent's detection tool when ticket 32 adds it to the Alerts reply | Open, for ticket 32's builder | Medium | Knowledge-base T13 spec review |
| AUD-049 | Stop sending finding counts the Alerts screen never shows | Open, parked until the author reopens it | Low | Knowledge-base ticket 43 scoping |
| AUD-050 | Harden Q21's three-successes check, which can pass a wrong answer | Open, parked until the author reopens it | Medium | Knowledge-base ticket 43 spec review |
| AUD-051 | Teach the `RECOMMENDS` pattern imperative advice such as "please follow" | Open, parked until the author reopens it | Low | B-077; T43 Port eval Q19 run 3 |
| AUD-052 | Stop the agent flagging benign twin B2 (oliver.hayes) as possibly compromised | Open, for phase 1 (clearing documents, investigation tool) | Medium | Knowledge-base ticket 43, ruling 9 spec review |
| AUD-053 | Codex terminal question discoverability | Closed: live queued-question test opened and answered by the author | Low | B-081; author confirmation, 26 October 2026 |
| AUD-054 | Herdr inherited pane context can identify another project | Open workflow concern, deferred; explicit pane targeting used | Medium | B-082; 26 October 2026 read-only diagnostics |
| AUD-055 | Corpus checker cannot see invented names written in prose, or the no-technique-ID runbook trait | Closed: T16 scans for all three checks, then the author's approval of the 27 documents, 27 October 2026 | Low | Knowledge-base T15 spec review |
| AUD-056 | Keep MITRE's ATT&CK source references as metadata for provenance | Open, future enhancement; not in phases 0 and 1 | Low | Knowledge-base T16 ruling P3 |
| AUD-057 | Reclaim superseded successful knowledge-base build databases | Open, scheduled in knowledge-base T44 (phase 0 cleanup); ruling still needed | Low | Knowledge-base T17 build lifecycle |
| AUD-058 | The staleness fingerprint covers chunking settings, not chunking code | Open, scheduled in knowledge-base T44 (phase 0 cleanup); ruling still needed | Medium | Knowledge-base T18 spec review |
| AUD-059 | The build command reads `LI_DATASET_DIR` from `.env`; the app reads the environment only | Open: rule ruled 28 October 2026 (environment, then `.env`, then default); code alignment scheduled in knowledge-base T44 | Medium | Knowledge-base T18 standards and spec reviews |
| AUD-060 | VPN address meaning and address-reuse evidence limits | Closed: T19 decisions and verified grouped context, 28 October 2026 | Medium | B-091; T19 decisions 2 to 5 |
| AUD-061 | Intermittent test-database teardown privilege failure | Open; candidate for T44 | Low | B-094 |
| AUD-062 | Recover all required evidence for a compound retrieval question | Open; K04 candidate-coverage gap, for review before the knowledge-base retrieval gate closes | High | B-098; T22 first live run |
| AUD-063 | One reader for the OpenRouter key and usage, one test guard for `.env` | Open; candidate for T44 | Medium | B-101; T23 standards review |
| AUD-064 | What the re-ranker's assessment still needs: a kept-5 check and calibration evidence | Open; for T39 and T41 | Medium | T23 spec review; T23 first live run |
| AUD-065 | Investigation evidence persistence and storage growth | Open, deferred design; bounded T24 checks approved | Medium | Author discussion before T24, 29 October 2026 |
| AUD-066 | Review Q04's compromise-attribution check for long structured answers | Open review concern, deferred outside T24 | Low | T24 Port eval Q04 run 1; B-105; related B-078 |
| AUD-067 | Review the graph foundation against the application's intended direction | Closed on T49 development migration and parity evidence, 1 November 2026; T25/T27 released | High | Author discussion and approval, 30 October 2026; T02 and T24 |
| AUD-068 | Production readiness after the development-stage Neo4j migration | Open, deferred until production is proposed; not a development-migration blocker | High | T46 author-approved Community limitation and later Enterprise/readiness review |
| AUD-069 | Intermittent Explorer interaction timeout during T47 safety checks | Open observation; affected-file rerun passed, investigate if repeated | Low | B-113; T47 frontend safety net |
| AUD-070 | Consider Pydantic Evals for evaluation orchestration | Open, future option; defer adoption pending a concrete maintenance need | Low | Author and Codex discussion, 31 October 2026; official documentation linked below |
| AUD-071 | Inspect passage text by graph passage ID | Parked by the author; no implementation approved or added to T49 | Low | T48 learning walkthrough with the author, 31 October 2026 |
| AUD-072 | Neo4j graph-integrity test query returned unavailable during import cleanup verification | Open intermittent observation; T49 full graph checks passed, root cause unproven | Medium | B-124; 31 October 2026 import cleanup and follow-up |
| AUD-073 | VPN session allocation record, the missing evidence for address co-presence | Open, future idea for phase 3 (network facts); no dataset or scope change approved | Low | T25 gate session with the author, 1 November 2026; research note 25 |

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

31 October 2026, AUD-012 closed: `sqlalchemy.ext.asyncio` imports successfully under
`backend/.venv/bin/python` with SQLAlchemy 2.1.6. The author's terminal initially used the
repository-root `.venv`, a different environment. After selecting the backend interpreter in
VS Code, the author confirmed the Pylance warning disappeared. Backend Pyright was also clean
in the same session. No package reinstall or dependency change was needed.

31 October 2026, AUD-013 partial progress: the author approved a focused backend import cleanup
after the T48 learning walkthrough. Editor-bundled Ruff 0.17.3, restricted to `--select I --fix`,
fixed 102 import diagnostics across 76 Python files. A structural comparison against HEAD
confirmed only import ordering, grouping and spacing changes. The import-only check passes;
127 other diagnostics remain outside this work. Ruff's verbose output confirms default settings
are in use. No project lint configuration was introduced, so AUD-013 remains open. Backend
Pyright reports zero errors or warnings; frontend tests pass 150/150. Initial full backend
verification was interrupted after 373 passes and one graph query failure; its isolated rerun
failed at Neo4j startup readiness. On the author's follow-up, the diagnostic and normal focused
runs passed, followed by all 701 backend tests in 957.38 seconds. The import cleanup's
verification gap is resolved; B-124/AUD-072 retain the intermittent failure and unproven cause.
No paid agent evaluation ran because no prompt, tool contract or non-import logic changed.

31 October 2026, AUD-013 follow-up: the author chose documented exceptions at the 12 reviewed
`BLE001` handlers rather than disabling the rule across the project. Each now has a line-level
`noqa: BLE001` with its reason: safe error translation, continuing cleanup, preserving
cancellation, or recording failed evaluations. The nine affected Python syntax trees are
identical before and after the comment edits. Import and BLE001 checks pass; an in-memory
unapproved broad-catch example still triggers BLE001. The remaining baseline is 115 diagnostics.
The earlier 701 backend passes, 150 frontend passes and clean type checks remain applicable to
the unchanged executable code; no services were rerun for these comment-only changes.
Project lint configuration remains undecided, so AUD-013 stays open. Documentation: Ruff 0.17.3,
official [BLE001 rule](https://docs.astral.sh/ruff/rules/blind-except/) and
[line-level suppression](https://docs.astral.sh/ruff/linter/#error-suppression); checked the
rule-specific suppression syntax and confirmed it with the installed editor binary.

31 October 2026, remaining Ruff baseline reviewed at the author's request: 115 diagnostics
across 21 rule codes after the BLE001 exceptions. The following is a proposal, not an adopted
configuration or approval for behaviour changes:

| Group | Count | Reviewed finding and proposed treatment |
| --- | --- | --- |
| Style and simplification | 46 | Consider ignoring UP017, SIM117, SIM102, SIM113, FURB167, FURB162, FURB192, RUF007, RUF015, ASYNC115, C405 and B009. Existing spelling and structure are valid; no correctness defect established. A CLI-only preview leaves 69 diagnostics. |
| Imported pytest fixtures (F811) | 37 | All cases are fixture parameters shadowing imported fixtures in seven test files. Prefer explicit same-name import aliases over disabling F811. A stdin-only preview on test_corpus_search.py removed its seven warnings; no file changed. |
| Deliberate constructs | 25 | ISC004 (16): intentional joined strings, make grouping explicit with parentheses. B023 (5): callbacks finish before the next iteration, document or bind values explicitly. TRY004 (3): preserve existing validation error contracts with explained exceptions. PLE2502 (1): hostile control character deliberately tested, spell it as a Unicode escape while preserving the runtime value. Keep these rules enabled. |
| Small cleanup candidates | 7 | F401 (2): unused imports; RUF059 (1): unused binding; PLW1510 (3): make subprocess failure policy explicit after checking each caller; ASYNC210 (1): blocking localhost HTTP probe inside an asynchronous test. Review/fix separately rather than hiding these categories. No runtime failure established by this lint review. |

The review changed no Python or Ruff settings. Keep correctness checks and reviewed BLE001
exceptions; agree the proposed policy before implementation. Reference: Ruff 0.17.3 official
[F811](https://docs.astral.sh/ruff/rules/redefined-while-unused/),
[B023](https://docs.astral.sh/ruff/rules/function-uses-loop-variable/), and
[ISC004](https://docs.astral.sh/ruff/rules/implicit-string-concatenation-in-collection-literal/)
documentation, with local code inspection and non-writing CLI previews.

31 October 2026, author approved the proposal above and instructed implementation. Work is
recorded in [tooling ticket 01](../../.scratch/tooling/issues/01-ruff-policy.md). Ruff 0.17.3 is
pinned, the twelve style preferences are relaxed, and the other reviewed diagnostics are
resolved with explicit intent or small cleanup. Full-policy Ruff and backend types pass;
frontend 150 pass. Diagnostic probes confirm F821, BLE001 and B023 still detect new mistakes.
The final full backend run passed all 701 tests in 993.52 seconds, with no failures or teardown
errors. B-125 records a tooling error during suppression cleanup and its verified correction;
admin manual section 7 contains tested setup/check commands. AUD-013 is closed on the agreed
policy and verified baseline. The Python 3.12 target's TypeVar-style warning (UP047) and explicit
fixture-alias warning (PLC0414) have specific explained exceptions; no additional rule was
disabled project-wide. AUD-072 remains separately open and did not recur in this run.

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

**26 October 2026, knowledge-base T10:** recurrence with one frontend worker while the backend
suite and live API eval also ran: 144/149 passed; five Explorer tests hit the existing five-second
timeout. Explorer code and timeouts were unchanged. B-066 retains the failures. An isolated rerun
passed 149/149 tests after the backend suite and live eval finished, with no code or timeout
changes. The cause remains unresolved.

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

**26 October 2026, knowledge-base T10:** Q07 run 1 repeats the same two-listed/three-total
contradiction on the unchanged Port exam. Runs 2 and 3 pass; the full run meets its gates at
55/57 overall and 15/15 security. Evidence: `backend/evals/results/2026-10-25-221147-7ff8e5ae.json`.
No counting fix in T10; this item remains open.

### AUD-031: Model retirement

On 20 October 2026 the author shared an OpenRouter service notice: OpenAI's GPT-4o, GPT-4o mini,
GPT-4.1 and GPT-4.1 mini retire on 14 January 2027, and requests to them fail after that date.
The agent's model is `openai/gpt-4o-mini` (`MODEL` in `backend/login_investigator/agent.py`;
also named in `env.example`, the project rules and the spec's technical constraints). After the
deadline the Investigator stops answering; dashboards are unaffected.

A model change is a behaviour change, not a configuration edit. The agent's judgement is gated by
the eval set, so a replacement is accepted only on a full API-mode eval run against the agreed
thresholds (at least 90% overall, 100% for injection and refusal checks), with the old model's
results kept for comparison. The notice names two OpenAI replacements; they are not yet verified.
Choosing the model is the author's decision and changes the spec, so it goes through the spec's
decisions log. v1 uses the same model and will also stop answering; it stays frozen.

Closure evidence: a spec decision naming the new model, the code and documents updated, and a
passing API-mode eval run on the new model before 14 January 2027.

### AUD-032: Agent memory in PostgreSQL

The knowledge-base initiative (ticket 02, 20 October 2026) chose the author's installed
PostgreSQL as the knowledge base's one store. LangChain ships `langgraph-checkpoint-postgres`,
the PostgreSQL twin of the `SqliteSaver` the agent uses. Moving memory would put everything the
app persists in one store. The author ruled it out of the initiative's scope: it has no bearing
on phases 0 and 1 and the eval set does not cover memory. Closure evidence: a spec decision, the
checkpointer swapped in the one agent-creation function, conversation continuity re-verified.
Parking reaffirmed by the author on 22 October 2026 after ticket 05: both checkpointers
serialise messages through the same LangChain code, so the artifact round-trip check in phase 0
does not favour either store, and the switch would make PostgreSQL a requirement for opening a
conversation, which the Port's service-free tests avoid. **Trigger to reopen: phase 2
(history), when incident write-ups enter the graph and a past investigation becomes knowledge;**
reopen with the eval extended to cover memory.

### AUD-033: Incremental sync of the knowledge base

Ticket 02 decided that the ground-truth files stand in for the upstream systems and the loader
is the sync job. Phases 0 and 1 rebuild the database in full on every run, which is right for
generated data. Production-shaped sync is incremental: only changed records and chunks are
reloaded, with provenance (which source, when). LangChain's indexing API with a record manager
covers the chunk side. Closure evidence: a spec section for a later phase, a loader that skips
unchanged inputs, and a test showing a changed record is reloaded and an unchanged one is not.

**Trigger to reopen (author, 25 October 2026):** a full rebuild takes too long or costs too much
to run per change, either because the world grows to thousands of documents or because its sources
change often. Until then the knowledge-base spec's staleness guard makes a forgotten rebuild fail
loudly at startup, and the content-made IDs (ticket 05, decision 5) keep an unchanged passage's ID
stable, which incremental sync will rely on.

### AUD-034: Intel-Mac wheel check

While researching ticket 02, two recommended packages (LanceDB 0.40.0, pgembed 0.2.0) turned out
to ship macOS wheels for Apple Silicon only. The author's Mac is Intel. The recommendation had
to be revised after the machine was checked. Lesson: before recommending a native Python package,
list its wheels on PyPI and confirm a `macosx_*_x86_64` build exists, or state the source-build
cost. Closure evidence: the check recorded in the research method of the next ticket that
recommends a native package. Applied in research note 03 (21 October 2026): PyPI wheel lists
were queried directly for torch, onnxruntime and fastembed before any local model was weighed;
the author then ruled out local models altogether.

### AUD-035: Cohere Rerank 5 with calibrated scores

Research note 03 proposes `cohere/rerank-v3.5` through OpenRouter's rerank endpoint as the
default re-ranker. Its relevance scores are for ranking only, so the refusal threshold has to be
calibrated on the eval set. On 21 October 2026 Cohere announced Rerank 5, whose scores are
described as calibrated probabilities (a score of 0.7 reads as a 70 percent chance the document
is useful), which would make the threshold a documented constant rather than a calibrated one. It
was not on OpenRouter when checked the same day. Closure evidence: an eval run comparing the two
models on precision at 5 and on the refusal metrics, and a spec row recording the choice.

### AUD-036: Langfuse for traces and eval results

The author has three months of free access to Langfuse, starting 21 October 2026 and therefore
ending around 21 January 2027. Langfuse stores traces of every agent run (tool calls, retrieval
candidates with their scores, model answers), holds datasets of test questions, attaches scores
to runs and compares runs side by side. It would serve the knowledge base as the place where eval
results and retrieval traces are stored and inspected. It does **not** replace the eval harness:
the map requires the eval to be runnable by the author or Codex without Claude, as a test script
in the repo with pass rates against agreed thresholds; the question files and gold answers in
the repo stay the truth. Traces leave the machine on the hosted service; all data is synthetic;
the key lives only in `.env`. Decision belongs to ticket 06 (eval design): whether to adopt it,
hosted or self-hosted, and what the trace record contains. Closure evidence: a ticket 06 decision
row and, if adopted, one eval run visible in Langfuse with the retrieval-layer record fields.

**Decided, 23 October 2026 (ticket 06, decision 10).** Adopted to the full as a mirror: traces
through one callback handler in the agent-building function, the two question files as datasets,
each eval run as an experiment run stamped with the same version fingerprint and commit as the
JSON record, every check verdict as a score, the judge's verdict and reason as a score with a
comment, judge verdicts labelled in the annotation UI, and the running app traced for latency and
cost. Off by default, one environment variable turns it on, key loaded only when on; the JSON file
is written first and an upload failure is logged and noted in the summary; runs, datasets and
scores flow out, only human labels flow back by an export script into a repo file; a masking hook
is wired from day one. The author's reason: hands-on use of an observability platform for evals
and monitoring is part of the career goal. Hosted (free tier) for now; self-hosting (six
containers) is not planned. Research note 06, section 3.4, holds the facts. Closure evidence
unchanged: one eval run visible in Langfuse.

### AUD-037 to AUD-039: Scenario coverage for a product-grade investigator

Context, recorded 22 October 2026 during the plain-English discussion before knowledge-base
ticket 04. The author asked whether the Port's planted scenarios are enough for an app that may
become a product. Claude's assessment, accepted by the author: enough for the knowledge base's
phases 0 and 1, not enough for a product MVP. The gap is not the number of attacks. The benign
side is too thin (the only false positives are three IP addresses judged on reputation), and each
log row carries too little signal for a behavioural judgement. An eval set over scenarios that
each have one obvious answer would show a high pass rate that proves little. The author accepted
that the Port's tests and eval set will be re-pointed to a regenerated log for the sake of a more
comprehensive foundation.

The ruling for ticket 04 is to take the cheapest changes with the largest effect on the honesty
of the eval, and to register the rest here so the design leaves room and nothing is forgotten.
The three entries below are that remainder; each names what ticket 04 takes now.

#### AUD-037: Attack scenarios beyond the Port's five

The Port's generator (`backend/login_investigator/generator.py`) plants brute force then
compromise (S1, S3), a spray that never succeeds (S2), a sign-in from a new country (S4) and
prompt injection in a log field (S5). A product needs, at least: a spray that succeeds on a
privileged account; impossible travel (two countries within a time that rules out a flight); MFA
fatigue (many prompts, one accepted); a dormant account that wakes up; after-hours use of a
privileged account; credential stuffing (many accounts, one attempt each, a breached-password
pattern) as distinct from spraying. **Taken into ticket 04 now:** the spray that succeeds on a
privileged account, because phase 1 needs it. **Future:** the rest, each as a planted scenario
with a ground-truth entry and eval questions, taken when a phase needs it or when the author opens
a scenario initiative. Closure evidence: generator scenarios, ground-truth entries and passing
eval questions per scenario.

#### AUD-038: Benign look-alikes

An investigator earns trust on the cases it refuses to flag. Every planted attack today has a
clean signature and no innocent twin. A product needs benign behaviours that share a signature
with an attack: legitimate travel that looks like a new country; a VPN or provider change that
looks like a new address; a new device after a laptop refresh that looks like an unknown browser;
a password reset burst that looks like brute force; a new joiner's first week that looks like a
dormant or unknown account; a scheduled scanner or monitoring job that looks like a spray; an
authorised test announced in a document that the knowledge base can find. **Taken into ticket 04
now:** two or three look-alikes, chosen in the grilling so that each twins one planted attack.
**Future:** the rest. Closure evidence: generator scenarios, ground-truth entries marked benign,
and eval questions whose gold answer is "not an incident", scored separately from the attacks.

#### AUD-039: Row signals and baseline

Each log row holds time, user, address, country, outcome, failure reason and browser string. A
behavioural judgement needs more: the MFA result (passed, failed, not prompted, prompt declined);
a device identifier so "same device, different user" is a fact rather than a guess from the
browser string; the authentication method or protocol (password, token, legacy); the target
application; a session identifier. The window is one week, so "usual for this user" has a thin
baseline. **Taken into ticket 04 now:** the MFA column, because adding a column later means
regenerating the log, the ground truth, the eval set and every test that reads the CSV at once.
**Future:** the other columns and a longer baseline, each weighed against the Port's rules and
screens that read the log. Closure evidence: the column in the generator and the CSV, the Port's
tests and eval passing on the regenerated log, and a rule or tool that reads the new signal.

### AUD-040: Structural escalation of the agent

Knowledge-base ticket 05 (22 October 2026) placed the playbook in the Port's `create_agent`
middleware, extended with `before_model`, `after_model` and `wrap_tool_call` hooks. Research note
05 verified two stronger shapes the pinned LangChain supports and the ticket did not take: the
agent dropped as a node into a parent `StateGraph` with deterministic steps before it (strongest
control-flow integrity, but code would classify the chat, which the author ruled out), and a
knowledge-base sub-agent isolating corpus text from the main model (the Dual-LLM pattern, at a
second model call per step). Both stay available without rework because middleware survives
composition into a parent graph. Trigger to reopen: the corpus admits documents the workspace
does not write, or the canary pass rate in the eval falls below the agreed threshold. Closure
evidence: a spec decision row and an eval run on the new shape.

### AUD-041: Structured agent answer

Ticket 05's decision 6 resolves short citation labels in code after the model answers. Research
note 05 and the grilling discussion noted that a structured answer (the text plus a list of the
labels cited) lets the `after_model` hook read a list instead of finding brackets in prose. It
is a build-time choice in phase 0, not a spec change; recorded so the build ticket weighs it.
Closure evidence: the build ticket's decision and the hook's tests.

### AUD-042: Injection-detector middleware

During ticket 06 the author asked whether LangChain's prompt-injection middleware should be used
for the fence around tool results. Checked on 23 October 2026: LangChain 1.3.1 ships no injection
middleware; its Guardrails page shows injection checks as custom middleware, which is what ticket
05's `wrap_tool_call` fence is. Detectors exist as third-party middleware (Azure Prompt Shield,
hosted; several community packages, some local). All are probabilistic classifiers layered over
the structural defences the design already has (plan in code, read-only tools, deterministic
answer checks), and research note 05 found that such layers lower the injection rate without
closing it. Not adopted. Trigger to reopen: the eval's canary pass rate (ticket 06, decision 7)
falls below 100% and the structural defences cannot explain the failure. A hosted detector would
also send every prompt and retrieved chunk across the trust boundary. Closure evidence: a
decision row in the ticket that reopens it, with the canary results that triggered it.

### AUD-043: The faithfulness judge's reason on the screen

Ticket 06 (decision 6) made the judge a smoke alarm for the eval, never a gate, because its
agreement with human labels is unmeasured. Ticket 07 (decision 8) keeps its reason off the
screen for the same reason: showing it would teach the analyst to trust a signal the workspace
does not yet trust. Parked. Trigger to reopen: a measured agreement (kappa) between the judge and
the author's labels on the stored verdicts, at a level the author accepts. Closure evidence: a
screen decision in its own ticket, with the kappa that justified it.

### AUD-044: Leftover test databases after a killed run

Ticket 09's fixture drops each session's database at the end of the session, after passing and
failing tests alike, and a test proves it. A run killed before its teardown (the process ended by
force, the machine switched off) leaves its `li_test_<12 hex>` database on the server. Nothing
sweeps them, on purpose: a sweep at session start would also drop the database of another test
session running at the same time, and the project allows parallel sessions on separate tickets.
Raised by the spec review of ticket 09 on 25 October 2026. Parked. Trigger to reopen: a leftover
`li_test_` database is seen in pgAdmin or `pg_database`. A safe sweep would drop only databases
whose owning session is gone, for example by recording the process ID in the name or a comment.
Closure evidence: the sweep's test, or a ruling that manual cleanup suffices.

### AUD-045: Narrow spraying answer includes a brute-force source

The unchanged Port API eval for knowledge-base ticket 10 passed 55/57 overall and 15/15 security,
but Q08 run 2 named a single-account brute-force address as a password sprayer, then retained it
in the follow-up. B-073 records the answer and tool evidence in
`backend/evals/results/2026-10-25-221147-7ff8e5ae.json`. The earlier B-069 scope-preserving policy
remains in place; no prompt or policy changed, and the dataset files moved byte-identically.
The model's own evidence choices can still broaden a narrow investigation. Deferred outside T10;
registration does not approve implementation. Closure evidence: a separately agreed scope rule,
its regression evidence and an unchanged Port eval meeting the agreed gates while checking Q08.
Recurrence: the T11 eval failed Q08 runs 2 and 3 (B-073 recurrence note).

### AUD-046: Broad compromise answer without reputation lookups

The unchanged Port API eval for knowledge-base ticket 11 passed 53/57 overall and 15/15 security,
but Q04 run 3 ("Was any account compromised this week?") ran the rules and searched the three
attacker addresses without looking up any of their reputations. B-074 records it in
`backend/evals/results/2026-10-26-095844-7ff8e5ae.json`. T11 left the tools' outputs unchanged. Deferred
outside T11; registration does not approve implementation. Closure evidence: an agreed rule for
when reputation lookups are required, its regression evidence and an unchanged Port eval meeting
the agreed gates while checking Q04. Recurrence: T12 Q04 fails the lookup checks in all three
runs; see the B-074 recurrence and the 2026-10-26-112540 eval artifact. T13 repeats it in all three
runs with no agent change (2026-10-26-131223 artifact). Scoped on 26 October 2026 in
knowledge-base ticket 43: the code hook enforces searches but not lookups, and Q04's checks never
ask about S6's compromise of amelia.ward, which no T13 run states. T43's eval
(2026-10-26-173622-f853f368): all required lookups ran in every Q04 run, but flagging amelia.ward
passed 1/3, so Q04 is 1/3 and AUD-046 stays open. Closed on 26 October 2026 by T43's third paid
run (`2026-10-26-181909-b70d0745`): lookups enforced in code ran in every Q04 run of all three T43
runs, and Q04 passed 2/3 against its bar (3/3 after the B-078 grader fix), with the Port gates
met at 62/63 and 15/15.

### AUD-047: Outcomes lost in a broad answer about two spray sources

T12's eval passes its overall and security gates, but Q02 runs 2 and 3 omit S2's explicit
no-success conclusion and describe S6 as 20 total attempts despite 20 failures plus three
successes in the log. The direct S6 questions pass 6/6. See B-076 and
`backend/evals/results/2026-10-26-112540-7ff8e5ae.json`. The generator and API tests agree on the
rows; the agent code is unchanged. Deferred outside T12. Closure needs a separately scoped
behaviour decision and evidence that a broad answer preserves each source's failure and success
counts, alongside the unchanged Port and direct-S6 checks. Registration is not approval to build.
Recurrence: T13's unchanged agent fails Q02 in all three runs (2026-10-26-131223 artifact). With
Q04 also at 0/3, the Port eval met its 90% gate at 57/63 with no spare run: one more failure
anywhere would fail the gate on behaviour no ticket has changed. Scoped on 26 October 2026 in
knowledge-base ticket 43: the search returned S6's successes but the model kept the finding's
failure-only count, and Q02's no-success check is stale now that one spray succeeded. T43's eval
(2026-10-26-173622-f853f368): Q02 still 0/3. With `address_activity` beside the finding's own
`success_count: 0`, the model repeated the finding and twice wrote "all failures". AUD-047 stays
open; see the B-076 entry for T43. Closed on 26 October 2026 by T43's third paid run
(`2026-10-26-181909-b70d0745`): Q02 3/3, each answer preserving S2's no-success and S6's three
successes to amelia.ward, after the agent's view gained a code-built success sentence (ruling 9).

Reopened on 26 October 2026: T14's required safety-net eval
(`2026-10-26-202907-b70d0745.json`) passes 62/63 overall and 15/15 security, but Q02 run 3
again says S6 had zero successes and omits Amelia's three successful sign-ins. Q02 is 2/3;
Q04 is 3/3. The agent fingerprint remains `b70d0745`; T14 only adds reference files and a
standalone converter/fetch script. The failed answer searched only S6's failure window
(02:00:00–02:06:20 UTC). This is an observed evidence-window limit, not a proven root cause
for disregarding the detection result. Preserve the T43 closure evidence above and defer any
behaviour change outside T14. No unchanged-code rerun was made to obtain a cleaner score.

T19 recurrence, 28 October 2026: `2026-10-28-121053-b70d0745.json` passes 61/63 overall and
15/15 security. Q02 runs 2 and 3 omit S2's explicit no-success outcome, while correctly stating
S6's three successes to Amelia. Q04 is 3/3. Agent fingerprint remains b70d0745; no behaviour
change or cleaner-score rerun. B-076 records the distinction from T14's S6 failure.

### AUD-048: The finding ID and the agent's detection tool

`Finding.to_dict()` is both the Alerts reply and the output of the agent's
`find_suspicious_activity` tool. T13 kept `finding_id` out of it, so neither changed. Ticket 32
requires "The Alerts reply gains `finding_id` and nothing else". Adding the field inside `to_dict()`
would also change what the agent sees, which is an agent behaviour change gated by an eval run.
Ticket 32's builder decides, with the author, whether the route adds the field or the tool carries
it too. Closure evidence: that decision recorded in ticket 32, and its eval run if the tool changes.
Note for ticket 32, 26 October 2026: ticket 43 makes the agent's detection output differ from
`to_dict()` by one agent-only field per finding (spec decisions log, same date), so the tool no
longer returns `to_dict()` alone.

### AUD-049: Finding counts the Alerts screen never shows

Found while scoping ticket 43. The Alerts reply sends `failure_count` and `success_count` for every
finding, but the Alerts table shows only `event_count` (`frontend/src/components/alerts-table.tsx`).
The project rule says the API returns only the fields the screen needs. A spraying finding's
`success_count` is also always 0 by construction, so a future screen that showed it would mislead.
Outside ticket 43's scope; registration is not approval. Closure evidence: the author's decision to
remove, show or relabel the fields, and its tests.

### AUD-050: Q21's three-successes check

Ticket 43's spec review probed Q02's first three-successes pattern, a copy of Q21's, and found it
passes wrong answers ("It made 3 failed logins", "No successful sign-ins in the last 3 days") and
fails right ones ("Three of those attempts succeeded", "signed in to amelia.ward three times").
Ticket 43 replaced Q02's copy with the shared `THREE_SUCCESSES` pattern and its both-direction
tests; Q21 keeps its own pattern. Q21 passed 3/3 in T13, so no wrong score is known. Registration is
not approval. Closure evidence: Q21 moved to the shared pattern, or the author's decision to keep
it, and a re-grade of the last saved run.

### AUD-051: Imperative recommendations in refusals

T43's eval failed Q19 run 3 on "recommends the step", although the answer said "Please follow your
organization's procedures to reset daniel.hughes's password." The shared `RECOMMENDS` pattern knows
advisory verbs only. See B-077. Registration is not approval. Closure evidence: the pattern
extended with both-direction tests, and a re-grade of the T43 artifact.

### AUD-052: Benign twin B2 flagged as possibly compromised

Ticket 43's rulings 8 and 9 tell the agent to flag an account that a brute-force or spraying
address signed in to, and add a true code-built sentence to such a finding's summary. B2's reset
burst (198.51.100.30, oliver.hayes) trips brute force and then signs in 11 times, so the agent now
sees "also signed in successfully 11 times, to oliver.hayes" and will likely flag him. The
knowledge-base spec requires that benign twins never slip; the Port eval has no check for it. His
clearing document and the investigation tool's clearing section (phase 0 corpus, phase 1 tool)
are the planned cure. Registration is not approval. Closure evidence: a knowledge-base eval
question on B2 passing with the twin cleared.

### AUD-053: Codex questions appear in a collapsed queue

The author reported invisible pop-ups during T14 and earlier sessions. The reproduced question
was present in the Login Investigator terminal as `? 1 question`, with `⇧← to answer`.
Shift + Left Arrow opened it, and the author answered through the tool. Closed on that live
confirmation. Future questions should be announced in normal commentary with the shortcut;
plain chat remains the fallback. No global setting change was needed. See B-081.

### AUD-054: Inherited Herdr pane identity is inconsistent

During the same investigation, `--current` pointed to another project's pane. Discovery by
working directory, live title and focus found the correct Login Investigator pane; explicit
targeting then exposed the diagnostic question. Root cause remains unknown. Deferred rather
than changing the multiplexer or another project's process. Until investigated, verify the live
project and use an explicit pane ID. Closure needs an explanation and a repeatable check that
this session's inherited caller identity resolves to its actual pane. See B-082.

### AUD-055: What the corpus checker cannot see

The T15 consistency script checks identifier-shaped mentions: `first.last` usernames, device
names and IDs, `asset-` IDs, IP addresses and ATT&CK IDs, plus the leaver's username and written
name. It cannot tell an invented system ("the CRM") or an invented person ("Sam Reed") from
ordinary prose, because both look like normal words. It also does not gate the counted trait
that `run-password-spray-response` names no technique ID; the ticket's script criteria do not
ask for it. The brief forbids all three. The author's read for feel in T16 covers them, including
a search of that runbook for `T1` and `M1`. Registration is not approval. Closure evidence: the
T16 read recorded with these three checks, or a later ticket that adds code checks for them.

Closed 27 October 2026. T16's "Real names scan" compared every capitalised name and system in the
27 documents with the organisation tables and the brief, and found none invented; it found no
technique ID in `run-password-spray-response`. The author then approved the 27 documents with no
rewrites. The checker's limit itself stands; a later corpus needs the same read.

### AUD-056: ATT&CK source references as provenance metadata

By the author's T16 ruling P3, the `## References` section of each ATT&CK page is kept in the file
but never chunked, and inline citation markers and link addresses are removed from chunk text
(P4a, P4c). Search then sees only text that explains. MITRE's STIX data holds each reference as a
structured field with a source name and URL. A later slice could keep those as metadata on the
technique's chunks, so an analyst can trace a claim to MITRE's source without the list being
searched. Phases 0 and 1 do not need it: citations point to our own chunks, not to MITRE's
sources. Registration is not approval. Closure evidence: a ticket that adds the metadata, or the
author's ruling that it is not wanted.

### AUD-057: Superseded successful build databases

T17 builds a new database and publishes its local pointer only after success. Failed builds are
dropped. Previous successful databases are deliberately retained for inspection and reported by
name, so a rebuild does not destroy a database a reader may still be using. Repeated explicit
builds therefore accumulate databases until the author removes them. The command and README
state this behaviour. A later maintenance command could reclaim only verified, superseded
knowledge-base builds while protecting the active database and unrelated projects. Registration
is not implementation approval. Closure evidence: an approved cleanup policy and tests protecting
the active/unrelated databases, or the author's decision to keep manual maintenance.

Manual cleanup, 29 October 2026: the author dropped `li_kb_f9d6bcf6f8c5` (T18's build) by hand
in pgAdmin. Kept: `li_kb_fe13d09e32f4`, the active build named by `backend/.knowledge-base.json`,
and `li_kb_0af9160cc4ed`, T17's first build, by the author's choice. Saved evidence that names
the dropped build keeps its recorded values. This is one manual clean, not a policy; the entry
stays open.

### AUD-058: Chunking code outside the staleness fingerprint

T18's fingerprint covers the dataset files, the embedding model, the vector length and the
chunking settings (encoding, passage and overlap sizes), as the spec asks. It does not cover the
chunking code itself: the heading, fence, step and ATT&CK cleaning rules in `chunking.py`, nor the
mention rules in `mentions.py`. A change to those rules leaves an old database passing the guard,
which sits uneasily with "the app never answers from a database built from an older world".
Options: a hand-bumped recipe version in the fingerprint, or a hash of the two modules' source,
which forces a rebuild on any edit (about 20 seconds and a tenth of a cent). Registration is not
implementation approval. Closure evidence: the author's ruling, and a door 2 test if code joins
the fingerprint.

### AUD-059: Two readers of `LI_DATASET_DIR`

The build command takes its default dataset folder from `.env` and the environment. The app's
`Settings.from_env` reads the environment only. With `LI_DATASET_DIR` set only in `.env`, the build
fingerprints one folder and the app checks another, so the guard refuses to start after every
rebuild. The refusal is the safe direction, but the cause is confusing. The split predates T18;
T18's fingerprint is what makes it matter. Options: the build reads the environment only, like
the app, or both read `.env`. Registration is not implementation approval. Closure evidence: one
reading rule for both, pinned by a test.

**Author's ruling, 28 October 2026:** every `LI_` setting, in the app, the build command and the
scripts, is read from the environment first, then `.env`, then the default (spec, API contract
change 5). `env.example` already presents `LI_DATASET_DIR` as an app setting, which the app does
not honour today; the alignment fixes that too. The code change waits for the phase 0 cleanup
ticket.

### AUD-060: VPN address observation point is not explicit

Open design concern, identified during T19 discussion on 28 October 2026; source B-091.
The corpus describes session-assigned VPN pool addresses, while the log stores only `source_ip`
and the generator does not declare the observation point. Public-exit semantics must not be
assumed. Before T19's network relationship is implemented, obtain the author's ruling on the
meaning and evidence limits. Any dataset or spec change requires author agreement. Closure:
an agreed explicit meaning, with affected records and checks aligned if changes are approved.

Author's ruling, 28 October 2026: follow the policy's session-assigned, reused-address meaning,
not public exits. Recorded in the spec and T19 Answer decision 2. Still open for the consequence:
whether and how the ten S6 address-reuse matches belong in the result, and the associated time
window. No dataset changes or allocation telemetry approved by that first ruling.

Subsequent author ruling, 28 October 2026: retain the ten address-reuse matches as labelled
supporting context, outside any exposed-account count (T19 decision 3 and spec graph section).
T19 must align the answer key and tests during implementation. Time-window decision and
implementation evidence remain outstanding; entry stays open.

Further author ruling, 28 October 2026: optional user dates take precedence, with the available
log period as the default. T19 decision 4, the spec and T25/T26 now record the contract. The date
decision is settled; implementation and verification remain outstanding.

Closed on 28 October 2026: T19 independently recomputes S6 with context grouped by address,
including the ten VPN matches and 43 office matches, outside exposure counts. Optional dates
filter successful observations on both sides; results state coverage and snapshot limitations.
The full backend suite passes 612 tests, including corruption and exact answer-key checks;
live reader evidence is `19-live-graph-2026-10-28.json`. Future tools retain the explicit T25/T26
acceptance criteria. No session-allocation telemetry or exposure inference was added.

### AUD-061: Intermittent test database teardown privilege failure

Open, scheduled for consideration in T44. Source: B-094, T19 corruption-test run on 28 October
2026. Existing `drop_database` uses FORCE, but li_admin cannot terminate all backend roles.
One fixture teardown failed after passing assertions. Do not broaden database privileges
without a ruling. Closure: diagnose the connection safely and approve a cleanup policy, or
record an explicit deferral; keep the original failure evidence.

Recurrence, T23, 29 October 2026: the first full backend run was clean (665 passed). After the
review fixes, the second full run had 666 passed and two teardown errors, both in the unchanged
`test_integrity_rejects_corruption` (`asset_id`, `mention`). Rerunning that test alone gave 20
passed and one teardown error on a third parameter (`swap`). Same message: permission denied to
terminate process. One focused run also hit it in `test_corpus_search.py`, passing alone. It
is now frequent in the corruption tests. Each occurrence may leave a test database behind; none
was cleaned, because cleanup needs the database password from `.env`. The fixture is unchanged.
Later the same day the author dropped the four leftover test databases by hand in pgAdmin
(`li_test_5b3c17d13b5f`, `li_test_292de847fa91`, `li_test_79349fb3823f`, `li_test_fc59a8fdc8e0`),
matching the four teardown errors of this session. New leftovers will appear until T44 rules.

T22 recurrence on 29 October 2026: 21 focused assertions passed, one database teardown failed
with the same InsufficientPrivilege. Recorded under B-094; no privilege or fixture change.
The final full run also passed all 646 assertions but exited 1 on one teardown of an unchanged
graph test. Exact cleanup and focused rerun evidence are in T22. The fixture issue remains open.

T24 recurrence, 29 October 2026: full backend run passed 677 assertions and exited 1 on
two teardown errors in unchanged tests (`test_numbered_runbook_steps_survive_whole` and
`test_open_graph_refuses_a_dataset_changed_since_build`). Same InsufficientPrivilege.
The exact leftovers `li_test_06f7a2ac8597` and `li_test_c36803010095` were verified to have zero
attached sessions, then dropped without FORCE. Both affected tests reran clean: 2 passed,
2.76 seconds, exit 0. No privilege or fixture change; concern stays with T44.

T48 recurrence, 30 October 2026: the affected-test run hit the same teardown privilege error
after `test_runner_checks_integrity_before_calling_the_embedding_service` passed. Its exact
idle leftover was dropped without FORCE. The separate intentional shutdown-failure test also
retained recovery state. Read-only diagnostics identified a `postgres` connection whose
application is pgAdmin holding that exact disposable database; a non-FORCE drop refused.
No connection was terminated and no privilege broadened. The session handoff records the exact
remaining resource for recovery after pgAdmin disconnects. Resource-closure tests now count
the configured application reader rather than unrelated pgAdmin/maintenance connections.

The author confirmed manually deleting `li_kb_86d2da6633c7` on 30 October 2026.
This closes that specific leftover; it does not authorize removal of other builds.
The final T48 full run passed 709 tests but exited 1 on the same teardown privilege error
in unchanged `test_integrity_rejects_corruption[extra]`, even with pgAdmin closed. Its exact
leftover `li_test_b94165a0c68e` was verified idle and dropped without FORCE. The affected test
reran clean: 1 passed in 2.58 seconds. No role privileges changed. This recurrence remains
open under T44; closing pgAdmin does not establish a general fix.

T49 recurrence, 1 November 2026: the full run passed the privileged-reader refusal assertion,
but its fixture teardown hit the same permission-to-terminate error. After the suite exited,
the exact leftover `li_test_22b850f6b794` had zero attached sessions and was dropped without
FORCE. No role privileges changed. B-133 records the full run and targeted follow-up.
All three affected tests then passed in 209.14 seconds, including teardown. The broader
intermittent cleanup concern remains open.

### AUD-062: Compound retrieval question loses the MFA exception register

T22's first live run misses one of K04's two required passages. The runbook ranks 9; the MFA
exception register ranks 115 in an exact dense diagnostic. The keyword leg yields no candidates
because the full question's terms are combined with AND. Its graph records and paths pass.
See B-098 and the saved per-question evidence. T22's acceptance permits a logged miss; this
does not waive the initiative's retrieval gate. No tuning or query-rewriting strategy is
approved by registering this concern. Review the candidate-generation approach before closing
that gate, preserving the existing questions and gold. Closure requires both K04 gold passages
in the fused top 20 and regression evidence on the other questions. T23 re-ranking alone cannot
restore missing candidates.

Follow-up diagnostic, 29 October 2026: an MFA-focused neutral query retrieves the register at
rank 7, an explicit exception query at rank 2, and a procedure-focused query retrieves the
runbook at rank 1. See T22's follow-up and its saved probe. Human-written queries after inspecting
the failure establish recoverability, not automatic decomposition or merged-budget performance.
The original K04 gate remains failed; no policy change or closure is claimed. T26 already
requires investigation searches constructed from finding records in code.

Research follow-up, 29 October 2026: the author requested Perplexity research into decomposition
and fallback. See [the primary-source research note](../../.scratch/knowledge-base/research/22-investigation-retrieval-recovery.md)
for bounded recovery, omitted-needs risks, an independent broad-route experiment and fixed-budget
evaluation proposals. No retrieval policy or spec change is approved by this research. The
original K04 gate and this entry remain open.

Fixed-budget experiment, 29 October 2026: [saved protocol and results](../../.scratch/knowledge-base/research/22-retrieval-experiment-results.md).
Focused searches retain both K04 passages within twenty, but adding a broad route with equal
cross-query RRF drops the MFA register to rank 25. One prewritten, human-triggered retry restores
it at rank 4. The broad route also rescues a deliberately omitted need in another case. This
exposes an additional selection risk: merging can lose evidence already retrieved. Future
design should test preserving evidence across needs; no allocation policy is approved. The
human-selected recovery is not an automatic coverage check. Two absent topics remain unresolved,
and the original K04 closure gate is unchanged. B-098 retains this diagnostic iteration.

Evidence-preservation follow-up, 29 October 2026: the author prioritized this before model
comparison. [Design and offline replay](../../.scratch/knowledge-base/research/22-evidence-checklist-design.md)
distinguish candidate retrieval, semantic support review and final selection. Fair route turns
recover K04 from saved candidates without another query, but two of six route orders fail and
a five-passage stress cap loses the MFA passage. This is not a T23 reranker test. Equal allocation
is not adopted; need-aware support preservation and selection repair require further design.
No application/spec changes or closure. The actual support reviewer remains undecided.

Author's deferral, 29 October 2026: park further custom retrieval-design work at T23. Evaluate
the planned reranker before resuming decomposition, evidence-checklist, selection or recovery
experiments. T23's Comments carry the reminder and evidence links; its implementation scope
is unchanged. AUD-062 remains open, and no candidate-gap fix or original-gold waiver is implied.

T23 first live run, 29 October 2026 (`backend/evals/results/2026-10-29-150414-681065-retrieval-0331ac624577.json`):
with the re-ranker on, K04's runbook moves from fused rank 9 to re-ranker rank 1 and is kept.
The MFA register is still outside the fused 20, so it is never scored. As recorded above,
re-ranking cannot recover a missing candidate. The gap and the original gold are unchanged.

Author's ruling, 29 October 2026: the parked design work moves to its own decision ticket,
[45](../../.scratch/knowledge-base/issues/45-compound-question-retrieval-design.md), which blocks
T26. It covers the chat path, where the model writes the search from any analyst question, and
the package path, where code builds searches from the finding. This entry stays open.

### AUD-063: One reader for the OpenRouter key and usage, one test guard for `.env`

Open, candidate for T44. Source: T23's standards review and B-101. The embedding factory and the
re-ranker factory each read `OPENROUTER_API_KEY` from the environment and `.env`, each count
usage from OpenRouter's reply, and the test run's guard in `backend/conftest.py` covers each
module by its own line. B-101 showed the cost: the new module was not covered until a test
caught it. `EmbeddingUsage.record_response` also converts provider usage fields with `int()` and
`float()` unguarded, so a malformed usage field would fail a build with provider text; T23 fixed
this for the re-ranker only. A shared reader for OpenRouter settings and usage, and one guard
point, would close the class of bug. Registration is not approval; T44 decides.

### AUD-064: What the re-ranker's assessment still needs

Open, for T39 and T41. Source: T23's spec review and first live run. Two inputs are missing
before the re-ranker can be judged:

1. **A kept-5 check.** T23 keeps the retrieval gate on the fused 20, which the re-ranker cannot
   change. T06 d9 judges a switch on decision 1's second check, the chunks the model receives.
   With the re-ranker on, that is the kept 5. T41's on-versus-off comparison needs that check
   in the retrieval layer; T23 records the kept 5 in every artifact, so saved runs can be
   rescored once it exists.
2. **Calibration evidence.** In the first live run, K06, an absent topic, has a top re-ranker
   score of 0.646, above K04's real top score of 0.516. K05's top score is 0.106. One run on
   eight questions proves nothing, but it warns that a single relevance threshold may not refuse
   every absent topic. T39 calibrates on its tuning file under T06 d4; no threshold is set here.

### AUD-065: Investigation evidence persistence and storage growth

Registered at the author's request, 29 October 2026, during the discussion before
[T24](../../.scratch/knowledge-base/issues/24-first-agent-tool-lookup-account.md).
The knowledge-base tools add saved evidence beyond the conversation and report. Keeping that
evidence outside the model's input limits context size, but does not limit storage growth.
No storage-size or scalability failure has been measured. This is a design concern, not a bug.

Preserve the evidence behind a saved answer rather than reconstructing it from a later version
of the knowledge base. Existing spec requirements already save artifacts for the screen and
eval. The later storage review should agree the persistence promise for conversations, reports,
evidence and downloads; distinguish durable evidence from disposable execution details; and
measure repeated payloads, checkpoint history, intermediate writes, database growth and reopen
latency across representative investigation lengths. Include repeated lookups, document searches
and investigation packages, not only the small account lookup.

Deferred options, to decide from measurements: retention periods, archival, deduplication,
checkpoint pruning and separate artifact storage. No automatic deletion, storage migration or
new retention policy is authorised. AUD-032 remains parked with its existing phase-2 trigger;
moving memory to PostgreSQL alone would not settle retention or duplication.

Read-only inspection on 29 October 2026: `login_investigator/investigations.py` uses one SQLite
file for the investigation index and `SqliteSaver` memory. `agent.write_report` saves report JSON
as a named message; `saved_history` reads it without a model. The PDF route renders the saved
report on download rather than keeping PDF bytes. The installed SQLite saver stores serialized
checkpoints and intermediate writes. Actual artifact duplication and growth remain unmeasured.

Approved T24 addition, author confirmation in chat on 29 October 2026: document the lookup
artifact's fields and persistence path; measure baseline storage and growth after 1, 10 and 50
repeated lookups with a fake model in a disposable database; prove close/reopen
preserves the original artifact without querying the source again; retain report-download
behaviour. Record measurements as a baseline, not an invented performance gate. This does not
implement the deferred storage options or the later evidence panel.

T24 measurement, 29 October 2026: a single lookup artifact is 601 JSON bytes. The disposable
SQLite file grew from 20,480 bytes at baseline to 40,960 / 811,008 / 16,404,480 bytes after
1 / 10 / 50 repeated lookups in one investigation. At 50 lookups, 350 checkpoint rows held
15,815,671 payload bytes, while 450 intermediate writes held 86,770 bytes. Latest-state reopen
took 0.0181 seconds and restored all 50 artifacts. Repeated growing checkpoint state dominates
this sample; no concurrency or production-capacity claim is made. Full method and limitations:
[T24 persistence evidence](../../.scratch/knowledge-base/research/24-persistence-evidence.md).
The broader storage design remains deferred; measurements do not authorise a remedy.

Trigger to revisit: the post-initiative improvement review, or earlier if measurements show
storage growth or reopen latency that makes the current design unsuitable. Closure requires an
author-approved persistence and retention policy, measured evidence for the selected design,
and tests that retained investigations and reports remain usable after restart and source rebuild.

### AUD-066: Q04 compromise attribution across a long structured answer

T24's live Port API eval (`2026-10-29-204751-654728-fa8f3e8f.json`) passes 62/63 overall
and 15/15 security. Q04 run 1 fails only the Amelia compromise-attribution check. It opens
with accounts that "may have been compromised", lists Amelia with S6's three successful
sign-ins and recommends securing her account. The current `AMELIA_COMPROMISED` pattern expects
a nearby same-line phrase or a narrowly formatted list. The long introductory claim and
multi-line list do not match. This is a suspected grader coverage limitation, not a proven
missing S6 fact or a recurrence of skipped reputation calls; all required calls ran.

Keep the failed score. Future review should decide whether that contextual attribution is
adequate, then test both valid long-list attribution and unrelated/negated account mentions
before changing the check. No grader or prompt change is authorised here. B-105 records the
observation; B-078 is the earlier, separately fixed phrasing limitation.

T49 follow-up, 1 November 2026: approved live Port evaluation
`2026-11-01-104006-806272-13987838.json` passes 60/63 overall and 15/15 security.
Q04 fails the same Amelia-attribution check in all three repetitions. All three answers contain
S6's three successful sign-ins. Run 1 uses a general possible-compromise introduction and
recommends securing Amelia; run 2 recommends securing other accounts; run 3 only recommends
monitoring Amelia. The latter answers also warrant a substantive attribution review. Do not
classify every failure as a grader defect. Scores and thresholds remain unchanged. This
migration does not authorise prompt/grader changes or another paid run. B-105 retains the
recurrence and the issue remains open.

### AUD-067: Graph foundation review

The author questioned whether T02's small, bounded graph assumption still fits the intended
application and proposed Neo4j Community for graph queries with PostgreSQL/pgvector retained
for document retrieval. On 30 October 2026 the author approved opening
[T46](../../.scratch/knowledge-base/issues/46-graph-store-architecture-review.md), with a scoped
architecture review and a disposable proof to agree before application changes.

This is an architecture concern, not a demonstrated NetworkX defect or capacity failure.
Compare database-enforced read-only serving, separate build access, exact graph answers,
cross-store build consistency, isolated tests/evaluations, recovery and operating burden.
Community edition limitations must be checked on the exact release; a database-wide read-only
setting is a candidate to test, not an assumed equivalent of PostgreSQL's reader role.

T25 and T27 wait for T46. T45's compound-retrieval work remains separate. T02's history and
the current spec are preserved; neither migration nor a security exception is approved.
Closure requires the author's recorded ruling backed by the agreed evidence and explicit
disposition of the hold. If migration is chosen, implementation blockers must be established
before T46 closes; audit closure follows the required implementation and parity evidence.

T46 progress, 30 October 2026: author confirmed Astra and agreed a shared analyst service,
measured maintenance downtime, free editions first and an isolated security-first proof.
[Pinned Community 2026.10.1 research](../../.scratch/knowledge-base/research/46-community-read-only-feasibility.md)
supports graph read-only configuration but identifies administrative capabilities retained
by authenticated users and a writable system database. This is source evidence of a mismatch
with unprivileged serving, not a reproduced live failure. The broader proof awaits discussion
of this finding; no migration decision or security exception exists. T25/T27 remain held.

Subsequent author ruling, 30 October 2026: continue the Community evaluation with retained
administrative access accepted as a development-stage limitation. The spec records this
conditional exception. Graph-data write prevention and separate writable builds still need
proof. Production use requires a separate review of permissions, recovery, availability,
monitoring and cost, including the possible Enterprise upgrade. No migration is approved;
T25/T27 remain held. This supersedes the preceding no-exception status for this narrow point.

Live proof, 30 October 2026: Community 2026.10.1 rejected graph/schema writes and the two
tested access-mode bypass attempts before and after restart, while allowing user administration.
[Results](../../.scratch/knowledge-base/research/46-community-security-result.json) record 24
outcomes; graph snapshots were unchanged and disposable resources cleaned. This supports the
accepted development boundary, not full production security or the remaining T46 proof gates.

Further proof, 30 October 2026: [parity and pair lifecycle evidence](../../.scratch/knowledge-base/research/46-parity-and-pair-proof.md)
records 38 checks across original, variant and rebuilt graphs, plus deliberate failed-build
cleanup. Exact query answers, dated peers, source IDs, S6 gold, read-only handoff, mismatch
refusal, activation and rollback passed. The unoptimised candidate is slower on the small
fixture; no speed/capacity claim is made. Actual application downtime, production readiness
and final migration design remain unresolved. [Impact inventory](../../.scratch/knowledge-base/research/46-impact-inventory.md)
identifies the synchronous/asynchronous boundary and export/integrity coupling. T46 stays open;
the author's engine ruling and reviewed migration tickets are still required.

Final T46 ruling, 30 October 2026: author selected Neo4j Community plus PostgreSQL/pgvector,
approved passage references without duplicate content, complete-version restart/rollback and
native Browser inspection replacing Gephi. The spec and decision log are updated; approved
build tickets are [47](../../.scratch/knowledge-base/issues/47-neo4j-build-and-graph-answers.md),
[48](../../.scratch/knowledge-base/issues/48-paired-lifecycle-and-native-inspection.md) and
[49](../../.scratch/knowledge-base/issues/49-neo4j-migration-acceptance.md). T46 resolves as a
decision; this audit item remains open until T49's implementation evidence. T25/T27 depend on
T49. The earlier pending-ruling statements above are historical, not the current status.

T49 progress, 1 November 2026: author accepted the measured candidate and maintenance/recovery
plan. Two retained pairs match all 320 passage rows/vectors, 50 accounts, ten findings and
40 dated radii. The live Port gate passes 60/63 and 15/15 security; all eight retrieval results
match the previous baseline exactly, preserving its known failures. NetworkX and the obsolete
publishing command are retired; both review axes pass after recorded operator/privacy fixes.
Final full verification and working activation remain pending. AUD-067 and the T25/T27 hold
remain open until that evidence is complete.

**Closed, 1 November 2026:** T49 completed the author-accepted development migration. The
working application now selects the verified Neo4j/PostgreSQL pair; 25 saved investigations
reopen identically. NetworkX is retired, both recovery routes are tested and retained, and the
final operator commands, regression cases and two-axis reviews are complete. Full-run findings
and passing affected reruns remain explicit in [T49 verification](../../.scratch/knowledge-base/research/49-verification.json);
[activation evidence](../../.scratch/knowledge-base/research/49-working-activation.json) records
actual readiness and readers. Exact graph/passage parity and live gates are linked from T49.
The retrieval baseline's existing failures are preserved, not waived. T25/T27 are released by
T49's resolved status. AUD-068 remains open as the separate production gate.

### AUD-068: Production readiness after the development-stage Neo4j migration

The author explicitly accepts Neo4j Community's retained administrative powers during current
development. This is not least-privilege serving and does not authorise a production offering.
Before production is proposed, open a scoped readiness review covering permissions, availability,
recovery/backup, monitoring and operating/licensing cost. Assess Enterprise or other suitable
controls at that time; the documented edition-upgrade path does not establish configured security
or availability. No purchase, deployment date, capacity target or downtime guarantee is assumed.

Source: T46's approved design and development-stage ruling, 30 October 2026. Owner: the future
production-readiness initiative; T49 must carry this condition forward without closing it.
Closure requires an author-approved production scope and evidence that its controls and operating
procedures work. This item does not block the authorised development migration T47–T49.

T47 startup observation, 30 October 2026: the pinned Community image logs anonymous usage
telemetry, Fleet discovery on the Docker bridge, and a forwarded-header allow-hosts warning.
The T47 command publishes only Bolt on localhost; HTTP is not published. These runtime defaults
are recorded for the production-readiness review, not silently treated as production safeguards.
No telemetry/network-policy change was made under this observation.

T48 native inspection update, 30 October 2026 (author walkthrough accepted; T48 resolved): newly created serving containers also publish
Browser HTTP on localhost, after sealing the graph read-only. The builder container still exposes
only Bolt. Browser starts in read access mode; this is a client preference, not least privilege.
The accepted Community administrative limitation and future production gate remain unchanged.

T49 closure, 1 November 2026: the development application is now active on the accepted pair.
Restart/rollback/recovery measurements and the earlier cold-start/readiness failures are
recorded in T49, B-126 and B-131. They establish local recovery evidence, not availability
bounds. Community administrative powers remain accepted only for development; this gate is open.

### AUD-069: Explorer interaction timeout under concurrent validation

T47's unchanged frontend suite recorded 149 passes and one five-second timeout in the valid-IP
submission/Reset test at `explorer.test.tsx:80`. The affected file then passed all eight tests
without code or timeout changes. Cause remains unproven; the original run overlapped Docker
integration startup. Keep B-113's failure evidence. Investigate if it recurs; no UI change or
relaxed timing threshold is approved. Candidate for the existing T44 cleanup review.
T48 reproduced the same timeout: 149 passed, one failed in 50.20 seconds, with concurrent
validation. No frontend changes were made. A separate rerun is recorded in T48; the cause
remains unproven and this item stays open for investigation.
The separate full rerun passed all 150 tests in 28.27 seconds without changes.
T49 reproduced the same timeout on 1 November: 149 passed, one failed in 49.95 seconds.
Only frontend type/lint checks overlapped, not a Neo4j build. Cause remains unproven; no
frontend or timeout change was made. The separate affected file passed all eight tests in
22.60 seconds. B-113 preserves both results; this concern remains open.


### AUD-070: Pydantic Evals adoption path

Recorded at the author's request, 31 October 2026. An evaluation framework organises the exam;
its quality still depends on the questions, gold evidence and grading rules. Pydantic Evals
offers reusable evaluators, experiment reports and repeated comparisons. It is independent of
Pydantic AI, so adoption would not require replacing LangChain. Sources:
[overview](https://pydantic.dev/docs/ai/evals/evals/) and
[core concepts](https://pydantic.dev/docs/ai/evals/getting-started/core-concepts/).

Codex recommendation: defer adoption. Our runner, deterministic scorer, saved results and
version fingerprints already cover much of the machinery. Langfuse is the agreed inspection
mirror (AUD-036). Adding a second runner now risks duplicate maintenance and does not resolve
retrieval gaps or weak grading rules.

Trigger to revisit: after migration acceptance, repeated model/retrieval comparisons or the
faithfulness-judge implementation expose a concrete maintenance problem. Proposed path: agree
a small ticket, wrap the existing scorer and a representative subset of saved cases in Pydantic
Evals, then compare verdicts and reporting effort with the current harness. Keep one source of
truth for questions and scoring, preserve acceptance thresholds and saved evidence, and keep
the judge advisory. Adopt only if the trial demonstrates useful simplification without a
permanent duplicate runner; otherwise retain the current harness. Closure evidence: recorded
comparison results and the author's adoption or rejection decision. Registration authorises
no dependency, implementation or spec change.

### AUD-071: Operator inspection of passage text by graph passage ID

- **Source:** Author discussion during the [T48 learning walkthrough](../../.scratch/knowledge-base/issues/48-paired-lifecycle-and-native-inspection.md), 31 October 2026.
- **Current boundary:** Neo4j passage nodes contain references and relationships. PostgreSQL owns
  passage text. Neo4j Browser does not automatically fetch that text; this is an accepted T48
  scope boundary, not a migration defect.
- **Operator need:** See the relevant passage text associated with a specific passage ID in a
  graph node. No broader document-browsing capability was requested.
- **Status and ruling:** Parked at the author's explicit request. Discussion considered adding
  it to T49, but no scope expansion was approved. T49 and the planned in-app Graph tab remain
  unchanged. Reopen only when the author requests it.
- **Decision still needed:** Where the text appears, including whether inspection must happen
  inside Browser or through a separate lookup. No implementation mechanism is selected.
- **Acceptance when reopened:** Agree the operator workflow, retrieve exact passage text and
  source information from the matching build, and verify missing IDs and version mismatches
  cannot silently return unrelated evidence. Preserve PostgreSQL as the passage-text owner.
  Closure requires tested evidence and author review; none exists yet.

### AUD-072: Graph-integrity test service failure during import cleanup verification

- **Source:** [B-124](../bug-log.md), 31 October 2026.
- **Observation:** `test_corrupt_graph_refused_and_successful_device_witness_preserved`
  raised `GraphUnavailable` during its device-peer query in the unrestricted regression run.
  The run was interrupted after 373 passes and one failure to investigate. The driver cause
  is suppressed, so timeout or import-order causation is not established.
- **Initial follow-up:** the isolated rerun failed in 133.99 seconds because Neo4j did not
  become ready within 120 seconds. This establishes a service-readiness problem in that run,
  but does not diagnose the earlier query failure.
- **31 October recovery evidence:** the author requested investigation and completion of
  verification. Without changing application code, timeouts or Docker settings, a temporary
  diagnostic run passed in 35.77 seconds (two harness-only pytest import-rewrite warnings).
  Graph readiness took 17.79 seconds; container state showed `OOMKilled=false` and memory
  usage was 713.8 MiB. The normal focused test then passed in 37.40 seconds. The complete
  backend suite passed all 701 tests in 957.38 seconds, including the previously failing
  graph-integrity check in 34.07 seconds. No failures or teardown errors occurred in that run.
- **Status:** verification gap resolved; intermittent observation remains open because the
  original driver cause was not captured. No speculative timeout increase or service restart
  was applied. If it recurs, capture driver error code and container state before cleanup.
  Final process/container inspection found no running tests and only the pre-existing retained
  walkthrough graph container. No application selection changed and no paid services ran.
- **1 November T49 recurrence:** B-131 records nine focused passes and seven shared-fixture
  setup errors when the serving restart exceeded the existing 120-second readiness deadline.
  The failed build cleaned its resources. A temporary diagnostic retry captures the underlying
  driver class/code and container state before any repeat cleanup. No settings were relaxed.
  The diagnostic retry then passed all 15 focused tests in 265.92 seconds. Both serving
  restarts completed under unchanged limits; the original cause remains unknown.
- **T49 final verification:** the complete backend run passed all graph availability, integrity,
  paired lifecycle and native-inspection checks. Its separate legacy-test mismatch and known
  PostgreSQL teardown recurrence were recovered through a test-only correction, exact cleanup
  and three passing affected tests. No graph service setting changed.
- **Closure evidence:** establish the cause or disposition with reproducible evidence and
  author review. A passing rerun alone does not prove the underlying problem fixed.

### AUD-073: VPN session allocation record for address co-presence

- **Source:** [T25 gate session](../../.scratch/knowledge-base/issues/25-peers-and-corpus-search-tools.md),
  question 2, author's ruling on 1 November 2026. Evidence:
  [research note 25](../../.scratch/knowledge-base/research/25-shared-address-value.md), sections 4.2 and 5.
- **Gap:** the log stores only `source_ip`. A session-assigned VPN pool address names one person
  only with a time plus the gateway's allocation record (IETF RFC 6302, NIST SP 800-86). Without
  it, "who else was on this VPN address at that moment?" cannot be answered, and co-users of a
  pool address cannot single anyone out. The dataset's own runbook step 6 asks analysts to
  compare session allocation times before drawing a connection.
- **Ruling:** add nothing now. The allocation record is a possible future capability for phase 3
  (travel and network facts), which the scope ruling of 20 October 2026 keeps outside this
  initiative's requirements.
- **When reopened:** agree the investigation question it serves first, then the synthetic
  allocation log's shape, generator and answer-key changes, graph edges and eval questions, in
  that phase's own spec. Registration authorises no dataset, spec or implementation change.

## Longer-term capabilities already named in the spec

These are future ideas, not approved implementation work. Each needs its own scope, design and
acceptance criteria. See the [spec](../../.scratch/v2-port/spec.md), future seams and Out of Scope.

| ID | Capability | Existing architectural seam | Status |
| --- | --- | --- | --- |
| AUD-015 | Retrieval-augmented generation | Central tool list | In progress: knowledge-base initiative, `.scratch/knowledge-base/` |
| AUD-016 | Knowledge graph | Data access in the core | In progress: knowledge-base initiative, `.scratch/knowledge-base/` |
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
| 2026-10-30 | Added AUD-067 and T46 graph foundation review; T25/T27 held. T02 and the current spec preserved pending a new ruling. | Author's approval to create the decision ticket; T46 scope and proposed proof |
| 2026-10-29 | T24 resolved: first graph tool, shared checked lifecycle, fenced results and saved artifacts, approved browser compatibility. AUD-065 measurement recorded; AUD-066 added for the one failed Q04 check. Known AUD-061 cleanup recurrence retained with exact cleanup and clean reruns. | T24 evidence; 24 review; 677 backend assertions, 150 frontend; Port API 62/63 and security 15/15 |
| 2026-10-29 | Author approved AUD-065's four bounded T24 checks; ticket criteria and spec updated. Broader storage design remains deferred. | Author confirmation in chat; T24; spec Testing Decisions and decisions log |
| 2026-10-29 | Added AUD-065 at the author's request: defer evidence-storage scaling decisions; record current report persistence and propose bounded T24 measurement. No spec change or implementation approved. | Discussion before T24; investigations, agent and PDF-route source inspection |
| 2026-10-26 | Reopened AUD-047 after T14's safety-net eval: Q02 run 3 again reports no S6 successes; Q02 2/3, Q04 3/3, overall 62/63 and security 15/15. Agent unchanged; behaviour work stays outside T14. | B-076 recurrence; `2026-10-26-202907-b70d0745.json` |
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

| 2026-10-20 | Added AUD-031: the agent's model retires on 14 January 2027. Recorded only; no model chosen. | P-121; OpenRouter service notice |

| 2026-10-20 | Knowledge-base ticket 02 resolved: PostgreSQL chosen as the one store. Added AUD-032 (memory to PostgreSQL, parked), AUD-033 (incremental sync, future), AUD-034 (Intel-Mac wheel check, lesson). AUD-015 and AUD-016 marked in progress. | Knowledge-base ticket 02 Answer; research note 02 |

| 2026-10-21 | Knowledge-base ticket 03 research done, awaiting the author's grilling. Added AUD-035 (Cohere Rerank 5 watch item). AUD-034 noted as applied once. The author ruled out local models. | Knowledge-base ticket 03 comments; research note 03 |

| 2026-10-21 | Added AUD-036: Langfuse as a candidate trace and eval-result store, three months of free access held by the author; decided in ticket 06. | Author |

| 2026-10-21 | Knowledge-base ticket 03 resolved: seven decisions on refusal path, embeddings, chunking, identifiers, re-ranker, metadata filters and fusion. Frontier moves to ticket 04. | Knowledge-base ticket 03 Answer; map |

| 2026-10-22 | Added AUD-037 to AUD-039 (attack scenarios, benign look-alikes, row signals and baseline) after the author asked whether the Port's planted scenarios suffice for a product. Each names what knowledge-base ticket 04 takes now and what stays future. The author accepted re-pointing the Port's tests and eval to a regenerated log. | Author; discussion before ticket 04 |

| 2026-10-22 | Knowledge-base ticket 04 resolved: seventeen decisions on the synthetic organisation, the stories, the corpus, the dataset folder and the truth file. AUD-037 to AUD-039's "taken now" items confirmed (S6, the MFA column, three twins). Frontier moves to ticket 05. | Knowledge-base ticket 04 Answer; map |

| 2026-10-22 | Knowledge-base ticket 05 resolved after a discussion, research note 05 and a fourteen-question grilling: five rulings (purpose, playbook in code, chat entry point, conversation then report, code does the deterministic work) and sixteen decisions (seven tools, bundled investigation package, content plus artifact, content-computed IDs including a stable finding ID on the Alerts API, label citations resolved in code, two answer checks, fencing middleware with canaries, middleware plan, tool choice as shortcut rule, report gate, caps, parallel calls, playbook as one list, rules unchanged, no context field). Added AUD-040 (structural escalation seam) and AUD-041 (structured answer option). Frontier moves to ticket 06. | Knowledge-base ticket 05 Answer; research note 05; map |

| 2026-10-22 | AUD-032 parking reaffirmed by the author; trigger to reopen set to phase 2 (history), when past investigations become knowledge. | Author, after ticket 05 |
| 2026-10-24 | Knowledge-base ticket 07 resolved, prototype first then an eight-point grilling with the prototype open, plus a ninth decision the author raised: the chat is the screen with a finding ID column on Alerts; citations in an evidence panel built from the artifact and downloadable; one line per hop; radii as counts first; the investigation tool's steps stack while running (an exception to AUD-027, noted on its row) with a build condition to study Anthropic's and OpenAI's progress patterns; letters L, G, D; judge's reason off the screen; a five-level visual hierarchy. Added AUD-043 (judge's reason on screen, parked with a trigger). All decision tickets resolved; frontier moves to the spec. | Knowledge-base ticket 07 Answer; prototype; map |
| 2026-10-25 | Knowledge-base spec for phases 0 and 1 written. AUD-033 gained its trigger to reopen (a full rebuild too slow or costly per change), raised by the author while ruling the spec's staleness guard. | Knowledge-base spec, decisions log |
| 2026-10-25 | Knowledge-base ticket 09 built (PostgreSQL with pgvector, the loud test fixture). Added AUD-044 (sweep of test databases left by a killed run, parked with a trigger), from the ticket's spec review. | Knowledge-base ticket 09 |
| 2026-10-23 | Knowledge-base ticket 06 resolved after a discussion, research note 06 and a ten-question grilling: two hard retrieval checks per question (top 20 and the 5 the model received), exact-set graph gate, a mix weighted to say-no and mixed questions, a separate tuning file for the refusal threshold, citation resolution with gold IDs as the answer gate, the judge as a smoke alarm with three trials and stored verdicts, playbook and canary checks as 100% gates, one scorer with two exams kept separate, on-versus-off comparisons for the re-ranker and BM25, and Langfuse adopted as a mirror. AUD-036 decided. Added AUD-042 (injection-detector middleware, parked with a trigger). Frontier moves to ticket 07. | Knowledge-base ticket 06 Answer; research note 06; map |
| 2026-10-26 | Knowledge-base T10 resolved: default dataset folder and unchanged Port exam verified. Recorded Explorer timeout recurrence and passing 149-test rerun (AUD-028), repeated count error (AUD-030), and narrow spraying-answer failure (new AUD-045). No agent changes; Port eval meets gates at 55/57 overall and 15/15 security. | T10 Answer; B-066/B-070/B-073; `2026-10-25-221147-7ff8e5ae.json` |
| 2026-10-26 | Knowledge-base T11 resolved: organisation tables and two internal log columns, Port rows byte-identical in their old columns, tools and API unchanged. Port eval meets gates at 53/57 overall and 15/15 security. Recurrences of AUD-030 (Q07) and AUD-045 (Q08 runs 2 and 3); new AUD-046 (Q04 run 3 skipped reputation lookups). | T11 Answer; B-070/B-073/B-074; `2026-10-26-095844-7ff8e5ae.json` |
| 2026-10-26 | T12 eval meets gates at 58/63 overall and 15/15 security; S6 questions 6/6. Recorded B-074/AUD-046 recurrence in all Q04 runs and new B-076/AUD-047 for broad spraying outcome/count omissions. Existing six frontend lint warnings persist as AUD-009. | T12; `2026-10-26-112540-7ff8e5ae.json` |
| 2026-10-26 | T13 finding IDs in the core; agent, tools and API unchanged. Port eval meets gates at exactly 57/63 (90%) and 15/15 security. Recurrences of AUD-046 (Q04 0/3) and AUD-047 (Q02 now 0/3), noting the gate's zero margin. Added AUD-048 (finding ID and the detection tool, for ticket 32). | T13; `2026-10-26-131223-7ff8e5ae.json` |
| 2026-10-26 | T43 restores the Port eval's margin: lookups enforced in the detection hook, the agent's view carries address outcomes with a code-built success sentence, Q02 and Q04 gain S6 checks. Three paid runs; the third meets gates at 62/63 and 15/15 with Q02 3/3 and Q04 2/3. AUD-046 and AUD-047 closed pending the author's acceptance; added AUD-049 to AUD-052; note on AUD-048. | T43; `2026-10-26-181909-b70d0745.json` |
| 2026-10-27 | T15 brief and corpus consistency script built and reviewed. Added AUD-055: the checker's limits on invented prose names and the no-technique-ID trait, left to the author's T16 read. | T15; B-083; `reviews/15-code-review-2026-10-27.md` |
| 2026-10-27 | T16 corpus copied in and checked; author ruled chunking proposals P1 to P4c. Added AUD-056: ATT&CK source references as provenance metadata, a future enhancement. Closed AUD-055 on the T16 scans and the author's approval of the documents. | T16 ticket; spec "Chunking rulings at T16" |
| 2026-10-27 | T17 build command delivered: 40 documents, 320 chunks, 257 organisation mentions. B-084 to B-088 fixed with regression evidence; two-axis review cleared. Added AUD-057 for retained successful build databases. Final safety net: 571 backend, 149 frontend, clean types, Port API eval 63/63 overall and 15/15 security. Six existing lint warnings (AUD-009) remain; no parked behaviour concern reopened. | T17; `reviews/17-code-review-2026-10-27.md`; `2026-10-27-160038-b70d0745.json` |
| 2026-10-28 | After T18, the author ruled one reading rule for every `LI_` setting and opened T44, the phase 0 cleanup, blocked by 28 and blocking 29. AUD-057, AUD-058 and AUD-059 scheduled there; each still needs its own ruling inside T44. | Spec decisions log, 28 October 2026; `issues/44-phase0-cleanup.md` |
| 2026-10-28 | T18 staleness guard built and reviewed. Added AUD-058 (chunking code outside the fingerprint) and AUD-059 (two readers of `LI_DATASET_DIR`), both unresolved review concerns. Final safety net: 585 backend, 149 frontend, clean types, Port API eval 63/63 overall and 15/15 security. Six existing lint warnings (AUD-009) remain; no parked behaviour concern reopened. | T18; B-089, B-090; `reviews/18-code-review-2026-10-28.md`; `2026-10-27-224010-b70d0745.json` |
| 2026-10-28 | T19 graph and exact S6 radius verified: 612 backend, 149 frontend, clean types, zero findings per review axis, Port API eval 61/63 and 15/15. AUD-060 closed; AUD-061 registered for T44. AUD-047 recurrence is S2 outcome omission, not an S6 zero-success claim. | T19; B-076 and B-091 to B-095; 19 review and evidence |
| 2026-10-29 | T23 re-ranker behind its switch. Added AUD-063 (one OpenRouter reader and one `.env` test guard) and AUD-064 (kept-5 check and calibration evidence for T39 and T41). AUD-062 note: the re-ranker keeps K04's runbook at rank 1; the MFA register is still absent. | T23; B-101; `reviews/23-code-review-2026-10-29.md`; `2026-10-29-150414-681065-retrieval-0331ac624577.json` |
| 2026-10-31 | Added AUD-070 at the author's request: Pydantic Evals potential value, recommendation to defer, and a bounded comparison trial before any adoption decision. | Author and Codex discussion; official Pydantic documentation |
| 2026-10-31 | Added AUD-071 at the author's request: park operator passage-text inspection by graph passage ID. Display location remains undecided; no expansion of T49 or implementation approval. | Author; T48 learning walkthrough |
| 2026-10-31 | Author-approved import-only cleanup fixed 102 Ruff diagnostics in 76 backend files; import and type checks plus 150 frontend tests pass. Backend run interrupted after 373 passes and one graph query failure; isolated rerun failed on Neo4j readiness. AUD-013 remains open; B-124/AUD-072 record the verification gap. Test processes ended and only the pre-existing retained walkthrough graph container remains. | Author; import cleanup verification |
| 2026-10-31 | At the author's request, investigated AUD-072 and completed verification without application or service-setting changes. Diagnostic and normal focused reruns pass; full backend 701 passed in 957.38 seconds. Import cleanup verification gap resolved; intermittent failure remains open with root cause unproven. Test resources cleaned up; retained inspection container preserved. | B-124; AUD-072 follow-up |
| 2026-10-31 | Closed AUD-012 after the author's backend-interpreter selection cleared Pylance's import warning. For AUD-013, the author chose 12 reasoned line-level BLE001 exceptions; comments only, syntax trees unchanged, lint and detection probe pass. 115 other diagnostics remain; no project-wide rule disabled. | Author confirmation and selected option; Ruff verification |
| 2026-10-31 | Closed AUD-013 after applying the approved policy: Ruff 0.17.3 pinned, twelve style preferences relaxed, remaining intentional patterns clarified and seven cleanup items handled. Full-policy Ruff and backend types clean; backend 701 passed in 993.52 seconds, frontend 150 passed. Admin commands tested; B-125 corrected and recorded. Only the retained inspection graph remains; no test process remains. | Tooling ticket 01; admin manual section 7; author approval |
