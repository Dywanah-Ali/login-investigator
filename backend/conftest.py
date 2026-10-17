"""Guards for every test, kept beside the copied v1 `tests/conftest.py` so that file stays unchanged.

Tests never see the real keys (ticket 24). Building the model loads `.env` into the process
environment, as the running app needs; in a test run that would give the real OpenRouter and
AbuseIPDB keys to every later test. A test that needs a key sets a fake one itself.
"""

import pytest

from login_investigator import agent, reputation


@pytest.fixture(autouse=True)
def no_real_keys(monkeypatch):
    monkeypatch.setattr(agent, "load_dotenv", lambda *args, **kwargs: False)
    monkeypatch.delenv(agent.KEY_NAME, raising=False)
    monkeypatch.delenv(reputation.KEY_NAME, raising=False)
