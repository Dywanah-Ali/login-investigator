"""Storage-independent graph query boundary and the existing in-memory implementation.

Returned values are domain records. T47 keeps this adapter for the active application;
T49 retires it after the replacement has been accepted.
"""

from typing import Protocol

import networkx as nx
import pandas as pd

from login_investigator.rules import Finding, detect_all
from .radius import FindingRadius, GraphWalk, account_groups, finding_radius, radius_walk


class GraphQueries(Protocol):
    def lookup_account(self, account_id: str) -> dict[str, object]: ...
    def account_groups(self, username: str) -> GraphWalk: ...
    def finding_radius(self, finding: Finding, start: str | None = None,
                       end: str | None = None) -> FindingRadius: ...
    def finding_walk(self, finding_id: str) -> GraphWalk: ...


class NetworkXQueries:
    def __init__(self, graph: nx.MultiDiGraph, log: pd.DataFrame):
        self.graph = graph
        self.log = log

    def finding_radius(self, finding: Finding, start: str | None = None, end: str | None = None) -> FindingRadius:
        if self.log is None:
            raise ValueError("Open the knowledge base with its dataset to compute a radius")
        return finding_radius(self.graph, self.log, finding, start, end)

    def account_groups(self, username: str) -> GraphWalk:
        return account_groups(self.graph, username)

    def lookup_account(self, account_id: str) -> dict[str, object]:
        """Return a snapshot of one account's owner, department and memberships.

        Accept the organisation's stable person ID or its login username. All returned records
        are copies: a caller cannot change the shared graph through the result.
        """
        matches = [(node, data) for node, data in self.graph.nodes(data=True)
                   if data["entity_type"] == "person" and
                   account_id.lower() in (node.lower(), data["username"].lower())]
        if len(matches) != 1:
            return {"status": "not_found", "account": None, "groups": [], "paths": []}
        person_id, data = matches[0]
        walk = self.account_groups(data["username"])
        return {"status": "found", "account": dict(data),
                "groups": [dict(self.graph.nodes[node]) for node in walk.records],
                "paths": walk.paths}

    def finding_walk(self, finding_id: str) -> GraphWalk:
        if self.log is None:
            raise ValueError("Open the knowledge base with its dataset to walk a finding")
        finding = next((f for f in detect_all(self.log) if f.finding_id == finding_id), None)
        if finding is None:
            raise ValueError("No finding has this ID in the dataset's log")
        return radius_walk(self.finding_radius(finding))
