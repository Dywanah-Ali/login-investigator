"""Tests never see the real keys in `.env` (ticket 24).

Building the model loads `.env` into the process environment, as v1 does for the running app. In a
test run that would hand the real OpenRouter and AbuseIPDB keys to every later test, so one
missing network guard would spend real quota and send log IPs to AbuseIPDB.

The values are never printed. The assertions compare only booleans: a plain `not in os.environ`
would make pytest print the whole environment, values included, if it failed.

The app here is shared by the whole module, as in the dashboard tests: module fixtures start before
any per-test guard, so they are where a guard that starts too late lets the keys in. On a machine
without `.env` there is no key to leak, and these tests pass either way.
"""

import os

import pytest
from fastapi.testclient import TestClient

from api.app import create_app
from api.settings import Settings
from login_investigator import agent, reputation


@pytest.fixture(scope="module")
def services(tmp_path_factory):
    memory = tmp_path_factory.mktemp("memory") / "investigations.sqlite"
    app = create_app(Settings.from_env({"LI_MEMORY_PATH": str(memory)}))
    with TestClient(app):
        yield app.state.services


def keys_set() -> tuple[bool, bool]:
    return agent.KEY_NAME in os.environ, reputation.KEY_NAME in os.environ


def test_an_app_shared_by_a_module_gets_no_model_key(services):
    assert (services.model is None, services.agent is None) == (True, True)


def test_starting_the_app_puts_no_key_into_the_test_environment(services):
    assert keys_set() == (False, False)


def test_building_the_model_finds_no_key():
    with pytest.raises(RuntimeError, match="is not set"):
        agent.make_model()
