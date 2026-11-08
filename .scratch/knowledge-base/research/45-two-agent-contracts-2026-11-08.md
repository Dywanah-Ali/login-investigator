# T45: request and response contracts between two agents

Date: 8 November 2026. Tier 3 decision research. Findings for discussion, not an adopted schema.

## Finding

There is a useful foundation to reuse: assign a bounded job, control the context crossing the
boundary, return usable results with traceable evidence, and validate the handoff in code.
The sources examined do not establish one universal request/response schema. They support
these responsibilities, while leaving exact fields and status names to the application.

For this project, the established chat/research role split remains appropriate to investigate.
The research does not independently prove that two agents outperform one here. IC-01–11 and
P-01–03 remain inherited requirements, not proposals needing approval again. In particular,
the analyst retains the verdict, and code owns facts and required-check enforcement.

## Scope and method

Security workflows were sought first, then research systems and framework documentation.
This is distinct from the later LangGraph orchestration research; no topology or migration is chosen.

Read the [earlier security-investigation research](45-security-investigation-initial-2026-11-07.md)
before searching. Perplexity supported discovery; material claims were checked in primary pages.
Keenable was unavailable. No benchmarks, application tests or application model experiments ran.

## Primary sources and limits

### 1. A close security example: Microsoft DTDA

