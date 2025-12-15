"""Tests for configuration settings."""
import os
from unittest.mock import patch

import pytest


@pytest.mark.unit
class TestAISettings:
    """Test AI configuration settings."""

    def test_default_provider_is_demo(self):
        """Default AI provider should be demo."""
        from app.services.ai.config import AIProvider, AISettings

        settings = AISettings()
        assert settings.AI_PROVIDER == AIProvider.DEMO

    def test_provider_from_env(self):
        """Should read provider from environment."""
        with patch.dict(os.environ, {"HELIX_AI_PROVIDER": "groq"}):
            from app.services.ai.config import AISettings
            settings = AISettings()
            assert settings.AI_PROVIDER.value == "groq"

    def test_chaos_disabled_by_default(self):
        """Chaos engineering should be disabled by default."""
        from app.services.ai.config import AISettings

        settings = AISettings()
        assert getattr(settings, "CHAOS_ENABLED", False) is False

    def test_openrouter_model_default(self):
        """Default OpenRouter model should be deepseek-chat."""
        from app.services.ai.config import AISettings

        settings = AISettings()
        assert "deepseek" in settings.OPENROUTER_MODEL.lower()


@pytest.mark.unit
class TestDatabaseSettings:
    """Test database configuration settings."""

    def test_redis_default_host(self):
        """Default Redis host should be localhost."""
        from app.database.core.config import settings

        assert settings.REDIS_HOST in ["localhost", "redis"]

    def test_redis_default_port(self):
        """Default Redis port should be 6379."""
        from app.database.core.config import settings

        assert settings.REDIS_PORT == 6379