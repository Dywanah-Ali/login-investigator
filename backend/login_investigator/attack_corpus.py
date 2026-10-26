"""Assemble the fixed ATT&CK reference corpus from a supplied STIX 2.1 bundle.

This module does no networking. The fetch script supplies the pinned source and licence.
"""

import json
from pathlib import Path
from typing import Any

ATTACK_VERSION = "20.0"
ATTACK_COMMIT = "20664a889568dce884a1dac0ec7b12ae3a199f51"
TECHNIQUES = (
    "T1110", "T1110.001", "T1110.002", "T1110.003", "T1110.004",
    "T1078", "T1078.002", "T1621", "T1021",
)
MITIGATIONS = ("M1032", "M1036", "M1027", "M1018")


def attack_reference(obj: dict[str, Any]) -> dict[str, str]:
    """The MITRE reference identifies an ATT&CK object, unlike its STIX UUID."""
    return next(
        (ref for ref in obj.get("external_references", [])
         if ref.get("source_name") == "mitre-attack" and ref.get("external_id")),
        {},
    )


def active(obj: dict[str, Any]) -> bool:
    return not obj.get("revoked") and not obj.get("x_mitre_deprecated")


def label(obj: dict[str, Any]) -> str:
    identifier = attack_reference(obj).get("external_id", obj["id"])
    return f"{identifier}: {obj['name']}"


def resolve(objects: dict[str, dict[str, Any]], identifier: str) -> dict[str, Any]:
    try:
        return objects[identifier]
    except KeyError as exc:
        raise ValueError(f"ATT&CK source is missing linked object: {identifier}") from exc


def linked_sections(
    obj: dict[str, Any], objects: dict[str, dict[str, Any]],
    relationships: list[dict[str, Any]], selected_ids: set[str],
) -> str:
    """Resolve STIX links locally, preserving relationship-specific advice and references."""
    sections: dict[str, list[str]] = {}
    sources = [obj]
    if obj.get("x_mitre_detection"):
        sections["Detection"] = [obj["x_mitre_detection"].strip()]
    for relationship in sorted(relationships, key=lambda item: item["id"]):
        kind = relationship["relationship_type"]
        source = relationship["source_ref"]
        target = relationship["target_ref"]
        if target == obj["id"] and kind in {"mitigates", "uses", "detects"}:
            other = resolve(objects, source)
            section = {"mitigates": "Mitigations", "uses": "Procedure examples",
                       "detects": "Detection"}[kind]
        elif source == obj["id"] and kind == "mitigates" and target in selected_ids:
            other = resolve(objects, target)
            section = "Techniques mitigated"
        else:
            continue
        if not active(other):
            continue
        text = f"### {label(other)}\n\n"
        if relationship.get("description"):
            text += relationship["description"].strip() + "\n\n"
        if kind == "mitigates" and other["type"] == "course-of-action":
            text += other.get("description", "").strip() + "\n\n"
        if kind == "detects":
            text += other.get("description", "").strip() + "\n\n"
            for analytic_id in sorted(other.get("x_mitre_analytic_refs", [])):
                analytic = resolve(objects, analytic_id)
                if active(analytic):
                    text += f"#### {label(analytic)}\n\n{analytic['description'].strip()}\n\n"
                    sources.append(analytic)
        sections.setdefault(section, []).append(text.strip())
        sources.extend([relationship, other])
    references = sorted({
        (ref["source_name"], ref["url"])
        for source in sources for ref in source.get("external_references", [])
        if ref.get("url")
    })
    if references:
        sections["References"] = ["\n".join(f"- [{name}]({url})" for name, url in references)]
    return "".join(
        f"\n## {name}\n\n" + "\n\n".join(sections[name]) + "\n"
        for name in ("Detection", "Mitigations", "Procedure examples", "Techniques mitigated",
                     "References") if name in sections
    )


def write_attack_corpus(bundle: dict[str, Any], licence: bytes, dataset: Path) -> None:
    """Write thirteen Markdown pages and the supplied MITRE licence below a dataset."""
    objects = {obj["id"]: obj for obj in bundle["objects"]}
    collections = [obj for obj in objects.values() if obj["type"] == "x-mitre-collection"]
    if (len(collections) != 1 or collections[0].get("name") != "Enterprise ATT&CK"
            or collections[0].get("x_mitre_version") != ATTACK_VERSION):
        raise ValueError(f"Expected Enterprise ATT&CK {ATTACK_VERSION} collection")
    selected = {
        attack_reference(obj).get("external_id"): obj for obj in bundle["objects"]
        if obj["type"] in {"attack-pattern", "course-of-action"}
        and active(obj)
    }
    missing = set((*TECHNIQUES, *MITIGATIONS)) - selected.keys()
    if missing:
        raise ValueError(f"ATT&CK source is missing active pages: {', '.join(sorted(missing))}")
    selected_ids = {selected[identifier]["id"] for identifier in (*TECHNIQUES, *MITIGATIONS)}
    relationships = [obj for obj in objects.values()
                     if obj["type"] == "relationship" and active(obj)]
    pages: dict[str, str] = {}
    for identifier in (*TECHNIQUES, *MITIGATIONS):
        obj = selected[identifier]
        metadata = {
            "id": "attack-" + identifier.lower().replace(".", "-"),
            "title": f"{identifier}: {obj['name']}",
            "kind": "attack",
            "owner": "mitre",
            "department": "external",
            "date": obj["modified"][:10],
            "version": ATTACK_VERSION,
            "status": "current",
            "supersedes": None,
        }
        header = "\n".join(f"{key}: {json.dumps(value)}" for key, value in metadata.items())
        pages[identifier] = (
            f"---\n{header}\n---\n\n# {metadata['title']}\n\n"
            f"## Description\n\n{obj['description'].strip()}\n"
            + linked_sections(obj, objects, relationships, selected_ids)
        )
    folder = dataset / "corpus" / "attack"
    folder.mkdir(parents=True, exist_ok=True)
    for identifier, page in pages.items():
        (folder / f"{identifier}.md").write_text(page, encoding="utf-8")
    (folder / "LICENSE.txt").write_bytes(licence)
