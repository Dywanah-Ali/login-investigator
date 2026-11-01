"""Disposable T49 measurement harness. Never selects the working application pointer."""
import asyncio
import json
import os
from pathlib import Path
import signal
import socket
import sqlite3
import subprocess
import time
import tarfile
from urllib.request import urlopen
from urllib.error import URLError

from dotenv import dotenv_values
from login_investigator.knowledge_base.graph_service import GraphService, docker
from login_investigator.knowledge_base.neo4j_graph import GraphSettings

backend = Path.cwd()
state = backend / '.graph-versions/t49/rehearsal.json'
prepared, replacement = json.loads((backend.parent / '.scratch/knowledge-base/research/49-preparation.json').read_text())['versions']
for version in (prepared, replacement):
    version['marker'] = str(backend / version['marker'])
state.write_text(json.dumps({'format': 'paired-v1', 'current': prepared['marker'], 'previous': None}))
working = backend / '.knowledge-base.json'
working_before = working.read_bytes()
with socket.socket() as probe:
    probe.bind(('127.0.0.1', 8012))
environ = dict(os.environ, LI_KNOWLEDGE_BASE_STATE='.graph-versions/t49/rehearsal.json',
               LI_MEMORY_PATH='.graph-versions/t49/rehearsal-memory.sqlite')
process = None
log_path = backend / '.graph-versions/t49-server.log'
log = log_path.open('wb')
measurements = {'offline_embeddings': False, 'readiness': 'GET /api/overview and GET /api/investigations',
                'provider_calls': 0, 'measurement_ceiling_seconds': 300, 'build_ids': [prepared['build_id'], replacement['build_id']]}



def seed_saved_evidence():
    from fastapi.testclient import TestClient
    from langchain_core.messages import AIMessage, ToolMessage
    from api.app import create_app
    from api.settings import Settings
    from login_investigator import agent, investigations
    from tests.test_agent import FakeModel, tool_call
    memory = Path(environ['LI_MEMORY_PATH'])
    if investigations.MEMORY_PATH.exists():
        with sqlite3.connect(f'file:{investigations.MEMORY_PATH}?mode=ro', uri=True) as source:
            with sqlite3.connect(memory) as destination:
                source.backup(destination)
    original = agent.make_model
    agent.make_model = lambda: FakeModel(responses=[tool_call('lookup_account', {'account_id': 'amelia.ward'}),
                                                   AIMessage('The saved account evidence names Amelia Ward.')])
    try:
        app = create_app(Settings.from_env(environ))
        with TestClient(app) as client:
            case = client.post('/api/investigations', json={'question': 'Who owns amelia.ward?'}).json()
            result = client.post(f"/api/investigations/{case['id']}/ask", json={'question': 'Who owns amelia.ward?'})
            assert result.status_code == 200 and 'event: error' not in result.text
            saved = app.state.services.memory.get_tuple({'configurable': {'thread_id': case['id']}})
            artifacts = [m.artifact for m in saved.checkpoint['channel_values']['messages'] if isinstance(m, ToolMessage)]
            assert artifacts[0]['account']['person_id'] == 'user-amelia.ward'
            return case['id'], client.get(f"/api/investigations/{case['id']}").json()
    finally:
        agent.make_model = original


async def verify_readers(marker):
    from sqlalchemy import select
    from langchain_core.embeddings import Embeddings
    from login_investigator.knowledge_base import schema
    from login_investigator.knowledge_base.graph_version import open_version
    from login_investigator.postgres import ServerSettings
    from login_investigator.loader import load_log
    from login_investigator.rules import detect_all
    class ExactStoredQuery(Embeddings):
        def embed_documents(self, texts):
            raise AssertionError('No new document embeddings')
        def embed_query(self, text):
            assert text == query
            return vector
    async with open_version(Path(marker), ServerSettings.from_env()) as kb:
        assert kb.lookup_account('amelia.ward')['account']['department'] == 'IT'
        finding = next(f for f in detect_all(load_log(kb.source_snapshot / 'logins.csv'))
                       if f.finding_id == 'F-password-spraying-d06a7545')
        assert kb.finding_radius(finding).accounts[0].account['person_id'] == 'user-amelia.ward'
        async with kb.engine.connect() as connection:
            row = (await connection.execute(select(schema.chunks).order_by(schema.chunks.c.chunk_id).limit(1))).mappings().one()
            query, vector, expected = row['content'], [float(v) for v in row['embedding']], row['chunk_id']
    async with open_version(Path(marker), ServerSettings.from_env(), embedder=ExactStoredQuery()) as kb:
        result = await kb.search_corpus(query)
        assert expected in [hit.chunk.id for hit in result.chunks]
        return {'build_id': kb.build_id, 'source_fingerprint': json.loads(Path(marker).read_text())['fingerprint'],
                'lookup': True, 's6_radius': True, 'document_self_retrieval': True}


case_id, expected_case = seed_saved_evidence()


