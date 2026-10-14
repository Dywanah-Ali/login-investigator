# Do the course rules bind v2

Type: grilling
Status: resolved
Blocked by: none
Map: [map.md](../map.md)

## Question

v1 was built under the course rule "LangChain only as taught in class, no custom LangGraph graphs"
(v1 `CLAUDE.md` lines 32-35; v1 `docs/PRD.md` lines 79, 105, 322). v2 is the base for later course
weeks that will add RAG, a knowledge graph, tracing and eval platforms.

Decide:

1. Does the "only as taught" rule still bind v2, in full, in part, or not at all?
2. If it binds, what does it allow for the pieces v2 must add: streaming the agent over an API,
   keeping the agent alive across requests, and a checkpointer shared by a server process?
3. Does the rule change as later weeks teach more, and who records that change (the PRD decisions
   log is the candidate)?

The answer sets the boundary for [How the agent stream reaches the browser](06-agent-stream.md) and
[The API contract](09-api-contract.md).

## Comments

### 14 October 2026, grilling with the author

**Facts found first.** v1 uses six LangChain pieces: prompt templates, `init_chat_model`, `@tool`,
`create_agent`, structured output and `SqliteSaver`. Streaming already runs through the taught
`agent.stream(..., stream_mode="messages")` call. v2 needs nothing new from LangChain. The three
things v2 adds (a web transport for the stream, one agent living for the server's lifetime, one
memory file shared by the server process) are plain Python and FastAPI.

**The author's ruling.** The course rule does not bind v2 at all. v2 is not under the "only as
taught" constraint.

**The design choice, made anyway.** For the Port, v2 keeps the agent exactly as v1 builds it: the
same six pieces, no hand-built LangGraph graph. Reasons: Parity is the acceptance gate and the
agent is already proven; a hand-built graph would add code and a second mental model while
changing nothing the user sees; the agent and model are created in one function, so moving to a
graph later is a one-place change. LangGraph is not banned in v2. It is simply not needed yet.

## Decision

1. The rule does not bind v2. The agent stays as in v1 by choice, not by rule.
2. The transport, the server-lifetime agent and the shared checkpointer are plain Python and
   FastAPI work, built freely.
3. Any later move away from the v1 agent build (a custom graph, a new agent library feature) is a
   PRD change: proposed to the author, then a row in the PRD decisions log naming the week or
   reason.

Boundary for [The API contract](09-api-contract.md) and
[How the agent stream reaches the browser](06-agent-stream.md): no LangChain constraint applies.
