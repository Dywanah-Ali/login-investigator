# Research note 05: how the knowledge base reaches the agent: tool shape, checkable citations, the injection stance, cost, and the plan in code

Ticket: [05-agent-tools-for-the-knowledge-base](../issues/05-agent-tools-for-the-knowledge-base.md)
Date: 22 October 2026
Method: Perplexity first, as the author ruled for this ticket. One Perplexity deep-research call was
attempted and **timed out after five minutes with no result**; the note therefore rests on twenty-one
Perplexity search calls restricted to primary domains (docs.langchain.com, python.langchain.com,
github.com/langchain-ai, neo4j.com, microsoft.github.io, genai.owasp.org, platform.openai.com,
developers.openai.com, arxiv.org, anthropic.com, platform.claude.com, simonwillison.net, openrouter.ai,
elastic.co, sigmahq.io, docs.ragas.io, deepeval.com), twenty-two WebFetch calls that opened primary pages
(three redirected or returned 404: the LangGraph plan-and-execute tutorial twice and the old
`python.langchain.com` tool-artifacts page), one Keenable fetch (the OpenRouter model page, which
rendered without prices; the OpenRouter endpoints API was opened instead), and direct reads of the
**installed, pinned** packages in `backend/.venv`: `langchain` 1.3.1 (`agents/middleware/types.py`,
`agents/factory.py`, `agents/middleware/tool_call_limit.py`), `langgraph-prebuilt` 1.1.0
(`prebuilt/tool_node.py`), `langchain-core` 1.4.0 (`messages/tool.py`), with `langgraph` 1.2.4 and
`langgraph-checkpoint-sqlite` 3.1.1 confirmed from `uv.lock`. No customer or personal data was sent
anywhere; no secrets involved. `[P]` marks a claim verified against a primary source opened in this
research (a fetched page or an installed source file); `[V]` marks a research-pass, vendor or
practitioner claim seen only through search snippets or aggregators.

