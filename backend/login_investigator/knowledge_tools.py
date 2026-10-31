"""Read-only knowledge-base tool adapters. The application supplies the checked core."""

import json
from typing import Any

from langchain_core.tools import BaseTool, tool

from login_investigator.knowledge_base import NOT_BUILT, KnowledgeBase


def account_tool(kb: KnowledgeBase | None) -> BaseTool:
    @tool(response_format="content_and_artifact")
    def lookup_account(account_id: str) -> tuple[str, dict[str, Any]]:
        """Look up an account's owner, department and privilege groups in the organisation graph.

        Read-only organisation snapshot, not proof of historical permissions or compromise.
        account_id: exact login username (thomas.price) or stable ID (user-thomas.price).
        """
        if kb is None:
            return NOT_BUILT, {"tool": "lookup_account", "status": "unavailable"}
        record = kb.lookup_account(account_id)
        artifact = {"tool": "lookup_account", "schema_version": 1,
                    "basis": "organisation snapshot; historical permissions unknown", **record}
        account = record["account"]
        if not isinstance(account, dict):
            return "Account lookup: not found in the organisation snapshot.", artifact
        groups = record["groups"]
        assert isinstance(groups, list)
        # JSON preserves field boundaries even when a source name contains newlines or quotes.
        briefing = {"account": account["username"], "owner": account["display_name"],
                    "department": account["department"],
                    "groups": [{"name": group["name"], "kind": group["kind"]} for group in groups]}
        return "Account context (organisation snapshot):\n" + json.dumps(briefing), artifact

    return lookup_account
