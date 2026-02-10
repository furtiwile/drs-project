from abc import abstractmethod

from app.domain.types.gateway_result import GatewayResult
from app.domain.dtos.gateway.flights.booking.booking_dto import BookingDTO
from app.domain.dtos.gateway.flights.booking.booking_create_dto import BookingCreateDTO
from app.domain.dtos.gateway.flights.booking.paginated_bookings_dto import PaginatedBookingsDTO

class IGatewayBookingService:
    @abstractmethod
    def create_booking(self, data: BookingCreateDTO, created_by: int) -> GatewayResult[BookingDTO]:
        pass

    @abstractmethod
    def get_all_bookings(self, page: int, per_page: int) -> GatewayResult[PaginatedBookingsDTO]:
        pass

    @abstractmethod
    def get_booking(self, booking_id: int) -> GatewayResult[BookingDTO]:
        pass

    @abstractmethod
    def get_user_bookings(self, page: int, per_page: int, user_id: int) -> GatewayResult[PaginatedBookingsDTO]:
        pass

    @abstractmethod
    def delete_booking(self, booking_id: int, deleted_by: int) -> GatewayResult[None]:
        pass