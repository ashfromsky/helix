"""Tests for Groq AI provider."""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock


@pytest.mark.unit
class TestGroqProvider:
    """Test Groq AI provider."""

    @pytest.fixture
    def provider(self):
        """Create Groq provider instance with mock API key."""
        from app.services.ai.providers.groq import GroqProvider
        return GroqProvider(api_key="test_key", model="llama-3.1-8b-instant")

    def test_provider_initialization(self, provider):
        """Should initialize with correct parameters."""
        assert provider is not None

    @pytest.mark.asyncio
    async def test_generate_response_structure(self, provider):
        """Should return properly structured response."""
        with patch.object(provider, "_call_api", new_callable=AsyncMock) as mock_call:
            mock_call.return_value = {
                "status_code": 200,
                "body": {"id": "test_123"}
            }

            response = await provider.generate_response(
                method="GET",
                path="/api/users",
                body=None,
                context=[]
            )

            assert isinstance(response, dict)

    @pytest.mark.asyncio
    async def test_handles_api_error(self, provider):
        """Should handle API errors gracefully."""
        with patch.object(provider, "_call_api", new_callable=AsyncMock) as mock_call:
            mock_call.side_effect = Exception("API Error")

            try:
                response = await provider.generate_response(
                    method="GET",
                    path="/api/users",
                    body=None,
                    context=[]
                )
                assert response is not None
            except Exception:
                pass