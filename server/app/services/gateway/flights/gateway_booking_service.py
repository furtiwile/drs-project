from app.domain.services.gateway.flights.igateway_booking_service import IGatewayBookingService, PaginatedBookingsDTO
from app.infrastructure.gateway.gateway_client import GatewayClient
from app.domain.dtos.gateway.flights.booking.booking_create_dto import BookingCreateDTO
from app.domain.types.gateway_result import GatewayResult, ok, err
from app.domain.dtos.gateway.flights.booking.booking_dto import BookingDTO

class GatewayBookingService(IGatewayBookingService):
    def __init__(self, gateway_client: GatewayClient) -> None:
        self.client = gateway_client

    def create_booking(self, data: BookingCreateDTO, created_by: int) -> GatewayResult[BookingDTO]:
        try:
            response = self.client.post("/bookings", headers={'user-id': str(created_by)}, json=data.to_dict())
            if response.status_code in (200, 201):
                return ok(BookingDTO.from_dict(response.json()))
            
            error_message = (
                response.json().get("error", response.text)
                if response.headers.get("Content-Type", "").startswith("application/json")
                else response.text or "Unknown error"
            )
            return err(response.status_code, error_message)
        
        except Exception:
            return err(500, 'Internal Gateway Error')

    def get_all_bookings(self, page: int, per_page: int) -> GatewayResult[PaginatedBookingsDTO]:
        try:
            response = self.client.get("/bookings", params={'page': page, 'per_page': per_page})
            if response.status_code == 200:
                return ok(PaginatedBookingsDTO.from_dict(response.json()))
            
            error_message = (
                response.json().get("error", response.text)
                if response.headers.get("Content-Type", "").startswith("application/json")
                else response.text or "Unknown error"
            )
            return err(response.status_code, error_message)
        
        except Exception:
            return err(500, 'Internal Gateway Error')

    def get_booking(self, booking_id: int) -> GatewayResult[BookingDTO]:
        try:
            response = self.client.get(f"/airports/{booking_id}")
            if response.status_code == 200:
                return ok(BookingDTO.from_dict(response.json()))
            
            error_message = (
                response.json().get("error", response.text)
                if response.headers.get("Content-Type", "").startswith("application/json")
                else response.text or "Unknown error"
            )
            return err(response.status_code, error_message)
        
        except Exception:
            return err(500, 'Internal Gateway Error')

    def get_user_bookings(self, page: int, per_page: int, user_id: int) -> GatewayResult[PaginatedBookingsDTO]:
        try:
            response = self.client.get(f"/users/{user_id}/bookings", params={'page': page, 'per_page': per_page})
            if response.status_code == 200:
                return ok(PaginatedBookingsDTO.from_dict(response.json()))
            
            error_message = (
                response.json().get("error", response.text)
                if response.headers.get("Content-Type", "").startswith("application/json")
                else response.text or "Unknown error"
            )
            return err(response.status_code, error_message)
        
        except Exception:
            return err(500, 'Internal Gateway Error')

    def delete_booking(self, booking_id: int, deleted_by: int) -> GatewayResult[None]:
        try:
            response = self.client.delete(f"/bookings/{booking_id}", headers={'user-id': str(deleted_by)})
            if response.status_code in (200, 204):
                return ok(None)
            
            error_message = (
                response.json().get("error", response.text)
                if response.headers.get("Content-Type", "").startswith("application/json")
                else response.text or "Unknown error"
            )
            return err(response.status_code, error_message)
        
        except Exception:
            return err(500, 'Internal Gateway Error')
