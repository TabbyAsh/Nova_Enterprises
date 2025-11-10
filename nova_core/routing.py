"""Router registration and common endpoints for NovaCore."""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, FastAPI, HTTPException, status
from fastapi.responses import PlainTextResponse
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from .config import settings
from .state import state

LOGGER = logging.getLogger(__name__)


def create_root_router() -> APIRouter:
    """Create the root API router with operational endpoints."""

    router = APIRouter()

    @router.get("/ops/health", summary="Readiness health check")
    async def health() -> dict[str, Any]:
        """Return readiness information for the service."""

        return {
            "status": "ok",
            "kill_switch": state.kill_switch,
            "environment": settings.app_env.value,
        }

    @router.post(
        "/ops/kill",
        summary="Toggle the global kill switch",
        status_code=status.HTTP_202_ACCEPTED,
    )
    async def toggle_kill_switch(payload: dict[str, Any]) -> dict[str, Any]:
        """Engage or disengage the kill switch based on the payload."""

        if "enabled" not in payload:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Request payload must include an 'enabled' field.",
            )
        enabled = bool(payload["enabled"])
        if enabled:
            state.engage_kill_switch()
            LOGGER.warning("Kill switch engaged via API request")
        else:
            state.disengage_kill_switch()
            LOGGER.info("Kill switch disengaged via API request")
        return {
            "kill_switch": state.kill_switch,
            "updated_at": state.kill_switch_updated_at,
        }

    @router.get("/metrics", summary="Prometheus metrics endpoint")
    async def metrics() -> PlainTextResponse:
        """Expose Prometheus metrics for scraping."""

        payload = generate_latest()  # type: ignore[arg-type]
        return PlainTextResponse(content=payload.decode(), media_type=CONTENT_TYPE_LATEST)

    return router


def attach_routers(app: FastAPI) -> None:
    """Attach root and subsystem routers to the FastAPI application."""

    root_router = create_root_router()
    app.include_router(root_router)

    # Stubs for future subsystem routers.
    app.include_router(APIRouter(), prefix="/trade", tags=["trade"])
    app.include_router(APIRouter(), prefix="/ops", tags=["ops"])
    app.include_router(APIRouter(), prefix="/store", tags=["store"])
    app.include_router(APIRouter(), prefix="/social", tags=["social"])
