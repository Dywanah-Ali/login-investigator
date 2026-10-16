"""Ticket 16, through HTTP with the copied model fixture and real temporary memory."""

import json
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor
from threading import Event

import pytest
import anyio
from fastapi.testclient import TestClient
from langchain_core.messages import AIMessage, AIMessageChunk
from langchain_core.outputs import ChatGenerationChunk
from langchain_core.runnables import RunnableLambda
from pypdf import PdfReader

from api.app import create_app
from api.settings import Settings
from login_investigator import agent
from test_agent import FakeModel, REPORT, tool_call


@pytest.fixture
def settings(tmp_path):
    return Settings.from_env({"LI_MEMORY_PATH": str(tmp_path / "cases.sqlite")})


@pytest.fixture
def model(monkeypatch):
    model = FakeModel(responses=[
        tool_call("search_logins", {"ip": "185.218.86.24"}),
        AIMessage("**150** failures, then one success."),
    ])
    monkeypatch.setattr(agent, "make_model", lambda: model)
    return model


@pytest.fixture
def client(settings, model):
    with TestClient(create_app(settings)) as client:
        yield client


def start(client, question="What did 185.218.86.24 do?"):
    response = client.post("/api/investigations", json={"question": question})
    assert response.status_code == 201
    return response.json()


def events(response):
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/event-stream")
    result = []
    for block in response.text.replace("\r\n", "\n").split("\n\n"):
        fields = dict(line.split(": ", 1) for line in block.splitlines() if ": " in line)
        if "event" in fields:
            result.append((fields["event"], json.loads(fields["data"])))
    return result


def test_start_only_creates_a_record_and_list_is_full_newest_first(client):
    first = start(client, "  first question  ")
    second = start(client, "second question")
    assert set(first) == {"id", "started_at", "first_question"}
    assert first["first_question"] == "first question"
    assert first["started_at"].endswith("Z")
    assert first["id"] != second["id"]
    assert client.get("/api/investigations").json() == {"investigations": [second, first]}
    assert client.get(f"/api/investigations/{first['id']}").json() == {
        **first, "turns": [], "report_offer": None,
    }


def test_ask_streams_then_reopen_shows_the_saved_answer_and_tool_evidence(client):
    case = start(client)
    path = f"/api/investigations/{case['id']}"
    assert events(client.post(path + "/ask", json={"question": case["first_question"]})) == [
        ("tool", {"name": "search_logins"}),
        ("text", {"text": "**150** failures, then one success."}),
        ("done", {}),
    ]
    reopened = client.get(path).json()
    assert reopened["report_offer"] == "Write the incident report"
    [turn] = reopened["turns"]
    assert turn["question"] == case["first_question"]
    assert turn["answer"] == "**150** failures, then one success."
    assert turn["report"] is None
    [tool] = turn["tools"]
    assert set(tool) == {"title", "asked", "found", "columns", "rows", "raw"}
    assert tool["title"] == "Sign-in search"
    assert tool["asked"] == "IP 185.218.86.24, all times"
    assert tool["found"].startswith("151 events: 150 failed, 1 succeeded")
    assert tool["columns"] == ["timestamp_utc", "username", "source_ip", "country", "outcome",
                               "failure_reason", "user_agent"]
    assert len(tool["rows"]) == 20
    assert json.loads(tool["raw"])["data"]["failures"] == 150


def test_report_offer_numbering_and_update_survive_reopen(client, monkeypatch):
    case = start(client)
    path = f"/api/investigations/{case['id']}"
    refused = client.post(path + "/report", json={"request": "Write the incident report"})
    assert refused.status_code == 409
    assert refused.json()["error"]["code"] == "not_offered"
    events(client.post(path + "/ask", json={"question": case["first_question"]}))
    report = client.post(path + "/report", json={"request": "Write the incident report"})
    assert report.status_code == 200
    assert report.json() == {**REPORT.model_dump(), "number": 1}
    saved = client.get(path).json()
    assert saved["turns"][-1]["report"] == report.json()
    assert saved["report_offer"] is None

    assert client.post(path + "/report", json={"request": "Write the incident report"}).status_code == 409
    events(client.post(path + "/ask", json={"question": "What else?"}))
    assert client.get(path).json()["report_offer"] == "Update the incident report"
    assert client.post(path + "/report", json={"request": "Write the incident report"}).status_code == 409
    updated_report = REPORT.model_copy(update={"title": "Updated incident report"})
    monkeypatch.setattr(FakeModel, "with_structured_output",
                        lambda *args, **kwargs: RunnableLambda(lambda _: updated_report))
    updated = client.post(path + "/report", json={"request": "Update the incident report"})
    assert updated.json() == {**updated_report.model_dump(), "number": 2}
    saved = client.get(path).json()
    assert saved["turns"][-1]["report"] == updated.json()
    assert saved["report_offer"] is None
    for number, title in [(1, REPORT.title), (2, updated_report.title)]:
        pdf = client.get(path + f"/reports/{number}.pdf")
        assert pdf.status_code == 200
        assert title in PdfReader(BytesIO(pdf.content)).pages[0].extract_text()


