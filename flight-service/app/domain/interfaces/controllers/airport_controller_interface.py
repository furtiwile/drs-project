from abc import ABC, abstractmethod
from typing import Any


class AirportControllerInterface(ABC):
    @abstractmethod
    def create_airport(self) -> Any:
        pass

    @abstractmethod
    def get_airport(self, airport_id: int) -> Any:
        pass

    @abstractmethod
    def get_all_airports(self) -> Any:
        pass

    @abstractmethod
    def update_airport(self, airport_id: int) -> Any:
        pass

    @abstractmethod
    def delete_airport(self, airport_id: int) -> Any:
        pass

    @abstractmethod
    def get_airport_info(self, airport_code: str) -> Any:
        pass