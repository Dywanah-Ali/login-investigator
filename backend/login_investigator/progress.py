"""Per-invocation tool lifecycle signals, without tool inputs, results or errors."""

from dataclasses import dataclass
from typing import Any, Literal
from uuid import UUID

from langchain_core.callbacks import BaseCallbackHandler
from langgraph.config import get_stream_writer


@dataclass(frozen=True)
class ToolProgress:
    name: str
    call_id: str
    phase: Literal["start", "end", "error"]


class ToolLifecycle(BaseCallbackHandler):
    """Inline callbacks retain the graph context needed by its custom stream writer."""

    run_inline = True

    def __init__(self, allowed_names: set[str]):
        self._allowed_names = allowed_names
        self._names: dict[UUID, str] = {}

    def on_tool_start(self, serialized: dict[str, Any] | None, input_str: str,
                      *, run_id: UUID, **kwargs: Any) -> None:
        name = (serialized or {}).get("name")
        if name in self._allowed_names:
            self._names[run_id] = name
            get_stream_writer()(ToolProgress(name, str(run_id), "start"))

    def _finish(self, run_id: UUID, phase: Literal["end", "error"]) -> None:
        name = self._names.pop(run_id, None)
        if name is not None:
            get_stream_writer()(ToolProgress(name, str(run_id), phase))

    def on_tool_end(self, output: Any, *, run_id: UUID, **kwargs: Any) -> None:
        self._finish(run_id, "end")

    def on_tool_error(self, error: BaseException, *, run_id: UUID, **kwargs: Any) -> None:
        self._finish(run_id, "error")
