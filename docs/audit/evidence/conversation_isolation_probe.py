"""Offline probe: real routes/agent/checkpointer, fake model, temporary database."""
import json
import os
import socket
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from unittest.mock import patch

# Reuse the project's existing offline model fixture. No live model is constructed.
_repo = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_repo / "backend"))
sys.path.insert(0, str(_repo / "backend" / "tests"))

from fastapi.testclient import TestClient
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda
from api.app import create_app
from api.settings import Settings
from login_investigator import agent
from test_agent import FakeModel, REPORT

for key in ('OPENROUTER_API_KEY', 'ABUSEIPDB_API_KEY'):
    os.environ.pop(key, None)

captures = []
reports = []
markers = ('ISOLATION_ALPHA_713', 'ISOLATION_BRAVO_829', 'ISOLATION_CHARLIE_941')

class RecordingModel(FakeModel):
    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        captures.append('\n'.join(m.text for m in messages))
        return super()._generate(messages, stop, run_manager, **kwargs)

    def with_structured_output(self, schema, **kwargs):
        def record(prompt):
            text = prompt.to_string()
            reports.append(text)
            own = [marker for marker in markers if marker in text]
            assert len(own) == 1, 'Report received another conversation marker'
            return REPORT.model_copy(update={'title': own[0] + ' report'})
        return RunnableLambda(record)

def no_network(*args, **kwargs):
    raise AssertionError('Unexpected outbound network connection')

def model_factory():
    return RecordingModel(responses=[AIMessage('Offline probe acknowledgement.')])

def assert_scope(text, own):
    assert markers[own] in text, 'Own conversation history missing'
    for i, marker in enumerate(markers):
        if i != own:
            assert marker not in text, 'Other conversation history reached boundary'

def ask(client, case, text, own):
    before = len(captures)
    response = client.post(f'/api/investigations/{case}/ask', json={'question': text})
    assert response.status_code == 200 and 'event: done' in response.text
    assert len(captures) == before + 1
    assert_scope(captures[-1], own)
    saved = client.get(f'/api/investigations/{case}')
    assert saved.status_code == 200
    assert_scope(json.dumps(saved.json()), own)

with TemporaryDirectory(prefix='li-isolation-') as directory:
    settings = Settings.from_env({'LI_MEMORY_PATH': str(Path(directory) / 'probe.sqlite')})
    with patch.object(agent, 'make_model', model_factory), patch.object(agent, 'load_dotenv', lambda *a, **kw: False), patch.object(socket.socket, 'connect', no_network):
        with TestClient(create_app(settings)) as client:
            ids = []
            for marker in markers:
                response = client.post('/api/investigations', json={'question': marker})
                assert response.status_code == 201
                ids.append(response.json()['id'])
            assert len(set(ids)) == 3
            ask(client, ids[0], 'Remember case label ' + markers[0], 0)
            ask(client, ids[1], 'Remember case label ' + markers[1], 1)
            for own in (0, 1):
                response = client.post(f'/api/investigations/{ids[own]}/report', json={'request': 'Write the incident report'})
                assert response.status_code == 200
                assert_scope(reports[-1], own)
            ask(client, ids[0], 'Which case label were we discussing?', 0)
            assert markers[0] + ' report' in captures[-1]
            ask(client, ids[1], 'Which case label were we discussing?', 1)
            assert markers[1] + ' report' in captures[-1]
            ask(client, ids[2], 'Remember case label ' + markers[2], 2)
        with TestClient(create_app(settings)) as reopened:
            ask(reopened, ids[0], 'Which case label were we discussing after reopening?', 0)
            ask(reopened, ids[1], 'Which case label were we discussing after reopening?', 1)

print(json.dumps({'result': 'PASS', 'temporary_cases': 3, 'model_input_captures': len(captures), 'report_input_captures': len(reports), 'cross_case_marker_leaks': 0, 'restart_checked': True, 'outbound_network_blocked': True, 'live_database_modified': False}))
