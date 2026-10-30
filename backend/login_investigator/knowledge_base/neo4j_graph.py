"""Bounded synchronous Neo4j reads. One driver owns short-lived per-call sessions.

Async callers must dispatch these operations off their event loop (T48). No Neo4j
record, node, relationship or session crosses this core boundary.
"""

from dataclasses import dataclass, field
from typing import Any, LiteralString

import pandas as pd
from neo4j import GraphDatabase, Query
from neo4j.exceptions import DriverError, Neo4jError

from login_investigator.rules import Finding, detect_all, BRUTE_FORCE, PASSWORD_SPRAYING
from .radius import (AccountRadius, AddressMatches, AddressReuse, FindingRadius, GraphWalk,
                     _period, _iso, radius_walk)


class GraphUnavailable(RuntimeError):
    """Fixed public error; connection details and database messages stay private."""


@dataclass(frozen=True)
class GraphSettings:
    uri: str
    user: str
    password: str = field(repr=False)


class Neo4jQueries:
    def __init__(self, settings: GraphSettings, log: pd.DataFrame | None):
        self.log = log
        self.driver = GraphDatabase.driver(
            settings.uri, auth=(settings.user, settings.password), connection_timeout=3,
            connection_acquisition_timeout=5, max_transaction_retry_time=0,
            max_connection_pool_size=8, telemetry_disabled=True,
        )

    def close(self) -> None:
        self.driver.close()

    def _read(self, query: LiteralString, **parameters: Any) -> list[dict[str, Any]]:
        try:
            with self.driver.session(database='neo4j', default_access_mode='READ') as session:
                return session.run(Query(query, timeout=10), parameters).data()
        except (Neo4jError, DriverError):
            raise GraphUnavailable('Neo4j is unavailable; start the selected graph service and retry.') from None

    def lookup_account(self, account_id: str) -> dict[str, Any]:
        rows = self._read("MATCH (p:Entity) WHERE p.entity_type='person' AND "
                          "(toLower(p.id)=$id OR toLower(p.username)=$id) "
                          "RETURN properties(p) AS account", id=account_id.lower())
        if len(rows) != 1:
            return {'status': 'not_found', 'account': None, 'groups': [], 'paths': []}
        person = rows[0]['account']
        groups = self._read("MATCH (:Entity {id:$id})-[:member_of]->(g:Entity) "
                            "RETURN properties(g) AS record ORDER BY g.id", id=person['id'])
        return {'status': 'found', 'account': domain_record(person),
                'groups': [domain_record(row['record']) for row in groups],
                'paths': [[person['id'], row['record']['id']] for row in groups]}

    def account_groups(self, username: str) -> GraphWalk:
        result = self.lookup_account(username)
        if result['status'] != 'found' or result['account']['username'].lower() != username.lower():
            raise ValueError('Account is absent from the organisation')
        return GraphWalk([row['group_id'] for row in result['groups']], result['paths'])

    def finding_walk(self, finding_id: str) -> GraphWalk:
        if self.log is None:
            raise ValueError('Open the knowledge base with its dataset to walk a finding')
        finding = next((item for item in detect_all(self.log) if item.finding_id == finding_id), None)
        if finding is None:
            raise ValueError("No finding has this ID in the dataset's log")
        return radius_walk(self.finding_radius(finding))

    def _peers(self, person: str, relation: str, lower: pd.Timestamp, upper: pd.Timestamp) -> list[dict[str, Any]]:
        # These are the only two supported peer relationships; no caller supplies Cypher.
        queries: dict[str, LiteralString] = {
            'used_device': 'MATCH (p:Entity {id:$id})-[a:used_device]->(shared:Entity)<-[b:used_device]-(peer:Entity) ',
            'used_address': 'MATCH (p:Entity {id:$id})-[a:used_address]->(shared:Entity)<-[b:used_address]-(peer:Entity) ',
        }
        return self._read(queries[relation] +
            'WHERE peer.id <> p.id '
            'WITH shared, peer, [t IN a.times WHERE datetime(t)>=datetime($start) AND datetime(t)<datetime($end)] AS subject_times, '
            '[t IN b.times WHERE datetime(t)>=datetime($start) AND datetime(t)<datetime($end)] AS peer_times '
            'WHERE size(subject_times)>0 AND size(peer_times)>0 '
            'RETURN properties(shared) AS shared, properties(peer) AS peer, subject_times, peer_times '
            'ORDER BY shared.id, peer.id', id=person, start=_iso(lower), end=_iso(upper))

    def finding_radius(self, finding: Finding, start: str | None = None, end: str | None = None) -> FindingRadius:
        if self.log is None:
            raise ValueError('Open the knowledge base with its dataset to compute a radius')
        period, lower, upper = _period(self.log, start, end)
        users = {str(user).lower() for user in finding.users}
        if finding.rule in {BRUTE_FORCE, PASSWORD_SPRAYING}:
            successes = self.log.loc[(self.log['outcome'] == 'success') & self.log['source_ip'].isin(finding.ips)
                                    & (self.log['timestamp_utc'] >= lower) & (self.log['timestamp_utc'] < upper)]
            users = {str(user).lower() for user in successes['username']}
        accounts = []
        for user in sorted(users):
            result = self.lookup_account(user)
            if result['status'] != 'found':
                raise ValueError('Finding names an account absent from the organisation')
            person = result['account']['person_id']
            assets = self._read('MATCH (:Entity {id:$id})-[:member_of]->(g:Entity)-[:grants]->(a:Entity) '
                                'RETURN g.id AS group_id, properties(a) AS asset ORDER BY g.id, a.id', id=person)
            asset_map = {row['asset']['id']: domain_record(row['asset']) for row in assets}
            paths = sorted(result['paths'] + [[person, row['group_id'], row['asset']['id']] for row in assets])
            device = self._peers(person, 'used_device', lower, upper)
            device_map = {row['peer']['id']: domain_record(row['peer']) for row in device}
            address = self._peers(person, 'used_address', lower, upper)
            grouped = []
            for shared in sorted({row['shared']['id'] for row in address}):
                matches = [row for row in address if row['shared']['id'] == shared]
                grouped.append(AddressMatches(domain_record(matches[0]['shared']),
                    [domain_record(row['peer']) for row in matches],
                    [[person, shared, row['peer']['id']] for row in matches],
                    [{'shared_id': shared, 'account_id': row['peer']['id'],
                      'subject_times': row['subject_times'], 'peer_times': row['peer_times']} for row in matches]))
            accounts.append(AccountRadius(result['account'], result['groups'],
                [asset_map[key] for key in sorted(asset_map)], paths,
                [device_map[key] for key in sorted(device_map)],
                sorted([person, row['shared']['id'], row['peer']['id']] for row in device), AddressReuse(grouped)))
        accounts.sort(key=lambda account: account.account['person_id'])
        return FindingRadius(finding.finding_id, _iso(finding.first_seen), _iso(finding.last_seen), period, accounts)


def domain_record(properties: dict[str, Any]) -> dict[str, Any]:
    record = {key: value for key, value in properties.items() if key != 'id'}
    # Neo4j omits null properties; the public organisation contract retains this nullable field.
    if record['entity_type'] == 'network':
        record.setdefault('person_id', None)
    return record
