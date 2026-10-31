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

import asyncio
import os

import pytest
from fastapi.testclient import TestClient

from api.app import create_app
from api.settings import Settings
from login_investigator import agent, postgres, reputation


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


def test_reading_the_database_settings_leaves_the_password_out_of_the_environment_and_repr(
    tmp_path, monkeypatch
):
    """The PostgreSQL password (knowledge-base ticket 09) is read from `.env` for the database
    fixture, but never copied into the process environment, and never shown when printed."""
    monkeypatch.delenv(postgres.PASSWORD_NAME, raising=False)
    env_file = tmp_path / ".env"
    env_file.write_text(f"{postgres.PASSWORD_NAME}=from-the-file\n", encoding="utf-8")
    settings = postgres.ServerSettings.from_env(env_file=env_file)
    assert (postgres.PASSWORD_NAME in os.environ, "from-the-file" in repr(settings)) == (False, False)


def test_embedding_factory_cannot_load_a_real_key_in_tests():
    from login_investigator.knowledge_base.embedding import embedding_service

    async def check():
        with pytest.raises(ValueError, match="OPENROUTER_API_KEY"):
            async with embedding_service():
                pass

    asyncio.run(check())


def test_reranker_factory_cannot_load_a_real_key_in_tests():
    from login_investigator.knowledge_base.reranking import reranker_service

    async def check():
        with pytest.raises(ValueError, match="OPENROUTER_API_KEY"):
            async with reranker_service({"LI_RERANKER": "on"}):
                pass

    asyncio.run(check())


def test_reader_settings_keep_password_out_of_environment_and_repr(tmp_path):
    from login_investigator.knowledge_base import reader_settings
    path = tmp_path / ".env"
    path.write_text("LI_PG_READER_PASSWORD=reader-test-value\n")
    database = postgres.ServerSettings("localhost", 5432, "li_admin", "builder-test-value")
    settings = reader_settings(database, environ={}, env_file=path)
    assert ("LI_PG_READER_PASSWORD" in os.environ, "reader-test-value" in repr(settings)) == (False, False)
