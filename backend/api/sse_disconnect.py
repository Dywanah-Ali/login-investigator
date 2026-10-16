"""Temporary B-014 guard for FastAPI's SSE queue teardown, installed on the ask route only.

Upstream: https://github.com/fastapi/fastapi/discussions/15725
Remove after an upstream release passes our strict disconnect regression without this guard.
Unknown origins fail visibly, including after a future FastAPI internal rename.
"""

from anyio import BrokenResourceError, ClosedResourceError
from fastapi.routing import APIRoute
from starlette.types import Message, Receive, Scope, Send


def _from_keepalive(error: BaseException) -> bool:
    """Match the known framework origin, never exception text or client-supplied data."""
    if not isinstance(error, (BrokenResourceError, ClosedResourceError)):
        return False
    trace = error.__traceback__
    while trace is not None:
        frame = trace.tb_frame
        if (frame.f_globals.get("__name__") == "fastapi.routing"
                and frame.f_code.co_name == "_keepalive_inserter"):
            return True
        trace = trace.tb_next
    return False


class DisconnectSafeRoute(APIRoute):
    """Handle known queue closure only after a successful stream and observed disconnect.

    Wrap the full ASGI route lifetime: request cleanup runs after the endpoint has returned.
    Unexpected errors, including siblings in an exception group, keep propagating normally.
    """

    async def handle(self, scope: Scope, receive: Receive, send: Send) -> None:
        disconnected = False
        streaming = False

        async def observed_receive() -> Message:
            nonlocal disconnected
            message = await receive()
            if message["type"] == "http.disconnect":
                disconnected = True
            return message

        async def observed_send(message: Message) -> None:
            nonlocal streaming
            if message["type"] == "http.response.start":
                headers = dict(message.get("headers", []))
                streaming = (message["status"] == 200 and
                             headers.get(b"content-type", b"").split(b";")[0] == b"text/event-stream")
            await send(message)

        try:
            await super().handle(scope, observed_receive, observed_send)
        except* (BrokenResourceError, ClosedResourceError) as group:
            if not (disconnected and streaming):
                raise
            _, unexpected = group.split(_from_keepalive)
            if unexpected is not None:
                raise unexpected
