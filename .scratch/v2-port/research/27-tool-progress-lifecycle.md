# Research: real tool execution progress in LangChain

Researched 19 October 2026 for ticket 19. Research only. No application or API-contract change is approved by this note.

## Finding

Show progress from execution events, rather than from the model's request to execute. LangChain already supplies this distinction. The current `ask()` reads model message chunks and extracts tool names. It therefore observes requests, despite the `Stream` docstring describing a tool starting. Source: [current adapter](../../../backend/login_investigator/agent.py), `ask()` and `Stream`.

The official Python event-streaming guide explicitly separates `message.tool_calls`, which describes argument generation, from `stream.tool_calls`, which describes execution. Its public `stream_events(..., version="v3")` interface supports synchronous consumption and raw protocol events as well as typed projections. [Official event-streaming guide](https://docs.langchain.com/oss/python/langchain/event-streaming).

## Version checks

The installed environment reports LangChain 1.3.1, langchain-core 1.4.0 and LangGraph 1.2.4 in package metadata under `backend/.venv/lib/python3.12/site-packages/`. These are source observations, not an assumption that today's examples match our version.

| Mechanism | Installed-source finding | Suitability |
| --- | --- | --- |
| `messages` | Model chunks include tool-call names and arguments. | Keep for answer text; requests do not prove execution. |
| `updates` | State updates occur after node completion. | Useful for results; not per-tool start tracking. |
| `custom` | Supports arbitrary signals through the graph stream writer. | Stable adaptation option if native lifecycle streaming is unsuitable. |
| `tools` | Runtime implemented in `Pregel.stream` and `astream`, but omitted from `types.StreamMode`. | Real lifecycle exists; direct low-level use has a typing/documentation mismatch. |
| `stream_events(version="v3")` | Implemented by installed Pregel; installed `create_agent` registers `ToolCallTransformer`. | Public native lifecycle interface, but installed docstring labels v3 experimental. |
| Callback handlers | `BaseTool.run/arun` emit start and end/error callbacks. | Alternative requiring transport into the existing synchronous generator. |
| `astream_events(version="v2")` | Async event dictionaries include tool lifecycle and model events. | Established alternative, but requires an async integration change. |

Sources for these local implementation findings: installed `langgraph/types.py:120`, `langgraph/pregel/main.py:2801`, `:3229`, `:3586`, `langgraph/pregel/_tools.py`, `langgraph/prebuilt/_tool_call_transformer.py`, `langchain/agents/factory.py:1678`, `langchain_core/tools/base.py:942`, `:1000`, `:1003`, and `langchain_core/runnables/base.py:1280`. Upstream primary-source references: [LangGraph 1.2.4 Pregel](https://raw.githubusercontent.com/langchain-ai/langgraph/refs/tags/1.2.4/libs/langgraph/langgraph/pregel/main.py), [langchain-core 1.4.0 tool execution](https://github.com/langchain-ai/langchain/blob/langchain-core%3D%3D1.4.0/libs/core/langchain_core/tools/base.py).

An important version boundary: the current official guide says middleware-registered stream transformers require LangChain 1.3.2. Our installed 1.3.1 already registers the built-in tool transformer inside `create_agent`; it must not be assumed to support that newer middleware-registration feature. [Official version requirement](https://docs.langchain.com/oss/python/langchain/event-streaming#register-transformers-on-middleware).

## What execution tracking gives us

Installed `StreamToolCallHandler` emits `tool-started`, `tool-finished` and `tool-error`, correlated by `tool_call_id`. Start includes the tool name. Finish includes output. Error includes an error message. Internally it correlates callbacks by `run_id`, since end callbacks do not receive the tool-call identifier directly. This is already framework behavior; a custom correlation layer is unnecessary when consuming native events. Source: installed `langgraph/pregel/_tools.py`, `StreamToolCallHandler`.

Track an active set by call identifier, not tool name. Parallel calls may execute the same tool twice. Installed `ToolNode._func()` executes tools through an executor, so a single last-seen name is insufficient. A finishing call removes only itself. Sources: installed `langgraph/prebuilt/tool_node.py:823` and `_tools.py`.

The standard callbacks surround invocation, including validation. A propagated tool exception triggers `on_tool_error`. A handled error can instead produce a terminal `ToolMessage` with error status through `on_tool_end`. Either terminal event must clear active progress. A tool function that returns an error-shaped string still completes from the framework's perspective. Source: installed `langchain_core/tools/base.py:942-1004`.

## Alternatives and recommendation

The main agent independently verified low-level combined `messages`/`tools` offline against the installed dependencies using two barrier-controlled parallel tools. It emitted start/start/end/end events with distinct identifiers, final text, and five saved messages. The main agent also verified a public callback handler using `run_inline=True` and `get_stream_writer()` with combined `messages`/`custom`. That path delivered the same lifecycle without changing tool bodies. Evidence scripts: `/private/tmp/li-tool-lifecycle-probe.py` and `/private/tmp/li-tool-callback-probe.py`. These are temporary research artifacts, not repository acceptance tests.

Recommendation: retain synchronous `agent.stream`, combine `messages` and `custom`, and use one per-invocation public callback handler to write small lifecycle signals through the graph writer. This uses the framework's execution callbacks, avoids the raw `tools` typing gap and avoids adopting an experimental streaming protocol for a narrow fix. The callback must be inline so it runs in the graph context. Only start/end/error signals belong in the custom payload. [Callback API](https://reference.langchain.com/python/langchain-core/callbacks/base/BaseCallbackHandler), [custom streaming](https://docs.langchain.com/oss/python/langchain/streaming#custom-updates).

The callback-to-writer combination is an integration recommendation supported by the offline probe. The two linked public APIs are documented independently; the documentation reviewed does not promise that exact combination across every future version. A separate offline error probe emitted start/error for a controlled `RuntimeError`, propagated that exception, and emitted start/end for another successful tool. No final answer was emitted. The checkpoint retained three pre-error messages. Evidence: `/private/tmp/li-tool-callback-error-probe.py`. Cancellation and the real model/provider were not tested.

Native v3 remains a legitimate broader streaming option. It does not require a dependency upgrade or changing the three tools, but should have its experimental status explicitly accepted and its token-stream behavior verified before adoption. Raw lifecycle events support active-set updates. Iterating each tool handle until completion in sequence would obscure overlapping progress. A middleware `wrap_tool_call` wrapper is another option if execution policy is later centralized there. [Custom middleware](https://docs.langchain.com/oss/python/langchain/middleware/custom).

Keep callback state per invocation. A shared mutable active set on a reused agent would risk mixing investigations. This is an integration inference from the synchronous generator and parallel execution, not a LangChain prohibition.

Keep the existing checkpointer and `thread_id`. Streaming does not replace conversation memory. The official guide demonstrates checkpoint configuration alongside streaming and states that the thread identifier is independent of stream mode. [Streaming and checkpoint configuration](https://docs.langchain.com/oss/python/langchain/streaming#agent-progress).

## Limits and acceptance evidence needed

- Lifecycle events improve truthfulness. They cannot guarantee that every millisecond-scale cached call is readable in the browser without retaining or delaying it.
- Keep one current status. For multiple active calls, use one combined label or an honest generic plural label. Do not show completed tools as still running.
- On tool completion, return to a neutral composing status while waiting for model text. On completion, error or disconnect, clear transient state.
- Expose only allowlisted tool names and opaque call identifiers. Framework inputs, outputs and raw errors must not be forwarded merely because the event contains them.
- Offline integration evidence should cover actual start versus request time, parallel calls, duplicate tool names, handled and propagated errors, first text, checkpoint continuation and stream cleanup. Browser evidence must still confirm the final presentation.

No provider latency, cached lookup duration or the user's exact missing-label timing was measured by this research.


## Follow-up local timing evidence, 19 October 2026

After P-086 implementation, P-087 live review reports mostly Thinking and unreadable flashes.
A separate process warmed the default synthetic log/findings, blocked reputation `_fetch`, then
invoked each production tool five times with no model. Detection used the overnight window,
search used 185.218.86.24 and reputation used its saved response. Timing includes tool.invoke:

| Tool | Median | Range |
| --- | --- | --- |
| Detection | 4.07 ms | 3.70–7.05 ms |
| Search | 13.33 ms | 12.92–13.55 ms |
| Saved reputation | 0.82 ms | 0.77–1.05 ms |

These are isolated warmed-process timings, not a capture of the live provider/browser sequence.
The frontend returns to Thinking as soon as no calls remain, explaining why long model waits
can dominate the visible experience. Proposed but not yet approved: retain the last finished
activity in past tense in that same line until the next tool or first answer text. No app edit,
forced dwell, cumulative activity list or live model call during this follow-up.
