from abc import abstractmethod

from app.domain.dtos.gateway.flights.airport.airport_dto import AirportDTO
from app.domain.types.gateway_result import GatewayResult
from app.domain.dtos.gateway.flights.airport.airport_create_dto import AirportCreateDTO
from app.domain.dtos.gateway.flights.airport.paginated_airports_dto import PaginatedAirportsDTO
from app.domain.dtos.gateway.flights.airport.airport_update_dto import AirportUpdateDTO


class IGatewayAirportService:
    @abstractmethod
    def create_airport(self, data: AirportCreateDTO) -> GatewayResult[AirportDTO]:
        pass

    @abstractmethod
    def get_all_airports(self, page: int, per_page: int) -> GatewayResult[PaginatedAirportsDTO]:
        pass

    @abstractmethod
    def get_airport(self, airport_id: int) -> GatewayResult[AirportDTO]:
        pass
    
    @abstractmethod
    def update_airport(self, airport_id: int, data: AirportUpdateDTO) -> GatewayResult[AirportDTO]:
        pass

    @abstractmethod
    def delete_airport(self, airport_id: int) -> GatewayResult[None]:
        pass

    @abstractmethod
    def get_airport_info(self, airport_code: str) -> GatewayResult[AirportDTO]:
        pass