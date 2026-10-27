"""The PostgreSQL server that holds the knowledge base (knowledge-base ticket 09).

The connection details live only in `.env`, or in the environment, which wins. They are read with
`dotenv_values`, never `load_dotenv`, so the password never enters the process environment.
"""

from __future__ import annotations

import os
import uuid
from collections.abc import Mapping
from dataclasses import dataclass, field, replace
from pathlib import Path

import psycopg
from dotenv import dotenv_values
from psycopg import pq, sql
from psycopg.conninfo import make_conninfo

from login_investigator.generator import REPO_ROOT

ENV_PATH = REPO_ROOT / ".env"
SETUP_SCRIPT = "backend/setup/postgres-setup.sql"
PASSWORD_NAME = "LI_PG_PASSWORD"
# An always-on Homebrew service (T02 d4). `restart` also works when the stopped service is still
# registered with macOS, where `start` fails (bug B-072).
START_COMMAND = "brew services restart postgresql@18"
CONNECT_TIMEOUT_SECONDS = 5
MAINTENANCE_DATABASE = "postgres"  # where databases are created and dropped from
DEFAULT_USER = "li_admin"  # both made by the one-time setup
DEFAULT_TEMPLATE = "li_template"
TEST_PREFIX = "li_test"


class DatabaseUnavailable(RuntimeError):
    """The server cannot be used. The message says what to do, and never carries the password."""


@dataclass(frozen=True)
class ServerSettings:
    """Where the server is, the limited role that can only create and drop its own databases, and
    the template every fresh database is copied from. `database` is the one to connect to."""

    host: str
    port: int
    user: str
    password: str = field(repr=False)
    database: str = MAINTENANCE_DATABASE
    template: str = DEFAULT_TEMPLATE

    @classmethod
    def from_env(
        cls, environ: Mapping[str, str] = os.environ, env_file: Path = ENV_PATH
    ) -> ServerSettings:
        values = {**dotenv_values(env_file), **environ}

        def value(name: str, default: str = "") -> str:
            return (values.get(name) or "").strip() or default

        password = value(PASSWORD_NAME)
        if not password:
            raise DatabaseUnavailable(
                f"{PASSWORD_NAME} is not set. Copy env.example to .env and set the password of the "
                f"limited role made by the one-time setup in {SETUP_SCRIPT}."
            )
        port = value("LI_PG_PORT", "5432")
        if not port.isdigit():
            raise DatabaseUnavailable(f"LI_PG_PORT must be a port number, not {port!r}.")
        return cls(
            host=value("LI_PG_HOST", "localhost"),
            port=int(port),
            user=value("LI_PG_USER", DEFAULT_USER),
            password=password,
            template=value("LI_PG_TEMPLATE", DEFAULT_TEMPLATE),
        )

    def conninfo(self) -> str:
        return make_conninfo(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            dbname=self.database,
            connect_timeout=CONNECT_TIMEOUT_SECONDS,
        )


def check_server(settings: ServerSettings) -> None:
    """Fail at once, with the start command, when the server does not answer. A ping needs no
    password, so a stopped service is never mistaken for a wrong one."""
    if pq.PGconn.ping(settings.conninfo().encode()) != pq.Ping.OK:
        raise DatabaseUnavailable(
            f"PostgreSQL is not answering at {settings.host}:{settings.port}. "
            f"Start it with: {START_COMMAND}"
        )


def create_fresh_database(server: ServerSettings, *, prefix: str = TEST_PREFIX) -> ServerSettings:
    """A new, uniquely named database copied from the template, so it has pgvector and nothing
    else. Returns the settings that connect to it. The caller drops it with `drop_database`."""
    if prefix not in (TEST_PREFIX, "li_kb"):
        raise ValueError("Database prefix must be li_test or li_kb")
    name = f"{prefix}_{uuid.uuid4().hex[:12]}"
    create = sql.SQL("CREATE DATABASE {} TEMPLATE {}").format(
        sql.Identifier(name), sql.Identifier(server.template)
    )
    try:
        with psycopg.connect(server.conninfo(), autocommit=True) as connection:
            connection.execute(create)
    except psycopg.OperationalError as error:
        raise DatabaseUnavailable(
            f"PostgreSQL refused the connection as {server.user}: {error}. "
            f"Check LI_PG_USER and {PASSWORD_NAME} in .env."
        ) from None
    except psycopg.Error as error:
        raise DatabaseUnavailable(
            f"Could not copy the template {server.template}: {error}. "
            f"The one-time setup is in {SETUP_SCRIPT}."
        ) from None
    return replace(server, database=name)


def drop_database(database: ServerSettings) -> None:
    """Drop a database made by `create_fresh_database`, closing any connection still open on it."""
    drop = sql.SQL("DROP DATABASE IF EXISTS {} WITH (FORCE)").format(
        sql.Identifier(database.database)
    )
    maintenance = replace(database, database=MAINTENANCE_DATABASE)
    with psycopg.connect(maintenance.conninfo(), autocommit=True) as connection:
        connection.execute(drop)
