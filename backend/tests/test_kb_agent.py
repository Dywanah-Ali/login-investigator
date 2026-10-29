"""T24: the first graph tool through the agent and application lifecycle doors."""

import json
import asyncio
import sqlite3
from contextlib import asynccontextmanager
from collections import Counter
from dataclasses import replace

from sqlalchemy import text

import pytest
from fastapi.testclient import TestClient
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.runnables import RunnableConfig
from sqlalchemy.exc import DBAPIError
from pydantic import Field

from api.app import create_app
from login_investigator import agent, investigations, knowledge_base
from tests.test_agent import FakeModel, tool_call
from tests.test_api_startup import built, memory_path, startup_settings  # noqa: F401
from tests.test_knowledge_base import FakeEmbedder, publish
from login_investigator.postgres import create_fresh_database, drop_database


class ObservingModel(FakeModel):
    seen: list = Field(default_factory=list)

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        self.seen.append(messages)
        return super()._generate(messages, stop=stop, run_manager=run_manager, **kwargs)


def test_lookup_uses_the_checked_graph_and_saves_its_evidence(built, memory_path, monkeypatch):
    dataset, state = built
    model = FakeModel(responses=[
        tool_call("lookup_account", {"account_id": "thomas.price"}),
        AIMessage("Thomas Price belongs to IT and All Staff."),
    ])
    monkeypatch.setattr(agent, "make_model", lambda: model)
    app = create_app(startup_settings(dataset, state, memory_path))
    with TestClient(app):
        configured = app.state.services.agent
        configured.invoke({"messages": [{"role": "user", "content": "Whose account is thomas.price?"}]},
                          {"configurable": {"thread_id": "lookup"}})
        messages = configured.get_state({"configurable": {"thread_id": "lookup"}}).values["messages"]
        result = next(message for message in messages if isinstance(message, ToolMessage))
        assert "Thomas Price" in result.text
        assert result.artifact["account"]["person_id"] == "user-thomas.price"
        assert result.artifact["account"]["department"] == "IT"
        assert {group["name"] for group in result.artifact["groups"]} == {"All Staff"}
        assert json.loads(json.dumps(result.artifact)) == result.artifact


def test_artifact_stays_saved_but_never_enters_model_input(built, memory_path, monkeypatch):
    dataset, state = built
    model = ObservingModel(responses=[
        tool_call("lookup_account", {"account_id": "user-thomas.price"}),
        AIMessage("Thomas Price is in IT."),
    ])
    monkeypatch.setattr(agent, "make_model", lambda: model)
    app = create_app(startup_settings(dataset, state, memory_path))
    with TestClient(app) as client:
        case = client.post("/api/investigations", json={"question": "Whose account is this?"}).json()
        reply = client.post(f"/api/investigations/{case['id']}/ask",
                            json={"question": "Whose account is user-thomas.price?"})
        assert reply.status_code == 200 and 'event: error' not in reply.text
        assert len(model.seen) == 2
        seen = next(m for m in model.seen[-1] if isinstance(m, ToolMessage))
        assert "Thomas Price" in seen.text
        assert seen.artifact is None
        assert "group-all-staff" not in seen.model_dump_json()
        saved = app.state.services.memory.get_tuple({"configurable": {"thread_id": case["id"]}})
        result = next(m for m in saved.checkpoint["channel_values"]["messages"] if isinstance(m, ToolMessage))
        assert result.artifact["groups"]
        reopened = client.get(f"/api/investigations/{case['id']}").json()
        view = reopened["turns"][0]["tools"][0]
        assert view["title"] == "Account context"
        assert "Thomas Price" in view["found"]
        assert "artifact" not in view


