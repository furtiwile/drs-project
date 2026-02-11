from abc import ABC, abstractmethod

class IBlacklistRepository(ABC):
    @abstractmethod
    def add_to_blacklist(self, jwt_token: str) -> None:
        pass

    @abstractmethod
    def remove_from_blacklist(self, jwt_token: str) -> None:
        pass

