# Research: how the agent stream reaches the browser

Ticket: [06-agent-stream](../issues/06-agent-stream.md). Researched 14 October 2026 against primary
sources (FastAPI docs, Starlette source, MDN, WHATWG HTML spec, React docs, LangChain docs). Feeds
[The API contract](../issues/09-api-contract.md).

## What the core already gives us

`agent.ask(agent, thread_id, question)` in v1 is a **synchronous generator**. It wraps
`agent.stream(..., stream_mode="messages")` and yields `Stream(kind, value)` where `kind` is `"text"`
(a piece of the answer) or `"tool"` (the name of a tool starting). Tool results are not streamed; they
are read from memory afterwards. The thread ID is passed in as `thread_id`. Source:
`login_investigator/agent.py`, `class Stream` and `def ask` (read only, not changed).

Two facts about this shape matter for the transport:

1. Both kinds already travel in one ordered stream. The transport only has to carry a small typed
   message, so a JSON object per piece such as `{"kind": "tool", "value": "search_logins"}` works for
   every option below.
2. It is sync. Whatever transport we pick, FastAPI has to run it off the event loop.

## Recommendation

**Server-Sent Events over `POST`, produced by FastAPI's `EventSourceResponse`, consumed in the browser
with `fetch` plus a `ReadableStream` reader (not the `EventSource` class), stopped with an
`AbortController` in a React effect cleanup.**

Reason, in one paragraph: the stream is one-way (question in, pieces out), which is exactly what SSE
is for, and FastAPI 0.135+ has first-class support with Pydantic-typed events, so the API contract can
declare the event shape in OpenAPI like any other endpoint. WebSockets give two-way traffic we do not
need and lose FastAPI's request validation, Pydantic response typing and plain HTTP error codes. A bare
chunked response works but forces us to invent a framing format; SSE's `event:`/`data:` framing is a
standard that already distinguishes a `tool` event from a `text` event and an `error` event. The one
catch with SSE is that the browser's built-in `EventSource` is `GET` only with no body, so the browser
reads the SSE text through `fetch` instead; that costs about twenty lines of parsing (or a small
library) and keeps the question in a `POST` body, where it belongs. LangChain's own hosted server uses
the same design: `POST /threads/{thread_id}/runs/stream` with SSE as the default wire transport.

## The three options compared

### 1. Server-Sent Events (`text/event-stream`)

**How FastAPI produces it.** "To stream SSE with FastAPI, use `yield` in your path operation function
and set `response_class=EventSourceResponse`." Import from `fastapi.sse`. "If you declare the return
type as `AsyncIterable[Item]`, FastAPI will use it to validate, document, and serialize the data using
Pydantic." Sync generators are allowed: "You can also use regular `def` functions (without `async`),
and use `yield` the same way. FastAPI will make sure it's run correctly so that it doesn't block the
event loop" with return type `Iterable[Item]`. To set SSE fields, "you can yield `ServerSentEvent`
objects instead of plain data" with `event`, `id`, `retry`, `comment`; `data` is "always encoded as
JSON", `raw_data` sends text unencoded. "SSE works with any HTTP method, not just GET" and the docs
show a `POST /chat/stream` example. FastAPI sets `Cache-Control: no-cache` and `X-Accel-Buffering: no`
and sends "a 'keep alive' ping comment every 15 seconds when there hasn't been any message". "Added in
FastAPI 0.135.0." Current release on PyPI is 0.143.0.
Source: https://fastapi.tiangolo.com/tutorial/server-sent-events/ and
https://fastapi.tiangolo.com/reference/sse/ (`EventSourceResponse` "Bases: StreamingResponse",
`media_type = 'text/event-stream'`).

**Wire format** (WHATWG HTML spec, "Server-sent events", and MDN "Using server-sent events"): UTF-8
text, messages separated by a blank line, lines of `field: value`. Recognised fields are `event`,
`data`, `id`, `retry`; "all other field names are ignored"; a line starting with a colon is a comment.
Consecutive `data:` lines are joined with newlines. Messages without `event` arrive as `message`
events; with `event` they arrive under that name.
Sources: https://html.spec.whatwg.org/multipage/server-sent-events.html,
https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events

**How the browser consumes it.** Two routes.

- `EventSource`: native, but the spec builds its request from the URL alone, so it is a `GET` with
  no request body and no custom headers; the only option is `withCredentials`. It reconnects on its
  own: "Clients will reconnect if the connection is closed", and "once the user agent has failed the
  connection, it does not attempt to reconnect", where failing means a non-200 status or a
  Content-Type other than `text/event-stream`. On reconnect it sends `Last-Event-ID`. For a chat
  turn this auto-reconnect is a liability: a finished answer would re-trigger the request unless the
  server answers the retry with 204. MDN also notes a limit of 6 open connections per browser and
  domain over HTTP/1.
  Sources: https://developer.mozilla.org/en-US/docs/Web/API/EventSource, WHATWG spec above.
