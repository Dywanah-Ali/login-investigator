# Conversation isolation investigation

Date: 18 October 2026. Source: author concern and P-060.
Status: diagnosis completed; no application or live-history changes.
Related register item: [AUD-020](improvement-register.md#aud-020-answer-completeness-versus-stored-memory).

## Finding

No evidence of conversation-history mixing was found in the inspected code, saved conversations
or offline model-input probe. The tested application path passes only the selected conversation's
history to the model. The three live conversations with the repeated recap question each already
contained Daniel's details in their own earlier evidence or report.

The evidence supports repeated discovery of the same dataset findings plus overly narrow recap
scope. It does not establish the model's private reasoning or guarantee every possible execution.
There was no fresh paid model replay and no historical outbound-request trace to inspect.

## Boundary between shared data and private conversation context

Think of each Investigation as a separate case folder. Every folder can consult the same sign-in
ledger. Finding Daniel in several folders does not mean one folder was read into another.

| Part | Shared between Investigations? | Evidence |
| --- | --- | --- |
| Synthetic sign-in log and saved reputation responses | Yes | Startup supplies one dataset to the three read-only tools. |
| Agent configuration and model client | Yes | Startup builds one agent and model client. |
| Checkpointer storage file | Yes | One SQLite file stores histories under distinct thread IDs. |
| Conversation messages supplied for a question | Selected thread only in the tested flow | Question route supplies the matched case ID; agent uses that ID as checkpoint configuration. Model-input probe confirms separation. |
| Transcript supplied for a report | Selected thread only in the tested flow | Report builder reads state using the case ID; probe checks both report inputs. |
| Browser history list | Visible to the user | Frontend fetches summaries for navigation. The list is not sent to the model as question context. |
| Tool for reading other Investigation histories | None in the current tool list | Tools are detection, sign-in search and IP reputation. |

This is context separation within a single-user app, not a claim about authentication or access
control. The app intentionally lets its user reopen saved Investigations.

## Live conversation comparison

The read-only list contained nine Investigations. Three contained the recap question; one repeated
it twice. Only the relevant facts are recorded here rather than copying all conversation contents.

| Investigation ID | Starting question | Evidence already in that same conversation before the recap |
| --- | --- | --- |
| `872227a3ca7948748f7b4f1ec57ee6c3` | Which IP addresses attacked us, and how bad are they? | Detection output names Daniel. Its saved report also names Daniel before the recap. |
| `9f06429702864efca91a6fab8f7c1517` | Was any account compromised this week? | Detection output, answer, named-account follow-up and report all contain Daniel. |
| `38b15638e0bd432fbe49206c902ce985` | Anything suspicious last night? | That night's detection output and first answer already describe Daniel, before either recap. |

Therefore, none of the observed Daniel recaps requires information from another conversation.
The last-night case also covers a different period from the weekly case; its account coverage
should not be expected to match the weekly case automatically.

The weekly case still contains Olivia's new-country finding and 35 password-spraying targets.
Their absence from a case-wide recap is a separate scope/completeness concern, B-060. The question
uses singular “account” and the prompt favours the most recently discussed user/IP. These are
plausible contributors to narrowing, not proof that the model used a particular reasoning path.

## Code trace

1. The frontend reads the selected `id` from the URL. Sending a question posts its text to
   `/api/investigations/{id}/ask`; it does not attach all browser histories.
2. The API matches that ID to a known case, then passes `case.thread_id` to the core agent.
3. The core's `_config` sets `configurable.thread_id`. Question execution and history reads both
   use that configuration. New case IDs come from independent UUIDs.
4. Report creation retrieves only that ID's messages, creates its transcript, then writes the
   report back into the same thread.
5. Frontend history state is tagged with its case ID. Navigation cancels the previous operation;
   the existing navigation tests cover both answer and report operations.

Sources:
[frontend hook](../../frontend/src/hooks/use-investigation.ts),
[API routes](../../backend/api/investigation_routes.py),
[core agent](../../backend/login_investigator/agent.py),
[case storage](../../backend/login_investigator/investigations.py),
[services](../../backend/api/services.py),
[tools](../../backend/login_investigator/tools.py).

## Model-input isolation probe

A fake model captured the messages it actually received through the real API routes, agent and
SQLite checkpointer. This is stronger evidence than checking only that saved records have different
IDs. The fake model does not demonstrate semantic answer quality.

Procedure:

1. Create three temporary cases with different unique markers absent from the shared log.
2. Ask in case A, then case B. Check each model input contains its own marker and no other marker.
3. Generate separate reports for A and B. Check their report inputs and saved titles are separate.
4. Alternate unnamed follow-ups between A and B. Confirm their own history and report remain in
   context and the other case's marker never appears.
5. Ask the first question in case C. Confirm neither earlier case's marker is supplied.
6. Stop and recreate the application against the temporary database. Repeat follow-ups in A and B
   and check the same boundary again.

Result: PASS. Three cases, seven captured question-model inputs, two captured report inputs,
zero cross-case marker leaks. Outbound socket connections were blocked. All writes were to a
temporary SQLite file that was removed afterwards. No real model was constructed or called.
No key or raw real conversation content is written by the probe.

Reproduce from `backend/`:

```sh
uv run python ../docs/audit/evidence/conversation_isolation_probe.py
```

[Probe source](evidence/conversation_isolation_probe.py) reuses the existing fake-model fixture.
It is an audit diagnostic, not a benchmark or a replacement for the test suite.

## Existing focused checks

| Check | Result |
| --- | --- |
| Core: separate case memory | Passed |
| Core: history survives restart | Passed |
| API: history/report/PDF survive restart, offline PDF works | Passed |
| Frontend: navigation during answer cancels old operation | Passed |
| Frontend: navigation during report cancels old operation | Passed |

Backend: three tests passed in 7.58 seconds. Frontend: two targeted tests passed; 18 unrelated tests
were skipped by the name filter. No new application test file or application code was added.

## Follow-up

Keep AUD-020/B-060 open for whole-case versus focused-account recap behaviour. Do not attempt to
fix unproven history leakage. If a future answer mentions a unique fact absent from its own saved
history and absent from its available dataset/tool outputs, preserve that example for a new
boundary investigation. The separately recorded workflow, injection-reporting and timeline issues
remain open. Ticket 19 is not closed by this diagnosis.
