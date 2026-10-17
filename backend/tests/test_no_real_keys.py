"""Tests never see the real keys in `.env` (ticket 24).

Building the model loads `.env` into the process environment, as v1 does for the running app. In a
test run that would hand the real OpenRouter and AbuseIPDB keys to every later test, so one
missing network guard would spend real quota and send log IPs to AbuseIPDB. The values are never
printed: only whether each name is set.
"""

import os

from fastapi.testclient import TestClient

from api.app import create_app
from api.settings import Settings
from login_investigator import agent, reputation


def test_starting_the_app_puts_no_key_into_the_test_environment(monkeypatch, tmp_path):
    monkeypatch.delenv(agent.KEY_NAME, raising=False)
    monkeypatch.delenv(reputation.KEY_NAME, raising=False)
    settings = Settings.from_env({"LI_MEMORY_PATH": str(tmp_path / "memory.sqlite")})
    with TestClient(create_app(settings)):
        pass
    assert (agent.KEY_NAME in os.environ, reputation.KEY_NAME in os.environ) == (False, False)
