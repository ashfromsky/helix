"""
Pytest configuration and fixtures for Helix tests.
"""
import asyncio
import os
from typing import AsyncGenerator, Generator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from faker import Faker
from fastapi.testclient import TestClient
from httpx import AsyncClient

os.environ["HELIX_AI_PROVIDER"] = "demo"
os.environ["HELIX_REDIS_HOST"] = "localhost"
os.environ["HELIX_REDIS_PORT"] = "6379"
os.environ["HELIX_CHAOS_ENABLED"] = "false"

from app.main import app



@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio. get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()



@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Synchronous test client."""
    with TestClient(app) as c:
        yield c


@pytest. fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Asynchronous test client."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac



@pytest.fixture
def fake() -> Faker:
    """Faker instance for generating test data."""
    return Faker()


@pytest.fixture
def sample_user(fake: Faker) -> dict:
    """Generate a sample user payload."""
    return {
        "name": fake.name(),
        "email": fake.email(),
        "username": fake.user_name(),
        "role": "developer"
    }


@pytest.fixture
def sample_product(fake: Faker) -> dict:
    """Generate a sample product payload."""
    return {
        "name": fake.word().capitalize(),
        "description": fake.sentence(),
        "price": round(fake.pyfloat(min_value=10, max_value=1000), 2),
        "sku": fake.bothify(text="SKU-???? -####"),
        "category": fake. word()
    }


@pytest.fixture
def sample_order(fake:  Faker) -> dict:
    """Generate a sample order payload."""
    return {
        "customer_id": f"cust_{fake.uuid4()[:8]}",
        "items": [
            {"product_id": f"prod_{fake.uuid4()[:8]}", "quantity": fake.random_int(1, 5)}
        ],
        "shipping_address": {
            "street": fake.street_address(),
            "city": fake.city(),
            "country": fake.country()
        }
    }



@pytest.fixture
def mock_redis():
    """Mock Redis client."""
    with patch("app.database.core.connect. redis_client") as mock:
        mock.ping = AsyncMock(return_value=True)
        mock.get = AsyncMock(return_value=None)
        mock.set = AsyncMock(return_value=True)
        mock.delete = AsyncMock(return_value=True)
        mock.keys = AsyncMock(return_value=[])
        yield mock


@pytest.fixture
def mock_ai_manager():
    """Mock AI manager."""
    with patch("app.services.ai. manager.ai_manager") as mock:
        mock.generate_response = AsyncMock(return_value={
            "status_code": 200,
            "headers": {"Content-Type": "application/json"},
            "body": {"id": "test_123", "message": "success"}
        })
        yield mock


@pytest.fixture
def mock_cache_service():
    """Mock cache service."""
    with patch("app.services.cache.cache_service") as mock:
        mock.get = AsyncMock(return_value=None)
        mock.set = AsyncMock(return_value=True)
        mock.delete = AsyncMock(return_value=True)
        yield mock


@pytest.fixture
def mock_context_manager():
    """Mock context manager."""
    with patch("app. services.context. context_manager") as mock:
        mock.get_context = AsyncMock(return_value=[])
        mock.add_to_context = AsyncMock(return_value=True)
        mock.clear_context = AsyncMock(return_value=True)
        yield mock



@pytest.fixture
def session_id(fake: Faker) -> str:
    """Generate a unique session ID."""
    return f"test-session-{fake.uuid4()[:8]}"


@pytest.fixture
def auth_headers(session_id: str) -> dict:
    """Headers with session ID."""
    return {
        "X-Session-ID": session_id,
        "Content-Type": "application/json"
    }



@pytest.fixture(autouse=True)
async def cleanup_after_test():
    """Cleanup after each test."""
    yield



def pytest_configure(config):
    """Configure custom markers."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "performance: Performance tests")
    config.addinivalue_line("markers", "slow: Slow running tests")