from abc import ABC, abstractmethod
from typing import Optional, Dict, List, TypedDict
from datetime import datetime
from app.domain.models.flights import Flight
from ...types.repository_types import FlightUpdateData

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
    def update_flight(self, flight: Flight) -> Optional[Flight]:
        """Update flight entity"""
        pass

    @abstractmethod
    def update_flight_status(self, flight_id: int, status: str, rejection_reason: Optional[str] = None, 
                            approved_by: Optional[int] = None) -> bool:
        """Update flight status with optional rejection reason and approver"""
        pass

    @abstractmethod
    def update_flight_details(self, flight_id: int, data: FlightUpdateData) -> Optional[Flight]:
        pass
         
    @abstractmethod
    def get_available_seats(self, flight_id: int) -> int:
        pass

    @abstractmethod
    def delete_flight(self, flight_id: int) -> bool:
        pass
    
    @abstractmethod
    def get_flights_by_status(self, status: str, page: int = 1, per_page: int = 10) -> FlightPaginationResult:
        """Get flights filtered by status"""
        pass
    
    @abstractmethod
    def get_flights_to_start(self, current_time: datetime) -> List[Flight]:
        """Get approved flights that should start (departure_time <= current_time)"""
        pass
    
    @abstractmethod
    def get_flights_to_complete(self, current_time: datetime) -> List[Flight]:
        """Get in-progress flights that should complete (arrival_time <= current_time)"""
        pass
    
    @abstractmethod
    def get_user_bookings_for_flight(self, flight_id: int) -> List[int]:
        """Get list of user IDs who have booked this flight"""
        pass