def test_history_and_pdf_survive_restart_and_pdf_needs_no_model(settings, model, monkeypatch):
    with TestClient(create_app(settings)) as client:
        case = start(client)
        path = f"/api/investigations/{case['id']}"
        events(client.post(path + "/ask", json={"question": case["first_question"]}))
        client.post(path + "/report", json={"request": "Write the incident report"})
        saved = client.get(path).json()
    with TestClient(create_app(settings)) as client:
        assert client.get(path).json() == saved
        assert client.get("/api/investigations").json() == {"investigations": [case]}

    def unavailable():
        raise RuntimeError("OPENROUTER_API_KEY is not set")

    monkeypatch.setattr(agent, "make_model", unavailable)
    with TestClient(create_app(settings)) as client:
        pdf = client.get(path + "/reports/1.pdf")
        assert pdf.status_code == 200
        assert pdf.headers["content-type"] == "application/pdf"
        assert pdf.headers["content-disposition"] == (
            f'attachment; filename="incident-report-{case["id"][:8]}-1.pdf"'
        )
        reader = PdfReader(BytesIO(pdf.content))
        assert REPORT.title in reader.pages[0].extract_text()
        for suffix in ["/reports/0.pdf", "/reports/-1.pdf", "/reports/2.pdf"]:
            assert client.get(path + suffix).status_code == 404
        assert client.get("/api/investigations/unknown/reports/1.pdf").status_code == 404
        for method, suffix, body in [
            ("GET", "", None), ("POST", "/ask", {"question": "hello"}),
            ("POST", "/report", {"request": "Update the incident report"}),
        ]:
            response = client.request(method, path + suffix, json=body)
            assert response.status_code == 503
            assert response.json()["error"]["code"] == "agent_unavailable"


@pytest.mark.parametrize("body", [
    {"question": ""}, {"question": " \n\t"}, {"question": "x" * 2001},
    {"question": None}, {"question": 5}, {}, [],
])
def test_invalid_questions_are_refused_before_streaming_without_echo(client, body):
    case = start(client)
    for path in ["/api/investigations", f"/api/investigations/{case['id']}/ask"]:
        response = client.post(path, json=body)
        assert response.status_code == 422
        assert response.headers["content-type"] == "application/json"
        assert set(response.json()) == {"error"}
        assert response.json()["error"]["code"] in {"invalid_question", "invalid_request"}
        assert "x" * 100 not in response.text
    assert client.get(f"/api/investigations/{case['id']}").json()["turns"] == []


def test_maximum_question_is_trimmed_and_list_label_is_shortened(client, model):
    model.responses = [AIMessage("Answer")]
    question = "q" * 2000
    case = start(client, "  " + question + "\n")
    assert case["first_question"] == "q" * 200
    path = f"/api/investigations/{case['id']}"
    events(client.post(path + "/ask", json={"question": "  " + question + "\n"}))
    assert client.get(path).json()["turns"][0]["question"] == question


def test_unknown_cases_and_invalid_report_requests_return_fixed_json(client):
    for method, suffix, body in [
        ("GET", "", None), ("POST", "/ask", {"question": "hello"}),
        ("POST", "/report", {"request": "Write the incident report"}),
        ("GET", "/reports/1.pdf", None),
    ]:
        response = client.request(method, "/api/investigations/unknown" + suffix, json=body)
        assert response.status_code == 404
        assert response.json() == {"error": {"code": "not_found", "message": "Not found."}}
    case = start(client)
    response = client.post(f"/api/investigations/{case['id']}/report",
                           json={"request": "<script>hostile</script>"})
    assert response.status_code == 422
    assert response.json() == {"error": {"code": "invalid_request", "message": "The request is not valid."}}


def test_missing_key_refuses_investigations_but_leaves_all_dashboards_working(settings, monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "")
    with TestClient(create_app(settings)) as client:
        for method, path, body in [
            ("GET", "/api/investigations", None),
            ("POST", "/api/investigations", {"question": "hello"}),
        ]:
            response = client.request(method, path, json=body)
            assert response.status_code == 503
            assert response.json() == {"error": {
                "code": "agent_unavailable",
                "message": "OPENROUTER_API_KEY is not set. Copy env.example to .env and add the key.",
            }}
        for path in ["dataset", "overview", "alerts", "explorer", "explorer.csv", "rules"]:
            assert client.get("/api/" + path).status_code == 200


def test_tool_views_without_tables_have_null_rows_and_no_columns(client, model):
    model.responses = [tool_call("lookup_ip_reputation", {"ip": "192.0.2.1"}), AIMessage("Reserved IP.")]
    case = start(client)
    path = f"/api/investigations/{case['id']}"
    events(client.post(path + "/ask", json={"question": "Check 192.0.2.1"}))
    [tool] = client.get(path).json()["turns"][0]["tools"]
    assert tool["title"] == "IP reputation"
    assert tool["rows"] is None
    assert tool["columns"] == []


