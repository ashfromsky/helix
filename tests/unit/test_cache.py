"""Tests for cache service."""
import pytest
from unittest.mock import AsyncMock, patch


@pytest.mark.unit
class TestCacheService:
    """Test caching functionality."""

    @pytest.mark.asyncio
    async def test_cache_key_generation(self):
        """Should generate consistent cache keys."""
        from app.services.cache import cache_service

        key1 = cache_service.generate_key("session1", "GET", "/api/users", None)
        key2 = cache_service.generate_key("session1", "GET", "/api/users", None)

        assert key1 == key2

    @pytest.mark.asyncio
    async def test_cache_key_differs_by_session(self):
        """Different sessions should have different cache keys."""
        from app.services.cache import cache_service

        key1 = cache_service.generate_key("session1", "GET", "/api/users", None)
        key2 = cache_service.generate_key("session2", "GET", "/api/users", None)

        assert key1 != key2

    @pytest.mark.asyncio
    async def test_cache_key_differs_by_method(self):
        """Different methods should have different cache keys."""
        from app.services.cache import cache_service

        key1 = cache_service.generate_key("session1", "GET", "/api/users", None)
        key2 = cache_service.generate_key("session1", "POST", "/api/users", None)

        assert key1 != key2

    @pytest.mark.asyncio
    async def test_cache_key_includes_body_hash(self):
        """Cache key should include body hash for POST requests."""
        from app.services.cache import cache_service

        body1 = {"name": "Alice"}
        body2 = {"name": "Bob"}

        key1 = cache_service.generate_key("session1", "POST", "/api/users", body1)
        key2 = cache_service.generate_key("session1", "POST", "/api/users", body2)

        assert key1 != key2

    @pytest.mark.asyncio
    async def test_cache_get_returns_none_on_miss(self, mock_redis):
        """Should return None on cache miss."""
        from app.services.cache import cache_service

        mock_redis.get.return_value = None
        result = await cache_service.get("nonexistent_key")

        assert result is None

    @pytest.mark.asyncio
    async def test_cache_set_with_ttl(self, mock_redis):
        """Should set cache with TTL."""
        from app.services.cache import cache_service

        await cache_service.set("test_key", {"data": "value"}, ttl=3600)

        mock_redis.set.assert_called_once()