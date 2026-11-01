"""T50 one-time preparation: build the paired version without address edges, with no provider calls.

Reuses the checked passage vectors of the currently selected working version, exactly as T49 did,
because the corpus is unchanged. Only truth.json changed, so the source fingerprint differs.
Parity with the selected version is checked for every passage, account, finding radius and walk,
with the removed address context as the only expected difference. The working selection is not
changed here; selection and restart follow the admin manual, section 5.

Run from backend/: uv run python ../.scratch/knowledge-base/research/50-prepare.py
"""
import asyncio
import json
import sys
import time
from dataclasses import asdict
from pathlib import Path

# Running a research file makes its directory sys.path[0]; mirror the backend server cwd.
sys.path.insert(0, str(Path.cwd()))

from dataclasses import replace  # noqa: E402

from dotenv import dotenv_values  # noqa: E402
from sqlalchemy import select  # noqa: E402

from login_investigator.generator import DATASET_DIR  # noqa: E402
from login_investigator.knowledge_base import database_engine, reader_settings, schema  # noqa: E402
from login_investigator.knowledge_base.evaluation_version import StoredEmbeddings  # noqa: E402
from login_investigator.knowledge_base.graph_service import GraphService  # noqa: E402
from login_investigator.knowledge_base.graph_version import build_version, open_version  # noqa: E402
from login_investigator.knowledge_base.neo4j_graph import GraphSettings, Neo4jQueries  # noqa: E402
from login_investigator.loader import load_log  # noqa: E402
from login_investigator.postgres import ServerSettings  # noqa: E402
from login_investigator.rules import detect_all  # noqa: E402

backend = Path.cwd()
working = backend / '.knowledge-base.json'
evidence = backend.parent / '.scratch/knowledge-base/research/50-preparation.json'
DATED = [('2026-10-07T11:03:00Z', '2026-10-07T11:11:00Z'), ('2026-10-07T11:07:00Z', '2026-10-07T11:11:00Z'),
         ('2026-09-01', '2026-11-01'), (None, '2026-09-01')]


async def passages(engine):
    async with engine.connect() as connection:
        rows = (await connection.execute(select(schema.chunks).order_by(schema.chunks.c.chunk_id))).mappings()
        return [{**dict(r), 'embedding': [float(v) for v in r['embedding']]} for r in rows]


async def main():
    server = ServerSettings.from_env()
    before = working.read_bytes()
    pointer = json.loads(before)
    assert pointer['format'] == 'paired-v1'
    current = Path(pointer['current'])
    descriptor = json.loads(current.read_text())
    assert descriptor['build_id'] == current.parent.name
    old_snapshot = current.parent / 'source'
    tick = time.monotonic()
    # The previous pair carries used_address edges, which the new integrity check refuses by
    # design, so it is read here directly, the way open_version reads it, minus that check.
    # The new radius code ignores those edges, so its answers over the old graph are the
    # answers the new graph must reproduce.
    values = dotenv_values(current.parent / '.env')
    settings = GraphSettings(GraphService(descriptor['container'], current.parent).uri(),
                             values.get('LI_GRAPH_USER') or '', values.get('LI_GRAPH_PASSWORD') or '')
    old_engine = database_engine(reader_settings(replace(server, database=descriptor['database'])), bounded=True)
    log = load_log(old_snapshot / 'logins.csv')
    findings = detect_all(log)
    old = Neo4jQueries(settings, log)
    try:
        rows = await passages(old_engine)
        old_nodes = {r['t']: r['n'] for r in old._read('MATCH (n:Entity) RETURN n.entity_type AS t, count(*) AS n')}
        old_edges = {r['t']: r['n'] for r in old._read('MATCH ()-[r]->() RETURN type(r) AS t, count(*) AS n')}
        people = [r['p'] for r in old._read("MATCH (p:Entity {entity_type:'person'}) RETURN p.username AS p ORDER BY p")]
        lookups = {username: old.lookup_account(username) for username in people}
        radii = {f.finding_id: asdict(old.finding_radius(f)) for f in findings}
        walks = {f.finding_id: asdict(old.finding_walk(f.finding_id)) for f in findings}
        dated = {(f.finding_id, a, b): asdict(old.finding_radius(f, a, b)) for f in findings for a, b in DATED}
    finally:
        old.close()
        await old_engine.dispose()
    address_edges_before = old_edges.pop('used_address', 0)
    assert address_edges_before > 0, 'The previous pair was expected to carry used_address edges'
    old_counts = {'nodes': old_nodes, 'edges': old_edges}
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
        for username, expected in lookups.items():
            assert kb.lookup_account(username) == expected
        for finding in findings:
            assert asdict(kb.finding_radius(finding)) == radii[finding.finding_id]
            assert asdict(kb.finding_walk(finding.finding_id)) == walks[finding.finding_id]
        for (identifier, start, end), expected in dated.items():
            finding = next(f for f in findings if f.finding_id == identifier)
            assert asdict(kb.finding_radius(finding, start, end)) == expected
        gold = json.loads((kb.source_snapshot / 'truth.json').read_text())['scenarios']['S6']['blast_radius']
        assert 'address_reuse_context' not in gold
        spray = next(f for f in findings if '45.148.10.80' in f.ips and len(f.users) > 10)
        radius = kb.finding_radius(spray).accounts[0]
        assert [g['group_id'] for g in radius.groups] == gold['groups']
        assert [a['asset_id'] for a in radius.assets] == gold['assets']
        assert radius.access_paths == gold['paths']
        assert [p['person_id'] for p in radius.device_peers] == gold['device_peers']
        assert not hasattr(radius, 'address_reuse')
    assert working.read_bytes() == before
    report = {'ticket': 'T50', 'previous_build': current.parent.name, 'build_id': version.build_id,
              'source_fingerprint': version.fingerprint, 'provider_calls': 0,
              'passages_compared': len(rows), 'accounts_compared': len(lookups),
              'findings_compared': len(radii), 'dated_radii_compared': len(dated),
              'used_address_edges_before': address_edges_before, 'used_address_edges_after': 0,
              'graph_counts': new_counts, 'working_pointer_unchanged': True,
              'marker': version.marker.relative_to(backend).as_posix(),
              'preparation_and_parity_seconds': round(time.monotonic() - tick, 3)}
    evidence.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2), flush=True)


asyncio.run(main())
