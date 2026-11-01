"""Select a verified complete version for the next restart. Never delete a version."""

import json
import tempfile
from pathlib import Path

from login_investigator.postgres import ServerSettings
from login_investigator.workers import owned_operation

from .graph_address import AddressMove, GraphAddress, GraphAddressUnavailable
from .graph_version import open_version
from .staleness import PAIR_UNCHECKABLE, KnowledgeBaseNotReady


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
                         server: ServerSettings | None = None, *, fixed_address: GraphAddress | None = None) -> dict:
    """Validate before a same-directory rename; failures preserve the old selection.

    Operators serialize selection commands. This local rename is not a distributed transaction
    or a power-loss durability guarantee. Running processes never reload this file.
    """
    temporary = None
    address = None
    published = False
    try:
        marker = marker.resolve(strict=True)
        server = server or ServerSettings.from_env()
        before = state_file.read_bytes() if state_file.exists() else None
        previous = read_selection(state_file) if before is not None else None
        descriptor = marker.read_bytes()
        async with open_version(marker, server) as kb:
            if kb.source_snapshot is None or state_file.resolve().is_relative_to(kb.source_snapshot):
                raise ValueError('Selection must be outside the immutable snapshot')
        if marker.read_bytes() != descriptor:
            raise ValueError('Version changed during validation')
        if (state_file.read_bytes() if state_file.exists() else None) != before:
            raise ValueError('Selection changed concurrently; retry')
        selected = {'format': 'paired-v1', 'current': str(marker),
                    'previous': previous['current'] if previous else None}
        if previous and previous['current'] == str(marker):
            selected = previous
        state_file.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(mode='w', dir=state_file.parent, delete=False) as handle:
            temporary = Path(handle.name)
            json.dump(selected, handle, indent=2)
            handle.write('\n')
        if fixed_address:
            outgoing = Path(previous['current']) if previous else None
            address = await owned_operation(lambda: AddressMove(marker, outgoing, fixed_address))
            await owned_operation(address.move)
            async with open_version(marker, server):
                pass
            if marker.read_bytes() != descriptor:
                raise ValueError('Version changed during address movement')
        if (state_file.read_bytes() if state_file.exists() else None) != before:
            raise ValueError('Selection changed concurrently; retry')
        temporary.replace(state_file)
        published = True
        return selected
    except BaseException as error:
        if address is not None and not published:
            try:
                await owned_operation(address.restore)
            except Exception:  # noqa: BLE001 - Keep recovery errors credential-safe.
                raise KnowledgeBaseNotReady('Graph address recovery failed. Selection file is unchanged. '
                                             'Keep the backend stopped and recover the named retained graph pairs.') from None
        if not isinstance(error, Exception):
            raise
        if isinstance(error, GraphAddressUnavailable):
            raise KnowledgeBaseNotReady(str(error)) from None
        raise KnowledgeBaseNotReady(PAIR_UNCHECKABLE) from None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


async def rollback_version(state_file: Path, server: ServerSettings | None = None,
                           *, fixed_address: GraphAddress | None = None) -> dict:
    """Revalidate the retained previous version and select it for a planned restart."""
    try:
        previous = read_selection(state_file)['previous']
        if previous is None:
            raise ValueError('There is no previous complete version')
        return await select_version(Path(previous), state_file, server, fixed_address=fixed_address)
    except KnowledgeBaseNotReady:
        raise
    except Exception:  # noqa: BLE001 - Refuse rollback with a fixed, credential-safe error.
        raise KnowledgeBaseNotReady(PAIR_UNCHECKABLE) from None
