"""Operator selection must never replace a good pointer with an unverified version."""

import asyncio

import pytest


def test_missing_version_preserves_existing_selection(tmp_path):
    from login_investigator.knowledge_base import KnowledgeBaseNotReady
    from login_investigator.knowledge_base.graph_selection import select_version

    pointer = tmp_path / 'selected.json'
    pointer.write_text('{"format":"paired-v1","current":"/previous/complete.json","previous":null}')
    before = pointer.read_bytes()
    with pytest.raises(KnowledgeBaseNotReady):
        asyncio.run(select_version(tmp_path / 'missing/complete.json', pointer))
    assert pointer.read_bytes() == before


def test_rollback_without_previous_version_refuses_without_rewriting(tmp_path):
    from login_investigator.knowledge_base import KnowledgeBaseNotReady
    from login_investigator.knowledge_base.graph_selection import rollback_version

    pointer = tmp_path / 'selected.json'
    pointer.write_text('{"format":"paired-v1","current":"/current/complete.json","previous":null}')
    before = pointer.read_bytes()
    with pytest.raises(KnowledgeBaseNotReady):
        asyncio.run(rollback_version(pointer))
    assert pointer.read_bytes() == before


def test_selection_rejects_unrecognised_fields(tmp_path):
    from login_investigator.knowledge_base.graph_selection import read_selection

    pointer = tmp_path / 'selected.json'
    pointer.write_text('{"format":"paired-v1","current":"/current/complete.json",'
                       '"previous":null,"unexpected":"do not echo this"}')
    with pytest.raises(ValueError):
        read_selection(pointer)
