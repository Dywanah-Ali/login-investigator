# T45 architecture council

8 November 2026. One independent five-persona review under the installed
[roast-technical skill](/Users/wael/.codex/skills/roast-technical/SKILL.md).
[Shared brief](45-architecture-council-brief-2026-11-08.md).
Three reviewers ran first, then two as slots became available. Findings were not shared
between reviewers. Reviewers were read-only; no services, inference or implementation tests ran.

## THE VERDICT: GO
Confidence: medium

**The call in one line:** Keep the approved explicit LangGraph workflow and create_agent
workers; finish T45's named design/ownership handoff before implementation.

**Why:** All five reviewers found the role, contract and code-enforcement boundaries coherent,
with no demonstrated P0/P1 architecture blocker. The tension is between a strong execution
ledger and the possibility of incomplete investigative meaning: recording that assigned work
ran cannot prove the correct work was assigned or decisive evidence was delivered. Keep the
existing semantic and application evaluation obligations alongside deterministic enforcement.

**Biggest risk:** A full-investigation request becomes a valid narrow assignment before
required-work enforcement, so later completion accounting certifies the wrong scope.
This is an acknowledged mapping dependency, not an observed implementation failure.

**Biggest upside:** One visible workflow can enforce obligations and preserve evidence while
leaving interpretation to models and the verdict to the analyst.

**Cost & effort read:** Moderate integration work, concentrated in procedure ownership,
state/evidence handling and existing streaming/report/history consumers. No additional
supervisor, service or database is required by this decision. Shared core and contract boundaries
keep worker changes contained, but saved-state changes require deliberate compatibility work.
No time/cost estimate or production readiness is established by this design review.

**The cheapest test to de-risk it:** In the existing build verification, use a fake chat
constructor that omits a mandatory task from an explicitly requested full investigation.
Confirm the trusted procedure definition still supplies or visibly accounts for that task;
pair it with a narrow lookup that remains narrow. This is a focused plumbing check under
existing IC-08 obligations, not a new gate or experiment to run during T45.

Contrarian 7/10 · Expansionist 8/10 · Logician 8/10 · Researcher 8/10 · Operator 8/10

## Independent reviewer records

### Contrarian

Stance: GO; no P0/P1 blocker; safety 7/10.

- A complete execution ledger can accompany an incomplete investigation.
- Full-investigation activation must survive the model's assignment construction.
- Important competing evidence can lose ranking before either model sees it; an exclusion
  receipt alone cannot support interpretation.
- A bounded no-match may fulfil execution while the query is semantically wrong.
- Late/resumed evidence needs answer association as well as valid source/task IDs.

Most important: procedural completeness and investigative adequacy are different.
Suggested cheapest check: the full-request/narrow-assignment mismatch above.

### Expansionist

Stance: FOR; no P0/P1 blocker; upside/durability 8/10.

- Code-owned assignment accounting makes omitted work inspectable.
- Separating evidence custody from interpretation remains useful with stronger models.
- Combined discovery, no second five-passage cut and parent-passage delivery support
  preservation, without proving coverage.
- Contracts enable later specialisation without requiring more agents now.
- Shared core must serve full and narrow paths; do not create a duplicate coordinator.

Most important: keep code responsible for whether work happened and models for its meaning.
Suggested cheapest check: one successful and one failed subject, with a worker falsely
claiming complete; code must retain the evidence and derive partial completion.

### Logician

Stance: GO; no P0/P1 blocker; coherence 8/10.

- Authoritative assignments and code-built receipts consistently implement P-01/IC-08.
- Legacy full-mode tool choice needs a bridge to the new intent/task contract.
- One core procedure definition should serve dispatch, completion and reports.
- Procedural completion is distinct from evidence adequacy.
- Parent state, worker state and saved evidence have coherent separate responsibilities;
  the exact saved-source representation remains an implementation dependency.

