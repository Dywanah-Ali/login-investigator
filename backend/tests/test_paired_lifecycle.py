"""T48: complete source worlds through the application and knowledge-base doors."""

import asyncio
import json
import shutil

import pytest
from fastapi.testclient import TestClient

from api.app import create_app
from api.settings import Settings
from login_investigator.knowledge_base.graph_version import (
    build_version,
    remove_version,
)
from login_investigator.postgres import ServerSettings
from tests.test_knowledge_base import DATASET, FakeEmbedder, sample_dataset


def assert_reader_disconnected(version):
    """Count this application's reader, not pgAdmin or server maintenance connections."""
    import psycopg

    from login_investigator.knowledge_base import reader_settings

    server = ServerSettings.from_env()
    with psycopg.connect(server.conninfo()) as connection:
        assert connection.execute(
            'SELECT count(*) FROM pg_stat_activity WHERE datname=%s AND usename=%s',
            (version.database, reader_settings(server).user),
        ).fetchone() == (0,)


@pytest.fixture(scope='module')
def version(tmp_path_factory):
    root = tmp_path_factory.mktemp('paired-lifecycle')
    server = ServerSettings.from_env()
    source = sample_dataset(root / 'inputs')
    shutil.copy(DATASET / 'logins.csv', source / 'logins.csv')
    built = asyncio.run(build_version(source, root, server, FakeEmbedder(), offline_embeddings=True))
    try:
        yield built
    finally:
        remove_version(built, server)


def test_app_reads_selected_snapshot_when_working_log_changes(version, tmp_path):
    working = tmp_path / 'working'
    shutil.copytree(DATASET, working)
    (working / 'logins.csv').write_text('invalid working input')
    pointer = tmp_path / 'selected.json'
    pointer.write_text(json.dumps({'format': 'paired-v1', 'current': str(version.marker), 'previous': None}))
    app = create_app(Settings.from_env({
        'LI_DATASET_DIR': str(working), 'LI_KNOWLEDGE_BASE_STATE': str(pointer),
        'LI_MEMORY_PATH': str(tmp_path / 'memory.sqlite'),
    }))
    with TestClient(app) as client:
        assert client.get('/api/dataset').status_code == 200
        assert app.state.services.settings.dataset_dir == version.snapshot
        assert app.state.knowledge_base.lookup_account('amelia.ward')['account']['department'] == 'IT'


def test_startup_graph_reads_do_not_block_the_event_loop(version, monkeypatch):
    import threading

    from neo4j import Session

    from login_investigator.knowledge_base.graph_version import open_version

    owner = threading.current_thread()
    original = Session.run

    def checked(self, *args, **kwargs):
        assert threading.current_thread() is not owner, 'Graph network call blocked the event loop'
        return original(self, *args, **kwargs)

    monkeypatch.setattr(Session, 'run', checked)

    async def check():
        async with open_version(version.marker, ServerSettings.from_env()):
            pass

    asyncio.run(check())


def test_direct_retrieval_uses_native_integrity_and_worker_graph_reads(version, monkeypatch):
    import threading
    from pathlib import Path

    from neo4j import Session

    from evals.retrieval import evaluate_retrieval
    from login_investigator.knowledge_base.graph_version import open_version

    owner = threading.current_thread()
    original = Session.run

    def checked(self, *args, **kwargs):
        assert threading.current_thread() is not owner, 'Retrieval blocked the event loop'
        return original(self, *args, **kwargs)

    monkeypatch.setattr(Session, 'run', checked)
    question = next(q for q in json.loads((Path(__file__).parents[1] /
        'evals/knowledge_base_questions.json').read_text())['questions'] if q['id'] == 'K03')

    async def check():
        async with open_version(version.marker, ServerSettings.from_env(), embedder=FakeEmbedder()) as kb:
            report = await evaluate_retrieval(kb, [question])
            assert report['records'][0]['passed'] is True

    asyncio.run(check())


