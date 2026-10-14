# How the agent stream reaches the browser

Type: research
Status: resolved
Blocked by: none
Map: [map.md](../map.md)

## Question

The core already streams. `agent.ask()` yields pieces of kind `text` (a piece of the answer) or
`tool` (a tool starting). What is open is only the transport from a FastAPI endpoint to a React page.

Compare, from primary sources (FastAPI, Starlette, MDN, React or the chosen framework's docs):

- Server-Sent Events (`StreamingResponse` with `text/event-stream`).
- WebSockets.
- A plain chunked HTTP response read with `fetch` and a `ReadableStream`.

For each record: how FastAPI produces it, how the browser consumes it, how a tool-start event and a
text piece travel in the same stream, how an error mid-stream reaches the page, whether the
Investigation ID travels in the URL or the body, and what happens when the user closes the tab
mid-answer. Note which option the LangChain docs show for serving an agent over HTTP, if any.

Give a recommendation with a reason. Save findings to `research/06-agent-stream.md`. The answer is
an input to [The API contract](09-api-contract.md).

## Comments

## Answer

Recommendation: Server-Sent Events over `POST`, produced with FastAPI's `EventSourceResponse`
(FastAPI 0.135 or later), read in the browser with `fetch` plus a `ReadableStream` reader, and stopped
with an `AbortController` in the React effect cleanup. The built-in `EventSource` class is not used:
it is `GET` only, carries no body, and reconnects on its own after every finished answer.

Reason: the stream is one-way, so SSE fits and FastAPI can type and document the events in OpenAPI like
any other endpoint. WebSockets add two-way traffic we do not need and lose request validation, Pydantic
typing and HTTP error codes. A plain chunked response works but means inventing our own framing.
LangChain's own hosted server makes the same choice (`POST /threads/{id}/runs/stream`, SSE by default).

Shape for the contract: `POST /investigations/{id}/ask` with `{"question": ...}`; events `text`,
`tool`, `error`, `done`; failures before the first byte are normal 404 or 422 responses. v1's sync
`ask()` generator is handed to the route as-is; Starlette runs it in a threadpool and stops advancing
it when the tab closes.

Full findings with sources: [research/06-agent-stream.md](../research/06-agent-stream.md).
