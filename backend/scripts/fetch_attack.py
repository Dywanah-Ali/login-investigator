"""Fetch the pinned MITRE source and regenerate the thirteen ATT&CK corpus pages.

From backend/: uv run python -m scripts.fetch_attack
Only this script uses the network. No keys or third-party packages are needed.
"""

import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen

from login_investigator.attack_corpus import (
    ATTACK_COMMIT,
    ATTACK_VERSION,
    write_attack_corpus,
)

SOURCE = f"https://raw.githubusercontent.com/mitre-attack/attack-stix-data/{ATTACK_COMMIT}"
BUNDLE_URL = f"{SOURCE}/enterprise-attack/enterprise-attack-{ATTACK_VERSION}.json"
BUNDLE_SHA256 = "81113ba98afa2928f3dcff62022539f7ce30c315c32e14422f11ff95ce534352"
LICENCE_URL = f"{SOURCE}/LICENSE.txt"
LICENCE_SHA256 = "738144f7fb054722a4ef9d3367c51710341dc12fc574c6ac3a41daaaecd8bf5e"
DEFAULT_DATASET = Path(__file__).resolve().parents[1] / "data" / "datasets" / "default"


def fetch_verified(url: str, expected_sha256: str) -> bytes:
    with urlopen(url, timeout=120) as response:
        content = response.read()
    if hashlib.sha256(content).hexdigest() != expected_sha256:
        raise ValueError(f"Pinned source checksum mismatch: {url}")
    return content


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset-dir", type=Path, default=DEFAULT_DATASET)
    args = parser.parse_args()
    bundle = json.loads(fetch_verified(BUNDLE_URL, BUNDLE_SHA256))
    licence = fetch_verified(LICENCE_URL, LICENCE_SHA256)
    write_attack_corpus(bundle, licence, args.dataset_dir)
    print(f"Wrote 13 ATT&CK {ATTACK_VERSION} pages and MITRE licence to "
          f"{args.dataset_dir / 'corpus' / 'attack'}")


if __name__ == "__main__":
    main()
