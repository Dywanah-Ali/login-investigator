"""Prepare native graph records. Passage content remains exclusively in PostgreSQL."""

from collections import defaultdict
from pathlib import Path
from typing import Any, LiteralString, cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine

from login_investigator.loader import TIMESTAMP_FORMAT, load_log

from . import schema
from .graph_service import execute
from .neo4j_graph import GraphSettings


async def import_graph(engine: AsyncEngine, dataset: Path, settings: GraphSettings,
                       build_id: str, fingerprint: str) -> None:
    nodes: list[dict[str, Any]] = []
    edges: dict[str, list[dict[str, Any]]] = defaultdict(list)
    async with engine.connect() as connection:
        for table, kind, identifier in (
            (schema.people, 'person', 'person_id'), (schema.groups, 'group', 'group_id'),
            (schema.assets, 'asset', 'asset_id'), (schema.devices, 'device', 'device_id'),
            (schema.networks, 'network', 'network_id'),
        ):
            for row in (await connection.execute(select(table))).mappings():
                nodes.append({**dict(row), 'id': row[identifier], 'entity_type': kind})
        for table, source, target, relation in (
            (schema.memberships, 'person_id', 'group_id', 'member_of'),
            (schema.grants, 'group_id', 'asset_id', 'grants'),
            (schema.device_assignments, 'person_id', 'device_id', 'assigned_device'),
            (schema.mentions, 'chunk_id', 'entity_id', 'mentions'),
        ):
            for row in (await connection.execute(select(table))).mappings():
                edges[relation].append({'source': row[source], 'target': row[target], 'properties': {}})
        for chunk in (await connection.scalars(select(schema.chunks.c.chunk_id))).all():
            nodes.append({'id': chunk, 'entity_type': 'chunk'})
    people = {node['username'].lower(): node['id'] for node in nodes if node['entity_type'] == 'person'}
    devices = {node['id'] for node in nodes if node['entity_type'] == 'device'}
    log = load_log(dataset / 'logins.csv')
    # Successful sign-ins draw used_device edges only. Network nodes stay as organisation facts
    # without used_address edges (author's T50 ruling, 1 November 2026).
    observed: dict[tuple[str, str], set[str]] = defaultdict(set)
    for row in log.loc[log['outcome'] == 'success'].to_dict('records'):
        person = people[str(row['username']).lower()]
        device = str(row['device_id'])
        if device and device not in devices:
            raise ValueError('Sign-in names an unregistered device')
        if device:
            observed[person, device].add(row['timestamp_utc'].strftime(TIMESTAMP_FORMAT))
    for (source, target), times in observed.items():
        edges['used_device'].append({'source': source, 'target': target, 'properties': {'times': sorted(times)}})
    execute(settings, 'CREATE CONSTRAINT entity_id FOR (n:Entity) REQUIRE n.id IS UNIQUE')
    execute(settings, 'UNWIND $rows AS row CREATE (n:Entity) SET n = row', rows=nodes)
    # Relationship names come only from the fixed mapping above, never from source input.
    for relation, rows in edges.items():
        execute(settings, 'UNWIND $rows AS row MATCH (a:Entity {id:row.source}), (b:Entity {id:row.target}) ' +
                cast(LiteralString, f'CREATE (a)-[r:{relation}]->(b) SET r = row.properties'), rows=rows)
    execute(settings, 'CREATE (:Build {id:$id, fingerprint:$fingerprint})', id=build_id, fingerprint=fingerprint)
