"""The agreed T14 boundary: saved MITRE bundle in, corpus files out. No network."""

import json
from pathlib import Path

import pytest

from login_investigator.attack_corpus import write_attack_corpus

SAMPLE = Path(__file__).parent / "fixtures" / "attack"


def test_saved_bundle_becomes_thirteen_versioned_pages_with_mitre_licence(tmp_path):
    bundle = json.loads((SAMPLE / "enterprise-attack-20.0-sample.json").read_text())
    licence = (SAMPLE / "LICENSE.txt").read_bytes()

    write_attack_corpus(bundle, licence, tmp_path)

    folder = tmp_path / "corpus" / "attack"
    assert {path.stem for path in folder.glob("*.md")} == {
        "T1110", "T1110.001", "T1110.002", "T1110.003", "T1110.004",
        "T1078", "T1078.002", "T1621", "T1021", "M1032", "M1036", "M1027", "M1018",
    }
    page = (folder / "T1110.003.md").read_text()
    assert 'id: "attack-t1110-003"' in page
    assert 'title: "T1110.003: Password Spraying"' in page
    assert 'kind: "attack"' in page
    assert 'version: "20.0"' in page
    for field in ("owner", "department", "date", "status", "supersedes"):
        assert f"\n{field}:" in page.split("\n---\n", 1)[0]
    assert "Adversaries may use a single or small list of commonly used passwords" in page
    assert (folder / "LICENSE.txt").read_bytes() == licence


def test_pages_follow_mitigation_procedure_and_detection_links(tmp_path):
    bundle = json.loads((SAMPLE / "enterprise-attack-20.0-sample.json").read_text())
    write_attack_corpus(bundle, (SAMPLE / "LICENSE.txt").read_bytes(), tmp_path)

    folder = tmp_path / "corpus" / "attack"
    spray = (folder / "T1110.003.md").read_text()
    assert "## Mitigations" in spray
    assert "M1032: Multi-factor Authentication" in spray
    assert "## Procedure examples" in spray
    assert "HAFNIUM" in spray
    assert "has gained initial access through password spray attacks" in spray
    assert "## Detection" in spray
    assert "DET0487" in spray
    assert "Analytic" in spray
    assert "## References" in spray
    assert "Microsoft Silk Typhoon MAR 2025" in spray
    assert "https://attack.mitre.org/techniques/T1110/003" in spray
    mitigation = (folder / "M1032.md").read_text()
    assert "## Techniques mitigated" in mitigation
    assert "T1110.003: Password Spraying" in mitigation


def test_repeated_build_and_reordered_bundle_write_identical_bytes(tmp_path):
    bundle = json.loads((SAMPLE / "enterprise-attack-20.0-sample.json").read_text())
    licence = (SAMPLE / "LICENSE.txt").read_bytes()
    write_attack_corpus(bundle, licence, tmp_path)
    before = {p.name: p.read_bytes() for p in (tmp_path / "corpus" / "attack").iterdir()}

    bundle["objects"].reverse()
    write_attack_corpus(bundle, licence, tmp_path)

    assert {p.name: p.read_bytes() for p in (tmp_path / "corpus" / "attack").iterdir()} == before


@pytest.mark.parametrize("corruption", ["release", "missing", "revoked", "link"])
def test_bad_source_fails_before_changing_existing_files(tmp_path, corruption):
    bundle = json.loads((SAMPLE / "enterprise-attack-20.0-sample.json").read_text())
    licence = (SAMPLE / "LICENSE.txt").read_bytes()
    write_attack_corpus(bundle, licence, tmp_path)
    folder = tmp_path / "corpus" / "attack"
    before = {p.name: p.read_bytes() for p in folder.iterdir()}
    if corruption == "release":
        collection = next(o for o in bundle["objects"] if o["type"] == "x-mitre-collection")
        collection["x_mitre_version"] = "19.0"
    elif corruption == "missing":
        bundle["objects"] = [o for o in bundle["objects"] if o.get("name") != "Password Spraying"
                             or o["type"] != "attack-pattern"]
    elif corruption == "revoked":
        next(o for o in bundle["objects"] if o.get("name") == "Password Spraying")["revoked"] = True
    else:
        next(o for o in bundle["objects"] if o.get("relationship_type") == "detects")[
            "source_ref"
        ] = "x-mitre-detection-strategy--missing"

    with pytest.raises(ValueError):
        write_attack_corpus(bundle, licence, tmp_path)
    assert {p.name: p.read_bytes() for p in folder.iterdir()} == before
