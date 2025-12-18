import logging
from app.services.ai.config import ai_settings
from app.services.ai.providers.deepseek import DeepSeekProvider
from app.services.ai.providers.ollama import OllamaProvider
from app.services.ai.providers.groq import GroqProvider
from app.services.ai.providers.demo import DemoProvider

logger = logging.getLogger(__name__)


class AIManager:
    def __init__(self):
        self.provider_name = ai_settings.AI_PROVIDER
        self.provider = self._get_provider()

    def _get_provider(self):
        try:
            if self.provider_name == "deepseek":
                if not ai_settings.OPENROUTER_API_KEY:
                    logger.warning("DeepSeek key missing. Falling back to DEMO.")
                    return DemoProvider()
                return DeepSeekProvider(api_key=ai_settings.OPENROUTER_API_KEY, model=ai_settings.OPENROUTER_MODEL)

            elif self.provider_name == "ollama":
                return OllamaProvider(host=ai_settings.OLLAMA_HOST, model=ai_settings.OLLAMA_MODEL)

            elif self.provider_name == "groq":
                if not ai_settings.GROQ_API_KEY:
                    logger.warning("Groq key missing. Falling back to DEMO.")
                    return DemoProvider()
                return GroqProvider(api_key=ai_settings.GROQ_API_KEY, model=ai_settings.GROQ_MODEL)

            else:
                return DemoProvider()

        except Exception as e:
            logger.error(f"Failed to init provider {self.provider_name}: {e}")
            return DemoProvider()

    async def generate_response(
        self, method: str, path: str, body: dict = None, context: list = None, system_prompt: str = None
    ) -> dict:
        return await self.provider.generate_response(method, path, body, context, system_prompt=system_prompt)

    def get_status(self) -> dict:
        """
        Returns the current status of the AI provider.
        Used by /health and /status endpoints.
        """
        return {
            "provider": self.provider_name,
            "model": getattr(self.provider, "model", "template-based"),
            "status": "active",
        }


ai_manager = AIManager()
