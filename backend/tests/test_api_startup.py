"""Startup, seen from outside (ticket 12): each of v1's seams is called once per process, the
configuration is read from the environment, and a failure stays inside the part it belongs to.

The first test watches the core's seam functions, which tests elsewhere never do: "exactly once" is
the requirement itself, and a reply cannot show it. The real functions still run; they are counted.
"""

import asyncio
import json
import logging
import shutil
from collections import Counter
from dataclasses import replace

import pytest
from fastapi.testclient import TestClient

from api.app import create_app
from api.settings import Settings
from login_investigator import (
    agent,
    generator,
    investigations,
    knowledge_base,
    loader,
    rules,
)
from login_investigator.knowledge_base import build_knowledge_base
from login_investigator.knowledge_base.staleness import NOT_BUILT, STALE, UNCHECKABLE
from login_investigator.postgres import (
    ServerSettings,
    create_fresh_database,
    drop_database,
)
from tests.test_knowledge_base import DATASET, FakeEmbedder, publish, sample_dataset

LOG_FAILED_VALIDATION = "The log failed validation. The server log lists the problems."

SEAMS = [(loader, "load_log"), (rules, "detect_all"), (investigations, "open_memory"),
         (agent, "make_model"), (agent, "build_agent")]


@pytest.fixture
def calls(monkeypatch):
    """Count every call to the startup seams, by name, letting each real call through."""
    counter = Counter()
    for module, name in SEAMS:
        real = getattr(module, name)

        def counted(*args, _real=real, _name=name, **kwargs):
            counter[_name] += 1
            return _real(*args, **kwargs)

        monkeypatch.setattr(module, name, counted)
    return counter


@pytest.fixture
def memory_path(tmp_path):
    return tmp_path / "memory" / "investigations.sqlite"


def test_each_seam_is_called_once_per_process(monkeypatch, calls, memory_path):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key-never-used")  # building calls no model
    app = create_app(Settings.from_env({"LI_MEMORY_PATH": str(memory_path)}))
    assert sum(calls.values()) == 0  # nothing happens before the server starts
    with TestClient(app) as client:
        for path in ["/api/dataset", "/api/overview", "/api/overview?outcome=failure",
                     "/api/rules", "/api/dataset"]:
            assert client.get(path).status_code == 200
    assert calls == {"load_log": 1, "detect_all": 1, "open_memory": 1, "make_model": 1,
                     "build_agent": 1}
    assert memory_path.is_file()  # the memory opened is the configured one


def test_a_missing_model_key_leaves_the_dashboards_working(monkeypatch, calls, memory_path):
    """Author's decision, 14 Oct: a failure stays inside the part it belongs to. The
    Investigation endpoints that answer 503 come with ticket 16."""
    monkeypatch.setenv("OPENROUTER_API_KEY", "")
    with TestClient(create_app(Settings.from_env({"LI_MEMORY_PATH": str(memory_path)}))) as client:
        assert client.get("/api/overview").status_code == 200
        assert client.get("/api/dataset").status_code == 200
    assert calls["build_agent"] == 0


def test_a_log_that_fails_validation_makes_the_dataset_endpoints_answer_log_invalid(
        tmp_path, memory_path):
    bad_log = tmp_path / "logins.csv"
    bad_log.write_text("timestamp_utc,username\n2026-10-01T00:00:00Z,alice\n", encoding="utf-8")
    settings = Settings.from_env({"LI_DATASET_DIR": str(bad_log.parent), "LI_MEMORY_PATH": str(memory_path)})
    with TestClient(create_app(settings)) as client:
        for path in ["/api/dataset", "/api/overview"]:
            reply = client.get(path)
            assert reply.status_code == 500
            error = reply.json()["error"]
            assert error == {"code": "log_invalid", "message": LOG_FAILED_VALIDATION}
        # Fixed text needs no dataset, so the rules guide still answers.
        assert client.get("/api/rules").status_code == 200


def test_a_bad_row_never_sends_its_log_values_back(tmp_path, memory_path):
    """The loader quotes a bad row's raw values in its message. Log fields are data and never
    travel inside a sentence, so the client gets fixed text (author's ruling, ticket 13; B-008)."""
    hostile = "<script>alert(1)</script>"
    row = {"timestamp_utc": "2026-10-01T00:00:00Z", "username": "alice", "source_ip": hostile,
           "country": "GB", "outcome": "success", "failure_reason": "", "user_agent": "x",
           "device_id": "", "mfa_result": "pass"}
    bad_log = tmp_path / "logins.csv"
    bad_log.write_text(",".join(generator.COLUMNS) + "\n"
                       + ",".join(row[column] for column in generator.COLUMNS) + "\n",
                       encoding="utf-8")
    settings = Settings.from_env({"LI_DATASET_DIR": str(bad_log.parent), "LI_MEMORY_PATH": str(memory_path)})
    with TestClient(create_app(settings)) as client:
        reply = client.get("/api/overview")
    assert reply.status_code == 500
    assert reply.json() == {"error": {"code": "log_invalid", "message": LOG_FAILED_VALIDATION}}
    assert "script" not in reply.text


