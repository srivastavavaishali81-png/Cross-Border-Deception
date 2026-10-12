"""
OZARK Backend — FastAPI Application Entry Point
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup → yield → shutdown."""
    setup_logging()
    # TODO: Initialize database connection pools here
    # await postgres.connect()
    # await neo4j_driver.verify_connectivity()
    yield
    # TODO: Close connections on shutdown
    # await postgres.disconnect()
    # await neo4j_driver.close()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="OZARK — Intelligent Data Platform API",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # ── CORS ──────────────────────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Routers ───────────────────────────────────────────────────────────────
    app.include_router(api_router, prefix="/api/v1")
    from app.api.v1.endpoints.companies import router as companies_router
    from app.api.v1.endpoints.network import router as network_router
    # Mount directly for root access: /companies..., /network/{company_id}, /api/network/{company_id}
    app.include_router(companies_router)
    app.include_router(network_router)
    app.include_router(network_router, prefix="/api")

    @app.get("/health", tags=["health"])
    async def health_check():
        return {"status": "ok", "version": settings.APP_VERSION}

    return app


app = create_app()
