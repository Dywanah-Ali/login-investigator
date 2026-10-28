"""The Gephi export (T08 d9): a builder's wall chart, written by a script, never served by the API."""

import json
from pathlib import Path
from typing import Any

import networkx as nx
from networkx.readwrite.gexf import GEXFWriter

from .radius import FindingRadius

# Gephi Lite reads `viz` colours from the file: one colour per node type.
NODE_COLOURS = {
    "person": {"r": 31, "g": 119, "b": 180}, "group": {"r": 255, "g": 127, "b": 14},
    "asset": {"r": 214, "g": 39, "b": 40}, "device": {"r": 44, "g": 160, "b": 44},
    "network": {"r": 148, "g": 103, "b": 189}, "chunk": {"r": 127, "g": 127, "b": 127},
}
# Names NetworkX 3.6.1's GEXF writer consumes or renames instead of writing as attributes
# (read in its installed source). Data under any of them would vanish from the file silently.
RESERVED = frozenset({"id", "label", "pid", "start", "end", "parents", "spells", "slices", "viz",
                      "weight", "type", "key", "networkx_key"})


class ExportRefused(ValueError):
    """The file cannot be written as asked. Every message is a text written here, never a source value
    other than an attribute name or a node type."""


def _attributes(data: dict[str, Any]) -> dict[str, Any]:
    reserved = sorted(RESERVED & data.keys())
    if reserved:
        raise ExportRefused(f"GEXF would drop the reserved attribute name {reserved[0]!r}")
    written: dict[str, Any] = {}
    for name, value in data.items():
        if value is None:
            continue  # GEXF has no null. An absent value reads back as absent.
        if isinstance(value, (tuple, list)):
            value = ", ".join(map(str, value))  # The writer reads a list as dynamic data.
        elif isinstance(value, dict):
            value = json.dumps(value, sort_keys=True)
        written[name] = value
    return written


def write_gexf(graph: nx.MultiDiGraph, path: Path) -> None:
    """Every check runs before the file is opened, so a refused export leaves no file."""
    export = nx.MultiDiGraph()
    for node, data in graph.nodes(data=True):
        colour = NODE_COLOURS.get(data.get("entity_type", ""))
        if colour is None:
            raise ExportRefused(f"The node type {data.get('entity_type')!r} has no export colour")
        export.add_node(node, **_attributes(data), viz={"color": dict(colour)})
    for source, target, key, data in graph.edges(keys=True, data=True):
        export.add_edge(source, target, key=key, **_attributes(data))
    # `write_gexf`'s own three steps, with one change between them: NetworkX always writes an alpha
    # on 1.2 colours, and Gephi Lite ignores any colour that carries one (gephi-lite issue #307).
    writer = GEXFWriter()
    writer.add_graph(export)
    for colour in writer.xml.iter(f"{{{writer.NS_VIZ}}}color"):
        del colour.attrib["a"]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as handle:
        writer.write(handle)


def finding_neighbourhood(graph: nx.MultiDiGraph, radius: FindingRadius) -> nx.MultiDiGraph:
    """The walk the radius made: organisation nodes only, each edge as the radius used it."""
    if not radius.accounts:
        raise ExportRefused("The finding reaches no account, so it has no neighbourhood to export")
    edges: set[tuple[str, str, str]] = set()
    for account in radius.accounts:
        for walk in account.access_paths:
            edges.add((walk[0], walk[1], "member_of"))
            if len(walk) == 3:
                edges.add((walk[1], walk[2], "grants"))
        address_walks = [walk for match in account.address_reuse.by_address for walk in match.paths]
        for walks, relationship in ((account.device_paths, "used_device"), (address_walks, "used_address")):
            for subject, shared, peer in walks:
                edges.update({(subject, shared, relationship), (peer, shared, relationship)})
    neighbourhood = nx.MultiDiGraph()
    for account in radius.accounts:
        person = account.account["person_id"]
        neighbourhood.add_node(person, **graph.nodes[person])
    for source, target, relationship in sorted(edges):
        for node in (source, target):
            neighbourhood.add_node(node, **graph.nodes[node])
        neighbourhood.add_edge(source, target, key=relationship, **graph[source][target][relationship])
    return neighbourhood
