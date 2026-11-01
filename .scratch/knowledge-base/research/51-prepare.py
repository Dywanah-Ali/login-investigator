"""T51 one-time preparation: build the paired version with the reworded answer key, no provider calls.

Reuses the checked passage vectors of the currently selected working version (the T50 pair), as T49
and T50 did, because the corpus is unchanged. Only truth.json changed, so the source fingerprint
differs. Unlike T50, the selected pair already has no address edges, so it opens through the normal
checked path. Parity is checked for every passage, graph count, account, finding radius and walk,
with no expected difference. The working selection is not changed here; selection and restart follow
the admin manual, section 5.

Run from backend/: uv run python ../.scratch/knowledge-base/research/51-prepare.py
"""
import asyncio
import csv
import json
import sys
import time
from dataclasses import asdict
from pathlib import Path

# Running a research file makes its directory sys.path[0]; mirror the backend server cwd.
sys.path.insert(0, str(Path.cwd()))

from sqlalchemy import select  # noqa: E402

from login_investigator.generator import DATASET_DIR  # noqa: E402
from login_investigator.knowledge_base import schema  # noqa: E402
from login_investigator.knowledge_base.evaluation_version import StoredEmbeddings  # noqa: E402
from login_investigator.knowledge_base.graph_version import build_version, open_version  # noqa: E402
from login_investigator.loader import load_log  # noqa: E402
from login_investigator.postgres import ServerSettings  # noqa: E402
from login_investigator.rules import detect_all  # noqa: E402

backend = Path.cwd()
working = backend / '.knowledge-base.json'
evidence = backend.parent / '.scratch/knowledge-base/research/51-preparation.json'
DATED = [('2026-10-07T11:03:00Z', '2026-10-07T11:11:00Z'), ('2026-10-07T11:07:00Z', '2026-10-07T11:11:00Z'),
         ('2026-09-01', '2026-11-01'), (None, '2026-09-01')]


async def passages(engine):
    async with engine.connect() as connection:
        rows = (await connection.execute(select(schema.chunks).order_by(schema.chunks.c.chunk_id))).mappings()
        return [{**dict(r), 'embedding': [float(v) for v in r['embedding']]} for r in rows]


def parity_snapshot(kb, findings, people):
    return {'lookups': {u: kb.lookup_account(u) for u in people},
            'radii': {f.finding_id: asdict(kb.finding_radius(f)) for f in findings},
            'walks': {f.finding_id: asdict(kb.finding_walk(f.finding_id)) for f in findings},
            'dated': {f'{f.finding_id}|{a}|{b}': asdict(kb.finding_radius(f, a, b))
                      for f in findings for a, b in DATED}}


async def main():
    server = ServerSettings.from_env()
    before = working.read_bytes()
    pointer = json.loads(before)
    assert pointer['format'] == 'paired-v1'
    current = Path(pointer['current'])
    old_snapshot = current.parent / 'source'
    tick = time.monotonic()
    log = load_log(old_snapshot / 'logins.csv')
    findings = detect_all(log)
    with open(old_snapshot / 'org' / 'people.csv', newline='', encoding='utf-8') as f:
        people = sorted(r['username'] for r in csv.DictReader(f))
    async with open_version(current, server) as old:
        rows = await passages(old.engine)
        old_counts = asdict(await old.check_graph_integrity())
        expected = parity_snapshot(old, findings, people)
    # The new source differs from the old snapshot only in truth.json.
    for path in sorted(p for p in old_snapshot.rglob('*') if p.is_file()):
        relative = path.relative_to(old_snapshot)
        same = path.read_bytes() == (DATASET_DIR / relative).read_bytes()
        assert same or relative.as_posix() == 'truth.json', relative
    vectors = {r['content']: r['embedding'] for r in rows}
    assert len(vectors) == len(rows)
    version = await build_version(DATASET_DIR, backend / '.graph-versions', server, StoredEmbeddings(vectors))
    async with open_version(version.marker, server) as kb:
        assert await passages(kb.engine) == rows
        new_counts = asdict(await kb.check_graph_integrity())
        assert new_counts == old_counts, (new_counts, old_counts)
        assert parity_snapshot(kb, findings, people) == expected
        gold = json.loads((kb.source_snapshot / 'truth.json').read_text())['scenarios']['S6']['blast_radius']
        assert 'used_address_filter' not in gold and 'shared address' not in gold['basis']
        spray = next(f for f in findings if '45.148.10.80' in f.ips and len(f.users) > 10)
        radius = kb.finding_radius(spray).accounts[0]
        assert [g['group_id'] for g in radius.groups] == gold['groups']
        assert [a['asset_id'] for a in radius.assets] == gold['assets']
        assert radius.access_paths == gold['paths']
        assert [p['person_id'] for p in radius.device_peers] == gold['device_peers']
    assert working.read_bytes() == before
    report = {'ticket': 'T51', 'previous_build': current.parent.name, 'build_id': version.build_id,
              'source_fingerprint': version.fingerprint, 'provider_calls': 0,
              'passages_compared': len(rows), 'accounts_compared': len(expected['lookups']),
              'findings_compared': len(expected['radii']), 'dated_radii_compared': len(expected['dated']),
              'graph_counts': new_counts, 'working_pointer_unchanged': True,
              'marker': version.marker.relative_to(backend).as_posix(),
              'preparation_and_parity_seconds': round(time.monotonic() - tick, 3)}
    evidence.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2), flush=True)


asyncio.run(main())
