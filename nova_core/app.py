"""FastAPI application factory for NovaCore."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .config import settings
from .observability import configure_tracing
from .routing import attach_routers
from .state import state

LOGGER = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown events."""

    configure_tracing()
    if settings.kill_switch:
        state.engage_kill_switch()
        LOGGER.warning("Kill switch engaged from initial settings")
    LOGGER.info("NovaCore service starting in %s mode", settings.mode)
    yield
    LOGGER.info("NovaCore service shutdown")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""

    app = FastAPI(
        title="NovaCore",
        version="0.1.0",
        description="Orchestrator API for Nova Enterprises subsystems.",
        lifespan=lifespan,
    )
    attach_routers(app)
    return app


app = create_app()
"""FastAPI application instance for ASGI servers."""
