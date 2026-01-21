from abc import ABC, abstractmethod
from typing import Optional, Dict
from app.domain.models.flights import Booking
from app.domain.dtos.booking_dto import BookingCreateDTO
from app.domain.interfaces.repositories.ibooking_repository import BookingPaginationResult

class BookingServiceInterface(ABC):
    @abstractmethod
    def create_booking(self, user_id: int, data: BookingCreateDTO) -> Optional[Booking]:
        """Create a new booking."""
        pass

    @abstractmethod
    def get_booking(self, booking_id: int) -> Optional[Booking]:
        """Retrieve a booking by ID."""
        pass

    @abstractmethod
    def get_user_bookings(self, user_id: int, page: int, per_page: int) -> BookingPaginationResult:
        """Retrieve all bookings for a user with pagination."""
        pass

    @abstractmethod
    def get_all_bookings(self, page: int, per_page: int) -> BookingPaginationResult:
        """Retrieve all bookings with pagination."""
        pass

    @abstractmethod
    def delete_booking(self, booking_id: int) -> bool:
        """Delete a booking by ID."""
        pass