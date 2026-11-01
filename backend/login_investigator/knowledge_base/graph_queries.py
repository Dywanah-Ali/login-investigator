"""Storage-independent graph query boundary. Results are plain domain records."""

from typing import Protocol

from login_investigator.rules import Finding

from .radius import FindingRadius, GraphWalk


class GraphQueries(Protocol):
    def lookup_account(self, account_id: str) -> dict[str, object]: ...
    def account_groups(self, username: str) -> GraphWalk: ...
    def finding_radius(self, finding: Finding, start: str | None = None,
                       end: str | None = None) -> FindingRadius: ...
    def finding_walk(self, finding_id: str) -> GraphWalk: ...
