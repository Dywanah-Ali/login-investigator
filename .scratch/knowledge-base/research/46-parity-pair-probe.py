"""DISPOSABLE T46 parity, isolated handoff and paired-build proof.

From repo root:
uv run --project backend --frozen --with neo4j==6.1.0 .scratch/knowledge-base/research/46-parity-pair-probe.py
Uses existing PostgreSQL builder/reader settings without printing them. Creates only fresh
li_test databases and unique Docker resources. Offline embeddings; no external model calls.
"""

import asyncio
import csv
import hashlib
import json
import os
from pathlib import Path
import secrets
import shutil
import statistics
import subprocess
import sys
import time
import uuid

# The backend is a non-packaged uv project. A research script lives outside its import root.
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "backend"))

import neo4j
import psycopg
from neo4j import GraphDatabase
from neo4j.exceptions import AuthError, ServiceUnavailable, SessionExpired
from langchain_core.embeddings import Embeddings

from login_investigator.knowledge_base import build_knowledge_base, open_knowledge_base, reader_settings
from login_investigator.knowledge_base.staleness import source_fingerprint
from login_investigator.loader import load_log, parse_utc
from login_investigator.postgres import ServerSettings, create_fresh_database, drop_database
from login_investigator.rules import detect_all, Finding, NEW_COUNTRY, PASSWORD_SPRAYING
from t46_graph_candidate import source_records, import_graph, readback, lookup, radius, assert_radius, json_shape, run

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DATASET = ROOT / "backend/data/datasets/default"
IMAGE = "neo4j:2026.10.1"
TOKEN = uuid.uuid4().hex[:10]
WORK = HERE / ("li-t46-pair-" + TOKEN)
RESULT = HERE / ("46-parity-pair-result-" + TOKEN + ".json")
REPORT = {"run": TOKEN, "image": IMAGE, "driver": neo4j.__version__,
          "psycopg": psycopg.__version__, "checks": [], "builds": [], "cleanup": []}
PGS = []
INSTANCES = []


class FakeEmbedder(Embeddings):
    def embed_documents(self, texts):
        return [[1.0] + [0.0] * 1535 for _ in texts]

    def embed_query(self, text):
        return self.embed_documents([text])[0]


def check(name, condition=True, **evidence):
    assert condition, name
    REPORT["checks"].append({"name": name, **evidence})
    print(name, flush=True)