- `fetch` + `ReadableStream`: `response.body.getReader()` then `read()` in a loop; each result is
  `{ value, done: false }` or `{ value: undefined, done: true }`; `response.body` is also an async
  iterable (`for await (const chunk of response.body)`). Bytes are decoded with
  `TextDecoder.decode(value, { stream: true })`, where `stream: true` means "additional data will
  follow in subsequent calls"; the decoder holds a partial multi-byte character across chunks. The
  page splits the text on blank lines and parses `event:` and `data:` itself. Nothing reconnects
  unless we write it, which is what we want for a one-shot answer. A `POST` with a JSON body is
  allowed.
  Sources: https://developer.mozilla.org/en-US/docs/Web/API/Streams_API/Using_readable_streams,
  https://developer.mozilla.org/en-US/docs/Web/API/TextDecoder/decode

**Tool-start and text in one stream.** Named events: `event: tool` with `data: {"name": "..."}`, and
`event: text` with `data: {"text": "..."}` (or one event type with `kind` inside the JSON). Both are
one ordered stream, matching the generator's order. With `EventSourceResponse` each is a
`ServerSentEvent(event=..., data=model)`.

**Error mid-stream.** Once streaming starts the HTTP status is already 200, so a Python exception
cannot become a 500. The answer is an `event: error` with a JSON body as the last event, then the
generator ends; the page shows the error and stops. The FastAPI SSE docs do not cover this; it follows
from the HTTP facts above. An error *before* the first byte (bad investigation ID, missing key) is an
ordinary `HTTPException` with a 404 or 422, since no body has been sent yet. The MDN `EventSource`
error event only fires for connection failures, another reason the page should read the stream itself.

**Investigation ID: URL or body.** Both work with `POST`. The REST-shaped choice is the ID in the path
and the question in the body: `POST /investigations/{id}/ask` with `{"question": "..."}`. This is the
same shape as LangChain's server (`POST /threads/{thread_id}/runs/stream`). If the `EventSource` class
were used instead, everything would have to go in the query string, a further point against it.