**Fixed constraints from the ticket (author's rulings, 22 October 2026).** The playbook lives in code;
the chat question is the only trigger; conversation first, report second, with a light gate per turn
and a full gate at report time; code walks the graph and the agent reads the joined result; the
playbook's corpus searches are derived in code from the alert record, with a free `search_corpus`
kept for follow-ups; the model translates prose into a typed tool call and code acts only on the
typed call. Earlier decisions the tools must fit: hand-written, parameterised, read-only tools and a
read-only database role (ticket 02, decision 8); typed filter options, never a model-written filter
(ticket 03, decision 6); the corpus tool returns a `none` / `weak` / `found` verdict computed in code
(ticket 03, decision 1); PostgreSQL with pgvector as the one store, NetworkX for walks (ticket 02).

## 1. The question

Ticket 05 decides which read-only tools the investigator gets, what each returns, how the agent cites
what it returns, how the design treats retrieved text it cannot trust, how many model calls a flagged
login should cost, and where the playbook lives in the pinned LangChain and LangGraph versions. The
author asked for the research to ground a grilling, so this note separates **what the sources say**
(sections 3.1 to 3.5, each with status marks) from **what this note recommends** (the closing
paragraph of each section, and section 5).

## 2. The criteria, from the ticket and the earlier decisions

| Criterion | Source |
|---|---|
| Each tool is justified by the playbook step it serves; no step, no tool | ticket 05, consequence 1 |
| A defined shortcut rule: full investigation versus narrow lookup, sturdier than the Port's regex test | ticket 05, consequence 2; entry-point ruling |
| The plan is testable: ticket 06 can check that the required steps ran, not only that the answer was right | ticket 05, consequence 3 |
| The plan is a floor, not a ceiling: policy adds missing steps, never removes the agent's own | ticket 05, caution |
| Two gates: light per turn (answer only what the tools returned, cite or refuse), full at report time | shape-of-the-answer ruling |
| Code walks the graph; one core function returns the joined radius, shared with the `truth.json` test | who-walks-the-graph ruling |
| Hand-written, parameterised, read-only tools; read-only database role; model writes no query or filter | ticket 02 decision 8; ticket 03 decision 6 |
| Corpus results carry the `none` / `weak` / `found` verdict, computed in code | ticket 03 decision 1 |
| Graph and corpus content are untrusted data, like log fields | ticket 05 scope; security rules |
| The model is gpt-4o-mini through OpenRouter until 14 January 2027 (AUD-031) | CLAUDE.md |
| Seams: tool list from one place, model and agent made in one function, data access in the core | architecture rules |

## 3. Findings

### 3.1 How agents consume a graph plus text in practice (question 1)

| What ships | Fact | Status |
|---|---|---|
| Neo4j `neo4j-graphrag` | Five retrievers: `VectorRetriever`, `VectorCypherRetriever` (vector hit, then a **fixed** Cypher `retrieval_query` written by the developer walks outward from `node`), `HybridRetriever`, `HybridCypherRetriever`, and `Text2CypherRetriever` (an LLM writes the Cypher; the docs warn "the LLM-generated query is not guaranteed to be syntactically correct"). A `ToolsRetriever` wraps retrievers as tools and uses an LLM to pick which to run. The `GraphRAG` class is retriever plus LLM plus prompt template. | [P] user guide; [V] `ToolsRetriever` source via snippet |
| Neo4j's LangChain agent guidance | Retrievers "are plain Python objects with a `search()` method, so they wrap with the `@tool` decorator like any other function"; the example exposes one `search_news(question)` tool whose fixed `retrieval_query` returns chunk text plus the article title and up to five company names. The graph walk is written by the developer, not the model. | [V] Neo4j Labs page via snippet |
| Microsoft GraphRAG | A query engine with fixed methods, not an agent: local search (entities, their neighbours, text units, community reports packed into one context window), global search (map-reduce over community reports), DRIFT (local search primed with community reports), basic search. The local-search prompt tells the model to cite "`[Data: <dataset name> (record ids); ...]`", "do not list more than 5 record ids in a single reference", and "do not include information where the supporting evidence for it is not provided". | [P] GraphRAG docs and `local_search_system_prompt.py`; [V] Microsoft Research DRIFT post |
| LangChain and LangGraph | The documented shapes are: a `create_agent` loop with typed `@tool` functions and middleware; the "agentic RAG" graph (model decides whether to retrieve, a grader node checks relevance, a rewrite node retries); and sub-agents as subgraphs. Per-thread sub-agent subgraphs "do not support parallel tool calls", and the docs use `ToolCallLimitMiddleware` to stop the model calling one in parallel. | [P] subgraphs page, built-in middleware page; [V] agentic-RAG tutorial via snippet |
| OpenAI tool guidance | "Aim for fewer than 20 functions available at the start of a turn", "combine functions that are always called in sequence", "don't make the model fill arguments you already know", "use enums and object structure to make invalid states unrepresentable"; function definitions are billed as input tokens. The o-series guide: fewer than about 100 tools and 20 arguments per tool is in-distribution, but "hallucinated or speculative tool calls" are reported "when the toolset is large and under-defined". | [P] function-calling guide and o3/o4-mini guide |
| Anthropic tool guidance | "Build a few thoughtful tools targeting specific high-impact workflows"; tools "can handle frequently chained, multi-step tasks in a single tool call"; "too many tools or overlapping tools can also distract agents"; return "high-signal" fields and keep low-level identifiers behind a `response_format` enum (`concise` / `detailed`); paginate or truncate large responses; name parameters unambiguously (`user_id`, not `user`). | [P] "Writing effective tools for agents" |

**Three shapes against the criteria.**

| Shape | For | Against |
|---|---|---|
| Few typed tools (what Neo4j's agent example, OpenAI and Anthropic all show) | Each tool is one playbook step with typed parameters; the schema is the shortcut rule (`investigate_alert` means the full plan, `lookup_account` means a narrow lookup); the eval can see which tool ran. | More schemas in every request; descriptions must not overlap. |
| One router tool (`query_knowledge_base(kind=..., ...)`) | One schema. | The router's `kind` enum hides the steps from the eval and from the policy; the model still has to choose, now with less description per choice; Neo4j's `ToolsRetriever` shows the alternative, an extra LLM call to route, which gpt-4o-mini would pay on every question. |
| Sub-agent for the knowledge base | Isolates the corpus from the main model's context (the Dual-LLM idea, section 3.3). | A second model call per step; per-thread subgraphs forbid parallel calls and need their own checkpoint namespace; the Port's one-function agent factory would become two; nothing in phases 0 and 1 needs it. |

**What this means for ticket 05.** The sources converge on few, typed, hand-written tools, each
wrapping a developer-written query, with a fixed walk behind a vector hit (Neo4j's
`VectorCypherRetriever` is the same idea as the author's "code walks, the agent reads"). Text2Cypher
is the one shape every source treats as the risky one, and ticket 02 already ruled it out. The
recommendation is seven tools: the Port's three unchanged, `investigate_alert(finding_id)` for the
playbook, `lookup_account(account_id)` and `find_peers(...)` for narrow lookups on the graph, and
`search_corpus(question, doc_type, technique_id)` for follow-ups. Whether a spray alert's targets need
`expand_alert(finding_id)` or are a section of the investigation package is a grilling question. No
router, no sub-agent, in this initiative.

### 3.2 Return shapes that make a citation checkable (question 2)

| Fact | Consequence | Status |
|---|---|---|
| LangChain tools can return `(content, artifact)` with `response_format="content_and_artifact"`; `ToolMessage.artifact` is "not meant to be sent to the model" and holds the part of the output the model does not need. Both `content` and `artifact` are in the message that the checkpointer saves. | The model reads a short `content`; the eval and the screen read the full `artifact` (chunk IDs, every recorded score, the verdict). One tool call, two audiences. | [P] `langchain_core` 1.4.0 `messages/tool.py`; `langchain_core` tool reference |
| Tools can read agent state through `runtime: ToolRuntime`, hidden from the model. | A tool can see which alert the conversation is about without the model restating it. Not needed for phase 1; a seam. | [P] LangChain tools page |
| OpenAI's citation guidance: cite at **block or chunk** level ("the best default"), give every source a **stable source ID** such as `turn0block1`, readable text, optional metadata; validate citations in code: parse markers, check the ID format, **resolve IDs against the sources actually provided**, flag any that do not resolve, strip markers before display. | Citation checking is a deterministic step after the model answers, not a prompt instruction alone. | [P] OpenAI citation-formatting guide |
| Anthropic's `search_result` content blocks: a tool returns `source` ("any stable string works: a URL, or an internal identifier such as `kb://article-1234`"), `title`, `content`; the model's citation returns `cited_text` and the block index. Not available to us (OpenAI-compatible endpoint), but it names the same three fields. | A chunk's citation needs a stable identifier, a title and the quoted text. | [P] Claude platform docs |
| GraphRAG's answers carry `[Data: Sources (15, 16); Entities (5, 7)]` references with at most five record IDs per reference and an instruction never to include unsupported information. | A precedent for citing **graph records and text chunks with the same marker syntax**. | [P] `local_search_system_prompt.py` |
| RAGAS faithfulness: split the answer into claims, check each against the retrieved context, score = supported claims / all claims; LangSmith's RAG tutorial does the same with a "groundedness" LLM judge against the retrieved documents; DeepEval's faithfulness counts a claim truthful "if it does not contradict" the context. These judge **groundedness**, not whether the citation points at the right chunk. | Two checks, not one: a deterministic **citation check** (every marker resolves to a chunk or record returned in this conversation; every material sentence carries one) and an LLM-judged **faithfulness** sample. The first is cheap and exact; the second catches claims that resolve but misread the chunk. | [P] RAGAS stable docs, LangSmith tutorial; [V] DeepEval via snippet |
| **The database is rebuilt per test session and per eval run (ticket 02, decision 5).** Any ID a database assigns on insert is therefore unstable. | Chunk IDs must be computed from content and position: document slug, version, section path, ordinal. Entity IDs come from the ground-truth files and are already stable. | design consequence of ticket 02 |

**Stable finding identifier (the ticket's candidate decision), precedent.** Sigma rule IDs are UUID v4
and change only for major logic changes, derivation or merge; that is a stable **rule** ID, not an
alert ID [P] SigmaHQ rules page. Elastic Security computes an alert's `_id` as
`sha256(docIndex + docId + version + ruleId)` so re-running a rule over the same source event yields
the same alert and duplicates are not created; its troubleshooting page says "the engine uses document
`_id` to avoid generating duplicate alerts for the same source event" [P] Kibana source `utils.ts`
(`generateId`), Elastic troubleshooting page. Splunk ES assigns `event_id` to notable events and keeps
`rule_id` and `orig_event_id` beside it [V] Splunk dev docs via snippet. The pattern across detection
systems is the same: **hash of rule identity plus the content that fired it**, so the ID survives a
re-run and a restart.

**What this means for ticket 05.** Every tool result should name its records with IDs the eval can
resolve: `F-<rule>-<hash8>` for a finding (rule slug plus a hash of the finding's defining fields:
rule, user, IPs, first and last seen), the ground-truth entity ID for a graph record, and
`<doc-slug>@<version>#<section-path>/<ordinal>` for a chunk. The tool's `content` shows the model
short per-call labels (`[S1]`, `[A1]`), because a small model copies short labels more reliably than
long IDs; the `artifact` carries the label-to-ID map and the full record. An `after_model` check
(section 3.5) resolves every label in the answer against the artifacts of the conversation. The
playbook package should carry the step name on each section, so a citation says which step produced
it. The stable finding ID touches `rules.py` and the Alerts API shape and stays a grilling question.

### 3.3 Prompt injection through tool outputs (question 3)

| Fact | Status |
|---|---|
| OWASP LLM01:2025: "it is unclear if there are fool-proof methods of prevention"; the seven mitigations are constrain behaviour in the system prompt, define and validate output formats with "source citations" and "deterministic code", filter input and output, least privilege with privileged functions "in code rather than providing them to the model", human approval for high-risk actions, "segregate and clearly denote untrusted content", adversarial testing. | [P] genai.owasp.org LLM01 |
| Greshake et al. 2023: indirect injection lets retrieved data "act as arbitrary code execution", "manipulate the application's functionality, and control how and if other APIs are called". | [P] arXiv 2302.12173 abstract |
| Hines et al. 2024 (Microsoft, "spotlighting"): three transformations, delimiting, datamarking (replace every space with a marker such as `^`) and encoding (base64); attack success fell "from greater than 50% to below 2%" on GPT-family models of that era; delimiting alone helped least, datamarking is the minimum they recommend, encoding only for high-capacity models. | [P] arXiv 2403.14720 abstract; [V] per-technique figures from the paper body via snippet |
| Karanjai et al. 2026, injection through **log fields** read by an LLM analyst: baseline success up to 88.2%; XML delimiting plus a trust-boundary sentence cut GPT-4o's rate from 87.3% to 51.4%, the best single defence they tested, **but the rate climbed from about 32% at 1K tokens of context to about 72% at 16K**; layered defences (filter, harden, validate output) reached 90.4% reduction with 8.4% residual. | [P] arXiv 2607.14493 abstract and HTML |
| Nasr et al. 2025: adaptive attacks bypassed twelve recent defences "with attack success rate above 90% for most", including ones that had reported near-zero rates. | [P] arXiv 2510.09023 abstract |
| Beurer-Kellner et al. 2025, six design patterns with structural guarantees: action-selector, **plan-then-execute** ("tool outputs cannot inject instructions that make the agent deviate from its plan", a form of control-flow integrity), LLM map-reduce, Dual LLM (Willison 2023), code-then-execute, context minimisation. | [P] arXiv 2506.08837 abstract; [V] pattern descriptions via Willison's summary and the HTML body |
| Willison's lethal trifecta: private data, untrusted content, and a channel to communicate externally; an agent with all three "can easily be tricked" into exfiltration; past incidents were fixed by removing the outbound channel. | [P] simonwillison.net, 16 June 2025 |
| LangChain at the pinned version: `wrap_tool_call` wraps every tool call and may return a modified `ToolMessage`; `after_model` runs after every model response and may `jump_to="model"`; built-in `PIIMiddleware` has `apply_to_tool_results`; `ContextEditingMiddleware` clears old tool outputs. There is no built-in "fence tool outputs" middleware; it is about ten lines of `wrap_tool_call`. | [P] installed `types.py`; built-in middleware page |

**Reading the evidence against this agent.** The agent holds private data (the log, the graph) and
reads untrusted content (log fields, corpus text), but it has **no third leg**: every tool is
read-only and the only outbound channel is the answer shown to the analyst. The worst an injection can
do here is make the agent say something wrong, skip a step, or dress attacker text as a finding; that
is a misinformation risk, not exfiltration. The defence target is therefore **answer integrity**, and
the measures that hold under adaptive attack are the structural ones: a plan the tool outputs cannot
alter (plan-then-execute, which the author's "plan lives in code" ruling already is), tools that cannot
act, and deterministic checks on the answer. Prompt-level measures reduce the rate and never close it;
delimiting helps less than datamarking; datamarking would break the Port's rule that log values are
copied in full (a `^` in every value is unacceptable in an answer the analyst reads); encoding is for
larger models and costs tokens.

**What this means for ticket 05.** A system-prompt sentence is not enough on its own, and the sources
do not make it enough. The cheap measures that hold: (1) every tool result is fenced and labelled with
its source and its trust level in one place, a `wrap_tool_call` middleware, so no tool author can forget
it and the eval can assert it; (2) results stay structured JSON with named fields, which is itself a
weak delimiter and makes stray prose stand out; (3) the plan in code: tool outputs cannot add or remove
steps; (4) deterministic output checks after the model: citations resolve, finding IDs exist, "do not
know" wording is used when the verdict is `none`; (5) the eval carries injection canaries in both the
log (the Port's S5) and the corpus (a planted paragraph that instructs the model), measured as a pass
rate; (6) keep contexts short, because the only measured defence degrades with context length, which
is one more argument for a bundled result over a long chain of raw tool outputs. The Port's prompt
rule that an instruction found in data is itself evidence of an attack stays.

### 3.4 Cost, efficiency and tool granularity (question 4)

| Fact | Status |
|---|---|
| OpenRouter serves `openai/gpt-4o-mini` at **$0.15 per million input tokens, $0.60 per million output, $0.075 cache read**, 128,000 context, from OpenAI and Azure (an EU Azure endpoint at $0.165 / $0.66). | [P] OpenRouter endpoints API, 22 October 2026 |
| OpenAI: keep the initial tool list under about 20; combine functions always called in sequence; the model may issue several calls in one turn unless `parallel_tool_calls=false`; tool definitions are billed as input tokens on every call. | [P] function-calling guide |
| gpt-4o-mini on tool benchmarks: in CallNavi it tracks GPT-4o on routing and syntax (overall 0.908 versus 0.913) but falls to 0.36 on the hardest nested, multi-call tasks; the paper finds small models "exhibit instability ... in complex, multi-step scenarios". An aggregator lists its BFCL v3 overall at 64%, and one paper reports 66.5% on a multi-turn subset against 68% for GPT-4o. | [V] arXiv 2501.05255, arXiv 2508.05118, whatmodel aggregator via snippets |
| Anthropic: consolidate "frequently chained, multi-step tasks in a single tool call"; this "reduces the context that would have otherwise been consumed by intermediate outputs". | [P] "Writing effective tools for agents" |
| OpenAI's own programmatic-tool-calling guidance: use a program when "a stage has predictable control flow and code can return a smaller structured result"; use direct tool calls when "each result requires fresh model judgment". | [V] OpenAI developers page via snippet |

**Arithmetic for one flagged login, stated assumptions.** System prompt about 1,200 tokens; seven tool
schemas about 1,500 tokens; each model call re-sends the whole conversation.

| Shape | Model calls | Input tokens (approx.) | Output tokens | Cost |
|---|---|---|---|---|
| Separate steps enforced by policy (find, then account, assets, peers, two searches, answer) | 7 | 7 calls × growing context, about 45,000 in total | 1,500 | about $0.008 |
| Bundled `investigate_alert` (find, bundle, answer) | 3 | about 15,000 | 1,500 | about $0.003 |
| Narrow lookup ("who owns this device") | 2 | about 6,000 | 300 | about $0.001 |
| Eval run, 100 questions, mixed | | | | $0.30 to $0.80 |

Cost is not the deciding factor at this scale; **reliability and latency are**. Seven dependent calls
is where the benchmarks show a small model drifting (a step skipped, a parameter mis-copied), and each
extra call is one more place the policy must repair. The user-watches-it-unfold argument for separate
calls is met another way: the Port already streams custom `ToolProgress` events, so a bundled tool can
emit one progress event per internal step and the screen can show "step 3 of 5: reachable assets"
while one tool call runs [P] `agent.py` custom stream mode; [V] LangGraph's stream writer API.

**What this means for ticket 05.** Default to the bundle for the playbook: `investigate_alert` returns
one joined package with a named section per step, each with its own verdict and citations, computed
and ordered in code; keep the narrow tools for follow-ups so a cheap question stays cheap; keep
`parallel_tool_calls` on, because the Port's policy already injects parallel `search_logins` calls and
narrow follow-ups benefit; cap the package (top five chunks per search, assets and peers paged with a
`truncated` flag) because the only measured injection defence weakens as context grows.

### 3.5 Plan-driven agents at the pinned versions (question 5)

**The middleware API, verified in `langchain` 1.3.1 as installed.**

| Element | What the source says | Status |
|---|---|---|
| Hooks | Node-style `before_agent`, `before_model`, `after_model`, `after_agent`, each `(state, runtime) -> dict | None`; wrap-style `wrap_model_call(request: ModelRequest, handler) -> ModelResponse` and `wrap_tool_call(request: ToolCallRequest, handler) -> ToolMessage | Command`. Decorators take `state_schema=`, `tools=`, `can_jump_to=`, `name=`; the class form sets `state_schema`, `tools` and uses `@hook_config(can_jump_to=...)`. | [P] `agents/middleware/types.py` lines 69 to 395 and 856 to 1261 |
| Jumps | `JumpTo = Literal["tools", "model", "end"]`; `AgentState` has `messages`, `jump_to` (ephemeral, private) and `structured_response`. `wrap_model_call` cannot `goto`: the factory raises "Command goto is not yet supported in wrap_model_call middleware. Use the jump_to state field with before_model/after_model hooks instead." | [P] `types.py` line 69, 350 to 355; `factory.py` |
| `ToolCallRequest` | Fields `tool_call` (name, args, id), `tool`, `state`, `runtime`. | [P] `langgraph/prebuilt/tool_node.py` line 133 |
| Order | `before_*` first to last, `after_*` last to first, wrap hooks nested with the first outermost. | [P] custom middleware page |
| Built-ins of interest | `ToolCallLimitMiddleware(tool_name, thread_limit, run_limit, exit_behavior)`, `ModelCallLimitMiddleware(thread_limit, run_limit, exit_behavior)`, `LLMToolSelectorMiddleware`, `ToolRetryMiddleware`, `PIIMiddleware(apply_to_tool_results=...)`, `ContextEditingMiddleware`. | [P] built-in page; `tool_call_limit.py` |
| Composition | Middleware runs inside the compiled graph; the whole agent "can be dropped into a larger `StateGraph` as a node or subgraph" for topologies that are "more than loop until done", such as classifying input before routing, or "stitching agent calls together with deterministic steps". Subgraph checkpointing is per-invocation (`None`), per-thread (`True`) or stateless (`False`). | [P] middleware overview and subgraphs pages |
| Plan-and-execute | LangGraph's tutorial pattern: state `input`, `plan: list[str]`, `past_steps`, `response`; a planner with structured output, an executor agent per step, a replanner that returns either new steps or the final response. The tutorial page now redirects and could not be opened; the pattern is confirmed through derivative notebooks. In the security literature it is the pattern with a structural guarantee against injection (section 3.3). | [V] via three derivative repositories |

**Where the plan can live, three options.**

| Option | How | Fits the rulings |
|---|---|---|
| A. Middleware on `create_agent` (the Port's shape, extended) | A `before_model` hook derives the investigation's status from the messages of the current turn, as `investigation_policy.py` does today, and injects the missing step as a tool call with `jump_to="tools"`; an `after_model` hook validates the answer and may `jump_to="model"` with a correction, bounded by a counter in a custom `state_schema`; a `wrap_tool_call` hook fences every result. | Keeps one agent factory, one tool list, the checkpointer and the streaming unchanged. The plan is code but not a graph; its order is implied by what the hook checks. |
| B. The agent as one node in a parent `StateGraph` | Deterministic nodes before and after the agent: classify the question (full versus narrow), run `investigate_alert` in code when the question names an alert, then the agent explains. | Strongest control-flow integrity, but it moves the shortcut rule out of the model's tool choice, against the author's ruling that the model translates prose into the typed call. |
| C. Plan-and-execute with planner and replanner | Two extra model calls per question. | Over-built for a plan that is fixed and known in advance; the plan is ours, not the model's. |

**The shortcut rule, expressed.** The sturdier replacement for the Port's regex test is the tool
schema itself: a call to `investigate_alert(finding_id)` *is* the decision to run the full plan, and a
call to a narrow tool is the decision not to. The policy no longer classifies prose; it reads tool
calls and tool results, which is exactly the Port's "log text never sets policy" rule. The remaining
regex-shaped risk, a broad question answered with no tool call at all, is handled by the per-turn gate
(an answer that cites nothing on a question that named an alert is sent back once).

**The report gate, implemented.** `write_report` is a separate chain over the saved messages, not an
agent turn, so the gate belongs in code before the chain runs: a core function
`playbook_status(messages) -> {finding_id: {step: done | missing}}` walks the saved tool calls and
results, the same way the Port's policy does. Because steps 2 to 6 are code-derived from the alert
record, **the gate can complete a missing step by calling the core directly, with no model call**, and
append the result to the transcript before the report is written; only when a step cannot run (store
down, alert not found) does the report say which step could not be completed and why. The same
`playbook_status` function is what ticket 06 asserts on.

**Seams for later phases without building them.** The playbook is a data structure, a list of steps
with the tool that serves each and a required-for-report flag, read by the policy, the report gate and
the eval; phase 4's attack paths add a step and a raw-neighbour tool, the GRC view adds a document type
and a section; nothing else changes. The investigation package has named sections, so a new section is
additive. Option B stays available: `create_agent` with middleware can be dropped into a parent graph
later with every hook intact, which is the documented path if a deterministic pre-step is ever wanted.

**What this means for ticket 05.** Option A, the Port's shape extended with three hooks and one custom
state field, is the recommendation: it keeps the seams, it is testable without a model (the hooks are
functions over message lists), and it is what the pinned version supports without workarounds.
`ModelCallLimitMiddleware` with a `run_limit` is the cheap guard against a correction loop.

## 4. Fit against the Port's rules

| Rule | How this note keeps it |
|---|---|
| Core independent of the screen | `investigate_alert`, `account_context`, `peers`, `search_corpus` and `playbook_status` are core functions; tools, routes and the eval call them |
| Build the seams | Tool list stays one tuple in `tools.py`; model and agent stay in `make_model` and `build_agent`; the playbook is one list; the store is handed over like the dataset is today |
| What works keeps working | The three log tools and the detection rules are unchanged; the policy for them is kept and extended, not replaced; the existing eval runs before and after |
| Read-only | New tools read the store through the read-only role; the gate completes steps by reading, never writing |
| Untrusted data | Fencing in one `wrap_tool_call`; the system prompt's rule is kept as the second lock |
| API returns only what the screen needs | The artifact stays server-side; the screen gets the citation fields it renders as plain text |

## 5. Recommendations for the grilling (one line each; the author rules)

1. Seven tools: the Port's three unchanged, `investigate_alert(finding_id)`, `lookup_account(account_id)`, `find_peers(account_id | device_id | network)`, `search_corpus(question, doc_type, technique_id)`; no router tool, no sub-agent.
2. `investigate_alert` bundles playbook steps 2 to 6 into one joined package with a named section per step, each with its own verdict and citations; progress streamed per internal step through the Port's custom stream.
3. Whether spray targets are a section of that package or a separate `expand_alert(finding_id)` tool.
4. Every tool returns `(content, artifact)`: short labelled text for the model, the full structured record with IDs, scores and verdicts for the eval and the screen.
5. Deterministic IDs because the database is rebuilt per run: chunk `<doc-slug>@<version>#<section>/<ordinal>`, entity IDs from the ground-truth files, finding `F-<rule>-<hash8>` computed from rule and content (the ticket's candidate decision; touches `rules.py` and the Alerts API).
6. Citations as short per-call labels in the answer, resolved in code against the conversation's artifacts; a label that does not resolve fails the turn.
7. Two answer checks in the eval: deterministic citation resolution on every question, LLM-judged faithfulness on a sample; gold chunk and record IDs per question.
8. Injection stance: fence and label every tool result in one `wrap_tool_call` middleware, keep the prompt rule, no datamarking or encoding, canaries in log and corpus measured as a pass rate.
9. Plan location: option A, the Port's middleware shape extended with `before_model` (add missing steps), `after_model` (validate and correct once), `wrap_tool_call` (fence), one custom state field for the correction count, `ModelCallLimitMiddleware` as the loop guard.
10. Shortcut rule: the tool schema is the classification; the policy reads tool calls, never prose.
11. Report gate: `playbook_status(messages)` in the core; missing code-derived steps are completed in code before the report is written; a step that cannot run is named in the report.
12. Caps: five chunks per search, paged assets and peers with a `truncated` flag, so a package stays well under a few thousand tokens.
13. `parallel_tool_calls` stays on.
14. The playbook as a data structure (step, tool, required-for-report), shared by policy, gate and eval, as the seam for phases 2 to 4 and the GRC view.

## 6. Evidence gaps

- The Perplexity deep-research call produced nothing; the landscape view is assembled from targeted searches and may miss a shape no primary domain documents.
- The LangGraph plan-and-execute tutorial could not be opened (redirect, then 404); its structure is taken from derivative notebooks.
- Spotlighting's per-technique figures (delimiting versus datamarking versus encoding) are from the paper body via snippets; only the abstract was opened.
- gpt-4o-mini's benchmark numbers come from papers and one aggregator, not from the BFCL leaderboard page itself; none measures a chain shaped like ours. Ticket 06 will.
- The cost table rests on stated token estimates; a real trace from the first build should replace it.
- Splunk's notable-event ID and the LangGraph stream-writer API were seen through snippets only.
- Whether `ToolMessage.artifact` survives `SqliteSaver` round-trips for our payload shape (JSON-serialisable dicts) was not tested; it is a phase-0 build check.
- No source measures fencing on gpt-4o-mini with our prompt; the canary pass rate is the only evidence that will count.

## Sources

Primary, opened in this research:

- Installed packages: `langchain` 1.3.1 `agents/middleware/types.py`, `agents/factory.py`,
  `agents/middleware/tool_call_limit.py`; `langgraph-prebuilt` 1.1.0 `prebuilt/tool_node.py`;
  `langchain-core` 1.4.0 `messages/tool.py`; `backend/uv.lock`.
- LangChain docs: custom middleware; built-in middleware; middleware overview; tools (ToolRuntime);
  subgraphs; `langchain_core` tool reference (`response_format`). LangSmith: evaluate a RAG application.
- Neo4j: `neo4j-graphrag-python` user guide (retrievers, GraphRAG class).
- Microsoft GraphRAG: query overview, local search page, `local_search_system_prompt.py`.
- OpenAI: function calling guide; citation formatting guide; o3/o4-mini function-calling guide.
- Anthropic: "Writing effective tools for agents"; Claude platform docs, search results and citations.
- OWASP Gen AI Security Project: LLM01:2025 Prompt Injection.
- arXiv abstracts: 2302.12173 (Greshake et al.), 2403.14720 (Hines et al.), 2406.13352 (AgentDojo),
  2506.08837 (design patterns), 2510.09023 (adaptive attacks), 2607.14493 (log contamination, abstract
  and HTML body).
- Simon Willison, "The lethal trifecta for AI agents" (16 June 2025).
- OpenRouter: `GET /api/v1/models/openai/gpt-4o-mini/endpoints`.
- Elastic: Kibana `security_solution` `rule_types/utils/utils.ts` (`generateId`); troubleshoot
  detection rules. SigmaHQ: rules basics (ID field).
- RAGAS: faithfulness (stable).

Research-pass and secondary (snippets only):

- Neo4j Labs LangChain agents page; `ToolsRetriever` source. Microsoft Research DRIFT post.
- LangChain agentic-RAG tutorial; plan-and-execute pattern via three derivative repositories.
- OpenAI programmatic tool calling guide. Anthropic "Building effective agents", context engineering.
- DeepEval faithfulness. Splunk ES notable events. Willison, dual-LLM pattern and design-patterns post.
- arXiv 2501.05255 (CallNavi), 2508.05118, 2509.25926; whatmodel aggregator for BFCL v3.
