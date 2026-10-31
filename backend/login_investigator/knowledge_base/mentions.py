"""Resolve literal mentions to the world's existing IDs, never to invented entities."""

import re
from pathlib import Path

from login_investigator.corpus_check import read_table

from .chunking import Chunk

# Owners in document front matter are teams, not account mentions. Only passage text is scanned.
ENTITY_FIELDS = {
    "people": ("person", "person_id", ("person_id", "username", "display_name")),
    "groups": ("group", "group_id", ("group_id", "name")),
    "assets": ("asset", "asset_id", ("asset_id", "name")),
    "devices": ("device", "device_id", ("device_id", "name")),
    "networks": ("network", "network_id", ("network_id", "address", "name")),
}


def find_mentions(dataset: Path, chunks: list[Chunk]) -> list[dict[str, str]]:
    aliases: list[tuple[str, str, re.Pattern[str]]] = []
    for table, (kind, id_field, fields) in ENTITY_FIELDS.items():
        for row in read_table(dataset, table):
            names = sorted({row[field] for field in fields if row[field]}, key=len, reverse=True)
            # A trailing full stop is punctuation; a dot followed by a word continues an ID.
            pattern = re.compile(
                r"(?<![\w.@-])(?:" + "|".join(re.escape(name) for name in names)
                + r")(?![\w-]|\.\w)", re.IGNORECASE,
            )
            aliases.append((kind, row[id_field], pattern))
    return [{"chunk_id": chunk.id, "entity_type": kind, "entity_id": identifier}
            for chunk in chunks for kind, identifier, pattern in aliases
            if pattern.search(chunk.text)]
