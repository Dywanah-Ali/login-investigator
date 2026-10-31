"""T47 isolated build boundary: capture one coherent, immutable source world."""

from pathlib import Path

import pytest

from login_investigator.knowledge_base.graph_version import capture_snapshot
from login_investigator.knowledge_base.staleness import source_fingerprint


def test_snapshot_is_independent_and_refuses_reuse(tmp_path: Path):
    source = tmp_path / 'source'
    source.mkdir()
    (source / 'logins.csv').write_text('original')
    destination = tmp_path / 'snapshot'
    fingerprint = capture_snapshot(source, destination)
    (source / 'logins.csv').write_text('changed')
    assert (destination / 'logins.csv').read_text() == 'original'
    assert fingerprint == source_fingerprint(destination)
    assert not (destination.stat().st_mode & 0o222)
    assert not ((destination / 'logins.csv').stat().st_mode & 0o222)
    with pytest.raises(FileExistsError):
        capture_snapshot(source, destination)
    destination.chmod(0o700)


def test_isolated_version_opens_reference_graph_and_keeps_active_pointer(tmp_path: Path):
    import asyncio
    import json

    from test_knowledge_base import DATASET, FakeEmbedder

    from login_investigator.knowledge_base.graph_version import (
        build_version,
        open_version,
        remove_version,
    )
    from login_investigator.postgres import ServerSettings

    active = tmp_path / 'active.json'
    active.write_text('{"database":"untouched"}')

    async def check():
        version = await build_version(DATASET, tmp_path / 'versions', ServerSettings.from_env(), FakeEmbedder())
        try:
            assert active.read_text() == '{"database":"untouched"}'
            assert version.marker.is_file()
            assert json.loads(version.marker.read_text())['build_id'] == version.build_id
            async with open_version(version.marker, ServerSettings.from_env()) as kb:
                result = kb.lookup_account('USER-AMELIA.WARD')
                assert result['status'] == 'found'
                assert isinstance(result['account'], dict)
                assert result['account']['department'] == 'IT'
                assert kb.lookup_account('missing')['status'] == 'not_found'
                from sqlalchemy import text
                from sqlalchemy.exc import DBAPIError
                with pytest.raises(DBAPIError):
                    async with kb.engine.begin() as connection:
                        await connection.execute(text("UPDATE graph_pair SET build_id='reader-write'"))

                from dataclasses import asdict, replace

                from login_investigator.knowledge_base import (
                    open_knowledge_base,
                    reader_settings,
                )
                from login_investigator.loader import load_log
                from login_investigator.rules import NEW_COUNTRY, detect_all
                async with open_knowledge_base(reader_settings(replace(ServerSettings.from_env(), database=version.database)),
                                               dataset=version.snapshot) as previous:
                    for finding in detect_all(load_log(version.snapshot / 'logins.csv')):
                        assert asdict(kb.finding_radius(finding)) == asdict(previous.finding_radius(finding))
                        assert kb.finding_walk(finding.finding_id) == previous.finding_walk(finding.finding_id)
                    assert kb.account_groups('AMELIA.WARD') == previous.account_groups('AMELIA.WARD')
                    people = await previous.organisation_records('people')
                    for person in people:
                        assert kb.lookup_account(str(person['username'])) == previous.lookup_account(str(person['username']))
                    findings = detect_all(load_log(version.snapshot / 'logins.csv'))
                    subject = next(f for f in findings if f.rule == NEW_COUNTRY and 'amelia.ward' in f.users)
                    for start, end in [('2026-10-07T11:03:00Z', '2026-10-07T11:11:00Z'),
                                       ('2026-10-07T11:07:00Z', '2026-10-07T11:11:00Z'),
                                       ('2026-09-01', '2026-11-01'), (None, '2026-09-01')]:
                        assert asdict(kb.finding_radius(subject, start, end)) == asdict(previous.finding_radius(subject, start, end))
                    spray = next(f for f in findings if '45.148.10.80' in f.ips and len(f.users) > 10)
                    radius = kb.finding_radius(spray).accounts[0]
                    gold = json.loads((DATASET / 'truth.json').read_text())['scenarios']['S6']['blast_radius']
                    assert [g['group_id'] for g in radius.groups] == gold['groups']
                    assert [a['asset_id'] for a in radius.assets] == gold['assets']
                    assert radius.access_paths == gold['paths']
                    assert [p['person_id'] for p in radius.device_peers] == gold['device_peers']
                    assert [{'network_id': m.network['network_id'], 'accounts': [p['person_id'] for p in m.accounts],
                             'paths': m.paths} for m in radius.address_reuse.by_address] == gold['address_reuse_context']['by_address']
            # A complete-looking file cannot legitimise a mismatched pair or edited snapshot.
            original = version.marker.read_text()
            descriptor = json.loads(original)
            descriptor['fingerprint'] = '0' * 64
            version.marker.write_text(json.dumps(descriptor))
            with pytest.raises(ValueError, match='Source snapshot changed'):
                async with open_version(version.marker, ServerSettings.from_env()):
                    pytest.fail('Mismatched fingerprint was accepted')
            version.marker.write_text(original)
            from sqlalchemy import text

            from login_investigator.knowledge_base import database_engine
            engine = database_engine(replace(ServerSettings.from_env(), database=version.database))
            try:
                async with engine.begin() as connection:
                    await connection.execute(text("UPDATE graph_pair SET build_id='wrong-pair'"))
                with pytest.raises(ValueError, match='build identities'):
                    async with open_version(version.marker, ServerSettings.from_env()):
                        pytest.fail('Mismatched PostgreSQL pair was accepted')
            finally:
                await engine.dispose()
        finally:
            remove_version(version, ServerSettings.from_env())

    asyncio.run(check())