def test_update_and_rollback_move_logs_graph_and_retrieval_together(version, tmp_path, monkeypatch):
    from langchain_core.messages import AIMessage, ToolMessage

    from login_investigator import agent
    from login_investigator.knowledge_base import (
        KnowledgeBaseNotReady,
        open_current_knowledge_base,
    )
    from login_investigator.knowledge_base.graph_selection import (
        rollback_version,
        select_version,
    )
    from tests.test_agent import FakeModel, tool_call

    monkeypatch.setattr(agent, 'make_model', lambda: FakeModel(responses=[
        tool_call('lookup_account', {'account_id': 'amelia.ward'}), AIMessage('Amelia Ward belongs to IT.')]))

    source = sample_dataset(tmp_path / 'inputs')
    lines = (DATASET / 'logins.csv').read_text().splitlines()
    (source / 'logins.csv').write_text('\n'.join([lines[0], *lines[11:]]) + '\n')
    people = source / 'org/people.csv'
    people.write_text(people.read_text().replace('Amelia Ward,IT,', 'Amelia Ward,Operations,'))
    document = source / 'corpus/own/sample.md'
    document.write_text(document.read_text().replace('thomas.price', 'amelia.ward'))
    pointer = tmp_path / 'selected.json'
    server = ServerSettings.from_env()

    async def facts():
        async with open_current_knowledge_base(source, pointer, embedder=FakeEmbedder()) as kb:
            assert kb is not None
            found = await kb.search_corpus('payroll')
            account = kb.lookup_account('amelia.ward')['account']
            assert isinstance(account, dict)
            return account['department'], found.chunks[0].chunk.text

    asyncio.run(select_version(version.marker, pointer, server))
    original_facts = asyncio.run(facts())
    assert original_facts[0] == 'IT' and 'thomas.price' in original_facts[1]
    settings = Settings.from_env({'LI_DATASET_DIR': str(source),
        'LI_KNOWLEDGE_BASE_STATE': str(pointer), 'LI_MEMORY_PATH': str(tmp_path / 'memory.sqlite')})
    replacement = None
    try:
        app = create_app(settings)
        with TestClient(app) as client:
            original_dataset = client.get('/api/overview').json()
            case = client.post('/api/investigations', json={'question': 'Who owns amelia.ward?'}).json()
            path = f"/api/investigations/{case['id']}"
            answer = client.post(path + '/ask', json={'question': case['first_question']})
            assert 'event: error' not in answer.text
            assert client.post(path + '/report', json={'request': 'Write the incident report'}).status_code == 200
            saved = client.get(path).json()
            original_pdf = client.get(path + '/reports/1.pdf')
            assert original_pdf.status_code == 200 and original_pdf.content.startswith(b'%PDF')
            config = {'configurable': {'thread_id': case['id']}}
            checkpoint = app.state.services.memory.get_tuple(config)
            artifact = next(m.artifact for m in checkpoint.checkpoint['channel_values']['messages']
                            if isinstance(m, ToolMessage))
            before = pointer.read_bytes()

            class FailedEmbeddings(FakeEmbedder):
                def embed_documents(self, texts):
                    raise RuntimeError('Injected build failure')

            with pytest.raises(RuntimeError, match='Injected build failure'):
                asyncio.run(build_version(source, tmp_path / 'failed', server, FailedEmbeddings()))
            assert pointer.read_bytes() == before
            assert list((tmp_path / 'failed').iterdir()) == []
            replacement = asyncio.run(build_version(source, tmp_path / 'versions', server,
                                                     FakeEmbedder(), offline_embeddings=True))
            from pathlib import Path
            replace_file = Path.replace

            def failed_publication(self, target):
                if Path(target) == pointer:
                    raise OSError('Injected publication failure')
                return replace_file(self, target)

            with monkeypatch.context() as fault:
                fault.setattr(Path, 'replace', failed_publication)
                with pytest.raises(KnowledgeBaseNotReady):
                    asyncio.run(select_version(replacement.marker, pointer, server))
            assert pointer.read_bytes() == before
            asyncio.run(select_version(replacement.marker, pointer, server))
            assert client.get('/api/overview').json() == original_dataset
            assert app.state.knowledge_base.lookup_account('amelia.ward')['account']['department'] == 'IT'
        updated = asyncio.run(facts())
        assert updated[0] == 'Operations' and 'amelia.ward' in updated[1]
        restarted = create_app(settings)
        with TestClient(restarted) as client:
            assert client.get('/api/overview').json() != original_dataset
            assert client.get(path).json() == saved
            restored_pdf = client.get(path + '/reports/1.pdf')
            assert restored_pdf.status_code == 200 and restored_pdf.content.startswith(b'%PDF')
            checkpoint = restarted.state.services.memory.get_tuple(config)
            assert next(m.artifact for m in checkpoint.checkpoint['channel_values']['messages']
                        if isinstance(m, ToolMessage)) == artifact
        asyncio.run(rollback_version(pointer, server))
        assert asyncio.run(facts()) == original_facts
        with TestClient(create_app(settings)) as client:
            assert client.get('/api/overview').json() == original_dataset
        assert document.read_text().endswith('Access to payroll needs approval from amelia.ward.\n')
        assert version.marker.exists() and replacement.marker.exists()
    finally:
        if replacement is not None:
            remove_version(replacement, server)


