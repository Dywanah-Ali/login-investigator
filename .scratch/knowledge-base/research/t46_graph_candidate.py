"""DISPOSABLE candidate queries for T46. Not application code or a migration adapter."""

import csv
import json
from collections import defaultdict
from dataclasses import asdict

import psycopg
from psycopg import sql
from psycopg.rows import dict_row

from login_investigator.knowledge_base.radius import (
    AccountRadius, AddressMatches, AddressReuse, FindingRadius, _period, _iso,
)
from login_investigator.rules import BRUTE_FORCE, PASSWORD_SPRAYING


KINDS = {"people": ("person", "person_id"), "groups": ("group", "group_id"),
         "assets": ("asset", "asset_id"), "devices": ("device", "device_id"),
         "networks": ("network", "network_id")}
RELATIONS = {"member_of", "grants", "assigned_device", "mentions", "used_device", "used_address"}


def run(driver, statement, database="neo4j", **params):
    with driver.session(database=database) as session:
        return session.run(statement, params).data()


def source_records(pg, dataset):
    """Independent mapping from stored rows and CSV, without using NetworkX export."""
    nodes = {}
    edges = {}
    with psycopg.connect(pg.conninfo(), row_factory=dict_row) as connection:
        for table, (kind, identifier) in KINDS.items():
            for row in connection.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(table))):
                nodes[row[identifier]] = {**row, "entity_type": kind}
        for table, source, target, relation in (
            ("memberships", "person_id", "group_id", "member_of"),
            ("grants", "group_id", "asset_id", "grants"),
            ("device_assignments", "person_id", "device_id", "assigned_device"),
        ):
            for row in connection.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(table))):
                edges[row[source], row[target], relation] = {"relationship": relation}
        for row in connection.execute("SELECT chunk_id, content, langchain_metadata FROM chunks"):
            nodes[row["chunk_id"]] = {"entity_type": "chunk", "content": row["content"],
                                    "metadata": row["langchain_metadata"]}
        for row in connection.execute("SELECT chunk_id, entity_id FROM chunk_mentions_entity"):
            edges[row["chunk_id"], row["entity_id"], "mentions"] = {"relationship": "mentions"}
    people = {p["username"].lower(): key for key, p in nodes.items() if p["entity_type"] == "person"}
    networks = {p["address"]: key for key, p in nodes.items() if p["entity_type"] == "network"}
    observed = defaultdict(set)
    with (dataset / "logins.csv").open(newline="") as stream:
        for row in csv.DictReader(stream):
            if row["outcome"] != "success":
                continue
            subject = people[row["username"].lower()]
            for target, relation in ((networks.get(row["source_ip"]), "used_address"),
                                     (row["device_id"], "used_device")):
                if target:
                    assert target in nodes
                    observed[subject, target, relation].add(row["timestamp_utc"])
    for key, times in observed.items():
        edges[key] = {"relationship": key[2], "times": sorted(times)}
    return nodes, edges


def import_graph(driver, nodes, edges, build_id, fingerprint):
    run(driver, "CREATE CONSTRAINT entity_id IF NOT EXISTS FOR (n:Entity) REQUIRE n.id IS UNIQUE")
    values = [{"id": key, "payload": json.dumps(value, sort_keys=True),
               "kind": value["entity_type"], "username": value.get("username", "").lower()}
              for key, value in nodes.items()]
    run(driver, "UNWIND $rows AS row CREATE (n:Entity) SET n = row", rows=values)
    for relation in sorted(RELATIONS):
        values = [{"source": a, "target": b, "times": value.get("times", []),
                   "payload": json.dumps(value, sort_keys=True)}
                  for (a, b, r), value in edges.items() if r == relation]
        run(driver, "UNWIND $rows AS row MATCH (a:Entity {id:row.source}), (b:Entity {id:row.target}) "
            f"CREATE (a)-[r:{relation}]->(b) SET r.times=row.times, r.payload=row.payload", rows=values)
    # Completion marker is written after all data. Serving validation also reconciles contents.
    run(driver, "CREATE (:Build {id:$id, fingerprint:$fingerprint, ready:true})",
        id=build_id, fingerprint=fingerprint)


def readback(driver):
    nodes = {r["id"]: json.loads(r["payload"])
             for r in run(driver, "MATCH (n:Entity) RETURN n.id AS id, n.payload AS payload")}
    edges = {(r["a"], r["b"], r["relation"]): json.loads(r["payload"])
             for r in run(driver, "MATCH (a:Entity)-[r]->(b:Entity) RETURN a.id AS a, b.id AS b, type(r) AS relation, r.payload AS payload")}
    return nodes, edges


