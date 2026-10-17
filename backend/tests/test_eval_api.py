"""The eval runner uses the public HTTP API, never the app's memory or private state."""

import httpx
import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from langchain_core.messages import AIMessage

from api.app import create_app
from api.settings import Settings
from evals import api_runner, run
from evals.scoring import load_questions
from login_investigator import agent
from tests.test_agent import FakeModel, REPORT, tool_call


def test_eval_server_uses_temporary_memory_and_cannot_reload_real_keys(monkeypatch):
    # A child does not inherit pytest's in-process guard. Even with a key in the parent,
    # the eval server must never recover the AbuseIPDB key from either source.
    monkeypatch.setenv("ABUSEIPDB_API_KEY", "fake-parent-key")
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.setenv("LI_MEMORY_PATH", "/not-the-eval-memory/cases.sqlite")
    # Observe the operating-system boundary while still launching the real child.
    popen = api_runner.subprocess.Popen
    child_env = {}

    def launch(*args, **kwargs):
        child_env.update(kwargs["env"])
        return popen(*args, **kwargs)

    monkeypatch.setattr(api_runner.subprocess, "Popen", launch)
    with api_runner.serve() as client:
        assert "ABUSEIPDB_API_KEY" not in child_env
        assert child_env["PYTHON_DOTENV_DISABLED"] == "1"
        memory = Path(child_env["LI_MEMORY_PATH"])
        assert memory.is_file()
        assert client.get("/api/dataset").status_code == 200
        response = client.post("/api/investigations", json={"question": "Anything suspicious?"})
        assert response.status_code == 503
        assert response.json()["error"]["code"] == "agent_unavailable"
        url = str(client.base_url)
    assert not memory.exists()
    # The child is stopped and its listening socket is closed on leaving the context.
    try:
        httpx.get(url, timeout=1, trust_env=False)
    except httpx.ConnectError:
        pass
    else:
        raise AssertionError("Eval server is still listening")


def test_api_eval_scores_the_reopened_answer_and_original_tool_arguments(tmp_path, monkeypatch):
    model = FakeModel(responses=[tool_call("search_logins", {"ip": "185.218.86.24"}),
                                 AIMessage("daniel.hughes signed in at 02:32 UTC.")])
    monkeypatch.setattr(agent, "make_model", lambda: model)
    settings = Settings.from_env({"LI_MEMORY_PATH": str(tmp_path / "eval.sqlite")})
    question = next(q for q in load_questions() if q["id"] == "Q05")
    with TestClient(create_app(settings)) as client:
        record = run.run_api_once(client, question, 1)
        assert record["passed"], record
        assert record["tools"] == [{"name": "search_logins", "args": {"ip": "185.218.86.24"}}]
        assert record["answer"] == "daniel.hughes signed in at 02:32 UTC."
        assert record["earlier_turns"] == []
        assert record["live_lookup"] is False
        # Every run gets a new Investigation, even for the same question.
        assert run.run_api_once(client, question, 2)["passed"]
        assert len(client.get("/api/investigations").json()["investigations"]) == 2


def test_api_eval_keeps_follow_up_turns_and_scores_only_the_last(tmp_path, monkeypatch):
    model = FakeModel(responses=[
        AIMessage("Earlier answer without the final answer's facts."),
        tool_call("search_logins", {"user": "daniel.hughes", "start": "2026-10-08T02:32:21Z"}),
        AIMessage("Two sign-ins afterwards: 198.51.100.20 at 07:23 and 203.0.113.10 at 08:45."),
    ])
    monkeypatch.setattr(agent, "make_model", lambda: model)
    settings = Settings.from_env({"LI_MEMORY_PATH": str(tmp_path / "eval.sqlite")})
    question = next(q for q in load_questions() if q["id"] == "Q07")
    with TestClient(create_app(settings)) as client:
        record = run.run_api_once(client, question, 1)
    assert record["passed"], record
    assert record["earlier_turns"] == [{"question": question["turns"][0],
                                        "answer": "Earlier answer without the final answer's facts.",
                                        "tools": []}]


def test_api_eval_writes_and_reopens_a_report(tmp_path, monkeypatch):
    model = FakeModel(responses=[AIMessage("Found an account takeover.")])
    monkeypatch.setattr(agent, "make_model", lambda: model)
    settings = Settings.from_env({"LI_MEMORY_PATH": str(tmp_path / "eval.sqlite")})
    question = {"id": "report", "category": "report", "turns": ["Find attacks", "REPORT"],
                "checks": [{"id": "critical", "report": {"field": "severity", "equals": "critical"},
                            "security": True}]}
    with TestClient(create_app(settings)) as client:
        record = run.run_api_once(client, question, 1)
    assert record["passed"], record
    assert record["report"] == REPORT.model_dump()
    assert "number" not in record["report"]
    assert "severity: critical" in record["answer"]
    assert record["tools"] == []
    assert len(record["earlier_turns"]) == 1


@pytest.mark.parametrize("body", [
    b'event: text\r\ndata: {"text":"partial"}\r\n\r\n',
    b'event: error\ndata: {"code":"agent_failed"}\n\nevent: done\ndata: {}\n\n',
])
def test_incomplete_or_failed_stream_is_a_failed_eval_even_if_history_would_pass(body):
    def handle(request):
        if request.url.path == "/api/investigations":
            return httpx.Response(201, json={"id": "test"})
        if request.url.path.endswith("/ask"):
            return httpx.Response(200, headers={"content-type": "text/event-stream"}, content=body)
        raise AssertionError("A failed stream must not be scored from old saved history")

    question = {"id": "stream", "category": "injection", "turns": ["Find attacks"],
                "checks": [{"id": "saved answer", "has": "correct", "security": True}]}
    with httpx.Client(transport=httpx.MockTransport(handle), base_url="http://eval") as client:
        record = run.run_api_once(client, question, 1)
    assert record["passed"] is False
    assert record["security_passed"] is False
    assert record["checks"] == [{"id": "saved answer", "security": True, "passed": False}]
    assert "error" in record
