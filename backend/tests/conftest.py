"""
OZARK Backend — Pytest Root Config

Place shared fixtures and plugins here.
"""

import sys
from pathlib import Path

# Ensure backend directory and root are in sys.path
backend_dir = Path(__file__).parent.parent
root_dir = backend_dir.parent
sys.path.insert(0, str(backend_dir))
sys.path.insert(0, str(root_dir))

from collections.abc import AsyncGenerator
import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Async HTTP test client wrapping the FastAPI app."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
