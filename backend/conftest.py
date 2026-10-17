"""Guards for the whole test run, kept beside the copied v1 `tests/conftest.py` so that file stays
unchanged.

Tests never see the real keys (ticket 24). Building the model loads `.env` into the process
environment, as the running app needs; in a test run that would give the real OpenRouter and
AbuseIPDB keys to every later test. The guard starts when pytest starts, before any fixture of
any scope and before any test module is imported, and is undone when pytest ends. A test that
needs a key sets a fake one itself.
"""

import pytest

from login_investigator import agent, reputation

_guard = pytest.MonkeyPatch()


def pytest_configure(config):
    _guard.setattr(agent, "load_dotenv", lambda *args, **kwargs: False)
    _guard.delenv(agent.KEY_NAME, raising=False)
    _guard.delenv(reputation.KEY_NAME, raising=False)


def pytest_unconfigure(config):
    _guard.undo()