**Closing the tab mid-answer.** Starlette's `StreamingResponse.__call__` runs `stream_response` and
`listen_for_disconnect` in one task group; when the ASGI server delivers `http.disconnect` the listener
returns and `task_group.cancel_scope.cancel()` stops the streaming task. A sync generator is wrapped by
`iterate_in_threadpool`, which does `yield await anyio.to_thread.run_sync(_next, as_iterator)` per
item, so the `await` between items is where cancellation lands: the current `next()` finishes in its
worker thread, and the generator is simply never advanced again. FastAPI warns: "An async task can
only be cancelled when it reaches an await. If there is no await, the generator ... may keep running
even after cancellation is requested." `request.is_disconnected()` exists for an explicit check
("In some cases such as long-polling, or streaming responses you might need to determine if the
client has dropped the connection"). On the browser side, "when `abort()` is called, the `fetch()`
promise rejects with a `DOMException` named `AbortError`", and React's effect cleanup is the place to
call it: "After your component is removed from the DOM, React will run your cleanup function", and in
Strict Mode React "will run one extra development-only setup+cleanup cycle", so the cleanup must
really abort. Consequence to record in the contract (my inference from how LangGraph checkpoints
after a node finishes, not a quoted fact): an abandoned turn is not written to the investigation's
memory because the model node never completed, so the user will not see a half answer in the history.
Sources: https://raw.githubusercontent.com/encode/starlette/master/starlette/responses.py,
https://raw.githubusercontent.com/encode/starlette/master/starlette/concurrency.py,
https://raw.githubusercontent.com/encode/starlette/master/docs/requests.md,
https://fastapi.tiangolo.com/advanced/custom-response/,
https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal,
https://react.dev/reference/react/useEffect

### 2. WebSockets

**How FastAPI produces it.** `@app.websocket("/ws")`, `await websocket.accept()`, then a loop of
`receive_text()` / `send_text()`; "you can receive and send binary, text, and JSON data". Path and
query parameters, `Depends`, `Cookie`, `Header`, `Query` work "the same way as for other FastAPI
endpoints". Errors are signalled by raising `WebSocketException(code=...)` with a close code, since
"it doesn't really make sense to raise an HTTPException".
Source: https://fastapi.tiangolo.com/advanced/websockets/

**How the browser consumes it.** `new WebSocket(url)` with `ws://` or `wss://`; the constructor takes
only a URL and optional sub-protocols, so no custom headers or body. Messages via `send()` and the
`message` event, typically JSON. "If an error occurs ... the error event will be fired. On an error,
the connection is closed and the close event will be fired." No automatic reconnection; MDN shows
reconnecting by hand and recommends closing on `pagehide`.
Source: https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/Writing_WebSocket_client_applications

**Tool and text in one stream.** Easy: one JSON message per piece with a `kind` field.

**Error mid-stream.** Send a JSON error message, or close with a code. There is no HTTP status at
all after the handshake, so the frontend needs its own error vocabulary.

**Investigation ID.** Path or query parameter on the socket URL (the docs' example is
`/items/{item_id}/ws?token=...`). The question is a message on the open socket.

**Closing the tab.** "When a WebSocket connection is closed, the `await websocket.receive_text()`
will raise a `WebSocketDisconnect` exception." But the server only notices while awaiting a receive;
while it is busy sending pieces from a sync generator it must check `websocket.client_state` or send
and catch the failure. More code, same outcome as SSE.

**Why not.** Two-way traffic is not needed; each question is one request and one answer. Pydantic
response typing and OpenAPI documentation of the stream are lost, which cuts against "every endpoint
has a written input and output shape". It adds a second protocol to proxy, test and secure. FastAPI's
own docs push the browser demo as not for production and offer no React guidance.

### 3. Plain chunked HTTP (`StreamingResponse`, or JSON Lines)

**How FastAPI produces it.** `response_class=StreamingResponse` with `yield`; "FastAPI will give each
chunk of data to the StreamingResponse as is, it won't try to convert it to JSON". For structured
data FastAPI offers JSON Lines (0.134+): yield Pydantic models from a path operation typed
`AsyncIterable[Item]` or `Iterable[Item]`, one JSON object per line, content type `application/jsonl`.
The docs say SSE "is quite similar but with a couple of extra details" and point to it as the
browser-native format.
Sources: https://fastapi.tiangolo.com/advanced/stream-data/,
https://fastapi.tiangolo.com/tutorial/stream-json-lines/

**How the browser consumes it.** Same `fetch` + reader + `TextDecoder` loop as SSE, splitting on
newlines instead of blank lines. Chunk boundaries do not match line boundaries, so the page keeps a
buffer of the unfinished tail.

**Tool and text in one stream.** One JSON object per line with `kind`.

**Error mid-stream.** Same as SSE: a final line `{"kind": "error", ...}` by convention, since the
status is already 200.

**Investigation ID and tab closing.** Identical to SSE; same Starlette machinery.

**Why not.** It is SSE without the standard framing and without the `event:` field, keep-alive
comments and `X-Accel-Buffering` header FastAPI adds for free. JSON Lines is the honest alternative if
the SSE parsing on the page feels like too much; the server code is nearly the same, so switching
later is cheap.

## What LangChain shows for serving an agent over HTTP

The LangChain OSS docs cover `stream` and `astream` with `stream_mode="messages"` (what v1 uses) but
do not show an HTTP server; they leave that to the hosted LangSmith Deployment / Agent Server. That
server's API is `POST /threads/{thread_id}/runs/stream`, resumable with a `Last-Event-ID` header, and
the JavaScript SDK reference states: "The wire transport defaults to SSE; pass `transport:
"websocket"` ... to use a WebSocket instead." So LangChain's own choice is SSE over `POST` with the
thread ID in the path, which is the recommendation here. Using LangGraph Server itself is out of
scope: v2's backend is our FastAPI app.
Sources: https://docs.langchain.com/oss/python/langgraph/streaming,
https://docs.langchain.com/langsmith/streaming,
https://reference.langchain.com/javascript/langchain-langgraph-sdk/client/ThreadsClient/stream

## Inputs for the API contract (ticket 09)

- `POST /investigations/{id}/ask`, body `{"question": str}`, response `text/event-stream`.
- Events: `text` (`{"text": str}`), `tool` (`{"name": str}`), `error` (`{"detail": str}`), and a
  final `done` event so the page knows the answer finished rather than the connection dropped.
- Pre-stream failures are normal HTTP errors (404 unknown investigation, 422 bad body).
- The route hands `agent.ask(...)` (sync) straight to the `EventSourceResponse` path operation as a
  `def` generator; FastAPI runs it in the threadpool. The route maps `Stream.kind` to the event name,
  nothing more, which keeps the core free of FastAPI.
- The frontend uses `fetch` with an `AbortController` whose `abort()` is called in the effect
  cleanup; it never uses `EventSource`.
- Agent text is rendered with links and images off (existing security rule); the event payload is
  untrusted data.
- Needs FastAPI 0.135 or later for `EventSourceResponse`.

## Open points noticed, not decided here

- Whether to parse SSE by hand (small, no dependency) or use a tiny client library. A decision for the
  frontend template ticket.
- Whether the answer should also be saved as it streams so a refresh mid-answer shows partial text.
  v1 does not do this, so parity says no.
