"""Door 2: independent corruption refusal and a positive dated device witness."""

import asyncio
import csv
import uuid
from pathlib import Path
from typing import LiteralString

import pytest

from login_investigator.knowledge_base import build_knowledge_base, database_engine, GraphIntegrityError
from login_investigator.knowledge_base.graph_ingestion import import_graph
from login_investigator.knowledge_base.graph_service import GraphService, execute
from login_investigator.knowledge_base.graph_verification import verify_graph
from login_investigator.knowledge_base.neo4j_graph import Neo4jQueries
from login_investigator.knowledge_base.staleness import source_fingerprint
from login_investigator.loader import load_log, parse_utc
from login_investigator.postgres import ServerSettings
from login_investigator.rules import Finding, NEW_COUNTRY
from test_knowledge_base import FakeEmbedder, build_database  # noqa: F401
from test_knowledge_graph import graph_dataset


def test_corrupt_graph_refused_and_successful_device_witness_preserved(build_database: ServerSettings, tmp_path: Path):
    dataset = graph_dataset(tmp_path / 'dataset')
    with (dataset / 'logins.csv').open() as handle:
        reader = csv.DictReader(handle)
        columns = reader.fieldnames
        template = next(row for row in reader if row['outcome'] == 'success')
    assert columns is not None
    entries = [('amelia.ward', 'dev-laptop-amelia.ward', 'success'),
               ('emily.foster', 'dev-laptop-amelia.ward', 'success'),
               ('chloe.barker', 'dev-laptop-amelia.ward', 'failure'),
               ('amelia.ward', '', 'success'), ('isabel.knight', '', 'success')]
    with (dataset / 'logins.csv').open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for minute, (user, device, outcome) in enumerate(entries):
            writer.writerow({**template, 'username': user, 'device_id': device, 'outcome': outcome,
                             'source_ip': '203.0.113.54', 'timestamp_utc': f'2026-10-07T11:0{minute}:00Z',
                             'failure_reason': 'bad_password' if outcome == 'failure' else ''})
    # One passage with no entity mentions is valid and must still exist in the graph.
    passage = dataset / 'corpus/own/sample.md'
    passage.write_text(passage.read_text().replace('thomas.price', 'the responsible team'))
    directory = tmp_path / 'graph'
    directory.mkdir()
    service = GraphService('li-graph-test-' + uuid.uuid4().hex, directory)

    async def check():
        await build_knowledge_base(dataset, build_database, FakeEmbedder())
        engine = database_engine(build_database)
        try:
            settings = await asyncio.to_thread(service.prepare)
            fingerprint = source_fingerprint(dataset)
            await import_graph(engine, dataset, settings, 'test-build', fingerprint)
            await verify_graph(engine, dataset, settings, 'test-build', fingerprint)
            changes: list[tuple[LiteralString, LiteralString]] = [
                ("MATCH (n:Entity {id:'user-amelia.ward'}) SET n.department='wrong'",
                 "MATCH (n:Entity {id:'user-amelia.ward'}) SET n.department='IT'"),
                ("MATCH (n:Entity {entity_type:'chunk'}) SET n.content='duplicated text'",
                 "MATCH (n:Entity {entity_type:'chunk'}) REMOVE n.content"),
                ("MATCH (n:Entity {entity_type:'chunk'}) SET n.id='wrong-reference'",
                 "MATCH (n:Entity {id:'wrong-reference'}) SET n.id='sample@1.0#access-policy/scope/1'"),
                ("MATCH (a:Entity {id:'user-amelia.ward'})-[r:used_device]->() SET r.times=['2026-10-07T11:05:00Z']",
                 "MATCH (a:Entity {id:'user-amelia.ward'})-[r:used_device]->() SET r.times=['2026-10-07T11:00:00Z']"),
                ("MATCH (a:Entity {id:'group-it-admins'})-[r:grants]->(b:Entity {id:'asset-domain-controller'}), "
                 "(c:Entity {id:'group-all-staff'}) DELETE r CREATE (c)-[:grants]->(b)",
                 "MATCH (a:Entity {id:'group-all-staff'})-[r:grants]->(b:Entity {id:'asset-domain-controller'}), "
                 "(c:Entity {id:'group-it-admins'}) DELETE r CREATE (c)-[:grants]->(b)"),
            ]
            for damage, repair in changes:
                execute(settings, damage)
                with pytest.raises(GraphIntegrityError):
                    await verify_graph(engine, dataset, settings, 'test-build', fingerprint)
                execute(settings, repair)
                await verify_graph(engine, dataset, settings, 'test-build', fingerprint)
            graph = Neo4jQueries(settings, load_log(dataset / 'logins.csv'))
            try:
                moment = parse_utc('2026-10-07T11:00:00Z', 'first_seen')
                finding = Finding(NEW_COUNTRY, 'test witness', ('203.0.113.54',), ('amelia.ward',), 1, 0, 1,
                                  moment, moment, ())
                radius = graph.finding_radius(finding).accounts[0]
                assert [p['person_id'] for p in radius.device_peers] == ['user-emily.foster']
                assert radius.device_paths == [['user-amelia.ward', 'dev-laptop-amelia.ward', 'user-emily.foster']]
                assert [p['person_id'] for p in radius.address_reuse.by_address[0].accounts] == [
                    'user-emily.foster', 'user-isabel.knight']
                for start, end in [('2026-10-07T11:00:00Z', '2026-10-07T11:01:00Z'),
                                   ('2026-10-07T11:01:00Z', '2026-10-07T11:05:00Z')]:
                    assert graph.finding_radius(finding, start, end).accounts[0].device_peers == []
                outside = graph.finding_radius(finding, '2026-09-01', '2026-11-01')
                assert outside.period.outside_record_bounds
                assert outside.permissions_basis == 'organisation snapshot; historical permissions unknown'
            finally:
                graph.close()
        finally:
            await engine.dispose()
            service.remove()

    asyncio.run(check())
