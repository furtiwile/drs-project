from abc import ABC, abstractmethod

from app.domain.types.result import Result
from app.domain.dtos.gateway.flights.booking.booking_dto import BookingDTO
from app.domain.dtos.gateway.flights.booking.booking_create_dto import BookingCreateDTO
from app.domain.dtos.gateway.flights.booking.paginated_bookings_dto import PaginatedBookingsDTO

class IGatewayBookingService(ABC):
    @abstractmethod
    def create_booking(self, data: BookingCreateDTO, created_by: int) -> Result[None, int]:
        pass

    @abstractmethod
    def get_all_bookings(self, page: int, per_page: int) -> Result[PaginatedBookingsDTO, int]:
        pass

    @abstractmethod
    def get_booking(self, booking_id: int) -> Result[BookingDTO, int]:
        pass

    @abstractmethod
    def get_user_bookings(self, page: int, per_page: int, user_id: int) -> Result[PaginatedBookingsDTO, int]:
        pass

    @abstractmethod
    def delete_booking(self, booking_id: int, deleted_by: int) -> Result[None, int]:
        pass