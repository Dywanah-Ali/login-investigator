"""Disposable T48 measurement harness. Never selects the working application pointer."""
import asyncio
import json
import os
from pathlib import Path
import signal
import socket
import subprocess
import time
from urllib.request import urlopen
from urllib.error import URLError

from dotenv import dotenv_values
from login_investigator.knowledge_base.graph_service import GraphService, docker
from login_investigator.knowledge_base.neo4j_graph import GraphSettings

backend = Path.cwd()
state = backend / '.graph-versions/t48-selection.json'
prepared = json.loads((backend / '.graph-versions/t48-prepared.json').read_text())
replacement = json.loads((backend / '.graph-versions/t48-replacement.json').read_text())
working = backend / '.knowledge-base.json'
working_before = working.read_bytes()
with socket.socket() as probe:
    probe.bind(('127.0.0.1', 8012))
environ = dict(os.environ, LI_KNOWLEDGE_BASE_STATE='.graph-versions/t48-selection.json',
               LI_MEMORY_PATH='.graph-versions/t48-memory.sqlite')
process = None
log_path = backend / '.graph-versions/t48-server.log'
log = log_path.open('wb')
measurements = {'offline_embeddings': True, 'readiness': 'GET /api/overview and GET /api/investigations',
                'provider_calls': 0, 'build_ids': [prepared['build_id'], replacement['build_id']]}


def start(expect_failure=False):
    global process
    tick = time.monotonic()
    process = subprocess.Popen(['uv', 'run', 'uvicorn', 'api.app:create_app', '--factory', '--port', '8012'],
                               env=environ, stdout=log, stderr=log, start_new_session=True)
    deadline = tick + 120
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
                if expect_failure:
                    raise RuntimeError('Unavailable graph was accepted at startup')
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
                             '--state-file', '.graph-versions/t48-selection.json', *action],
                            capture_output=True, text=True, timeout=120)
    if result.returncode:
        raise RuntimeError('Selection command failed; no working application change was made')


try:
    measurements['initial_ready_seconds'] = start()
    selection('--version', '.graph-versions/' + replacement['version_file'])
    tick = time.monotonic()
    stop()
    start()
    measurements['update_interruption_seconds'] = round(time.monotonic() - tick, 3)
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
    target = backend.parent / '.scratch/knowledge-base/research/48-lifecycle-measurements.json'
    target.write_text(json.dumps(measurements, indent=2) + '\n')
    print(json.dumps(measurements, indent=2))
finally:
    stop()
    log.close()
