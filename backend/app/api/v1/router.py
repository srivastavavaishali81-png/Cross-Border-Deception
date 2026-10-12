"""
OZARK Backend — API v1 Router
"""

from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.companies import router as companies_router
from app.api.v1.endpoints.network import router as network_router

api_router = APIRouter()

# ── Health (internal) ─────────────────────────────────────────────────────────
@api_router.get("/ping", tags=["health"])
async def ping():
    """Simple liveness probe."""
    return {"ping": "pong"}


# ── Auth ──────────────────────────────────────────────────────────────────────
api_router.include_router(auth_router)

# ── Companies ─────────────────────────────────────────────────────────────────
api_router.include_router(companies_router)

# ── Network Graph ─────────────────────────────────────────────────────────────
api_router.include_router(network_router)

