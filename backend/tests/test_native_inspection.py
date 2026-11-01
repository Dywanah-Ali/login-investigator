"""Browser query results must preserve core identities, including peer edge direction."""

import asyncio
import csv
import json
import shutil
from pathlib import Path

import pytest
from test_knowledge_base import DATASET, FakeEmbedder

from login_investigator.knowledge_base.graph_version import (
    build_version,
    open_version,
    remove_version,
)
from login_investigator.knowledge_base.inspection import (
    FINDING,
    ORGANISATION,
    finding_parameters,
)
from login_investigator.knowledge_base.inspection import prepare_inspection as prepare
from login_investigator.knowledge_base.neo4j_graph import Neo4jQueries
from login_investigator.knowledge_base.radius import radius_neighbourhood
from login_investigator.loader import load_log
from login_investigator.postgres import ServerSettings
from login_investigator.rules import detect_all


def source_organisation(dataset):
    """Independent Browser oracle from source rows, excluding passage references."""
    tables = {}
    nodes = set()
    for name, key in [('people', 'person_id'), ('groups', 'group_id'), ('assets', 'asset_id'),
                      ('devices', 'device_id'), ('networks', 'network_id')]:
        with (dataset / 'org' / (name + '.csv')).open() as handle:
            tables[name] = list(csv.DictReader(handle))
        nodes.update(row[key] for row in tables[name])
    edges = set()
    for name, left, right, relation in [('memberships', 'person_id', 'group_id', 'member_of'),
                                      ('grants', 'group_id', 'asset_id', 'grants'),
                                      ('device_assignments', 'person_id', 'device_id', 'assigned_device')]:
        with (dataset / 'org' / (name + '.csv')).open() as handle:
            edges.update((row[left], row[right], relation) for row in csv.DictReader(handle))
    people = {r['username'].lower(): r['person_id'] for r in tables['people']}
    addresses = {r['address']: r['network_id'] for r in tables['networks']}
    with (dataset / 'logins.csv').open() as handle:
        for row in csv.DictReader(handle):
            if row['outcome'] == 'success':
                person = people[row['username'].lower()]
                if row['device_id']:
                    edges.add((person, row['device_id'], 'used_device'))
                if row['source_ip'] in addresses:
                    edges.add((person, addresses[row['source_ip']], 'used_address'))
    return nodes, edges


def identities(graph, query, parameters):
    with graph.driver.session(database='neo4j', default_access_mode='READ') as session:
        row = session.run(query, parameters).single()
        if row is None:
            return None
        nodes = {node['id'] for node in row['nodes']}
        edges = {(edge.start_node['id'], edge.end_node['id'], edge.type) for edge in row['relationships']}
        assert len(nodes) == row['node_count']
        assert len(edges) == row['relationship_count']
        return nodes, edges


