"""Saved eval evidence identifies its transport and cannot disclose loaded API keys."""

import json
import sys
from datetime import datetime, timezone

import pytest

from evals import run


def test_saved_results_label_the_mode_and_redact_keys(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(run, "RESULTS", tmp_path)
    monkeypatch.setenv("OPENROUTER_API_KEY", "fake-model-secret")
    monkeypatch.setenv("ABUSEIPDB_API_KEY", "fake-reputation-secret")
    records = [{"question": "Q01", "category": "detection", "run": 1,
                "checks": [{"id": "a check", "security": True, "passed": False}],
                "passed": False, "security_checked": True, "security_passed": False,
                "error": "provider included fake-model-secret and fake-reputation-secret"}]
    run.save(records, datetime.now(timezone.utc), "35d4d98f", "test", 1, 1,
             "API smoke", mode="api")
    [path] = tmp_path.glob("*.json")
    saved = json.loads(path.read_text())
    assert saved["mode"] == "api"
    assert saved["summary"]["overall"] == 0
    output = path.read_text() + (tmp_path / "summary.md").read_text() + capsys.readouterr().out
    assert "fake-model-secret" not in output
    assert "fake-reputation-secret" not in output
    assert "api: API smoke" in (tmp_path / "summary.md").read_text()


@pytest.mark.parametrize("arguments, message", [
    (["--mode", "api", "--runs", "0"], "must be a positive integer"),
    (["--mode", "api", "--jobs", "-1"], "must be a positive integer"),
    (["--mode", "api", "--only", "Q99"], "Unknown question ids: Q99"),
    (["--mode", "api", "--only"], "--only needs at least one question id"),
])
def test_cli_refuses_invalid_runs_before_loading_model(arguments, message, monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["evals.run", *arguments])
    with pytest.raises(SystemExit) as error:
        run.main()
    assert error.value.code == 2
    assert message in capsys.readouterr().err