Most important: define mandatory work once in code.
Suggested cheapest check: omitted mandatory task under full mode versus a valid narrow lookup.

### Researcher

Stance: GO; no P0/P1 blocker; evidence support 8/10.

- [Subgraph documentation](https://docs.langchain.com/oss/python/langgraph/use-subgraphs)
  supports isolated per-invocation research with inherited checkpointing.
- [Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api) and
  [streaming documentation](https://docs.langchain.com/oss/python/langgraph/streaming)
  do not make private state schemas a public-output security boundary. A nested worker can
  also have a model node; public answer routing must be explicit.
- State reducers require deliberate request scoping; a new message does not imply all
  accumulated completion state resets.
- [Checkpointers](https://docs.langchain.com/oss/python/langgraph/checkpointers) support
  recovery of successful sibling work, not automatic construction of a valid partial answer.

Most important: the framework coordinates; the application defines completeness and public output.
Suggested focused check: failure/resume then a new request on the same conversation, with
no stale completion, misplaced evidence or research-only tokens in the public stream.

### Operator

Stance: GO; no P0/P1 blocker; operability 8/10.

- Existing model-node stream filtering and top-level message consumers need an adapter.
- Cancellation must retain the case writer reservation until child work actually stops.
- Explicit failed/unavailable/omitted outcomes support trustworthy partial results.
- Reopening a conversation and preserving historical evidence are separate obligations.

Most important: make finished, partial and cancelled outcomes distinguishable.
Suggested focused check: two fake workers, one successful and one blocked, then disconnect;
check public output, cleanup/writer ownership and reopening. No new monitoring service.

## Judge fact-check and disposition

| Concern | Verified basis | Disposition and existing owner |
| --- | --- | --- |
| Full versus narrow activation | T45 gives chat task construction but explicitly forbids waiving code-required checks; spec's legacy shortcut still relies on investigate_alert tool choice. | Open handoff dependency, not a contradiction requiring new architecture. T45 reconciles the trigger and shared procedure ownership with T26/T28 and the orchestration build ticket before release. |
| Evidence lost despite procedural completion | T45 explicitly distinguishes complete work from semantic adequacy and preserves unresolved original K04 obligations. | Retain AUD-062 and existing T29/T40/T41 evidence-stage tests. No new cap/gold/threshold ruling. |
| Private worker output in public stream | agent.py filters on langgraph_node == model. A future nested create_agent has model output too; actual propagation depends on configuration. | Inferred future integration risk, not a reproduced current leak. Orchestration owner must explicitly route only public answer text and preserve progress separately. |
| Stale or late results | Existing response contract requires retained request identity; research note requires request-scoped state and cancellation ownership. | Implement generation/answer association and reset/merge semantics under existing lifecycle contract. No new cross-batch memory policy. |
| Cancelled workers outliving writer lock | API writing/question_stream currently hold the reservation through core cleanup. | Preserve that guarantee across all child work. Existing lifecycle verification owns proof. |
| Historical evidence versus checkpoints | IC-09 and T45 require captured source-bound evidence; saved representation remains open. | Retain T27/T33/T35/T42 and orchestration integration responsibilities; link AUD-065 without reopening a storage migration. |

These are lower-severity review observations and named dependencies, registered under AUD-086
with existing concerns linked. No application bug was reproduced, so no fabricated bug-log
entry is created. No second review round or extra proof programme is requested. The proposed
checks above are alternatives/concrete examples for existing build checks, not a demand to
stack all of them as new gates. No review finding changes the approved architecture.

## Remaining T45 closure work

This GO is for the design direction. T45 remains claimed: full-procedure/task-search mapping,
prompt examples, E06 source approval, original gate/keyword dispositions, final tool/core
ownership and the two implementation-ticket handoffs remain. Numeric budgets/source adapters
and runtime proof keep explicit downstream owners. No build, migration, push or deployment
is authorised by this report.