[GenAI-Driven Threat Detection with Microsoft Security Copilot, v1, 20 May 2026](https://arxiv.org/html/2605.20896v1),
sections 3.1 and 5.2, describes fixed input/output schemas, permitted values, grounding checks
and bounded invalid-output retries. Planner assignments specify entity scope, a hypothesis
and evidence needed. The executor returns relevant timeline evidence and a short explanation
of its relationship to the task. This is unusually close to our evidence delegation boundary.

Limits: the inspected paper gives prose descriptions, not a complete published JSON contract
to copy. It discovers attack gaps and generates alerts, unlike our analyst-owned verdict.
Its suppression of invalid tasks/evidence must not become silent omission in our workflow.
Its two investigation rounds are its own design, not a justified retry limit for us.
Reported deployment/performance claims were not reproduced; none is used as an acceptance target.

### 2. Production research delegation: Anthropic

[How we built our multi-agent research system, 13 June 2025](https://www.anthropic.com/research/multi-agent-research-system)
describes a lead researcher delegating to workers with separate contexts. Assignments need an
objective, expected output, tool/source guidance and boundaries. Vague assignments caused
duplication and gaps. Workers inspect results and refine searches; the lead synthesizes returned
findings. Citation processing is separately described.

Limits: this is a first-party engineering account of broad research, not a controlled comparison
of contract formats. It does not prescribe our task enum, response statuses or evidence schema.
Its many-worker topology and token budgets do not transfer automatically to two agents.

### 3. Explicit input/output control: LangChain subagents

[Subagents documentation](https://docs.langchain.com/oss/python/langchain/multi-agent/subagents),
accessed 8 November 2026, describes supervisor-owned routing and context isolation. Inputs can
be a task description or selected state/history. Outputs can be formatted in code with additional
state. It warns that useful work may be absent from a worker's final message, which is all a
simple wrapper returns. Its concrete output example pairs a ToolMessage with an injected
tool-call ID and returns an extra state field through Command.

Limits: the example demonstrates correlation and explicit data transfer, not a research-evidence
schema. Full history is an option, not a requirement. A concise final summary is insufficient
for our preserved-evidence requirement unless supporting material is transferred as well.

### 4. Typed output mechanics: LangChain structured output

[Structured output documentation](https://docs.langchain.com/oss/python/langchain/structured-output),
accessed 8 November 2026, shows a schema passed through response_format, validated output in
structured_response, and configurable handling of malformed or multiple outputs. Provider-native
and tool-based strategies are distinguished. Its worked examples validate field types,
permitted values and numeric constraints.

Limits: these examples establish shape-validation mechanisms, not truth, relevance, source
coverage or that a claimed check ran. Compatibility with the eventual model/provider path
must be checked during implementation. The local lockfile pins LangChain 1.3.1 and LangGraph
1.2.4; that is a dependency observation, not runtime compatibility proof. No Deep Agents
adoption is implied.

### 5. General architectural guidance: Azure Architecture Center

[Agentic Behavior Engineering](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/agentic-behavior-engineering),
accessed 8 November 2026, recommends an overall behavior contract plus handoff contracts where
responsibility, evidence requirements or permissions change. Its grounding guidance preserves
source, version and authority. The retrieval layer distinguishes returned data, no matches and
failure; application logic decides how insufficient evidence affects continuation.

Limits: this is architectural guidance, not experimental evidence for a particular schema.
Its product-review example and Azure service choices are not our workflow. The transferable
point is that retrieval outcomes and application decisions have different owners.

### 6. Concrete lifecycle envelope: A2A

[A2A specification](https://a2a-protocol.org/latest/specification/), sections 4.1 and 6.1,
accessed 8 November 2026, separates task identity, lifecycle status, interaction history and
result artifacts. The basic example returns a task ID, completed state and an artifact with
its own ID and content. Structured-data examples allow domain-specific result content.

Limits: A2A addresses interoperating agents across service boundaries. Our in-process agents
do not thereby need A2A, remote discovery or its network lifecycle. Its completed state does
not define an investigation's evidence sufficiency, and its enums do not settle our partial,
empty or omitted distinctions. The latest URL is a moving specification, not a pinned
implementation dependency.

## What should carry forward

The following recommendations are local design inferences from the source patterns and our
existing contract. They are not claims that an external standard mandates these fields.

| Area | Recommendation | Basis |
| --- | --- | --- |
| Request scope | Keep intent, explicit subjects, task associations, focus and timing. Verify that this combination tells the worker the actual evidence question without requiring the conversation history. | Anthropic assignment guidance; DTDA task scope; current approved request design |
| Purpose | Do not add a generic context field by habit. Test whether current focus can distinguish, for example, checking policy applicability from finding the actual exception record. Add a bounded question only if a concrete ambiguity remains. | Input control in LangChain; local inference, not an adopted new field |
| Output shape | Keep a predictable response with request/task correlation, results, evidence and limitations. Treat exact names as application choices. | LangChain structured outputs; A2A separation; IC-07/09 |
| Packet ownership | Distinguish model-authored selections/annotations from the final assembled packet. Let the model refer to retrieved evidence IDs; code resolves them and attaches preserved content, provenance and observed execution outcomes. | LangChain code-formatted outputs; DTDA grounding; P-01 and IC-09 |
| Meaning | Allow brief relevance/applicability observations linked to evidence. Keep these visibly separate from source facts and the chat agent's overall assessment. | DTDA executor explanation; settled role split |
| Missing work | Preserve per-operation outcomes and outstanding obligations. Never infer success or failure solely from evidence count. | Azure retrieval distinction; IC-07/08 |
| Context | Return the evidence needed for interpretation without the entire exploratory transcript. Keep the trace available for inspection separately. | LangChain context isolation/output warning; IC-06/09 |
| Trust | Neither retrieved passages nor worker prose can grant scope, change required checks or become trusted instructions. Validate identifiers and scope against application state. | IC-10 and P-01; this is inherited local policy, not a new guarantee from JSON |

### Keep, revise and defer in the current drafts

**Keep:** explicit request/subject/task identity; scoped assignments; actual returned evidence
with provenance; distinct missing outcomes; code validation; preservation of competing evidence.
These fit the external patterns and already serve approved requirements.

**Revise before freezing:** distinguish the worker's model output from the code-assembled
response. The research model should not have to reproduce source text, invent evidence IDs or
self-certify execution. The existing packet table can describe the final handoff, but each field
needs a clear producer and validator. This sharpens the existing design rather than adding a
third agent.

**Reconsider the status taxonomy:** execution versus evidence yield is a useful local distinction,
but the current complete/partial/failed/unavailable/omitted by found/empty/undetermined cross-product
is not an industry standard. Prove that every supported combination has a distinct meaning and
consumer action. A simpler outcome list plus explicit outstanding work may suffice. Do not
collapse distinctions required by IC-07 simply to reduce the number of fields.

**Defer:** schema-version mechanics, cross-batch memory, saved-version loading, graph nodes,
streaming, retry caps and persistent worker identity. They need decisions, but this research
does not establish their implementations. Contract versioning deserves an explicit later choice
because saved evidence may outlive a schema revision; no version field is adopted here.

## Small design exercise before adding more fields

Use the existing request example and one mixed policy/exception request. Walk each through these
outcomes on paper, assigning a producer and consumer to every field:

1. Useful records and passages are returned.
2. A bounded search succeeds with no match.
3. One source fails after another supplies useful evidence.
4. Evidence is found but omitted from the final model-visible packet by a limit.
5. A returned reference is invalid or points to the wrong source version.

This proposed design exercise adds no runtime proof requirement or evaluation gate.

## Verification limits

Direct reading supports what these sources describe, not local effectiveness. The response
draft remains provisional. Exact field ownership, outcome aggregation, evidence representation
and saved-contract interpretation remain open as identified above.
