"""Named, deterministic graph walks. Shared addresses are context, never exposed accounts."""

from dataclasses import dataclass
from typing import Any, cast

import networkx as nx
import pandas as pd

from login_investigator.loader import parse_window
from login_investigator.rules import BRUTE_FORCE, PASSWORD_SPRAYING, Finding


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


def _targets(graph: nx.MultiDiGraph, source: str, relationship: str) -> list[str]:
    return sorted(target for _, target, key in graph.out_edges(source, keys=True) if key == relationship)


def _times(graph: nx.MultiDiGraph, source: str, target: str, relationship: str,
           start: pd.Timestamp, end: pd.Timestamp) -> list[str]:
    return [value for value in graph[source][target][relationship]["times"]
            if start <= pd.Timestamp(value) < end]


def _peers(graph: nx.MultiDiGraph, person: str, relationship: str,
           start: pd.Timestamp, end: pd.Timestamp) -> tuple[list[str], list[list[str]], list[dict[str, Any]]]:
    peers: set[str] = set()
    paths: list[list[str]] = []
    observations: list[dict[str, Any]] = []
    for shared in _targets(graph, person, relationship):
        subject_times = _times(graph, person, shared, relationship, start, end)
        if not subject_times:
            continue
        for peer, _, key in sorted(graph.in_edges(shared, keys=True)):
            if peer == person or key != relationship:
                continue
            peer_times = _times(graph, peer, shared, relationship, start, end)
            if peer_times:
                peers.add(peer)
                paths.append([person, shared, peer])
                observations.append({"shared_id": shared, "account_id": peer,
                                     "subject_times": subject_times, "peer_times": peer_times})
    return sorted(peers), sorted(paths), observations


def finding_radius(graph: nx.MultiDiGraph, log: pd.DataFrame, finding: Finding,
                   start: str | None = None, end: str | None = None) -> FindingRadius:
    """Read permissions from the snapshot and login relationships from the requested period.

    For sprays/brute force, only accounts successfully accessed by a finding address in that
    period receive a radius. Targeted usernames alone do not establish account access. Other
    findings name their subject accounts directly. No result labels an account compromised.
    """
    period, lower, upper = _period(log, start, end)
    users = {str(user).lower() for user in finding.users}
    if finding.rule in {BRUTE_FORCE, PASSWORD_SPRAYING}:
        successes = log.loc[(log["outcome"] == "success") & log["source_ip"].isin(finding.ips)
                            & (log["timestamp_utc"] >= lower) & (log["timestamp_utc"] < upper)]
        users = {str(user).lower() for user in successes["username"]}
    people = {data["username"].lower(): node for node, data in graph.nodes(data=True)
              if data["entity_type"] == "person"}
    if users - people.keys():
        raise ValueError("Finding names an account absent from the organisation")
    results: list[AccountRadius] = []
    for person in sorted(people[user] for user in users):
        group_ids = _targets(graph, person, "member_of")
        paths = [[person, group] for group in group_ids]
        paths += [[person, group, asset] for group in group_ids for asset in _targets(graph, group, "grants")]
        assets = sorted({path[2] for path in paths if len(path) == 3})
        device_ids, device_paths, _ = _peers(graph, person, "used_device", lower, upper)
        _, network_paths, observations = _peers(graph, person, "used_address", lower, upper)
        by_address = []
        for network in sorted({path[1] for path in network_paths}):
            shared_paths = [path for path in network_paths if path[1] == network]
            by_address.append(AddressMatches(
                dict(graph.nodes[network]), [dict(graph.nodes[path[2]]) for path in shared_paths],
                shared_paths, [row for row in observations if row["shared_id"] == network],
            ))
        results.append(AccountRadius(
            dict(graph.nodes[person]), [dict(graph.nodes[node]) for node in group_ids],
            [dict(graph.nodes[node]) for node in assets], sorted(paths),
            [dict(graph.nodes[node]) for node in device_ids], device_paths,
            AddressReuse(by_address),
        ))
    return FindingRadius(finding.finding_id, _iso(finding.first_seen), _iso(finding.last_seen), period, results)
