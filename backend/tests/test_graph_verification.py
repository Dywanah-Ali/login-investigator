"""Door 2: independent corruption refusal and a positive dated device witness."""

import asyncio
import csv
import uuid
from pathlib import Path
from typing import LiteralString, cast

import pytest
from test_knowledge_base import FakeEmbedder
from test_knowledge_base import build_database as build_database  # noqa: PLC0414 - Explicitly expose this imported pytest fixture.
from test_knowledge_graph import graph_dataset

from login_investigator.knowledge_base import (
    GraphIntegrityError,
    build_knowledge_base,
    database_engine,
)
from login_investigator.knowledge_base.graph_ingestion import import_graph
from login_investigator.knowledge_base.graph_service import GraphService, execute
from login_investigator.knowledge_base.graph_verification import verify_graph
from login_investigator.knowledge_base.neo4j_graph import Neo4jQueries
from login_investigator.knowledge_base.staleness import source_fingerprint
from login_investigator.loader import load_log, parse_utc
from login_investigator.postgres import ServerSettings
from login_investigator.rules import NEW_COUNTRY, Finding


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
    with (dataset / 'org/networks.csv').open('a') as handle:
        handle.write('unused-network,192.0.2.99,vpn,Unused,\n')
    mentioned = passage.parent / 'mentioned.md'
    mentioned.write_text(passage.read_text().replace('id: "sample"', 'id: "mentioned"')
                        .replace('the responsible team', 'thomas.price'))
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
                ("MATCH (n:Entity {id:'sample@1.0#access-policy/scope/1'}) SET n.id='wrong-reference'",
                 "MATCH (n:Entity {id:'wrong-reference'}) SET n.id='sample@1.0#access-policy/scope/1'"),
                ("MATCH (a:Entity {id:'user-amelia.ward'})-[r:used_device]->() SET r.times=['2026-10-07T11:05:00Z']",
                 "MATCH (a:Entity {id:'user-amelia.ward'})-[r:used_device]->() SET r.times=['2026-10-07T11:00:00Z']"),
                (("MATCH (a:Entity {id:'group-it-admins'})-[r:grants]->(b:Entity {id:'asset-domain-controller'}), "
                 "(c:Entity {id:'group-all-staff'}) DELETE r CREATE (c)-[:grants]->(b)"),
                 ("MATCH (a:Entity {id:'group-all-staff'})-[r:grants]->(b:Entity {id:'asset-domain-controller'}), "
                 "(c:Entity {id:'group-it-admins'}) DELETE r CREATE (c)-[:grants]->(b)")),
            ]
            for damage, repair in changes:
                execute(settings, damage)
                with pytest.raises(GraphIntegrityError):
                    await verify_graph(engine, dataset, settings, 'test-build', fingerprint)
                execute(settings, repair)
                await verify_graph(engine, dataset, settings, 'test-build', fingerprint)
            for identifier in ['user-amelia.ward', 'group-it-admins', 'asset-domain-controller',
                               'dev-laptop-amelia.ward', 'net-vpn-4', 'sample@1.0#access-policy/scope/1']:
                execute(settings, 'MATCH (n:Entity {id:$id}) SET n.id="missing-identity"', id=identifier)
                with pytest.raises(GraphIntegrityError):
                    await verify_graph(engine, dataset, settings, 'test-build', fingerprint)
                execute(settings, 'MATCH (n:Entity {id:"missing-identity"}) SET n.id=$id', id=identifier)
            extra_changes: list[tuple[LiteralString, LiteralString]] = [
                ("CREATE (:Entity {id:'invented', entity_type:'unknown'})",
                 "MATCH (n:Entity {id:'invented'}) DELETE n"),
                ("MATCH (n:Entity {id:'user-amelia.ward'}) SET n:Unexpected",
                 "MATCH (n:Entity {id:'user-amelia.ward'}) REMOVE n:Unexpected"),
            ]
            # Restore source attributes from independently read rows, never guessed literals.
            with (dataset / 'org/assets.csv').open() as handle:
                asset = next(r for r in csv.DictReader(handle) if r['asset_id'] == 'asset-domain-controller')
            attribute_changes: list[tuple[LiteralString, str]] = [
                ('MATCH (n:Entity {id:"asset-domain-controller"}) SET n.sensitivity=$value', asset['sensitivity']),
                ('MATCH (n:Entity {id:"asset-domain-controller"}) SET n.owner_id=$value', asset['owner_id']),
            ]
            for statement, original in attribute_changes:
                execute(settings, statement, value='wrong')
                with pytest.raises(GraphIntegrityError):
                    await verify_graph(engine, dataset, settings, 'test-build', fingerprint)
                execute(settings, statement, value=original)
            for damage, repair in extra_changes:
                execute(settings, damage)
                with pytest.raises(GraphIntegrityError):
                    await verify_graph(engine, dataset, settings, 'test-build', fingerprint)
                execute(settings, repair)
            for relation in ['member_of', 'grants', 'assigned_device', 'mentions', 'used_address', 'used_device']:
                edge = execute(settings,
                    'MATCH (a)-[r]->(b) WHERE type(r)=$relation '
                    'RETURN a.id AS source, b.id AS target, properties(r) AS properties LIMIT 1',
                    relation=relation)[0]
                execute(settings, 'MATCH (a {id:$source})-[r]->(b {id:$target}) '
                        'WHERE type(r)=$relation DELETE r', relation=relation,
                        source=edge['source'], target=edge['target'])
                with pytest.raises(GraphIntegrityError):
                    await verify_graph(engine, dataset, settings, 'test-build', fingerprint)
                # The relationship type is from the fixed test list, never source/model text.
                execute(settings, cast(LiteralString,
                    f'MATCH (a {{id:$source}}), (b {{id:$target}}) CREATE (a)-[r:{relation}]->(b) SET r=$properties'),
                    **edge)
                # Corrupt one relationship's recorded attributes, independent of entity count.
                execute(settings, 'MATCH ()-[r]->() WHERE type(r)=$relation WITH r LIMIT 1 SET r.unexpected=true', relation=relation)
                with pytest.raises(GraphIntegrityError):
                    await verify_graph(engine, dataset, settings, 'test-build', fingerprint)
                execute(settings, 'MATCH ()-[r]->() WHERE type(r)=$relation REMOVE r.unexpected', relation=relation)
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
