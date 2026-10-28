"""Door 2: the Gephi export writes the checked graph, and nothing in the API serves it."""

import ast
import asyncio
import csv
import json
import re
import xml.etree.ElementTree as ElementTree
from collections import Counter
from pathlib import Path

import networkx as nx
import pytest

from login_investigator.knowledge_base import build_knowledge_base, open_knowledge_base, reader_settings
from login_investigator.knowledge_base.gexf import (
    NODE_COLOURS, RESERVED, ExportRefused, finding_neighbourhood, write_gexf,
)
from login_investigator.loader import load_log, parse_utc
from login_investigator.postgres import ServerSettings
from login_investigator.rules import NEW_COUNTRY, PASSWORD_SPRAYING, Finding, detect_all
from scripts.export_graph import main
from test_knowledge_base import DATASET, FakeEmbedder, build_database  # noqa: F401
from test_knowledge_graph import graph_dataset

API = Path(__file__).resolve().parents[1] / "api"
# The names the ticket and T08 d9 forbid. The module refuses a wider set the writer also consumes.
TICKET_RESERVED = ("id", "label", "pid")


def declared_attributes(path: Path) -> set[str]:
    return {str(element.get("title")) for element in ElementTree.parse(path).iter()
            if element.tag.endswith("}attribute")}


def relationships(graph: nx.Graph) -> set[tuple[str, str, str]]:
    return {(source, target, data["relationship"]) for source, target, data in graph.edges(data=True)}


def test_whole_graph_and_s6_neighbourhood_read_back_as_checked(build_database: ServerSettings, tmp_path: Path):
    gold = json.loads((DATASET / "truth.json").read_text())["scenarios"]["S6"]["blast_radius"]
    findings = detect_all(load_log(DATASET / "logins.csv"))
    s6 = next(f for f in findings if f.rule == PASSWORD_SPRAYING and "45.148.10.80" in f.ips)
    whole, neighbourhood = tmp_path / "graph.gexf", tmp_path / "s6.gexf"

    async def check():
        await build_knowledge_base(DATASET, build_database, FakeEmbedder())
        async with open_knowledge_base(reader_settings(build_database), dataset=DATASET) as kb:
            counts = await kb.check_graph_integrity()
            kb.export_gexf(whole)
            kb.export_gexf(neighbourhood, s6.finding_id)
            for finding_id, reason in (("F-unknown-00000000", "No finding"),
                                       (next(f.finding_id for f in findings if not kb.finding_radius(f).accounts),
                                        "no account")):
                with pytest.raises(ExportRefused, match=reason):
                    kb.export_gexf(tmp_path / "refused.gexf", finding_id)
            assert not (tmp_path / "refused.gexf").exists()
            return counts

    counts = asyncio.run(check())

    graph = nx.read_gexf(whole)
    assert dict(Counter(data["entity_type"] for _, data in graph.nodes(data=True))) == counts.nodes
    assert dict(Counter(data["relationship"] for _, _, data in graph.edges(data=True))) == counts.edges
    assert counts.nodes["chunk"] == 320
    amelia = graph.nodes["user-amelia.ward"]
    assert amelia["department"] == "IT"
    # The reader supplies alpha 1.0 when the file has none.
    assert amelia["viz"]["color"] == {**NODE_COLOURS["person"], "a": 1.0}
    assert all(data["viz"]["color"] == {**NODE_COLOURS[data["entity_type"]], "a": 1.0}
               for _, data in graph.nodes(data=True))
    # The file itself has no alpha: Gephi Lite ignores a viz colour that carries one
    # (gephi-lite issue #307, B-097).
    colours = [element for element in ElementTree.parse(whole).iter() if element.tag.endswith("}color")]
    assert len(colours) == sum(counts.nodes.values())
    assert all(set(element.attrib) == {"r", "g", "b"} for element in colours)
    times = graph["user-amelia.ward"]["net-vpn-4"]["used_address"]["times"]
    assert re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ(, \d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ)*", times)
    # The module's wider set. The writer itself declares `networkx_key` to carry each edge's key.
    assert declared_attributes(whole) & RESERVED == {"networkx_key"}
    assert "entity_type" in declared_attributes(whole)

    # The neighbourhood is S6's radius, computed independently from the answer key.
    subject = "user-amelia.ward"
    reuse = gold["address_reuse_context"]["by_address"]
    expected_nodes = ({subject, *gold["groups"], *gold["assets"], *gold["device_peers"]}
                      | {match["network_id"] for match in reuse}
                      | {account for match in reuse for account in match["accounts"]})
    expected_edges = {(path[0], path[1], "member_of") for path in gold["paths"]}
    expected_edges |= {(path[1], path[2], "grants") for path in gold["paths"] if len(path) == 3}
    expected_edges |= {(person, match["network_id"], "used_address")
                       for match in reuse for path in match["paths"] for person in (path[0], path[2])}
    s6_graph = nx.read_gexf(neighbourhood)
    assert set(s6_graph) == expected_nodes
    assert relationships(s6_graph) == expected_edges
    assert declared_attributes(neighbourhood) & RESERVED == {"networkx_key"}


