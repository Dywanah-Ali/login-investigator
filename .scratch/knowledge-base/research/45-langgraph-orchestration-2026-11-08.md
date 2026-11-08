# T45: LangGraph orchestration for the investigator

8 November 2026. Tier 3 design research, against the
[scoped brief](45-langgraph-orchestration-brief-2026-11-08.md).
Recommendation for author review, not an adopted topology or implementation release.

Subsequent ruling, 8 November 2026: the author accepted the explicit workflow recommendation
and the create_agent harness choice after the scalability/Deep Agents clarification. T45 and
the spec now carry that approval. Preserve the research wording below as its reasoning; the
architecture council follows next. Approval does not establish runtime proof or release build.

## Finding

Use a small explicit LangGraph workflow around the two approved agent roles. Let code
control assignment validation, required-work accounting, dispatch, evidence assembly and
completion. Let chat interpret the question/results and let research choose bounded retrieval
follow-ups. Keep the conversation persistent; start each research assignment with an isolated
context. No extra supervisor model or separate agent service is justified by this design.

This is a project-specific recommendation. Official documentation supports the component
mechanisms, but does not establish that this topology improves our investigation accuracy.
The inherited IC-01–11 requirements and existing evaluation gates remain the proof standard.

## Evidence checked

Perplexity discovery was followed by direct reading of official documentation. Keenable was
not available. The earlier contract research was reused; this pass concerns orchestration.
No inference, application tests, dependency upgrades or source-data changes ran.

