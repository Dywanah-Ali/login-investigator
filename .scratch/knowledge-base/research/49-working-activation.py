"""T49 one-time accepted operator check and activation. No provider calls."""
import argparse
import asyncio
import hashlib
import json
import os
from pathlib import Path
import signal
import socket
import subprocess
import sys
import time
from urllib.error import URLError
from urllib.request import urlopen

BACKEND = Path.cwd()
# Running a research file makes its directory sys.path[0]; mirror the backend server cwd.
sys.path.insert(0, str(BACKEND))
PRIVATE = BACKEND / '.graph-versions/t49'
PUBLIC = BACKEND.parent / '.scratch/knowledge-base/research'
POINTER = BACKEND / '.knowledge-base.json'
ORIGINAL_HASH = '09412e45a833a4a780144c7342506e3f480527b8855b410e88ac9889c4c2d993'
CANDIDATE = '3d58516ccfe84f74ade0ee255607fe19'
ROLLBACK = 'eb6c7d59d40d4a94b87633593ae8649f'


def get(path):
    with urlopen('http://127.0.0.1:8000/api/' + path, timeout=5) as response:
        return json.load(response)


def start(command, name):
    with socket.socket() as probe:
        probe.bind(('127.0.0.1', 8000))
    log = (PRIVATE / (name + '.log')).open('wb')
    started = time.monotonic()
    process = subprocess.Popen(['bash', '-c', command], cwd=BACKEND, stdout=log,
                               stderr=log, start_new_session=True)
    try:
        while time.monotonic() - started < 300:
            if process.poll() is not None:
                raise RuntimeError('Server exited; inspect private log')
            try:
                overview = get('overview')
                listing = get('investigations')
                cases = {case['id']: get('investigations/' + case['id'])
                         for case in listing['investigations']}
                return process, round(time.monotonic() - started, 3), overview, cases
            except (URLError, TimeoutError, ConnectionError):
                time.sleep(.2)
        raise RuntimeError('Operator readiness exceeded measurement-only 300-second ceiling')
    except BaseException:
        stop(process)
        raise
    finally:
        log.close()


def stop(process):
    if process.poll() is None:
        os.killpg(process.pid, signal.SIGTERM)
        try:
            process.wait(timeout=30)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait(timeout=10)


async def validate_retained(prepared):
    from login_investigator.knowledge_base.graph_version import open_version
    from login_investigator.postgres import ServerSettings
    for key, build_id in (('current', CANDIDATE), ('previous', ROLLBACK)):
        expected = BACKEND / '.graph-versions' / build_id / 'complete.json'
        assert Path(prepared[key]).resolve() == expected.resolve()
        async with open_version(expected, ServerSettings.from_env()) as kb:
            assert kb.build_id == build_id
            assert kb.source_snapshot == expected.parent / 'source'


