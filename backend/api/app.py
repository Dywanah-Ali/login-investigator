"""The FastAPI app. Run it from `backend/` with:

    uv run uvicorn api.app:create_app --factory --port 8000
"""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api import dashboard_routes, errors, investigation_routes
from api.services import start, stop
from api.settings import Settings
from login_investigator import knowledge_base

log = logging.getLogger(__name__)


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings.from_env()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        # The staleness guard (knowledge-base T18) runs before anything else starts. A stale or
        # uncheckable build raises fixed text here, so the server never starts and no endpoint
        # answers. With nothing built, the app runs without a knowledge base: the marker is None,
        # otherwise the checked database's name, for the knowledge-base tools to come.
        app.state.knowledge_base = await knowledge_base.check_knowledge_base(
            settings.dataset_dir, settings.knowledge_base_state)
        if app.state.knowledge_base is None:
            log.warning(knowledge_base.NOT_BUILT)
        app.state.services = start(settings)
        yield
        stop(app.state.services)

    app = FastAPI(title="Login Investigator", lifespan=lifespan)
    errors.install(app)
    app.include_router(dashboard_routes.router, prefix="/api")
    app.include_router(investigation_routes.router, prefix="/api")
    return app
