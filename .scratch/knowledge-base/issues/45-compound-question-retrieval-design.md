# 45: Retrieval for compound questions, in chat and in the package

Type: research, then grilling
Status: resolved
Blocked by: 52
Blocks: 25, 26, and the initiative's retrieval gate (AUD-062's closure)
Phase: 0
Model: strongest (Fable 5.1 or Astra)

Investigator contract: [IC-01/02 scope and authority, IC-05/06 evidence and preservation,
IC-07/08 uncertainty and workflow, IC-10/11 security and proof](../../../docs/investigator-contract.md).
These are inherited approved requirements. This ticket decides retrieval mechanisms and
guidance sources; it does not reopen those requirements or certify their implementation.

Opened by the author's ruling of 29 October 2026, after T23. The retrieval-design work parked at
T23 is significant enough for its own ticket. This is a decision ticket: it produces rulings,
not code. The author reaffirmed this boundary on 8 November 2026. Implementation is handed
to two additional build tickets after the design is settled, with existing T25/T26 ownership
reconciled explicitly rather than duplicated.

## Current disposition — resolved, 8 November 2026

Closed after the author's request to close T45, following approval and publication of the
seven-slice implementation handoff. The Answer below consolidates all six original decisions
and closure evidence. Older claimed/frontier/next-step statements are chronological history.
This closes design and ownership only. No application implementation, runtime acceptance,
source ingestion, paid run, commit or push is authorised by closure. AUD-062/AUD-086 stay open.

## Planning and implementation split — author ruling, 8 November 2026

**Latest author ruling, 8 November 2026:** defer implementation-ticket planning to a fresh
session and use the to-tickets skill. Choose the number of tickets from clear responsibilities,
dependencies and independently testable outcomes; do not force the previously proposed two.
This supersedes every fixed two-ticket requirement below, including the acceptance criterion.
Reconcile T25/T26/T28 and evaluation ownership before adding work; avoid duplicate ownership
and excessive fragmentation. All five closing design decisions are approved. No build release.

**Discussion-depth correction, author, 8 November 2026:** stop the fine-grained execution-limit
walkthrough. The author explicitly identified graph scan limits/overflow as excessive detail
and rejected continuing for hours through similar items. Do not present each numeric budget,
retry count or routine failure case as another approval question. Consolidate those details
as implementation responsibilities constrained by the accepted scope, evidence-preservation,
bounded-execution and truthful-outcome rules. Unselected numbers remain unselected, not
implicitly approved or verified. Surface only decisions that materially change architecture,
product behaviour, scope, evidence guarantees or acceptance gates. Do not treat this process
correction as implementation authorisation or a waiver of unresolved responsibilities.

Next: consolidate the remaining architecture-level choices and implementation dependencies
in one bounded pass, then proceed to the already-agreed scoped LangGraph research and
architecture review. Do not require a numeric-limit approval tour before that research.

T45 owns planning and decisions only. Complete the roles, request/response contracts and
execution boundaries first. Then conduct one scoped research pass on LangGraph orchestration
for the overall investigator workflow, using that concrete agent design as the research input.
Research covers workflow state, research-request dispatch, required checks, bounded follow-ups,
failure handling and conversation persistence. Establish where LangGraph helps and where code
should control behaviour directly; no graph topology or framework migration is adopted yet.
Bring the findings back into T45 and settle the orchestration design before the agreed
`roast-technical` review. That review therefore examines the complete proposed workflow.

After review findings are resolved or explicitly deferred, hand implementation to two additional
tickets. The provisional split is research-agent implementation (request handling, retrieval,
response construction and evidence preservation) and investigator orchestration implementation
(chat/research coordination, state, required checks, stopping and final-answer handoff).
Final ticket boundaries and acceptance criteria follow the completed design; no build is
authorised by this sequencing decision.

Existing ownership checked on 8 November 2026:

| Existing ticket | Responsibility to reconcile before creating the build tickets |
| --- | --- |
| T25 | Read-only peer and corpus-search tool interfaces over shared core functions. The research-agent ticket must not independently rebuild these tools. Final tool exposure follows T45. |
| T26 | Deterministic investigation package, required evidence/check outcomes, selection, citations and per-step progress. The orchestration ticket must not duplicate this coordinator or move its factual duties into model judgement. |

T25/T26 remain blocked by T45. Record any final responsibility transfers and dependency changes
in all affected tickets and the spec before implementation. IC-01–11 and existing evaluation
gates remain inherited requirements. Design approval and external research are not runtime proof.

## Scoped orchestration research completed — 8 November 2026

Following the author's approval to proceed without a numeric-limit walkthrough, saved the
[consolidated brief](../research/45-langgraph-orchestration-brief-2026-11-08.md) and
[LangGraph findings](../research/45-langgraph-orchestration-2026-11-08.md).
Perplexity discovery and eight official sources informed the findings; Keenable unavailable.
Installed LangChain 1.3.1/LangGraph 1.2.4/checkpoint 4.2.0/SQLite saver 3.1.1 match the lock.
Read-only installed-source and current-consumer checks supply integration context, not runtime proof.

**Architecture approved by the author, 8 November 2026:** use a thin explicit parent workflow
around the approved chat/research roles. Code owns assignment validation, required-work
enforcement, independent dispatch, result validation and evidence assembly. Research runs
with isolated per-invocation working state; the conversation retains persistent parent state.
Keep normal chat clarification and current persistence infrastructure. No extra supervisor
model, separate service or long-term research memory is proposed. This is a project-specific
recommendation supported by documented mechanisms, not a measured reliability improvement.

The alternative is a main agent calling research as a tool with equivalent code-enforced
boundaries. It is viable; explicit workflow is recommended because mandatory stages are
visible and testable instead of distributed across wrappers/middleware. Framework choice
does not replace plain core functions or prove semantic evidence sufficiency.

Retain three implementation obligations: expected worker failures must become honest outcomes
for partial-result assembly; resume/replay must preserve assignment/source identity and avoid
uncontrolled repeated operations; existing streaming/report/history and case-writer interfaces
need explicit compatibility. Checkpointing is not an immutable evidence archive or exactly-once
execution. Node names, budgets and routine error cases do not require separate author rulings.

Author also accepted create_agent for bounded research workers, behind the existing central
construction seam. Use plain model calls for individual chat stages where no agent loop is
needed. Deep Agents is not adopted. Future specialist workers may fit behind the same
validated contracts; no additional agent roles or infrastructure are authorised now.
The scalability and harness comparison is saved in the findings note's follow-up.

The agreed single roast-technical review is now complete:
[five-persona council and Judge verdict](../reviews/45-architecture-council-2026-11-08.md).
GO for the architecture, medium confidence, no demonstrated P0/P1 blocker. Lower observations
are retained in its ledger and AUD-086: full-investigation activation/shared obligations,
public-answer streaming boundaries, request/answer association, child cancellation ownership
and saved-case/evidence compatibility. These refine the existing handoff obligations; they
do not reopen the approved architecture or demand another review round.

Current frontier, 8 November 2026: all five closing design decisions are approved, including
prompt examples, guidance sources, retrieval acceptance and keyword disposition. Reconcile
implementation-ticket ownership and dependencies next. T45 remains claimed and AUD-062 open;
no code, inference, dependency change, migration or implementation release.

## T52 scope handoff — 2 November 2026 (inherited baseline)

