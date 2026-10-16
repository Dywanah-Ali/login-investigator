"""B-014 guard through ASGI, including failures it must never hide."""

import anyio
import pytest
from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.sse import EventSourceResponse

from api import errors
from api.sse_disconnect import DisconnectSafeRoute


def scope(path):
    return {"type": "http", "asgi": {"version": "3.0", "spec_version": "2.0"},
            "method": "GET", "path": path, "raw_path": path.encode(), "query_string": b"",
            "root_path": "", "scheme": "http", "http_version": "1.1", "headers": [],
            "client": ("testclient", 1234), "server": ("testserver", 80)}


@pytest.fixture(scope="module")
def upstream_error():
    """Get a genuine FastAPI traceback via its unguarded SSE route, without fabricating frames.

    When upstream fixes this, the fixture stops reproducing the bug. Remove the compatibility
    guard then and retain the strict real Investigation disconnect test.
    """
    async def reproduce():
        app = FastAPI()
        disconnected, buffered = anyio.Event(), anyio.Event()

        @app.get("/raw", response_class=EventSourceResponse)
        async def stream():
            for i in range(1000):
                if i >= 4:
                    buffered.set()
                yield {"text": "piece"}

        async def receive():
            await disconnected.wait()
            return {"type": "http.disconnect"}

        async def send(message):
            if message["type"] == "http.response.body":
                await buffered.wait()
                disconnected.set()
                await anyio.sleep(0)

        with anyio.fail_after(5), pytest.raises(ExceptionGroup) as failure:
            await app(scope("/raw"), receive, send)
        broken = failure.value.subgroup(anyio.BrokenResourceError)
        assert broken is not None
        return broken

    return anyio.run(reproduce)


@pytest.mark.parametrize("scenario", [
    "before_disconnect", "before_response", "json_response", "error_status",
    "other_resource_origin", "closed_resource_origin", "mixed_failures", "mixed_resource_failures",
])
def test_guard_preserves_unexpected_failures(upstream_error, scenario, caplog):
    failure = upstream_error
    if scenario == "other_resource_origin":
        failure = anyio.BrokenResourceError("application resource failed")
    elif scenario == "closed_resource_origin":
        failure = anyio.ClosedResourceError("application resource failed")
    elif scenario == "mixed_failures":
        failure = ExceptionGroup("mixed", [upstream_error, RuntimeError("genuine failure")])
    elif scenario == "mixed_resource_failures":
        failure = ExceptionGroup("mixed", [upstream_error, anyio.BrokenResourceError("application resource failed")])

    class FailingDelivery(Response):
        async def __call__(self, request_scope, receive, send):
            if scenario != "before_response":
                await send({"type": "http.response.start",
                            "status": 503 if scenario == "error_status" else 200,
                            "headers": [(b"content-type", b"application/json" if scenario == "json_response"
                                         else b"text/event-stream; charset=utf-8")]})
            if scenario != "before_disconnect":
                assert (await receive())["type"] == "http.disconnect"
            raise failure

    app = FastAPI()
    errors.install(app)

    def endpoint():
        return FailingDelivery()

    app.router.add_api_route("/guarded", endpoint, route_class_override=DisconnectSafeRoute)

    async def run_request():
        sent = []

        async def receive():
            return {"type": "http.disconnect"}

        async def send(message):
            sent.append(message)

        with pytest.raises(ExceptionGroup) as raised:
            await app(scope("/guarded"), receive, send)
        if scenario == "mixed_failures":
            assert raised.value.subgroup(RuntimeError) is not None
            assert raised.value.subgroup(anyio.BrokenResourceError) is None
        elif scenario == "closed_resource_origin":
            assert raised.value.subgroup(anyio.ClosedResourceError) is not None
        else:
            assert raised.value.subgroup(anyio.BrokenResourceError) is not None
        assert "genuine failure" not in str(sent)
        assert "application resource failed" not in str(sent)

    anyio.run(run_request)
    assert any(record.levelname == "ERROR" for record in caplog.records)