def test_browser_queries_equal_checked_core_and_reject_wrong_build(tmp_path: Path):
    async def check():
        server = ServerSettings.from_env()
        dataset = tmp_path / 'dataset'
        shutil.copytree(DATASET, dataset)
        # The default findings have no device peers. Plant one in this disposable source.
        with (dataset / 'logins.csv').open() as handle:
            reader = csv.DictReader(handle)
            columns = reader.fieldnames
            row = next(r for r in reader if r['username'] == 'amelia.ward'
                       and r['outcome'] == 'success' and r['device_id'])
        assert columns is not None
        with (dataset / 'logins.csv').open('a', newline='') as handle:
            csv.DictWriter(handle, fieldnames=columns).writerow({**row, 'username': 'emily.foster'})
        version = await build_version(dataset, tmp_path / 'versions', server, FakeEmbedder())
        try:
            params = {'build_id': version.build_id, 'fingerprint': version.fingerprint}
            async with open_version(version.marker, server) as kb:
                graph = kb.graph_queries
                assert isinstance(graph, Neo4jQueries)
                org_nodes, org_edges = source_organisation(version.snapshot)
                assert identities(graph, ORGANISATION, params) == (org_nodes, org_edges)
                saw_device_peer = saw_address = saw_empty = False
                selection = {**params, "nodes": [], "edges": []}
                for finding in detect_all(load_log(version.snapshot / 'logins.csv')):
                    radius = kb.finding_radius(finding)
                    expected_nodes = {a.account['person_id'] for a in radius.accounts}
                    expected_edges = set()
                    # Independent oracle from the public result, not the projection helper.
                    for account in radius.accounts:
                        for group in account.groups:
                            expected_edges.add((account.account['person_id'], group['group_id'], 'member_of'))
                        for path in account.access_paths:
                            if len(path) == 3:
                                expected_edges.add((path[1], path[2], 'grants'))
                        peer_paths = [(p, 'used_device') for p in account.device_paths]
                        peer_paths += [(p, 'used_address') for m in account.address_reuse.by_address for p in m.paths]
                        for (person, shared, peer), relation in peer_paths:
                            expected_edges.add((person, shared, relation))
                            expected_edges.add((peer, shared, relation))
                        saw_device_peer |= bool(account.device_peers)
                        saw_address |= bool(account.address_reuse.by_address)
                    expected_nodes.update(n for a, b, _ in expected_edges for n in (a, b))
                    saw_empty |= not radius.accounts
                    selection = finding_parameters(radius, version.build_id, version.fingerprint)
                    assert identities(graph, FINDING, selection) == (expected_nodes, expected_edges)
                    assert set(radius_neighbourhood(radius).edges) == expected_edges
                assert saw_device_peer and saw_address and saw_empty
                from neo4j import Query

                from login_investigator.knowledge_base.inspection import (
                    browser_parameters,
                )
                # Execute the actual generated command's expression, including escaping.
                escaped = {**selection, 'nodes': ['quote" slash\\ newline\n'], 'edges': []}
                with graph.driver.session(database='neo4j', default_access_mode='READ') as session:
                    for values in (params, escaped):
                        expression = browser_parameters(values).removeprefix(':params ').strip()
                        from typing import LiteralString, cast
                        row = session.run(Query(cast(LiteralString, 'RETURN ' + expression + ' AS params'))).single()
                        assert row is not None and row['params'] == values
                assert identities(graph, ORGANISATION, {**params, 'build_id': 'wrong'}) is None
                assert identities(graph, FINDING, {**selection, 'fingerprint': 'wrong'}) is None
                broken = {**selection, 'nodes': ['missing'], 'edges': []}
                assert graph._read(FINDING, **broken)[0]['complete'] is False
            output = tmp_path / 'inspection'
            report = await prepare(version.marker, output)
            assert report['organisation_nodes'] == len(org_nodes)
            assert report['organisation_relationships'] == len(org_edges)
            assert (output / 'finding.cypher').read_text() == FINDING + ';\n'
            assert (output / 'organisation.cypher').read_text() == ORGANISATION + ';\n'
            assert json.loads((output / 'inspection.json').read_text()) == report
            from urllib.request import urlopen

            def check_browser():
                with urlopen(str(report['browser_url']), timeout=10) as response:
                    assert response.status == 200
                    assert b'Neo4j' in response.read()

            await asyncio.to_thread(check_browser)
            with pytest.raises(FileExistsError):
                await prepare(version.marker, output)
            with pytest.raises(ValueError, match='No finding'):
                await prepare(version.marker, tmp_path / 'invalid', 'unknown')
            with pytest.raises(ValueError, match='outside'):
                await prepare(version.marker, version.snapshot / 'inspection')
            assert not (tmp_path / 'invalid').exists()
        finally:
            remove_version(version, server)
    asyncio.run(check())


def test_browser_parameter_map_round_trips_as_cypher():
    # Runtime evaluation is covered by the paired test; pin the Browser command syntax here.
    from login_investigator.knowledge_base.inspection import browser_parameters
    assert browser_parameters({'build_id': 'a"b', 'nodes': ['x\\y']}) == ':params {build_id: "a\\"b", nodes: ["x\\\\y"]}\n'
    with pytest.raises(ValueError, match='Unsupported'):
        browser_parameters({'untrusted key': 'value'})
