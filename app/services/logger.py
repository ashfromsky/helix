import json
import time
from datetime import datetime
from app.database.core.connect import get_redis_connection
import logging

logger = logging.getLogger(__name__)


class LoggerService:
    def __init__(self):
        self.redis = get_redis_connection()
        self.log_key = "helix:request_logs"
        self.max_logs = 100

    def log_request(self, method: str, path: str, status: int, duration_ms: float, body: dict, response: dict):
        try:
            log_entry = {
                "id": str(time.time()),
                "timestamp": datetime.utcnow().strftime("%H:%M:%S"),
                "method": method,
                "path": path,
                "status": status,
                "duration": round(duration_ms, 2),
                "body": body,
                "response": response
            }

            self.redis.lpush(self.log_key, json.dumps(log_entry))

            self.redis.ltrim(self.log_key, 0, self.max_logs - 1)

        except Exception as e:
            logger.error(f"Failed to log request: {e}")

    def get_recent_logs(self, limit: int = 50):
        try:
            logs_raw = self.redis.lrange(self.log_key, 0, limit - 1)
            return [json.loads(log) for log in logs_raw]
        except Exception as e:
            logger.error(f"Failed to fetch logs: {e}")
            return []

    def clear_logs(self):
        self.redis.delete(self.log_key)


logger_service = LoggerService()