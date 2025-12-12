from .config import ai_settings, AIProvider
from .providers.demo import DemoProvider
from .providers.deepseek import DeepSeekProvider
from .providers.ollama import OllamaProvider
from .providers.groq import GroqProvider
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class AIManager:
    """
    AI Manager - orchestrates AI providers
    Handles fallback logic and provider initialization
    """

    def __init__(self):
        self.provider = self._initialize_provider()
        self.demo_provider = DemoProvider()

    def _initialize_provider(self):
        """Initialize AI provider based on settings"""
        provider_type = ai_settings.AI_PROVIDER

        try:
            if provider_type == AIProvider.DEEPSEEK:
                if not ai_settings.OPENROUTER_API_KEY:
                    logger.warning(
                        "DeepSeek selected but HELIX_OPENROUTER_API_KEY not set. "
                        "Falling back to DEMO mode. "
                        "Get free key at: https://openrouter.ai/"
                    )
                    return DemoProvider()

                logger.info("Using DeepSeek via OpenRouter")
                return DeepSeekProvider(
                    api_key=ai_settings.OPENROUTER_API_KEY,
                    model=ai_settings.OPENROUTER_MODEL
                )

            elif provider_type == AIProvider.OLLAMA:
                logger.info(f"Using Ollama at {ai_settings.OLLAMA_HOST}")
                return OllamaProvider(
                    host=ai_settings.OLLAMA_HOST,
                    model=ai_settings.OLLAMA_MODEL
                )

            elif provider_type == AIProvider.GROQ:
                if not ai_settings.GROQ_API_KEY:
                    logger.warning(
                        "Groq selected but HELIX_GROQ_API_KEY not set. "
                        "Falling back to DEMO mode."
                    )
                    return DemoProvider()

                logger.info("Using Groq")
                return GroqProvider(
                    api_key=ai_settings.GROQ_API_KEY,
                    model=ai_settings.GROQ_MODEL
                )

            else:  # DEMO
                logger.info("Using DEMO mode (template-based responses)")
                return DemoProvider()

        except Exception as e:
            logger.error(f"Failed to initialize {provider_type}: {e}")
            logger.info("Falling back to DEMO mode")
            return DemoProvider()

    async def generate_response(
            self,
            method: str,
            path: str,
            body: Optional[Dict] = None,
            context: Optional[list] = None
    ) -> Dict[str, Any]:
        """Generate API response using configured provider"""
        try:
            return await self.provider.generate_response(
                method=method,
                path=path,
                body=body,
                context=context
            )
        except Exception as e:
            logger.error(f"AI generation failed: {e}")

            if ai_settings.AI_AUTO_FALLBACK:
                logger.info("Using fallback DEMO mode")
                return await self.demo_provider.generate_response(
                    method=method,
                    path=path,
                    body=body,
                    context=context
                )
            else:
                raise

    def get_status(self) -> Dict[str, Any]:
        """Get current AI manager status"""
        return {
            "provider": ai_settings.AI_PROVIDER.value,
            "model": self._get_current_model(),
            "fallback_enabled": ai_settings.AI_AUTO_FALLBACK,
            "available_providers": self._check_available_providers()
        }

    def _get_current_model(self) -> str:
        """Get current model name"""
        if ai_settings.AI_PROVIDER == AIProvider.DEEPSEEK:
            return ai_settings.OPENROUTER_MODEL
        elif ai_settings.AI_PROVIDER == AIProvider.OLLAMA:
            return ai_settings.OLLAMA_MODEL
        elif ai_settings.AI_PROVIDER == AIProvider.GROQ:
            return ai_settings.GROQ_MODEL
        else:
            return "template-based"

    def _check_available_providers(self) -> Dict[str, bool]:
        """Check which providers are available"""
        return {
            "deepseek": bool(ai_settings.OPENROUTER_API_KEY),
            "ollama": self._check_ollama_available(),
            "groq": bool(ai_settings.GROQ_API_KEY),
            "demo": True
        }

    def _check_ollama_available(self) -> bool:
        """Check if Ollama is accessible"""
        import httpx
        try:
            response = httpx.get(f"{ai_settings.OLLAMA_HOST}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False


# Singleton instance
ai_manager = AIManager()