@pytest.mark.parametrize("name,args", [
    ("search_logins", {"user": "thomas.price"}),
    ("find_suspicious_activity", {"user": "thomas.price"}),
    ("lookup_ip_reputation", {"ip": "192.0.2.1"}),
    ("lookup_account", {"account_id": "thomas.price"}),
])
def test_every_tool_result_reaches_model_inside_an_untrusted_fence(name, args, memory_path):
    from login_investigator.investigations import open_memory

    model = ObservingModel(responses=[tool_call(name, args), AIMessage("Read the evidence.")])
    memory = open_memory(memory_path)
    try:
        configured = agent.build_agent(model, memory)
        configured.invoke({"messages": [{"role": "user", "content": "Check thomas.price only."}]},
                          {"configurable": {"thread_id": "fence"}})
        results = [m for m in model.seen[-1] if isinstance(m, ToolMessage)]
        assert results
        for result in results:
            assert result.text.startswith(f'<tool_result source="{result.name}" trust="untrusted">\n')
            assert result.text.endswith("\n</tool_result>")
    finally:
        memory.conn.close()


def test_rebuilt_dataset_is_adopted_only_on_restart(built, memory_path, fresh_database, monkeypatch):
    dataset, state = built
    monkeypatch.setattr(agent, "make_model", lambda: FakeModel(responses=[]))
    settings = startup_settings(dataset, state, memory_path)
    app = create_app(settings)
    replacement = create_fresh_database(replace(fresh_database, database="postgres"))
    try:
        with TestClient(app):
            original = app.state.knowledge_base
            assert original.lookup_account("amelia.ward")["account"]["department"] == "IT"
            people = dataset / "org/people.csv"
            people.write_text(people.read_text().replace("Amelia Ward,IT,", "Amelia Ward,Operations,"))
            asyncio.run(knowledge_base.build_knowledge_base(dataset, replacement, FakeEmbedder()))
            publish(state, replacement)
            assert original.lookup_account("amelia.ward")["account"]["department"] == "IT"
        restarted = create_app(settings)
        with TestClient(restarted):
            assert restarted.state.knowledge_base is not original
            assert restarted.state.knowledge_base.lookup_account("amelia.ward")["account"]["department"] == "Operations"
    finally:
        drop_database(replacement)


def test_startup_failure_closes_memory_and_the_knowledge_base(built, memory_path, monkeypatch):
    dataset, state = built
    opened = []
    closed = []
    real_memory = investigations.open_memory
    real_open = knowledge_base.open_current_knowledge_base

    def memory(*args, **kwargs):
        result = real_memory(*args, **kwargs)
        opened.append(result)
        return result

    @asynccontextmanager
    async def observed_open(*args, **kwargs):
        try:
            async with real_open(*args, **kwargs) as kb:
                yield kb
        finally:
            closed.append(True)

    def broken(*args, **kwargs):
        raise RuntimeError("Agent construction failed")

    monkeypatch.setattr(investigations, "open_memory", memory)
    monkeypatch.setattr(knowledge_base, "open_current_knowledge_base", observed_open)
    monkeypatch.setattr(agent, "make_model", lambda: FakeModel(responses=[]))
    monkeypatch.setattr(agent, "build_agent", broken)
    with pytest.raises(RuntimeError, match="Agent construction failed"):
        with TestClient(create_app(startup_settings(dataset, state, memory_path))):
            pytest.fail("Startup accepted a failed agent")
    with pytest.raises(sqlite3.ProgrammingError, match="closed"):
        opened[0].conn.execute("SELECT 1")
    assert closed == [True]


