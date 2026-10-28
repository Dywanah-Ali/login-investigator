"""Build the organisation map. Source identities stay intact on nodes and typed edges."""

from pathlib import Path

import networkx as nx
import pandas as pd
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine

from login_investigator.loader import TIMESTAMP_FORMAT, load_log
from . import schema


async def build_graph(engine: AsyncEngine, dataset: Path) -> tuple[nx.MultiDiGraph, pd.DataFrame]:
    graph = nx.MultiDiGraph()
    entities = (
        (schema.people, "person", "person_id"), (schema.groups, "group", "group_id"),
        (schema.assets, "asset", "asset_id"), (schema.devices, "device", "device_id"),
        (schema.networks, "network", "network_id"),
    )
    async with engine.connect() as connection:
        for table, kind, identifier in entities:
            for row in (await connection.execute(select(table))).mappings():
                graph.add_node(row[identifier], **dict(row), entity_type=kind)
        for table, source, target, relationship in (
            (schema.memberships, "person_id", "group_id", "member_of"),
            (schema.grants, "group_id", "asset_id", "grants"),
            (schema.device_assignments, "person_id", "device_id", "assigned_device"),
        ):
            for row in (await connection.execute(select(table))).mappings():
                graph.add_edge(row[source], row[target], key=relationship, relationship=relationship)
        for row in (await connection.execute(select(schema.chunks.c.chunk_id, schema.chunks.c.content,
                                                     schema.chunks.c.langchain_metadata))).mappings():
            graph.add_node(row["chunk_id"], entity_type="chunk", content=row["content"],
                           metadata=row["langchain_metadata"])
        for row in (await connection.execute(select(schema.mentions))).mappings():
            graph.add_edge(row["chunk_id"], row["entity_id"], key="mentions", relationship="mentions")

    log = load_log(dataset / "logins.csv")
    people = {data["username"].lower(): node for node, data in graph.nodes(data=True)
              if data["entity_type"] == "person"}
    addresses = {data["address"]: node for node, data in graph.nodes(data=True)
                 if data["entity_type"] == "network"}
    devices = {node for node, data in graph.nodes(data=True) if data["entity_type"] == "device"}
    for row in log.loc[log["outcome"] == "success"].to_dict("records"):
        person = people.get(str(row["username"]).lower())
        if person is None:
            raise ValueError("Successful sign-in names an unknown account")
        targets = [(addresses.get(row["source_ip"]), "used_address")]
        device = str(row["device_id"])
        if device:
            if device not in devices:
                raise ValueError("Sign-in names an unregistered device")
            targets.append((device, "used_device"))
        for target, relationship in targets:
            if target is None:
                continue  # External addresses remain log evidence, not organisation nodes.
            if not graph.has_edge(person, target, relationship):
                graph.add_edge(person, target, key=relationship, relationship=relationship, times=[])
            graph[person][target][relationship]["times"].append(
                row["timestamp_utc"].strftime(TIMESTAMP_FORMAT))
    for _, _, data in graph.edges(data=True):
        if "times" in data:
            data["times"] = tuple(sorted(set(data["times"])))
    return graph, log
