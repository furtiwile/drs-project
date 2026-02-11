from app.domain.services.gateway.flights.igateway_airline_service import IGatewayAirlineService
from app.domain.repositories.redis.icache_repository import ICacheRepository
from app.domain.dtos.gateway.flights.airline.airline_create_dto import AirlineCreateDTO
from app.domain.dtos.gateway.flights.airline.airline_dto import AirlineDTO
from app.domain.dtos.gateway.flights.airline.airline_update_dto import AirlineUpdateDTO
from app.domain.dtos.gateway.flights.airline.paginated_airlines_dto import PaginatedAirlinesDTO
from app.domain.types.result import Result, ok

from app.infrastructure.gateway.gateway_client import GatewayClient
from app.infrastructure.gateway.utils.api_callers import make_api_call

class GatewayAirlineService(IGatewayAirlineService):
    def __init__(self, client: GatewayClient, cache_repository: ICacheRepository) -> None:
        self.client = client
        self.cache_repository = cache_repository
        self.cache_prefix = "airlines:"

    def create_airline(self, data: AirlineCreateDTO) -> Result[AirlineDTO, int]:
        result = make_api_call(
            lambda: self.client.post("/airlines", json=data.to_dict()),
            lambda r: AirlineDTO.from_dict(r.json()),
            success_codes=(200, 201)
        )

        if isinstance(result, ok):
            self.cache_repository.set_cache(f"{self.cache_prefix}{result.data.id}", result.data, 300)
            self.cache_repository.delete_pattern(f"{self.cache_prefix}page:*")

        return result
    
    def get_all_airlines(self, page: int, per_page: int) -> Result[PaginatedAirlinesDTO, int]:
        cached_data = self.cache_repository.get_cache(f"{self.cache_prefix}page:{page}:per_page:{per_page}")
        if cached_data is not None:
            return ok(cached_data)
        
        result = make_api_call(
            lambda: self.client.get("/airlines", params={'page': page, 'per_page': per_page}),
            lambda r: PaginatedAirlinesDTO.from_dict(r.json()) 
        )

        if isinstance(result, ok):
            self.cache_repository.set_cache(f"{self.cache_prefix}page:{page}:per_page:{per_page}", result.data, 60)

        return result

    def get_airline(self, airline_id: int) -> Result[AirlineDTO, int]:
        cached_data = self.cache_repository.get_cache(f"{self.cache_prefix}{airline_id}")
        if cached_data is not None:
            return ok(cached_data)

        result = make_api_call(
            lambda: self.client.get(f"/airlines/{airline_id}"),
            lambda r: AirlineDTO.from_dict(r.json()) 
        )

        if isinstance(result, ok):
            self.cache_repository.set_cache(f"{self.cache_prefix}{airline_id}", result.data, 300)

        return result
    
    def update_airline(self, airline_id: int, data: AirlineUpdateDTO) -> Result[AirlineDTO, int]:
        result = make_api_call(
            lambda: self.client.patch(f"/airlines/{airline_id}", json=data.to_dict()),
            lambda r: AirlineDTO.from_dict(r.json())
        )

        if isinstance(result, ok):
            self.cache_repository.delete_pattern(f"{self.cache_prefix}page:*")
            self.cache_repository.set_cache(f"{self.cache_prefix}{airline_id}", result.data, 300)

        return result
    
    def delete_airline(self, airline_id: int) -> Result[None, int]:
        result = make_api_call(
            lambda: self.client.delete(f"/airlines/{airline_id}"),
            lambda _: None,
            success_codes=(200, 204)
        )

        if isinstance(result, ok):
            self.cache_repository.delete_pattern(f"{self.cache_prefix}page:*")
            self.cache_repository.delete_cache(f"{self.cache_prefix}{airline_id}")

        return result
