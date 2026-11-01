"""Door 2: a legacy pointer must never reopen the retired graph engine."""

import asyncio
import json

import pytest

from login_investigator.knowledge_base import (
    KnowledgeBaseNotReady,
    open_current_knowledge_base,
)
from login_investigator.knowledge_base.staleness import PAIR_UNCHECKABLE
from login_investigator.postgres import ServerSettings


def test_legacy_selection_refuses_before_opening_any_store(tmp_path, monkeypatch):
    pointer = tmp_path / 'legacy.json'
    pointer.write_text(json.dumps({'database': 'li_kb_000000000000'}))
    before = pointer.read_bytes()

    def forbidden():
        raise AssertionError('A legacy selection must refuse before reading database credentials')

    monkeypatch.setattr(ServerSettings, 'from_env', forbidden)

    async def check():
        with pytest.raises(KnowledgeBaseNotReady, match='selected source') as caught:
            async with open_current_knowledge_base(tmp_path, pointer):
                pytest.fail('The retired graph selection was accepted')
        assert str(caught.value) == PAIR_UNCHECKABLE

    asyncio.run(check())
    assert pointer.read_bytes() == before
