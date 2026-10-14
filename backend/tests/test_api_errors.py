"""Every reply that is not a success has the one error shape, whatever the status (ticket 12)."""

import pytest
from fastapi.testclient import TestClient

from api.app import create_app
from api.settings import Settings

SECRET = "sk-or-v1-0000-must-never-leave-the-server"


@pytest.fixture(scope="module")
def client(tmp_path_factory):
    app = create_app(Settings.from_env(
        {"LI_MEMORY_PATH": str(tmp_path_factory.mktemp("memory") / "m.sqlite")}))

    def crash():
        raise RuntimeError(f"an exception whose text holds {SECRET}")

    # A route of the test's own, to see what any unexpected failure looks like from outside.
    app.add_api_route("/api/test-crash", crash)
    # The test client would re-raise the crash; a real server answers 500 instead.
    with TestClient(app, raise_server_exceptions=False) as client:
        yield client


def test_an_unknown_path_is_not_found_in_the_one_shape(client):
    reply = client.get("/api/no-such-thing")
    assert reply.status_code == 404
    assert reply.json() == {"error": {"code": "not_found", "message": "Not found."}}


def test_a_wrong_method_is_refused_in_the_one_shape(client):
    reply = client.post("/api/overview")
    assert reply.status_code == 405
    assert reply.json() == {
        "error": {"code": "method_not_allowed", "message": "This method is not allowed here."}}


def test_an_unexpected_failure_hides_the_exception_text(client):
    """As in v1: the exception's own text is logged on the server and never sent."""
    reply = client.get("/api/test-crash")
    assert reply.status_code == 500
    assert reply.json() == {
        "error": {"code": "internal_error", "message": "The server hit an unexpected error."}}
    assert SECRET not in reply.text
