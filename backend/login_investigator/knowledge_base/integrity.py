"""Independent reconciliation: never use the graph builder to derive expected records."""

import csv
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import networkx as nx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine

from . import schema


class GraphIntegrityError(ValueError):
    """The in-memory map cannot be trusted to represent its sources."""


@dataclass(frozen=True)
class GraphCounts:
    """What the sources say the graph holds, per node type and per relationship."""
    nodes: dict[str, int]
    edges: dict[str, int]


async def check_graph_integrity(engine: AsyncEngine, dataset: Path, graph: nx.MultiDiGraph) -> GraphCounts:
    node_counts: dict[str, int] = {}
    expected_nodes: set[str] = set()
    expected_edges: set[tuple[str, str, str]] = set()
    people: dict[str, str] = {}
    networks: dict[str, str] = {}
    devices: set[str] = set()
    async with engine.connect() as connection:
        # Separate source reads and mappings from the builder, intentionally. Sharing its
        # transform would allow a missing relationship to fool both the build and the check.
        for name, kind, id_column in (
            ("people", "person", "person_id"), ("groups", "group", "group_id"),
            ("assets", "asset", "asset_id"), ("devices", "device", "device_id"),
            ("networks", "network", "network_id"),
        ):
            records = list((await connection.execute(select(schema.ORG_TABLES[name]))).mappings())
            ids = {row[id_column] for row in records}
            actual = {node for node, data in graph.nodes(data=True) if data.get("entity_type") == kind}
            if ids != actual:
                raise GraphIntegrityError(f"{kind} node identities differ from storage")
            expected_nodes.update(ids)
            node_counts[kind] = len(ids)
            for row in records:
                if any(graph.nodes[row[id_column]].get(key) != value for key, value in row.items()):
                    raise GraphIntegrityError(f"{kind} attributes differ from storage")
                if kind == "person":
                    people[row["username"].lower()] = row[id_column]
                elif kind == "network":
                    networks[row["address"]] = row[id_column]
                elif kind == "device":
                    devices.add(row[id_column])
        for row in (await connection.execute(select(schema.memberships))).mappings():
            expected_edges.add((row["person_id"], row["group_id"], "member_of"))
        for row in (await connection.execute(select(schema.grants))).mappings():
            expected_edges.add((row["group_id"], row["asset_id"], "grants"))
        for row in (await connection.execute(select(schema.device_assignments))).mappings():
            expected_edges.add((row["person_id"], row["device_id"], "assigned_device"))
        chunk_rows = list((await connection.execute(select(
            schema.chunks.c.chunk_id, schema.chunks.c.content, schema.chunks.c.langchain_metadata,
        ))).mappings())
        chunk_ids = {row["chunk_id"] for row in chunk_rows}
        if chunk_ids != {node for node, data in graph.nodes(data=True) if data.get("entity_type") == "chunk"}:
            raise GraphIntegrityError("chunk node identities differ from storage")
        expected_nodes.update(chunk_ids)
        node_counts["chunk"] = len(chunk_ids)
        for row in chunk_rows:
            data = graph.nodes[row["chunk_id"]]
            if data.get("content") != row["content"] or data.get("metadata") != row["langchain_metadata"]:
                raise GraphIntegrityError("chunk attributes differ from storage")
        for row in (await connection.execute(select(schema.mentions))).mappings():
            target = row["entity_id"]
            if target not in graph or graph.nodes[target].get("entity_type") != row["entity_type"]:
                raise GraphIntegrityError("mention points to an unknown entity or wrong type")
            expected_edges.add((row["chunk_id"], target, "mentions"))

    observed: dict[tuple[str, str, str], set[str]] = {}
    with (dataset / "logins.csv").open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["outcome"] != "success":
                continue
            person = people.get(row["username"].lower())
            if person is None:
                raise GraphIntegrityError("successful log account is absent from organisation")
            address = networks.get(row["source_ip"])
            if address is not None:
                observed.setdefault((person, address, "used_address"), set()).add(row["timestamp_utc"])
            device = row["device_id"]
            if device:
                if device not in devices:
                    raise GraphIntegrityError("logged device is absent from organisation")
                observed.setdefault((person, device, "used_device"), set()).add(row["timestamp_utc"])
    expected_edges.update(observed)
    if set(graph) != expected_nodes:
        raise GraphIntegrityError("unexpected graph nodes")
    if set(graph.edges(keys=True)) != expected_edges:
        raise GraphIntegrityError("relationship identities differ from sources")
    for source, target, key, data in graph.edges(keys=True, data=True):
        if data.get("relationship") != key:
            raise GraphIntegrityError("relationship type differs from its key")
        if (source, target, key) in observed:
            if data.get("times") != tuple(sorted(observed[source, target, key])):
                raise GraphIntegrityError("relationship times differ from login records")
    for node, data in graph.nodes(data=True):
        if data["entity_type"] in {"person", "group", "asset", "device"} and graph.degree(node) == 0:
            raise GraphIntegrityError("isolated organisation node")
    return GraphCounts(node_counts, dict(Counter(key for _, _, key in expected_edges)))
