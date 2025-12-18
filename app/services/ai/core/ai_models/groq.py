from typing import Any, Dict, Optional

import httpx

from ..config import ai_settings
from .base import BaseAIProvider


class GroqProvider(BaseAIProvider):
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.groq.com/openai/v1"

    async def generate_response(
        self, method: str, path: str, body: Optional[Dict] = None, context: Optional[list] = None
    ) -> Dict[str, Any]:
        prompt = self._build_prompt(method, path, body, context)

        async with httpx.AsyncClient(timeout=ai_settings.AI_TIMEOUT) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": self._get_system_prompt()},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": ai_settings.AI_TEMPERATURE,
                    "max_tokens": ai_settings.AI_MAX_TOKENS,
                },
            )
            response.raise_for_status()

            ai_text = response.json()["choices"][0]["message"]["content"]
            return self._parse_ai_response(ai_text)

    def _get_system_prompt(self) -> str:
        with open("assets/AI/MOCKPILOT_SYSTEM.md", "r") as f:
            return f.read()

    def _build_prompt(self, method, path, body, context) -> str:
        prompt = f"Method: {method}\nPath: {path}\n"
        if body:
            prompt += f"Body: {body}\n"
        if context:
            prompt += f"Context: {context}\n"
        return prompt

    def _parse_ai_response(self, text: str) -> Dict:
        import json
        import re

        json_match = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1))

        return json.loads(text)
