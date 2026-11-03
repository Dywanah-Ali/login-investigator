"""One streaming HTTP request with an enclosing elapsed-time deadline.

Requests' timeout is an inactivity timeout. A short-lived worker process lets the parent stop
the connection at the agreed elapsed deadline even during DNS, headers or a trickling body.
There is no background request left to overlap the runner's next attempt. Cancellation does
not prove provider billing stopped. No retries and no redirects are performed here.
"""

from __future__ import annotations

import json
import multiprocessing
import time
from collections.abc import Generator, Iterator
from multiprocessing.connection import Connection

import requests

from evals.comparison.adapters import AdapterError
from evals.comparison.records import redact


def _sse(lines) -> Iterator[dict]:
    data: list[str] = []
    for line in lines:
        if line == "":
            if data:
                payload = "\n".join(data)
                data = []
                if payload == "[DONE]":
                    return
                event = json.loads(payload)
                if not isinstance(event, dict):
                    raise ValueError("SSE event is not an object")
                yield event
        elif line.startswith("data:"):
            data.append(line[5:].removeprefix(" "))
    if data:
        raise ValueError("incomplete SSE frame")


def _http_worker(pipe: Connection, url: str, api_key: str, body: dict, timeout_s: float) -> None:
    try:
        with requests.Session() as session:
            # Explicit credentials only. Do not pick up .netrc credentials or proxy settings.
            session.trust_env = False
            with session.post(url, headers={"Authorization": f"Bearer {api_key}",
                                            "Content-Type": "application/json",
                                            "X-OpenRouter-Metadata": "enabled",
                                            "Accept": "text/event-stream"},
                              json=body, stream=True, timeout=timeout_s,
                              allow_redirects=False) as response:
                if response.status_code != 200:
                    # Failed requests can still report charges. Retain the response after
                    # removing credentials, including classification and generation identity.
                    try:
                        data = response.json()
                    except ValueError:
                        data = {}
                    if not isinstance(data, dict):
                        data = {"unparsed_error": data}
                    clean = redact(data, [api_key])
                    pipe.send({"type": "transport.http_error", "status": response.status_code,
                               "body": clean, "response": clean})
                elif "text/event-stream" not in response.headers.get("Content-Type", ""):
                    pipe.send({"type": "transport.error", "kind": "permanent",
                               "message": "Expected an OpenRouter SSE response"})
                else:
                    response.encoding = "utf-8"
                    for event in _sse(response.iter_lines(chunk_size=1, decode_unicode=True)):
                        pipe.send(event)
                        if event.get("type") in ("response.completed", "response.failed",
                                                  "response.incomplete", "error"):
                            break
    except requests.Timeout:
        pipe.send({"type": "transport.error", "kind": "timeout",
                   "message": "OpenRouter HTTP inactivity timeout; billing may be unknown"})
    except requests.RequestException:
        pipe.send({"type": "transport.error", "kind": "transient",
                   "message": "OpenRouter HTTP connection failed; billing may be unknown"})
    except (TypeError, ValueError):
        pipe.send({"type": "transport.error", "kind": "permanent",
                   "message": "Malformed OpenRouter event stream"})
    finally:
        pipe.close()


def response_events(url: str, api_key: str, body: dict, timeout_s: float) -> Generator[dict, None, None]:
    if timeout_s <= 0:
        raise AdapterError("timeout", "No request time remains")
    context = multiprocessing.get_context("spawn")
    receiving, sending = context.Pipe(duplex=False)
    worker = context.Process(target=_http_worker, args=(sending, url, api_key, body, timeout_s),
                             daemon=True)
    deadline = time.monotonic() + timeout_s
    try:
        worker.start()
        sending.close()
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0 or not receiving.poll(max(0, remaining)):
                raise AdapterError("timeout", "OpenRouter elapsed deadline; billing may be unknown")
            try:
                yield receiving.recv()
            except EOFError:
                return
    finally:
        receiving.close()
        sending.close()
        if worker.pid is not None:
            if worker.is_alive():
                worker.terminate()
            worker.join(timeout=1)
            if worker.is_alive():
                worker.kill()
                worker.join()
            worker.close()