def test_failed_embedding_build_leaves_no_resources_or_marker(tmp_path: Path):
    import asyncio

    from test_knowledge_base import DATASET, FakeEmbedder

    from login_investigator.knowledge_base.graph_version import build_version
    from login_investigator.postgres import ServerSettings

    class FailedEmbedder(FakeEmbedder):
        def embed_documents(self, texts: list[str]) -> list[list[float]]:
            raise RuntimeError('deliberate offline failure')

    with pytest.raises(RuntimeError, match='deliberate offline failure'):
        asyncio.run(build_version(DATASET, tmp_path / 'versions', ServerSettings.from_env(), FailedEmbedder()))
    assert list((tmp_path / 'versions').iterdir()) == []


@pytest.mark.parametrize('stage', [1, 2], ids=['preparation', 'sealing'])
def test_cancelled_partial_docker_creation_finishes_before_cleanup(tmp_path: Path, monkeypatch, stage: int):
    """Inject a lost Docker response after real creation, during either lifecycle stage."""
    import asyncio
    import subprocess
    import threading

    from test_knowledge_base import DATASET, FakeEmbedder

    from login_investigator.knowledge_base.graph_version import build_version
    from login_investigator.postgres import ServerSettings

    original_run = subprocess.run
    created: list[str] = []
    reached = threading.Event()
    release = threading.Event()

    def interrupted_response(command, *args, **kwargs):
        result = original_run(command, *args, **kwargs)
        if command[:2] == ['docker', 'create']:
            created.append(command[command.index('--name') + 1])
            if len(created) == stage:
                reached.set()
                if not release.wait(30):
                    raise RuntimeError('Test did not release Docker response')
                raise subprocess.TimeoutExpired(command, 90)
        return result

    monkeypatch.setattr(subprocess, 'run', interrupted_response)

    async def check():
        task = asyncio.create_task(build_version(DATASET, tmp_path / 'versions', ServerSettings.from_env(), FakeEmbedder()))
        try:
            assert await asyncio.to_thread(reached.wait, 240), 'Docker creation checkpoint was not reached'
            task.cancel()
            await asyncio.sleep(0.05)
            assert not task.done(), 'Cancellation must await the worker before cleaning resources'
        finally:
            release.set()
        with pytest.raises(asyncio.CancelledError):
            await task

    asyncio.run(check())
    assert created
    assert list((tmp_path / 'versions').iterdir()) == []
    for name in set(created):
        assert original_run(['docker', 'container', 'inspect', name], capture_output=True).returncode != 0
        assert original_run(['docker', 'volume', 'inspect', name + '-data'], capture_output=True).returncode != 0


def test_unknown_docker_ownership_retains_recovery_state(tmp_path: Path, monkeypatch):
    import asyncio
    import json
    import subprocess
    from dataclasses import replace

    from test_knowledge_base import DATASET, FakeEmbedder

    from login_investigator.knowledge_base.graph_service import GraphService
    from login_investigator.knowledge_base.graph_version import (
        build_version,
        dispose_resources,
    )
    from login_investigator.knowledge_base.neo4j_graph import GraphUnavailable
    from login_investigator.postgres import ServerSettings

    original_run = subprocess.run
    lost_response = False

    def unavailable_after_creation(command, *args, **kwargs):
        nonlocal lost_response
        if lost_response and command[:3] == ['docker', 'container', 'inspect']:
            return subprocess.CompletedProcess(command, 1, '', 'Docker daemon unavailable')
        result = original_run(command, *args, **kwargs)
        if command[:2] == ['docker', 'create']:
            lost_response = True
            raise subprocess.TimeoutExpired(command, 90)
        return result

    monkeypatch.setattr(subprocess, 'run', unavailable_after_creation)
    with pytest.raises(GraphUnavailable, match='Cleanup incomplete'):
        asyncio.run(build_version(DATASET, tmp_path / 'versions', ServerSettings.from_env(), FakeEmbedder()))
    directory, = (tmp_path / 'versions').iterdir()
    recovery = json.loads((directory / 'cleanup.json').read_text())
    assert recovery['incomplete'] == ['neo4j']
    assert not (directory / 'complete.json').exists()
    assert (directory / 'source/logins.csv').exists()
    monkeypatch.setattr(subprocess, 'run', original_run)
    service = GraphService(recovery['container'], directory)
    service.creation_attempted = True
    dispose_resources(service, replace(ServerSettings.from_env(), database=recovery['database']), directory)
    assert not directory.exists()


def test_configured_reader_must_be_separate_before_completion(tmp_path: Path, monkeypatch):
    import asyncio

    from test_knowledge_base import DATASET, FakeEmbedder

    from login_investigator.knowledge_base.graph_version import build_version
    from login_investigator.postgres import DatabaseUnavailable, ServerSettings

    server = ServerSettings.from_env()
    monkeypatch.setenv('LI_PG_READER_USER', server.user)
    with pytest.raises(DatabaseUnavailable, match='separate read-only login'):
        asyncio.run(build_version(DATASET, tmp_path / 'versions', server, FakeEmbedder()))
    assert list((tmp_path / 'versions').iterdir()) == []