@pytest.mark.parametrize("folder_kind", ["missing", "empty", "file"])
def test_an_invalid_dataset_folder_does_not_reveal_where_the_server_looked(
        tmp_path, memory_path, folder_kind):
    """The loader's own message holds the full path, which can name the machine's user (B-003)."""
    missing = tmp_path / "private-folder" / "logins.csv"
    if folder_kind == "empty":
        missing.parent.mkdir()
    elif folder_kind == "file":
        missing.parent.write_text("not a folder", encoding="utf-8")
    settings = Settings.from_env({"LI_DATASET_DIR": str(missing.parent), "LI_MEMORY_PATH": str(memory_path)})
    with TestClient(create_app(settings)) as client:
        reply = client.get("/api/dataset")
    assert reply.status_code == 500
    assert reply.json() == {"error": {"code": "log_invalid",
                                      "message": "The configured log file was not found."}}
    assert "private-folder" not in reply.text


def test_the_settings_default_to_the_paths_in_the_contract():
    settings = Settings.from_env({})
    assert settings.dataset_dir.parts[-4:] == ("backend", "data", "datasets", "default")
    assert settings.memory_path.parts[-3:] == ("backend", "memory", "investigations.sqlite")
    assert settings.reputation_dir.parts[-3:] == ("backend", "data", "ip_reputation")
    # The test run replaces the core's default (root conftest); the app reads whatever it is.
    assert settings.knowledge_base_state == knowledge_base.STATE_FILE
    assert not knowledge_base.STATE_FILE.exists()


def test_the_settings_read_each_path_from_the_environment(tmp_path):
    settings = Settings.from_env({"LI_DATASET_DIR": str(tmp_path / "dataset"),
                                  "LI_MEMORY_PATH": str(tmp_path / "b.sqlite"),
                                  "LI_REPUTATION_DIR": str(tmp_path / "c"),
                                  "LI_KNOWLEDGE_BASE_STATE": str(tmp_path / "d.json")})
    assert settings == Settings(dataset_dir=tmp_path / "dataset", memory_path=tmp_path / "b.sqlite",
                                reputation_dir=tmp_path / "c", knowledge_base_state=tmp_path / "d.json")


# The staleness guard at startup (knowledge-base ticket 18). These tests build a small knowledge
# base in real PostgreSQL with offline embeddings, exactly as door 2's tests do.

@pytest.fixture
def built(fresh_database, tmp_path):
    """A dataset with the real log, built into its own database and published to a pointer file."""
    dataset = sample_dataset(tmp_path / "dataset")
    shutil.copy(DATASET / "logins.csv", dataset / "logins.csv")
    database = create_fresh_database(replace(fresh_database, database="postgres"))
    try:
        asyncio.run(build_knowledge_base(dataset, database, FakeEmbedder()))
        yield dataset, publish(tmp_path / "active.json", database)
    finally:
        drop_database(database)


def startup_settings(dataset, state, memory_path):
    return Settings.from_env({"LI_DATASET_DIR": str(dataset), "LI_MEMORY_PATH": str(memory_path),
                              "LI_KNOWLEDGE_BASE_STATE": str(state)})


def test_a_stale_knowledge_base_stops_the_server_before_anything_starts(built, memory_path, tmp_path):
    dataset, state = built
    (dataset / "org" / "people.csv").write_text("person_id\n", encoding="utf-8")
    app = create_app(startup_settings(dataset, state, memory_path))
    with pytest.raises(knowledge_base.KnowledgeBaseNotReady) as caught:
        with TestClient(app):
            raise AssertionError("The server started on a stale knowledge base")
    message = str(caught.value)
    assert message == STALE
    assert "uv run python -m scripts.build_knowledge_base" in message
    assert str(tmp_path) not in message
    # No earlier error, which could carry a host or a path, travels with it.
    assert caught.value.__cause__ is None
    assert caught.value.__context__ is None or caught.value.__suppress_context__
    # Nothing behind the guard ran: the memory file is opened only by the services.
    assert not memory_path.exists()


def test_a_build_that_cannot_be_checked_stops_the_server(fresh_database, memory_path, tmp_path):
    state = publish(tmp_path / "active.json", replace(fresh_database, database="li_kb_000000000000"))
    app = create_app(startup_settings(DATASET, state, memory_path))
    with pytest.raises(knowledge_base.KnowledgeBaseNotReady) as caught:
        with TestClient(app):
            raise AssertionError("The server started on a knowledge base it could not check")
    assert str(caught.value) == UNCHECKABLE
    # This one is raised while handling the database's own error, which names the database.
    assert caught.value.__cause__ is None and caught.value.__suppress_context__
    assert not memory_path.exists()


def test_a_matching_knowledge_base_starts_the_server_as_before(built, memory_path):
    dataset, state = built
    app = create_app(startup_settings(dataset, state, memory_path))
    with TestClient(app) as client:
        assert client.get("/api/dataset").status_code == 200
        assert client.get("/api/overview").status_code == 200
        assert isinstance(app.state.knowledge_base, knowledge_base.KnowledgeBase)
        assert app.state.knowledge_base.engine.url.database == json.loads(state.read_text())["database"]
    assert memory_path.is_file()


def test_with_nothing_built_the_server_starts_and_says_so(monkeypatch, memory_path, tmp_path, caplog):
    def must_not_read(*args, **kwargs):
        raise AssertionError("No database settings are needed when nothing has been built")

    monkeypatch.setattr(ServerSettings, "from_env", must_not_read)
    settings = startup_settings(DATASET, tmp_path / "absent.json", memory_path)
    app = create_app(settings)
    with caplog.at_level(logging.WARNING, logger="api.app"):
        with TestClient(app) as client:
            assert client.get("/api/dataset").status_code == 200
            assert app.state.knowledge_base is None
    assert [record.getMessage() for record in caplog.records if record.name == "api.app"] == [NOT_BUILT]
