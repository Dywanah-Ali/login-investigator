"""The FastAPI app. Run it from `backend/` with:

    uv run uvicorn api.app:create_app --factory --port 8000
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api import dashboard_routes, errors, investigation_routes
from api.services import start
from api.settings import Settings


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings.from_env()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        app.state.services = start(settings)
        yield
        app.state.services.memory.conn.close()

    app = FastAPI(title="Login Investigator", lifespan=lifespan)
    errors.install(app)
    app.include_router(dashboard_routes.router, prefix="/api")
    app.include_router(investigation_routes.router, prefix="/api")
    return app
