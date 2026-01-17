import redis

from app.domain.repositories.redis.iblocklist_repository import IBlocklistRepository

class BlocklistRepository(IBlocklistRepository):
    def __init__(self, redis_client: redis.Redis, block_threshold: int, ttl: int) -> None:
        self.redis_client = redis_client
        self.blocklist_key = "blocklist:"
        self.block_threshold = block_threshold
        self.ttl = ttl

    def add_attempt_to_blocklist(self, ip_address: str) -> None:
        key = f"{self.blocklist_key}{ip_address}"
        attempts = self.redis_client.incr(key)

        if(attempts == self.block_threshold):
            self.redis_client.expire(key, self.ttl)

    def is_blocked(self, ip_address: str) -> bool:
        attempts = self.redis_client.get(f"{self.blocklist_key}{ip_address}")
        return attempts is not None and int(str(attempts)) >= self.block_threshold

    def remove_from_blocklist(self, ip_address: str) -> None:
        self.redis_client.delete(f"{self.blocklist_key}{ip_address}")