def start(expect_failure=False, legacy=False):
    global process
    tick = time.monotonic()
    print('Starting archived baseline' if legacy else 'Starting paired application', flush=True)
    settings = dict(environ)
    cwd = backend
    if legacy:
        cwd = backend / '.graph-versions/t49/legacy-recovery/code/backend'
        settings = {**{k: v for k, v in dotenv_values(backend / '.env').items() if v is not None}, **settings}
        settings.update(LI_DATASET_DIR=str(backend / '.graph-versions/t49/legacy-recovery/source'),
                        LI_KNOWLEDGE_BASE_STATE=str(backend / '.graph-versions/t49/legacy-recovery/selection.json'),
                        LI_MEMORY_PATH=str(backend / environ['LI_MEMORY_PATH']), PYTHONPATH=str(cwd))
    process = subprocess.Popen(['uv', 'run', '--frozen', 'uvicorn', 'api.app:create_app', '--factory', '--port', '8012'],
                               cwd=cwd, env=settings, stdout=log, stderr=log, start_new_session=True)
    deadline = tick + 300
    while time.monotonic() < deadline:
        if process.poll() is not None:
            if expect_failure and process.returncode != 0:
                return round(time.monotonic() - tick, 3)
            raise RuntimeError('Demonstration server did not start; inspect the private server log')
        try:
            with urlopen('http://127.0.0.1:8012/api/overview', timeout=.5) as response:
                ready = response.status == 200
            with urlopen('http://127.0.0.1:8012/api/investigations', timeout=.5) as response:
                ready = ready and response.status == 200
            if ready:
                with urlopen(f'http://127.0.0.1:8012/api/investigations/{case_id}', timeout=5) as response:
                    assert json.load(response) == expected_case
                if expect_failure:
                    raise RuntimeError('Unavailable graph was accepted at startup')
                print('Ready in', round(time.monotonic() - tick, 3), 'seconds; saved evidence matches', flush=True)
                return round(time.monotonic() - tick, 3)
        except (URLError, TimeoutError, ConnectionError):
            pass
        time.sleep(.1)
    raise RuntimeError('Demonstration server exceeded readiness deadline')


def stop():
    global process
    if process is not None and process.poll() is None:
        os.killpg(process.pid, signal.SIGTERM)
        try:
            process.wait(timeout=20)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait()
            raise RuntimeError('Demonstration server required forced shutdown')
    process = None


def selection(*action):
    result = subprocess.run(['uv', 'run', 'python', '-m', 'scripts.select_graph_version',
                             '--state-file', '.graph-versions/t49/rehearsal.json', *action],
                            capture_output=True, text=True, timeout=120)
    if result.returncode:
        raise RuntimeError('Selection command failed; no working application change was made')


try:
    archived = backend / '.graph-versions/t49/legacy-recovery/code'
    archived.mkdir(exist_ok=True)
    with tarfile.open(archived.parent / 'code.tar') as archive:
        archive.extractall(archived, filter='data')
    subprocess.run(['uv', 'sync', '--frozen'], cwd=archived / 'backend', stdout=log, stderr=log, check=True)
    measurements['legacy_recovery_ready_seconds'] = start(legacy=True)
    tick = time.monotonic()
    stop()
    start()
    measurements['legacy_to_pair_interruption_seconds'] = round(time.monotonic() - tick, 3)
    stop()
    measurements['initial_ready_seconds'] = start()
    measurements['rollback_readers'] = asyncio.run(verify_readers(prepared['marker']))
    selection('--version', replacement['marker'])
    tick = time.monotonic()
    stop()
    start()
    measurements['update_interruption_seconds'] = round(time.monotonic() - tick, 3)
    measurements['candidate_readers'] = asyncio.run(verify_readers(replacement['marker']))
    selection('--rollback')
    tick = time.monotonic()
    stop()
    start()
    measurements['rollback_interruption_seconds'] = round(time.monotonic() - tick, 3)
    stop()
    docker('stop', prepared['container'])
    measurements['unavailable_graph_startup_refused_seconds'] = start(expect_failure=True)
    stop()
    tick = time.monotonic()
    docker('start', prepared['container'])
    directory = backend / '.graph-versions' / prepared['build_id']
    service = GraphService(prepared['container'], directory)
    values = dotenv_values(directory / '.env')
    service.wait(GraphSettings(service.uri(), values.get('LI_GRAPH_USER') or '', values.get('LI_GRAPH_PASSWORD') or ''))
    start()
    measurements['graph_recovery_seconds'] = round(time.monotonic() - tick, 3)
    assert working.read_bytes() == working_before
    measurements['working_pointer_unchanged'] = True
    measurements['saved_evidence_reopened_after_each_restart'] = True
    measurements['memory_is_copy_with_scripted_model_probe'] = True
    target = backend.parent / '.scratch/knowledge-base/research/49-lifecycle-measurements.json'
    target.write_text(json.dumps(measurements, indent=2) + '\n')
    print(json.dumps(measurements, indent=2))
finally:
    stop()
    log.close()