async def readers():
    from langchain_core.embeddings import Embeddings
    from sqlalchemy import select
    from login_investigator.knowledge_base import open_current_knowledge_base, schema
    from login_investigator.knowledge_base.graph_version import open_version
    from login_investigator.loader import load_log
    from login_investigator.rules import detect_all
    from login_investigator.postgres import ServerSettings
    class StoredQuery(Embeddings):
        def embed_documents(self, texts):
            raise AssertionError('No provider call authorised')
        def embed_query(self, text):
            assert text == query
            return vector
    async with open_current_knowledge_base(BACKEND / 'data/datasets/default', POINTER) as kb:
        assert kb.build_id == CANDIDATE
        assert kb.lookup_account('amelia.ward')['account']['person_id'] == 'user-amelia.ward'
        finding = next(f for f in detect_all(load_log(kb.source_snapshot / 'logins.csv'))
                       if f.finding_id == 'F-password-spraying-d06a7545')
        assert kb.finding_radius(finding).accounts[0].account['person_id'] == 'user-amelia.ward'
        async with kb.engine.connect() as connection:
            row = (await connection.execute(select(schema.chunks).order_by(schema.chunks.c.chunk_id).limit(1))).mappings().one()
            query, vector, expected = row['content'], [float(v) for v in row['embedding']], row['chunk_id']
        snapshot = kb.source_snapshot
    async with open_version(BACKEND / '.graph-versions' / CANDIDATE / 'complete.json',
                            ServerSettings.from_env(), embedder=StoredQuery()) as kb:
        hits = await kb.search_corpus(query)
        assert expected in [hit.chunk.id for hit in hits.chunks]
    return {'build_id': CANDIDATE, 'snapshot': str(snapshot.relative_to(BACKEND)),
            'lookup': True, 's6_radius': True, 'document_self_retrieval': True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('operation', choices=['recovery', 'activate'])
    args = parser.parse_args()
    assert hashlib.sha256(POINTER.read_bytes()).hexdigest() == ORIGINAL_HASH
    if args.operation == 'recovery':
        link = PRIVATE / 'legacy-recovery/code/backend/.env'
        if not link.exists():
            link.symlink_to(BACKEND / '.env')
        command = '''LI_RECOVERY_ROOT="$PWD/.graph-versions/t49/legacy-recovery"
LI_DATASET_DIR="$LI_RECOVERY_ROOT/source" LI_KNOWLEDGE_BASE_STATE="$LI_RECOVERY_ROOT/selection.json" LI_MEMORY_PATH="$PWD/memory/investigations.sqlite" uv run --directory "$LI_RECOVERY_ROOT/code/backend" --frozen uvicorn api.app:create_app --factory --port 8000'''
        process, elapsed, overview, cases = start(command, 'manual-recovery')
        try:
            (PRIVATE / 'working-before.json').write_text(json.dumps({'overview': overview, 'cases': cases}))
            report = {'command': 'admin manual section 5 pre-migration recovery, as written',
                      'readiness_seconds': elapsed, 'saved_investigations_reopened': len(cases),
                      'working_pointer_unchanged': POINTER.read_bytes() == (PRIVATE / 'legacy-recovery/selection.json').read_bytes(),
                      'provider_calls': 0}
            (PUBLIC / '49-manual-recovery.json').write_text(json.dumps(report, indent=2) + '\n')
            print(json.dumps(report), flush=True)
        finally:
            stop(process)
        return
    from api.settings import Settings
    from login_investigator.investigations import MEMORY_PATH
    configured = Settings.from_env()
    assert configured.knowledge_base_state.resolve() == POINTER.resolve()
    assert configured.memory_path.resolve() == MEMORY_PATH.resolve()
    original = POINTER.read_bytes()
    prepared = json.loads((PRIVATE / 'selected.json').read_text())
    asyncio.run(validate_retained(prepared))
    assert hashlib.sha256(POINTER.read_bytes()).hexdigest() == ORIGINAL_HASH
    # The accepted one-time format transition cannot use select_version on a legacy pointer.
    temporary = POINTER.with_suffix('.t49-tmp')
    temporary.write_text(json.dumps(prepared) + '\n')
    temporary.replace(POINTER)
    process = None
    try:
        checks = asyncio.run(readers())
        process, elapsed, overview, cases = start('uv run uvicorn api.app:create_app --factory --port 8000', 'working-server')
        before = json.loads((PRIVATE / 'working-before.json').read_text())
        assert overview == before['overview']
        assert cases == before['cases']
        report = {'current': CANDIDATE, 'previous': ROLLBACK,
                  'readiness_seconds': elapsed, 'saved_investigations_reopened': len(cases),
                  'saved_evidence_identical': True, 'overview_identical': True,
                  'default_server_selection_and_memory_verified': True,
                  'readers': checks, 'provider_calls': 0, 'server_pid': process.pid,
                  'port': 8000, 'legacy_recovery_retained': True}
        (PUBLIC / '49-working-activation.json').write_text(json.dumps(report, indent=2) + '\n')
        (PRIVATE / 'working-server.pid').write_text(str(process.pid))
        print(json.dumps(report), flush=True)
    except BaseException:
        try:
            if process is not None:
                stop(process)
        finally:
            temporary.write_bytes(original)
            temporary.replace(POINTER)
            print('Activation failed. Original pointer restored. '
                  'The current code refuses legacy pointers. Run the archived recovery command '
                  'in admin manual section 5 to restore service after confirming this server stopped.', file=sys.stderr, flush=True)
        raise


if __name__ == '__main__':
    main()
