"""Stable operator access through build, provisioning and selection boundaries."""

import asyncio

import pytest
from test_knowledge_base import DATASET, FakeEmbedder

from login_investigator.knowledge_base.graph_version import build_version
from login_investigator.postgres import ServerSettings


@pytest.mark.parametrize('missing', ['LI_GRAPH_ADMIN_PASSWORD', 'LI_GRAPH_READER_PASSWORD'])
def test_build_refuses_missing_browser_password_before_resources(tmp_path, monkeypatch, missing):
    from login_investigator.knowledge_base import browser_access

    env = tmp_path / '.env'
    env.write_text('\n'.join(f'{name}=test-password' for name in
                             ['LI_GRAPH_ADMIN_PASSWORD', 'LI_GRAPH_READER_PASSWORD'] if name != missing))
    monkeypatch.setattr(browser_access, 'ENV_PATH', env)
    server = ServerSettings('invalid.invalid', 1, 'unused', 'unused')
    with pytest.raises(ValueError, match=missing):
        asyncio.run(build_version(DATASET, tmp_path / 'versions', server, FakeEmbedder()))
    assert not (tmp_path / 'versions').exists()


def test_new_build_and_repeat_provisioning_keep_separate_logins(paired_default, tmp_path, monkeypatch, capsys):
    from neo4j import GraphDatabase

    from login_investigator.knowledge_base import browser_access
    from login_investigator.knowledge_base.graph_service import (
        GraphService,
        check_serving_protection,
    )
    from login_investigator.knowledge_base.neo4j_graph import GraphSettings
    from scripts.provision_browser_users import main

    version = paired_default
    service = GraphService(version.container, version.marker.parent)
    uri = service.uri()
    for name, password in [('li_admin', 'test-browser-admin-password'),
                           ('li_reader', 'test-browser-reader-password')]:
        with GraphDatabase.driver(uri, auth=(name, password)) as driver:
            driver.verify_connectivity()
        assert len(check_serving_protection(GraphSettings(uri, name, password))) == 8
    from dotenv import dotenv_values

    from login_investigator.knowledge_base.graph_service import execute
    values = dotenv_values(version.marker.parent / '.env')
    serving = GraphSettings(uri, values['LI_GRAPH_USER'] or '', values['LI_GRAPH_PASSWORD'] or '')
    assert serving.user == 'li_serving'
    execute(serving, 'DROP USER li_admin', 'system')
    execute(serving, 'DROP USER li_reader', 'system')
    assert main(['--version-file', str(version.marker)]) == 0
    assert 'created' in capsys.readouterr().out
    # A repeat with changed requested passwords must preserve the existing accounts.
    env = tmp_path / '.env'
    env.write_text('LI_GRAPH_ADMIN_PASSWORD=different-admin-password\n'
                   'LI_GRAPH_READER_PASSWORD=different-reader-password\n')
    monkeypatch.setattr(browser_access, 'ENV_PATH', env)
    for _ in range(2):
        assert main(['--version-file', str(version.marker)]) == 0
        output = capsys.readouterr().out
        assert 'already present' in output
        assert 'password' not in output
    with GraphDatabase.driver(uri, auth=('li_reader', 'test-browser-reader-password')) as driver:
        driver.verify_connectivity()
    assert main(['--version-file', str(tmp_path / 'incomplete/complete.json')]) == 1
    assert 'different-reader-password' not in capsys.readouterr().err
    from login_investigator.knowledge_base.graph_service import docker
    docker('stop', service.name)
    try:
        assert main(['--version-file', str(version.marker)]) == 1
    finally:
        docker('start', service.name)
        service.wait(GraphSettings(service.uri(), serving.user, serving.password))


def test_fixed_address_conflict_selection_and_rollback(paired_default, tmp_path, monkeypatch):
    import json
    import socket

    from login_investigator.knowledge_base.graph_address import GraphAddress
    from login_investigator.knowledge_base.graph_selection import (
        rollback_version,
        select_version,
    )
    from login_investigator.knowledge_base.graph_service import GraphService
    from login_investigator.knowledge_base.graph_version import remove_version
    from login_investigator.knowledge_base.staleness import KnowledgeBaseNotReady

    # Inject an address at the selection seam, so a working graph can keep 7474/7687.
    with socket.socket() as bolt_socket, socket.socket() as http_socket:
        bolt_socket.bind(('127.0.0.1', 0))
        http_socket.bind(('127.0.0.1', 0))
        address = GraphAddress(bolt_socket.getsockname()[1], http_socket.getsockname()[1])
    fixed_uri = f'bolt://127.0.0.1:{address.bolt}'
    server = ServerSettings.from_env()
    version = paired_default
    service = GraphService(version.container, version.marker.parent)
    pointer = tmp_path / 'selected.json'
    asyncio.run(select_version(version.marker, pointer, server))
    before = pointer.read_bytes()
    protection = (version.marker.parent / 'protection.json').read_bytes()
    original_uri = service.uri()
    for port in (address.http, address.bolt):
        with socket.socket() as occupied:
            occupied.bind(('127.0.0.1', port))
            occupied.listen()
            with pytest.raises(KnowledgeBaseNotReady, match=str(port)):
                asyncio.run(select_version(version.marker, pointer, server, fixed_address=address))
    assert pointer.read_bytes() == before and service.uri() == original_uri
    replacement = asyncio.run(build_version(DATASET, tmp_path / 'versions', server, FakeEmbedder()))
    other = GraphService(replacement.container, replacement.marker.parent)
    try:
        assert other.uri() != fixed_uri
        asyncio.run(select_version(version.marker, pointer, server, fixed_address=address))
        assert service.uri() == fixed_uri
        from pathlib import Path
        original_replace = Path.replace
        before_failure = pointer.read_bytes()
        def failed_publication(path, target):
            if Path(target) == pointer:
                raise OSError('Injected pointer publication failure')
            return original_replace(path, target)
        with monkeypatch.context() as fault:
            fault.setattr(Path, 'replace', failed_publication)
            with pytest.raises(KnowledgeBaseNotReady):
                asyncio.run(select_version(replacement.marker, pointer, server, fixed_address=address))
        assert pointer.read_bytes() == before_failure
        assert service.uri() == fixed_uri
        assert other.uri() != fixed_uri
        asyncio.run(select_version(replacement.marker, pointer, server, fixed_address=address))
        assert other.uri() == fixed_uri
        assert service.uri() != fixed_uri
        asyncio.run(rollback_version(pointer, server, fixed_address=address))
        assert service.uri() == fixed_uri
        assert other.uri() != fixed_uri
        assert json.loads(pointer.read_text())['current'] == str(version.marker)
        assert (version.marker.parent / 'protection.json').read_bytes() == protection
        assert replacement.marker.exists()
        # A missing outgoing marker must not prevent recovery to a healthy pair.
        saved_marker = version.marker.read_bytes()
        version.marker.unlink()
        try:
            asyncio.run(select_version(replacement.marker, pointer, server, fixed_address=address))
            assert other.uri() == fixed_uri
        finally:
            version.marker.write_bytes(saved_marker)
        from login_investigator.knowledge_base.graph_service import docker
        docker('stop', other.name)
        asyncio.run(select_version(version.marker, pointer, server, fixed_address=address))
        assert service.uri() == fixed_uri
        assert docker('inspect', '--format', '{{.State.Running}}', other.name) == 'false'
    finally:
        remove_version(replacement, server)
