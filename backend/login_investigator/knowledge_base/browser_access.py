"""Stable human identities, separate from each version's application identity."""

from dataclasses import dataclass, field
from pathlib import Path

from dotenv import dotenv_values

from login_investigator.postgres import ENV_PATH

from .graph_service import execute
from .neo4j_graph import GraphSettings


@dataclass(frozen=True)
class BrowserPasswords:
    admin: str = field(repr=False)
    reader: str = field(repr=False)


class MissingBrowserPassword(ValueError):
    """Only a variable name, safe for operator output."""


def browser_passwords() -> BrowserPasswords:
    # These operator credentials deliberately come only from the main private file.
    values = dotenv_values(ENV_PATH, interpolate=False)
    passwords = []
    for name in ('LI_GRAPH_ADMIN_PASSWORD', 'LI_GRAPH_READER_PASSWORD'):
        value = values.get(name)
        if not value or not value.strip():
            raise MissingBrowserPassword(f'{name} is missing or empty in the main .env')
        passwords.append(value)
    return BrowserPasswords(*passwords)


def create_browser_users(settings: GraphSettings, passwords: BrowserPasswords) -> dict[str, str]:
    present = {row['user'] for row in execute(settings, 'SHOW USERS YIELD user RETURN user', 'system')}
    result = {}
    for name, password in (('li_admin', passwords.admin), ('li_reader', passwords.reader)):
        execute(settings, 'CREATE USER $name IF NOT EXISTS SET PASSWORD $password CHANGE NOT REQUIRED',
                'system', name=name, password=password)
        result[name] = 'already present' if name in present else 'created'
    return result


async def provision_browser_users(marker: Path) -> dict[str, str]:
    """Check a running complete pair before adding users; never reset existing passwords."""
    from login_investigator.postgres import ServerSettings
    from login_investigator.workers import owned_operation

    from .graph_service import docker
    from .graph_version import open_version

    passwords = browser_passwords()
    # open_version validates the descriptor, source, both stores and serving protection.
    async with open_version(marker, ServerSettings.from_env()):
        import json

        descriptor = json.loads(marker.read_text())
        if await owned_operation(lambda: docker('inspect', '--format', '{{.State.Running}}',
                                               descriptor['container'])) != 'true':
            raise ValueError('The complete graph pair must be running')
        values = dotenv_values(marker.parent / '.env')
        from .graph_service import GraphService

        service = GraphService(descriptor['container'], marker.parent)
        settings = GraphSettings(await owned_operation(service.uri), values['LI_GRAPH_USER'] or '',
                                 values['LI_GRAPH_PASSWORD'] or '')
        return await owned_operation(lambda: create_browser_users(settings, passwords))
