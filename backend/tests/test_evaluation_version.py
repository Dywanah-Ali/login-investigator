"""Each evaluation owns resources that cannot replace the application's version."""

import asyncio

import pytest

from login_investigator.knowledge_base.graph_selection import select_version
from login_investigator.knowledge_base.graph_version import (
    build_version,
    remove_version,
)
from login_investigator.postgres import ServerSettings
from tests.test_knowledge_base import FakeEmbedder
from tests.test_knowledge_graph import graph_dataset


@pytest.fixture
def evaluation_source(tmp_path):
    server = ServerSettings.from_env()
    # Inject a test provider at the normal build seam. This fixture is not live evaluation
    # evidence. The separate offline-mode refusal test continues to enforce that boundary.
    version = asyncio.run(build_version(graph_dataset(tmp_path / 'source'),
                                        tmp_path / 'versions', server, FakeEmbedder()))
    state = tmp_path / 'selected.json'
    try:
        asyncio.run(select_version(version.marker, state, server))
        yield version, state
    finally:
        remove_version(version, server)


def test_evaluation_without_a_knowledge_base_needs_no_database(tmp_path, monkeypatch):
    from login_investigator.knowledge_base.evaluation_version import isolated_evaluation
    from login_investigator.postgres import ServerSettings

    def forbidden(*args, **kwargs):
        raise AssertionError('No-build evaluation must not read database settings')

    monkeypatch.setattr(ServerSettings, 'from_env', forbidden)

    async def check():
        from login_investigator.knowledge_base import open_current_knowledge_base

        working = tmp_path / 'absent.json'
        async with isolated_evaluation(tmp_path, working) as version:
            assert version.build_id is None
            assert version.dataset == tmp_path
            assert not version.state_file.exists()
            working.write_text('{"database": "newly_published_build"}')
            async with open_current_knowledge_base(version.dataset, version.state_file) as kb:
                assert kb is None
        assert not version.state_file.parent.exists()

    asyncio.run(check())


def test_evaluation_builds_its_own_pair_and_cleans_after_caller_failure(evaluation_source, tmp_path):
    import psycopg

    from login_investigator.knowledge_base import open_current_knowledge_base
    from login_investigator.knowledge_base.evaluation_version import isolated_evaluation
    from login_investigator.knowledge_base.graph_service import GraphService
    from login_investigator.postgres import ServerSettings
    from tests.test_knowledge_base import FakeEmbedder

    source, state = evaluation_source
    dataset = source.snapshot
    before = state.read_bytes()
    original_database = source.database
    observed = {}

    async def check():
        with pytest.raises(RuntimeError, match='Injected evaluation failure'):
            async with isolated_evaluation(dataset, state, root=tmp_path / 'evaluations') as version:
                assert version.build_id is not None
                assert version.dataset != dataset and version.state_file != state
                async with open_current_knowledge_base(version.dataset, version.state_file,
                                                       embedder=FakeEmbedder()) as kb:
                    assert kb is not None
                    observed['database'] = kb.engine.url.database
                    observed['build_id'] = version.build_id
                    observed['snapshot'] = version.dataset
                    assert observed['database'] != original_database
                    assert kb.lookup_account('amelia.ward')['status'] == 'found'
                    search = await kb.search_corpus('payroll')
                    assert len(search.chunks) == 1 and 'thomas.price' in search.chunks[0].chunk.text
                raise RuntimeError('Injected evaluation failure')
        assert state.read_bytes() == before
        async with open_current_knowledge_base(dataset, state) as kb:
            assert kb is not None and kb.lookup_account('amelia.ward')['status'] == 'found'

    asyncio.run(check())
    assert not observed['snapshot'].exists()
    assert list((tmp_path / 'evaluations').iterdir()) == []
    service = GraphService('li-graph-' + observed['build_id'], tmp_path)
    assert not service.owns('container', service.name)
    assert not service.owns('volume', service.volume)
    with psycopg.connect(ServerSettings.from_env().conninfo()) as connection:
        assert connection.execute('SELECT datname FROM pg_database WHERE datname=%s',
                                  (observed['database'],)).fetchone() is None
