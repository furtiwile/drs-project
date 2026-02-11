from typing import Any

from app.domain.services.gateway.flights.igateway_flight_service import IGatewayFlightService
from app.domain.dtos.gateway.flights.flight.flight_create_dto import FlightCreateDTO
from app.domain.dtos.gateway.flights.flight.flight_dto import FlightDTO
from app.domain.dtos.gateway.flights.flight.flight_remaining_time_dto import FlightRemainingTimeDTO
from app.domain.dtos.gateway.flights.flight.flight_status_update_dto import FlightStatusUpdateDTO
from app.domain.dtos.gateway.flights.flight.flight_update_dto import FlightUpdateDTO
from app.domain.dtos.gateway.flights.flight.paginated_flights_dto import PaginatedFlightsDTO
from app.domain.dtos.gateway.flights.flight.flight_available_seats_dto import FlightAvailableSeatsDTO
from app.domain.dtos.gateway.flights.flight.paginated_flights_by_tab import PaginatedFlightsByTabDTO
from app.domain.dtos.gateway.flights.flight.flight_cancel_dto import FlightCancelDTO
from app.domain.types.result import Result

from app.infrastructure.gateway.gateway_client import GatewayClient
from app.infrastructure.gateway.utils.api_callers import make_api_call

class GatewayFlightService(IGatewayFlightService):
    def __init__(self, gateway_client: GatewayClient) -> None:
        self.client = gateway_client

    def create_flight(self, data: FlightCreateDTO, created_by: int) -> Result[FlightDTO, int]:
        return make_api_call(
            lambda: self.client.post("/flights", headers={'user-id': str(created_by)}, json=data.to_dict()),
            lambda r: FlightDTO.from_dict(r.json()),
            success_codes=(200, 201)
        )

    def get_all_flights(self, page: int, per_page: int, filters: dict[str, Any] | None = None) -> Result[PaginatedFlightsDTO, int]:
        return make_api_call(
            lambda: self.client.get("/flights", params={'page': page, 'per_page': per_page, **(filters or {})}),
            lambda r: PaginatedFlightsDTO.from_dict(r.json())
        )

    def get_flights_by_tab(self, tab: str, page: int, per_page: int, filters: dict[str, Any] | None = None) -> Result[PaginatedFlightsByTabDTO, int]:
        return make_api_call(
            lambda: self.client.get(f"/flights/tabs/{tab}", params={'page': page, 'per_page': per_page, **(filters or {})}),
            lambda r: PaginatedFlightsByTabDTO.from_dict(r.json())
        )

    def get_flight(self, flight_id: int) -> Result[FlightDTO, int]:
        return make_api_call(
            lambda: self.client.get(f"/flights/{flight_id}"),
            lambda r: FlightDTO.from_dict(r.json())
        )

    def update_flight(self, flight_id: int, data: FlightUpdateDTO, updated_by: int) -> Result[FlightDTO, int]:
        return make_api_call(
            lambda: self.client.patch(f"/flights/{flight_id}", headers={'user-id': str(updated_by)}, json=data.to_dict()),
            lambda r: FlightDTO.from_dict(r.json())
        )

    def update_flight_status(self, flight_id: int, data: FlightStatusUpdateDTO, admin_id: int) -> Result[FlightDTO, int]:
        return make_api_call(
            lambda: self.client.patch(f"/flights/{flight_id}/status", headers={'admin-id': str(admin_id)}, json=data.to_dict()),
            lambda r: FlightDTO.from_dict(r.json())
        )

    def cancel_flight(self, flight_id: int, data: FlightCancelDTO, admin_id: int) -> Result[FlightDTO, int]:
        return make_api_call(
            lambda: self.client.post(f"/flights/{flight_id}/cancel", headers={'admin-id': str(admin_id)}, json=data.to_dict()),
            lambda r: FlightDTO.from_dict(r.json())
        )

    def delete_flight(self, flight_id: int, deleted_by: int) -> Result[None, int]:
        return make_api_call(
            lambda: self.client.delete(f"/flights/{flight_id}", headers={'user-id': str(deleted_by)}),
            lambda _: None,
            success_codes=(200, 204)
        )

    def get_available_seats(self, flight_id: int) -> Result[FlightAvailableSeatsDTO, int]:
        return make_api_call(
            lambda: self.client.get(f"/flights/{flight_id}/available-seats"),
            lambda r: FlightAvailableSeatsDTO.from_dict(r.json())
        )
    
    def get_flight_remaining_time(self, flight_id: int) -> Result[FlightRemainingTimeDTO, int]:
        return make_api_call(
            lambda: self.client.get(f"/flights/{flight_id}/remaining-time"),
            lambda r: FlightRemainingTimeDTO.from_dict(r.json())
        )
