"""Door 2: the graph is checked against real storage before any walk is used."""

import asyncio
import csv
import json
import shutil
from copy import deepcopy
from pathlib import Path

import pytest
from sqlalchemy import text
from test_knowledge_base import DATASET, FakeEmbedder, sample_dataset
from test_knowledge_base import build_database as build_database  # noqa: PLC0414 - Explicitly expose this imported pytest fixture.

from login_investigator.knowledge_base import (
    GraphIntegrityError,
    KnowledgeBaseNotReady,
    build_knowledge_base,
    database_engine,
    open_knowledge_base,
    reader_settings,
)
from login_investigator.loader import load_log, parse_utc
from login_investigator.postgres import ServerSettings
from login_investigator.rules import NEW_COUNTRY, PASSWORD_SPRAYING, Finding, detect_all


def graph_dataset(tmp_path: Path) -> Path:
    dataset = sample_dataset(tmp_path)
    shutil.copy(DATASET / "logins.csv", dataset / "logins.csv")
    return dataset


def test_open_builds_the_organisation_and_passage_graph(build_database: ServerSettings, tmp_path: Path):
    dataset = graph_dataset(tmp_path)

    async def check():
        await build_knowledge_base(dataset, build_database, FakeEmbedder())
        async with open_knowledge_base(build_database, dataset=dataset) as kb:
            graph = kb.graph
            assert graph.nodes["user-amelia.ward"]["department"] == "IT"
            assert graph.has_edge("user-amelia.ward", "group-it-admins", "member_of")
            assert graph.has_edge("group-it-admins", "asset-domain-controller", "grants")
            chunk = "sample@1.0#access-policy/scope/1"
            assert graph.nodes[chunk]["entity_type"] == "chunk"
            assert graph.has_edge(chunk, "user-thomas.price", "mentions")
            assert graph.has_edge("user-amelia.ward", "net-vpn-4", "used_address")
            await kb.check_graph_integrity()

    asyncio.run(check())


def test_open_graph_refuses_a_dataset_changed_since_build(build_database: ServerSettings, tmp_path: Path):
    dataset = graph_dataset(tmp_path)

    async def check():
        await build_knowledge_base(dataset, build_database, FakeEmbedder())
        with (dataset / "logins.csv").open("a") as handle:
            handle.write("\n")
        with pytest.raises(KnowledgeBaseNotReady):
            async with open_knowledge_base(build_database, dataset=dataset):
                pytest.fail("A graph must not combine a stale database with a newer log")

    asyncio.run(check())


@pytest.mark.parametrize("damage", [
    "person_id", "group_id", "asset_id", "device_id", "network_id", "chunk_id",
    "department", "sensitivity", "owner", "membership", "grant", "assignment", "mention",
    "address", "device", "times", "type", "extra", "swap", "chunk_content",
])
def test_integrity_rejects_corruption(build_database: ServerSettings, tmp_path: Path, damage: str):
    dataset = graph_dataset(tmp_path)

    async def check():
        await build_knowledge_base(dataset, build_database, FakeEmbedder())
        async with open_knowledge_base(build_database, dataset=dataset) as kb:
            graph = deepcopy(kb.graph.copy())
            nodes = {"person_id": "user-amelia.ward", "group_id": "group-it-admins",
                     "asset_id": "asset-domain-controller", "device_id": "dev-laptop-amelia.ward",
                     "network_id": "net-vpn-4", "chunk_id": "sample@1.0#access-policy/scope/1"}
            relationships = {"membership": "member_of", "grant": "grants", "assignment": "assigned_device",
                             "mention": "mentions", "address": "used_address", "device": "used_device"}
            if damage in nodes:
                graph.remove_node(nodes[damage])
            elif damage in relationships:
                edge = next(e for e in graph.edges(keys=True) if e[2] == relationships[damage])
                graph.remove_edge(*edge)
            elif damage in {"department", "sensitivity", "owner"}:
                node, attribute = {"department": ("user-amelia.ward", "department"),
                                   "sensitivity": ("asset-domain-controller", "sensitivity"),
                                   "owner": ("asset-domain-controller", "owner_id")}[damage]
                graph.nodes[node][attribute] = "incorrect"
            elif damage == "times":
                graph["user-amelia.ward"]["net-vpn-4"]["used_address"]["times"] = ()
            elif damage == "type":
                graph["user-amelia.ward"]["group-it-admins"]["member_of"]["relationship"] = "grants"
            elif damage == "extra":
                graph.add_node("invented", entity_type="unknown")
            elif damage == "chunk_content":
                graph.nodes[nodes["chunk_id"]]["content"] = "Changed passage"
            elif damage == "swap":
                # Valid endpoints and identical counts, but wrong grants.
                graph.remove_edge("group-it-admins", "asset-domain-controller", "grants")
                graph.remove_edge("group-all-staff", "asset-email", "grants")
                graph.add_edge("group-it-admins", "asset-email", key="grants", relationship="grants")
                graph.add_edge("group-all-staff", "asset-domain-controller", key="grants", relationship="grants")
            with pytest.raises(GraphIntegrityError):
                await kb.check_graph_integrity(graph)

    asyncio.run(check())


