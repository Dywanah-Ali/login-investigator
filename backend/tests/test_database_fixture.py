"""The shared database fixture (knowledge-base ticket 09), seen the way a test that asks for a
database sees it. Most tests here run a small pytest session of their own and read its outcome.

Every test that asks for `fresh_database` needs the running service, and fails without it."""

import psycopg

INNER_CONFTEST = "from postgres_fixture import fresh_database  # noqa: F401\n"


def one(settings, query, params=None):
    """The single value a query returns, read through its own connection."""
    with psycopg.connect(settings.conninfo()) as connection:
        row = connection.execute(query, params).fetchone()
    assert row is not None
    return row[0]


def test_a_test_gets_a_fresh_empty_database_of_its_own_with_pgvector(fresh_database):
    assert one(fresh_database, "SELECT current_database()") == fresh_database.database
    assert fresh_database.database.startswith("li_test_")
    tables = "SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public'"
    assert one(fresh_database, tables) == 0
    assert one(fresh_database, "SELECT '[1,2,3]'::vector <-> '[1,2,4]'::vector") == 1.0


def test_the_template_gives_the_pinned_pgvector_version(fresh_database):
    """The template is an input of every fresh database, so its pgvector is pinned like a package.
    Upgrading it in the template is a deliberate change that updates this pin (ticket 09)."""
    version = "SELECT extversion FROM pg_extension WHERE extname = 'vector'"
    assert one(fresh_database, version) == "0.8.7"


def test_each_session_gets_its_own_database_dropped_at_the_end_even_after_a_failing_test(
    pytester, fresh_database
):
    pytester.makeconftest(INNER_CONFTEST)
    pytester.makepyfile(
        """
        from pathlib import Path

        def test_records_its_database_then_fails(fresh_database):
            Path("inner-database.txt").write_text(fresh_database.database)
            assert False, "this test fails on purpose"
        """
    )

    result = pytester.runpytest()

    result.assert_outcomes(failed=1)
    inner = (pytester.path / "inner-database.txt").read_text()
    assert inner != fresh_database.database
    still_there = "SELECT count(*) FROM pg_database WHERE datname = %s"
    assert one(fresh_database, still_there, (inner,)) == 0


def test_a_stopped_service_fails_the_test_with_the_start_command_and_never_skips(
    pytester, monkeypatch
):
    monkeypatch.setenv("LI_PG_HOST", "127.0.0.1")
    monkeypatch.setenv("LI_PG_PORT", "1")  # nothing listens on port 1
    monkeypatch.setenv("LI_PG_PASSWORD", "not-a-real-password")
    pytester.makeconftest(INNER_CONFTEST)
    pytester.makepyfile("def test_needs_the_database(fresh_database):\n    pass\n")

    result = pytester.runpytest()

    result.assert_outcomes(errors=1)  # and nothing skipped
    # `restart`, not `start` (bug B-072).
    result.stdout.fnmatch_lines(["*Start it with: brew services restart postgresql@18*"])
    assert "not-a-real-password" not in result.stdout.str()
