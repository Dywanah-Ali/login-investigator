# T45: scoped LangGraph orchestration research brief

8 November 2026. Tier 3, design research only. The author authorised this pass after
stopping the fine-detail approval loop. No application code, inference, migration or topology
adoption. Findings inform a consolidated architecture recommendation before the agreed review.

## Approved workflow to support

- Chat clarifies intent, constructs bounded assignments and interprets returned evidence.
  Research selects permitted read-only retrieval operations, examines evidence and makes
  bounded follow-ups within the assignment. Code owns facts, identity, scope, required checks
  and completion receipts. The analyst retains the verdict. IC-01–11 and P-01–03 stand.
- A full investigation must satisfy code-owned required checks; a narrow question stays narrow.
  Models cannot waive checks or approve expanded history. Known independent assignments may
  run together; interpretation-dependent assignments wait for chat reasoning.
- One intent per request; code-assigned request/task/subject IDs. Retain original scope and
  source snapshot. One final task result per assigned task with every subject accounted for.
  Distinguish complete, partial and not_completed from evidence relevance or a resolved case.
- Research alone receives investigative retrieval tools. Shared core stays independent of
  screen/framework. Code assembles authentic evidence around model selections/observations.
  Failed/unavailable/omitted work remains visible. No-match is not inferred from an empty packet.
- Research calls are bounded; numeric budgets belong to implementation. A hard stop must not
  erase completed work or outstanding obligations. Invalid references/outputs cannot become
  successful evidence. Tool output and documents remain untrusted data.
- Preserve important supporting/competing text through delivery and saved answers. No second
  five-passage combined cap. Graph/corpus discovery and ranking policies are settled in T45.
  Saving a checkpoint is not automatically immutable evidence preservation.
- Persistent conversations already exist. Cross-batch research memory/evidence reuse has not
  been adopted. Research must not inherit unrestricted chat history or silently current data.

## Questions for this pass

1. Compare a thin explicit workflow graph containing code stages and agent calls with a
   supervisor/tool-only approach. Where does each enforce required checks, handoff validation
   and return of useful partial work? Do not assume a second supervisor model is necessary.
2. What state belongs to the conversation, one investigation/request, or an isolated research
   invocation? How do documented subgraph/checkpointer modes affect parallel calls and memory?
3. How can code dispatch independent assignments, merge by stable identity and continue after
   an isolated failure without losing or falsely completing sibling results?
4. What does durable execution actually replay? Distinguish retries, resumable interruption,
   cancellation and a new chat turn. Identify evidence-snapshot and duplicate-call risks.
5. Which mechanisms are framework-supported and which remain application responsibilities?
   Include required-check enforcement, semantic validation, scope approval and saved evidence.
6. Recommend the smallest useful topology and integration boundary. Note compatibility with
   installed/locked versions and existing chat persistence; do not design every field/node.

## Evidence and output

Use Perplexity for discovery and official LangChain/LangGraph docs/source for claims.
Keenable is not present in the current tool catalogue; disclose that limitation. Check local
versions without installing/upgrading dependencies. Current lock: LangChain 1.3.1, LangGraph
1.2.4, checkpoint 4.2.0, checkpoint-sqlite 3.1.1. Confirm installed versions separately.
Current documentation is not proof of installed runtime compatibility or application correctness.

Save one focused findings note with links, supported mechanisms, application inferences,
version caveats and a small list of material architecture choices. Do not expand into provider
selection, new infrastructure, generic framework surveys or an experiment programme.

## Subsequent work, not prerequisites for this research

Prompt examples; approved E06 practice-source set; original K04 gate/path and keyword-strategy
dispositions; precise full-procedure task/search coverage; T25/T26 ownership reconciliation;
numeric scan/token/retry limits and source adapters. These remain named obligations before
their relevant build/acceptance stages, not claims of completion or silently waived gates.

## Local grounding checked during the pass

Installed package metadata matches all four locked versions above. This was a read-only
metadata check, not an integration test. Installed LangGraph source contains StateGraph
compilation/checkpointer inheritance, Send for per-assignment parallel dispatch, RetryPolicy
and interrupt/resume. Its interrupt documentation explicitly says the node restarts.

Current `backend/login_investigator/agent.py` builds a LangChain create_agent with the supplied
checkpointer. Streaming filters the node name `model`; report writing updates state as that
node. History and offline saved-report reading consume the checkpoint's messages channel.
These consumers need an explicit compatibility path if the outer graph changes. Existing
SQLite checkpoints are not automatically migrated by selecting a new graph design.

`backend/api/investigation_routes.py` reserves one writer per investigation through streaming
and report creation. Stream cleanup closes the core before releasing that reservation.
Internal parallel research must preserve this conversation-level ownership. A browser
disconnect is not evidence of a durable human-approval pause or guaranteed provider cancellation.

These are integration constraints, not reproduced defects or authority to rewrite existing
tools before the planned architecture is settled. No application test or inference ran.