def test_open_rejects_an_isolated_device_from_storage(build_database: ServerSettings, tmp_path: Path):
    dataset = graph_dataset(tmp_path)

    async def check():
        await build_knowledge_base(dataset, build_database, FakeEmbedder())
        engine = database_engine(build_database)
        try:
            async with engine.begin() as connection:
                await connection.execute(text("INSERT INTO devices VALUES ('isolated-device', 'laptop', 'Spare')"))
        finally:
            await engine.dispose()
        with pytest.raises(GraphIntegrityError, match="isolated"):
            async with open_knowledge_base(build_database, dataset=dataset):
                pytest.fail("Opening an invalid graph must fail before yielding it")

    asyncio.run(check())


def test_unmentioned_chunk_and_unused_network_are_valid(build_database: ServerSettings, tmp_path: Path):
    dataset = graph_dataset(tmp_path)
    passage = dataset / "corpus/own/sample.md"
    passage.write_text(passage.read_text().replace("thomas.price", "the responsible team"))

    async def check():
        await build_knowledge_base(dataset, build_database, FakeEmbedder())
        engine = database_engine(build_database)
        try:
            async with engine.begin() as connection:
                await connection.execute(text("INSERT INTO networks VALUES "
                                              "('unused-network', '192.0.2.99', 'vpn', 'Unused', NULL)"))
        finally:
            await engine.dispose()
        async with open_knowledge_base(build_database, dataset=dataset) as kb:
            assert kb.graph.degree("sample@1.0#access-policy/scope/1") == 0
            assert kb.graph.degree("unused-network") == 0

    asyncio.run(check())


def test_s6_radius_matches_the_planted_answer_key(build_database: ServerSettings, tmp_path: Path):
    dataset = DATASET
    gold = json.loads((DATASET / "truth.json").read_text())["scenarios"]["S6"]["blast_radius"]
    finding = next(f for f in detect_all(load_log(dataset / "logins.csv"))
                   if f.rule == PASSWORD_SPRAYING and "45.148.10.80" in f.ips)

    async def check():
        await build_knowledge_base(dataset, build_database, FakeEmbedder())
        async with open_knowledge_base(reader_settings(build_database), dataset=dataset) as kb:
            result = kb.finding_radius(finding)
            assert len(result.accounts) == 1  # Successful account, not all twenty spray targets.
            radius = result.accounts[0]
            assert radius.account["person_id"] == "user-amelia.ward"
            assert [g["group_id"] for g in radius.groups] == gold["groups"]
            assert [a["asset_id"] for a in radius.assets] == gold["assets"]
            assert [p["person_id"] for p in radius.device_peers] == gold["device_peers"]
            context = gold["address_reuse_context"]
            assert [{"network_id": match.network["network_id"],
                     "accounts": [p["person_id"] for p in match.accounts], "paths": match.paths}
                    for match in radius.address_reuse.by_address] == context["by_address"]
            assert radius.access_paths == gold["paths"]
            assert all("sensitivity" in asset and "owner_id" in asset for asset in radius.assets)
            assert result.permissions_basis == "organisation snapshot; historical permissions unknown"
            assert "not evidence of exposure or spread" in radius.address_reuse.meaning
            assert len([node for node, data in kb.graph.nodes(data=True)
                        if data["entity_type"] == "chunk"]) == 320

    asyncio.run(check())