@pytest.mark.parametrize('damage', ['missing_marker', 'changed_snapshot', 'mixed_database', 'bad_format',
                                  'postgres_unavailable', 'graph_unavailable'])
def test_invalid_pair_refuses_before_application_services(version, tmp_path, damage, monkeypatch):
    from dotenv import dotenv_values

    from login_investigator.knowledge_base import KnowledgeBaseNotReady
    from login_investigator.knowledge_base.graph_service import GraphService, docker
    from login_investigator.knowledge_base.neo4j_graph import GraphSettings
    from login_investigator.knowledge_base.staleness import PAIR_UNCHECKABLE

    marker_bytes = version.marker.read_bytes()
    log = version.snapshot / 'logins.csv'
    log_bytes = log.read_bytes()
    pointer = tmp_path / 'selected.json'
    pointer.write_text(json.dumps({'format': 'paired-v1', 'current': str(version.marker), 'previous': None}))
    memory = tmp_path / 'memory.sqlite'
    try:
        if damage == 'missing_marker':
            version.marker.unlink()
        elif damage == 'changed_snapshot':
            log.chmod(0o600)
            log.write_bytes(log_bytes + b'\nchanged\n')
        elif damage == 'mixed_database':
            value = json.loads(marker_bytes)
            value['database'] = 'li_kb_000000000000'
            version.marker.write_text(json.dumps(value))
        elif damage == 'bad_format':
            pointer.write_text('{"format":"unknown"}')
        elif damage == 'postgres_unavailable':
            monkeypatch.setenv('LI_PG_PORT', '1')
        elif damage == 'graph_unavailable':
            docker('stop', version.container)
        settings = Settings.from_env({'LI_KNOWLEDGE_BASE_STATE': str(pointer),
                                      'LI_MEMORY_PATH': str(memory)})
        with pytest.raises(KnowledgeBaseNotReady, match='selected source') as caught:
            with TestClient(create_app(settings)):
                pytest.fail('Invalid pair started the application')
        assert str(caught.value) == PAIR_UNCHECKABLE
        assert caught.value.__suppress_context__
        assert not memory.exists()
    finally:
        version.marker.write_bytes(marker_bytes)
        if damage == 'changed_snapshot':
            log.write_bytes(log_bytes)
            log.chmod(0o400)
        if damage == 'graph_unavailable':
            docker('start', version.container)
            service = GraphService(version.container, version.marker.parent)
            values = dotenv_values(version.marker.parent / '.env')
            service.wait(GraphSettings(service.uri(), values['LI_GRAPH_USER'] or '',
                                       values['LI_GRAPH_PASSWORD'] or ''))


