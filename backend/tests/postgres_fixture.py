"""The shared database fixture (knowledge-base ticket 09). A test that needs PostgreSQL asks for
`fresh_database`; every other test runs without the service.

Kept in its own module, imported by `tests/conftest.py`, so the fixture's own tests can load it into
the small pytest sessions they run.
"""

from collections.abc import Iterator

import pytest

from login_investigator import postgres


def _create() -> postgres.ServerSettings | str:
    """A fresh database's settings, or what to do when the server cannot be used."""
    try:
        server = postgres.ServerSettings.from_env()
        postgres.check_server(server)
        return postgres.create_fresh_database(server)
    except postgres.DatabaseUnavailable as error:
        return str(error)


@pytest.fixture(scope="session")
def fresh_database() -> Iterator[postgres.ServerSettings]:
    """One fresh database for the whole test session, dropped when the session ends, whether its
    tests passed or failed. Fails, never skips, when the server cannot be used: a missing database
    must never pass."""
    database = _create()
    if isinstance(database, str):
        pytest.fail(database, pytrace=False)
    yield database
    postgres.drop_database(database)
