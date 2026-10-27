"""Guards for the whole test run, kept beside the copied v1 `tests/conftest.py` so that file stays
unchanged.

Tests never see the real keys (ticket 24). Building the model loads `.env` into the process
environment, as the running app needs; in a test run that would give the real OpenRouter and
AbuseIPDB keys to every later test. The guard starts when pytest starts, before any fixture of
any scope and before any test module is imported, and is undone when pytest ends. A test that
needs a key sets a fake one itself.

Tests never meet the real knowledge-base build either (knowledge-base ticket 18). The app's default
pointer file, and the one an eval server started by a test inherits, name a file that does not
exist, so startup runs as "nothing built". A test that needs a build makes its own.
"""

import shutil
import tempfile
from pathlib import Path

import pytest

from login_investigator import agent, knowledge_base, reputation
from login_investigator.knowledge_base import embedding

# The database fixture's own tests run small pytest sessions inside a test (knowledge-base ticket 09).
pytest_plugins = ["pytester"]

_guard = pytest.MonkeyPatch()
_folders: list[Path] = []


def pytest_configure(config):
    _guard.setattr(agent, "load_dotenv", lambda *args, **kwargs: False)
    _guard.delenv(agent.KEY_NAME, raising=False)
    _guard.delenv(reputation.KEY_NAME, raising=False)
    _guard.setattr(embedding, "dotenv_values", lambda *args, **kwargs: {})
    _folders.append(Path(tempfile.mkdtemp(prefix="li-no-knowledge-base-")))
    no_build = _folders[-1] / "none.json"
    _guard.setattr(knowledge_base, "STATE_FILE", no_build)
    _guard.setenv("LI_KNOWLEDGE_BASE_STATE", str(no_build))


def pytest_unconfigure(config):
    _guard.undo()
    while _folders:
        shutil.rmtree(_folders.pop(), ignore_errors=True)
