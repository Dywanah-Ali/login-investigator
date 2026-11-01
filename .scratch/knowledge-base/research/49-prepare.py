"""Historical T49 pre-retirement evidence, run from baseline 13f5fdd.

No provider calls or working selection changes. The retained baseline archive preserves its
legacy comparison interface; this is not an operator command for the final application."""
import asyncio
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import subprocess
import time
from sqlalchemy import select
from login_investigator.knowledge_base import open_current_knowledge_base, schema
from login_investigator.knowledge_base.evaluation_version import StoredEmbeddings
from login_investigator.knowledge_base.graph_selection import select_version
from login_investigator.knowledge_base.graph_version import build_version, capture_snapshot, open_version
from login_investigator.generator import DATASET_DIR
from login_investigator.loader import load_log
from login_investigator.postgres import ServerSettings
from login_investigator.rules import detect_all

backend = Path.cwd()
root = backend / '.graph-versions/t49'
working = backend / '.knowledge-base.json'
evidence = backend.parent / '.scratch/knowledge-base/research/49-preparation.json'

async def passages(kb):
    async with kb.engine.connect() as connection:
        rows = (await connection.execute(select(schema.chunks).order_by(schema.chunks.c.chunk_id))).mappings()
        return [{**dict(r), 'embedding': [float(v) for v in r['embedding']]} for r in rows]

async def main():
    before = working.read_bytes()
    root.mkdir(parents=True, exist_ok=False, mode=0o700)
    recovery = root / 'legacy-recovery'
    recovery.mkdir(mode=0o700)
    (recovery / 'selection.json').write_bytes(before)
    fingerprint = capture_snapshot(DATASET_DIR, recovery / 'source')
    with (recovery / 'code.tar').open('wb') as output:
        subprocess.run(['git', 'archive', '13f5fdd'], cwd=backend.parent, stdout=output, check=True)
    findings = detect_all(load_log(DATASET_DIR / 'logins.csv'))
    async with open_current_knowledge_base(DATASET_DIR, working) as old:
        assert old is not None
        rows = await passages(old)
        old_counts = asdict(await old.check_graph_integrity())
        people = await old.organisation_records('people')
        lookups = {str(p['username']): old.lookup_account(str(p['username'])) for p in people}
        radii = {f.finding_id: asdict(old.finding_radius(f)) for f in findings}
        walks = {f.finding_id: asdict(old.finding_walk(f.finding_id)) for f in findings}
        dated = {(f.finding_id, a, b): asdict(old.finding_radius(f, a, b)) for f in findings
                 for a, b in [('2026-10-07T11:03:00Z', '2026-10-07T11:11:00Z'),
                              ('2026-10-07T11:07:00Z', '2026-10-07T11:11:00Z'),
                              ('2026-09-01', '2026-11-01'), (None, '2026-09-01')]}
    vectors = {r['content']: r['embedding'] for r in rows}
    assert len(vectors) == len(rows)
    report = {'baseline_commit': '13f5fdd', 'source_fingerprint': fingerprint,
              'working_pointer_sha256': hashlib.sha256(before).hexdigest(), 'provider_calls': 0,
              'passages_compared': len(rows), 'accounts_compared': len(lookups),
              'findings_compared': len(radii), 'dated_radii_compared': len(dated), 'versions': []}
    for label in ('rollback', 'candidate'):
        tick = time.monotonic()
        version = await build_version(recovery / 'source', backend / '.graph-versions', ServerSettings.from_env(), StoredEmbeddings(vectors))
        async with open_version(version.marker, ServerSettings.from_env()) as kb:
            assert await passages(kb) == rows
            assert asdict(await kb.check_graph_integrity()) == old_counts
            for username, expected in lookups.items():
                assert kb.lookup_account(username) == expected
            for finding in findings:
                assert asdict(kb.finding_radius(finding)) == radii[finding.finding_id]
                assert asdict(kb.finding_walk(finding.finding_id)) == walks[finding.finding_id]
            for (identifier, start, end), expected in dated.items():
                finding = next(f for f in findings if f.finding_id == identifier)
                assert asdict(kb.finding_radius(finding, start, end)) == expected
            gold = json.loads((kb.source_snapshot / 'truth.json').read_text())['scenarios']['S6']['blast_radius']
            spray = next(f for f in findings if '45.148.10.80' in f.ips and len(f.users) > 10)
            radius = kb.finding_radius(spray).accounts[0]
            assert [g['group_id'] for g in radius.groups] == gold['groups']
            assert [a['asset_id'] for a in radius.assets] == gold['assets']
            assert radius.access_paths == gold['paths']
            assert [p['person_id'] for p in radius.device_peers] == gold['device_peers']
            assert [{'network_id': m.network['network_id'], 'accounts': [p['person_id'] for p in m.accounts],
                     'paths': m.paths} for m in radius.address_reuse.by_address] == gold['address_reuse_context']['by_address']
        await select_version(version.marker, root / 'selected.json')
        report['versions'].append({'role': label, **version.description(), 'snapshot': version.snapshot.relative_to(backend).as_posix(),
                                   'marker': version.marker.relative_to(backend).as_posix(),
                                   'preparation_and_parity_seconds': round(time.monotonic()-tick, 3)})
        assert working.read_bytes() == before
        report['working_pointer_unchanged'] = True
        evidence.write_text(json.dumps(report, indent=2) + '\n')
        print(label, version.build_id, 'exact source/store/parity checks passed', flush=True)
    print('Preparation complete; working selection unchanged.', flush=True)

asyncio.run(main())
