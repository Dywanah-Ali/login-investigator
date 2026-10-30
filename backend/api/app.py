"""The FastAPI app. Run it from `backend/` with:

    uv run uvicorn api.app:create_app --factory --port 8000
"""

from __future__ import annotations

import logging
import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import replace

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
        started = time.monotonic()
        async with knowledge_base.open_current_knowledge_base(
            settings.dataset_dir, settings.knowledge_base_state,
        ) as kb:
            app.state.knowledge_base = kb
            if kb is None:
                log.warning(knowledge_base.NOT_BUILT)
            else:
                log.info("Knowledge-base preparation completed in %.3f seconds",
                         time.monotonic() - started)
            selected_settings = (replace(settings, dataset_dir=kb.source_snapshot)
                                 if kb is not None and kb.source_snapshot is not None else settings)
            app.state.services = start(selected_settings, kb)
            try:
                yield
            finally:
                stop(app.state.services)

    app = FastAPI(title="Login Investigator", lifespan=lifespan)
    errors.install(app)
    app.include_router(dashboard_routes.router, prefix="/api")
    app.include_router(investigation_routes.router, prefix="/api")
    return app