def test_cancelled_startup_waits_for_graph_worker_before_cleanup(version, monkeypatch):
    import threading

    from neo4j import Session

    from login_investigator.knowledge_base.graph_version import open_version

    reached, release = threading.Event(), threading.Event()
    original = Session.run

    def delayed(self, query, *args, **kwargs):
        if 'WHERE NOT n:Build' in str(query.text):
            reached.set()
            assert release.wait(15), 'Test did not release the query'
        return original(self, query, *args, **kwargs)

    monkeypatch.setattr(Session, 'run', delayed)

    async def opening():
        async with open_version(version.marker, ServerSettings.from_env()):
            pytest.fail('Cancelled startup reached the caller')

    async def check():
        task = asyncio.create_task(opening())
        try:
            assert await asyncio.to_thread(reached.wait, 15)
            task.cancel()
            await asyncio.sleep(0.05)
            assert not task.done(), 'Cancellation abandoned an active graph query'
        finally:
            release.set()
        with pytest.raises(asyncio.CancelledError):
            await task

    asyncio.run(check())


def test_concurrent_investigations_keep_their_own_account_evidence(version, tmp_path, monkeypatch):
    from concurrent.futures import ThreadPoolExecutor

    from langchain_core.messages import AIMessage, ToolMessage
    from langchain_core.outputs import ChatGeneration, ChatResult

    from login_investigator import agent
    from tests.test_agent import FakeModel, tool_call

    class AccountModel(FakeModel):
        def _generate(self, messages, stop=None, run_manager=None, **kwargs):
            last = messages[-1]
            if isinstance(last, ToolMessage):
                reply = AIMessage('The account evidence is recorded.')
            else:
                account = 'amelia.ward' if 'amelia.ward' in last.text else 'thomas.price'
                reply = tool_call('lookup_account', {'account_id': account})
            return ChatResult(generations=[ChatGeneration(message=reply)])

    monkeypatch.setattr(agent, 'make_model', lambda: AccountModel(responses=[]))
    pointer = tmp_path / 'selected.json'
    pointer.write_text(json.dumps({'format': 'paired-v1', 'current': str(version.marker), 'previous': None}))
    settings = Settings.from_env({'LI_KNOWLEDGE_BASE_STATE': str(pointer),
                                  'LI_MEMORY_PATH': str(tmp_path / 'memory.sqlite')})
    app = create_app(settings)
    with TestClient(app) as client:
        def investigate(account):
            question = f'Who owns {account}?'
            case = client.post('/api/investigations', json={'question': question}).json()
            response = client.post(f"/api/investigations/{case['id']}/ask", json={'question': question})
            assert response.status_code == 200 and 'event: error' not in response.text
            config = {'configurable': {'thread_id': case['id']}}
            saved = app.state.services.memory.get_tuple(config)
            artifacts = [m.artifact for m in saved.checkpoint['channel_values']['messages']
                         if isinstance(m, ToolMessage)]
            assert len(artifacts) == 1
            return artifacts[0]['account']['username']

        with ThreadPoolExecutor(max_workers=2) as executor:
            assert list(executor.map(investigate, ['amelia.ward', 'thomas.price'])) == ['amelia.ward', 'thomas.price']


def test_paired_reader_bounds_postgresql_statements(version):
    from sqlalchemy import text
    from sqlalchemy.exc import DBAPIError

    from login_investigator.knowledge_base.graph_version import open_version

    async def check():
        async with open_version(version.marker, ServerSettings.from_env()) as kb:
            async with kb.engine.connect() as connection:
                milliseconds = await connection.scalar(text(
                    "SELECT setting::integer FROM pg_settings WHERE name='statement_timeout'"))
                assert 0 < milliseconds <= 10000
                with pytest.raises(DBAPIError, match='statement timeout'):
                    await asyncio.wait_for(connection.execute(text('SELECT pg_sleep(20)')), timeout=12)

    asyncio.run(check())


