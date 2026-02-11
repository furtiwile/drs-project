from app.domain.services.gateway.flights.igateway_airport_service import IGatewayAirportService
from app.domain.repositories.redis.icache_repository import ICacheRepository
from app.domain.dtos.gateway.flights.airport.airport_dto import AirportDTO
from app.domain.dtos.gateway.flights.airport.airport_create_dto import AirportCreateDTO
from app.domain.dtos.gateway.flights.airport.paginated_airports_dto import PaginatedAirportsDTO
from app.domain.dtos.gateway.flights.airport.airport_update_dto import AirportUpdateDTO
from app.domain.types.result import Result, ok

from app.infrastructure.gateway.gateway_client import GatewayClient
from app.infrastructure.gateway.utils.api_callers import make_api_call

class GatewayAirportService(IGatewayAirportService):
    def __init__(self, gateway_client: GatewayClient, cache_repository: ICacheRepository) -> None:
        self.client = gateway_client
        self.cache_repository = cache_repository
        self.cache_prefix = "airports:"
    
    def create_airport(self, data: AirportCreateDTO) -> Result[AirportDTO, int]:
        result = make_api_call(
            lambda: self.client.post("/airports", json=data.to_dict()),
            lambda r: AirportDTO.from_dict(r.json()),
            success_codes=(200, 201)
        )

        if isinstance(result, ok):
            self.cache_repository.set_cache(f"{self.cache_prefix}{result.data.id}", result.data, 300)
            self.cache_repository.set_cache(f"{self.cache_prefix}code:{result.data.code}", result.data, 300)
            self.cache_repository.delete_pattern(f"{self.cache_prefix}page:*")

        return result
    
    def get_all_airports(self, page: int, per_page: int) -> Result[PaginatedAirportsDTO, int]:
        cached_data = self.cache_repository.get_cache(f"{self.cache_prefix}page:{page}:per_page:{per_page}")
        if cached_data is not None:
            return ok(cached_data)
        
        result = make_api_call(
            lambda: self.client.get("/airports", params={'page': page, 'per_page': per_page}),
            lambda r: PaginatedAirportsDTO.from_dict(r.json()),
        )

        if isinstance(result, ok):
            self.cache_repository.set_cache(f"{self.cache_prefix}page:{page}:per_page:{per_page}", result.data, 60)

        return result

    def get_airport(self, airport_id: int) -> Result[AirportDTO, int]:
        cached_data = self.cache_repository.get_cache(f"{self.cache_prefix}{airport_id}")
        if cached_data is not None:
            return ok(cached_data)

        result = make_api_call(
            lambda: self.client.get(f"/airports/{airport_id}"),
            lambda r: AirportDTO.from_dict(r.json()),
        )

        if isinstance(result, ok):
            self.cache_repository.set_cache(f"{self.cache_prefix}{airport_id}", result.data, 300)
            self.cache_repository.set_cache(f"{self.cache_prefix}code:{result.data.code}", result.data, 300)

        return result
    
    def update_airport(self, airport_id: int, data: AirportUpdateDTO) -> Result[AirportDTO, int]:
        result = make_api_call(
            lambda: self.client.patch(f"/airports/{airport_id}", json=data.to_dict()),
            lambda r: AirportDTO.from_dict(r.json()),
        )

        if isinstance(result, ok):
            self.cache_repository.delete_pattern(f"{self.cache_prefix}page:*")
            self.cache_repository.delete_pattern(f"{self.cache_prefix}code:*")
            self.cache_repository.set_cache(f"{self.cache_prefix}code:{result.data.code}", result.data, 300)
            self.cache_repository.set_cache(f"{self.cache_prefix}{airport_id}", result.data, 300)

        return result

    def delete_airport(self, airport_id: int) -> Result[None, int]:
        result = make_api_call(
            lambda: self.client.delete(f"/airports/{airport_id}"),
            lambda _: None,
            success_codes=(200, 204)
        )

        if isinstance(result, ok):
            self.cache_repository.delete_pattern(f"{self.cache_prefix}page:*")
            self.cache_repository.delete_pattern(f"{self.cache_prefix}code:*")
            self.cache_repository.delete_cache(f"{self.cache_prefix}{airport_id}")

        return result

    def get_airport_info(self, airport_code: str) -> Result[AirportDTO, int]:
        cached_data = self.cache_repository.get_cache(f"{self.cache_prefix}code:{airport_code}")
        if cached_data is not None:
            return ok(cached_data)
        
        result = make_api_call(
            lambda: self.client.get(f"/airports/info/{airport_code}"),
            lambda r: AirportDTO.from_dict(r.json()),
        )

        if isinstance(result, ok):
            self.cache_repository.set_cache(f"{self.cache_prefix}{result.data.id}", result.data, 300)
            self.cache_repository.set_cache(f"{self.cache_prefix}code:{airport_code}", result.data, 300)

        return result
