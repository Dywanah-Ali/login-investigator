"""Drive the real HTTP transport in isolated memory, without live reputation lookups."""

from __future__ import annotations

import os
import socket
import subprocess
import sys
import tempfile
import time
from collections.abc import Iterator
from contextlib import AbstractContextManager, contextmanager
from pathlib import Path
from typing import Any, Protocol

import httpx

from login_investigator import agent, reputation

REPORT_TURN = "REPORT"


class HttpClient(Protocol):
    """The HTTP operations shared by HTTPX and Starlette's HTTPX2-based test client."""

    def post(self, url: str, *, json: dict) -> Any: ...
    def get(self, url: str) -> Any: ...
    def stream(self, method: str, url: str, *, json: dict) -> AbstractContextManager[Any]: ...


def conversation(client: HttpClient, questions: list[str]) -> list[agent.Turn]:
    """Create, ask, drain each stream, then reopen through the contract's endpoints only."""
    response = client.post("/api/investigations", json={"question": questions[0]})
    response.raise_for_status()
    path = f"/api/investigations/{response.json()['id']}"
    for question in questions:
        if question == REPORT_TURN:
            response = client.post(path + "/report", json={"request": agent.REPORT_REQUEST})
            response.raise_for_status()
        else:
            with client.stream("POST", path + "/ask", json={"question": question}) as stream:
                stream.raise_for_status()
                if not stream.headers.get("content-type", "").startswith("text/event-stream"):
                    raise RuntimeError("The ask endpoint did not return an event stream.")
                done, failed = False, False
                event = ""
                # httpx assembles UTF-8 lines across network chunks and normalizes CRLF.
                # Only terminal event names affect completion; text/tool payloads are read
                # from saved history below, exactly as the browser does.
                for line in stream.iter_lines():
                    if line.startswith("event:"):
                        event = line.partition(":")[2].strip()
                    elif not line:
                        done |= event == "done"
                        failed |= event == "error"
                        event = ""
                if failed or not done:
                    raise RuntimeError("The agent stream failed or ended without done.")
    response = client.get(path)
    response.raise_for_status()
    turns = response.json()["turns"]
    if len(turns) != len(questions):
        raise RuntimeError("The reopened Investigation is missing completed turns.")
    return [agent.Turn(
        question=turn["question"], answer=turn["answer"],
        tools=[agent.ToolUse(name=tool["name"], args=tool["args"], result=tool["raw"])
               for tool in turn["tools"]],
        report=agent.IncidentReport.model_validate(turn["report"]) if turn["report"] else None,
    ) for turn in turns]


@contextmanager
def serve() -> Iterator[httpx.Client]:
    """Start one local API server, then stop it and remove its memory even on failure.

    The caller loads .env once, before removing the reputation key. Disabling dotenv in the
    child stops make_model from restoring that key. Hold the socket until the child inherits
    it, rather than releasing a free port for another process to take.
    """
    environ = dict(os.environ)
    environ.pop(reputation.KEY_NAME, None)
    environ["PYTHON_DOTENV_DISABLED"] = "1"
    with tempfile.TemporaryDirectory(prefix="li-eval-") as folder, socket.socket() as sock:
        environ["LI_MEMORY_PATH"] = str(Path(folder) / "memory.sqlite")
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
        sock.listen()
        process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "api.app:create_app", "--factory",
             "--fd", str(sock.fileno()), "--no-access-log", "--log-level", "critical"],
            cwd=Path(__file__).resolve().parent.parent, env=environ,
            pass_fds=(sock.fileno(),), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        sock.close()
        try:
            with httpx.Client(base_url=f"http://127.0.0.1:{port}",
                              timeout=httpx.Timeout(180, connect=2), trust_env=False) as client:
                # Startup imports the model stack and runs the detection rules. Allow a
                # bounded two minutes when the host is also running the test suite.
                deadline = time.monotonic() + 120
                while True:
                    if process.poll() is not None:
                        raise RuntimeError("The eval API server failed to start.")
                    try:
                        ready = client.get("/openapi.json", timeout=0.5).status_code == 200
                    except httpx.TransportError:
                        ready = False
                    if ready:
                        break
                    if time.monotonic() >= deadline:
                        raise RuntimeError("The eval API server did not become ready in 120 seconds.")
                    time.sleep(0.1)
                yield client
        finally:
            if process.poll() is None:
                process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
