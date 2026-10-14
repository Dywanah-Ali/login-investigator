"""Startup, seen from outside (ticket 12): each of v1's seams is called once per process, the
configuration is read from the environment, and a failure stays inside the part it belongs to.

The first test watches the core's seam functions, which tests elsewhere never do: "exactly once" is
the requirement itself, and a reply cannot show it. The real functions still run; they are counted.
"""

from collections import Counter

import pytest
from fastapi.testclient import TestClient

from api.app import create_app
from api.settings import Settings
from login_investigator import agent, investigations, loader, rules

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
    bad_log = tmp_path / "bad.csv"
    bad_log.write_text("timestamp_utc,username\n2026-10-01T00:00:00Z,alice\n", encoding="utf-8")
    settings = Settings.from_env({"LI_LOG_PATH": str(bad_log), "LI_MEMORY_PATH": str(memory_path)})
    with TestClient(create_app(settings)) as client:
        for path in ["/api/dataset", "/api/overview"]:
            reply = client.get(path)
            assert reply.status_code == 500
            error = reply.json()["error"]
            assert error["code"] == "log_invalid"
            assert error["message"].startswith("bad.csv has the wrong columns.")
        # Fixed text needs no dataset, so the rules guide still answers.
        assert client.get("/api/rules").status_code == 200


def test_the_settings_default_to_the_paths_in_the_contract():
    settings = Settings.from_env({})
    assert settings.log_path.parts[-3:] == ("backend", "data", "logins.csv")
    assert settings.memory_path.parts[-3:] == ("backend", "memory", "investigations.sqlite")
    assert settings.reputation_dir.parts[-3:] == ("backend", "data", "ip_reputation")


def test_the_settings_read_each_path_from_the_environment(tmp_path):
    settings = Settings.from_env({"LI_LOG_PATH": str(tmp_path / "a.csv"),
                                  "LI_MEMORY_PATH": str(tmp_path / "b.sqlite"),
                                  "LI_REPUTATION_DIR": str(tmp_path / "c")})
    assert settings == Settings(log_path=tmp_path / "a.csv", memory_path=tmp_path / "b.sqlite",
                                reputation_dir=tmp_path / "c")
