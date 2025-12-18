"""
DeepSeek AI Provider via OpenRouter
Uses DeepSeek models through OpenRouter API
Free tier: ~500 requests/day
"""

import logging
from typing import Any, Dict, Optional

import httpx

from ..config import ai_settings
from .base import BaseAIProvider

logger = logging.getLogger(__name__)


class DeepSeekProvider(BaseAIProvider):
    """
    DeepSeek provider using OpenRouter API

    Setup:
    1. Sign up at https://openrouter.ai/
    2. Get API key from dashboard
    3. Set HELIX_OPENROUTER_API_KEY in .env
    """

    def __init__(self, api_key: str, model: str = "deepseek/deepseek-chat"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://openrouter.ai/api/v1"
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
        Generate response using DeepSeek via OpenRouter
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
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://github.com/helix",
                        "X-Title": "Helix Mock Server",
                    },
                    json={
                        "model": self.model,
                        "messages": [
                            {"role": "system", "content": sys_prompt_content},
                            {"role": "user", "content": user_prompt},
                        ],
                        "temperature": ai_settings.AI_TEMPERATURE,
                        "max_tokens": ai_settings.AI_MAX_TOKENS,
                        "response_format": {"type": "json_object"},
                    },
                )

                response.raise_for_status()
                data = response.json()

                ai_text = data["choices"][0]["message"]["content"]

                parsed = self._parse_ai_response(ai_text)

                return self._validate_response(parsed)

        except httpx.HTTPStatusError as e:
            logger.error(f"OpenRouter API error: {e.response.status_code} - {e.response.text}")
            raise Exception(f"OpenRouter API error: {e.response.status_code}")

        except httpx.TimeoutException:
            logger.error("OpenRouter API timeout")
            raise Exception("OpenRouter API timeout - request took too long")

        except Exception as e:
            logger.error(f"DeepSeek provider error: {str(e)}")
            raise

    def _parse_ai_response(self, text: str) -> Dict[str, Any]:
        """
        Override parent method to handle OpenRouter-specific response format
        """
        import json

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return super()._parse_ai_response(text)

    async def check_health(self) -> bool:
        """
        Check if OpenRouter API is accessible
        """
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get(
                    f"{self.base_url}/models", headers={"Authorization": f"Bearer {self.api_key}"}
                )
                return response.status_code == 200
        except Exception:
            return False

    def get_info(self) -> Dict[str, Any]:
        """
        Get provider information
        """
        return {
            "provider": "deepseek",
            "model": self.model,
            "api": "OpenRouter",
            "base_url": self.base_url,
            "free_tier": "~500 requests/day",
            "docs": "https://openrouter.ai/docs",
        }
