"""One error shape for every reply that is not a success, replacing FastAPI's default `detail`:

    {"error": {"code": "invalid_filter", "message": "from is not a date (YYYY-MM-DD)."}}

Messages are fixed text written here. They name a field, never the value sent, because a value sent
by a client is untrusted and an echo of it is how reflected attacks start.
"""

from __future__ import annotations

import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

log = logging.getLogger(__name__)


class ApiError(Exception):
    """A refusal with its status, code and fixed message, raised anywhere in the API."""

    def __init__(self, status: int, code: str, message: str) -> None:
        super().__init__(message)
        self.status = status
        self.code = code
        self.message = message


def reply(status: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(status_code=status, content={"error": {"code": code, "message": message}})


async def _api_error(request: Request, error: Exception) -> JSONResponse:
    assert isinstance(error, ApiError)
    return reply(error.status, error.code, error.message)


async def _validation_error(request: Request, error: Exception) -> JSONResponse:
    """FastAPI's own checks failed. Its default reply copies the value sent into `input`, so this
    one sends fixed text. The filters are checked in `filters.py` and never reach here."""
    assert isinstance(error, RequestValidationError)
    return reply(422, "invalid_request", "The request is not valid.")


# Statuses raised by the framework itself, such as an unknown path. Any other gets a general code.
HTTP_ERRORS = {
    404: ("not_found", "Not found."),
    405: ("method_not_allowed", "This method is not allowed here."),
}


async def _http_error(request: Request, error: Exception) -> JSONResponse:
    assert isinstance(error, StarletteHTTPException)
    code, message = HTTP_ERRORS.get(error.status_code, ("http_error", "The request failed."))
    return reply(error.status_code, code, message)


async def _unexpected_error(request: Request, error: Exception) -> JSONResponse:
    """Anything not foreseen. The exception's text may hold paths or secrets: it is logged here,
    on the server, and the client gets fixed text."""
    log.exception("Unexpected error on %s %s", request.method, request.url.path, exc_info=error)
    return reply(500, "internal_error", "The server hit an unexpected error.")


def install(app: FastAPI) -> None:
    app.add_exception_handler(ApiError, _api_error)
    app.add_exception_handler(RequestValidationError, _validation_error)
    app.add_exception_handler(StarletteHTTPException, _http_error)
    app.add_exception_handler(Exception, _unexpected_error)