def test_active_ask_refuses_other_writers_but_other_cases_work(client, model, monkeypatch):
    model.responses = [AIMessage("Answer")]
    started, release = Event(), Event()
    real_generate = FakeModel._generate

    def blocked(self, *args, **kwargs):
        if not started.is_set():
            started.set()
            assert release.wait(10), "test did not release the model"
        return real_generate(self, *args, **kwargs)

    monkeypatch.setattr(FakeModel, "_generate", blocked)
    first, second = start(client), start(client)
    path = f"/api/investigations/{first['id']}"
    with ThreadPoolExecutor() as pool:
        pending = pool.submit(client.post, path + "/ask", json={"question": "First"})
        try:
            assert started.wait(10), "model did not start"
            for suffix, body in [("/ask", {"question": "Second"}),
                                 ("/report", {"request": "Write the incident report"})]:
                response = client.post(path + suffix, json=body)
                assert response.status_code == 409
                assert response.json()["error"]["code"] == "busy"
            other_path = f"/api/investigations/{second['id']}"
            assert events(client.post(other_path + "/ask", json={"question": "Other"}))[-1] == ("done", {})
        finally:
            release.set()
        assert events(pending.result(timeout=10))[-1] == ("done", {})
    assert len(client.get(path).json()["turns"]) == 1
    assert events(client.post(path + "/ask", json={"question": "After"}))[-1] == ("done", {})


def test_model_failure_sends_fixed_error_logs_details_and_releases_case(client, monkeypatch, caplog):
    def failed(*args, **kwargs):
        raise RuntimeError("private model error should stay on server")

    monkeypatch.setattr(FakeModel, "_generate", failed)
    case = start(client)
    path = f"/api/investigations/{case['id']}"
    for _ in range(2):
        response = client.post(path + "/ask", json={"question": "Question"})
        assert events(response) == [("error", {
            "code": "agent_failed", "message": "The agent stopped before it finished.",
        })]
        assert "private model error" not in response.text
    assert "private model error should stay on server" in caplog.text


def test_failure_after_partial_text_ends_with_error_and_never_done(client, monkeypatch):
    def partial(*args, **kwargs):
        yield ChatGenerationChunk(message=AIMessageChunk(content="Partial answer"))
        raise RuntimeError("private failure after a chunk")

    monkeypatch.setattr(FakeModel, "_stream", partial)
    case = start(client)
    response = client.post(f"/api/investigations/{case['id']}/ask", json={"question": "Question"})
    assert events(response) == [
        ("text", {"text": "Partial answer"}),
        ("error", {"code": "agent_failed", "message": "The agent stopped before it finished."}),
    ]
    assert "private failure" not in response.text


def test_disconnect_stops_advancing_the_core_and_releases_the_case(client, monkeypatch):
    """Drive HTTP disconnect through ASGI: TestClient's normal calls buffer the whole stream."""
    advanced = []
    closed = Event()
    real_ask = agent.ask

    def tracked_ask(*args, **kwargs):
        # Count actual core advancement, not model chunks buffered inside LangGraph.
        stream = real_ask(*args, **kwargs)
        try:
            for item in stream:
                advanced.append(item)
                yield item
        finally:
            stream.close()
            closed.set()

    def chunks(*args, **kwargs):
        for i in range(1000):
            yield ChatGenerationChunk(message=AIMessageChunk(content="piece"))

    monkeypatch.setattr(FakeModel, "_stream", chunks)
    monkeypatch.setattr(agent, "ask", tracked_ask)
    case = start(client)
    path = f"/api/investigations/{case['id']}"

    async def disconnect_after_text():
        disconnected = anyio.Event()
        received_body = False
        sent = []

        async def receive():
            nonlocal received_body
            if not received_body:
                received_body = True
                return {"type": "http.request", "body": b'{"question":"Question"}', "more_body": False}
            await disconnected.wait()
            return {"type": "http.disconnect"}

        async def send(message):
            sent.append(message)
            if b"event: text" in message.get("body", b""):
                disconnected.set()
            await anyio.sleep(0)

        scope = {"type": "http", "asgi": {"version": "3.0", "spec_version": "2.0"},
                 "method": "POST", "path": path + "/ask", "raw_path": (path + "/ask").encode(),
                 "query_string": b"", "root_path": "", "scheme": "http", "http_version": "1.1",
                 "headers": [(b"content-type", b"application/json")],
                 "client": ("testclient", 1234), "server": ("testserver", 80)}
        with anyio.fail_after(10):
            await client.app(scope, receive, send)
        assert disconnected.is_set()
        assert not any(b"event: done" in message.get("body", b"") for message in sent)

    assert client.portal is not None
    client.portal.call(disconnect_after_text)
    assert 0 < len(advanced) < 1000
    assert closed.wait(1), "the core generator was not closed"
    monkeypatch.undo()
    # A follow-up is accepted, rather than finding an abandoned busy reservation.
    assert events(client.post(path + "/ask", json={"question": "After disconnect"}))[-1] == ("done", {})
