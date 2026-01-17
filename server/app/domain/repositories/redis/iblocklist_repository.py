from abc import abstractmethod

class IBlocklistRepository:
    @abstractmethod
    def add_attempt_to_blocklist(self, ip_address: str) -> None:
        pass

    @abstractmethod
    def is_blocked(self, ip_address: str) -> bool:
        pass

    @abstractmethod
    def remove_from_blocklist(self, ip_address: str) -> None:
        pass