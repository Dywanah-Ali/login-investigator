"""Independent reconciliation against source CSVs and stored passage identities.

No importer transforms are used here. Counts cannot hide swapped endpoints or attributes.
"""

import csv
from collections import Counter
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine

from . import schema
from .integrity import GraphCounts, GraphIntegrityError
from .graph_service import execute
from .neo4j_graph import GraphSettings


async def verify_graph(engine: AsyncEngine, dataset: Path, settings: GraphSettings,
                       build_id: str, fingerprint: str) -> GraphCounts:
    node_rows = execute(settings, 'MATCH (n) WHERE NOT n:Build RETURN properties(n) AS properties, labels(n) AS labels')
    if any(not isinstance(row['properties'].get('id'), str) for row in node_rows):
        raise GraphIntegrityError('Graph node has no stable identity')
    actual = {row['properties']['id']: row['properties'] for row in node_rows}
    if len(actual) != len(node_rows) or any(row['labels'] != ['Entity'] for row in node_rows):
        raise GraphIntegrityError('Unexpected graph node identities or labels')
    expected = {}
    expected_edges = {}
    async with engine.connect() as connection:
        for name, kind, key in (('people', 'person', 'person_id'), ('groups', 'group', 'group_id'),
                                ('assets', 'asset', 'asset_id'), ('devices', 'device', 'device_id'),
                                ('networks', 'network', 'network_id')):
            with (dataset / 'org' / (name + '.csv')).open(newline='') as handle:
                source = [{k: v or None for k, v in row.items()} for row in csv.DictReader(handle)]
            stored = [dict(row) for row in (await connection.execute(select(schema.ORG_TABLES[name]))).mappings()]
            if sorted(source, key=lambda r: str(r[key])) != sorted(stored, key=lambda r: str(r[key])):
                raise GraphIntegrityError('PostgreSQL organisation differs from source snapshot')
            for row in source:
                expected[row[key]] = {**{k: v for k, v in row.items() if v is not None},
                                      'id': row[key], 'entity_type': kind}
        for name, source_key, target_key, relation in (
            ('memberships', 'person_id', 'group_id', 'member_of'),
            ('grants', 'group_id', 'asset_id', 'grants'),
            ('device_assignments', 'person_id', 'device_id', 'assigned_device'),
        ):
            with (dataset / 'org' / (name + '.csv')).open(newline='') as handle:
                rows = list(csv.DictReader(handle))
            stored = [dict(row) for row in (await connection.execute(select(schema.ORG_TABLES[name]))).mappings()]
            if sorted(rows, key=lambda r: sorted(r.items())) != sorted(stored, key=lambda r: sorted(r.items())):
                raise GraphIntegrityError('PostgreSQL links differ from source snapshot')
            for row in rows:
                expected_edges[row[source_key], row[target_key], relation] = {}
        for chunk in (await connection.scalars(select(schema.chunks.c.chunk_id))).all():
            expected[chunk] = {'id': chunk, 'entity_type': 'chunk'}
        for row in (await connection.execute(select(schema.mentions))).mappings():
            if row['entity_id'] not in expected or expected[row['entity_id']]['entity_type'] != row['entity_type']:
                raise GraphIntegrityError('Passage mention has an invalid target')
            expected_edges[row['chunk_id'], row['entity_id'], 'mentions'] = {}
    people = {row['username'].lower(): key for key, row in expected.items() if row['entity_type'] == 'person'}
    networks = {row['address']: key for key, row in expected.items() if row['entity_type'] == 'network'}
    observations = {}
    with (dataset / 'logins.csv').open(newline='') as handle:
        for row in csv.DictReader(handle):
            if row['outcome'] != 'success':
                continue
            person = people[row['username'].lower()]
            for target, relation in ((networks.get(row['source_ip']), 'used_address'),
                                     (row['device_id'], 'used_device')):
                if target:
                    observations.setdefault((person, target, relation), set()).add(row['timestamp_utc'])
    for edge, times in observations.items():
        expected_edges[edge] = {'times': sorted(times)}
    edges = execute(settings, 'MATCH (a)-[r]->(b) RETURN a.id AS source, b.id AS target, '
                              'type(r) AS relation, properties(r) AS properties')
    actual_edges = {(row['source'], row['target'], row['relation']): row['properties'] for row in edges}
    if actual != expected or actual_edges != expected_edges or len(edges) != len(expected_edges):
        raise GraphIntegrityError('Graph identities, attributes, passage references or observations differ from sources')
    connected = {node for source, target, _ in expected_edges for node in (source, target)}
    if any(key not in connected and row['entity_type'] in {'person', 'group', 'asset', 'device'}
           for key, row in expected.items()):
        raise GraphIntegrityError('Isolated organisation node')
    if execute(settings, 'MATCH (b:Build) RETURN properties(b) AS properties') != [
        {'properties': {'id': build_id, 'fingerprint': fingerprint}}
    ]:
        raise GraphIntegrityError('Graph build identity does not match the pair')
    return GraphCounts(dict(Counter(row['entity_type'] for row in expected.values())),
                       dict(Counter(edge[2] for edge in expected_edges)))
