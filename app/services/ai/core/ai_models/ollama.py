from typing import Any, Dict, Optional

import httpx

from .base import BaseAIProvider


class OllamaProvider(BaseAIProvider):
    def __init__(self, host: str, model: str):
        self.host = host
        self.model = model

    async def generate_response(
        self, method: str, path: str, body: Optional[Dict] = None, context: Optional[list] = None
    ) -> Dict[str, Any]:
        pass
