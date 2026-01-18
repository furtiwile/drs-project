from abc import ABC, abstractmethod
from typing import Optional, Dict
from app.domain.models.flights import Flight
from app.domain.dtos.flight_dto import FlightCreateDTO, FlightUpdateDTO, FlightStatusUpdateDTO, FlightUpdateDTO
from app.domain.interfaces.repositories.iflight_repository import FlightPaginationResult

class FlightServiceInterface(ABC):
    @abstractmethod
    def create_flight(self, data: FlightCreateDTO) -> Optional[Flight]:
        """Create a new flight."""
        pass

    @abstractmethod
    def update_flight(self, flight_id: int, data: FlightUpdateDTO) -> Optional[Flight]:
        """Update a flight."""
        pass

    @abstractmethod
    def get_flight(self, flight_id: int) -> Optional[Flight]:
        """Retrieve a flight by ID."""
        pass

    @abstractmethod
    def get_all_flights(self, page: int, per_page: int, filters: Optional[Dict] = None) -> FlightPaginationResult:
        """Retrieve all flights with pagination and filters."""
        pass

    @abstractmethod
    def update_flight_status(self, flight_id: int, data: FlightStatusUpdateDTO) -> bool:
        """Update flight status."""
        pass

    @abstractmethod
    def delete_flight(self, flight_id: int) -> bool:
        """Delete a flight by ID."""
        pass

    @abstractmethod
    def get_available_seats(self, flight_id: int) -> int:
        """Get available seats for a flight."""
        pass