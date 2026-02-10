from typing import Any
from app.domain.services.gateway.flights.igateway_flight_service import IGatewayFlightService
from app.infrastructure.gateway.gateway_client import GatewayClient
from app.domain.types.result import Result, ok, err
from app.domain.dtos.gateway.flights.flight.flight_create_dto import FlightCreateDTO
from app.domain.dtos.gateway.flights.flight.flight_dto import FlightDTO
from app.domain.dtos.gateway.flights.flight.flight_remaining_time_dto import FlightRemainingTimeDTO
from app.domain.dtos.gateway.flights.flight.flight_status_update_dto import FlightStatusUpdateDTO
from app.domain.dtos.gateway.flights.flight.flight_update_dto import FlightUpdateDTO
from app.domain.dtos.gateway.flights.flight.paginated_flights_dto import PaginatedFlightsDTO
from app.domain.dtos.gateway.flights.flight.flight_available_seats_dto import FlightAvailableSeatsDTO
from app.domain.dtos.gateway.flights.flight.paginated_flights_by_tab import PaginatedFlightsByTabDTO
from app.domain.dtos.gateway.flights.flight.flight_cancel_dto import FlightCancelDTO

class GatewayFlightService(IGatewayFlightService):
    def __init__(self, gateway_client: GatewayClient) -> None:
        self.client = gateway_client

    def create_flight(self, data: FlightCreateDTO, created_by: int) -> Result[FlightDTO, int]:
        try:
            response = self.client.post("/flights", headers={'user-id': str(created_by)}, json=data.to_dict())
            if response.status_code in (200, 201):
                return ok(FlightDTO.from_dict(response.json()))
            
            error_message = (
                response.json().get("error", response.text)
                if response.headers.get("Content-Type", "").startswith("application/json")
                else response.text or "Unknown error"
            )
            return err(response.status_code, error_message)
        
        except Exception:
            return err(500, 'Internal Gateway Error')

    def get_all_flights(self, page: int, per_page: int, filters: dict[str, Any] | None = None) -> Result[PaginatedFlightsDTO, int]:
        try:
            response = self.client.get("/flights", params={'page': page, 'per_page': per_page, **(filters or {})})
            if response.status_code == 200:
                return ok(PaginatedFlightsDTO.from_dict(response.json()))
            
            error_message = (
                response.json().get("error", response.text)
                if response.headers.get("Content-Type", "").startswith("application/json")
                else response.text or "Unknown error"
            )
            return err(response.status_code, error_message)
        
        except Exception:
            return err(500, 'Internal Gateway Error')

    def get_flights_by_tab(self, tab: str, page: int, per_page: int, filters: dict[str, Any] | None = None) -> Result[PaginatedFlightsByTabDTO, int]:
        try:
            response = self.client.get(f"/flights/tabs/{tab}", params={'page': page, 'per_page': per_page, **(filters or {})})
            if response.status_code in (200, 204):
                return ok(PaginatedFlightsByTabDTO.from_dict(response.json()))
            
            error_message = (
                response.json().get("error", response.text)
                if response.headers.get("Content-Type", "").startswith("application/json")
                else response.text or "Unknown error"
            )
            return err(response.status_code, error_message)
        
        except Exception:
            return err(500, 'Internal Gateway Error')

    def get_flight(self, flight_id: int) -> Result[FlightDTO, int]:
        try:
            response = self.client.get(f"/flights/{flight_id}")
            if response.status_code == 200:
                return ok(FlightDTO.from_dict(response.json()))
            
            error_message = (
                response.json().get("error", response.text)
                if response.headers.get("Content-Type", "").startswith("application/json")
                else response.text or "Unknown error"
            )
            return err(response.status_code, error_message)
        
        except Exception:
            return err(500, 'Internal Gateway Error')

    def update_flight(self, flight_id: int, data: FlightUpdateDTO, updated_by: int) -> Result[FlightDTO, int]:
        try:
            response = self.client.patch(f"/flights/{flight_id}", headers={'user-id': str(updated_by)}, json=data.to_dict())
            if response.status_code == 200:
                return ok(FlightDTO.from_dict(response.json()))
            
            error_message = (
                response.json().get("error", response.text)
                if response.headers.get("Content-Type", "").startswith("application/json")
                else response.text or "Unknown error"
            )
            return err(response.status_code, error_message)
        
        except Exception:
            return err(500, 'Internal Gateway Error')

    def update_flight_status(self, flight_id: int, data: FlightStatusUpdateDTO, admin_id: int) -> Result[FlightDTO, int]:
        try:
            response = self.client.patch(f"/flights/{flight_id}/status", headers={'admin-id': str(admin_id)}, json=data.to_dict())
            if response.status_code == 200:
                return ok(FlightDTO.from_dict(response.json()))
            
            error_message = (
                response.json().get("error", response.text)
                if response.headers.get("Content-Type", "").startswith("application/json")
                else response.text or "Unknown error"
            )
            return err(response.status_code, error_message)
        
        except Exception:
            return err(500, 'Internal Gateway Error')

    def cancel_flight(self, flight_id: int, data: FlightCancelDTO, admin_id: int) -> Result[FlightDTO, int]:
        try:
            response = self.client.post(f"/flights/{flight_id}/cancel", headers={'admin-id': str(admin_id)}, json=data.to_dict())
            if response.status_code == 200:
                return ok(FlightDTO.from_dict(response.json()))
            
            error_message = (
                response.json().get("error", response.text)
                if response.headers.get("Content-Type", "").startswith("application/json")
                else response.text or "Unknown error"
            )
            return err(response.status_code, error_message)
        
        except Exception:
            return err(500, 'Internal Gateway Error')

    def delete_flight(self, flight_id: int, deleted_by: int) -> Result[None, int]:
        try:
            response = self.client.delete(f"/flights/{flight_id}", headers={'user-id': str(deleted_by)})
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

    def get_available_seats(self, flight_id: int) -> Result[FlightAvailableSeatsDTO, int]:
        try:
            response = self.client.get(f"/flights/{flight_id}/available-seats")
            if response.status_code == 200:
                return ok(FlightAvailableSeatsDTO.from_dict(response.json()))
            
            error_message = (
                response.json().get("error", response.text)
                if response.headers.get("Content-Type", "").startswith("application/json")
                else response.text or "Unknown error"
            )
            return err(response.status_code, error_message)
        
        except Exception:
            return err(500, 'Internal Gateway Error')
    
    def get_flight_remaining_time(self, flight_id: int) -> Result[FlightRemainingTimeDTO, int]:
        try:
            response = self.client.get(f"/flights/{flight_id}/remaining-time")
            if response.status_code == 200:
                return ok(FlightRemainingTimeDTO.from_dict(response.json()))
            
            error_message = (
                response.json().get("error", response.text)
                if response.headers.get("Content-Type", "").startswith("application/json")
                else response.text or "Unknown error"
            )
            return err(response.status_code, error_message)
        
        except Exception:
            return err(500, 'Internal Gateway Error')