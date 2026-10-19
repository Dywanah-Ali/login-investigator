"""Ensure detection findings receive their required sign-in evidence before answering."""

import ipaddress
import json
import re
from typing import Any
from uuid import uuid4

from langchain.agents.middleware import AgentState, before_model
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langgraph.runtime import Runtime


def _ip(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    try:
        return str(ipaddress.ip_address(value))
    except ValueError:
        return None


def _specific_question(question: str) -> bool:
    """Explicit attack-type or IP questions must not expand to every detection category."""
    if re.search(r"\b(?:spray\w*|brute[ -]*force|new countr\w*|success.{0,30}after.{0,20}fail)\w*",
                 question, re.IGNORECASE):
        return True
    return any(_ip(token.strip('.:')) or _ip(token)
               for token in re.findall(r"[0-9a-fA-F:.]+", question))


@before_model(can_jump_to=["tools"])
def complete_detection_searches(state: AgentState, runtime: Runtime[Any]) -> dict[str, Any] | None:
    """Only actual current-turn tool results trigger coverage; log text never sets policy."""
    messages = state["messages"]
    start = next((i for i in range(len(messages) - 1, -1, -1)
                  if isinstance(messages[i], HumanMessage)), len(messages))
    if start < len(messages) and _specific_question(messages[start].text):
        return None
    calls: dict[str, dict[str, Any]] = {}
    required: dict[str, None] = {}
    searched: set[str] = set()
    for message in messages[start:]:
        if isinstance(message, AIMessage):
            for call in message.tool_calls:
                call_id = call.get("id")
                if isinstance(call_id, str):
                    calls[call_id] = dict(call)
        elif isinstance(message, ToolMessage):
            call = calls.get(message.tool_call_id)
            if call is None:
                continue
            if call["name"] == "search_logins":
                args = call["args"]
                address = _ip(args.get("ip"))
                if address and not any(args.get(field) for field in
                                       ("user", "start", "end", "outcome", "country")):
                    # Even a failed attempt counts: let the model explain it, never retry forever.
                    searched.add(address)
            elif call["name"] == "find_suspicious_activity":
                try:
                    payload = json.loads(message.text)
                except (ValueError, TypeError):
                    continue
                data = payload.get("data") if isinstance(payload, dict) else None
                findings = data.get("findings") if isinstance(data, dict) else None
                if not isinstance(findings, list):
                    continue
                for finding in findings:
                    values = finding.get("ips") if isinstance(finding, dict) else None
                    if isinstance(values, list):
                        for value in values:
                            address = _ip(value)
                            if address:
                                required[address] = None
    missing = [address for address in required if address not in searched]
    if not missing:
        return None
    return {"messages": [AIMessage("", tool_calls=[
        {"name": "search_logins", "args": {"ip": address}, "id": uuid4().hex,
         "type": "tool_call"} for address in missing
    ])], "jump_to": "tools"}
