from abc import ABC, abstractmethod
from typing import Any


class AirlineControllerInterface(ABC):
    @abstractmethod
    def create_airline(self) -> Any:
        pass

    @abstractmethod
    def get_airline(self, airline_id: int) -> Any:
        pass

    @abstractmethod
    def get_all_airlines(self) -> Any:
        pass

    @abstractmethod
    def update_airline(self, airline_id: int) -> Any:
        pass

    @abstractmethod
    def delete_airline(self, airline_id: int) -> Any:
        pass