@pytest.mark.parametrize("name", TICKET_RESERVED)
@pytest.mark.parametrize("on", ["node", "edge"])
def test_reserved_attribute_names_fail_loudly(tmp_path: Path, name: str, on: str):
    graph = nx.MultiDiGraph()
    graph.add_node("user-a", entity_type="person", **({name: "x"} if on == "node" else {}))
    graph.add_node("group-a", entity_type="group")
    graph.add_edge("user-a", "group-a", key="member_of", relationship="member_of",
                   **({name: "x"} if on == "edge" else {}))
    with pytest.raises(ExportRefused, match=f"'{name}'"):
        write_gexf(graph, tmp_path / "graph.gexf")
    assert not (tmp_path / "graph.gexf").exists()


def test_neighbourhood_draws_device_peers_and_shared_addresses(build_database: ServerSettings, tmp_path: Path):
    dataset = graph_dataset(tmp_path / "dataset")
    with (dataset / "logins.csv").open() as handle:
        reader = csv.DictReader(handle)
        columns = reader.fieldnames
        template = next(row for row in reader if row["outcome"] == "success")
    assert columns is not None
    with (dataset / "logins.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for minute, user in enumerate(["amelia.ward", "emily.foster"]):
            writer.writerow({**template, "username": user, "device_id": "dev-laptop-amelia.ward",
                             "outcome": "success", "source_ip": "203.0.113.54", "failure_reason": "",
                             "timestamp_utc": f"2026-10-07T11:0{minute}:00Z"})
    finding = Finding(NEW_COUNTRY, "test observation", ("203.0.113.54",), ("amelia.ward",),
                      1, 0, 1, parse_utc("2026-10-07T11:00:00Z", "first_seen"),
                      parse_utc("2026-10-07T11:00:00Z", "last_seen"), ())
    output = tmp_path / "neighbourhood.gexf"

    async def check():
        await build_knowledge_base(dataset, build_database, FakeEmbedder())
        async with open_knowledge_base(build_database, dataset=dataset) as kb:
            write_gexf(finding_neighbourhood(kb.graph, kb.finding_radius(finding)), output)

    asyncio.run(check())
    walked = {edge for edge in relationships(nx.read_gexf(output)) if edge[2] not in {"member_of", "grants"}}
    assert walked == {
        ("user-amelia.ward", "dev-laptop-amelia.ward", "used_device"),
        ("user-emily.foster", "dev-laptop-amelia.ward", "used_device"),
        ("user-amelia.ward", "net-vpn-4", "used_address"),
        ("user-emily.foster", "net-vpn-4", "used_address"),
    }


def test_script_writes_the_published_graph_and_refuses_unknown_findings(
    build_database: ServerSettings, tmp_path: Path, capsys: pytest.CaptureFixture[str],
):
    dataset = graph_dataset(tmp_path / "dataset")
    state = tmp_path / "state.json"
    state.write_text(json.dumps({"database": build_database.database}))
    output = tmp_path / "out" / "graph.gexf"
    asyncio.run(build_knowledge_base(dataset, build_database, FakeEmbedder()))

    arguments = ["--dataset-dir", str(dataset), "--state-file", str(state), "--output", str(output)]
    assert main(arguments) == 0
    assert nx.read_gexf(output).has_edge("user-amelia.ward", "group-it-admins")
    assert str(output) in capsys.readouterr().out

    refused = tmp_path / "refused.gexf"
    assert main([*arguments[:4], "--output", str(refused), "--finding-id", "F-unknown-00000000"]) == 1
    assert "No finding" in capsys.readouterr().err
    assert not refused.exists()

    # A file in the dataset folder would change its fingerprint and make the build stale.
    inside = dataset / "graph.gexf"
    assert main([*arguments[:4], "--output", str(inside)]) == 1
    assert "outside the dataset folder" in capsys.readouterr().err
    assert not inside.exists()
    assert main(arguments) == 0

    capsys.readouterr()
    unbuilt = ["--dataset-dir", str(dataset), "--state-file", str(tmp_path / "none.json"),
               "--output", str(refused)]
    assert main(unbuilt) == 1
    assert "no knowledge base has been built" in capsys.readouterr().err
    assert not refused.exists()


def test_no_api_module_serves_the_export():
    files = sorted(API.rglob("*.py"))
    assert files
    offenders = [str(path.relative_to(API)) for path in files
                 if re.search("gexf|gephi", path.read_text(encoding="utf-8"), re.IGNORECASE)
                 or any(isinstance(node, ast.ImportFrom) and node.module == "scripts.export_graph"
                        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))))]
    assert offenders == []
