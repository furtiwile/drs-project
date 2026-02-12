from abc import ABC, abstractmethod
from typing import Optional, Dict
from app.domain.models.flights import Flight
from app.domain.dtos.flight_dto import DeleteFlightDTO, FlightCreateDTO, FlightUpdateDTO, FlightStatusUpdateDTO, FlightUpdateDTO
from app.domain.interfaces.repositories.iflight_repository import FlightPaginationResult

class FlightServiceInterface(ABC):
    @abstractmethod
    def create_flight(self, data: FlightCreateDTO, created_by: int) -> Optional[Flight]:
        """Create a new flight."""

    @abstractmethod
    def update_flight(self, flight_id: int, data: FlightUpdateDTO) -> Optional[Flight]:
        """Update a flight."""

    @abstractmethod
    def get_flight(self, flight_id: int) -> Optional[Flight]:
        """Retrieve a flight by ID."""

    @abstractmethod
    def get_all_flights(self, page: int, per_page: int, filters: Optional[Dict] = None) -> FlightPaginationResult:
        """Retrieve all flights with pagination and filters."""

    @abstractmethod
    def update_flight_status(self, flight_id: int, data: FlightStatusUpdateDTO, admin_id: int) -> Optional[Flight]:
        """Update flight status (approve/reject/cancel)."""

    # @abstractmethod
    # def delete_flight(self, flight_id: int) -> bool:
    #     """Delete a flight by ID."""

    @abstractmethod
    def get_available_seats(self, flight_id: int) -> int:
        """Get available seats for a flight."""
    
    @abstractmethod
    def get_flights_by_tab(self, tab: str, page: int, per_page: int, filters: Optional[Dict] = None) -> FlightPaginationResult:
        """Get flights by tab (upcoming, in-progress, completed/cancelled)."""
    
    @abstractmethod
    def cancel_flight(self, flight_id: int, admin_id: int) -> Optional[DeleteFlightDTO]:
        """Cancel an approved flight and notify users."""
    
    @abstractmethod
    def get_flight_remaining_time(self, flight_id: int) -> Optional[Dict]:
        """Get remaining time for in-progress flight."""

    @abstractmethod
    def get_price_for_flight(self, flight_id: int) -> Optional[float]:
        """Get the price of a flight"""