def test_partial_app_startup_closes_graph_drivers_and_reader_pool(version, tmp_path, monkeypatch):
    from neo4j import GraphDatabase
    from neo4j.exceptions import DriverError

    from login_investigator import agent

    drivers = []
    original = GraphDatabase.driver

    def tracked(*args, **kwargs):
        driver = original(*args, **kwargs)
        drivers.append(driver)
        return driver

    def broken_model():
        raise ValueError('Injected failure after knowledge-base preparation')

    monkeypatch.setattr(GraphDatabase, 'driver', tracked)
    monkeypatch.setattr(agent, 'make_model', broken_model)
    pointer = tmp_path / 'selected.json'
    pointer.write_text(json.dumps({'format': 'paired-v1', 'current': str(version.marker), 'previous': None}))
    settings = Settings.from_env({'LI_KNOWLEDGE_BASE_STATE': str(pointer),
                                  'LI_MEMORY_PATH': str(tmp_path / 'memory.sqlite')})
    with pytest.raises(ValueError, match='Injected failure'):
        with TestClient(create_app(settings)):
            pytest.fail('Partial startup accepted requests')
    assert drivers
    for driver in drivers:
        with pytest.raises(DriverError):
            driver.verify_connectivity()
    assert_reader_disconnected(version)


def test_shutdown_failure_still_disposes_the_postgresql_pool(version, monkeypatch):
    from neo4j import Driver

    from login_investigator.knowledge_base.graph_version import open_version
    from login_investigator.knowledge_base.neo4j_graph import Neo4jQueries

    persistent = None
    original = Driver.close

    def failing_close(self):
        original(self)
        if self is persistent:
            raise RuntimeError('Injected graph shutdown failure')

    monkeypatch.setattr(Driver, 'close', failing_close)

    async def check():
        nonlocal persistent
        opened = None
        try:
            with pytest.raises(RuntimeError, match='Injected graph shutdown failure'):
                async with open_version(version.marker, ServerSettings.from_env()) as kb:
                    opened = kb
                    graph = kb.graph_queries
                    assert isinstance(graph, Neo4jQueries)
                    persistent = graph.driver
            assert_reader_disconnected(version)
        finally:
            if opened is not None:
                await opened.engine.dispose()

    asyncio.run(check())


def test_cancelled_shutdown_joins_graph_close_and_disposes_postgresql(version, monkeypatch):
    import threading

    from neo4j import Driver

    from login_investigator.knowledge_base.graph_version import open_version
    from login_investigator.knowledge_base.neo4j_graph import Neo4jQueries

    reached, release = threading.Event(), threading.Event()
    persistent = None
    original = Driver.close

    def delayed(self):
        if self is persistent:
            reached.set()
            assert release.wait(15), 'Test did not release graph shutdown'
        original(self)

    monkeypatch.setattr(Driver, 'close', delayed)

    async def closing():
        nonlocal persistent
        async with open_version(version.marker, ServerSettings.from_env()) as kb:
            graph = kb.graph_queries
            assert isinstance(graph, Neo4jQueries)
            persistent = graph.driver

    async def check():
        task = asyncio.create_task(closing())
        try:
            assert await asyncio.to_thread(reached.wait, 30)
            task.cancel()
            await asyncio.sleep(0.05)
            assert not task.done()
        finally:
            release.set()
        with pytest.raises(asyncio.CancelledError):
            await task
        assert_reader_disconnected(version)

    asyncio.run(check())


def test_offline_pair_cannot_become_live_evaluation_evidence(version, tmp_path):
    from login_investigator.knowledge_base import KnowledgeBaseNotReady
    from login_investigator.knowledge_base.evaluation_version import isolated_evaluation

    pointer = tmp_path / 'selected.json'
    pointer.write_text(json.dumps({'format': 'paired-v1', 'current': str(version.marker), 'previous': None}))
    before = pointer.read_bytes()

    async def check():
        with pytest.raises(KnowledgeBaseNotReady, match='Offline graph versions'):
            async with isolated_evaluation(DATASET, pointer, root=tmp_path / 'evaluations'):
                pytest.fail('Offline embeddings were accepted for live evaluation')

    asyncio.run(check())
    assert pointer.read_bytes() == before
    assert not (tmp_path / 'evaluations').exists()
