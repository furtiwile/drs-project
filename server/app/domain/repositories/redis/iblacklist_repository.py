from abc import abstractmethod

class IBlacklistRepository:
    @abstractmethod
    def add_to_blacklist(self, jwt_token: str):
        pass

    @abstractmethod
    def remove_from_blacklist(self, jwt_token: str):
        pass

