"""
Groq AI Provider
Ultra-fast LLM inference using Groq's LPU
Free tier: 14,400 requests/day
"""

import httpx
from typing import Dict, Any, Optional
import logging
from .base import BaseAIProvider
from ..config import ai_settings

logger = logging.getLogger(__name__)


class GroqProvider(BaseAIProvider):
    """
    Groq provider for fast AI inference

    Setup:
    1. Sign up at https://console.groq.com/
    2. Get API key from dashboard
    3. Set HELIX_GROQ_API_KEY in .env

    Models available:
    - llama-3.1-70b-versatile (recommended)
    - llama-3.1-8b-instant (faster, less capable)
    - mixtral-8x7b-32768
    - gemma2-9b-it
    """

    def __init__(self, api_key: str, model: str = "llama-3.1-70b-versatile"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.groq.com/openai/v1"
        self.timeout = ai_settings.AI_TIMEOUT

    async def generate_response(
        self,
        method: str,
        path: str,
        body: Optional[Dict] = None,
        context: Optional[list] = None,
        system_prompt: str = None,
    ) -> Dict[str, Any]:
        """
        Generate response using Groq's fast inference
        """
        try:
            if system_prompt is None:
                sys_prompt_content = self._get_system_prompt()
            else:
                sys_prompt_content = system_prompt

            user_prompt = self._build_user_prompt(method, path, body, context)

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                    json={
                        "model": self.model,
                        "messages": [
                            {"role": "system", "content": sys_prompt_content},
                            {"role": "user", "content": user_prompt},
                        ],
                        "temperature": ai_settings.AI_TEMPERATURE,
                        "max_tokens": ai_settings.AI_MAX_TOKENS,
                        "response_format": {"type": "json_object"},  # Force JSON output
                    },
                )

                response.raise_for_status()
                data = response.json()

                # Extract AI response text
                ai_text = data["choices"][0]["message"]["content"]

                # Parse JSON from response
                parsed = self._parse_ai_response(ai_text)

                # Validate and return
                return self._validate_response(parsed)

        except httpx.HTTPStatusError as e:
            logger.error(f"Groq API error: {e.response.status_code} - {e.response.text}")

            if e.response.status_code == 401:
                raise Exception("Invalid Groq API key. Get one at: https://console.groq.com/")
            elif e.response.status_code == 429:
                raise Exception("Groq rate limit exceeded. Free tier: 14,400 requests/day")
            elif e.response.status_code == 400:
                error_data = e.response.json()
                raise Exception(f"Groq API error: {error_data.get('error', {}).get('message', 'Bad request')}")
            else:
                raise Exception(f"Groq API error: {e.response.status_code}")

        except httpx.TimeoutException:
            logger.error("Groq API timeout")
            raise Exception("Groq API timeout - request took too long")

        except Exception as e:
            logger.error(f"Groq provider error: {str(e)}")
            raise

    def _parse_ai_response(self, text: str) -> Dict[str, Any]:
        """
        Override parent method to handle Groq-specific response format
        """
        import json

        # Groq with json_object mode returns clean JSON
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Fallback to parent's robust parsing
            return super()._parse_ai_response(text)

    async def check_health(self) -> bool:
        """
        Check if Groq API is accessible
        """
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get(
                    f"{self.base_url}/models", headers={"Authorization": f"Bearer {self.api_key}"}
                )
                return response.status_code == 200
        except Exception:
            return False

    async def list_models(self) -> list:
        """
        List available Groq models
        """
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get(
                    f"{self.base_url}/models", headers={"Authorization": f"Bearer {self.api_key}"}
                )
                response.raise_for_status()

                models = response.json().get("data", [])
                return [
                    {"id": m.get("id"), "owned_by": m.get("owned_by"), "context_window": m.get("context_window")}
                    for m in models
                ]
        except Exception:
            return []

    def get_info(self) -> Dict[str, Any]:
        """
        Get provider information
        """
        return {
            "provider": "groq",
            "model": self.model,
            "api": "Groq",
            "base_url": self.base_url,
            "free_tier": "14,400 requests/day",
            "speed": "ultra-fast (LPU)",
            "docs": "https://console.groq.com/docs",
        }

    def get_available_models(self) -> list:
        """
        Get list of recommended Groq models
        """
        return [
            {
                "id": "llama-3.1-70b-versatile",
                "name": "Llama 3.1 70B",
                "context": "128K tokens",
                "speed": "fast",
                "recommended": True,
            },
            {
                "id": "llama-3.1-8b-instant",
                "name": "Llama 3.1 8B",
                "context": "128K tokens",
                "speed": "ultra-fast",
                "recommended": False,
            },
            {
                "id": "mixtral-8x7b-32768",
                "name": "Mixtral 8x7B",
                "context": "32K tokens",
                "speed": "fast",
                "recommended": False,
            },
            {
                "id": "gemma2-9b-it",
                "name": "Gemma 2 9B",
                "context": "8K tokens",
                "speed": "ultra-fast",
                "recommended": False,
            },
        ]
