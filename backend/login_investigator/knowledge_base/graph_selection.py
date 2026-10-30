"""Select a verified complete version for the next restart. Never delete a version."""

import json
import tempfile
from pathlib import Path

from login_investigator.postgres import ServerSettings
from .graph_version import open_version
from .staleness import KnowledgeBaseNotReady, PAIR_UNCHECKABLE


def read_selection(state_file: Path) -> dict:
    value = json.loads(state_file.read_text())
    if (not isinstance(value, dict) or set(value) != {'format', 'current', 'previous'}
            or value.get('format') != 'paired-v1'
            or not isinstance(value.get('current'), str)
            or not Path(value['current']).is_absolute()
            or (value.get('previous') is not None and
                (not isinstance(value['previous'], str) or not Path(value['previous']).is_absolute()))):
        raise ValueError('Invalid paired selection')
    return value


async def select_version(marker: Path, state_file: Path,
                         server: ServerSettings | None = None) -> dict:
    """Validate before a same-directory rename; failures preserve the old selection.

    Operators serialize selection commands. This local rename is not a distributed transaction
    or a power-loss durability guarantee. Running processes never reload this file.
    """
    temporary = None
    try:
        marker = marker.resolve(strict=True)
        before = state_file.read_bytes() if state_file.exists() else None
        previous = read_selection(state_file) if before is not None else None
        descriptor = marker.read_bytes()
        async with open_version(marker, server or ServerSettings.from_env()) as kb:
            if kb.source_snapshot is None or state_file.resolve().is_relative_to(kb.source_snapshot):
                raise ValueError('Selection must be outside the immutable snapshot')
        if marker.read_bytes() != descriptor:
            raise ValueError('Version changed during validation')
        if (state_file.read_bytes() if state_file.exists() else None) != before:
            raise ValueError('Selection changed concurrently; retry')
        selected = {'format': 'paired-v1', 'current': str(marker),
                    'previous': previous['current'] if previous else None}
        if previous and previous['current'] == str(marker):
            return previous
        state_file.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(mode='w', dir=state_file.parent, delete=False) as handle:
            temporary = Path(handle.name)
            json.dump(selected, handle, indent=2)
            handle.write('\n')
        temporary.replace(state_file)
        return selected
    except Exception:
        raise KnowledgeBaseNotReady(PAIR_UNCHECKABLE) from None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


async def rollback_version(state_file: Path, server: ServerSettings | None = None) -> dict:
    """Revalidate the retained previous version and select it for a planned restart."""
    try:
        previous = read_selection(state_file)['previous']
        if previous is None:
            raise ValueError('There is no previous complete version')
        return await select_version(Path(previous), state_file, server)
    except Exception:
        raise KnowledgeBaseNotReady(PAIR_UNCHECKABLE) from None
