from typing import List, Dict
from app.services.cache import cache_service


class ContextManager:
    async def get_context(self, session_id: str, limit: int = 5) -> List[Dict]:
        """Get last N requests from session"""
        key = f"context:{session_id}"
        context = await cache_service.get(key)
        return context[-limit:] if context else []

    async def add_to_context(self, session_id: str, request_data: Dict):
        """Add request to context history"""
        key = f"context:{session_id}"
        context = await cache_service.get(key) or []
        context.append(request_data)
        await cache_service.set(key, context, ttl=3600)


context_manager = ContextManager()
