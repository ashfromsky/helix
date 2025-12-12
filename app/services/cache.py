from app.database.core.connect import get_redis_connection
import json
import hashlib


class CacheService:
    def __init__(self):
        self.redis = get_redis_connection()

    def get_cache_key(self, session_id: str, method: str, path: str, body: dict = None):
        body_hash = hashlib.md5(json.dumps(body or {}).encode()).hexdigest()
        return f"{session_id}:{method}:{path}:{body_hash}"

    async def get(self, key: str):
        data = self.redis.get(key)
        return json.loads(data) if data else None

    async def set(self, key: str, value: dict, ttl: int = 86400):
        self.redis.setex(key, ttl, json.dumps(value))

    async def delete(self, key: str):
        self.redis.delete(key)


cache_service = CacheService()