| Primary source | Supported mechanism and practical limit |
| --- | --- |
| [Workflows and agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents) | Combines predetermined workflow paths with dynamic agent steps. Its examples support code gates around model calls; they do not prescribe our investigation procedure. |
| [Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api) | State, nodes, conditional edges, reducers and `Send` support explicit routing and parallel work with separate inputs. Reducers merge updates; they do not decide whether evidence satisfies an assignment. |
| [Subagents](https://docs.langchain.com/oss/python/langchain/multi-agent/subagents) | A main agent can call subagents as tools, with isolated context and explicit input/output transfer. A simple wrapper returning only the last message can omit evidence collected internally. The pattern still needs application enforcement of mandatory checks. |
| [Subgraphs](https://docs.langchain.com/oss/python/langgraph/use-subgraphs) | Default per-invocation persistence inherits the parent's checkpointer while keeping calls isolated. Per-thread persistence retains worker memory and has parallel-call conflicts. Stateless mode removes durable recovery. Explicit node integration supports state inspection better than tool-hidden subgraphs. These are current documented behaviours, not our runtime test results. |
| [Checkpointers](https://docs.langchain.com/oss/python/langgraph/checkpointers) | Persist thread state and successful sibling writes during a failed parallel step. New input, continuation after error and interrupt-resume are distinct operations. A saved checkpoint does not define an immutable evidence archive or certify task completeness. |
| [Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) | Pause for external input and resume with `Command(resume=...)`. Resuming restarts the interrupted node; earlier work can repeat. Broad exception handling can swallow the special interrupt signal. |
| [Fault tolerance](https://docs.langchain.com/oss/python/langgraph/fault-tolerance) | Describes retry boundaries, repeat-safe operations and timeout/error handling. Current docs include newer mechanisms that were not all checked against the installed version. Runtime recovery is not evidence-validity checking. |
| [Thinking in the Graph API](https://docs.langchain.com/oss/python/langgraph/thinking-in-graph-api) | Separates model reasoning, data operations and user-input stages. Useful for assigning responsibilities without making every helper a graph node. |

The older durable-execution URL now redirects to persistence. This note uses the current
checkpointer, graph and fault-tolerance pages rather than assuming the old page's layout.

## Smallest useful workflow

The following is a logical design recommendation, not a fixed node inventory:

```text
Chat interprets the question / constructs assignments
                      |
Code validates scope and establishes required work
                      |
Code dispatches independent research assignments
                      |
Research gathers and examines evidence within each assignment
                      |
Code validates results, assembles evidence and accounts for every task
                      |
Chat interprets evidence and gaps
         |                                |
Bounded authorised follow-up       Answer or clarification
```

Code-required collection is enforced through shared core and the assignment execution
boundary independently of a model choosing to call a tool. The exact full-procedure mapping
remains T26/T28 integration work. The graph should orchestrate those functions rather than
reimplement them or hard-code investigative meaning into routing.

Research can remain a `create_agent` graph with its own restricted tools. It need not become
a second overall investigator. A thin wrapper transforms the dispatched contract into worker
input and transforms its selections plus recorded operations into the validated response.
That wrapper must transfer actual evidence, not just the worker's final prose.

### Why not only a supervisor calling a research tool?

Both approaches are viable mechanisms. The tool-only approach is compact and preserves the
natural conversational loop. It can meet our requirements if deterministic middleware and
wrappers enforce all obligations. It does not inherently make checks optional.

For this application, an explicit outer workflow makes the already-required enforcement and
assembly boundaries easier to inspect and test. Otherwise much of the same workflow becomes
hidden in tool wrappers and middleware. That is the reason for the recommendation, rather
than an assumption that more graph nodes improve reliability. No supervisor package or third
model role is necessary. This comparison is an architectural inference from the contracts.

## State and memory boundaries

| Scope | Recommended ownership |
| --- | --- |
| Conversation | Preserve user-visible conversation continuity and trusted approvals at the parent level. Keep the existing case identity and one-writer boundary. |
| Investigation / batch / request | Store authoritative assignments, task identities, required-work states, evidence references and observed outcomes in code-owned state. Explicitly scope/reset these across new requests; do not infer them from conversational prose. |
| Research invocation | Supply only its assignment, permitted context and required evidence references. Use per-invocation persistence, with no automatic cross-call worker memory. |
| Saved answer evidence | Preserve actual source-bound content and provenance through the application's evidence persistence contract. Graph checkpoint retention is a separate concern. |

This does not introduce a new database or long-term memory store. Per-invocation isolation
does not mean that work cannot be checkpointed within that invocation. Checkpointed worker
internals also do not become authoritative evidence merely because they were saved.

## Independent work, failures and stopping

Use code dispatch, potentially `Send`, for assignments already known to be independent.
Interpretation-dependent work waits for chat's assessment. Aggregate by stable request/task
identity with deterministic duplicate/conflict handling, not by completion order. Application
code must still verify that every assigned result and subject is accounted for.

The distinction that matters: successful sibling checkpoint writes can survive a failed
worker for later resume, but an unhandled worker failure does not automatically produce a
useful partial answer. At the execution boundary, convert expected exhausted retrieval or
provider failures into the agreed typed outcomes so aggregation can report partial work.
Do not disguise programming/integrity failures as no-match, and do not swallow cancellation
or graph-interrupt control signals. These handling choices are application responsibilities.

Code enforces the stopping policy. The research model can identify a gap but cannot waive a
required check, enlarge scope or reset its own allowance. When execution stops, retain useful
validated evidence and outstanding obligations. Numeric budgets remain implementation details.

## Resume, replay and cancellation

Do not treat all subsequent calls on a conversation as the same operation. A new analyst
message starts new work against conversation state; a technical retry resumes unfinished
work; replay intentionally re-executes history. Continuing must retain original assignment
and source snapshot identity rather than silently querying today's replacement sources.

Node re-execution can repeat model/API calls. Keep expensive or non-repeatable operations at
deliberate persistence boundaries, preserve operation identity and outcomes, and distinguish
an uncertain remote result from proof that no work occurred. Checkpointing alone is not an
exactly-once guarantee. These are implementation constraints, not a new recovery product.

For ordinary clarification or analyst-approved scope expansion, retain the normal chat-turn
interaction initially. A durable `interrupt()` is available if a future workflow genuinely
must pause mid-execution, but this design does not require a new approval interface. Trusted
application state must record consent either way; a worker's text cannot grant it.

Cancellation remains the API/application's responsibility: stop active work, preserve honest
outcomes, and retain the existing per-case writer lock until execution has actually stopped.
A disconnected stream must not be mistaken for a successful research result. Do not equate
cancel with approval-wait or automatically resume cancelled work on the next message.

## Local compatibility and integration findings

Parent-session read-only checks confirmed installed versions match the lockfile:
LangChain 1.3.1; LangGraph 1.2.4; checkpoint 4.2.0; checkpoint-sqlite 3.1.1.
Installed source confirms `StateGraph.compile` checkpointer inheritance, `Send`, `RetryPolicy`
and interrupt restart semantics. This is not an executed integration or compatibility test.
Do not adopt every current documentation example, such as newer timeout/drain/error-handler
features, without checking the installed interface during implementation.

The existing `build_agent` uses `create_agent` with a supplied `SqliteSaver` and conversation
`thread_id`. Therefore this is an extension of existing LangGraph-backed execution, not a
first introduction of that runtime. Important consumers need deliberate adaptation:

- `backend/login_investigator/agent.py`: streaming filters for `langgraph_node == "model"`;
  report writing reads messages and updates state as node `model`; history reads messages.
- `backend/api/investigation_routes.py`: per-case writer coordination and
  stream closure/cancellation protect the existing lifecycle.

An outer graph can change message locations, node names and namespaces. Preserve or adapt
those interfaces and existing conversation reopening explicitly. No automatic migration is
established, and these observations are integration constraints rather than reproduced bugs.

## Follow-up: more researchers and choice of agent harness

The author asked these two questions before choosing the architecture. They are clarifications,
not approval of a topology, additional agents or a new dependency.

**Extensibility:** the proposed dispatcher can route existing evidence assignments to different
registered research implementations, each with the same validated request/result boundary,
isolated context and appropriate tools. Independent work can run in parallel and results join
by task/request identity. [LangGraph workflow guidance](https://docs.langchain.com/oss/python/langgraph/workflows-agents)
documents routing and parallel workers. This supports the mechanism; smooth local expansion is
an inference conditional on preserving those boundaries. Specialist ownership, cross-purpose
tasks, duplication, costs/concurrency and quality still require design/evaluation. More workers
do not automatically improve accuracy or imply infrastructure scaling. Do not split tools into
agents merely because four documentary purposes exist.

**Harness choice:** the first orchestration pass did not directly compare Deep Agents with
create_agent. This follow-up checked official
[LangChain agents](https://docs.langchain.com/oss/python/langchain/agents),
[Deep Agents overview](https://docs.langchain.com/oss/python/deepagents/overview) and
[customization](https://docs.langchain.com/oss/python/deepagents/customization).
create_agent supplies a configurable model/tool loop. Deep Agents adds an assembled harness
for work such as context offloading, filesystem-backed context and subagent delegation, with
planning/memory capabilities available. Those capabilities are configurable, not proof that
every deployment must expose unrestricted files or execute code. Both compose with LangGraph;
create_deep_agent's documented return is a compiled graph.

Recommend create_agent for the bounded research tool loop and retain the existing LangChain
agent construction seam. Chat construction can use create_agent where it needs a loop, or
ordinary model calls for individual workflow stages; no need to force a tool loop onto each
code stage. The outer StateGraph coordinates either. This is a fit recommendation: our fixed
contracts, restricted tools, code-owned checks and evidence-preservation needs are explicit,
whereas adopting a larger harness would require reconciling its delegation and context
management with them. It is not a claim that Deep Agents is inferior or that create_agent
cannot plan, handle multiple steps or cooperate with other agents.

Revisit Deep Agents if future requirements materially benefit from its long-running context,
workspace or delegation machinery. A compatible worker could then sit behind the same
contract, subject to validation; this is not a promise of a drop-in replacement. Neither
factory supplies a smarter model by itself. Local metadata confirms deepagents is not installed;
LangChain 1.3.1 is installed. No installation, agent execution or comparative benchmark ran.

## Architecture ruling still pending

Seek one architecture ruling: a thin explicit parent workflow, isolated per-invocation research,
and code-owned enforcement/assembly, retaining normal chat clarification and existing persistence
infrastructure. The alternative is the tool-only main-agent pattern with equivalent enforced
boundaries. Both require implementation verification; documentation alone cannot select by
measured quality. Do not reopen the approved two roles, evidence contract or analyst verdict.

After that ruling, reconcile the architecture with T25/T26, retain remaining T45 obligations,
and run the agreed architecture review. Do not turn node names, numeric limits or routine
retry cases into another approval tour. No implementation or paid experiment is authorised
by this note.
