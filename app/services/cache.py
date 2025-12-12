from app.database.core.connect import get_redis_connection
import json
import hashlib
import logging

logger = logging.getLogger(__name__)

class CacheService:
    def __init__(self):
        self.redis = get_redis_connection()

    def get_cache_key(self, session_id: str, method: str, path: str, body: dict = None):
        body_hash = hashlib.md5(json.dumps(body or {}).encode()).hexdigest()
        return f"{session_id}:{method}:{path}:{body_hash}"

    async def get(self, key: str):
        try:
            data = self.redis.get(key)
            return json.loads(data) if data else None
        except Exception as e:
            logger.warning(f"⚠️ Redis is unavailable: {e}")
            return None

    async def set(self, key: str, value: dict, ttl: int = 86400):
        try:
            self.redis.setex(key, ttl, json.dumps(value))
        except Exception as e:
            logger.warning(f"⚠️ Could not write to Redis: {e}")

    async def delete(self, key: str):
        try:
            self.redis.delete(key)
        except Exception:
            pass

cache_service = CacheService()