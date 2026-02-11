from app.domain.services.gateway.flights.igateway_airport_service import IGatewayAirportService
from app.domain.dtos.gateway.flights.airport.airport_dto import AirportDTO
from app.domain.dtos.gateway.flights.airport.airport_create_dto import AirportCreateDTO
from app.domain.dtos.gateway.flights.airport.paginated_airports_dto import PaginatedAirportsDTO
from app.domain.dtos.gateway.flights.airport.airport_update_dto import AirportUpdateDTO
from app.domain.types.result import Result

from app.infrastructure.gateway.gateway_client import GatewayClient
from app.infrastructure.gateway.utils.api_callers import make_api_call

class GatewayAirportService(IGatewayAirportService):
    def __init__(self, gateway_client: GatewayClient) -> None:
        self.client = gateway_client
        return
    
    def create_airport(self, data: AirportCreateDTO) -> Result[AirportDTO, int]:
        return make_api_call(
            lambda: self.client.post("/airports", json=data.to_dict()),
            lambda r: AirportDTO.from_dict(r.json()),
            success_codes=(200, 201)
        )
    
    def get_all_airports(self, page: int, per_page: int) -> Result[PaginatedAirportsDTO, int]:
        return make_api_call(
            lambda: self.client.get("/airports", params={'page': page, 'per_page': per_page}),
            lambda r: PaginatedAirportsDTO.from_dict(r.json()),
        )

    def get_airport(self, airport_id: int) -> Result[AirportDTO, int]:
        return make_api_call(
            lambda: self.client.get(f"/airports/{airport_id}"),
            lambda r: AirportDTO.from_dict(r.json()),
        )
    
    def update_airport(self, airport_id: int, data: AirportUpdateDTO) -> Result[AirportDTO, int]:
        return make_api_call(
            lambda: self.client.patch(f"/airports/{airport_id}", json=data.to_dict()),
            lambda r: AirportDTO.from_dict(r.json()),
        )

    def delete_airport(self, airport_id: int) -> Result[None, int]:
        return make_api_call(
            lambda: self.client.delete(f"/airports/{airport_id}"),
            lambda _: None,
            success_codes=(200, 204)
        )

    def get_airport_info(self, airport_code: str) -> Result[AirportDTO, int]:
        return make_api_call(
            lambda: self.client.get(f"/airports/info/{airport_code}"),
            lambda r: AirportDTO.from_dict(r.json()),
        )
