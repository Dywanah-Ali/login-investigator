"""DISPOSABLE T46 proof. No application imports or active database access.

Run: uv run --no-project --with neo4j==6.1.0 <this-file>
Requires a running Docker engine. Creates and cleans only uniquely named probe resources.
Credentials exist only in a temporary .env and process memory; output contains no secrets.
"""

import json
import os
from pathlib import Path
import secrets
import subprocess
import time
import uuid

import neo4j
from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError, ServiceUnavailable, SessionExpired


HERE = Path(__file__).resolve().parent
IMAGE = "neo4j:2026.10.1"
NAME = "li-t46-security-" + uuid.uuid4().hex[:10]
VOLUME = NAME + "-data"
RUN = HERE / NAME
RESULT = HERE / "46-community-security-result.json"
REPORT = {"image": IMAGE, "driver": neo4j.__version__, "resource": NAME, "checks": []}


def docker(*args):
    return subprocess.run(["docker", *args], check=True, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.strip()


def connect(user, password):
    binding = docker("port", NAME, "7687/tcp")
    port = int(binding.rsplit(":", 1)[1])
    return GraphDatabase.driver(f"bolt://127.0.0.1:{port}", auth=(user, password),
                               connection_timeout=3, max_transaction_retry_time=0)


def wait_ready(user, password):
    deadline = time.monotonic() + 120
    while time.monotonic() < deadline:
        try:
            with connect(user, password) as driver:
                driver.verify_connectivity()
                return
        except (ServiceUnavailable, SessionExpired):
            time.sleep(2)
    raise TimeoutError("Probe server did not become ready")


def query(driver, cypher, database="neo4j", **params):
    # Default write access deliberately avoids client-side read-mode rejection.
    with driver.session(database=database) as session:
        return session.run(cypher, params).data()


def attempt(driver, phase, name, cypher, database="neo4j", **params):
    try:
        query(driver, cypher, database, **params)
        result = {"phase": phase, "check": name, "outcome": "allowed"}
    except Neo4jError as error:
        result = {"phase": phase, "check": name, "outcome": "rejected", "code": error.code}
    REPORT["checks"].append(result)
    print(json.dumps(result), flush=True)


def snapshot(driver):
    return {
        "nodes": query(driver, "MATCH (n:Probe) RETURN n.id AS id, n.value AS value ORDER BY id"),
        "edges": query(driver, "MATCH (a:Probe)-[r]->(b:Probe) RETURN a.id AS source, type(r) AS type, b.id AS target ORDER BY source, type, target"),
    }


def start(read_only=False):
    args = ["run", "--detach", "--name", NAME,
            "--label", "purpose=li-t46-disposable-security",
            "--publish", "127.0.0.1::7687", "--volume", VOLUME + ":/data",
            "--env-file", str(RUN / ".env"),
            "--env", "NEO4J_server_memory_heap_initial__size=256m",
            "--env", "NEO4J_server_memory_heap_max__size=512m",
            "--env", "NEO4J_server_memory_pagecache_size=256m"]
    if read_only:
        args.extend(["--env", "NEO4J_server_databases_read__only=neo4j"])
    docker(*args, IMAGE)


def main():
    builder_password = secrets.token_urlsafe(24)
    reader_password = secrets.token_urlsafe(24)
    other_password = secrets.token_urlsafe(24)
    created_volume = False
    RUN.mkdir(mode=0o700)
    env_path = RUN / ".env"
    fd = os.open(env_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w") as stream:
        stream.write("NEO4J_AUTH=neo4j/" + builder_password + "\n")
    try:
        docker("version", "--format", "{{.Server.Version}}")
        docker("volume", "create", "--label", "purpose=li-t46-disposable-security", VOLUME)
        created_volume = True
        start()
        wait_ready("neo4j", builder_password)
        with connect("neo4j", builder_password) as driver:
            REPORT["server"] = query(driver, "CALL dbms.components() YIELD name, versions, edition RETURN name, versions, edition")
            query(driver, "CREATE (a:Probe {id: 1, value: 'original'}), (b:Probe {id: 2, value: 'original'}), (a)-[:LINK]->(b)")
            query(driver, "CREATE USER probe_reader SET PASSWORD $password CHANGE NOT REQUIRED", "system", password=reader_password)
            REPORT["baseline"] = snapshot(driver)
        docker("stop", NAME)
        docker("rm", NAME)
        start(read_only=True)
        wait_ready("probe_reader", reader_password)
        for phase in ("read_only_start", "after_restart"):
            if phase == "after_restart":
                docker("restart", NAME)
                wait_ready("probe_reader", reader_password)
            with connect("probe_reader", reader_password) as driver:
                REPORT[phase + "_read"] = snapshot(driver)
                for name, cypher in (
                    ("create_node", "CREATE (:Probe {id: 3})"),
                    ("update_node", "MATCH (n:Probe {id: 1}) SET n.value = 'changed'"),
                    ("create_relationship", "MATCH (a:Probe {id: 1}), (b:Probe {id: 2}) CREATE (b)-[:EXTRA]->(a)"),
                    ("delete_relationship", "MATCH (:Probe)-[r:LINK]->(:Probe) DELETE r"),
                    ("delete_node", "MATCH (n:Probe {id: 2}) DETACH DELETE n"),
                    ("create_index", "CREATE INDEX probe_index IF NOT EXISTS FOR (n:Probe) ON (n.value)"),
                ):
                    attempt(driver, phase, name, cypher)
                attempt(driver, phase, "change_read_only_setting", "CALL dbms.setConfigValue('server.databases.read_only', '')", "system")
                attempt(driver, phase, "alter_access", "ALTER DATABASE neo4j SET ACCESS READ WRITE", "system")
                attempt(driver, phase, "create_user", "CREATE USER probe_other SET PASSWORD $password CHANGE NOT REQUIRED", "system", password=other_password)
                attempt(driver, phase, "alter_other_user", "ALTER USER probe_other SET PASSWORD $password CHANGE NOT REQUIRED", "system", password=secrets.token_urlsafe(24))
                attempt(driver, phase, "drop_user", "DROP USER probe_other", "system")
                attempt(driver, phase, "write_after_bypass_attempts", "CREATE (:Probe {id: 4})")
                REPORT[phase + "_after"] = snapshot(driver)
        REPORT["completed"] = True
    finally:
        # Only resources created by this invocation are eligible for cleanup.
        cleanup = []
        for args in (("rm", "--force", NAME), ("volume", "rm", VOLUME)):
            if not created_volume:
                break
            try:
                docker(*args)
                cleanup.append({"operation": args[0], "ok": True})
            except subprocess.CalledProcessError:
                cleanup.append({"operation": args[0], "ok": False})
        REPORT["cleanup"] = cleanup
        env_path.unlink(missing_ok=True)
        RUN.rmdir()
        RESULT.write_text(json.dumps(REPORT, indent=2) + "\n")
        print("Evidence: " + RESULT.name, flush=True)


if __name__ == "__main__":
    main()