def test_dates_filter_both_sides_and_preserve_requested_coverage(build_database: ServerSettings, tmp_path: Path):
    dataset = graph_dataset(tmp_path)
    finding = next(f for f in detect_all(load_log(dataset / "logins.csv"))
                   if f.rule == NEW_COUNTRY and "amelia.ward" in f.users)

    async def check():
        await build_knowledge_base(dataset, build_database, FakeEmbedder())
        async with open_knowledge_base(build_database, dataset=dataset) as kb:
            radius = kb.finding_radius(finding, "2026-10-07T11:03:00Z", "2026-10-07T11:11:00Z")
            assert len(radius.accounts[0].address_reuse.by_address) == 1
            match = radius.accounts[0].address_reuse.by_address[0]
            assert match.network["network_id"] == "net-vpn-4"
            assert [p["person_id"] for p in match.accounts] == ["user-emily.foster"]
            assert radius.period.effective_start == "2026-10-07T11:03:00Z"
            assert radius.period.effective_end == "2026-10-07T11:11:00Z"
            # The subject also needs an observation in the period; a peer's observation alone
            # must not use the subject's earlier graph edge to manufacture a shared address.
            no_subject = kb.finding_radius(finding, "2026-10-07T11:07:00Z", "2026-10-07T11:11:00Z")
            assert no_subject.accounts[0].address_reuse.by_address == []
            assert no_subject.accounts[0].device_peers == []
            wide = kb.finding_radius(finding, "2026-09-01", "2026-11-01")
            assert wide.period.outside_record_bounds
            assert wide.period.requested_start == "2026-09-01T00:00:00Z"
            assert wide.period.first_record.startswith("2026-10-01")
            assert wide.period.last_record == "2026-10-08T08:59:48Z"
            for start, end in [("today", None), ("2026-10-08", "2026-10-01")]:
                with pytest.raises(ValueError):
                    kb.finding_radius(finding, start, end)
            before = kb.finding_radius(finding, end="2026-09-01")
            assert before.accounts[0].address_reuse.by_address == []
            assert before.period.outside_record_bounds
            assert before.period.effective_start is None and before.period.effective_end is None
            # Snapshot permissions stay present and explicitly labelled even outside log bounds.
            assert len(before.accounts[0].assets) == 7

    asyncio.run(check())


def test_successful_observations_make_peers_but_failures_and_empty_devices_do_not(
    build_database: ServerSettings, tmp_path: Path,
):
    dataset = graph_dataset(tmp_path)
    with (dataset / "logins.csv").open() as handle:
        reader = csv.DictReader(handle)
        columns = reader.fieldnames
        template = next(row for row in reader if row["outcome"] == "success")
    assert columns is not None
    entries = [
        ("amelia.ward", "dev-laptop-amelia.ward", "success"),
        ("emily.foster", "dev-laptop-amelia.ward", "success"),
        ("chloe.barker", "dev-laptop-amelia.ward", "failure"),
        ("amelia.ward", "", "success"),
        ("isabel.knight", "", "success"),
    ]
    with (dataset / "logins.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for minute, (user, device, outcome) in enumerate(entries):
            writer.writerow({**template, "username": user, "device_id": device, "outcome": outcome,
                             "source_ip": "203.0.113.54", "timestamp_utc": f"2026-10-07T11:0{minute}:00Z",
                             "failure_reason": "bad_password" if outcome == "failure" else ""})
    finding = Finding(NEW_COUNTRY, "test observation", ("203.0.113.54",), ("amelia.ward",),
                      1, 0, 1, parse_utc("2026-10-07T11:00:00Z", "first_seen"),
                      parse_utc("2026-10-07T11:00:00Z", "last_seen"), ())

    async def check():
        await build_knowledge_base(dataset, build_database, FakeEmbedder())
        async with open_knowledge_base(build_database, dataset=dataset) as kb:
            radius = kb.finding_radius(finding).accounts[0]
            assert [peer["person_id"] for peer in radius.device_peers] == ["user-emily.foster"]
            assert radius.device_paths == [["user-amelia.ward", "dev-laptop-amelia.ward", "user-emily.foster"]]
            assert [peer["person_id"] for peer in radius.address_reuse.by_address[0].accounts] == [
                "user-emily.foster", "user-isabel.knight"]
            assert not kb.graph.has_edge("user-chloe.barker", "net-vpn-4", "used_address")
            assert "" not in kb.graph
            assert kb.finding_radius(finding, "2026-10-07T11:03:00Z").accounts[0].device_peers == []

    asyncio.run(check())
