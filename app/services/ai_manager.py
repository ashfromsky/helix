import logging

logger = logging.getLogger(__name__)

class AIManager:
    def __init__(self):
        self.is_initialized = True
        self.provider = "OpenAI (Mock)"
        logger.info("AIManager service initialized")

    def generate_response(self, prompt: str) -> str:
        return f"Mock response for: {prompt}"

    def get_status(self) -> dict:
        return {
            "initialized": self.is_initialized,
            "provider": self.provider,
            "status": "operational" if self.is_initialized else "error"
        }

ai_manager = AIManager()