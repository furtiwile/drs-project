from app.domain.services.gateway.flights.igateway_airline_service import IGatewayAirlineService
from app.domain.dtos.gateway.flights.airline.airline_create_dto import AirlineCreateDTO
from app.domain.dtos.gateway.flights.airline.airline_dto import AirlineDTO
from app.domain.dtos.gateway.flights.airline.airline_update_dto import AirlineUpdateDTO
from app.domain.dtos.gateway.flights.airline.paginated_airlines_dto import PaginatedAirlinesDTO
from app.domain.types.result import Result

from app.infrastructure.gateway.gateway_client import GatewayClient
from app.infrastructure.gateway.utils.api_callers import make_api_call

class GatewayAirlineService(IGatewayAirlineService):
    def __init__(self, client: GatewayClient) -> None:
        self.client = client

    def create_airline(self, data: AirlineCreateDTO) -> Result[AirlineDTO, int]:
        return make_api_call(
            lambda: self.client.post("/airlines", json=data.to_dict()),
            lambda r: AirlineDTO.from_dict(r.json()),
            success_codes=(200, 201)
        )
    
    def get_all_airlines(self, page: int, per_page: int) -> Result[PaginatedAirlinesDTO, int]:
        return make_api_call(
            lambda: self.client.get("/airlines", params={'page': page, 'per_page': per_page}),
            lambda r: PaginatedAirlinesDTO.from_dict(r.json()) 
        )

    def get_airline(self, airline_id: int) -> Result[AirlineDTO, int]:
        return make_api_call(
            lambda: self.client.get(f"/airlines/{airline_id}"),
            lambda r: AirlineDTO.from_dict(r.json()) 
        )
    
    def update_airline(self, airline_id: int, data: AirlineUpdateDTO) -> Result[AirlineDTO, int]:
        return make_api_call(
            lambda: self.client.patch(f"/airlines/{airline_id}", json=data.to_dict()),
            lambda r: AirlineDTO.from_dict(r.json())
        )
    
    def delete_airline(self, airline_id: int) -> Result[None, int]:
        return make_api_call(
            lambda: self.client.delete(f"/airlines/{airline_id}"),
            lambda _: None,
            success_codes=(200, 204)
        )