def lookup(driver, account_id):
    rows = run(driver, "MATCH (p:Entity) WHERE p.kind='person' AND "
               "(toLower(p.id)=$id OR p.username=$id) RETURN p.id AS id, p.payload AS payload",
               id=account_id.lower())
    if len(rows) != 1:
        return {"status": "not_found", "account": None, "groups": [], "paths": []}
    row = rows[0]
    groups = run(driver, "MATCH (p:Entity {id:$id})-[:member_of]->(g:Entity) "
                 "RETURN g.id AS id, g.payload AS payload ORDER BY id", id=row["id"])
    return {"status": "found", "account": json.loads(row["payload"]),
            "groups": [json.loads(g["payload"]) for g in groups],
            "paths": [[row["id"], g["id"]] for g in groups]}


def peers(driver, person, relation, lower, upper):
    assert relation in {"used_device", "used_address"}
    return run(driver,
        f"MATCH (p:Entity {{id:$id}})-[a:{relation}]->(shared:Entity)<-[b:{relation}]-(peer:Entity) "
        "WHERE peer.id <> p.id "
        "WITH shared,peer, [t IN a.times WHERE datetime(t)>=datetime($start) AND datetime(t)<datetime($end)] AS subject_times, "
        "[t IN b.times WHERE datetime(t)>=datetime($start) AND datetime(t)<datetime($end)] AS peer_times "
        "WHERE size(subject_times)>0 AND size(peer_times)>0 "
        "RETURN shared.id AS shared_id, shared.payload AS shared_payload, peer.id AS peer_id, "
        "peer.payload AS peer_payload, subject_times, peer_times ORDER BY shared_id,peer_id",
        id=person, start=_iso(lower), end=_iso(upper))


def radius(driver, log, finding, start=None, end=None):
    # Reuse date parsing and public result types; all relationship traversal runs in Cypher.
    period, lower, upper = _period(log, start, end)
    users = {u.lower() for u in finding.users}
    if finding.rule in {BRUTE_FORCE, PASSWORD_SPRAYING}:
        users = {str(row.username).lower() for row in log.itertuples()
                 if row.outcome == "success" and row.source_ip in finding.ips
                 and lower <= row.timestamp_utc < upper}
    accounts = []
    for username in sorted(users):
        account = lookup(driver, username)
        if account["status"] != "found":
            raise ValueError("Account absent")
        person = account["account"]["person_id"]
        assets = run(driver, "MATCH (p:Entity {id:$id})-[:member_of]->(g:Entity)-[:grants]->(a:Entity) "
                     "RETURN g.id AS group_id, a.id AS id, a.payload AS payload ORDER BY group_id,id", id=person)
        asset_map = {a["id"]: json.loads(a["payload"]) for a in assets}
        paths = sorted(account["paths"] + [[person, a["group_id"], a["id"]] for a in assets])
        device = peers(driver, person, "used_device", lower, upper)
        device_map = {p["peer_id"]: json.loads(p["peer_payload"]) for p in device}
        addresses = peers(driver, person, "used_address", lower, upper)
        grouped = []
        for shared in sorted({p["shared_id"] for p in addresses}):
            matches = [p for p in addresses if p["shared_id"] == shared]
            grouped.append(AddressMatches(json.loads(matches[0]["shared_payload"]),
                [json.loads(p["peer_payload"]) for p in matches],
                [[person, shared, p["peer_id"]] for p in matches],
                [{"shared_id": shared, "account_id": p["peer_id"],
                  "subject_times": p["subject_times"], "peer_times": p["peer_times"]} for p in matches]))
        accounts.append(AccountRadius(account["account"], account["groups"],
            [asset_map[key] for key in sorted(asset_map)], paths,
            [device_map[key] for key in sorted(device_map)],
            sorted([person, p["shared_id"], p["peer_id"]] for p in device), AddressReuse(grouped)))
    accounts.sort(key=lambda a: a.account["person_id"])
    return FindingRadius(finding.finding_id, _iso(finding.first_seen), _iso(finding.last_seen), period, accounts)


def json_shape(value):
    return json.loads(json.dumps(value, sort_keys=True, default=str))


def assert_radius(actual, expected):
    assert json_shape(asdict(actual)) == json_shape(asdict(expected)), "Full radius differs"
