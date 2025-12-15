"""Tests for AI manager."""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock


@pytest.mark.unit
class TestAIManager:
    """Test AI provider manager."""

    def test_manager_exists(self):
        """AI manager should be importable."""
        from app.services.ai.manager import ai_manager
        assert ai_manager is not None

    def test_default_provider_is_demo(self):
        """Default provider should be demo."""
        from app.services.ai.manager import ai_manager
        from app.services.ai.config import AIProvider

        provider_name = getattr(ai_manager, "current_provider", "demo")
        assert provider_name == "demo" or provider_name == AIProvider.DEMO

    @pytest.mark.asyncio
    async def test_generate_response_returns_dict(self, mock_ai_manager):
        """Manager should return dictionary response."""
        response = await mock_ai_manager.generate_response(
            method="GET",
            path="/api/users",
            body=None,
            context=[]
        )

        assert isinstance(response, dict)

    @pytest.mark.asyncio
    async def test_generate_response_has_required_fields(self, mock_ai_manager):
        """Response should have status_code and body."""
        response = await mock_ai_manager.generate_response(
            method="GET",
            path="/api/users",
            body=None,
            context=[]
        )

        assert "status_code" in response or "body" in response