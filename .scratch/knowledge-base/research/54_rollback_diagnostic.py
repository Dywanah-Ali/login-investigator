"""Diagnostic-only launcher for B-149. Does not alter app files or readiness/retry policy.

Run from the repository root:
    uv run --locked --directory backend python ../.scratch/knowledge-base/research/54_rollback_diagnostic.py

The existing test owns its temporary resources. This wrapper records exception context before
the test's cleanup, including contexts hidden by `raise ... from None`. It never prints driver
messages, credentials, query parameters, full settings objects or container environment.
"""

import json
import os
import re
import runpy
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from functools import wraps
from pathlib import Path
from urllib.parse import urlsplit

BACKEND = Path(__file__).resolve().parents[3] / 'backend'
REPORT = Path(__file__).with_name('54-rollback-diagnostic.jsonl')
sys.path.insert(0, str(BACKEND))
os.chdir(BACKEND)

from login_investigator.knowledge_base import graph_selection

original_select = graph_selection.select_version
call_number = 0
known_names = set()


def save(event, **fields):
    row = {'at': datetime.now(timezone.utc).isoformat(), 'event': event, **fields}
    with REPORT.open('a') as handle:
        handle.write(json.dumps(row) + '\n')
        handle.flush()
    print('B-149 diagnostic:', event, fields.get('call', ''), flush=True)


def remember(marker):
    path = Path(marker).resolve()
    if (path.is_relative_to(Path(tempfile.gettempdir()).resolve())
            and re.fullmatch('[0-9a-f]{32}', path.parent.name)):
        known_names.add('li-graph-' + path.parent.name)


def exception_chain(error):
    result = []
    seen = set()
    while error is not None and id(error) not in seen:
        seen.add(id(error))
        code = getattr(error, 'code', None)
        node = {'type': type(error).__name__, 'module': type(error).__module__,
                'code': code if isinstance(code, str) and re.fullmatch(r'Neo\.[A-Za-z0-9.]+', code) else None,
                'errno': error.errno if isinstance(error, OSError) else None, 'frames': []}
        if type(error).__module__.startswith('login_investigator.'):
            node['public_message'] = str(error)  # These core errors are explicitly credential-safe.
        trace = error.__traceback__
        while trace is not None:
            frame = trace.tb_frame
            entry = {'module': frame.f_globals.get('__name__'),
                     'function': frame.f_code.co_name, 'line': trace.tb_lineno}
            settings = frame.f_locals.get('settings')
            if type(settings).__name__ == 'GraphSettings':
                parsed = urlsplit(settings.uri)
                if parsed.hostname in ('127.0.0.1', 'localhost'):
                    entry['local_bolt_port'] = parsed.port
            node['frames'].append(entry)
            trace = trace.tb_next
        result.append(node)
        error = error.__cause__ or error.__context__
    return result


def container_state():
    states = []
    for name in sorted(known_names):
        try:
            process = subprocess.run(['docker', 'inspect', name, '--format', '{{json .State}}'],
                                     capture_output=True, text=True, timeout=10)
            if process.returncode:
                states.append({'name': name, 'inspect_exit': process.returncode})
                continue
            raw = json.loads(process.stdout)
            state = {'name': name, **{key: raw.get(key) for key in (
                'Status', 'Running', 'OOMKilled', 'ExitCode', 'StartedAt', 'FinishedAt')}}
            logs = subprocess.run(['docker', 'logs', '--tail', '60', name],
                                  capture_output=True, text=True, timeout=10)
            state['startup_markers'] = [line for line in (logs.stdout + logs.stderr).splitlines()
                                        if ' INFO ' in line and any(marker in line for marker in (
                                            'Started.', 'Starting...', 'Bolt enabled', 'Remote interface available'))]
            states.append(state)
        except (OSError, subprocess.TimeoutExpired, ValueError) as error:
            states.append({'name': name, 'capture_error_type': type(error).__name__})
    return states


@wraps(original_select)
async def observed_select(marker, state_file, server=None, **kwargs):
    global call_number
    call_number += 1
    number = call_number
    remember(marker)
    started = time.monotonic()
    save('select_started', call=number, incoming=Path(marker).parent.name,
         fixed_address=kwargs.get('fixed_address') is not None)
    try:
        result = await original_select(marker, state_file, server, **kwargs)
    except Exception as error:
        chain = exception_chain(error)
        expected = (any(frame['function'] == 'failed_publication'
                        for node in chain for frame in node['frames'])
                    or any('held by another process' in node.get('public_message', '') for node in chain))
        save('select_failed', call=number, elapsed_s=time.monotonic() - started,
             expected_test_fault=expected, exceptions=chain,
             containers=[] if expected else container_state())
        raise
    save('select_finished', call=number, elapsed_s=time.monotonic() - started)
    return result


if __name__ == '__main__':
    graph_selection.select_version = observed_select
    save('diagnostic_started', policy='logging only; original waits, drivers and retries unchanged')
    sys.argv = ['pytest', '-q', '-x',
                'tests/test_browser_access.py::test_fixed_address_conflict_selection_and_rollback']
    runpy.run_module('pytest', run_name='__main__', alter_sys=True)
