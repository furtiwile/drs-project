import logging
import pickle
from typing import Any, cast
import redis
from app.domain.repositories.redis.icache_repository import ICacheRepository

logger = logging.getLogger(__name__)

class CacheRepository(ICacheRepository):
    def __init__(self, redis_client: redis.Redis) -> None:
        self.redis_client = redis_client
        self.cache_key = "cache:"

    def set_cache(self, key: str, value: Any, ttl: int) -> None:
        try:
            serialized_value = pickle.dumps(value)
            full_key = f"{self.cache_key}{key}"
            self.redis_client.setex(full_key, ttl, serialized_value)
            logger.debug(f"Cached '{key}' with TTL {ttl}s")

        except (pickle.PickleError, redis.RedisError) as e:
            logger.error(f"Failed to cache '{key}': {e}")

        except Exception as e:
            logger.error(f"Unexpected error caching '{key}': {e}")

    def get_cache(self, key: str) -> Any | None:
        try:
            full_key = f"{self.cache_key}{key}"
            raw = self.redis_client.get(full_key)
            
            if raw is None:
                logger.debug(f"Cache miss: '{key}'")
                return None
            
            value = pickle.loads(cast(bytes, raw))
            logger.debug(f"Cache hit: '{key}'")
            return value
            
        except (pickle.PickleError, pickle.UnpicklingError) as e:
            logger.warning(f"Failed to unpickle '{key}': {e}")
            self.delete_cache(key)
            return None
        
        except redis.RedisError as e:
            logger.error(f"Redis error retrieving '{key}': {e}")
            return None
        
        except Exception as e:
            logger.error(f"Unexpected error retrieving '{key}': {e}")
            return None

    def delete_cache(self, key: str) -> None:
        try:
            full_key = f"{self.cache_key}{key}"
            self.redis_client.delete(full_key)
            logger.debug(f"Deleted cache: '{key}'")

        except redis.RedisError as e:
            logger.error(f"Failed to delete cache '{key}': {e}")
        
    def delete_pattern(self, pattern: str) -> None:
        try:
            keys: list[str] = list(self.redis_client.scan_iter(f"{self.cache_key}{pattern}")) # type: ignore
            if keys:
                self.redis_client.delete(*keys)

        except redis.RedisError as e:
            logger.error(f"Failed to delete cache for pattern '{self.cache_key}{pattern}': {e}")