def docker(*args):
    return subprocess.run(["docker", *args], check=True, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.strip()


class Instance:
    def __init__(self, suffix):
        self.name = "li-t46-pair-" + TOKEN + "-" + suffix
        self.volume = self.name + "-data"
        self.password = secrets.token_urlsafe(24)
        self.builder_password = secrets.token_urlsafe(24)
        self.env = WORK / (suffix + "-auth") / ".env"
        self.env.parent.mkdir()
        fd = os.open(self.env, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w") as stream:
            stream.write("NEO4J_AUTH=neo4j/" + self.builder_password + "\n")
        self.volume_created = False
        INSTANCES.append(self)
        docker("volume", "create", "--label", "purpose=li-t46-disposable-pair", self.volume)
        self.volume_created = True

    def start(self, serving=False):
        args = ["run", "--detach", "--name", self.name, "--label", "purpose=li-t46-disposable-pair",
                "--publish", "127.0.0.1::7687", "--volume", self.volume + ":/data",
                "--env", "NEO4J_server_memory_heap_initial__size=256m",
                "--env", "NEO4J_server_memory_heap_max__size=512m",
                "--env", "NEO4J_server_memory_pagecache_size=256m"]
        if serving:
            args += ["--env", "NEO4J_server_databases_read__only=neo4j"]
        else:
            args += ["--env-file", str(self.env)]
        docker(*args, IMAGE)
        self.wait(serving)

    def driver(self, builder=False):
        port = int(docker("port", self.name, "7687/tcp").rsplit(":", 1)[1])
        return GraphDatabase.driver(f"bolt://127.0.0.1:{port}",
            auth=("neo4j", self.builder_password) if builder else ("probe_reader", self.password),
            connection_timeout=3, max_transaction_retry_time=0)

    def wait(self, serving=True):
        until = time.monotonic() + 120
        while time.monotonic() < until:
            try:
                with self.driver(builder=not serving) as driver:
                    run(driver, "RETURN 1 AS ready")
                    return
            except (ServiceUnavailable, SessionExpired):
                time.sleep(2)
        raise TimeoutError("Neo4j startup deadline")

    def handoff(self):
        # Distinct credential at handoff. CE still grants it administrative powers.
        with self.driver(builder=True) as driver:
            run(driver, "CREATE USER probe_reader SET PASSWORD $password CHANGE NOT REQUIRED",
                "system", password=self.password)
        with self.driver() as driver:
            run(driver, "DROP USER neo4j", "system")
        docker("stop", self.name)
        docker("rm", self.name)
        self.start(serving=True)
        environment = json.loads(docker("inspect", "--format", "{{json .Config.Env}}", self.name))
        check("serving_container_has_no_builder_credential", not any(self.builder_password in s for s in environment))
        try:
            with self.driver(builder=True) as driver:
                driver.verify_connectivity()
        except AuthError:
            check("retired_builder_login_rejected")
        else:
            raise AssertionError("Builder credential still usable")


async def build_pg(dataset, build_id):
    pg = create_fresh_database(ServerSettings.from_env())
    PGS.append(pg)
    started = time.monotonic()
    await build_knowledge_base(dataset, pg, FakeEmbedder(), reader_role=reader_settings(pg).user)
    fingerprint = source_fingerprint(dataset)
    with psycopg.connect(pg.conninfo()) as connection:
        connection.execute("CREATE TABLE t46_pair (build_id text PRIMARY KEY, fingerprint text, ready boolean)")
        connection.execute("INSERT INTO t46_pair VALUES (%s,%s,true)", (build_id, fingerprint))
        # Existing reader gets the probe marker only; no role changes.
        connection.execute(psycopg.sql.SQL("GRANT SELECT ON t46_pair TO {}").format(
            psycopg.sql.Identifier(reader_settings(pg).user)))
    REPORT["builds"].append({"id": build_id, "postgres": pg.database,
                            "pg_build_seconds": round(time.monotonic()-started, 3), "fingerprint": fingerprint})
    return pg, fingerprint


def build_neo(pg, dataset, build_id, fingerprint, suffix):
    instance = Instance(suffix)
    started = time.monotonic()
    instance.start()
    nodes, edges = source_records(reader_settings(pg), dataset)
    import_started = time.monotonic()
    with instance.driver(builder=True) as driver:
        import_graph(driver, nodes, edges, build_id, fingerprint)
    import_seconds = time.monotonic()-import_started
    instance.handoff()
    with instance.driver() as driver:
        check("independent_source_roundtrip", readback(driver)==(nodes, edges), nodes=len(nodes), edges=len(edges))
        try:
            run(driver, "CREATE (:ForbiddenProbe)")
        except neo4j.exceptions.Neo4jError as error:
            check("handoff_is_read_only", error.code=="Neo.ClientError.General.WriteOnReadOnlyAccessDatabase")
        else:
            raise AssertionError("Writable serving graph")
    REPORT.setdefault("neo_builds", []).append({"resource": instance.name, "build_id": build_id,
        "nodes": len(nodes), "edges": len(edges), "import_seconds": round(import_seconds,3),
        "prepare_and_handoff_seconds": round(time.monotonic()-started,3)})
    return instance


def validate_pair(pg, instance, build_id, fingerprint):
    with psycopg.connect(reader_settings(pg).conninfo()) as connection:
        rows = connection.execute("SELECT build_id,fingerprint,ready FROM t46_pair").fetchall()
        original = connection.execute("SELECT fingerprint FROM build_record").fetchall()
    with instance.driver() as driver:
        graph = run(driver, "MATCH (b:Build) RETURN b.id AS id,b.fingerprint AS fingerprint,b.ready AS ready")
    if rows != [(build_id, fingerprint, True)] or original != [(fingerprint,)] or graph != [
            {"id": build_id, "fingerprint": fingerprint, "ready": True}]:
        raise ValueError("Pair refused")


def activate(pg, instance, build_id, fingerprint):
    validate_pair(pg, instance, build_id, fingerprint)
    pointer = {"build_id": build_id, "postgres": pg.database, "graph": instance.name, "fingerprint": fingerprint}
    temp = WORK / "pointer.tmp"
    temp.write_text(json.dumps(pointer))
    temp.replace(WORK / "active.json")


async def compare(pg, dataset, instance, include_gold=False):
    async with open_knowledge_base(reader_settings(pg), dataset=dataset) as kb:
        with instance.driver() as driver:
            nodes, edges = readback(driver)
            actual_edges = {(a,b,k):json_shape(v) for a,b,k,v in kb.graph.edges(keys=True,data=True)}
            check("networkx_full_graph_parity", nodes==dict(kb.graph.nodes(data=True)) and edges==actual_edges)
            people = [p["username"] for _,p in kb.graph.nodes(data=True) if p["entity_type"]=="person"]
            for username in people + ["AMELIA.WARD", "USER-AMELIA.WARD", "absent-account"]:
                assert lookup(driver, username)==kb.lookup_account(username)
            check("account_lookup_parity", count=len(people)+3)
            log = load_log(dataset / "logins.csv")
            findings = detect_all(log)
            for finding in findings:
                assert_radius(radius(driver, log, finding), kb.finding_radius(finding))
            check("all_detected_findings_full_radius_parity", count=len(findings))
            subject = next(f for f in findings if f.rule==NEW_COUNTRY and "amelia.ward" in f.users)
            windows = [("2026-10-07T11:03:00Z", "2026-10-07T11:11:00Z"),
                       ("2026-10-07T11:07:00Z", "2026-10-07T11:11:00Z"),
                       ("2026-09-01", "2026-11-01"), (None,"2026-09-01")]
            for start,end in windows:
                assert_radius(radius(driver,log,subject,start,end),kb.finding_radius(subject,start,end))
            check("dated_address_and_coverage_parity", count=len(windows))
            s6 = next(f for f in findings if f.rule==PASSWORD_SPRAYING and "45.148.10.80" in f.ips)
            if include_gold:
                answer = radius(driver,log,s6).accounts[0]
                gold=json.loads((dataset/"truth.json").read_text())["scenarios"]["S6"]["blast_radius"]
                check("s6_frozen_gold", [g["group_id"] for g in answer.groups]==gold["groups"]
                    and [a["asset_id"] for a in answer.assets]==gold["assets"]
                    and [p["person_id"] for p in answer.device_peers]==gold["device_peers"]
                    and answer.access_paths==gold["paths"]
                    and [{"network_id":m.network["network_id"],"accounts":[p["person_id"] for p in m.accounts],
                          "paths":m.paths} for m in answer.address_reuse.by_address]==gold["address_reuse_context"]["by_address"])
            # One cold call already occurred. Compare warm samples on this synthetic workload only.
            samples={"networkx_ms":[],"neo4j_ms":[]}
            for _ in range(10):
                tick=time.perf_counter(); kb.finding_radius(s6)
                samples["networkx_ms"].append((time.perf_counter()-tick)*1000)
                tick=time.perf_counter(); radius(driver,log,s6)
                samples["neo4j_ms"].append((time.perf_counter()-tick)*1000)
            REPORT.setdefault("latency",[]).append({"dataset":dataset.name,
                "warm_s6_median_ms":{k:round(statistics.median(v),3) for k,v in samples.items()},
                "samples":samples})
            if not include_gold:
                moment=parse_utc("2026-10-09T11:00:00Z","test")
                f=Finding(NEW_COUNTRY,"synthetic peer witness",("203.0.113.54",),("amelia.ward",),1,0,1,moment,moment,())
                start,end="2026-10-09T11:00:00Z","2026-10-09T11:05:00Z"
                result=radius(driver,log,f,start,end)
                assert_radius(result,kb.finding_radius(f,start,end))
                account=result.accounts[0]
                check("positive_device_witness", [p["person_id"] for p in account.device_peers]==["user-emily.foster"]
                    and account.device_paths==[["user-amelia.ward","dev-laptop-amelia.ward","user-emily.foster"]])
                check("failed_and_empty_device_excluded", [p["person_id"] for p in account.address_reuse.by_address[0].accounts]
                    ==["user-emily.foster","user-isabel.knight"])
                for start,end in [("2026-10-09T11:00:00Z","2026-10-09T11:01:00Z"),
                                  ("2026-10-09T11:01:00Z","2026-10-09T11:05:00Z")]:
                    result=radius(driver,log,f,start,end)
                    assert_radius(result,kb.finding_radius(f,start,end))
                    check("device_peer_needs_both_sides_in_half_open_window", not result.accounts[0].device_peers)


def make_variant():
    dataset=WORK/"variant"
    shutil.copytree(DATASET,dataset)
    with (dataset/"logins.csv").open(newline="") as stream:
        reader=csv.DictReader(stream); columns=reader.fieldnames
        template=next(r for r in reader if r["outcome"]=="success")
    entries=[("amelia.ward","dev-laptop-amelia.ward","success"),
             ("emily.foster","dev-laptop-amelia.ward","success"),
             ("chloe.barker","dev-laptop-amelia.ward","failure"),
             ("amelia.ward","","success"),("isabel.knight","","success")]
    with (dataset/"logins.csv").open("a",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=columns)
        for minute,(user,device,outcome) in enumerate(entries):
            writer.writerow({**template,"username":user,"device_id":device,"outcome":outcome,
                "source_ip":"203.0.113.54","timestamp_utc":f"2026-10-09T11:0{minute}:00Z",
                "failure_reason":"bad_password" if outcome=="failure" else ""})
    return dataset


async def main():
    WORK.mkdir(mode=0o700)
    initial=source_fingerprint(DATASET)
    try:
        a,fa=await build_pg(DATASET,"A-"+TOKEN)
        if "--fail-after-pg" in sys.argv:
            REPORT["injected_failure"] = "after_pg_before_graph_or_publication"
            check("injected_failure_has_no_published_pair", not (WORK/"active.json").exists())
            raise RuntimeError("Intentional T46 failed-build cleanup probe")
        na=build_neo(a,DATASET,"A-"+TOKEN,fa,"a")
        await compare(a,DATASET,na,include_gold=True)
        activate(a,na,"A-"+TOKEN,fa)
        original=(WORK/"active.json").read_bytes()
        variant=make_variant()
        b,fb=await build_pg(variant,"B-"+TOKEN)
        nb=build_neo(b,variant,"B-"+TOKEN,fb,"b")
        await compare(b,variant,nb)
        check("distinct_source_versions",fa!=fb)
        try:
            activate(b,na,"B-"+TOKEN,fb)
        except ValueError:
            check("mixed_build_refused_without_changing_active",(WORK/"active.json").read_bytes()==original)
        else:
            raise AssertionError("Mixed pair accepted")
        with psycopg.connect(b.conninfo()) as connection:
            connection.execute("UPDATE t46_pair SET ready=false")
        try:
            activate(b,nb,"B-"+TOKEN,fb)
        except ValueError:
            check("incomplete_build_refused_without_changing_active",(WORK/"active.json").read_bytes()==original)
        else:
            raise AssertionError("Incomplete pair accepted")
        with psycopg.connect(b.conninfo()) as connection:
            connection.execute("UPDATE t46_pair SET ready=true")
        activate(b,nb,"B-"+TOKEN,fb)
        check("activate_matching_replacement",json.loads((WORK/"active.json").read_text())["build_id"]=="B-"+TOKEN)
        # Explicit rollback uses the retained complete pair, never a mixed partial fallback.
        activate(a,na,"A-"+TOKEN,fa)
        check("rollback_to_previous_pair",(WORK/"active.json").read_bytes()==original)
        docker("stop",nb.name)
        try:
            validate_pair(b,nb,"B-"+TOKEN,fb)
        except (ServiceUnavailable,subprocess.CalledProcessError,ValueError):
            check("unavailable_graph_refused",(WORK/"active.json").read_bytes()==original)
        else:
            raise AssertionError("Unavailable graph accepted")
        recovery=time.monotonic()
        recovered=build_neo(a,DATASET,"A-"+TOKEN,fa,"recovered")
        activate(a,recovered,"A-"+TOKEN,fa)
        await compare(a,DATASET,recovered,include_gold=True)
        REPORT["recovery_rebuild_seconds"]=round(time.monotonic()-recovery,3)
        check("rebuild_and_reactivate_matching_graph")
        REPORT["resource_samples"]=[json.loads(docker("stats","--no-stream","--format","{{json .}}",i.name))
                                    for i in (na,recovered)]
        check("source_dataset_unchanged",source_fingerprint(DATASET)==initial)
        REPORT["completed"]=True
    finally:
        for instance in reversed(INSTANCES):
            for args in (("rm","--force",instance.name),("volume","rm",instance.volume)):
                if not instance.volume_created:
                    break
                try:
                    docker(*args)
                    REPORT["cleanup"].append({"resource":args[-1],"ok":True})
                except subprocess.CalledProcessError:
                    REPORT["cleanup"].append({"resource":args[-1],"ok":False})
        for pg in reversed(PGS):
            try:
                drop_database(pg)
                REPORT["cleanup"].append({"resource":pg.database,"ok":True})
            except psycopg.Error:
                REPORT["cleanup"].append({"resource":pg.database,"ok":False})
        # This unique directory contains only this run's synthetic copies and temporary secrets.
        shutil.rmtree(WORK)
        RESULT.write_text(json.dumps(REPORT,indent=2)+"\n")
        print("Evidence: "+RESULT.name,flush=True)


if __name__=="__main__":
    asyncio.run(main())
