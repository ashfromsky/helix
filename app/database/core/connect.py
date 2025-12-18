import redis
from .config import settings

r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB, decode_responses=True)


def get_redis_connection():
    return r


def ping_redis():
    try:
        return r.ping()
    except redis.ConnectionError:
        return False
