"""One tool-result fence and one model boundary for saved evidence."""

from collections.abc import Callable

from langchain.agents.middleware import ModelRequest, ModelResponse, wrap_model_call, wrap_tool_call
from langchain_core.messages import ToolMessage
from langgraph.prebuilt.tool_node import ToolCallRequest
from langgraph.types import Command


def _opening(source: str) -> str:
    return f'<tool_result source="{source}" trust="untrusted">\n'


_CLOSING = "\n</tool_result>"


def tool_content(message: ToolMessage) -> str:
    """Read the payload for code and existing views, including pre-fence saved messages.

    Remove exactly our outer frame, never search inside untrusted text for a delimiter.
    The saved marker distinguishes our frame from a historical result containing similar text.
    """
    source = message.additional_kwargs.get("evidence_source")
    if isinstance(source, str):
        opening = _opening(source)
        if message.text.startswith(opening) and message.text.endswith(_CLOSING):
            return message.text[len(opening):-len(_CLOSING)]
    return message.text


@wrap_tool_call
def fence_tool_result(
    request: ToolCallRequest,
    handler: Callable[[ToolCallRequest], ToolMessage | Command],
) -> ToolMessage | Command:
    result = handler(request)
    if not isinstance(result, ToolMessage):
        raise TypeError("Read-only tools must return a tool message")
    # The registered tool supplies the source, never a field inside the returned evidence.
    source = request.tool.name if request.tool is not None else "unknown_tool"
    return result.model_copy(update={
        "content": _opening(source) + result.text + _CLOSING,
        "additional_kwargs": {**result.additional_kwargs, "evidence_source": source},
    })


@wrap_model_call
def briefings_only(
    request: ModelRequest, handler: Callable[[ModelRequest], ModelResponse],
) -> ModelResponse:
    """Copies for the model only. The checkpoint keeps the original full artifacts."""
    messages = [message.model_copy(update={"artifact": None})
                if isinstance(message, ToolMessage) else message for message in request.messages]
    return handler(request.override(messages=messages))