def test_graph_prepared_once_reused_across_investigations_and_pool_closed(built, memory_path, monkeypatch):
    dataset, state = built
    counts = Counter()
    real_build = knowledge_base.build_graph
    real_check = knowledge_base.KnowledgeBase.check_graph_integrity
    real_open = knowledge_base.open_knowledge_base
    pools = []

    async def build(*args, **kwargs):
        counts["build"] += 1
        return await real_build(*args, **kwargs)

    async def check(self, *args, **kwargs):
        counts["check"] += 1
        return await real_check(self, *args, **kwargs)

    @asynccontextmanager
    async def observed_open(settings, **kwargs):
        async with real_open(settings, **kwargs) as kb:
            if kwargs.get("dataset") is not None:
                # Public database boundary verifies the identity and transaction restriction
                # used to prepare the graph, not just a configuration string.
                async with kb.engine.connect() as connection:
                    assert await connection.scalar(text("SELECT current_user")) == "li_reader"
                    with pytest.raises(DBAPIError, match="permission denied"):
                        await connection.execute(text("DELETE FROM people"))
                pools.append(kb.engine.pool)
            yield kb

    monkeypatch.setattr(knowledge_base, "build_graph", build)
    monkeypatch.setattr(knowledge_base.KnowledgeBase, "check_graph_integrity", check)
    monkeypatch.setattr(knowledge_base, "open_knowledge_base", observed_open)
    model = FakeModel(responses=[item for i in range(3) for item in (
        tool_call("lookup_account", {"account_id": "amelia.ward"}, f"lookup-{i}"),
        AIMessage("Amelia Ward belongs to IT Admins."),
    )])
    monkeypatch.setattr(agent, "make_model", lambda: model)
    app = create_app(startup_settings(dataset, state, memory_path))
    with TestClient(app) as client:
        assert counts == {"build": 1, "check": 1}
        for _ in range(3):
            case = client.post("/api/investigations", json={"question": "Whose account is amelia.ward?"}).json()
            reply = client.post(f"/api/investigations/{case['id']}/ask", json={"question": case["first_question"]})
            assert 'event: error' not in reply.text
            assert "Amelia Ward" in reply.text
        assert counts == {"build": 1, "check": 1}
        assert pools[0].checkedout() == 0
    assert pools[0].checkedin() == 0
    with pytest.raises(sqlite3.ProgrammingError, match="closed"):
        app.state.services.memory.conn.execute("SELECT 1")


def test_integrity_failure_prevents_startup_and_disposes_pool(built, memory_path, monkeypatch):
    dataset, state = built
    real_build = knowledge_base.build_graph
    real_engine = knowledge_base.database_engine
    pools = []

    async def corrupt(*args, **kwargs):
        graph, frame = await real_build(*args, **kwargs)
        graph.nodes["user-amelia.ward"]["department"] = "Incorrect department"
        return graph, frame

    def engine(*args, **kwargs):
        result = real_engine(*args, **kwargs)
        pools.append(result.pool)
        return result

    monkeypatch.setattr(knowledge_base, "build_graph", corrupt)
    monkeypatch.setattr(knowledge_base, "database_engine", engine)
    with pytest.raises(knowledge_base.KnowledgeBaseNotReady):
        with TestClient(create_app(startup_settings(dataset, state, memory_path))):
            pytest.fail("Corrupt graph reached the application")
    assert not memory_path.exists()
    assert pools and all(pool.checkedin() == pool.checkedout() == 0 for pool in pools)


def test_saved_evidence_survives_close_reopen_without_source_and_stays_out_of_followup(
    built, memory_path, monkeypatch,
):
    dataset, state = built
    monkeypatch.setattr(agent, "make_model", lambda: FakeModel(responses=[
        tool_call("lookup_account", {"account_id": "amelia.ward"}), AIMessage("Amelia Ward is in IT."),
    ]))
    app = create_app(startup_settings(dataset, state, memory_path))
    config: RunnableConfig = {"configurable": {"thread_id": "saved"}}
    with TestClient(app):
        app.state.services.agent.invoke({"messages": [{"role": "user", "content": "Who owns amelia.ward?"}]}, config)
        saved = app.state.services.memory.get_tuple(config)
        original = next(m.artifact for m in saved.checkpoint["channel_values"]["messages"] if isinstance(m, ToolMessage))

    def forbidden(*args, **kwargs):
        pytest.fail("Reopening evidence must not query the current graph")

    monkeypatch.setattr(knowledge_base.KnowledgeBase, "lookup_account", forbidden)
    memory = investigations.open_memory(memory_path)
    try:
        saved = memory.get_tuple(config)
        assert saved is not None
        restored = next(m.artifact for m in saved.checkpoint["channel_values"]["messages"] if isinstance(m, ToolMessage))
        assert restored == original
        assert restored["account"]["display_name"] == "Amelia Ward"
        model = ObservingModel(responses=[AIMessage("The saved evidence names Amelia Ward.")])
        reopened = agent.build_agent(model, memory)
        reopened.invoke({"messages": [{"role": "user", "content": "Remind me who that was."}]}, config)
        assert all(m.artifact is None for m in model.seen[-1] if isinstance(m, ToolMessage))
        assert "group-it-admins" not in " ".join(m.model_dump_json() for m in model.seen[-1])
    finally:
        memory.conn.close()
