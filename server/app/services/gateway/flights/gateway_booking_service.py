from app.domain.services.gateway.flights.igateway_booking_service import IGatewayBookingService
from app.domain.dtos.gateway.flights.booking.booking_create_dto import BookingCreateDTO
from app.domain.dtos.gateway.flights.booking.paginated_bookings_dto import PaginatedBookingsDTO
from app.domain.dtos.gateway.flights.booking.booking_dto import BookingDTO
from app.domain.types.result import Result

from app.infrastructure.gateway.gateway_client import GatewayClient
from app.infrastructure.gateway.utils.api_callers import make_api_call

class GatewayBookingService(IGatewayBookingService):
    def __init__(self, gateway_client: GatewayClient) -> None:
        self.client = gateway_client

    def create_booking(self, data: BookingCreateDTO, created_by: int) -> Result[BookingDTO, int]:
        return make_api_call(
            lambda: self.client.post("/bookings", headers={'user-id': str(created_by)}, json=data.to_dict()),
            lambda r: BookingDTO.from_dict(r.json()),
            success_codes=(200, 201)
        )

    def get_all_bookings(self, page: int, per_page: int) -> Result[PaginatedBookingsDTO, int]:
        return make_api_call(
            lambda: self.client.get("/bookings", params={'page': page, 'per_page': per_page}),
            lambda r: PaginatedBookingsDTO.from_dict(r.json())
        )

    def get_booking(self, booking_id: int) -> Result[BookingDTO, int]:
        return make_api_call(
            lambda: self.client.get(f"/bookings/{booking_id}"),
            lambda r: BookingDTO.from_dict(r.json())
        )

    def get_user_bookings(self, page: int, per_page: int, user_id: int) -> Result[PaginatedBookingsDTO, int]:
        return make_api_call(
            lambda: self.client.get(f"/users/{user_id}/bookings", params={'page': page, 'per_page': per_page}),
            lambda r: PaginatedBookingsDTO.from_dict(r.json())
        )

    def delete_booking(self, booking_id: int, deleted_by: int) -> Result[None, int]:
        return make_api_call(
            lambda: self.client.delete(f"/bookings/{booking_id}", headers={'user-id': str(deleted_by)}),
            lambda _: None,
            success_codes=(200, 204)
        )
