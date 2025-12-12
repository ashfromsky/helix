from app.services.ai.core.config import ai_settings
from app.services.ai.providers.deepseek import DeepSeekProvider
from app.services.ai.providers.ollama import OllamaProvider
from app.services.ai.providers.groq import GroqProvider
from app.services.ai.providers.demo import DemoProvider # Fallback

class AIManager:
    def __init__(self):
        self.provider_name = ai_settings.AI_PROVIDER # "deepseek", "ollama", etc.
        self.provider = self._get_provider()

    def _get_provider(self):
        if self.provider_name == "deepseek":
            return DeepSeekProvider()
        elif self.provider_name == "ollama":
            return OllamaProvider()
        elif self.provider_name == "groq":
            return GroqProvider()
        else:
            return DemoProvider()

    async def generate(self, system: str, user: str) -> str:
        return await self.provider.generate_code(system, user)

ai_manager = AIManager()