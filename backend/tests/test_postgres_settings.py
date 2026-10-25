"""The PostgreSQL connection settings (knowledge-base ticket 09). They come from `.env`, or from the
environment, which wins. No test here needs the service."""

import pytest

from login_investigator import postgres


def env_file(tmp_path, text):
    path = tmp_path / ".env"
    path.write_text(text, encoding="utf-8")
    return path


def test_a_missing_password_fails_naming_the_setting_and_the_setup(tmp_path):
    with pytest.raises(postgres.DatabaseUnavailable) as caught:
        postgres.ServerSettings.from_env(environ={}, env_file=env_file(tmp_path, ""))
    assert "LI_PG_PASSWORD" in str(caught.value)
    assert "setup/postgres-setup.sql" in str(caught.value)


def test_the_environment_wins_over_the_file_and_unset_names_take_the_defaults(tmp_path):
    path = env_file(tmp_path, "LI_PG_PASSWORD=from-the-file\nLI_PG_PORT=5433\n")
    settings = postgres.ServerSettings.from_env(
        environ={"LI_PG_PASSWORD": "from-the-environment"}, env_file=path
    )
    assert settings == postgres.ServerSettings(
        host="localhost",
        port=5433,
        user="li_admin",
        password="from-the-environment",
        database="postgres",
        template="li_template",
    )


def test_a_port_that_is_not_a_number_fails_naming_the_setting(tmp_path):
    path = env_file(tmp_path, "LI_PG_PASSWORD=x\nLI_PG_PORT=five\n")
    with pytest.raises(postgres.DatabaseUnavailable, match="LI_PG_PORT"):
        postgres.ServerSettings.from_env(environ={}, env_file=path)
