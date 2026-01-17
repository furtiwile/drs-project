import redis

from app.domain.repositories.redis.iblacklist_repository import IBlacklistRepository

class BlacklistRepository(IBlacklistRepository):
    def __init__(self, redis_client: redis.Redis, ttl: int) -> None:
        self.redis_client = redis_client
        self.blacklist_key = "blacklist:"
        self.ttl = ttl

    def add_to_blacklist(self, jwt_token: str) -> None:
        self.redis_client.setex(f"{self.blacklist_key}{jwt_token}", self.ttl, "")

    def remove_from_blacklist(self, jwt_token: str) -> None:
        self.redis_client.delete(f"{self.blacklist_key}{jwt_token}")
