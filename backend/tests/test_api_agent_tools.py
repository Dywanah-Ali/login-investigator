"""The agent's tools read what the dashboards read (ticket 22): the log and the saved-reputation
folder the settings name, never the core's defaults behind the settings' back.

The tools are called directly, as the agent's tool node calls them, while the app runs. No test
reaches the network or a model.
"""

import json

import pytest
from fastapi.testclient import TestClient

from api.app import create_app
from api.settings import Settings
from login_investigator import generator, investigations, reputation, tools
from login_investigator.tools import find_suspicious_activity, lookup_ip_reputation, search_logins

LOG_REFUSED = "The configured sign-in log failed validation, so it cannot be read."

# Three quiet sign-ins: no rule fires. The default log has 5 findings and far more rows.
TINY_LOG = [
    ("2026-10-01T09:00:00Z", "alice", "81.2.69.160", "GB", "success", ""),
    ("2026-10-01T09:05:00Z", "bob", "81.2.69.161", "GB", "failure", "bad_password"),
    ("2026-10-01T09:06:00Z", "bob", "81.2.69.161", "GB", "success", ""),
]


def run(tool, **args) -> dict:
    return json.loads(tool.invoke(args))


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    def refuse(*args, **kwargs):
        raise AssertionError("a live call was made")
    monkeypatch.setattr(reputation.requests, "get", refuse)
    monkeypatch.delenv(reputation.KEY_NAME, raising=False)


@pytest.fixture
def tiny_log(tmp_path):
    path = tmp_path / "tiny.csv"
    lines = [",".join(generator.COLUMNS)]
    lines += [",".join((*row[:5], row[5], "Mozilla/5.0")) for row in TINY_LOG]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def settings_for(tmp_path, **environ) -> Settings:
    return Settings.from_env({"LI_MEMORY_PATH": str(tmp_path / "memory.sqlite"), **environ})


def test_the_search_and_rules_tools_read_the_configured_log(monkeypatch, tmp_path, tiny_log):
    """The tools share the dashboards' startup load: the right counts, and no load of their own.
    A second load of the same file would give the same counts, so the loads are counted too."""
    with TestClient(create_app(settings_for(tmp_path, LI_LOG_PATH=str(tiny_log)))) as client:
        own_loads = []
        monkeypatch.setattr(tools, "load_log", lambda *a, **k: own_loads.append("log"))
        monkeypatch.setattr(tools, "detect_all", lambda *a, **k: own_loads.append("rules"))
        overview = client.get("/api/overview").json()
        searched = run(search_logins)["data"]
        found = run(find_suspicious_activity)["data"]
    assert searched["total"] == overview["summary"]["total"] == 3
    assert searched["failures"] == overview["summary"]["failures"] == 1
    assert found["finding_count"] == overview["alert_count"] == 0
    assert own_loads == []


def test_the_reputation_tool_reads_the_configured_folder(tmp_path):
    folder = tmp_path / "reputation"
    folder.mkdir()
    saved = {"fetchedAt": "2026-10-01T00:00:00+00:00",
             "data": {"ipAddress": "1.1.1.1", "abuseConfidenceScore": 7, "isp": "Test ISP"}}
    (folder / "1.1.1.1.json").write_text(json.dumps(saved), encoding="utf-8")
    with TestClient(create_app(settings_for(tmp_path, LI_REPUTATION_DIR=str(folder)))):
        answer = run(lookup_ip_reputation, ip="1.1.1.1")["data"]
    assert answer["source"] == "saved"
    assert answer["fetched_at"] == "2026-10-01T00:00:00+00:00"
    assert answer["abuse_confidence_score"] == 7
    assert answer["isp"] == "Test ISP"


def test_a_log_that_fails_validation_is_refused_never_replaced_by_the_default(tmp_path):
    """Author's ruling, 17 Oct: a failure stays inside the part it belongs to. The log tools
    refuse with fixed text; the reputation tool, which needs no log, keeps working."""
    bad_log = tmp_path / "bad.csv"
    bad_log.write_text("timestamp_utc,username\n2026-10-01T00:00:00Z,alice\n", encoding="utf-8")
    with TestClient(create_app(settings_for(tmp_path, LI_LOG_PATH=str(bad_log)))):
        searched = run(search_logins, user="alice")
        found = run(find_suspicious_activity)
        looked_up = run(lookup_ip_reputation, ip="8.8.8.8")
    assert searched == found == {"error": LOG_REFUSED}
    assert looked_up["data"]["source"] == "saved"


def test_after_shutdown_the_tools_read_the_default_log_again(tmp_path, tiny_log, truth):
    """No app leaves its data behind for the next test, or for the eval runner's direct mode."""
    with TestClient(create_app(settings_for(tmp_path, LI_LOG_PATH=str(tiny_log)))):
        pass
    assert run(search_logins)["data"]["total"] == truth["row_count"]


def test_a_startup_that_fails_leaves_nothing_behind(monkeypatch, tmp_path, tiny_log, truth):
    """A failed startup never reaches shutdown, so it must not have handed anything over."""
    def broken(path):
        raise OSError("the memory file cannot be opened")
    monkeypatch.setattr(investigations, "open_memory", broken)
    with pytest.raises(OSError):
        with TestClient(create_app(settings_for(tmp_path, LI_LOG_PATH=str(tiny_log)))):
            pass
    assert run(search_logins)["data"]["total"] == truth["row_count"]
