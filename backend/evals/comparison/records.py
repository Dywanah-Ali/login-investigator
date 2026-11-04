"""Local request records: frozen manifest, durable append-only events and hashed artifacts.

Request starts precede dispatch; unknown cost stays unknown. No scheduling, model
selection, assessment workflow or hosted integration is defined by this module.
"""

from __future__ import annotations

import hashlib
import json
import os
import time
from collections.abc import Callable
from pathlib import Path

from evals.privacy import redact

SCHEMA = "comparison-record/1"

def _sync_write(path: Path, text: str, mode: str) -> None:
    with path.open(mode, encoding="utf-8") as handle:
        handle.write(text)
        handle.flush()
        os.fsync(handle.fileno())


class RunBundle:
    def __init__(self, root: Path, manifest: dict, clock: Callable[[], float] = time.time):
        self.root = root
        self.manifest = manifest
        self.clock = clock
        self.torn_tail = False
        self._seq = len(self.events())

    @classmethod
    def create(cls, root: Path, manifest: dict, clock: Callable[[], float] = time.time) -> RunBundle:
        if (root / "manifest.json").exists():
            raise FileExistsError(f"{root} already holds a run; a manifest is never overwritten")
        root.mkdir(parents=True, exist_ok=True)
        (root / "artifacts").mkdir(exist_ok=True)
        frozen = redact({"record_schema": SCHEMA, **manifest})
        tmp = root / "manifest.json.tmp"
        _sync_write(tmp, json.dumps(frozen, indent=2, ensure_ascii=False) + "\n", "w")
        tmp.replace(root / "manifest.json")
        (root / "events.jsonl").touch()
        return cls(root, frozen, clock)

    @classmethod
    def open(cls, root: Path, clock: Callable[[], float] = time.time) -> RunBundle:
        return cls(root, json.loads((root / "manifest.json").read_text()), clock)

    def events(self) -> list[dict]:
        """Every complete event in order. A torn final line (a crash mid-write) is skipped and
        flagged; a torn line anywhere else means the file was edited and stops the read."""
        path = self.root / "events.jsonl"
        if not path.exists():
            return []
        lines = path.read_text(encoding="utf-8").split("\n")
        events = []
        self.torn_tail = False
        for index, line in enumerate(lines):
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                if index == len(lines) - 1:
                    self.torn_tail = True
                    continue
                raise ValueError(f"{path} line {index + 1} is not valid JSON") from None
        return events

    def append(self, event_type: str, **fields) -> dict:
        if self.torn_tail:
            self._set_aside_torn_tail()
        self._seq += 1
        event = redact({"seq": self._seq, "at": round(self.clock(), 3), "type": event_type, **fields})
        _sync_write(self.root / "events.jsonl", json.dumps(event, ensure_ascii=False) + "\n", "a")
        return event

    def _set_aside_torn_tail(self) -> None:
        """Move a crash's partial last line to `torn-fragments.txt`, kept as evidence, so the
        events file stays valid JSON lines before the next event is appended."""
        path = self.root / "events.jsonl"
        data = path.read_bytes()
        cut = data.rfind(b"\n") + 1
        _sync_write(self.root / "torn-fragments.txt",
                    data[cut:].decode("utf-8", errors="replace") + "\n", "a")
        with path.open("r+b") as handle:
            handle.truncate(cut)
            handle.flush()
            os.fsync(handle.fileno())
        self.torn_tail = False

    def write_artifact(self, name: str, text: str) -> dict:
        clean = redact(text)
        relative = Path("artifacts") / name
        target = self.root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        _sync_write(target, clean, "w")
        return {"path": relative.as_posix(),
                "sha256": hashlib.sha256(clean.encode("utf-8")).hexdigest()}

    def read_artifact(self, ref: dict) -> str:
        text = (self.root / ref["path"]).read_text(encoding="utf-8")
        if hashlib.sha256(text.encode("utf-8")).hexdigest() != ref["sha256"]:
            raise ValueError(f"artifact {ref['path']} does not match its recorded hash")
        return text


def _by_type(events: list[dict], *types: str) -> list[dict]:
    return [e for e in events if e["type"] in types]


def recover(bundle: RunBundle) -> dict:
    """Close what a crash left open, explicitly. A request that started but never finished may
    have been billed: it is marked unresolved with unknown cost, and it is never sent again. A
    caller explicitly decides whether a later attempt is appropriate."""
    events = bundle.events()
    closed_requests = {e["request_id"] for e in _by_type(events, "request_finished", "request_unresolved")}
    unresolved = [e["request_id"] for e in _by_type(events, "request_started")
                  if e["request_id"] not in closed_requests]
    for request_id in unresolved:
        bundle.append("request_unresolved", request_id=request_id,
                      reason="started before an interruption; outcome and billing unknown")
    return {"unresolved_requests": unresolved}


USAGE_KEYS = ("input", "output", "reasoning", "cache_read")


def resources(bundle: RunBundle) -> dict:
    """Per-request and total resources. One entry per request ID, so a settlement can never
    double-charge; the latest settlement wins. Missing cost or usage is counted as unknown, never
    as zero. Reasoning is kept as the provider reports it: some count it inside output, so the
    output and reasoning sums are shown side by side, never added together."""
    requests: dict[str, dict] = {}
    for event in bundle.events():
        kind = event["type"]
        if kind == "request_started":
            requests[event["request_id"]] = {
                "trial_id": event.get("trial_id"), "role": event.get("role"),
                "retry_of": event.get("retry_of"), "status": "started", "elapsed_s": None,
                "usage": None, "cost_usd": None, "cost_source": None}
        elif kind == "request_finished":
            entry = requests.setdefault(event["request_id"], {})
            entry.update(status=event["status"], elapsed_s=event.get("elapsed_s"),
                         usage=event.get("usage"))
            if event.get("cost_usd") is not None:
                entry.update(cost_usd=event["cost_usd"],
                             cost_source=event.get("cost_source", "response"))
        elif kind == "request_unresolved":
            requests.setdefault(event["request_id"], {}).update(status="unresolved")
        elif kind == "cost_settled":
            requests.setdefault(event["request_id"], {}).update(
                cost_usd=event["cost_usd"], cost_source=event.get("source", "settlement"))
    return {"requests": requests, "total": summarise(list(requests.values()))}


def summarise(entries: list[dict]) -> dict:
    known = [e["cost_usd"] for e in entries if e.get("cost_usd") is not None]
    usage = {key: sum((e.get("usage") or {}).get(key) or 0 for e in entries) for key in USAGE_KEYS}
    # A provider that reports some usage fields but not others leaves those fields unknown.
    unknown_by_key = {key: sum(1 for e in entries if (e.get("usage") or {}).get(key) is None)
                      for key in USAGE_KEYS}
    return {
        "request_count": len(entries),
        "retry_count": sum(1 for e in entries if e.get("retry_of")),
        "known_cost_usd": round(sum(known), 6),
        "unknown_cost_requests": len(entries) - len(known),
        "cost_complete": len(known) == len(entries),
        "usage": usage,
        "unknown_usage_requests": sum(1 for e in entries if not e.get("usage")),
        "unknown_usage_by_key": unknown_by_key,
    }
