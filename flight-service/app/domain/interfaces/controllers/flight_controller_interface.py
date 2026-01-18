from abc import ABC, abstractmethod
from typing import Any


class FlightControllerInterface(ABC):
    @abstractmethod
    def create_flight(self) -> Any:
        pass

    @abstractmethod
    def update_flight(self, flight_id: int) -> Any:
        pass

    @abstractmethod
    def get_flight(self, flight_id: int) -> Any:
        pass

    @abstractmethod
    def get_all_flights(self) -> Any:
        pass

    @abstractmethod
    def update_flight_status(self, flight_id: int) -> Any:
        pass

    @abstractmethod
    def delete_flight(self, flight_id: int) -> Any:
        pass

    @abstractmethod
    def get_available_seats(self, flight_id: int) -> Any:
        pass