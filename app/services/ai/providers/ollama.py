import httpx
from typing import Dict, Any, Optional
import logging
from .base import BaseAIProvider
from ..config import ai_settings

logger = logging.getLogger(__name__)


class OllamaProvider(BaseAIProvider):
    """
    Ollama provider for local AI models
    """

    def __init__(
            self,
            host: str = "http://localhost:11434",
            model: str = "llama3"
    ):
        self.host = host.rstrip("/")
        self.model = model
        self.timeout = ai_settings.AI_TIMEOUT

    async def generate_response(
            self,
            method: str,
            path: str,
            body: Optional[Dict] = None,
            context: Optional[list] = None,
            system_prompt: str = None
    ) -> Dict[str, Any]:
        """
        Generate response using local Ollama model
        """
        try:
            if system_prompt is None:
                sys_prompt_content = self._get_system_prompt()
            else:
                sys_prompt_content = system_prompt

            user_prompt = self._build_user_prompt(method, path, body, context)

            full_prompt = f"{sys_prompt_content}\n\n{user_prompt}"

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.host}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": full_prompt,
                        "stream": False,
                        "options": {
                            "temperature": ai_settings.AI_TEMPERATURE,
                            "num_predict": ai_settings.AI_MAX_TOKENS
                        },
                        "format": "json"
                    }
                )

                response.raise_for_status()
                data = response.json()

                ai_text = data.get("response", "")

                parsed = self._parse_ai_response(ai_text)

                return self._validate_response(parsed)

        except httpx.ConnectError:
            logger.error(f"Cannot connect to Ollama at {self.host}")
            raise Exception(
                f"Ollama is not running at {self.host}. "
                "Please start Ollama: 'ollama serve'"
            )

        except httpx.HTTPStatusError as e:
            logger.error(f"Ollama API error: {e.response.status_code}")

            if e.response.status_code == 404:
                raise Exception(
                    f"Model '{self.model}' not found. "
                    f"Pull it first: 'ollama pull {self.model}'"
                )
            raise

        except httpx.TimeoutException:
            logger.error("Ollama request timeout")
            raise Exception(
                f"Ollama timeout - model '{self.model}' might be too slow. "
                "Try a smaller model like 'llama3:8b'"
            )

        except Exception as e:
            logger.error(f"Ollama provider error: {str(e)}")
            raise

    async def check_health(self) -> bool:
        """
        Check if Ollama server is running and model is available
        """
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get(f"{self.host}/api/tags")
                if response.status_code != 200:
                    return False

                models = response.json().get("models", [])
                model_names = [m.get("name", "") for m in models]

                model_base = self.model.split(":")[0]
                return any(model_base in name for name in model_names)

        except Exception:
            return False

    async def list_models(self) -> list:
        """
        List available Ollama models
        """
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get(f"{self.host}/api/tags")
                response.raise_for_status()

                models = response.json().get("models", [])
                return [
                    {
                        "name": m.get("name"),
                        "size": m.get("size"),
                        "modified": m.get("modified_at")
                    }
                    for m in models
                ]
        except Exception:
            return []

    def get_info(self) -> Dict[str, Any]:
        """
        Get provider information
        """
        return {
            "provider": "ollama",
            "model": self.model,
            "host": self.host,
            "type": "local",
            "free": True,
            "offline": True,
            "docs": "https://ollama.com/library"
        }

    async def pull_model(self, model_name: str) -> bool:
        """
        Pull/download a model (if Ollama supports it via API)
        """
        try:
            async with httpx.AsyncClient(timeout=300) as client:
                response = await client.post(
                    f"{self.host}/api/pull",
                    json={"name": model_name}
                )
                return response.status_code == 200
        except Exception:
            return False