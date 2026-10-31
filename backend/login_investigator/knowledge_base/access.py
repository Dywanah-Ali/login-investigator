"""Separate builder and reader credentials, with grants enforced by PostgreSQL."""

import os
from collections.abc import Mapping
from dataclasses import replace
from pathlib import Path

from dotenv import dotenv_values
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from login_investigator.postgres import ENV_PATH, DatabaseUnavailable, ServerSettings


def reader_settings(
    database: ServerSettings, environ: Mapping[str, str] = os.environ, env_file: Path = ENV_PATH,
) -> ServerSettings:
    values = {**dotenv_values(env_file), **environ}
    password = values.get("LI_PG_READER_PASSWORD") or ""
    user = values.get("LI_PG_READER_USER") or "li_reader"
    if not password or user == database.user:
        raise DatabaseUnavailable(
            "Set LI_PG_READER_PASSWORD for the separate read-only login. "
            "Run backend/setup/postgres-reader-setup.sql once as your administrator."
        )
    return replace(database, user=user, password=password)


async def check_reader_role(engine: AsyncEngine, role: str) -> None:
    async with engine.connect() as connection:
        row = (await connection.execute(text("""
            SELECT rolname, rolsuper, rolcreatedb, rolcreaterole, rolreplication, rolbypassrls,
                   rolname = current_user AS is_builder,
                   EXISTS (SELECT 1 FROM pg_auth_members WHERE member = pg_roles.oid) AS member
            FROM pg_roles WHERE rolname = :role
        """), {"role": role})).mappings().one_or_none()
    if row is None or any(value for key, value in row.items() if key != "rolname"):
        raise DatabaseUnavailable(
            "The reader must be a separate unprivileged role with no memberships. "
            "Run backend/setup/postgres-reader-setup.sql once as your administrator."
        )


async def grant_read_only(engine: AsyncEngine, database: str, role: str) -> None:
    # Only trusted settings become quoted identifiers. Data values always use bound parameters.
    quote = engine.dialect.identifier_preparer.quote_identifier
    async with engine.begin() as connection:
        for statement in (
            f"REVOKE ALL ON DATABASE {quote(database)} FROM PUBLIC",
            f"GRANT CONNECT ON DATABASE {quote(database)} TO {quote(role)}",
            "REVOKE ALL ON SCHEMA public FROM PUBLIC",
            f"GRANT USAGE ON SCHEMA public TO {quote(role)}",
            f"GRANT SELECT ON ALL TABLES IN SCHEMA public TO {quote(role)}",
        ):
            await connection.execute(text(statement))
