import os
from dotenv import load_dotenv
import redis

load_dotenv()

_redis_client: redis.Redis | None = None

def init_redis():
    global _redis_client 
    if _redis_client is not None:
        return
    
    REDIS_URL = os.getenv("REDIS_URL")
    REDIS_MAX_CONNECTIONS = int(os.getenv("REDIS_MAX_CONNECTIONS", default="10"))

    _redis_client = redis.Redis(
        REDIS_URL,
        max_connections=REDIS_MAX_CONNECTIONS,
        decode_responses=True
    )

    

def get_redis_client() -> redis.Redis:
    if _redis_client is None:
        raise RuntimeError("Redis is not initialized")
    return _redis_client