Author confirmed reliable login investigation as the sole phase-0/1 objective, with bounded
account-impact and directly connected activity context. Standalone full inventory, exhaustive
permission-path presentation and reverse asset exposure are deferred. This supersedes broader
product-scope wording below. See [spec Current scope ruling](../spec.md#current-scope-ruling--t52-2-november-2026).
Detailed criteria below carry the approved T52 boundaries. Open design decisions remain
explicit; this reconciliation does not release T52 or authorise implementation.
Existing source code, questions, gold and thresholds are not changed or waived by this note.

## Question

How does the knowledge base find every passage a compound question needs, such as K04 ("what
happened in S6, and what does it reach"), when the evidence sits in different documents?

The question has two paths, and the answer may differ for each:

1. **The chat path.** The analyst can ask anything; the app cannot force a style of question.
   The model reads the question and writes the search through `search_corpus(question, ...)`
   (spec, T05 d1). It may send one long search or several focused ones; nothing in code
   decides. T22 showed one long search losing K04's MFA register: the keyword leg returns
   nothing when every term must match, and the register falls to dense rank 115.
2. **The package path.** `investigate_alert` builds its clearing and aggravating searches in code
   from the finding's record, never from the chat (spec, T05 R5). Here the search templates
   decide coverage, and text cannot steer them. That protection stays.

## What to decide

1. **What K04's gate measures.** The analyst's raw question, the package's code-built searches,
   or both, each as its own check. The original questions and gold stay unchanged; a change to
   what a gate measures is a spec change and needs the author's ruling.
2. **The chat path.** Where splitting a compound question belongs, if anywhere: in the model's
   instructions or a focused skill, in `search_corpus` itself as a guard against a long
   question, or nowhere until the stronger-model comparison (AUD-031, P-03). The architecture is
   not shaped around the current model's weaknesses (P-03).
3. **The package path.** Which searches T26 must build from a finding so that every playbook
   step's evidence is covered, and how that coverage is tested.
4. **Keeping what was found.** Whether evidence already retrieved for one need can be lost when
   results are merged or cut to five, and what protects it. T22's experiments showed both risks.
5. **The keyword leg.** Whether all-terms-must-match keyword search is right for long questions,
   or whether T41's BM25 comparison settles it.
6. **Retrieval boundaries by subject.** Decide whether MITRE ATT&CK, HR-related documents
   and other corpus subjects need different query construction, filters, retrieval methods
   or result formats. Separately decide whether any specialised retrievers should sit behind
   the shared `search_corpus` tool or be exposed as separate agent tools. One agent tool does
   not require one identical internal retrieval method. Compare the existing shared-tool
   baseline with subject-specific alternatives rather than assuming either is superior.
   Keep structured owner/department/group lookup through `lookup_account` distinct from
   HR document search; its existence is not evidence for splitting document retrievers.
   Examine both single-subject and cross-subject questions, including attack guidance plus
   an internal exception. Consider routing errors, evidence coverage, merge/cap losses,
   troubleshooting, evaluation and any actual access requirements. Subject filters and tool
   names are not access controls; any required permissions must be enforced in the backend.

## Inputs (research already done, none of it adopted)

- [Retrieval recovery research](../research/22-investigation-retrieval-recovery.md):
  decomposition, sufficiency, omitted needs, bounded recovery, preserved access and scope.
- [Fixed-budget experiment](../research/22-retrieval-experiment-results.md): focused queries
  keep both K04 passages; a broad route with equal fusion drops the register to rank 25; a
  human-chosen retry restores it. Recovery used human knowledge of the gold.
- [Evidence checklist design and offline replay](../research/22-evidence-checklist-design.md):
  fair turns recover K04 from saved lists but fail in two of six route orders and under a
  five-passage cap.
- T22's focused-query probe (T22 ticket, follow-up exploration): human-written queries find
  the register at rank 7 or 2 and the runbook at 1.
- T23's live runs: the re-ranker keeps K04's runbook at rank 1; the register is never scored,
  because it is not among the fused 20 (AUD-062 note).
- AUD-062 (the gap), AUD-064 (kept-5 check and calibration), B-098, P-03 in `PRINCIPLES.md`.

## Acceptance criteria

- [x] After contracts and execution boundaries are concrete, complete the scoped LangGraph
      orchestration research above, save its findings, and record the resulting design rulings
      before `roast-technical`. Check relevant installed versions and primary documentation;
      distinguish supported mechanisms from recommendations and unresolved local questions.
- [x] After the design review, use to-tickets in the fresh session to define an appropriate
      number of implementation tickets with explicit ownership,
      dependencies and acceptance criteria reconciled with T25/T26. Assign runtime verification
      to build/evaluation owners; T45 closes on design decisions and handoff, not runtime success.

- [x] Discuss agent prompt examples separately after the contract structure is defined.
      Selection evidence: approved role-specific cases in the 8 November section above;
      wording and runtime evaluation remain implementation work.
      Distinguish documentation examples from examples selected for actual prompts. Select
      chat-agent examples for intent classification/request construction and research-agent
      examples for tool-work boundaries/result examination/contracted responses. Consider
      ambiguous requests, missing information, multiple intents and failed retrievals as well
      as successful cases. Record selections and the evaluation needed to establish their
      value; do not automatically copy documentation examples into either prompt. Example
      counts and any new evaluation execution remain undecided.

- [x] Author-requested pre-implementation design review: once T45's proposed agent roles,
      intent/evidence mappings, request/response contracts, execution boundaries and the
      research-informed orchestration design are concrete,
      run `roast-technical` once before implementing the resulting design. Review the context
      benefit versus added complexity, role clarity, contract failure modes and evidence
      preservation. Verify council claims against T52, the investigator contract and actual
      project evidence; bring material findings to the author for rulings. The review does not
      reopen settled requirements, establish runtime proof, or authorise implementation or
      paid experiments. This added review is specific to T45's new delegated-agent architecture
      and its handoff risks, not a new review requirement for every downstream ticket.

- [x] Map search needs to E01–E06: activity, bounded account impact, supporting and competing
      evidence, applicability and uncertainty. Specify downstream tests for partial explanations, including
      travel that does not explain separate attack activity. No standalone inventory task.
- [x] Define how to record candidate, reranked, retained and model-visible evidence separately. Specify downstream tests for loss
      during merging and caps, not only first-hit rank. Original K04 questions/gold remain;
      apply the author's explicit 8 November acceptance-path/AUD-062 closure revision below.
- [x] Map each relevant document subject to its actual retrieval needs. Record separate
      rulings for internal retriever boundaries and agent-facing tool boundaries, with
      evidence or explicit remaining uncertainties. Include subject-specific and cross-subject
      evaluation needs, routing and stage-level diagnostic evidence. Reuse existing evidence
      where sufficient; no paid comparison is authorised by this criterion. Any proposed
      tool/spec change needs author approval before adoption. Carry approved shared-core
      boundaries into T26 without duplicating retrieval logic in `investigate_alert`.
- [x] Select a small E06 guidance source set for the author's review. Map proposed passages
      to case uncertainties and record provenance and applicability. Consider existing
      corpus sources first; previously consulting NIST SP 800-61r3 does not adopt it wholesale.
      Obtain the author's source approval before ingestion/use, then define T26's retrieval
      handoff. A general practice passage cannot establish that a case event occurred.

- [x] Before any work starts, the agent tells the author this ticket's `Model:` line and waits
      for the author to confirm the model is set; a dated comment records it.
- [x] Research uses the author's revised 7 November method: Perplexity with primary-source
      checks, findings saved in research notes. Keenable was unavailable and was not used.
      The dated author-method ruling in Comments supersedes the original two-tool wording;
      this completion does not claim a Keenable run.
- [x] Each of the six numbered decisions above has a ruling recorded under the Answer, or an explicit
      deferral with its reason and owner ticket.
- [x] Any change to what a gate measures, or to the spec, is proposed first, ruled by the author,
      and recorded in the spec's decisions log.
- [x] T26's criteria are updated to match the package-path ruling before T26 is built.
- [x] AUD-062 is updated with the rulings. It closes only on the evidence its own entry demands.

Closure evidence for these design criteria is indexed in the Answer below. Checked boxes
do not certify implementation or downstream evaluation success.

## Request contract: consolidated design, 8 November 2026

### Full investigation versus narrow lookup — approved, 8 November 2026

8 November 2026. First of the five remaining decision areas, taken individually at the
author's request. IC-03–08 and the existing full-investigation/playbook requirements are
inherited. The author approved changing the activation mechanism formerly defined by tool choice.

Retain an explicit full-investigation versus narrow-lookup choice in the parent
workflow before research assignments are dispatched. Chat interprets the user's wording and
conversation context; code resolves the target/scope and retains the selected workflow mode
and its basis. An explicit user workflow action can supply that choice directly. No new screen
or mandatory confirmation on every question is proposed. Clarify material ambiguity or missing
target identity before executing; a keyword detector alone is not a sufficient classifier.

Examples: "Investigate this alert" and a case-level "Is this a threat?" use the full procedure
under existing rules. "Who owns this account?" or "Show this policy" remains a bounded lookup.
A new narrow follow-up does not erase outstanding work in a previous full investigation, nor
does an old full-investigation choice automatically turn every later question into a full run.

For a full investigation, code instantiates obligations from the one core playbook/procedure
definition rather than from the model-selected task list. This retains triggering/surrounding
activity and coverage, account significance/bounded access, applicable connected activity,
supporting/competing documentary evidence and relevant guidance/gaps under the approved
contract. Applicability and missing inputs remain explicit. Research may add permitted focused
follow-ups but cannot delete or downgrade those obligations. Failed required work remains
visible; neither the worker nor a polished answer can certify it complete.

Preserve the existing full-package protection: required baseline clearing/aggravating searches
come from resolved finding/event facts and the core procedure, not arbitrary chat text. Research
refinements supplement rather than replace those searches. The obligation mapping below
consolidates inherited requirements, without permission to invent telemetry or scope.
Narrow lookup runs only its assigned evidence needs, with the same provenance/security rules.

The workflow mode belongs above the six-intent research request contract. A full procedure
can produce one or several valid requests, each retaining exactly one approved intent, with
shared parent obligation accounting. Do not add a seventh research intent or overload focus
text to activate a hidden full procedure. Full/narrow is scope of work; the intent describes
the purpose of an individual research assignment.

Code can prevent later task omission from shrinking a recognised full procedure. It cannot
prove that chat classified the original user request correctly. Retain classification examples
and existing workflow/evaluation coverage for that boundary, including full questions mapped
incorrectly to narrow assignments. The cheapest council check tests enforcement after full
mode is known; it does not prove natural-language classification quality.

This approval supersedes the legacy spec rule that actual tool choice alone identifies
full mode. It preserves the single shared procedure and full/narrow behaviour, and needs no
extra supervisor model. Spec and T26/T28 handoffs record this ruling before implementation.

### Full-procedure obligation mapping — consolidation of inherited requirements

Code derives baseline collection/search inputs from the resolved target, recorded activity,
approved period and the shared procedure. The table is a responsibility mapping, not new
telemetry, a fixed number of tool calls or a second playbook. Narrow queries use only assigned
needs. Applicable required checks cannot disappear because a model omitted their task.

| Required evidence area | Existing task/capability mapping | Baseline and limitation rule |
| --- | --- | --- |
| Trigger and surrounding activity, IC-03 | retrieve_triggering_activity; retrieve_surrounding_activity; coverage returned with both | Code resolves alert/events and derives the approved default or explicit window. Preserve failures/successes, counts/sequence and requested versus available coverage. Separate coverage task only for an independent coverage question. |
| Account significance and bounded impact, IC-04 | retrieve_account_context; retrieve_relevant_access | Use target-derived accounts and the procedure's relevance rules; preserve recorded role and supporting permission paths. Snapshot permissions do not establish access at event time. |
| Directly connected activity, IC-04 | retrieve_same_source_activity; retrieve_shared_device_activity | Derive involved sources/devices from target records and use the authorised window. Missing usable identifiers and unavailable data stay explicit. Do not infer all historical devices, common control or restored address-sharing exposure. |
| Supporting and competing explanations, IC-05/06 | retrieve_explanation_evidence through organisation-rule and case-context searches | Required baseline clearing/aggravating searches use code-built, source-grounded inputs. Account/event context and conditions matter; a travel explanation cannot clear separate attack activity. Research may supplement these searches but not replace or suppress required sides. |
| Threat context, IC-05/07 | retrieve_threat_guidance through threat-knowledge search | Select relevant reference needs from recorded activity and the procedure, without claiming a technique occurred merely because a reference matched. Preserve uncertainty and competing explanations. |
| Unanswered questions and next steps, IC-07 | Explicit gaps; retrieve_investigation_guidance under recommend_investigation_steps when an identified unanswered question needs practice support | Chat/research identifies the question; code validates the assignment and enforces approved-source eligibility. Guidance is not executed action. The next T45 decision selects sources; this mapping does not approve them. |

Full/narrow mode is parent state. Most evidence collection can use assess_login_explanations
with its compatible tasks; guidance can use a separate recommend_investigation_steps request.
Keep all requests tied to the same parent obligations without changing their one-intent rule.
Do not automatically call all four documentary searches for every narrow request or treat
every allowed task as mandatory regardless of applicability.

Implementation supplies concrete fact-to-query templates and relevance/applicability rules
under this mapping. The code-built baseline must remain unchanged by arbitrary chat prose;
semantic usefulness is proved by existing retrieval/application evaluations, not template
determinism alone. No-match, failed and unavailable outcomes retain the established meanings.
Existing IC-11 checks cover full versus narrow classification/enforcement, source/window
scope, lost competing evidence and false completion. Exact proof ownership is assigned in
the forthcoming ticket handoff; no new evaluation thresholds or additional proof suite.

## Investigation-guidance source selection — approved, 8 November 2026

8 November 2026. Second closing decision, considered individually. Read all three existing
runbooks below in full. The author approved the bounded initial set of investigative passages
below together with the extensible catalogue approach described after the table. This is
not adoption of their full response procedures or a new external standard. These are the
synthetic organisation's existing corpus documents, not externally certified practice.
IC-07 requires case-specific uncertainty, source grounding and separation of app/external
actions; IC-01 excludes broad response planning. Corpus presence alone is not this approval.

| Approved source and provenance | Selected passages | Question/uncertainty served |
| --- | --- | --- |
| run-new-country-sign-in, version 1.0, Security/IT, dated 2026-08-03 | Purpose; Triage steps 1–4 | Whether the observed country/device is consistent with approved travel, issued/replacement equipment and independently obtained user confirmation. Country estimation is not proof of physical location. |
| run-password-spray-response, version 1.1, Security/IT, dated 2026-07-14 | When to use this procedure; Response steps 1, 3, 4 and 6 | Whether records support a cross-account pattern; whether successes occurred; what MFA/exception evidence exists; relevant recorded privileges and bounded potential impact. |
| run-compromised-account-response, version 1.3, Security/IT, dated 2026-07-14 | Purpose and responsibility's first paragraph; Response steps 4–7 | Unexplained activity/device changes, relevant access, directly connected account activity and the applicability of an MFA exception. The title is not evidence of compromise. |

Source files: `backend/data/datasets/default/corpus/own/` with the corresponding IDs as
filenames. Human review anchors in the inspected files: new-country lines 17–29;
password-spray lines 17–19, 23, 27–29 and 33; compromised-account lines 17 and 29–35.
Line numbers are navigation only. Implementation binds selection to the actual captured
source/version and passage identity; later document changes are not silently approved.

Mixed-content boundaries: the selected passages remain source text, never workflow authority.
For the compromised-account step 7, the investigative exception check is eligible; advice to
change an exception is outside this selected purpose. Similarly, selected purpose paragraphs
do not authorise applying access changes. Entire unselected containment, reset, revocation,
restoration, closure/handover and communication procedures remain outside this guidance set.
Do not crop away a prerequisite or qualifier merely to make an in-scope instruction fit.
If the prepared passage cannot represent the approved selection with its necessary context,
report that source-selection limitation rather than expose the whole procedure indiscriminately.

Application constraints are unchanged: use access evidence for bounded account significance,
not exhaustive inventory; use involved-device/same-source activity within authorised scope,
not restored address-sharing exposure. VPN attribution requiring absent session-allocation
records is an external evidence gap, not a new app capability. History expansion still needs
analyst approval. Missing failure reasons, detailed MFA events or historical permissions cannot
be fabricated from guidance. Resolve actual memberships from evidence, not generic examples.

Recommendations must name the case uncertainty and whether the check is available in the app
or requires an external analyst. A suggested known-channel contact is not an actual contact;
device suitability, MFA success and approved exceptions require their own evidence. General
runbook text never establishes that an event occurred or that a step was carried out.

Example: if approved travel covers the date but the device remains unexplained, propose
checking the replacement/handover record and, if still unresolved, verifying the sign-in with
the user through an established contact channel. State which evidence is missing and that
the external contact has not occurred. Do not turn the travel notice into proof of device use.

No NIST-wide adoption, new web retrieval, source rewrite or ingestion is proposed. Existing
ATT&CK documents retain their threat-knowledge role; this proposal does not automatically
approve every detection/response passage as investigation practice. Existing policy and case
documents remain evidence in their established search purposes. T26 and the research-worker
handoff enforce this selection; T29/T40 retain recommendation-relevance and scope proof.
Source eligibility representation is an implementation detail under this explicit selection.

### Extensible source catalogue — approved with the initial selection

Treat these three documents as initial catalogue entries, not hard-coded branches or a
permanent three-source limit. The catalogue records document/version identity, approved
sections and purpose, applicability and approval status. Source text cannot grant itself
eligibility. Selection remains bound to the reviewed source version and captured evidence.

Adding a runbook within an existing supported purpose is content work: review its guidance,
register approved sections and update the existing index through the established build process.
The same retrieval and exact-reading interfaces consume the catalogue. No new agent, tool or
workflow branch is required merely because another runbook is added. New purposes/capabilities
or changed required procedures remain separate scope/design decisions. Revised source text
needs review; previous approval does not silently transfer to changed sections.

An eligible guidance source supplies possible next checks. It does not modify the core
mandatory procedure or make every source step required. That separation permits source growth
without allowing corpus edits to change workflow obligations. The exact catalogue storage and
registration command belong to implementation. Its operator task belongs in the admin manual
when built. No new database, runtime file-write tool or ingestion is authorised by this ruling.

## Retrieval acceptance paths — approved, 8 November 2026

8 November 2026. Third closing decision. After the plain-language explanation, the author
approved the recommendation below. This explicitly supersedes the T06/spec/T29/AUD-062
corpus-fused-top-20 acceptance condition with path-specific candidate/delivery checks against
the approved pipeline. The earlier candidate-count approval alone did not revise that gate.
Original questions/gold and historical failures remain; no current pass or closure is claimed.

Use two separately reported views of the same acceptance case, retaining original
questions, gold passages/records/paths, source identities and existing answer/security gates:

| View | Input and execution | What it establishes |
| --- | --- | --- |
| Analyst-question path | Submit the original question unchanged. Chat/research perform their normal assignment/query work within approved scope. No human rewriting or gold-informed retrieval hints. | The application can turn the actual analyst question into evidence requests, retrieve expected evidence, deliver it and ground its answer. |
| Code-built investigation path | Resolve the same case using target identity already available independently of gold. Run the shared procedure's fact-derived baseline searches and normal assembly. Keep baseline evidence separate from any subsequent model-driven supplements. | Required collection does not depend on arbitrary chat text; the package collects and preserves the expected evidence. Package-only success does not establish final answer quality or rescue a failing analyst-question path. |

For K04, retain the exact question in knowledge_base_questions.json and both existing gold
passages: the MFA Exception Register and the Password Spray Response passage. Existing
record/path gold and graph correctness checks stay unchanged. The current retrieval_requests.json
already supplies a case finding reference independently of passage gold; validate the appropriate
source snapshot rather than generate a target from the answer key.

Approved candidate-stage check: each expected passage must be present in the admitted,
deduplicated candidate pool of at least one actual relevant search in that path. Each search
retains up to 20 corpus plus 20 additional unique graph passages, five final search results,
and the eventual bounded execution policy. Record route/candidate admission, ranking, retained
results and actual model-visible delivery separately. A passage excluded before ranking,
saved only as an artifact, or found only in the other path does not satisfy delivery.
Do not merge unrelated attempts, retries after a finished run or different source versions
to manufacture a pass. Query/search volume and configuration accompany the result; larger
budgets are not silently comparable to earlier runs.

Require all expected passages at the relevant delivered-evidence boundary and, on the
application path, at chat's interpretation boundary. Existing citation/answer rules still apply.
Successful candidate admission alone does not close a case. Report baseline package misses
even if an optional research follow-up later recovers them; the views diagnose different work.
Other questions' regressions remain visible under existing evaluation owners and gates.

Retain the unchanged raw-question, corpus-only fused-top-20 measurement as
a diagnostic baseline, not a second release condition for the new pipeline. Its historical
K04 failure remains a failure of that measured path, never relabelled as passing. This revises
AUD-062's previous top-20 closure condition; it does not close AUD-062 now. Closure requires
the new path-specific candidate/delivery evidence and existing regression/answer obligations.

Unselected alternative, retained as history: retain the original corpus-only top-20 gate as an additional acceptance condition
while separately measuring both new paths. That keeps the old component target but can block
release even when the approved graph-assisted pipeline delivers all required evidence.

These are component and application views within existing T26/T29/T40/T41 responsibilities,
not an instruction to run duplicate full suites or two independent paid campaigns. Exact
execution/evidence reuse follows the implemented paths and must not claim one path proves
another. No run, gold edit, gate implementation or audit closure is authorised by this ruling.

## Keyword-search disposition — approved, 8 November 2026

Fourth closing decision. The author approved retaining PostgreSQL's current keyword search
for the initial implementation, using the already-approved focused searches. T41 retains
ownership of the measured BM25 comparison and its existing adoption/refusal rules.

The installed langchain_postgres v2 implementation uses plainto_tsquery for matching and
ts_rank_cd for ordering. PostgreSQL documents that plainto_tsquery joins surviving terms
with AND: https://www.postgresql.org/docs/current/textsearch-controls.html.
Matching and ranking are separate concerns. Replacing scoring alone cannot recover passages
excluded by the matching rule. Focused queries may improve coverage but have not proved it.

Keep candidate/delivery diagnostics and the approved path-specific acceptance checks. If the
baseline fails those checks, address the failure before accepting the implementation; the
later phase-1 T41 comparison does not waive or postpone phase-0 requirements.
No blanket AND-to-OR change, BM25 adoption, new search engine, runtime success or audit
closure is approved here. Implementation ownership reconciliation must retain this obligation.

## Prompt-example selection — approved, 8 November 2026

Fifth and final closing design decision before implementation-ticket ownership. The author
approved a small, targeted set of role-specific teaching cases. These are selected behaviours,
not final prompt wording or a requirement for exactly six serialized examples.

| Role | Selected teaching cases |
| --- | --- |
| Chat | Convert a compound question into focused requests; clarify a materially ambiguous target; handle a narrow follow-up without erasing outstanding full-investigation obligations. |
| Research | Choose tools and inspect evidence within the assignment; report missing or failed retrieval honestly; return supporting and competing evidence with source references and unresolved gaps. |

Write concrete examples against the final contracts during implementation. Include successful
and unsuccessful retrieval outcomes. Missing information must not be invented; an ambiguity
that materially affects scope/identity requires clarification. Multiple intents become focused
requests under the approved parent mode, not an enlarged worker assignment. Research examples
teach tool-work boundaries, result examination and contracted responses, not verdict authority.
Documentation examples are not copied into prompts automatically. Keep evaluation answers out
of prompt examples. Assess value through the existing agent evaluations and inherited gates;
no new paid campaign or runtime success is authorised or claimed. Exact wording/counts are
implementation details. Chat examples belong to orchestration; research examples to the worker.

## Request contract baseline

This section consolidates the author's individual rulings and completes routine field/value
details under the author's 8 November delegation. It is the current request-side design;
comments below retain decision history. Newly completed details are delegated design work,
not claims of separate author approval or runtime support. T45 remains claimed. No application
code, paid experiment, acceptance threshold or corpus change is authorised here.

Inherited requirements: IC-01/02 scope and authority; IC-03/04 activity and account context;
IC-05/06 supporting/competing evidence and preservation; IC-07/08 explicit incomplete states
and required checks; IC-09 evidence identity; IC-10 trust boundaries; IC-11 separate proof.

### Responsibility and request construction

- Chat agent classifies intent, clarifies user context, selects subjects and evidence tasks,
  and interprets the returned evidence. Research agent selects permitted tools, examines
  retrieval quality, makes bounded follow-ups and returns evidence. Code owns facts, dates,
  validation and required-check enforcement. Analyst retains the verdict.
  In approved full-investigation mode, the core procedure supplies mandatory obligations
  independently of chat's task selections; chat-selected refinements cannot replace them.
- One intent per request. Batch requests known together; return a distinct result/status for
  each request. Research agent can reuse evidence within the batch without merging request
  obligations. Interpretation-dependent subsequent requests wait for chat-agent reasoning.
- Fields below describe the **dispatched contract**. Chat-agent construction is a precursor:
  it chooses semantic task/subject associations; code allocates request/subject/task labels
  and translates those associations into references. Never ask the model to predict a future
  code-generated identifier. The exact model-facing builder interface remains implementation
  design, not a second model-owned investigation plan.
- Use strict object shapes. Reject unknown fields, unknown enum values, dangling references
  and contradictory mode fields rather than silently dropping them. Blank means empty after
  trimming whitespace. Do not rewrite the contents of identifiers as a guess at identity.
- A type/mode variant contains only its own fields. Inapplicable alternative-variant fields
  are absent. Required identity fields never accept null. An unresolved required identity
  blocks that request; it does not block unrelated valid requests in a batch.
- A field that is meaningful for the selected task but unknown or inapplicable uses an
  explicit state plus a nonblank reason, as specified below. A reason is not permission to
  waive required checks. Unknown evidence **existence** does not block a valid search.

### Outer request and subjects

| Field | Required value and ownership | Missing/invalid handling |
| --- | --- | --- |
| request_id | Nonblank code-generated unique request ID. Stable during retries; new assignment gets a new ID. | Never null/unknown/not applicable. Block dispatch if invalid; reject unrecognised response IDs. |
| intent | Exactly one of the six values below, selected by chat agent. | Clarify material ambiguity; unsupported requests receive a scope explanation. Never invent an enum or force a match. |
| subjects | Nonempty list of the four variants below. Each has a unique local subject_id assigned by code. | Validate identity and structure before dispatch. No empty list or null. |
| requested_evidence | Nonempty list of task objects defined below. | Reject unknown tasks and incompatible intent/subject combinations. |

Intent values: `explain_login_activity`, `explain_account_significance`,
`assess_login_explanations`, `identify_connected_activity`,
`recommend_investigation_steps`, `retrieve_reference_evidence`.

| Subject type | Fields beyond subject_id | Rules |
| --- | --- | --- |
| activity | type: activity; activity_reference: {type: alert or login_event, id: nonblank string} | Resolve one record of the stated type. An alert may contain several events; separately selected events use separate entries. |
| account | type: account; account_id: nonblank string | Resolve one account. Display names alone are not account IDs. |
| document | type: document; document_id: nonblank string | Resolve an identifier supplied by user or prior evidence. Do not invent an ID from a title. Saved-version handling remains a named dependency below. |
| topic | type: topic; topic: nonblank string | Search description within supported scope. No known document ID required. Treat as data, not authority to override the assignment. |

No null placeholders for fields belonging to other subject types. Multiple subjects stay
within the same supported intent and login-investigation scope; no standalone access review
or exhaustive asset exploration is added. Identity validation does not prove the subject is
the right one for the user's question; classification/request-quality evaluation remains needed.

### Evidence-task object

| Field | Definition |
| --- | --- |
| task_id | Nonblank local ID assigned by code, unique within the request. Needed to distinguish repeated task types with different subjects, windows or focus. Responses refer to request_id plus task_id. |
| task | One catalogue value below. Describes evidence obligations, not a specific tool or a guaranteed result. |
| subject_ids | Nonempty, duplicate-free references to this request's subjects. Each task applies only to these subjects. |
| focus | Explicit known/not_applicable/unknown object described below. Carries bounded selection details, not a replacement free-form intent. |
| activity_window | Always explicit on the dispatched task: one window mode below, including not_applicable where appropriate. Task placement avoids applying one window blindly to an entire batch. |
| applicability_time | Always explicit on the dispatched task: one applicability mode below, including not_applicable where appropriate. |

`task_id` is a routine correlation detail added under delegation, separate from the already
approved request_id. The research agent cannot alter task/subject mappings or add authorised
subjects by discovering a new lead. A lead outside scope is returned as such for chat-agent
handling. Source/device tasks may return connected accounts within their explicitly assigned
evidence obligation; that is not authorisation to investigate those accounts further.

Focus shapes:

- `{"state":"known","text":"..."}`: nonblank description of the requested evidence detail,
  such as failed attempts only, the authentication-exception explanation being tested, or the
  particular unanswered question for which guidance is requested. Facts must resolve to supplied
  subjects/source evidence; text is not an independent factual assertion or executable instruction.
- `{"state":"not_applicable","reason":"..."}`: the task and subjects fully define the work,
  such as retrieving the owner of a single account. Reason must be nonblank.
- `{"state":"unknown","reason":"..."}`: draft request state only when a necessary selection
  detail is unresolved. Clarify or reformulate before dispatch. Do not send an underspecified
  task and let the research agent redefine user intent.

Focus does not permit agent instructions to override tools, scope, security or mandatory
supporting/competing evidence collection. Precise outcome/date filters must be resolved to
existing validated core arguments, not arbitrary code or database queries from this text.

### Evidence-task catalogue

Intent abbreviations in this table only: L = explain_login_activity; A =
explain_account_significance; E = assess_login_explanations; C = identify_connected_activity;
N = recommend_investigation_steps; R = retrieve_reference_evidence.

| task | Allowed intents | Allowed subject types | Evidence obligation |
| --- | --- | --- | --- |
| retrieve_triggering_activity | L, E, N | activity | Referenced event or alert's underlying records; outcomes, times, accounts, sources/devices, code counts/sequence. No automatic surrounding-history expansion. |
| retrieve_surrounding_activity | L, E, C, N | activity, account | Relevant login records in the authorised window, with failures/successes, source/device changes and code counts/sequence. Account-only explicit periods are supported here; the task name does not require an alert. |
| inspect_activity_coverage | L, E, C, N | activity, account | Available record coverage versus requested scope and known collection gaps. For direct coverage questions; other activity tasks already report coverage without requiring this extra task. |
| retrieve_account_context | A, E, N | account, activity | Recorded owner, department, role and group context relevant to the question. Activity-derived accounts retain links to their source events. Missing role information stays explicit. |
| retrieve_relevant_access | A, E, N | account, activity | Relevant privileges, sensitive assets and supporting permission paths. Snapshot limits; no exhaustive inventory or inference of exercised access. |
| retrieve_same_source_activity | C, E, N | activity | Other-account login activity from sources involved in the referenced activity, within the authorised window, with recorded links/outcomes. No restored shared-address exposure feature. |
| retrieve_shared_device_activity | C, E, N | activity | Other-account use of devices involved in the referenced activity, within the authorised window, with dated links. Not all devices ever used by an account. |
| retrieve_explanation_evidence | E, N | activity, account, topic, document | Supporting and competing case documents, applicable policies, actual exceptions/records, conditions and relevant history. Focus states the explanation or bounded evidence question. |
| retrieve_threat_guidance | E, N | activity, topic, document | Applicable approved threat references and their scope/limitations. General guidance is not evidence that a case event occurred. |
| retrieve_investigation_guidance | N | activity, account, topic, document | Approved practice addressing the specific unanswered question stated in focus. No execution of the recommended next step. |
| retrieve_reference_material | R | document, topic, account, activity | Known document or matching passages about the specified subject, plus needed conditions/context and source identity. Account/activity subjects require focus describing the material sought. |

Compatibility permits supporting tasks under an intent without reclassifying those supporting
tasks as additional user intents. It does not require every permitted task on every request.
For activity-derived account/access tasks, focus must make clear whether the request concerns
all accounts in the referenced activity or a known subset; never silently choose one.

`retrieve_relevant_access`, explanation and investigation-guidance tasks require known focus.
Threat/reference tasks may use not_applicable only where topic/document identity fully specifies
what is sought. Other tasks permit not_applicable when their subjects and timing are sufficient.
Selecting a single explanation never permits confirmation-only retrieval. Evaluations must test
whether the focus is faithful and complete; structural validation cannot establish that.

Every retrieval carries source/provenance and limits regardless of task selection. There is no
optional task that can disable citation evidence, contradictory material, coverage reporting or
failed-check reporting. Current field absence is not licence to add telemetry or fabricate data.

### Window and applicability variants

All reference lists are nonempty, duplicate-free local subject references. No mode accepts
extraneous fields from another mode. Explicit timestamps use ISO 8601 with a UTC offset;
code normalises to UTC and checks start < end. Calendar dates use YYYY-MM-DD; named time zones
must be valid. Null, blank, unresolved relative strings and invented time zones are rejected.

| activity_window mode | Fields | Meaning |
| --- | --- | --- |
| default_from_activity | subject_ids referencing activity subjects | Code derives each alert's start minus 24 hours through end plus 24 hours, or each event timestamp ±24 hours. Preserve separately derived windows and their anchors. |
| explicit_range | subject_ids; start; end | User-requested or analyst-approved range, start included/end excluded. References must cover the target subjects of the task. |
| not_applicable | reason | No collection window is needed: e.g. exact triggering records, account snapshot or document retrieval. |
| unknown | reason | Draft only. Resolve required collection scope before dispatch; never silently broaden. |

Surrounding, same-source, shared-device and coverage tasks require a concrete window.
Default anchor subjects must also be among the task subjects; for an account-only historical
query use explicit_range. If different task targets need different ranges, make separate task
entries. Do not silently take the earliest start and latest end as one broad interval. Overlapping
retrievals may be deduplicated while retaining original task/window attribution.

Coverage clips execution to available records but preserves the originally requested interval
and discloses gaps. The default's exact endpoint behaviour must be reconciled with the current
core before implementation; explicit_range's half-open semantics do not silently change IC-03.
Code enforces approval from trusted conversation/workflow state, never from a model-written
claim of approval. A direct user request supplies approval; agent-proposed expansion requires it.

| applicability_time mode | Fields | Meaning |
| --- | --- | --- |
| from_activity | subject_ids referencing activity subjects | Code obtains relevant event times, preserving event-to-time attribution, not substituting an alert's first timestamp for all events. |
| explicit_date | date; timezone | Calendar day as requested; preserve any change within that day. Do not substitute midnight for the whole day. |
| not_applicable | reason | Temporal applicability is not being assessed, e.g. inspect a known document without a historical question. |
| unknown | reason | A relevant historical time is unavailable. May dispatch a bounded evidence search with this explicit limitation, but cannot claim temporal applicability established. Clarify first if the missing date prevents meaningful selection. |

These final two explicit states complete the author's missing-field requirement under delegated
design authority; they were not individually approved earlier. Applicability subject references
may be context anchors outside the task target list, but must exist in the same request. This
allows an account-document task to use a referenced login's date without applying it to every
other subject. No silent inheritance of a date across unrelated subjects.

Known event timing cannot be marked unknown/not_applicable to skip an explanation's temporal
check. Historical access questions retain applicability_time but report if only a current
snapshot exists. Record validity conditions and publication dates separately: a date filter
matching a document's publication date is not proof of validity. Older documents may remain
essential. Explicit-date source precision remains unchanged; never infer missing hours.

Relative expressions are resolved before dispatch using established reference date/time zone.
Yesterday is a calendar day; last 24 hours is a rolling interval. Missing material context is
clarified once and reused. No silent selection of host clock versus dataset reference time.
The exact translation of explicit instants or longer applicability periods is deferred; reject
unsupported shapes clearly rather than silently rounding to one day. Existing from_activity
supports event instants, but not an invented event created solely to bypass this limitation.

### Validation and incomplete input

1. Validate field presence, enums, types and variant shapes; reject unexplained nulls.
2. Resolve subject identities against the applicable source context; do not conflate a source
   outage with a nonexistent identifier. Report the distinction without guessing or substitution.
3. Check task/intent/subject compatibility and all local references; labels are code-owned.
4. Resolve timing, scope approval and relevant task focus. Reject contradictory timing modes.
5. Dispatch valid requests with code-resolved context. A rejected request remains visibly
   rejected within its batch; do not report the batch as completely fulfilled.

Errors need the request/task/field location, reason and what would resolve the problem.
Malformed model output is a construction error, not automatically a question for the user.
Only missing user context requires clarification. No unbounded self-repair loop is implied.
Code-required procedure checks cannot be removed via focus text, omission or a reason field.
The full procedure's task coverage remains a T26/T28 integration dependency.

### Documentation example

These are illustrative references, not executable fixture IDs or selected prompt examples.
Code assigns labels after the chat agent selects the semantic associations.

```json
{
  "request_id": "request_1",
  "intent": "explain_login_activity",
  "subjects": [
    {
      "subject_id": "s1",
      "type": "activity",
      "activity_reference": {"type": "alert", "id": "example-alert-id"}
    }
  ],
  "requested_evidence": [
    {
      "task_id": "t1",
      "task": "retrieve_triggering_activity",
      "subject_ids": ["s1"],
      "focus": {"state": "not_applicable", "reason": "Retrieve the referenced alert's triggering records."},
      "activity_window": {"mode": "not_applicable", "reason": "Exact triggering records are identified by the alert."},
      "applicability_time": {"mode": "not_applicable", "reason": "This task establishes observed activity, not document validity."}
    },
    {
      "task_id": "t2",
      "task": "retrieve_surrounding_activity",
      "subject_ids": ["s1"],
      "focus": {"state": "not_applicable", "reason": "Collect relevant surrounding successes, failures and source/device changes."},
      "activity_window": {"mode": "default_from_activity", "subject_ids": ["s1"]},
      "applicability_time": {"mode": "not_applicable", "reason": "This task collects activity rather than assessing policy validity."}
    }
  ]
}
```

### Current-code grounding and remaining architecture work

Read-only source checks on 8 November, not runtime tests or new library integration:

- `backend/login_investigator/rules.py`: Finding.finding_id provides stable finding IDs;
  constituent rows use row_ids. The new dispatched login_event identifier/resolver is not
  demonstrated by this inspection. Bind it to the correct dataset, not an unqualified row number.
- `backend/login_investigator/knowledge_tools.py`: lookup_account accepts an exact username
  or stable user ID and returns owner/department/groups. Canonical account-reference construction
  must use that existing seam. It does not prove the new access-task implementation exists.
- `backend/data/datasets/default/corpus/own/reg-mfa-exceptions.md`: existing document ID,
  version and dated approval context. Document ID alone cannot select original saved evidence.
- `backend/login_investigator/knowledge_base/retrieval.py`: existing SearchFilters contains
  document_type, technique_id, incident_id, version and effective_date. No equivalence between
  that metadata filter and the proposed temporal-applicability semantics is assumed.
- `backend/login_investigator/generator.py`, `agent.py`, `dashboard.py`: current reference
  instant comes from CAPTURED_AT, 2026-10-08T09:00:00Z. Dataset truth files also record captured_at,
  but ground-truth answers must not become agent inputs. A dataset-owned reference-time seam
  for future datasets remains implementation work; do not assume the current constant is universal.
- Default log columns have no target application. Groups/grants/assets supply privilege and
  sensitivity context, not observed application access or detailed rights. No application filter
  is added to this contract merely because an earlier example mentioned email versus payroll.

Remaining substantive work, not waived by delegation of routine field values:

1. Response/evidence contract is consolidated below. Its source-binding adapters, required-work
   definitions and execution integration remain design/build dependencies, not verified features.
2. Cross-batch memory/reuse and saved-document version selection. available_evidence_refs is
   still not adopted. No implicit persistent research-agent memory or silent latest-version swap.
3. Runtime tool exposure, existing package integration, scope/budget enforcement and exact
   retry/stop limits. No new numerical limits invented here. A tool catalogue is not the same
   as this evidence-task catalogue.
4. T45's retrieval mechanisms, gate-path rulings, keyword strategy, approved guidance sources,
   and T26/T28/T29 handoffs. Existing K04 gold and all acceptance thresholds remain unchanged.
5. Separate prompt-example discussion and the agreed roast-technical review once request,
   response and execution boundaries are concrete. Do not run the council prematurely against
   an unfinished response contract. Do not implement before the design/spec handoffs are settled.

## Response contract: consolidated design, 8 November 2026

This is the current response-design home. It consolidates the discussion, research and delegated
field definitions below. Earlier drafts and walkthroughs remain as history; where their status
names or next-step wording differ, this section governs the current design. It is a logical
contract, not an implemented JSON schema or proof of runtime behaviour. IC-02 and IC-05–11 remain
inherited requirements. Field naming/validation details are delegated design, not claims that
the author individually approved each field. The author explicitly confirmed the request/response
alignment and the evidence-limit ruling.

### Alignment with the dispatched request

Code retains the dispatched request as the authoritative assignment. Never reconstruct it from
the research model's response. A batch returns distinct request results, even where evidence
is reused. Every valid dispatched request must be accounted for; construction rejection before
dispatch remains a visible batch outcome, not a fabricated retrieval result.

| Request element | Response obligation |
| --- | --- |
| request_id | Exact match to one dispatched request. Unknown or mismatched IDs are contract errors. |
| requested_evidence task_id | Exactly one final task_result for every assigned task. No extra, duplicate or silently missing tasks. Attempts are separate operation records. |
| task and intent | Original values govern the result. Resolve through request/task IDs rather than repeat model-authored copies. Research cannot substitute a different assignment. |
| subject_ids on each task | Account for every assigned subject. Evidence and gaps retain subject attribution; a successful result for one cannot hide incomplete work for another. |
| focus | Evidence and observations address the specified question. Code enforces structural scope; evaluation checks semantic fulfilment. |
| activity_window | Preserve the requested window and the actual checked intervals/coverage gaps, retaining separately anchored windows rather than broadening them into one range. |
| applicability_time | Preserve the requested event/date context. Return source dates, relevant conditions and uncertainty without changing the requested time or inventing precision. |

Task-to-result is one-to-one. Task-to-evidence is many-to-many: one task may return many or no
items, and one item may serve several tasks. Every task still has a result. Evidence sharing
does not merge subjects, task obligations or request completion.

### Outer shape and task results

The final assembled response contains request_id, task_results and evidence. All three are
required. task_results covers the nonempty assigned task list; evidence may be empty with
explicit operation outcomes and limitations. Code assembles this envelope around the research
model's selections/observations and observed tool results; the model does not reproduce facts,
source payloads, execution receipts or authoritative completion labels.

| Task-result field | Required meaning |
| --- | --- |
| task_id | Exact assigned task reference, unique within the response. |
| completion | Code-derived complete, partial or not_completed as defined below. |
| subject_results | One entry per assigned subject_id, with completion, delivered evidence_ids and gap_ids for that subject. A genuinely joint operation may be referenced by several entries. No invented individual success when only a collective result is available. |
| operations | Code-owned receipts for executed or explicitly unperformed required work, and material follow-ups. Each has operation_id, subject_ids, outcome, checked scope, output evidence references where applicable, and reasons for non-success. Detailed attempts remain in the trace. |
| evidence_ids | Unique references to actual delivered items in this response. May be empty. This is not a list of everything ever retrieved. |
| gaps | Execution limitations and research-identified missing evidence, using distinct origin variants below. Empty only when neither kind is known. |
| observations | Research-model relevance/applicability notes tied to subjects and delivered evidence. May be empty. They are not original source facts or the overall investigative assessment. |

Checked scope includes requested versus checked activity intervals when relevant, source/snapshot
coverage and known gaps. A non-temporal operation marks a collection window not applicable with
a reason rather than manufacturing dates. Check-only operations return their code-produced check
result; a successful coverage check can itself reveal unavailable history.

Subject_results is a coverage accounting mechanism, not a requirement for a separate tool call
per subject. Its exact task-specific required-work rules must be defined in trusted code. A
missing sub-result is a contract error, not evidence that nothing was found for that subject.

### Outcomes and gaps

Component outcomes distinguish found, no_match, completed, partial, failed, unavailable and
omitted. completed is for a check-only operation, with its result; found/no_match describe a
completed retrieval. partial retains usable output and completed scope alongside outstanding
scope. failed means attempted but not completed; unavailable means the source/capability could
not be used before execution; omitted means not run, with its reason. All non-success reasons
remain visible. no_match is never inferred from an empty packet and never proves nonexistence
outside the checked scope. Exact retry/attempt encoding remains execution design.

| Completion | Definition for a subject, then its task |
| --- | --- |
| complete | All required obligations are satisfied, including delivery and validation of required selected evidence. A completed bounded no-match lookup can satisfy a retrieval obligation. This is procedural completion, not exhaustive discovery or a resolved investigation. |
| partial | Some required obligations are satisfied but others remain incomplete. Preserve useful evidence and explicit gaps. |
| not_completed | No required obligation is satisfied. Component outcomes retain the cause rather than collapsing unavailable, omitted and failed into one reason. |

The task is complete only when every assigned subject and any joint task obligations are complete.
If none of its required obligations is satisfied it is not_completed; otherwise it is partial.
Count satisfied obligations, not merely successful tool calls. An optional failed follow-up stays
visible but does not automatically invalidate fulfilled required work. The model cannot relabel
required work optional. Retry success can resolve an obligation without erasing failed attempts.

Each gap has a code-assigned gap_id, subject_ids and a nonblank explanation. origin determines
its authority and remaining fields:

- execution: code supplies a reason code and the relevant operation/assembly-validation record
  reference. Covers failed/unavailable/omitted checks, excluded evidence and invalid references.
  An omitted/rejected item is referenced through that record, never falsely listed as delivered.
- evidence: research identifies missing information or an unresolved condition, with supporting
  evidence_ids where available. If no supporting item exists, an explicit reason accompanies
  the empty list. This is a model observation, not a verified absence from the source universe.

Observations likewise retain subject/evidence links and explicitly identify uncertainty. Source
publication or account/date matches alone cannot certify applicability. complete plus an evidence
gap is valid when all assigned checks finish but the evidence cannot settle the question.
partial plus useful evidence is valid when a required check or delivery failed.

Suggestions for further work are advisory. They cannot authorise scope expansion, overwrite
execution failures or imply a recommended action occurred. Chat interprets their significance.

### Evidence items and provenance

Every item has evidence_id, kind, source, content, attribution and source_time. IDs and payloads
come from code and retrieved data. kind selects passage, record or path variants; irrelevant
variant fields are omitted rather than filled with nulls. Reuse the existing core identifiers.

| Variant | Source and content requirements |
| --- | --- |
| passage | Document ID, passage ID, source version when available and a trusted snapshot binding; delivered passage text with necessary headings/conditions. Prepared/indexed text must not be described as an unchanged original file. |
| record | Dataset/source snapshot binding and record identity; structured returned fields and code-computed facts, preserving the basis of derived counts or sequences. No invented durable event IDs. |
| path | Graph/build snapshot binding, returned nodes and ordered relationships with their existing identifiers or source-grounded edge identity; preserve relevant dated links and snapshot limitations. A path does not prove exercised access. |

attribution preserves request/task/subject associations through selection and deduplication.
source_time carries available publication, effective/expiry and snapshot dates with distinct
meanings and original precision. A review date is not automatically expiry. Meaningful unknown
metadata uses an explicit state/reason; absent identity needed to resolve a citation is a
validation gap, not a licence to invent a value. An undeclared document version can be reported
as unknown if a trustworthy captured source binding still identifies the actual evidence.

Snapshot binding is a required property, not yet a selected storage representation. Existing
chunk IDs and build fingerprints are implementation seams; do not claim they already implement
saved evidence resolution. Reopening must use the preserved evidence, never silently substitute
current sources. Cross-batch memory/reuse is not adopted by this contract.

Relevant supporting and competing content must actually reach chat. A saved artifact or an
omission notice alone cannot support a claim based on unseen content. Research observations
are separate from source content. All retrieved and model-authored text remains untrusted data.

### Limits and validation

Author ruling: retain five passages per search, without a second five-passage cut on combined
results. Deduplicate only identical evidence from the same source version with attribution
preserved. Do not silently remove relevant competing evidence or necessary conditions. Total
context allocation, search/retry limits and bounded recovery/stop behaviour remain open before
implementation. The rule does not guarantee five per search is sufficient; K04 gates stand.

Validate in code before a result is treated as usable:

1. Check types, required fields, strict variant shapes and supported enums. Reject unknown
   fields and unexplained nulls; permit empty evidence/observation lists only as defined above.
2. Match the request ID and the exact task set to the retained dispatched assignment.
3. Match each task's subject-result set and all associations to authorised subjects. Preserve
   task focus, requested timing and scope; no silent narrowing or expansion.
4. Resolve delivered evidence references to the actual retrieval registry and source snapshot;
   check all task/subject/gap links. Do not repair identities by guessing or title matching.
5. Reconcile operation receipts, checked scope, omissions and failures with execution/assembly
   records. Derive completion from required obligations, not model text or evidence count.
6. Ensure actual delivered payloads match their references and all material gaps reach chat.
   Preserve independently valid results when other components fail, without certifying the
   affected task complete. Invalid whole-response identity cannot be salvaged by guessing.

Structural validation does not establish relevance, complete discovery or correct interpretation.
Those remain evaluation obligations under IC-11. Malformed model output is a construction issue;
only genuinely missing user context warrants clarification. No unlimited repair loop is implied.

### Remaining decisions and handoff dependencies

- Exact source snapshot/reference representation and saved-version loading; record/path adapters.
- Code-owned required-work definitions per task/subject and integration with full-procedure checks.
- Request/batch lifecycle, cancellation, timeout/retry rules, context/search budgets and recovery.
- Cross-batch reuse, runtime tool exposure and original T45 retrieval/gate/guidance rulings.
- Prompt examples, then the separately agreed LangGraph orchestration research after contracts
  and execution boundaries are concrete, followed by roast-technical and build-ticket handoffs.

No application code, new evaluation gates, paid experiments or implementation release follows
from this consolidation. Next discussion: execution boundaries, starting with permitted tools
and who can initiate a follow-up, while keeping these dependencies visible.

## Execution boundaries: working design, 8 November 2026

**Design-order correction, author ruling, 8 November 2026:** design the planned research
agent's tools from its approved responsibilities, evidence tasks and request/response contracts.
Set capability boundaries, input/output obligations, permissions, separation of model decisions
from code duties, and follow-up/stop rules first. Do not use current tool names or gaps in their
mapping to choose the next design question. Only after the planned tool design is complete,
inventory the old implementation and decide what to reuse, repurpose, combine, replace or retire.
Existing approved behavioural/security requirements remain inputs; legacy interfaces do not.

The earlier capability map is retained as implementation history, not the design baseline.
The proposed next step of placing existing discovery/reputation tools is superseded. No feature
is removed by deferring that reconciliation, and no legacy-preservation requirement is created.
Resume with boundaries between planned evidence capabilities and their code-enforced contracts.

Begin with inherited authority, then decide actual tool exposure. The approved role split gives
chat user-intent clarification, assignment construction and overall interpretation; research
selects permitted tools and makes bounded evidence-gathering follow-ups. Code enforces required
checks and authorised scope; the analyst retains the verdict. No numeric limit chosen here.

### Follow-up authority within and beyond an assignment

- Research may refine a search, inspect relevant retrieved material and try another permitted
  source for the same assigned evidence need, within the eventual budgets. Its next tool call
  must retain the assigned subjects, timing and scope. Query wording may change; the assignment
  does not. Any passage expansion capability still requires a permitted tool/core interface.
- Research may return connected accounts/devices when the assigned connection task requires
  them. Discovering one does not authorise a new investigation into it. Return the lead for chat
  to assess. Research cannot add a new intent, task or subject to the dispatched request.
- Chat may construct another request within established user intent and authority after
  interpreting results. Ask the user only for genuinely missing context or an expansion requiring
  their ruling. A direct user request for more history already supplies the relevant approval;
  an agent-proposed history expansion still needs it.
- A tool failure remains an execution fact. Research can propose or attempt an allowed bounded
  recovery, but cannot erase the failure, invent evidence or mark required work optional.
  Required checks are enforced in code independently of either agent's proposed tool sequence.

### Planned capability families — design proposal, 8 November 2026

Derived from approved evidence tasks, not legacy tool interfaces. Use four families to organise
the design before deciding exact model-visible tool names/count. A family is a coherent module
interface; it can contain distinct operations where inputs, outputs or failure semantics differ.
This does not assert that four tools are sufficient or adopt a generic dispatch-everything tool.

| Family | Question it answers and task coverage | Distinct rules |
| --- | --- | --- |
| Activity evidence | What was recorded, when, and over what coverage? Triggering activity, surrounding activity and activity coverage. | Exact identity, authorised windows, code-owned counts/order, requested versus checked coverage and disclosed sampling. |
| Account and access context | Who owns the account and what relevant access is recorded? Account context and relevant access. | Snapshot evidence, bounded relevant permission paths, no inference of observed use or complete historical entitlement. |
| Connected activity | Which other activity has a recorded source/device link to the assigned activity? Same-source and shared-device tasks. | Link basis, involved source/device selection and dated scope must accompany results. Connection is a lead, not proof of common control; no investigation of newly discovered subjects without another assignment. |
| Documentary evidence | What source material answers the assigned evidence question? Explanation, threat guidance, investigation guidance and reference-material tasks. | Preserve original passages, source/version identity, conditions and competing evidence. Approved sources only where required; guidance is not an event fact. |

This partitions all eleven assigned task types without assigning each one a separate tool.
Connected activity may reuse activity and graph core operations internally; the research caller
should request a supported connection and receive its evidence basis rather than reconstruct
cross-source joins itself. Account/access context stays distinct because permissions are a
snapshot and not a record of behaviour.

The documentary family is a logical grouping, not a ruling that all documents use identical
retrieval or a single exposed search tool. T45's original internal-versus-exposed specialisation
decision remains open. At minimum distinguish discovering passages from reading an identified
passage/version with its required context; whether these become separate tools follows their
interface design. No unrestricted document browsing or numeric passage-limit bypass is implied.

Required supporting capabilities that are not separate evidence-task names must also be accounted
for before freezing the tool set. In particular, source-reputation context must retain its
approved factual/temporal limitations and required-check behaviour. Its placement will follow
the activity-evidence design, without preserving a legacy tool interface. Four families are a
starting organisation, not a declaration that all required workflow capabilities are mapped.

Common interface rules:

- Calls bind to the trusted dispatched request/task and authorised subject/scope. Code supplies
  resolved identity/timing context; model-supplied IDs cannot grant authority. Research chooses
  only supported operations/options and bounded query details, never SQL/Cypher or arbitrary code.
- Every operation returns evidence plus a code-owned receipt, coverage and failure information.
  Model observations stay separate. Shared core functions keep deterministic facts consistent.
- Tool choice cannot waive mandatory evidence/check coverage. The procedure/task definition in
  code determines required work; research can refine retrieval within it, not redefine it.
- Limits, invalid references and unavailable sources are explicit. No source or scope expansion
  is authorised by a failed search. The five-per-search/no-second-five-cap ruling still applies.

Next design slice: activity-evidence interface, beginning with exact records versus bounded
history versus coverage, and which decisions code owns. Then account/access, connections and
documentary interfaces. Reconcile legacy tools only when the planned design is complete.

### Architecture constraints and the planned activity interface

Author instruction, 8 November 2026: account for the actual RAG and graph design when defining
planned tools. This is architectural grounding, not a reversal of the decision to defer legacy
tool-interface reconciliation. Read the spec's retrieval/graph sections and radius semantics.

- Login records establish observed activity and code-computed counts/sequence. Graph relations
  and document passages cannot substitute for the actual event records.
- Neo4j owns named deterministic relationship queries. It supplies recorded permissions and
  device relationships; permissions are a snapshot, and log-derived links have explicit time
  semantics. Research does not write Cypher or choose arbitrary traversal depth. Same-source
  activity comes from log evidence, not the removed address-sharing graph feature.
- PostgreSQL holds passage text/search metadata; graph chunk nodes hold references connected
  by mentions links. A graph mention identifies a candidate connection, not proof the passage
  supports a claim. Resolve the actual passage from the paired source version before citing it.
- Keep graph and corpus identities bound to the same validated selected build. No silent mixing
  of current documents with an older graph, and no rebuilding/hot replacement during a question.
- RAG candidate search, ranking and retention are separate from exact activity collection.
  A passage score is neither event evidence nor a completeness certificate. Preserve the
  existing uncalibrated weak verdict/reason; response-level found means material returned,
  not that calibrated relevance or applicability was established.

Proposed activity module interface: three distinct operations, without yet fixing whether the
model sees three tools or one typed interface. Each binds to the trusted request/task context;
the model selects only supported refinements within that context.

| Operation | Input meaning | Output and guarantees |
| --- | --- | --- |
| Read exact activity | The resolved alert or login-event subject | The event or alert's constituent records, code-owned outcomes/counts/order and source-bound record references. No automatic surrounding-history expansion. Missing constituent records are explicit, not replaced by similar events. |
| Collect bounded activity | Assigned subjects, code-resolved windows and permitted focus filters | Matching activity facts, counts over the stated filtered population, delivered records or a disclosed sample, requested/checked periods and known coverage limitations. Keep full scoped population counts distinct from displayed sample counts. |
| Inspect coverage | The task's authorised subjects/windows and applicable collection metadata | Available record bounds, requested/checked intervals, documented collection gaps where known and explicit unknown continuous coverage. It can explain a coverage limitation without fetching all activity rows. |

Code owns source binding, identity resolution, window derivation/clipping, filter validation,
counts/order and coverage receipts. The research model may choose a permitted refinement or
inspect additional relevant records inside the assignment. It cannot silently turn a required
all-outcomes collection into failures-only, hide a success through selection, widen a period,
or use sample size as the count of matching events. Narrow user requests remain narrow.

Coverage is attached to every applicable activity result even if the explicit coverage operation
was not requested. Availability of events at the beginning and end of a period does not establish
continuous collection between them. An empty bounded result is not proof that no activity happened.
Overlapping task windows can share retrieved records while retaining separate coverage receipts.

Required source-reputation context is a supporting enrichment of activity evidence, not a
replacement for it. Preserve lookup source, lookup time/cache age and unavailable/private-address
states; current reputation cannot prove what was known or true at the login time. The exact
enrichment interface and required-check triggers remain to be defined from the approved procedure,
without retaining a legacy tool name or exposing unrestricted external lookups.

Open details before final interface: dataset-bound exact event identity, default-window endpoints,
selection/paging that preserves important events, trusted collection metadata and missing coverage,
and enrichment placement. These are explicit design dependencies, not capabilities demonstrated
by the three operation names. No new telemetry or broad graph traversal is adopted.

Next: account/access and connected-activity interfaces, carrying graph snapshot/date/relationship
semantics into their results; then documentary evidence with the RAG/graph reference join explicit.

### Planned account/access and connected-activity interfaces

Design continuation, 8 November 2026. The source inspection below checks graph meaning only;
existing tool signatures do not determine the planned interfaces. Inherited IC-04 requires
bounded account impact and treats connections as leads, not attribution or compromise verdicts.

#### Account and access context

Two operations serve different evidence questions within one family:

| Operation | Assignment and returned evidence | Required limits |
| --- | --- | --- |
| Read account context | Assigned account, or the explicitly selected accounts derived from assigned activity; recorded owner, department, role and relevant group membership with source records/paths | Preserve missing role/owner information. Do not infer a behavioural baseline from a job title or attach unrequested accounts. |
| Read relevant access | Assigned accounts and known access-related focus; relevant privileged/sensitive access with supporting account-to-group-to-asset paths and selection basis | Bounded potential impact, not exhaustive inventory. Preserve snapshot identity, unknown historical permissions, omissions and selection versus truncation. |

Research can request supported context/access operations and select allowed refinements faithful
to the focus. Code resolves accounts and computes deterministic records/paths. Exact relevance
rules must be defined before implementation; a field labelled relevant is not an algorithm.
No free-form graph traversal, model-authored Cypher or guessed permission edges.

The present graph models group membership and grants. A recorded grant does not encode arbitrary
fine-grained read/write/admin rights or prove an asset was accessed. If a question needs rights
or historical permission evidence absent from the source, return that limitation rather than
inventing detail. Event-time applicability can remain requested even when the only available
permission evidence is a snapshot. Role evidence, permission evidence and observed activity
remain distinct in the response.

#### Connected activity

| Operation | Assigned anchor and output | What the link does not establish |
| --- | --- | --- |
| Read same-source activity | Source addresses resolved from the referenced activity; other-account login records using those sources inside the authorised window, with outcomes, times, counts and originating-event attribution | No graph address-sharing exposure, common operator, simultaneous connectivity or lateral movement inferred from address equality. |
| Read involved-device activity | Nonempty device identities observed in the assigned activity; dated use by other accounts in the authorised window, with device/link identity and supporting activity where resolvable | No expansion to every device ever used by the account; no inferred common control, compromise or simultaneous use. |

An event can carry an involved-device anchor even when a particular graph edge is absent.
Code derives anchors from assigned records, then obtains supported relationship evidence.
Missing device identifiers are explicit; blank values never form a shared device. If no usable
anchor exists, distinguish that missing prerequisite from a completed search with no peers.

Architecture-specific constraint: graph_ingestion.py builds used_device edges from successful
sign-ins only and stores sorted usage times. neo4j_graph.py checks each participant's times
within the requested interval. Thus the current graph supplies successful-use links, not all
attempted device activity, and two uses in one window need not be simultaneous. A failed login
can still be activity evidence in the log; graph absence must not erase it. If the assigned
question requires failed attempts as well, planned collection must use the log evidence alongside
graph results or report the unfulfilled part. No automatic graph-schema change is authorised.

Author-requested verification, 8 November 2026: distinguish relationship meaning from its
construction rule. used_device links an account/person to the device recorded on a sign-in;
it does not mean authentication *to that device*, device ownership, or physical-human identity.
The current builder explicitly filters outcome == success (graph_ingestion.py line 45), and
the independent graph_verification.py excludes failed rows (line 66). T19's Implementation
section documents the same rule; test_native_inspection.py's expected graph also applies it.
The separate assigned_device relation comes from organisation device_assignments and has no
login-outcome filter. The generator can attach device_id to failed login rows, but those rows
do not contribute used_device edges/timestamps under the current build. Source/document/test
inspection only; no running graph query or test execution. This confirms current behaviour,
not a ruling that the new design must preserve the success-only construction rule.

Subsequent author ruling, 8 November 2026: broaden used_device to successful and failed
sign-in records with known devices during T55's planned 30-day expansion. T55 owns the deferred
graph/query/verification reconciliation as well as the expanded data. Planned connected-activity
interfaces must preserve outcome distinctions and support that intended meaning, while current
source capability remains success-only until delivered. No immediate build or invented device
identity. This resolves the semantic question; resume documentary evidence design next.

The current graph relationship timestamps are not demonstrated durable event references.
Joining back to source records needs validated identity rules; do not guess a unique event
from a timestamp when several records could match. Return relationship evidence as such, with
its actual source basis and an explicit unresolved event-reference gap where necessary.

Code assembles links and counts, retains source/build identity and checks scope. Research may
inspect relevant connected evidence within the assigned task, but investigating a returned
account as a new subject requires chat to construct a new authorised request. Same-source and
same-device links remain different types even when both concern the same accounts.

Shared return obligations: per-subject results, requested/checked periods for activity-derived
links, snapshot dates for permissions, evidence/paths, operation outcomes and explicit gaps.
Related-record pagination must preserve full matching counts where computable and disclose
what reached chat. The five-document-passage rule is not a limit on graph nodes or login rows;
their delivery limits remain separate execution/interface decisions.

Next: documentary evidence discovery versus exact passage reading, including entity-to-passage
graph links, applicability and RAG candidate/ranking/retention stages. Remaining access-selection,
record-resolution and paging details stay visible before final tool signatures are frozen.

### Planned documentary evidence interface

Design continuation, 8 November 2026. Covers explanation evidence, threat guidance,
investigation guidance and reference material. The family groups evidence obligations, not
all corpus subjects into one mandatory retrieval algorithm. Derived from the approved tasks
and actual RAG/graph architecture; legacy agent-tool interfaces remain outside this design pass.

Three operations have different success criteria and should be explicit at the interface:

| Operation | Input meaning | Result and success criterion |
| --- | --- | --- |
| Discover relevant passages | Assigned evidence question/focus, authorised subjects and typed source filters | Ranked candidate/retained passage evidence with retrieval verdict and limitations. Returning candidates does not establish relevance, sufficient coverage or a resolved question. |
| Find subject-linked passages | Assigned resolved entity and the permitted direct mentions relationship | Passage references associated with that entity, with their linking basis and source/build identity. Missing mentions do not prove no relevant documents exist. No arbitrary graph traversal or unassigned entity investigation. |
| Read identified evidence | A trusted document/passage reference from the request or permitted discovery, bound to a source version/snapshot, with a bounded context need | Exact referenced content and necessary available context, or explicit missing/version/unavailable result. Similarity-ranked substitutes cannot satisfy this operation. |

Graph links supply a candidate discovery route, not another copy of document text. The graph's
chunk references resolve to PostgreSQL passage content from the same selected paired build.
Reading a graph-linked passage must not silently re-search by title and return a newer or
different version. General policies or threat guidance may have no direct account mention, so
graph-linked discovery cannot be the sole route or a mandatory filter on all corpus searches.

#### What research chooses and code controls

Research can formulate focused searches for the assigned evidence need, inspect relevance,
request permitted context and perform bounded follow-ups. It cannot redefine user intent or
treat a selected explanation as permission for confirmation-only retrieval. For a required
standard procedure, code-built search/check obligations still apply; model query refinements
do not replace those protected searches or waive their coverage.

Code binds the operation to its task/subjects, validates typed filters and source eligibility,
builds safe queries, runs retrieval and attaches original evidence and receipts. Separate search
targets where necessary to preserve policy conditions and account-specific records; combining
everything into one broad query is not a coverage guarantee. Exact mandatory search templates
remain T45's package-path decision, not invented here.

Applicability_time guides evidence selection and later assessment; it must not be translated
blindly to a publication-date equality filter. Preserve older still-effective policies, recorded
exceptions, supersession and relevant change history where available. Source metadata does not
by itself prove that a policy or exception applies to this person/activity/time. Unknown validity
remains visible. General threat/practice guidance does not establish that a case event occurred.

#### Retrieval stages and evidence preservation

Retain the approved hybrid baseline: filtered keyword/dense candidates, fusion, optional reranking
and up to five passages per search. Record candidate, reranked, retained and actually delivered
evidence separately, with query/filter provenance. No new ranking method or threshold adopted.
The current uncalibrated weak/not_calibrated verdict must survive the handoff; task-level evidence
found does not convert it into a confident match. An exact source read is not given an invented
similarity score. Retrieval failure remains different from a completed search with no match.

Multiple focused searches may contribute more than five unique passages to the response under
the author's ruling. Deduplicate identical version-bound passages without losing task/subject
attribution. Preserve relevant supporting/competing evidence and necessary conditions. Record
selection decisions and omissions; rank alone cannot certify that important evidence survived.

The five-per-search rule does not yet define the limits of direct graph-reference listings or
exact context reads. These operations need explicit bounded delivery rules before implementation;
do not use repeated direct reads to bypass execution limits or silently import a whole corpus.
The interface must expose what was delivered and any truncation. No numeric read/list cap or
automatic context-expansion policy is selected in this section.

Known document identity does not guarantee a single returned passage answers the question.
Reading context must preserve relevant headings/conditions and identify each returned passage
from the original version. Prepared chunk text may omit formatting/references under the existing
chunking design; citations must use preserved source provenance rather than fabricate removed
reference text. Source documents remain available as source artifacts under their current rules.

#### Example and remaining interface choice

For the MFA question, the research assignment can seek the governing policy through corpus
search and the named account's exception through scoped discovery or an available mentions
link, then read the relevant conditions. The link alone cannot establish approval; the policy
alone cannot establish that an exception exists. Either route can fail independently and must
leave its own receipt. This example does not assert that a particular graph link exists.

Next substantive choice: whether document subjects require separate model-visible tools, or
typed options/internal retrieval specialisation behind common discovery/read interfaces. Compare
actual evidence needs across policies, case records and threat guidance before ruling. Exact
tool count remains open; the three operations above are a proposed interface organisation.
Required guidance-source approval, keyword strategy, package searches and original K04 gate
path decisions also remain visible. No current tool migration or RAG/graph build performed.

### Subject-specific documentary tools: approved direction, 8 November 2026

8 November 2026: author recalls the earlier discussion and leans toward separate tools by
document subject, while requesting an independent recommendation. History confirms this was
an open decision, not an already approved split. Author subsequently agreed to a small set of model-visible search
interfaces differentiated by evidence purpose, not one tool per file kind or department.

| Proposed search purpose | Evidence question and differentiated obligations |
| --- | --- |
| Threat knowledge | Which known attack behaviours could fit? Retrieve approved technique descriptions, relevant conditions and limitations; general knowledge cannot establish a case event. |
| Organisation rules | What policy or rule applies? Preserve governing text, relevant versions, validity and exceptions/conditions; a policy does not prove an account-specific approval. |
| Case-specific context | What recorded explanation concerns this account/activity? Search approvals, travel, helpdesk/device changes and other relevant case documents using entity/time context; preserve competing material and uncertainty. |
| Investigation practice | What approved next check addresses this specific unresolved question? Return relevant practice with prerequisites and limits; no execution of the recommendation. Source-set approval remains open. |

These four purposes are the approved direction, not final tool names/signatures or exclusive storage
partitions. An email or meeting note can supply case context or policy-change evidence; document
kind alone must not decide eligibility. Sources/passages may legitimately support more than one
purpose, with explicit eligibility mapping rather than accidental exclusion. Avoid a catch-all
HR tool mixing organisational facts, general policy and dated individual records. Structured
account facts remain in the separate account/context family.

Use shared retrieval infrastructure, source storage, graph-linked candidate resolution, citation
validation and exact-reading machinery underneath. Each search interface should own meaningful
typed inputs, source eligibility and retrieval obligations, not only a different name over an
identical unconstrained query. Separate vector stores, embeddings or rerankers are not implied.
One shared exact-reference reader is recommended because source/version resolution follows the
same rules regardless of discovery purpose. Graph-linked discovery can be shared internally;
whether it remains separately exposed depends on the final interfaces.

Tradeoff: purpose-specific interfaces make intended evidence categories explicit but add a
routing decision. The researcher can call more than one for a mixed question; code-required
coverage cannot depend solely on that choice. A wrong route could miss evidence even when
retrieval works correctly. No local evaluation has established that separate tools outperform
a common typed search interface. The existing mixed policy/exception/threat cases must test
selection and evidence delivered, not merely whether every tool was called.

Comparison: a common typed search interface can enforce the same policies with fewer tool
definitions, but the caller must express all category differences as options. Recommend separate
search interfaces here because the evidence questions differ in purpose, necessary inputs and
interpretation limits, while keeping common internals to prevent implementation drift. This is
a design judgement, not a claim of universal best practice or measured improvement.

Source check: Anthropic's [Writing effective tools for agents](https://www.anthropic.com/research/writing-tools-for-agents),
11 September 2025, consulted 8 November 2026, recommends a small number of distinct workflow-oriented
tools and warns that overlapping tools can confuse selection. It supports the design criterion,
not this exact four-purpose split. Earlier security research likewise did not isolate the
benefit of subject-specific tool exposure. No API integration or model experiment performed.

Author accepted this direction, including shared retrieval internals and a shared exact-reference
reader. Tool naming, source eligibility, interface details and guidance-source adoption remain
separate work. No new retrieval performance claim follows from approval.

### Initial corpus-to-purpose mapping

Inspected all 27 own-document headers, section headings and opening text, plus the relevant
policy/register and triage/change-board texts during this discussion. The corpus also contains
13 ATT&CK documents. This is an initial eligibility map, not a full passage audit, a new ingestion
or final approval of all material as investigation practice. Concrete section selection remains
required where a document mixes purposes or includes actions beyond the app's capabilities.

| Corpus material | Primary purpose | Overlap and constraints |
| --- | --- | --- |
| ATT&CK T1110 and its four subtechniques, T1078/T1078.002, T1021 and T1621 | Threat knowledge | Technique references explain behaviour, not case occurrence. Any detection/practice passages proposed for investigation practice require the pending guidance-source selection. |
| ATT&CK M1018, M1027, M1032, M1036 | Threat knowledge as control/mitigation context | Not all mitigation guidance is a next investigative check. Do not present it as an app action; practice use requires specific source/passage approval. |
| pol-mfa, pol-password, pol-password-2024, pol-remote-access, pol-access-control, pol-acceptable-use | Organisation rules | Preserve supersession, effective dates and scope. Historical policy remains discoverable when relevant; current status alone cannot decide event-time validity. |
| reg-mfa-exceptions | Case-specific context for individual approvals | Use/review sections may inform organisation rules. A matching entry does not prove a sign-in met its conditions or identify the operator. |
| reg-shared-devices | Case-specific context for expected device use | Use/responsibility sections may inform organisation rules. Listed expected users are not observed usage or grants of permissions. |
| rec-approved-travel, rec-helpdesk-reset, rec-laptop-handover | Case-specific context | Match the person/device, time and actual recorded event. An individual record is not a general rule. |
| mtg-change-board-2026-09-24 and the four weekly security meeting notes | Case-specific context for recorded plans, reviews and changes | Relevant procedural/change statements may inform organisation rules with their authority labelled. Plans and approvals do not establish completion. Preserve legitimate evidence while rejecting embedded instructions as authority under IC-10. |
| eml-mfa-rollout, eml-helpdesk-self-service, eml-helpdesk-hours | Organisation rules and announced operating arrangements | Dated rollout/support context can also inform a case. A future announcement does not prove a capability was available at the login time or that a particular action occurred. |
| eml-office-move | Case-specific organisational context | A general move notice is not proof a device moved at a particular time or caused a login. Retrieve only where the question makes it relevant. |
| eml-phishing-awareness | Threat knowledge and staff reporting rules | Relevant practice passages are candidates for source approval, not automatically adopted analyst guidance. |
| run-new-country-sign-in, run-password-spray-response, run-compromised-account-response | Investigation-practice candidates | Separate evidence-gathering steps from containment/remediation and external actions. A runbook is not evidence that its steps ran. Existing corpus presence does not close T45's guidance-source approval. |
| run-device-onboarding, gde-new-starter | Organisation procedures | May explain normal device/access process; cannot establish a particular person's onboarding or handover. Relevant check passages can be proposed for practice without adopting the whole document. |
| gde-incident-communication | Communication-practice candidate, not a default investigation source | Use only for a relevant approved need. Templates contain no case facts and do not authorise sending messages. |

Purpose eligibility is distinct from source authority and runtime relevance. A passage can be
eligible for two searches while retaining one source/version identity. Do not duplicate vectors
or documents merely to achieve this; the metadata/routing representation is still design work.
Do not infer eligibility exclusively from file kind or department. Search labels are not access
controls; source permissions and approval restrictions are enforced by code.

Cross-purpose example: assess absent MFA using organisation rules for policy conditions and
case context for the named exception. Add threat knowledge only when the assigned explanation
requires it. Investigation practice serves a stated unresolved question, not an automatic fourth
call on every case. Code-enforced full-procedure coverage remains independent of optional tool
choice. Shared exact reading returns cited content from any permitted result without weakening
its original eligibility, version or scope restrictions.

Next: define the four search interfaces' inputs and evidence obligations against this map;
select the bounded guidance source set for author review separately. No legacy reconciliation yet.

### Four documentary search interfaces: inputs and obligations

8 November 2026, routine interface definitions under delegated authority. Names below are working
names, not implemented tools. Each operation receives trusted execution context from code:
request_id/task_id, assigned subjects/focus, applicability_time, selected source snapshot and
permitted source set. Those values are resolved from the assignment, not independently rewritten
by the model. A model selecting a task handle cannot enlarge that task's authority.

The research model supplies a nonblank query describing the bounded evidence need. Query text
is search data, not a place to set permissions, time windows, required checks or source authority.
The code validates structural compatibility and typed options; semantic query quality remains
model/evaluation responsibility. Do not claim a query can be proved faithful by schema validation.

| Working search interface | Additional model-selected inputs | Evidence obligations |
| --- | --- | --- |
| search_threat_knowledge | Optional explicit technique/control references already grounded in the assignment or retrieved evidence; omission means no identifier restriction | Relevant behaviour descriptions and conditions from permitted threat sources. Distinguish technique, mitigation and detection material. Preserve caveats and potentially competing explanations; do not turn a technique match into a claim that it occurred. |
| search_organisation_rules | Optional bounded rule topic when needed to refine the query; event/date context comes from the task | Governing provisions plus material conditions, exceptions and version/supersession evidence. An older applicable policy must not be excluded merely for being older. Report conflicts or uncertain authority; do not automatically choose by latest publication date. |
| search_case_context | Assigned subject subset when the task has several subjects; optional recorded-context category such as approval, travel, helpdesk, device_change or organisational_change | Relevant individual/context records with subject/date links, scope and competing or limiting material. Distinguish request, approval, scheduled change and recorded completion. A general rule cannot satisfy a missing individual record. |
| search_investigation_practice | The specific unresolved question supplied by task focus; optional references to already retrieved evidence that make the question concrete | Approved practice passages relevant to that uncertainty, including prerequisites and limits. Distinguish available app checks from external analyst actions. No advice is recorded as executed and no unapproved source becomes eligible through a tool call. |

Avoid redundant parameters: a topic/category/refinement is omitted when query plus trusted task
focus already expresses it. Optional categories narrow retrieval; they are not a mandatory
exclusive partition of document kinds. No guessed technique IDs or invented context categories.
The task's relevant missing dates retain their explicit unknown/reason states. Unknown evidence
existence permits a search; missing information essential to form a meaningful task is handled
before dispatch under the request contract, not silently guessed inside a tool.

For case-context searches, omission of a subject subset means all assigned targets; it cannot
mean all accounts in the organisation. Publication date is not the time of the described event.
Entity association may be established by explicit record identity, source text or a validated
graph link; absence of a mentions edge is not a conclusive negative. Exact entity-match filters
must not remove relevant organisational changes that lack a direct account mention. Return the
association basis and its uncertainty. Concrete category/filter representation remains to be
checked against the source schema before implementation; no inferred application field added.

For practice searches, the evidence references can point only to available, validated evidence
within the permitted execution context. This does not introduce cross-batch memory or the
previously unapproved available_evidence_refs request field. The agent does not need to search
practice merely because another search returned no match; practice must serve its assigned task.

#### Task compatibility and required breadth

Document search purposes are not extra user intents. retrieve_explanation_evidence can use
threat knowledge, organisation rules and case context as its assigned evidence question requires.
retrieve_threat_guidance uses threat knowledge; retrieve_investigation_guidance uses approved
practice. retrieve_reference_material can use the appropriate permitted purpose when locating
unknown material; known source identity can go directly to the shared exact reader.
Practice retrieval is not silently added to an explanation task, and source eligibility/approval
still applies to reference requests. Other task types do not gain arbitrary documentary access
merely because the research agent has these interfaces registered.

When an explanation needs both a rule and an individual approval, required coverage names both
obligations; one successful tool call cannot satisfy both by its name alone. Research chooses
focused searches within that coverage. Code-owned full-procedure search templates and required
checks remain independent of model-selected queries. Neither a universal call-all-four rule
nor a particular number of queries is adopted here.

#### Shared result guarantees

Each search returns the same underlying evidence/receipt shape: source-bound passages, query
and effective filters, retrieval verdict/reason, checked source scope, candidate/retained/delivered
references, omissions and failed components. Subject-specific annotations explain why material
was retrieved without changing original text or presenting model observations as facts.
Scores/trace details can remain in the saved artifact while material limitations reach research
and chat. Five passages per search remains; no combined five-passage cut is added.

No-match, irrelevant candidates and failed search are distinct. In particular, returned material
with weak/not_calibrated relevance cannot be described as a verified matching approval. Exact
validation, applicability and semantic coverage are separate from search execution completion.
Purpose eligibility selects candidates; it is not evidence of source authority or a permission
grant. Code enforces approvals and source access for every search and subsequent exact read.

Next: define the shared exact-reference reader and graph-linked discovery exposure, including
bounded context reading, before stop/retry and total-context rules. Legacy reconciliation remains
deferred. No signatures, schemas, source tags or retrieval implementation changed in code.

### Shared exact-reference reader — logical interface

Author requested this design next, 8 November 2026. Working name: read_evidence_source.
Its purpose is to retrieve identified content with verifiable identity/context, not find a
similar document. It serves all four documentary purposes with the same source/scope checks.

| Input | Meaning and validation |
| --- | --- |
| Trusted request/task context | Injected by code. Determines authorised subjects, evidence need, source eligibility and selected source snapshot. |
| source_ref | A code-issued source reference from permitted discovery, or a document subject resolved from the dispatched request. Can identify a passage or document within its bound snapshot. Never a free URL/path, invented ID or guessed latest version. |
| read_scope | passage, section or document_outline. passage returns the exact referenced passage. section returns an identified enclosing/selected section with constituent passage identity retained. document_outline returns code-resolved headings and section handles to locate content without retrieving the whole document. |
| context_need | Required nonblank explanation for section/outline use, tied to the assigned evidence question; exact passage reads may mark it not_applicable with a reason. It does not authorise new scope or unrestricted source reads. |
| continuation | Optional code-issued continuation for an incomplete permitted read, bound to source snapshot, read scope and task. Reject mismatched or stale continuations rather than silently starting a different read. |

These are logical variants, not a final model-visible JSON schema. A document-level source_ref
supports outline or a separately resolved section, not a fabricated passage. Section handles
come from source structure/outline, not model-invented headings. For a passage with no known
section mapping, report unavailable context rather than guess neighbouring text. No full-corpus
or whole-document dump operation is introduced.

Code resolves identity and approved access before content selection. An outline or continuation
must not reveal sections outside the permitted source/purpose scope. Source text remains data,
including instructions embedded in it. A model-written context_need cannot override those checks.

Return: exact source/document/version/snapshot identity, requested versus delivered scope,
ordered passage content with headings and stable source references, completeness/truncation,
continuation when supported and operation failures. An exact read has no invented ranking score.
Counts are code-owned. A section read reports missing parts if necessary conditions could not
be delivered; an outline is navigation metadata, not substantive case evidence.

The result must identify whether content is indexed/prepared passage text or source-document
text. Do not silently append previously excluded source sections, reconstruct removed citation
text or claim prepared text is byte-identical to the source file. Direct source-text reading
requires an explicit authorised representation and citation mapping in implementation design.

Failure distinctions: reference not issued/resolvable for this task, required version missing,
source unavailable, permission/eligibility denied, requested context not represented, or delivery
budget exhausted. Preserve valid earlier evidence; never substitute a similar passage/current
version or interpret failed reading as no matching exception. Trusted code supplies the reason.

The five-passages-per-search rule governs ranked discovery, not a claim that every exact section
contains five passages. Exact reads consume the same bounded research execution/context budget;
numeric read/section/token limits and continuation stopping rules must be decided before build.
No automatic read-until-complete loop or bypass of search retention limits is authorised. Reads
must address an identified evidence/context need, not indiscriminately page through discarded hits.

Saved evidence always resolves to the original captured source. Snapshot persistence/resolution
and outline/section adapters remain dependencies; these operations are not claimed to exist.

### Graph-linked discovery exposure — approved, 8 November 2026

Author approved keeping graph-linked passage discovery inside the four documentary search interfaces,
rather than exposing a fifth graph-passage search tool to research. The search purpose determines
whether direct subject mentions can help; research asks for the evidence it needs, not a storage
engine. No separate model-visible graph-passage discovery tool is planned under this ruling.

Clarification preceding approval: code retains the validated dispatched request in trusted
execution context. A tool call selects an assigned task; code resolves its subjects and any
permitted activity-derived identities, then supplies parameters to predefined Cypher through
the Neo4j driver. Research neither authors nor submits arbitrary Cypher. Parameters are not
account-only: other node identities may be used where the specific task and operation permit
them. A node's existence is not permission to explore it. Alert/event IDs are not assumed to
be graph nodes. Exact runtime state plumbing remains the later orchestration design.

Code can use permitted direct mentions links from assigned/resolved subjects as one candidate
route and fetch their passages from the matching PostgreSQL snapshot. Corpus search remains
available for general rules/threat material lacking entity links. No arbitrary traversal, new
subject investigation, automatic exclusive graph filter or new graph schema is implied.

Expose route receipts even though route execution is internal: whether corpus and graph-linked
discovery ran, their candidate identities, failures and omissions, plus each retained passage's
discovery basis. A failed route is not a no-match route. Whether a graph-route failure makes
the task partial depends on its required evidence obligations, not simply on having two engines.
Any permitted degraded operation must obey the existing paired-store readiness rules; this
proposal does not authorise bypassing a failed integrity/startup check.

One search call still returns at most five selected passages across its internal routes, not
five per route hidden inside one call. Multiple focused calls retain the approved no-second-five
cap on combined responses. Candidate merging/ranking must preserve stage-level provenance;
the exact way graph candidates participate in selection remains an explicit retrieval decision,
not an unapproved change to hybrid fusion or score weights.

Alternative: a separate graph-linked discovery tool gives research direct route choice but adds
an implementation-oriented decision and another possible omission path. Prefer it only if a
concrete assigned evidence question needs that independent operation. Account/access and
connected-activity graph operations stay explicit in their own families; this recommendation
concerns documentary mentions discovery only. A known passage reference goes straight to the
shared reader without a redundant graph or similarity search.

### Internal discovery routes and candidate preservation

Design continuation under delegation. The exposure decision does not itself settle ranking or
prove graph-linked discovery improves retrieval. Preserve these obligations before choosing the
merge algorithm:

1. Code derives eligible routes from search purpose, assigned subjects and available source
   metadata. Direct mentions may help case-context discovery; general policy/threat retrieval
   must not require an entity mention. Exact route-selection rules remain to be specified per
   search purpose, with required versus optional routes explicit.
2. Record corpus and graph-route candidates separately, including route execution outcome,
   query/filters, source/build identity and any internal limit. Failed graph discovery is not
   a successful empty candidate set; no attempt to bypass paired-store readiness checks.
3. A graph-linked candidate resolves to actual passage content before it can count as delivered
   evidence. A mentions edge is a discovery basis, not a relevance score or proof of support.
4. Deduplicate identical source-version/passage candidates, retaining every discovery basis.
   Never add a graph-link count to similarity scores as if the quantities were comparable.
   Normalisation/selection strategy requires an explicit design before changing the hybrid baseline.
5. Final search delivery stays at five passages per call across its internal routes. Record
   which candidates were selected, excluded or could not be resolved; the response retains
   material coverage gaps. Important evidence found but excluded is not a no-match outcome.
6. Required policy, account-record or competing-evidence obligations must survive at task level.
   One high-ranked passage does not fulfil an unrelated obligation. Multiple focused calls may
   be needed within the eventual budgets; neither automatic retries nor unlimited retrieval is
   adopted here. No second five-passage cap is applied when combining their results.

Selection coverage includes a semantic judgement. Code can require named evidence needs,
track source identities and enforce delivery rules; it cannot prove a passage supports or
contradicts an explanation just by its type, score or graph link. Research observations and
the existing retrieval/assembly/application evaluations still matter.

Next substantive choice: how graph-derived candidates join corpus candidates for ranking and
selection, preserving the existing keyword/dense baseline and visibility of competing evidence.
Exact-reader scope/budgets and stop rules remain pending. No tool implementation or legacy
reconciliation yet.

### Candidate ranking direction — approved, 8 November 2026

Author approved a common relevance-ranking stage for the unique passage candidates admitted from
corpus search and permitted graph discovery. Keep origin/basis attached, but do not reserve a
fixed number of final places merely because a passage came from the graph rather than search.
A mentions link establishes a connection, not that its text answers the evidence question.

Approved sequence for a focused search with reranking enabled:

1. Obtain the normal bounded hybrid corpus candidates and the bounded permitted graph-linked
   candidates. Keep each route's receipt and its own preselection limits visible.
2. Resolve graph references to passage text from the same paired build; reject unresolved
   versions visibly. Deduplicate by captured source/passage identity, retaining all route bases.
3. Submit the admitted combined pool to the same relevance reranker for that focused question.
   Do not assign graph candidates invented cosine/fusion scores or require them to pass a
   corpus-only shortlist again before scoring.
4. Return up to five ranked passages, preserving ranking and omissions in the trace. After
   multiple focused searches, retain task-required supporting/competing evidence under the
   approved no-second-five-cap rule. Exact requested references use the reader, not a ranking
   contest against unrelated documents.

This expands the rerank input beyond the current corpus-only fused shortlist when additional
graph candidates are admitted. This retrieval direction is now approved separately from the
exposure ruling; implementation is not released. Final combined-candidate budgets and fair route admission remain open; no
unbounded pool or arbitrary graph-first cutoff is implied. Preserve the existing keyword/dense
fusion inside its route until that strategy receives its own ruling.

Do not confuse common ranking with completeness. Five highly similar passages may all address
one part of a question. Required policy/exception/competing-evidence needs remain separately
accounted for, using focused searches and explicit gaps where needed. Code tracks obligations
and delivered identities; it cannot prove semantic completeness from scores or source labels.
The mechanism for recognising/recovering important excluded evidence still needs design and
the existing coverage evaluation; this recommendation alone does not close AUD-062.

Alternative: fixed final slots per retrieval route. This guarantees route representation but
can retain an irrelevant graph mention while excluding a relevant corpus passage. It also
protects engine categories rather than investigative evidence needs. Not recommended as the
default without local evidence that such a quota improves the required coverage.

Disabled-reranker comparison and reranker failure require explicit policies before implementation.
Do not silently invent scores, drop graph candidates or claim that unchanged baseline ordering
defines the new combined path. Existing on/off evaluation gates remain; no model replacement,
new threshold, paid run or gold revision is authorised by this proposal.

Documentation/source check, 8 November 2026: Cohere's current official
[reranking guide](https://docs.cohere.com/docs/reranking-with-cohere) describes ranking an input
document list against a query independently of its retrieval source. Its current examples use
newer models; this is conceptual support, not an API-compatibility check or model migration.
The project's reranking.py names cohere/rerank-v3.5 through OpenRouter and records a score for
every supplied candidate. No network inference was executed. Shared scoring is a local design
recommendation; official documentation does not prove its retrieval coverage here.

Next: define bounded admission and preservation/recovery rules before final execution budgets
and the separately planned orchestration research. Reranker-off/failure behaviour also remains
explicitly unresolved; approval of enabled-path ranking does not choose either policy.

Three control points must remain distinct in that work:

- Admission: which candidates enter the combined pool, each route's limits and ordering,
  and which potential evidence was excluded before scoring. Deduplication alone does not
  bound a pool. Do not silently use a corpus-only ranking to eliminate all graph contributions.
- Delivery: which admitted candidates reach research and later chat. Five passages per search
  remains distinct from task completeness; preserve delivered evidence from separate searches
  and distinguish omitted material from no-match retrieval. Semantic sufficiency needs evaluation.
- Recovery: permitted focused follow-ups/exact reads when coverage remains inadequate, plus
  retry/stop handling for failures. Recovery stays within assignment and shared budgets; no
  recursive retries, unbounded pagination or mandatory success is implied.

### Candidate admission: approved separation, open numeric limits

8 November 2026. Candidate admission happens before common reranking. It determines which
passages get scored, so it must have its own limits, ordering and omission evidence. This section
records author approval of separate route admission allowances; new numeric budgets remain open.

Author approved separately bounded corpus and graph admission, followed by deduplication and the
already-approved common rerank. Source-specific admission allocations are not reserved final
answer slots. A combined work/context ceiling must accommodate the admitted pool or explicitly
report an incomplete admission; it must not silently take the first N concatenated candidates.

#### Corpus route

Keep the approved baseline for now: typed filters before dense/keyword retrieval, 20 candidates
per leg, reciprocal-rank fusion and the existing 20-passage fused shortlist as this route's
admission. Do not discard that provenance or claim those 20 exhaust the corpus. Improving keyword
construction/BM25 remains its separate T45/T41 decision. No change to those existing numeric
limits is adopted by the addition of graph candidates.

#### Graph-linked route

First constrain by the assigned task, permitted entity identities, source-purpose eligibility
and known compatible source metadata. Resolve direct mentions references to actual passage
content from the paired build. Do not filter out uncertain validity merely because publication
date differs from the event date. Missing eligibility/identity is handled explicitly rather
than assigned fabricated authority.

Admit a bounded set of additional unique passages, excluding duplicates already admitted by
the corpus route while retaining the graph discovery basis on those shared items. Duplicates
must not consume the additional-unique allowance; scanning/resolution still consumes execution
budget. An independent scan ceiling prevents unbounded work to fill a unique allowance.

When more graph-linked passages are eligible than can be admitted, a deliberate ordering is
needed. Stable ID order is reproducible but not a relevance policy. Prefer an eligibility-first,
query-relevance ordering within that linked subset, using an explicitly designed existing
text-ranking mechanism where suitable. Do not treat link counts or graph proximity as calibrated
relevance. The specific subset-ranking method remains a substantive retrieval decision, not an
implemented property or a reason to reapply the global corpus-only top-20 cutoff.

#### Limits and receipts

The graph additional-unique allowance, graph scan ceiling and total admitted text/token ceiling
remain to be selected against realistic candidate volumes and the chosen reranker/provider
limits. No evidence currently justifies declaring a particular number sufficient. First measure
the available linked-candidate distribution and passage sizes without model calls, then choose
a bounded provisional configuration and evaluate it with the existing coverage gate.

Receipts distinguish discovered candidates, duplicates, eligibility exclusions, unresolved
references, pre-rank truncation, scored candidates and final unselected candidates. Counts may
be complete only for an enumerated bounded population; if scanning stops early, report the
remaining size as unknown rather than pretend all possible candidates were examined. Original
identities and exclusion reasons stay inspectable; material limitations reach the model.

An admission limit means incomplete candidate coverage, not necessarily a failed entire task.
Task completion depends on its code-owned required obligations and declared coverage. Do not
mark a required exhaustive check complete after truncation. Conversely, a normal bounded search
does not promise exhaustive discovery. A source or route error is distinct from planned truncation.

Recovery can refine the same evidence question or read a specifically identified source within
the task. It must not automatically page through every rejected candidate, silently enlarge
limits or broaden the investigation. Exact-read and retry controls still need final definition.

Separate route allowances are approved. Next: choose the graph subset-ordering method and
measure volumes before assigning new numbers. The current corpus-route shortlist remains the
baseline; graph additional-unique and scan allowances are not yet set.

### Offline candidate-volume measurement, 8 November 2026

After author approval of separate admission allowances, reconstructed chunks and direct entity
mentions from the working default dataset using the repository's read_chunks/find_mentions.
Saved [measurement and source hashes](../research/45-candidate-volume-profile-2026-11-08.json).
No database queried, embedding/reranker/model call, rebuild or dataset edit. This is an unfiltered
single-entity structural profile, not the active serving snapshot, relevance or recall proof.

| Population | Entities | Entities without linked passages | Largest linked-passage set |
| --- | --- | --- | --- |
| People/accounts | 50 | 24 | 15 |
| Devices | 53 | 47 | 5 |
| Groups | 4 | 0 | 14 |
| Assets | 10 | 1 | 36 |
| Networks | 53 | 51 | 13 |

Total: 40 documents, 320 prepared passages, 257 entity-to-passage mentions. Passage length is
139–2,134 characters; nearest-rank 95th percentile 1,869 characters. These are character counts,
not model/provider tokens. Existing node categories were profiled, not authorised as new
investigation subjects. Multiple assigned identities can produce larger unions; purpose/date
eligibility and deduplication against actual corpus candidates were not measured.

Implications: for current single-account searches, all linked passages may fit a modest graph
allowance, while a common asset can produce more candidates. Many accounts/devices have no
mentions, reinforcing the need for corpus retrieval alongside graph discovery. Link counts do
not determine relevance and do not establish a safe cap for the planned 30-day corpus.

Do not pick a production allowance solely from the largest current account. Define overflow
ordering and scan/text budgets, then record a provisional configuration and validate the
existing evidence needs. The measurement supports load estimates only, not AUD-062 closure.

Execution note: the first attempt failed because the tokenizer vocabulary was uncached and
sandbox DNS blocked its download. The escalated rerun downloaded the public vocabulary and
completed. That preparatory download was not inference. No application defect was established;
both attempts are retained here. Temporary measurement script: /private/tmp/t45-candidate-profile.py.

Next: choose graph overflow ordering, then assign provisional numeric limits with their scope
and remaining validation requirements explicit.

### Graph overflow ordering — approved, 8 November 2026

8 November 2026: author approved exact semantic-similarity ordering within the permitted graph-linked
passage set when it exceeds its additional-unique admission allowance. Use stored passage
embeddings and the focused search query's compatible embedding, reused from the same search
where available. This is a local subset selection policy, not another whole-corpus top-20 gate,
an approximate vector index, a new embedding model or a second reranker call.

Approved order:

1. Resolve permitted direct mentions links and apply trusted source-purpose/snapshot constraints.
   Retain uncertain temporal applicability rather than misuse publication-date equality.
2. Record graph provenance on passages already admitted from corpus search and exclude those
   duplicates from the additional-unique allowance.
3. If the remaining eligible set fits all admission/text budgets, admit it without relevance
   pre-pruning. If the count allowance is exceeded, order that linked subset by query cosine
   similarity, with stable passage identity only as a tie-breaker, then admit the allowed count.
4. Combine the admitted routes and apply the already-approved common reranker. The preliminary
   distance remains distinct from the final reranker score. Record excluded candidates and
   preselection cause where enumeration is complete.

Graph linkage narrows the population first, so a passage that ranked poorly against the entire
corpus can still reach the reranker through its subject's smaller linked set. The graph route
does not require all query keywords to occur, avoiding that lexical hard gate. This does not
guarantee a critical exception/competing passage wins the subset ranking; coverage/gap recovery
and the original eval obligations remain. Do not convert similarity to a truth/confidence score.

Exact distance ordering applies to the fully resolved eligible subset. If graph enumeration,
source resolution or text budget stops first, report incomplete candidate coverage; do not
claim to have selected the best candidates from an unseen remainder. Text/scan budget overflow
handling and missing/query-embedding failure remain explicit execution-policy decisions.
No silently arbitrary fallback to database/ID order. No new numeric allowance selected here.

Alternative: lexical relevance inside the linked subset. It may help literal terms but can
miss paraphrased explanations or impose another all-terms gate if copied carelessly from the
current keyword leg. Recommend semantic subset ordering initially, with local coverage evaluation
deciding whether a hybrid subset strategy is warranted. This choice does not settle T41's
separate corpus keyword/BM25 comparison or waive its gate.

Primary documentation checked: [pgvector README, exact search and filtering](https://github.com/pgvector/pgvector#filtering),
8 November 2026. It supports exact distance ordering with filters. Exact nearest-neighbour
recall describes the specified distance operation, not semantic relevance or investigative
completeness. Current docs are conceptual support, not a deployed-version compatibility test.
No embedding, graph/database query or reranking run performed for this proposal.

Next: provisional graph admission/scan/text limits and explicit overflow/failure
behaviour, then remaining bounded follow-up rules. Legacy reconciliation stays deferred.

### Initial candidate-count ruling — approved provisional limit

Author approved up to 20 additional unique graph passages per focused search, alongside the existing
corpus shortlist of up to 20, for at most 40 unique candidates before the reranker input-size
guard. Duplicates already in the corpus pool retain graph provenance without consuming the
additional-unique allowance. Neither route must fill its allowance if fewer eligible passages
exist; no invented scores or filler. This is an approved provisional count,
not an established performance optimum, provider limit or implementation release.

Rationale: the offline current-source profile's largest single-account set is 15 and its largest
device set is 5, before purpose filtering or corpus overlap. Twenty would admit all of those
currently measured single-subject sets while bounding additional rerank work to at most the
size of the current corpus shortlist. The 36-passage asset example and multi-subject unions show
why the approved overflow ordering is still needed. This does not establish sufficiency for
the 30-day target, all possible questions or relevance of all admitted passages.

If more than 20 eligible additional graph passages exist, exact semantic ordering within that
linked set determines admission and the receipt records pre-rank truncation. Missing evidence
may justify a bounded focused follow-up; it never automatically raises the limit. Existing K04
and downstream coverage evaluations, not the count alone, establish adequacy.

The count ceiling is separate from query/scan runtime, token/text limits, per-request calls and
retry limits. Those remain open; 40 passages must not be presented as universally safe for the
reranker or chat context. Provider input handling must not silently truncate important text.

Session stop, 8 November 2026: author accepted this recommendation and requested a fresh session
at high context usage. Resume with input-size/scan limits and overflow/failure handling, including
reranker-off/failure policy and bounded recovery. Do not ask again about the approved candidate
counts, five final passages per search, separate route allowances, semantic graph overflow or
internal graph exposure. No implementation starts.

### Ranking input overflow — initial proposal withdrawn after research, 8 November 2026

Author accepted the revised direction after the research summary: keep the approved
candidate counts and distinguish query/individual-passage fit from actual request limits
and downstream chat context. Continue with those separate checks before selecting numeric
guardrails. This acceptance does not approve splitting, batching, new numbers or live calls.

Status correction: the author requested focused primary-source research before deciding.
The earlier approval question is withdrawn. Cohere documents the model context limit per
query plus individual document, not the combined text of all admitted candidates. The
initial explanation conflated those limits. Keep the proposal below as history, not the
current recommendation or an approved policy. Research is recorded in
[the focused overflow note](../research/45-reranking-input-overflow-2026-11-08.md).
Separate per-passage/query limits, API request limits, operational budgets and downstream
chat context. A narrower search is not established as the first remedy for size overflow.
No numeric limit, batching policy, chunking change or implementation is adopted by research.

Resumed from the saved candidate-count frontier. Inherited IC-06 requires evidence
preservation; IC-07/08 require truthful limitation and completion reporting. The approved
20 corpus plus 20 additional unique graph candidates and five delivered passages remain.
The open choice here is how to handle an admitted pool that exceeds the ranking input budget,
not whether limits or incomplete work must be disclosed.

Recommendation: validate the complete ranking request before submission. Preserve whole
prepared passages and their necessary headings. If an individual passage or the combined
request exceeds the supported input budget, do not silently shorten text or drop candidates
until it fits. Return an explicit input-size limitation for this ranking attempt, retain
earlier independently valid evidence, and permit a focused in-assignment recovery search
within the separately defined recovery budget. Do not repeatedly submit the same oversized
input, raise the allowance automatically, or label the outcome no_match.

Record the admitted candidate identities, size-check result and affected operation. An
unscored pool is not a successfully ranked result. Its references may support permitted,
need-specific exact reading, but do not authorise reading every rejected candidate. Task
completion follows the existing required-obligation rules; an optional failed attempt does
not erase fulfilled obligations. Where required work remains unsatisfied, preserve that gap.

Alternative for the author's ruling: deterministically reduce the pool by whole candidates
and rank the retained subset, with explicit exclusions and incomplete coverage. This can
return useful evidence immediately, but requires another selection policy and can remove
important evidence before the common reranker. No such reduction policy is adopted here.

Numeric limits remain unselected. Before proposing them, verify the configured provider's
per-query, per-passage and aggregate input behaviour, including automatic truncation and
the available token measurement. The saved source profile measured characters, not provider
tokens. No claim about provider limits, paid execution or runtime compatibility follows
from this proposal. Graph enumeration limits, reranker-off/failure handling and request-wide
recovery limits remain subsequent decisions.

### Separate input checks — design refinement, 8 November 2026

Under the accepted input-size direction, define independent checks rather than a shared
40-passage model window. These are logical responsibilities; numeric thresholds and overflow
recovery mechanisms remain open.

| Boundary | Code checks | What it must not claim |
| --- | --- | --- |
| Focused query | Validate size using a verified model-compatible measurement and the applicable query limit. Include the actual submitted text. | Shortening the question is a transport-only change; essential evidence needs must survive any reformulation. |
| Each passage with the query | Include actual submitted headings/text, query and model overhead in the fit check. Retain source identity and the measurement method. | Character counts or the embedding tokenizer are exact reranker-token measurements without compatibility evidence. |
| Whole API request | Enforce the approved candidate count and independently established request/payload and operational budgets. | Summed passage tokens must fit one 4,096-token window, or another provider's published request limit applies here. |
| Returned ranking | Validate every admitted candidate's score/index and retain the serving model/provider when available. | A score or echoed original text certifies that no internal truncation occurred. |

OpenRouter SDK source at commit f0ceb9be02fd9c78a4898382b74b36db11b41610 exposes no
rerank token-limit or truncation-switch field and no processed-text coverage receipt.
See the focused research note's follow-up. Provider-compatible token measurement and exact
runtime input handling remain implementation-readiness dependencies. No current overflow
bug is demonstrated. Unknown limits are unknown, not unlimited or permission to invent a cap.

The checks identify the affected boundary. Query repair, source-preserving passage splitting,
request batching and final incomplete-result handling remain distinct policy choices.
Do not repeatedly retry an identical known oversized request. Downstream evidence delivery
has its own context budget and cannot be certified by a successful rerank request.

### Oversized individual passage — approved direction, 8 November 2026

Author explicitly approved the controlled-splitting recommendation. The mechanism below
is the accepted direction: temporary source-linked pieces, all pieces scored, maximum-piece
parent score, one parent candidate/result slot and original prepared passage delivery.
The alternative of leaving splitting out was not selected. Numeric piece/work limits and
provider-compatible measurement remain open. This is design approval, not implementation
or verification of the exception path.

This is an approved exception path for a verified query/passage size failure, not a new
default chunking scheme. No current oversized passage has been demonstrated. IC-06/09
require preservation and source identity; the following mechanism implements that direction
in the design, with runtime proof still outstanding.

Use temporary source-linked splitting for ranking, subject to a bounded piece/work
allowance to be set with execution budgets. Keep the stored passage and its identity unchanged.
Code partitions the prepared text using existing paragraph/sentence structure where possible,
retains necessary headings, and records exact source ranges. The pieces must cover the whole
passage without silently dropping its tail. A heading or individual unit that cannot fit,
or a piece allowance exhausted before full coverage, produces an explicit size limitation.
Do not introduce model-written summaries as substitutes for source text.

Score every piece against the same focused query with the same model/settings. Use the
maximum piece score as the parent passage's ranking score, following Cohere's documented
internal-chunking example. This is an approved local design, not a guarantee that our
splitting reproduces provider internals. All pieces must be successfully accounted for before
claiming full scoring of that parent; a partly scored parent cannot silently enter the normal
complete ranking. Preserve useful prior evidence and the failed attempt under existing rules.

Merge back to parent passages before selecting the final five. One original passage consumes
one candidate allowance and at most one result slot regardless of its number of pieces.
Pieces consume additional processing budget, not additional unique graph admission places.
No batching across API calls is implied by this proposal.

If selected, deliver the original prepared parent passage with its conditions and provenance,
not merely the highest-scoring piece. If downstream context cannot carry the necessary text,
that is a separate explicit delivery limitation, not permission to silently cut it. References
continue to identify the same source snapshot; no corpus rebuild or new persistent chunk IDs.

Primary basis: [Cohere best practices](https://docs.cohere.com/docs/reranking-best-practices)
supports controlled chunking and maximum-piece aggregation. Our parent identity, budget,
failure and delivery rules apply IC-06/07/09 to that mechanism. More pieces can increase a
parent's opportunity to get a high score, and splitting can separate related conditions.
Existing retrieval/retention validation must cover those risks before relying on the path;
no new acceptance gate or calibrated confidence claim is created here.

Unselected alternative, retained as decision history: leave automatic splitting out of the initial implementation and return a clear
size limitation for oversized passages. This avoids an unproven recovery path but leaves such
passages unranked. Either choice retains size checks and truthful gap reporting. Numeric
piece limits and provider-compatible measurement remain open; no implementation release.

### Tool exposure: source grounding and approved role restriction

Read-only code inspection: tools_for currently returns find_suspicious_activity, search_logins,
lookup_ip_reputation and lookup_account; build_agent exposes that collection to the existing
single agent. T25's peer/corpus tools and T26's investigation package are planned, not demonstrated
as current tools. The eleven evidence-task names are obligations, not eleven implemented tools.
This inspection establishes registration only, not complete capability or runtime proof.

Author approved research-only exposure on 8 November 2026: all model-initiated investigative
retrieval goes through the research boundary. Chat receives validated evidence via that boundary,
with no direct narrow-lookup exception. A deterministic input/identifier resolver is not a second
investigative model and need not be an exposed chat tool. Code continues to enforce required checks
through the shared core; these cannot depend solely on research choosing the right tools.

Spec T05's older "No router tool, no sub-agent" and shared-exposure wording is reconciled with
this ruling. Central registration/construction stays; role-specific exposure is derived there.
Exact allowlists, full-procedure dispatch and T25/T26 ownership still need the final design handoff.
The ruling does not adopt a LangGraph topology or release any new tool for implementation.

### Capability mapping to the eleven evidence tasks

Historical implementation inventory: defer using this mapping until the planned tool design
is complete, under the design-order correction above. It does not define the future tool set.

**Author ruling, 8 November 2026:** current tools serve the new investigator design, not the
other way around. Existing interfaces may be repurposed, combined, replaced or removed when
the final design calls for it. No requirement to preserve a tool name, signature, model exposure
or legacy interaction merely because it exists. Treat the map below as an inventory of reusable
capabilities, not a commitment to retain current tools. This is design authority, not permission
to implement before T45's agreed research/review and build-ticket handoff.

Approved investigation outcomes, security constraints and existing acceptance gates remain
requirements. Distinguish retiring a tool interface from removing a required capability; any
proposed change to a settled requirement or gate must be explicit. For example, reputation
enrichment may move into a code-controlled activity operation rather than remain a separate
model-selected tool. That placement is an option, not a decision adopted by this ruling.

This is a design mapping, not a claim of eleven tools or finished adapters. Code constrains every
call to the dispatched task's subjects, windows and permitted evidence needs. Read-only access
alone does not authorise arbitrary searches. Research can choose among permitted retrieval
operations within the task; mandatory coverage stays code-owned.

| Evidence task | Permitted capability needed | Existing seam and remaining work |
| --- | --- | --- |
| retrieve_triggering_activity | Resolve the exact alert/event and return its underlying login facts | Finding records exist; dataset-bound event resolution and exact-record delivery need adapters. Broad detection is not a substitute for exact lookup. |
| retrieve_surrounding_activity | Query login facts for assigned accounts/activity and windows | search_logins/core search exists; bind scope and preserve exact counts, coverage and sample limits. |
| inspect_activity_coverage | Inspect requested versus available history and known collection gaps | Add an explicit coverage result over dataset/log metadata; do not infer completeness merely from first/last returned sample rows. |
| retrieve_account_context | Look up recorded owner/role/group context | lookup_account exists; preserve missing information and links to activity-derived accounts. |
| retrieve_relevant_access | Select relevant recorded permission paths and sensitive assets | Graph account_groups/finding_radius seams exist; bounded relevance selection and task adapter remain. Do not expose arbitrary graph queries or full inventory. |
| retrieve_same_source_activity | Query logins from the referenced activity's source addresses | search_logins supports IP/time filters; derive addresses in code and retain originating-event links. This does not restore address-sharing exposure. |
| retrieve_shared_device_activity | Find dated peer activity for devices involved in the referenced activity | Graph/radius seams exist; T25 peer interface and involved-device selection remain. search_logins currently has no device filter. |
| retrieve_explanation_evidence | Search case documents, policy and exception records with supporting/competing coverage | Core search_corpus exists; T25 tool interface, task-specific searches and applicability context remain. |
| retrieve_threat_guidance | Search approved threat references within assigned focus | Reuse core corpus retrieval; explicit source eligibility and relevant context required. No general web tool is implied. |
| retrieve_investigation_guidance | Retrieve approved practice for the stated unanswered question | Reuse core corpus retrieval; T45 source-selection approval remains open. Do not execute the recommended action. |
| retrieve_reference_material | Search focused reference material or resolve a known document/passages | Core corpus search exists; exact version-bound document/passage resolution needs design. Similarity search alone does not prove that the requested document was returned. |

Read-only inspection for this map: tools.py exposes search_logins with exact aggregate counts and
a bounded row sample (limit 1–50), plus account/reputation/detection tools; KnowledgeBase exposes
search_corpus, account_groups, finding_radius and finding_walk. This establishes reusable seams,
not complete task support. Sampling must remain visible; no assumption that all matching rows
reach the model. Source/build binding and response adapters still require implementation design.

Existing find_suspicious_activity and lookup_ip_reputation have not been removed by this mapping,
but their current interfaces are not protected requirements under the author's ruling above.
Finding discovery before a subject is resolved, and required reputation enrichment, must receive
explicit workflow placement/task association before the final allowlist is frozen. Preserve the
existing mandatory reputation behaviour; this map neither waives it nor gives every evidence task
unrestricted reputation/detection access. Full-procedure package execution likewise remains
code-controlled, with its dispatch boundary to be settled before budgets/orchestration research.

Next after the role-exposure ruling and design-order correction: derive the planned capability
boundaries from the evidence tasks, define their contracts and restrictions, then follow-up/stop
and budget rules. Reconcile existing tools only after that design is complete. Read-only access
does not by itself authorise a capability for every task.

## Response contract: earlier working design, 8 November 2026

Historical draft: the consolidated response section above supersedes its provisional status
taxonomy. Retained to explain the design's development, not as a competing contract.

Author requested a scoped research checkpoint before extending this section on 8 November
2026. The draft below remains provisional. Research examines general two-agent delegation
contracts, prioritising security investigation and evidence-gathering examples, then comparable
research assistants. Compare published patterns with both request and response definitions;
do not treat our current field names or status matrix as established best practice.
This contract-focused research precedes further response design and is separate from the later
LangGraph orchestration research agreed above. Settled investigator requirements remain in force.

Scoped research completed: [two-agent contract findings](../research/45-two-agent-contracts-2026-11-08.md).
Six primary sources support bounded assignments, explicit context transfer, validated results
and traceable evidence, but no universal field schema. The closest inspected security example
is Microsoft's DTDA planner/executor paper. Recommendations for discussion: distinguish model
selections/annotations from the code-assembled evidence packet, and exercise incomplete outcomes
before freezing the status taxonomy. No recommendation automatically changes the contract.

This section records delegated design work, not individual author approval of each field,
an implemented schema or completion of the response contract. Inherited requirements are
IC-02 and IC-05–11: preserve evidence and competing material, distinguish missing outcomes,
retain source identity, enforce checks in code and keep retrieved content untrusted.

### Return structure and accountability

Treat the response as an evidence packet with a receipt for every assigned task. One response
belongs to one request_id. A batch retains separate responses. The packet contains:

| Field | Responsibility |
| --- | --- |
| request_id | Exact dispatched ID, checked by code. No guessed or replacement request. |
| task_results | Exactly one final result per assigned task_id, including tasks that could not run. Preserve original subject associations. Attempts are recorded separately, not mistaken for additional assignments. |
| evidence | Returned records, paths and passages with code-owned evidence IDs and source/version identity. Task results reference these items; within-batch reuse preserves each task's attribution. Actual supporting content must reach chat, not only references or research summaries. |

Code validates correspondence with the dispatched request and observed execution records.
Unknown or duplicate task IDs are contract errors. Missing task results are never silently
accepted as completed work. The coordinator records an explicit execution/contract failure
when a malformed response cannot be recovered within the eventual execution limits.
The research agent does not authoritatively certify that required checks ran.

### Separate execution from evidence yield

A completed search can return no matching evidence. Conversely, useful evidence can survive a
failed follow-up. Do not collapse these into one success/failure flag.

- Task execution uses complete, partial, failed, unavailable or omitted, with a reason for
  every non-complete outcome. Complete means the assigned retrieval/check procedure finished
  within its stated scope; it does not certify exhaustive discovery or a resolved case.
- Evidence yield uses found, empty or undetermined. Empty is permitted only for a completed
  applicable search/check that returned no matching evidence. It means no match in the checked
  scope, not proof that the fact or document does not exist. Incomplete work without usable
  results is undetermined. Usable returned evidence is found even if other work failed.
- Multiple subjects or retrieval operations retain their own outcomes beneath the task result
  where they differ. One successful component cannot conceal another's empty/failed outcome.
  Partial denotes completed work alongside outstanding obligations; failed denotes attempted
  work that could not complete, unavailable a required capability/source unavailable before
  execution, and omitted work deliberately not run with its reason. Preserve the underlying
  outcomes rather than infer them from evidence count.
- Coverage, truncation, applicability uncertainty and outstanding checks remain explicit even
  for complete/found results. Detailed shapes and aggregate precedence remain to be specified.

Illustration only: the exception-register search finishes with no matching entry, while the
policy search fails. The two outcomes remain empty and undetermined respectively; the combined
task is partial. Chat must not infer that no exception exists or that policy was checked.

Next design slice: evidence-item shapes, provenance and version binding, relevance/applicability
annotations, source content versus model observations, limitations and validation. Cross-batch
reuse, persistence mechanisms and execution limits remain open. No orchestration research starts
until contracts and execution boundaries are concrete.

## Response-contract walkthrough — 8 November 2026

Author agreed to start the research-informed design exercise. This is a paper walkthrough,
not a live retrieval, evaluation result or approval of a final response schema.

### One bounded question

Illustrative question: "Could an approved MFA exception explain why this login did not use
MFA?" Assume a resolved login reference, its recorded account/time and its MFA result are
already available. Do not invent a login ID or infer the MFA result from an exception.
The request uses assess_login_explanations with retrieve_explanation_evidence. Its known
focus asks for the applicable MFA policy, any account-specific exception and relevant
conditions or competing evidence. applicability_time comes from the referenced activity.
This assignment asks about the absence of MFA, not whether the whole login was legitimate.

The existing focus field can express this bounded question; this example does not demonstrate
a need for another free-form context field. Policy and register retrieval are component
operations within the evidence task, not automatically two user intents or new task enums.

Read-only grounding: current corpus pol-mfa.md requires a named, approved, time-limited
exception recorded in the register. reg-mfa-exceptions.md version 1.6 records named approvals,
reasons and dates, and explicitly separates approval from who performed a sign-in. These
files ground the example's evidence needs. The variants below are hypothetical retrieval
outcomes, not claims that those outcomes occurred against the corpus.

### Same assignment, three outcomes

| Variant | Evidence packet and execution receipt | What chat can conclude or do |
| --- | --- | --- |
| Both sources return useful evidence | Relevant policy passages and a matching exception entry, with account/date links, conditions, source versions and completed component operations. Any unverified condition remains explicit. | Discuss the recorded exception as a possible explanation for missing MFA, conditional on applicability. It does not prove who signed in or that the login was legitimate. |
| Policy returns; exception search completes with no match | Policy evidence plus the exception search's actual scope and no-match outcome. No invented exception evidence item. Search limitations remain visible. | Say no matching exception was found in the checked material. Do not infer that no approval exists from a retrieval miss. A verified complete register check could support a stronger bounded statement, but a generic search alone cannot. |
| Exception returns; policy retrieval fails | Preserve the exception entry and its provenance. Retain the failed policy operation and outstanding applicability work. Useful evidence must survive the failure. | State that an approval entry was found but its policy applicability could not be fully checked. A retry within the eventual limits or an explicit limitation is needed; never present policy as checked. |

### Ownership emerging from the exercise

The model proposes evidence selections and short observations of relevance or missing context.
Code resolves references to retrieved items and assembles preserved payloads/provenance and
observed operation outcomes. Chat interprets the assembled evidence for the user's question.
Code can enforce identity, scope and required coverage rules; it does not establish semantic
relevance or policy applicability merely by validating a reference. Selection still needs the
existing preservation/evaluation requirements so competing evidence cannot vanish unchecked.

This supports retaining separate evidence and operation-result records, without yet choosing
the final status taxonomy. An absent match needs a search receipt, not a fabricated "negative
document"; an unavailable check needs an explicit gap, not an empty evidence list alone.
No new schema fields, numeric retry limits or request changes are adopted by this walkthrough.

### Evidence lost at the handoff or rejected during validation

The author agreed to continue the remaining paper cases. These are hypothetical failure
conditions, not newly discovered application bugs or executed tests.

| Variant | Required handling | What chat receives |
| --- | --- | --- |
| Policy and exception were retrieved, but a size limit excludes the exception | Assembly records the excluded item's identity and reason separately from a no-match retrieval. Preserve original retrieved evidence under the evidence-retention requirement. Apply the eventual preservation/reselection mechanism before claiming adequate coverage; do not silently increase a budget. | The delivered policy plus an explicit exception-evidence omission. Until the exception content is delivered, chat cannot assess its terms or treat its absence as no exception. |
| A model-selected evidence reference does not resolve to an item retrieved for this assignment | Code rejects that reference and records a contract-validation failure. Retain independently valid evidence. Any repair is bounded by the eventual execution policy; never invent a source or silently map to a similarly named item. | Valid remaining material plus the affected task's unresolved evidence gap. No citation from the rejected reference. |
| A reference resolves to a document, but not the required source version | Code checks against the run's bound evidence identity or the original saved artifact. A current copy is not a substitute for a saved version. If the required version cannot be recovered, retain that explicit limitation. | Verified material plus an unresolved-version gap. No assertion that current text was the original evidence. |

Retrieval success, delivery success and reference validity are separate observations. A complete
search can coexist with an incomplete handoff. An omission notice conveys that material was
excluded; it does not provide that material's contents or support a substantive claim about it.
Merely naming an excluded evidence ID in model context does not satisfy IC-06.

Version validation requires a trusted binding from the retrieval/saved artifact, not only two
model-supplied strings that agree. Exact source fingerprints, version selectors and saved-evidence
loading remain implementation/design dependencies. Authenticity of a version also does not prove
that it applies to the event date; historical applicability remains a separate evidence question.

### Minimal logical handoff after the five cases

**Resume marker, 8 November 2026:** before writing the small response example showing
code-owned fields versus model observations, the author asked to settle how evidence limits
apply. Limit ruling recorded below; resume the example now. Do not lose or
replace the response-contract work with the later orchestration research.

Retain the three-part outer shape (request_id, task_results, evidence). Do not add a second
parallel packet solely to represent failures. Each task result links delivered evidence and
contains operation outcomes plus explicit gaps, including retrieval failure, assembly omission
and rejected references. Exact field names, nesting and aggregate statuses remain provisional.

| Information | Producer and check |
| --- | --- |
| Request/task identity and authorised scope | Code copies and validates against the dispatched assignment. |
| Delivered evidence with original content and source identity | Code resolves retrieved references and assembles the payload. Model selections remain subject to preservation rules. |
| Retrieval operation outcomes and checked coverage | Tool/core execution records supplied by code. Model prose cannot certify that work ran. |
| Assembly omissions and reference-validation failures | Assembly/validation code, with the affected task and reason. |
| Relevance or applicability observations and suspected semantic gaps | Research model, visibly marked as observations and linked to evidence where available. Schema validation does not certify these judgements. |

The downstream chat model must receive limitations alongside delivered evidence, not only in
an operator trace. Detailed attempts can remain in the trace while their material effect stays
visible in the task result. No final status enum, new numeric limit, automatic recovery loop or
saved-version mechanism is adopted by these paper examples. No LangGraph design yet.

### Evidence-limit ruling — approved, 8 November 2026

Read-only checks on 8 November 2026: spec T05 d12 and T05 decision 12 state five chunks
per corpus search, not five chunks across an entire research request. Existing retrieval
implementation and T03 also distinguish candidates from kept passages. Chunking limits an
individual passage; it does not bound the combined input from several searches and conversation.
The earlier paper case of an assembly size limit was hypothetical, not evidence that a new
response-wide cap already exists.

Author approved the recommendation: retain five passages per search for now; do not introduce a second global
five-passage cut when combining searches. Deduplicate identical evidence from the same source
version while preserving task attribution. Preserve relevant supporting and competing evidence
and necessary conditions; relevance selection must not become silent numerical truncation.
Two searches can therefore supply more than five unique passages to a response. This does not
authorise unlimited searches, waive existing budgets or settle the adequacy of five per search.

A finite model-context constraint remains. Exact token allocations and search/retry limits
belong to the execution-boundary design and must precede implementation. If essential evidence
cannot fit, do not silently drop it or replace it with an unsupported summary: surface the
coverage gap and use the eventually agreed bounded recovery/stop behavior. No numeric response
budget or automatic splitting mechanism is adopted here. Original K04 gates remain unchanged.

### Small response example: code data and model observations

Return point resumed after the limit ruling. This abbreviated paper example shows the final
assembled handoff for policy retrieved / exception-register retrieval failed. IDs are illustrative,
not fixture IDs. The quoted sentence exists in pol-mfa version 1.0; the operation outcomes are
hypothetical. This is not a full schema, a live search result, or an assertion that this single
sentence provides all policy conditions. Final evidence items must retain necessary context,
source snapshot/passage identity, subject attribution and applicability information.

```json
{
  "request_id": "request_1",
  "task_results": [
    {
      "task_id": "t1",
      "evidence_ids": ["e1"],
      "operations": [
        {"operation_id": "op1", "source": "pol-mfa", "outcome": "found"},
        {"operation_id": "op2", "source": "reg-mfa-exceptions", "outcome": "failed", "reason": "Source retrieval failed."}
      ],
      "gaps": [
        {"operation_id": "op2", "reason": "The account's exception record could not be checked."}
      ],
      "observations": [
        {"evidence_ids": ["e1"], "text": "The policy requires a recorded approval. This policy passage alone does not establish approval for the account."}
      ]
    }
  ],
  "evidence": [
    {
      "evidence_id": "e1",
      "source": {"document_id": "pol-mfa", "version": "1.0"},
      "content": "Approval is time-limited and must be recorded in the MFA Exception Register before it is applied."
    }
  ]
}
```

Field names illustrate the logical contract, not an adopted replacement for the unfinished
status taxonomy. Here operation outcome describes one operation, not an aggregate task status.
Code supplies correlation IDs, delivered evidence links/content/provenance and observed operation
outcomes. Code records the shown gap from the failed required operation. The model supplies the
observation and proposes evidence references; code resolves those references. Model-identified
semantic gaps will need separate attribution from code-observed failures in the full shape.

Chat can explain the policy and disclose that account approval remains unchecked. It cannot
claim there was no exception, nor infer legitimacy of the login. Further policy conditions and
event applicability remain necessary before reaching a case-specific interpretation.

Next: finish evidence-item identity/context/applicability fields and distinguish code-observed
gaps from model observations, then settle consistent outcome aggregation. Routine field work
remains delegated; substantive architecture choices remain visible.

### Evidence-item fields: identity, content and applicability

Continued under delegated routine-design authority after the response example. These are
logical field definitions, not an implemented schema or individually approved field names.
IC-05/06/09 govern applicability, preservation and citation identity; IC-10 keeps all payload
text untrusted. Source identity and case applicability must remain distinct.

| Field | Meaning and ownership |
| --- | --- |
| evidence_id | Code-generated handle for the returned item, checked against the retrieval registry. It is not the document ID or a promise of cross-batch persistence. |
| kind | Record, path or passage; determines the payload/source variant. Do not force graph paths or login records into document fields. |
| source | Code-supplied source identity bound to the actual retrieved snapshot. For passages: document ID, declared version when available, passage ID and source/build snapshot reference. Snapshot reference must resolve to preserved provenance; its storage mechanism remains open. |
| content | Actual retrieved passage text, or structured records/path facts from core code. Preserve relevant headings, conditions and context. Do not replace source text with a model-written paraphrase. Distinguish prepared/indexed passage text from a byte-identical original document. |
| attribution | Links to the assigned task and subject references, retained through deduplication. Code validates reference membership; model relevance selection does not authorise new subjects. Related entities returned within a permitted connection task remain linked to the originating subject. |
| source_time | Source-provided publication, effective/expiry or snapshot dates where available, with their distinct meanings and original precision. Do not invent validity dates from publication dates or treat a review date automatically as expiry. Meaningful missing dates carry an explicit reason; inapplicable variant fields are absent. |

Passage ID plus a version label is not automatically an immutable saved-evidence binding.
Read-only grounding: current Chunk has id/text/metadata; schema.py stores chunk_id/content
and a build_record fingerprint. These provide existing identity seams, not proof that the
new response or saved-source resolver has been implemented. Reuse those seams in the build
design; do not add a parallel identity system without a need. The precise variant shapes
for records/paths and the snapshot-reference representation remain to be completed.

Applicability is expressed as research observations linked to evidence, task and subject,
not as an authoritative boolean stored on a document. The same passage can be relevant to
one task/person/time and unsuitable for another. Observations should identify the condition
being considered, supporting evidence and unresolved information. Any suggested applicability
is model judgement; code checks references and explicit dates where possible, while chat
assesses the explanation and the analyst retains the verdict.

Example: an exception entry matches the account and covers the event date, but its stated
reason concerns emergency access during an MFA outage. Those matches do not establish that
an outage occurred or that this sign-in met that condition. Return the entry's actual terms
and the missing event-context evidence. Do not invent outage telemetry or expand scope.

Next: distinguish operation/assembly gaps observed by code from semantic gaps identified by
the model, then define consistent task outcomes. The evidence-limit ruling remains in force.

### Gaps and task outcomes: delegated design refinement

This section refines the provisional execution/evidence-yield cross-product above. Keep
component execution outcomes, delivered evidence references and explicit gaps; do not add a
second mandatory task-wide found/empty/undetermined field that repeats the component records.
Empty/no-match remains an explicit component outcome, never inferred from an empty evidence list.
This is routine design under delegation, not a claim of an external standard or runtime proof.

Two gap variants share task association and a nonblank explanation:

| Gap origin | Basis and fields | Authority |
| --- | --- | --- |
| execution | Code records a failed/unavailable/omitted operation, delivery omission or invalid reference. Include affected operation/evidence reference where one exists and a reason code. References to omitted/rejected items resolve through the execution record, not the delivered evidence list. | Establishes an observed execution or assembly limitation. Only code updates it from subsequent execution/validation. |
| evidence | Research model identifies an unanswered evidence question or an unresolved condition. Include relevant subject references, supporting delivered evidence references when available, and the missing information. Empty evidence references are permitted with an explicit explanation when the necessary source is absent. | A model observation, not proof that the information does not exist. Code validates associations but does not certify this judgement. Chat assesses its significance. |

Model suggestions for resolving either gap are advisory. They cannot expand authorised scope,
claim an external action occurred, or overwrite an observed failure. Later valid evidence may
resolve the outstanding need without erasing the original failed attempt from the trace.

Examples for the same MFA question:

- execution: the register lookup failed, so the required account-entry check is outstanding.
- evidence: the entry is available but applies to emergency recovery, and available records
  do not establish whether that condition held. This can remain after every assigned lookup
  successfully finishes. Do not automatically dispatch a broader investigation to fill it.

#### Component outcomes

Code records found, no_match, failed, unavailable or omitted for each applicable component.
Found requires usable returned material; no_match requires a completed bounded lookup with
no matching results. Failed means attempted but not successfully completed; unavailable means
the necessary source/capability was unavailable before the operation could run; omitted means
not performed, with its reason. Coverage-only/check operations use completed plus their check
result, not a fabricated found/no_match. Streaming/partial operations must preserve completed
scope, usable output and outstanding scope rather than flattening a partial return into no_match.
Detailed attempt/retry representation remains part of execution design.

#### Task-level completion

Code derives a task's completion from the required work and final evidence delivery, not from
the model's confidence or its text saying done. The schema must define the task-specific required
work in trusted code; until that integration exists a status cannot certify procedure coverage.

| Completion | Meaning |
| --- | --- |
| complete | All required operations are accounted for and satisfied, and required selected evidence was delivered and validated. A properly scoped no-match lookup may satisfy an operation. This does not prove exhaustive discovery, semantic relevance or that the investigative question is resolved. |
| partial | Some assigned obligations were satisfied but required work or evidence delivery remains incomplete. Retain useful evidence, completed scopes and all outstanding gaps. |
| not_completed | No assigned obligation was satisfied. Component outcomes explain whether work failed, was unavailable or was omitted; do not collapse those reasons into a generic failure. |

An optional failed follow-up remains visible but does not automatically make a satisfied required
procedure partial. Conversely, required work cannot be relabelled optional by the model. A
successful retry can satisfy an obligation while the failed attempt remains in the trace.
A batch retains separate request/task results; it does not erase an incomplete task because
another succeeded. Request-level aggregation and cancellation/input-rejection lifecycle stay
with execution design rather than being silently squeezed into these final retrieval outcomes.

Thus complete with an evidence gap is valid: the assigned searches finished, but the material
does not settle the condition. Partial with useful evidence is also valid: the policy arrived,
but the required register lookup failed. Chat must inspect both completion and gaps.

Next: consolidate the response fields and validation rules using these definitions, retaining
explicit unresolved execution and source-binding dependencies. No implementation or eval run.

## Comments

- 2026-11-08 — Author confirmed the request/response alignment explanation and requested
  consolidation. Added the current response-design section with exact request/task/subject
  accounting, code-owned assembly and validation, source variants, distinct gap origins and
  task completion. Routine fields remain delegated design rather than separately approved
  values. Earlier response drafts retained as explicitly superseded history. Author-approved
  five-per-search/no-second-five-cap rule incorporated; required-work definitions, snapshot
  adapters and execution policies remain visible dependencies. Documentation only.

- 2026-11-08 — Contract research completed and saved in
  [45-two-agent-contracts-2026-11-08.md](../research/45-two-agent-contracts-2026-11-08.md).
  Perplexity discovery plus direct primary-source checks; Keenable unavailable. Reviewed six
  sources, including a close security planner/executor example and general delegation guidance.
  LangChain current official subagent/structured-output docs checked for input/output transfer
  and schema validation; local lock pins LangChain 1.3.1 and LangGraph 1.2.4, without runtime
  compatibility proof. Research recommendations remain for discussion; no schema adoption,
  application tests, new evaluation gate or orchestration decision.

- 2026-11-08 — Author requested scoped research into established request/response contracts
  for two-agent workflows before continuing the response design, preferring closely related
  use cases but accepting general patterns where direct examples are unavailable. Research
  skill used with one background research agent; primary-source verification and a saved note
  required. Focus: assignment scope, context boundaries, result structure, correlation,
  provenance, incomplete outcomes and validation. No implementation or general orchestration
  research authorised by this checkpoint. Findings inform design; they do not reopen IC-01–11.

- 2026-11-08 — Common **requested_evidence** value rules approved: required non-empty list
  of task objects. Each has `task` from a supported evidence-task catalogue and a non-empty
  `subject_ids` list referencing subjects in the request, plus applicable task-specific fields.
  Missing, null and empty required values are invalid; invented task names are rejected. Code
  validates task compatibility with the request intent and referenced subject types. Unknown
  evidence existence is not invalid input: a valid exception search may return no matching
  evidence, represented in the research response. Exact task catalogue, compatibility mapping
  and task-specific requirements remain open; prior examples do not establish enum values.

- 2026-11-08 — Topic-subject value rules approved: required non-empty code-generated
  subject_id, `type: topic`, and non-empty topic text describing material sought within the
  supported investigation scope. Missing, null, empty and whitespace-only values are invalid.
  Chat agent derives topic from the user request; research agent may construct focused queries.
  Topic is search input, not authority to override tasks/tool restrictions. Code validates
  presence/structure; faithfulness to user intent needs evaluation. Text-length limits remain
  undecided pending actual retrieval needs. No implementation authorised.

- 2026-11-08 — Document-subject value rules approved: required non-empty code-generated
  subject_id, `type: document`, and non-empty document_id resolvable by code to the referenced
  document. Missing, null, empty and not-applicable values are invalid. Identifier comes from
  user input or available evidence; a title/description without an established ID uses topic
  discovery rather than an invented ID. A document identifier alone does not select a version;
  preserved-evidence version/reference handling remains open and must respect IC-09.

- 2026-11-08 — Account-subject value rules approved: required non-empty code-generated
  subject_id, `type: account`, and non-empty account_id resolvable by code to one account.
  Missing, null, empty and not-applicable values are invalid. A display name alone is not an
  account identifier; resolve ambiguity before dispatch. Multiple explicitly selected accounts
  use separate subject entries. Mapping account_id to existing application identifiers remains
  to be verified before implementation; example values are not runtime evidence.

- 2026-11-08 — Activity-subject value rules approved: required non-empty code-generated
  subject_id, `type: activity`, and activity_reference containing `type: alert` or
  `type: login_event` plus a non-empty `id` resolvable by code to that record type. Missing,
  null, empty and not-applicable values are invalid. Resolve identity before dispatch under
  the agreed clarification rule. One alert reference may cover multiple constituent events;
  separately selected individual events use separate subject entries. Actual application
  identifier formats/resolution still need verification before implementation; example IDs
  do not establish runtime support.

- 2026-11-08 — Common **subjects** value rules approved: required non-empty list with entry
  types `activity`, `account`, `document` or `topic`. Null/empty lists are invalid at dispatch.
  Each entry has a code-generated subject_id unique within the request and the required
  type-specific reference or non-empty topic description. Resolve or clarify unidentified
  records before dispatch; never invent identifiers. Code validates structure, local-label
  uniqueness and supplied record references. A topic search does not require a known document
  ID. Fields exclusive to other subject types are absent, not null placeholders. Exact
  per-type required fields and task/type compatibility rules remain to be completed.

- 2026-11-08 — Completed **intent** value rules approved: exactly one required catalogue
  value per dispatched request: `explain_login_activity`, `explain_account_significance`,
  `assess_login_explanations`, `identify_connected_activity`, `recommend_investigation_steps`,
  or `retrieve_reference_evidence`. Null, empty and not-applicable values are invalid. Multiple
  recognised intents produce separate requests, batched under the approved rule. Chat agent
  clarifies ambiguity when it materially changes the work; unsupported requests receive an
  explanation of supported scope, not an invented value or forced match. Code rejects values
  outside the catalogue; classification correctness requires evaluation rather than merely
  schema validation. No implementation or evaluation execution authorised.

- 2026-11-08 — Completed **request_id** value rules approved: always required in the
  dispatched research request; code supplies a non-empty unique identifier before dispatch.
  Missing, null, empty, unknown and not-applicable values are invalid. The model does not
  supply a placeholder or missing-value reason for this code-owned field. Do not dispatch
  without a valid identifier or accept a response linked to an unrecognised request. Existing
  stable-during-execution/new-assignment-new-ID rules remain. Exact format and implementation
  remain open. Continue completing allowed values, requiredness, missing/not-applicable
  handling, relationships and validation for existing fields before adding more fields.

- 2026-11-08 — **applicability_time explicit_date** approved: use `mode: explicit_date`,
  `date` and `timezone` on the relevant evidence task when the user supplies a calendar date
  without identifying a login. Task subject_ids identify the account or other applicable
  subject. Time zone comes from established context or clarification, not an assumed example
  value. Code resolves the calendar-day boundaries; research agent retrieves relevant approval
  history/conditions; chat agent explains applicability and uncertainty. Do not silently turn
  the date into a single midnight instant. Preserve changes within the day, and do not invent
  time precision absent from source records. Exact validation and implementation remain open.
  Author requested a pause for a question after recording this ruling.

- 2026-11-08 — **applicability_time** approved on the evidence task requiring a temporal
  applicability check. Initial mode is `from_activity` with `subject_ids` referencing activity
  subjects. Code derives relevant event timestamps; research agent retrieves approval dates,
  conditions and relevant history; chat agent weighs whether that evidence supports the
  explanation. This is distinct from the surrounding-activity collection window. For alerts
  containing several logins, preserve relevant event times rather than silently applying the
  alert start to every event. Applicability time guides retrieval but must not automatically
  exclude older documents that could establish validity at the event time. Exact multi-event
  representation, explicit user-date modes and task vocabulary remain open; no implementation
  authorised.

- 2026-11-08 — Relative-date rule approved: reuse an established conversation reference
  date/time zone; if the reference is materially unclear, chat agent asks one clarification
  rather than silently selecting wall-clock time or a dataset date. Code resolves relative
  expressions, and the research-agent request carries explicit timestamps rather than an
  unresolved phrase. Reuse established context without repetitive clarification and disclose
  the actual examined period in the answer. “Yesterday” means the preceding calendar day in
  the established zone; “last 24 hours” means a rolling interval and needs an appropriate
  reference instant. Existing loader rejects relative strings and documents dataset capture
  date rather than computer clock as its notion of today. Verify how the dataset reference
  date is represented before automating it; exact resolution mechanism, context persistence
  and implementation remain open. No change to existing parser behaviour implemented.

- 2026-11-08 — **activity_window explicit_range** approved following clarification:
  fields are `mode: explicit_range`, `subject_ids`, `start` and `end`. Each subject_id is a
  local reference to a subjects entry, not the underlying account/record identifier. Chat
  agent recognises the user-requested period and clarifies materially ambiguous dates/time
  zones; code validates dates/order and enforces applicable scope approval; research agent
  retrieves within the resolved period and reports coverage limits. Include start, exclude
  end. A user's explicit request for additional history supplies that approval without a
  redundant confirmation; an agent-proposed expansion still requires analyst approval.
  activity_window is contract data, not an agent-facing tool. Validation/default derivation
  may be ordinary code; login-retrieval tools belong to the research agent. Exact tool
  interfaces, relative-date interpretation and validation mechanics remain open. No
  implementation authorised.

- 2026-11-07 — Default **activity_window** representation approved: `mode:
  default_from_activity` with `subject_ids` referencing the activity subjects whose windows
  apply. Code resolves each referenced alert/login and derives the approved window: alert
  start minus 24 hours through alert end plus 24 hours, or single login timestamp ±24 hours.
  Research agent receives resolved dates for execution; chat agent does not calculate or
  duplicate derivable dates. Report actual data-coverage gaps. Applies to evidence tasks
  needing surrounding activity; trigger-only retrieval does not automatically expand to
  surrounding records. Exact placement and handling of multiple derived windows remain open;
  do not infer a merged request-wide window. User-specified periods and analyst-approved
  expansions require separate rules; no other modes or implementation approved.

- 2026-11-07 — Date-purpose separation approved: distinguish the **activity window** used
  to collect login records from the **applicability date(s)** used to assess whether a policy
  or exception applied to the activity. An exception need not cover the entire surrounding
  collection window merely because those records are retrieved. Where possible, code derives
  dates from referenced activity rather than requiring chat-agent calculations. Multiple
  login events may require distinct applicability dates; do not silently replace them with
  one request-wide date. Exact field names, placement, derivation rules and missing-date
  handling remain open. Existing approved investigation windows and analyst-controlled
  expansion remain unchanged; no implementation authorised.

- 2026-11-07 — Read-only applicability check before proposing application constraints:
  default logins.csv has timestamp_utc, username, source_ip, country, outcome, failure_reason,
  user_agent, device_id and mfa_result; no target-application field. loader.py enforces the
  expected column set. The MFA policy/register describe account approval, reasons and dates,
  not a structured per-application exception key. The earlier email-versus-payroll example
  was illustrative, not current dataset evidence. Do not infer target application from user_agent
  or permissions. Dedicated application constraints remain unapproved; recommendation is to
  avoid adding that field on the strength of this example. No schema/data changes made.

- 2026-11-07 — Task-to-subject links approved: each entry in `subjects` receives a local
  **subject_id**, assigned by code. Each `requested_evidence` entry becomes an object with
  **task** and **subject_ids**, explicitly identifying the subjects that task applies to.
  A subject's real record identifier (such as account_id) remains distinct from its local
  request label. Chat agent chooses the semantic task/subject associations; code assigns
  labels during final request construction and rejects references to absent subjects. Do not
  require the model to guess code-generated labels. Exact construction mechanics, task-name
  vocabulary and validation remain open. Examples illustrated owner retrieval for two
  relevant accounts with privilege retrieval for only one; tasks do not automatically apply
  to every subject. No implementation authorised.

- 2026-11-07 — **subjects** list approved, replacing singular `subject`: each request has
  one or more typed subject entries, retaining the approved activity/account/document/topic
  structures. One intent may concern several subjects when each is relevant to the assigned
  login-investigation task; preserve which evidence belongs to each subject. This does not
  introduce standalone access review, arbitrary account comparisons or broad asset exploration.
  Multiple accounts relevant to the same suspicious activity provide an in-scope example.
  Exact task-to-subject mapping, comparison instructions, collection limits and validation
  remain open. Earlier singular examples describe entry shapes, not the final outer field.

- 2026-11-07 — Document/topic subject types approved: a known document uses
  `subject.type: document` with `document_id`; a document-discovery request uses
  `subject.type: topic` with a `topic` description. Known identifiers come from prior evidence
  or user input and are validated by code, never invented from a title. Supported known-document
  cases include follow-up inspection of a previously retrieved/cited document and an explicitly
  supplied identifier; their frequency has not been measured. Topic text is bounded search
  input, not permission to change the assignment. A research agent finding and inspecting a
  document within an existing assignment does not require a new chat-agent request. Fields
  belonging to other subject types are omitted. Example evidence-task names were illustrative;
  content-size limits, response amounts and full schema validation remain open.

- 2026-11-07 — Author approved a separate T45 sub-discussion for agent prompt examples.
  Contract examples explain valid structures; chat-agent and research-agent prompt examples
  teach their respective responsibilities and require deliberate selection and evaluation.
  A shared example may serve both purposes after review, but documentation examples are not
  automatically prompt content or fields in research requests. No prompt examples selected
  or prompt implementation authorised. Continue contract design first.

- 2026-11-07 — Typed **subject** structure approved through activity/account examples:
  `subject` identifies what the request concerns. An activity subject has `type: activity`
  and contains the already-approved `activity_reference` with record `type` and `id`.
  An account subject has `type: account` and `account_id`. This places `activity_reference`
  inside `subject`, preserving its meaning and validation rules. Fields belonging only to
  other subject types are absent, not empty fields requiring reasons: an account-only subject
  does not include an empty `activity_reference`. Missing required information still needs
  explicit handling. JSON examples illustrated the structure; exact intent/evidence-task
  spellings were not approved by those examples. Document/topic subjects, multiple-subject
  handling and full validation/missing-input rules remain open. No implementation authorised.

- 2026-11-07 — **request_id** approved: code generates a unique identifier when each request
  is created, including separate requests with the same intent. Every returned result includes
  its originating identifier. Tool retries and follow-up searches within that request retain
  it; a new assignment from the chat agent receives a new identifier. Code validates returned
  identifiers against submitted requests; models do not invent them. Identifier format remains
  an implementation detail to settle. This links results to requests but does not certify that
  the evidence task was fulfilled. Exact response schema and implementation remain open.

- 2026-11-07 — Batching rule approved: chat agent sends evidence requests known together
  as a batch, retaining **one intent per request**. Research agent coordinates tool execution
  order, retrieves shared evidence once where suitable, and examines its usefulness for each
  assigned request. Return a distinct result and status for each request, with references to
  shared evidence. Batching does not require simultaneous tool calls. If a subsequent request
  depends on the chat agent interpreting earlier results, return those results first and let
  the chat agent determine the next request. Intent selection and final interpretation remain
  with the chat agent; tool coordination and within-batch evidence reuse remain with the
  research agent. Cross-batch reuse/persistence is undecided; `available_evidence_refs` remains
  a proposal, not an approved field. Exact batch/result schemas and implementation remain open.

- 2026-11-07 — Request grouping approved: **one intent per research request**, with multiple
  evidence tasks allowed. Chat agent combines returned evidence into the user-facing answer;
  reuse available shared evidence rather than automatically retrieving it again. This settles
  singular intent context per request, not one tool call per request, a fresh research-agent
  instance per request, or sequential execution. Batching, scheduling, dependency handling and
  evidence-reuse mechanics remain open. Author chose to keep one chat agent for now; potential
  additional/intent-specialised chat agents are deferred for possible future evaluation-led
  reconsideration, not current scope or implementation approval.

- 2026-11-07 — Intent context approved for the request contract: include the classified
  **intent**, using the agreed supported-intent catalogue rather than free text. Intent tells
  the research agent what user need the evidence supports; `requested_evidence` states what
  it must obtain. Intent context does not authorise scope expansion or transfer the final
  investigative assessment from the chat agent. Whether a request carries one intent or
  several, and the resulting exact field structure, remain open with the batching decision.

- 2026-11-07 — Second request-contract field approved: **requested_evidence**, an explicit
  list of evidence tasks selected from the agreed intent-to-evidence mappings. Chat agent
  specifies needed evidence; research agent selects permitted tools and examines their results.
  Define supported task names rather than unrestricted prose; exact names and schema remain
  open. For Explain login activity, a success-count question requests relevant triggering
  records/counts; a surrounding-activity explanation requests triggering records, relevant
  surrounding activity and coverage. Collection failures and limitations must always be
  reported even if not explicitly requested. No new tool, execution limit or implementation
  authorised. Author requested a pause for a question before discussing the next field.

- 2026-11-07 — Activity-reference ambiguity rule approved: chat agent uses an already
  selected or clearly identified alert/login record. If the reference remains ambiguous,
  ask the analyst to identify the activity before sending that activity research request.
  Never guess a record identifier. This resolves the previously reconsidered starting-record
  ambiguity boundary for these assignments; it does not assign investigative evidence
  collection to the chat agent or require an activity reference for general document lookups.

- 2026-11-07 — First request-contract field approved: **activity_reference**, containing
  `type` (alert or login event) and `id` (the specific record identifier). For an assignment
  to explain activity around an identified alert/login, the chat agent supplies this reference,
  code verifies it exists, and the research agent uses it to retrieve evidence. Code derives
  the approved investigation window from the record. This is not a mandatory field for general
  document lookups. “Starting record” was replaced with the more descriptive field name.
  Exact enum spellings and handling of missing/ambiguous references remain open; no code or
  complete schema approved.

- 2026-11-07 — Author requested global Codex installation of `roast-technical` from the local
  Claude skill and an explicit pre-implementation checkpoint in this ticket. Run after the
  proposed design is concrete, before building it; no council review requested at this stage.

- 2026-11-07 — Evidence-task mapping approved for **Retrieve reference evidence**: find
  documents/passages matching the requested subject and supplied account/system/date
  constraints; retrieve conditions, exclusions or neighbouring context when needed to read
  the material correctly; preserve checkable source references, available date/version
  information and retrieval limitations. Return relevant candidates with distinguishing
  details when evidence does not justify choosing one. Chat agent presents material and
  ambiguity; assessing its explanation of an incident remains a separate intent. Follow-up
  retrieval stays bounded. All six proposed intents now have approved evidence-task mappings;
  exact request/response fields, classification validation and execution limits remain open.
  These approvals do not certify implementation or close T45's retrieval gate.

- 2026-11-07 — Evidence-task mapping approved for **Recommend next investigation steps**:
  obtain only missing case evidence relevant to the specific unanswered question, reusing
  available records and previous check results; retrieve applicable approved guidance with
  references and conditions describing checks that could resolve that uncertainty. Chat agent
  forms the recommendation and explains its purpose, distinguishing app-supported checks from
  external analyst actions. Research agent does not automatically execute the recommended
  next check; asking for guidance is not execution authorisation. Missing applicable guidance
  must be explicit. Guidance-source approval, exact fields/tools and implementation remain open.

- 2026-11-07 — Evidence-task mapping approved for **Identify directly connected activity**:
  establish relevant source/device identifiers from the activity, reusing available evidence;
  retrieve other-account login activity from the involved source or recorded other-account
  use of the involved device, as the question requires, within the approved window; return
  supporting account identifiers, timestamps, recorded outcomes where available, and coverage
  gaps/failed checks. Source and device searches are not automatically both required. Code
  establishes recorded links/counts; research agent retrieves and examines results; chat agent
  explains relevance without claiming common control or compromise. Shared infrastructure can
  connect unrelated users. Exact fields/tools and implementation remain open.

- 2026-11-07 — Evidence-task mapping approved for **Assess explanations for login activity**:
  obtain relevant facts the explanation must account for, reusing available evidence; retrieve
  supporting and competing evidence; obtain person/system/time/condition details needed to
  assess applicability. For exception questions this includes relevant login facts, applicable
  policy and the actual exception record, including qualifications or contradictions. For
  attack questions, include relevant threat guidance and evidence of legitimate explanations
  rather than confirmation-only searches. Research agent examines retrieval quality and makes
  bounded follow-ups; chat agent weighs the explanation. General policy does not establish an
  actual exception, and an exception may explain only part of the activity. Exact fields/tools
  and implementation remain open.

- 2026-11-07 — Evidence-task mapping approved for **Explain account significance**:
  retrieve recorded owner, department and role where available; retrieve group memberships,
  privileges and sensitive permissions relevant to the question; return supporting records
  or permission paths and the limits of what they establish at the event time. Owner-only
  questions may need only identity/context; sensitive-access questions need relevant access
  evidence and its support. Do not automatically collect every reachable asset. Research
  agent obtains evidence; chat agent explains significance. Permissions do not establish
  exercised access, role does not establish normal behaviour, and current permissions may
  not establish historical permissions. Exact fields/tools and implementation remain open.

- 2026-11-07 — Evidence-task mapping approved for **Explain login activity**: retrieve the
  triggering login records with recorded outcomes, times, accounts, sources and devices;
  retrieve relevant surrounding successes/failures and source/device changes within the
  approved window when the question calls for them; establish actual record coverage and
  collection limitations, including missing data and failed checks. Code supplies counts and
  event sequence. Research agent calls tools, examines results and makes permitted follow-ups;
  chat agent explains the evidence. These are evidence obligations, not a prescribed number
  of tool calls. Narrow factual requests use only necessary evidence, rather than automatically
  expanding to surrounding activity. Failed checks remain distinct from successful empty
  results, and missing later records do not prove no later activity. Exact fields/tools and
  implementation remain open.

- 2026-11-07 — Sixth catalogue intent approved: **Retrieve reference evidence**. Covers
  finding or inspecting corpus documents/passages relevant to a stated subject, such as an
  account's authentication exception or the applicable authentication policy. Return matching
  material, checkable source references, enough context to understand its scope, and retrieval
  limitations. Do not automatically assess whether it explains an incident. Activity/account
  lookups remain under their respective intents. This fills the direct-document-lookup gap
  identified while defining the third intent; it is not a new standalone T52 objective or
  approval for additional sources. First catalogue now has six agreed intents; classification
  examples, required inputs, request/response schemas and implementation remain open.

- 2026-11-07 — Fifth catalogue intent approved with narrowed information needs:
  **Recommend next investigation steps**, grounded in T52 E06/IC-07. Connect a specific
  unanswered question to an evidence-gathering check that could resolve it. Its basis is that
  question, relevant evidence, any previous attempt to answer it, and applicable approved
  investigation guidance. Do not require a broad case summary or all prior checks. Reuse
  available evidence rather than automatically retrieving it again. Research agent retrieves
  needed evidence/guidance; chat agent forms the recommendation and explains the uncertainty
  it addresses. Distinguish app-supported checks from external analyst actions; recommendations
  do not imply execution. Broad response planning and automated containment remain deferred.
  Honest limitation reporting remains mandatory across intents, independent of a request for
  recommendations. Guidance-source selection/approval and exact contract fields remain open.

- 2026-11-07 — Fourth catalogue intent approved: **Identify directly connected activity**,
  grounded in T52 E05 and the definitive scope ruling/IC-04. Covers other accounts targeted
  by the suspicious source and accounts using devices involved in the activity, supported by
  dated login/device-use evidence within the approved window. Connections are investigative
  leads, not proof of compromise or common control. Does not authorise exploring every device
  ever used by the account, restoring removed shared-address exposure, or standalone full
  asset inventory. May combine with Explain login activity. Exact contract fields and
  implementation remain open.

- 2026-11-07 — Third catalogue intent approved: **Assess explanations for login activity**,
  grounded in T52 E03/IC-05. Covers assessing the most supported explanation or testing a
  specified explanation using activity facts, relevant account context, supporting/competing
  evidence and person/time/system/activity applicability. Travel, authentication exceptions
  and approved maintenance are candidate explanations within this intent, not separate intents
  merely because the explanation differs. Research agent gathers and examines requested
  evidence; chat agent weighs it and communicates the assessment with uncertainty; analyst
  retains the verdict. Partial explanations must not erase unrelated concerning activity.
  Direct requests to retrieve a record are distinct from assessing its explanatory value;
  their catalogue treatment remains open. Exact fields and implementation remain open.

- 2026-11-07 — Second catalogue intent approved: **Explain account significance**, grounded
  in T52 E02/IC-04. Covers recorded owner, department, relevant role, group memberships and
  sensitive permissions to explain why an account matters and its bounded potential impact.
  Evidence collection follows the specific question; an owner lookup does not automatically
  require exploring all permissions. Permissions do not prove observed access or compromise,
  current permissions do not establish event-time permissions, and unavailable role information
  must remain explicit. May combine with Explain login activity. Exact contract fields remain
  open; no implementation authorised.

- 2026-11-07 — Intent-catalogue planning direction and first intent approved: the chat agent
  classifies each user request against an explicit supported-intent catalogue, selecting one
  or several intents rather than inventing a free-form investigation objective. Derive the
  catalogue from T52, without assuming one objective equals one intent. Each intent will map
  to required inputs and evidence needs; ambiguous/unsupported-request handling remains open.
  Focused evidence requests are the research-agent work units. Do not classify every user
  request as either a narrow lookup or a full investigation: a bounded question can need
  several evidence requests. Explicit standard procedures retain their required checks.
  Batching and request/response fields remain open.

  First agreed intent: **Explain login activity**, grounded in E01/IC-03. It covers explaining
  the identified activity and relevant surrounding context using login records, successes
  and failures, event sequence, source/device changes and explicit coverage gaps. Attack
  assessment and exception applicability require additional intents to be defined. The
  specific question determines necessary collection; recognising this intent alone does not
  mandate the broadest investigation. Approved window rules and mandatory checks for an
  explicitly invoked procedure remain in force. Precise handling of narrow factual questions
  and catalogue granularity still need examples before schema/spec finalisation.
  No application implementation or acceptance-gate change authorised.

- 2026-11-07 — Author-approved delegated-agent role clarification, superseding overlapping
  planning proposals above this discussion: the purpose of the proposed two-agent split is
  to separate conversation context from intermediate tool-working context. The chat agent
  understands the user's request, asks the user for missing context when needed, decides what
  evidence to request, and interprets the returned evidence for the final answer. The research
  agent receives that bounded request, selects and runs permitted tools, examines results for
  relevance, failures and gaps, makes bounded follow-up calls where useful, and returns a
  contracted evidence response. Its judgement concerns tool execution and result quality;
  it does not independently redefine user intent or own the overall investigative assessment.
  The analyst retains the verdict; code retains facts, scope enforcement and required checks.
  The author's “one or two” follow-ups describes bounded work, not an adopted numeric limit.
  Request/response schemas, tool permissions and execution limits remain to be defined.
  No application implementation is authorised by this role ruling.

  Evidence loss at the handoff is an engineering risk to address through suitable practices
  and verification, not a reason to blur the roles. Structured returns, checkable references,
  supporting/competing evidence preservation and explicit incomplete states are design
  directions consistent with IC-05/06/07/09; exact mechanisms and tests remain open. No claim
  that these eliminate evidence loss or that the two-agent design has been measured.

  Reconciliation: retain the approved ability to gather activity evidence through tools and
  code ownership of counts/windows/checks. The earlier E01 starting-record ruling is subject
  to reconsideration during contract design; do not treat it as requiring the chat agent to
  perform investigative collection before delegation. The proposals to pass the original
  question plus a rewritten objective, trace every derived question's origin, or make the
  research agent a second interpreter of intent were not approved and are not requirements.
  Resume from this clarified role split and T52 objectives, not those overlapping proposals.

- 2026-11-07 — Request-contract planning, E01 starting-record ruling: author approved
  requiring the chat agent to establish an unambiguous alert or login reference before
  delegating an activity investigation. It may use a selected record or look up candidates;
  if ambiguity remains, ask the analyst to choose. Code verifies the reference and derives
  the already-approved investigation window from that record. This requirement applies to
  activity-investigation assignments, not general document questions. Exact field names and
  request-type definitions remain open; no implementation authorised by this ruling.

- 2026-11-07 — Request-contract planning, E01 responsibility ruling: author approved the
  recommendation that the proposed research agent may gather login activity evidence through
  tools, alongside document evidence. The chat agent identifies the alert or login and the
  assignment's purpose; the research agent requests evidence, examines results and identifies
  gaps; code resolves records, enforces the approved investigation window, calculates counts
  and sequence, and reports data coverage. The chat agent explains the combined findings.
  This inherits E01/IC-03 and P-01; required full-investigation checks remain enforced in code,
  and additional history remains analyst-controlled. Integrate with the existing code-built
  package rather than duplicating its collection logic. This settles one responsibility
  boundary in the proposed delegated-agent design, not its complete architecture or
  implementation. Exact tools, request/response fields and remaining boundaries are open.
  Author's planning direction: derive structured request and response contracts from T52
  objectives, one objective at a time; account explicitly for missing/inapplicable inputs and
  unsuccessful/incomplete evidence collection, with reasons. Exact statuses and validation
  rules are still proposals, not adopted field definitions.

- 2026-11-07 — Pre-handoff storage clarification: author understands the eight corpus kinds
  (policy, runbook, register, record, meeting, email, guidance, attack) share `chunks`, with
  separate chunk rows/vectors and typed metadata. T02 d7 and T03 d3/d6 approved that baseline;
  no dedicated one-table-versus-per-kind comparison was established by the inspected history.
  Shared storage can support filtered searches and specialised retrieval; table separation
  does not itself preserve evidence through merging/caps. Author accepted revisiting layout
  when retrieval, scale, access, embedding-space or maintenance needs justify it. This is
  clarification, not a migration or architecture change. Any future migration needs preserved
  evidence IDs/citations, filter/permission checks and retrieval comparison before switching;
  no migration has been designed or tested. Start the fresh session with unresolved retrieval
  mechanisms under the contract, not a storage redesign or repeated T52 approvals.

- 2026-11-07 — Author approved a durable investigator contract after identifying that the
  briefing reopened T52 requirements. Added `docs/investigator-contract.md`, stable IDs and
  decision sources; linked it from both session instruction files and the spec. This ticket
  now references applicable IDs. No new behavioural ruling or acceptance claim.

- 2026-11-07 — Author challenged the post-research briefing for reopening recent decisions.
  Checked T52's accepted E01/E03/E06–E10 and downstream reconciliation, T54's fixed-evidence
  screening/closure and T56's closure. Most proposed practices were already approved in T52.
  Corrected the research note: inherit those requirements; discuss only unresolved retrieval
  mechanisms, tool boundaries, exact budgets and guidance sources. No reapproval required
  for competing evidence, applicability, preservation, incomplete states or evaluation separation.

- 2026-11-07 — Initial Perplexity research and selected primary-source checks complete:
  [research note](../research/45-security-investigation-initial-2026-11-07.md). Security-specific
  evidence supports separating discovery, preservation and interpretation; it does not select
  agent/tool count or retrieval boundaries. Eight primary sources checked to the depth stated;
  benchmark reporting limits are explicit. No architecture, ingestion or new evaluation gate
  adopted. All six design rulings and source approval remain open. Keenable is unavailable;
  no execution claimed. B-162 records a corrected research-request orchestration error.

- 2026-11-07 — Author approved initial security-investigation-focused research using
  Perplexity research, then design discussion. Customer-support RAG is not the governing
  use case. Prioritise defensive investigations combining observed events, account/device
  context, threat guidance and internal policies/exceptions; competing explanations,
  applicability, uncertainty and evidence preservation. Consider future expansion of the
  investigator's role without expanding phase 0/1 implementation scope. Verify material
  claims against primary sources and distinguish measured results from proposals/vendor
  claims. Perplexity is the requested research engine; use primary-source checks to verify
  it. No architecture, sources for ingestion, new benchmark or application changes approved.
  The author also approved T45 before T25 to avoid implementing an unsettled tool boundary.
- 2026-11-07 — Model gate: author explicitly confirmed proceeding with the selected
  strongest model through the model-confirmation question. No exact model identifier was
  supplied by the author; do not infer one. Initial research authorised by “ok go ahead”.
  Research brief: [security investigation research brief](../research/45-security-investigation-brief-2026-11-07.md).

- 2026-10-29 — Author: open this as its own ticket, a decision ticket that blocks T26. T24 and
  T25 proceed meanwhile. The chat path matters because the analyst can ask anything; a user
  guide cannot guarantee how questions are asked.

- 2026-11-01 — Author: wait for [T52](52-agent-objectives-and-reliability-review.md), the
  phase 0 and 1 objectives and reliability review. Carry its approved requirements into this
  ticket before work starts; existing requirements remain in force until explicitly amended.

- 2026-11-02 — Author approved T45 owning guidance-source selection and presentation for
  review. Source approval precedes use; T26 owns integration. This adds a source-selection
  decision to this ticket without settling its five existing retrieval decisions.

- 2026-11-03 — Author requested an explicit design review of shared versus subject-specific
  RAG retrieval after discussing MITRE and HR examples. Added decision 6 and its acceptance
  criterion. Distinguish internal specialised retrieval from separate agent tools and structured
  account lookup from document search. Neither design is selected; the shared tool remains
  the current spec baseline pending author ruling. Resolve when T45 starts, alongside its
  existing decisions and guidance-source selection. Documentation only; no implementation,
  gold/threshold change or T54 change authorised.

- 2026-11-08 — Author approved retrieve_triggering_activity and delegated remaining routine
  contract values/details without per-field approval stops. Consolidated the request design
  above: preserved individually approved rules and completed task catalogue/compatibility,
  per-task timing placement, explicit missing/inapplicable states, task correlation and bounded
  focus semantics under that delegation. Read-only source checks distinguish existing identity,
  time and retrieval mechanisms from planned adapters. No response-schema completion, new
  numerical budgets, source adoption, runtime proof or application build claimed. Next substantive
  work is the response/evidence contract; preserve separate prompt-example discussion and
  pre-implementation roast review. Historical comments retained.


## Answer — design and handoff complete, 8 November 2026

The author approved the implementation breakdown, authorised publication, then requested T45
closure. The ticket is resolved on its design evidence and assigned implementation/proof owners.
IC-01–11 and P-01–03 remain inherited; approval is not runtime proof.

### Six original decisions

| Decision | Final ruling and evidence | Implementation/proof owner |
| --- | --- | --- |
| 1. What K04 measures | The approved Retrieval acceptance paths section retains original questions/gold and measures analyst-question and applicable same-case code-built baseline paths separately. Candidate admission and actual delivery both matter. Raw corpus-only top 20 is diagnostic; historical failures remain. | T58/T25 stage records; T26 baseline; T59/T60 delivery; T29 acceptance, T40/T41 later coverage/comparisons |
| 2. Chat decomposition | Chat interprets intent, clarifies material ambiguity and constructs focused requests under explicit full/narrow mode. Code resolves scope/IDs; only isolated research receives investigative tools. Six intents and eleven tasks remain the contract. | T57 shared contracts, T59 worker and research examples, T60 parent/chat examples; T29 classification/interpretation evaluation |
| 3. Package searches | One core procedure supplies mandatory obligations independently of model-selected tasks. Code-built clearing/aggravating searches derive from resolved case facts; research supplements them without hiding baseline misses. | T26 procedure/package, T60 activation, T28 report gate; T29 separate baseline proof |
| 4. Keeping evidence | Up to 20 corpus plus 20 additional unique graph candidates, common reranking, five results per search and no second combined-five cap. Preserve source-bound original content, conditions, competing evidence and attribution. Controlled oversized-passage splitting scores all pieces and retains the original parent. Record candidate, ranked, retained and delivered stages separately. | T58 admission/ranking/input guards; T25 reader; T26/T59 assembly; T60 actual chat delivery/reopen; T29 gates |
| 5. Keyword matching | Keep current PostgreSQL keyword search for focused queries initially. Resolve acceptance failures before phase-0 acceptance. Matching and scoring are distinct; no blanket OR change or BM25 adoption. | T58 initial behaviour, T29 acceptance, T41 measured comparison |
| 6. Retrieval boundaries | Four model-visible documentary purposes share internals and one exact-reference reader. Graph-linked discovery stays internal. Purpose eligibility and approved guidance versions/sections are enforced in code; no arbitrary graph/database queries or general web retrieval. | T25 interfaces/catalogue/reader; T58 shared pipeline; T59 restricted exposure; T29/T40 subject/cross-subject proof |

### Closure evidence

| Criterion group | Evidence |
| --- | --- |
| Model gate | Dated 7 November comment records the author's strongest-model confirmation. Exact model identifier was not supplied and is not inferred. |
| Research | [Initial security research](../research/45-security-investigation-initial-2026-11-07.md), [overflow research](../research/45-reranking-input-overflow-2026-11-08.md) and [orchestration research](../research/45-langgraph-orchestration-2026-11-08.md). Perplexity and primary-source checks recorded; Keenable unavailable. |
| Architecture and single review | Approved thin LangGraph parent and isolated create_agent workers; [completed council](../reviews/45-architecture-council-2026-11-08.md) returned GO with no demonstrated P0/P1 blocker. Lower observations retained in AUD-086; no second council. |
| E01–E06 mapping and partial explanations | Full-procedure obligation mapping, eleven-task catalogue and purpose mapping in this ticket. T57 covers activity/account/connection facts; T25 documentary applicability; T26/T59 evidence assembly; T29/T40 test interpretation, including travel that does not explain separate attack activity. |
| Evidence preservation and limits | Consolidated response contract, shared result guarantees, ranking/admission and controlled-splitting sections. T58/T26/T59/T60 explicitly own stage receipts, merge/cap losses, original content and delivery; T29 proves the integrated paths. |
| Guidance and prompt selection | Approved three-runbook source/version/section table and extensible catalogue; approved role-specific teaching cases. T25 implements catalogue restrictions, T26 integrates guidance, T59/T60 write examples; existing evaluations assess relevance and behaviour. |
| Ticket ownership and dependencies | Author-approved [spec ownership table](../spec.md#approved-t45-implementation-ownership--8-november-2026), four published T57–T60 tickets and revised T25/T26/T28. T27/T29/T36/T40/T41 consumer handoffs recorded. Dependency/link/whitespace checks passed at publication. |
| Spec and gates | Approved path-specific gate, keyword, source, mode, orchestration and prompt rulings are retained in the spec and its decision records. Seven-slice approval is in the decisions log. No original gold/threshold change beyond the explicit candidate-stage ruling. |
| T26 and audit reconciliation | T26 now owns shared procedure and code-built baseline with step evidence. AUD-062 records path-specific closure requirements and implementation owners; it remains open. AUD-086 ownership is assigned but runtime observations remain open. |

### Remaining implementation responsibilities

T57 → T58 → T25 supplies evidence capabilities. T26 and T59 then proceed independently;
T60 joins them with T27, followed by T28 and the existing T44/T29 phase-0 gate.
T55 remains the expanded-data/device-edge owner; T36 retains the later step-stack screen.
T30/T39/T40/T41/T42 retain their existing evaluation/acceptance roles; T31 retains tracing.

Routine numeric budgets, retries, source adapters, catalogue storage, provider-compatible size
measurement and runtime policies belong to the published owners. They are not unrecorded
architecture decisions or grounds for another numeric-limit approval tour. Material scope,
evidence-guarantee or acceptance changes still require author ruling.

T45 does not claim retrieval success, faithful interpretation, saved-case compatibility or audit
closure. Those require the build/evaluation evidence specified in their owner tickets. No code,
source-data write, inference, rebuild, commit or push occurred during this closeout.
