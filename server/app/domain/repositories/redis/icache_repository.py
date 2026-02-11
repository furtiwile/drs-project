from abc import ABC, abstractmethod
from typing import Any

class ICacheRepository(ABC):
    @abstractmethod
    def set_cache(self, key: str, value: Any, ttl: int) -> None:
        pass

    @abstractmethod
    def get_cache(self, key: str) -> Any | None:
        pass

    @abstractmethod
    def delete_cache(self, key: str) -> None:
        pass

    @abstractmethod
    def delete_pattern(self, pattern: str) -> None:
        pass