"""Named, deterministic graph walks. Shared addresses are context, never exposed accounts."""

from dataclasses import dataclass
from typing import Any, cast

import pandas as pd

from login_investigator.loader import parse_window


@dataclass(frozen=True)
class Period:
    requested_start: str | None
    requested_end: str | None
    effective_start: str | None
    effective_end: str | None
    first_record: str
    last_record: str
    outside_record_bounds: bool
    coverage_note: str = "Record bounds do not establish continuous logging coverage. End is excluded."


@dataclass(frozen=True)
class AddressMatches:
    network: dict[str, Any]
    accounts: list[dict[str, Any]]
    paths: list[list[str]]
    observations: list[dict[str, Any]]


@dataclass(frozen=True)
class AddressReuse:
    by_address: list[AddressMatches]
    meaning: str = "Shared address context, not evidence of exposure or spread; session overlap unknown."


@dataclass(frozen=True)
class AccountRadius:
    account: dict[str, Any]
    groups: list[dict[str, Any]]
    assets: list[dict[str, Any]]
    access_paths: list[list[str]]
    device_peers: list[dict[str, Any]]
    device_paths: list[list[str]]
    address_reuse: AddressReuse


@dataclass(frozen=True)
class FindingRadius:
    finding_id: str
    finding_first_seen: str
    finding_last_seen: str
    period: Period
    accounts: list[AccountRadius]
    permissions_basis: str = "organisation snapshot; historical permissions unknown"


@dataclass(frozen=True)
class GraphWalk:
    records: list[str]
    paths: list[list[str]]


def radius_walk(radius: FindingRadius) -> GraphWalk:
    paths = {tuple(path) for account in radius.accounts
             for path in [*account.access_paths, *account.device_paths]}
    return GraphWalk(sorted({path[-1] for path in paths}), [list(path) for path in sorted(paths)])


def _iso(moment: pd.Timestamp) -> str:
    return moment.isoformat().replace("+00:00", "Z")


def _period(log: pd.DataFrame, start: str | None, end: str | None) -> tuple[Period, pd.Timestamp, pd.Timestamp]:
    lower, upper = parse_window(start, end)
    first = cast(pd.Timestamp, log["timestamp_utc"].min())
    last = cast(pd.Timestamp, log["timestamp_utc"].max())
    # The source format has second precision. The exclusive bound includes its last event.
    log_end = cast(pd.Timestamp, last + pd.Timedelta(seconds=1))
    effective_start = lower if lower is not None else first
    effective_end = upper if upper is not None else log_end
    covered_start, covered_end = max(first, effective_start), min(log_end, effective_end)
    has_overlap = covered_start < covered_end
    period = Period(None if lower is None else _iso(lower), None if upper is None else _iso(upper),
                    _iso(covered_start) if has_overlap else None,
                    _iso(covered_end) if has_overlap else None, _iso(first), _iso(last),
                    effective_start < first or effective_end > log_end
                    or effective_start >= log_end or effective_end <= first)
    return period, effective_start, effective_end


@dataclass(frozen=True)
class Neighbourhood:
    """Exact directed identities used by the radius, including address context."""
    nodes: list[str]
    edges: list[tuple[str, str, str]]


def radius_neighbourhood(radius: FindingRadius) -> Neighbourhood:
    nodes = {account.account["person_id"] for account in radius.accounts}
    edges: set[tuple[str, str, str]] = set()
    for account in radius.accounts:
        for path in account.access_paths:
            edges.add((path[0], path[1], "member_of"))
            if len(path) == 3:
                edges.add((path[1], path[2], "grants"))
        address_paths = [path for match in account.address_reuse.by_address for path in match.paths]
        for paths, relation in ((account.device_paths, "used_device"), (address_paths, "used_address")):
            for subject, shared, peer in paths:
                edges.update({(subject, shared, relation), (peer, shared, relation)})
    nodes.update(node for source, target, _ in edges for node in (source, target))
    return Neighbourhood(sorted(nodes), sorted(edges))
