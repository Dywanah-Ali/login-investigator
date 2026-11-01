"""Door 2: the graph is checked against real storage before any walk is used."""

import asyncio
import json
import shutil
from pathlib import Path

import pytest
from test_knowledge_base import DATASET, sample_dataset
from test_knowledge_base import build_database as build_database  # noqa: PLC0414 - Explicitly expose this imported pytest fixture.

from login_investigator.knowledge_base.graph_version import open_version
from login_investigator.loader import load_log
from login_investigator.postgres import ServerSettings
from login_investigator.rules import NEW_COUNTRY, PASSWORD_SPRAYING, detect_all


def graph_dataset(tmp_path: Path) -> Path:
    dataset = sample_dataset(tmp_path)
    shutil.copy(DATASET / "logins.csv", dataset / "logins.csv")
    return dataset


def test_s6_radius_matches_the_planted_answer_key(paired_default):
    dataset = DATASET
    gold = json.loads((DATASET / "truth.json").read_text())["scenarios"]["S6"]["blast_radius"]
    finding = next(f for f in detect_all(load_log(dataset / "logins.csv"))
                   if f.rule == PASSWORD_SPRAYING and "45.148.10.80" in f.ips)

    async def check():
        async with open_version(paired_default.marker, ServerSettings.from_env()) as kb:
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
            assert (await kb.check_graph_integrity()).nodes["chunk"] == 320

    asyncio.run(check())


def test_dates_filter_both_sides_and_preserve_requested_coverage(paired_default):
    dataset = DATASET
    finding = next(f for f in detect_all(load_log(dataset / "logins.csv"))
                   if f.rule == NEW_COUNTRY and "amelia.ward" in f.users)

    async def check():
        async with open_version(paired_default.marker, ServerSettings.from_env()) as kb:
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
