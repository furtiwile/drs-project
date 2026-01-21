from abc import ABC, abstractmethod
from typing import Optional, Dict, List, TypedDict
from app.domain.models.flights import Booking


class BookingPaginationResult(TypedDict):
    bookings: List[Booking]
    page: int
    per_page: int
    total: int
    pages: int


class IBookingRepository(ABC):
    @abstractmethod
    def save_booking(self, booking: Booking) -> Booking:
        pass

    @abstractmethod
    def get_booking_by_id(self, booking_id: int) -> Optional[Booking]:
        pass

    @abstractmethod
    def get_bookings_by_user(self, user_id: int, page: int = 1, per_page: int = 10) -> BookingPaginationResult:
        pass

    @abstractmethod
    def get_all_bookings(self, page: int = 1, per_page: int = 10) -> BookingPaginationResult:
        pass

    @abstractmethod
    def get_bookings_by_flight_id(self, flight_id: int) -> List[Booking]:
        pass

    @abstractmethod
    def delete_booking(self, booking_id: int) -> bool:
        pass