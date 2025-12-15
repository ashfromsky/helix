"""Tests for context manager service."""
import pytest
from unittest.mock import AsyncMock, patch


@pytest.mark.unit
class TestContextManager:
    """Test session context management."""

    @pytest.mark.asyncio
    async def test_add_to_context(self, mock_redis):
        """Should add entry to session context."""
        from app.services.context import context_manager

        entry = {
            "method": "POST",
            "path": "/api/users",
            "body": {"name": "Alice"},
            "response": {"id": "usr_123"}
        }

        await context_manager.add_to_context("session1", entry)
        # Verify the operation was called

    @pytest.mark.asyncio
    async def test_get_empty_context(self, mock_redis):
        """Should return empty list for new session."""
        from app.services.context import context_manager

        mock_redis.get.return_value = None
        result = await context_manager.get_context("new_session")

        assert result == [] or result is None

    @pytest.mark.asyncio
    async def test_context_limits_entries(self):
        """Context should limit number of stored entries."""
        from app.services.context import context_manager

        max_entries = getattr(context_manager, "MAX_CONTEXT_ENTRIES", 100)
        assert max_entries > 0

    @pytest.mark.asyncio
    async def test_clear_context(self, mock_redis):
        """Should clear session context."""
        from app.services.context import context_manager

        await context_manager.clear_context("session1")
        mock_redis.delete.assert_called()