"""The staleness guard's fingerprint and fixed texts (knowledge-base ticket 18).

A build records the fingerprint of the world it was built from. At startup the app recomputes it
from the dataset folder; a database built from older files or settings is never used. Every text
here is fixed: none carries a path, a host or a value from the files.
"""

import hashlib
import json
from dataclasses import asdict
from pathlib import Path

from login_investigator.postgres import START_COMMAND
from . import chunking, schema

BUILD_COMMAND = "uv run python -m scripts.build_knowledge_base"
NOT_BUILT = (f"No knowledge base has been built, so the app runs without it. "
             f"Build it from backend/ with: {BUILD_COMMAND}")
STALE = (f"The knowledge base was built from older files or settings. "
         f"Rebuild it from backend/ with: {BUILD_COMMAND}")
# PostgreSQL gives no error code at connection time that tells a wrong login from a missing
# database, so this text names both fixes (decision 5).
UNCHECKABLE = (f"The knowledge base named by the last build cannot be checked. Check the reader's "
               f"login in .env, or rebuild it from backend/ with: {BUILD_COMMAND}")
SERVER_DOWN = (f"PostgreSQL is not answering, so the knowledge base cannot be checked. "
               f"Start it with: {START_COMMAND}")
SETTINGS_INCOMPLETE = ("The knowledge base cannot be checked because the PostgreSQL settings in "
                       ".env are incomplete. env.example lists them.")


class KnowledgeBaseNotReady(RuntimeError):
    """The server must not start. The message is one of the fixed texts above."""


def fingerprinted_settings() -> dict[str, object]:
    """Read at call time from the same objects the build uses, so a changed setting changes the
    fingerprint."""
    return {"embedding_model": schema.EMBEDDING_MODEL, "vector_size": schema.VECTOR_SIZE,
            "chunking": asdict(chunking.SETTINGS)}


def source_fingerprint(dataset: Path) -> str:
    """SHA-256 over the build settings and every file in the folder, by relative path and content.

    Hidden entries (a name starting with a dot, at any depth) are skipped: they hold tooling state,
    such as Finder's or an editor's, never the world.
    """
    digest = hashlib.sha256(json.dumps(fingerprinted_settings(), sort_keys=True).encode())
    files = sorted((path.relative_to(dataset).as_posix(), path) for path in dataset.rglob("*")
                   if path.is_file() and not any(part.startswith(".")
                                                 for part in path.relative_to(dataset).parts))
    for relative, path in files:
        # A path never holds a NUL byte and the content digest has a fixed length, so no two
        # different folders can produce the same sequence of bytes here.
        digest.update(relative.encode() + b"\0" + hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()
