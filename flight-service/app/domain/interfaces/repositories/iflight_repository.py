from abc import ABC, abstractmethod
from typing import Optional, Dict, List, TypedDict
from app.domain.models.flights import Flight


class FlightPaginationResult(TypedDict):
    flights: List[Flight]
    page: int
    per_page: int
    total: int
    pages: int


class IFlightRepository(ABC):
    @abstractmethod
    def save_flight(self, flight: Flight) -> Flight:
        pass

    @abstractmethod
    def get_flight_by_id(self, flight_id: int) -> Optional[Flight]:
        pass

    @abstractmethod
    def get_all_flights(self, page: int = 1, per_page: int = 10, filters: Optional[Dict] = None) -> FlightPaginationResult:
        pass

    @abstractmethod
    def update_flight(self, flight_id: int, status: str, rejection_reason: Optional[str] = None) -> bool:
        pass

    @abstractmethod
    def update_flight_details(self, flight_id: int, data: Dict[str, any]) -> Optional[Flight]:
        pass

    @abstractmethod
    def get_available_seats(self, flight_id: int) -> int:
        pass

    @abstractmethod
    def delete_flight(self, flight_id: int) -> bool:
        pass