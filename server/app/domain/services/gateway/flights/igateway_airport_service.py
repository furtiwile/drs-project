from abc import abstractmethod

from app.domain.dtos.gateway.flights.airport.airport_dto import AirportDTO
from app.domain.types.result import Result
from app.domain.dtos.gateway.flights.airport.airport_create_dto import AirportCreateDTO
from app.domain.dtos.gateway.flights.airport.paginated_airports_dto import PaginatedAirportsDTO
from app.domain.dtos.gateway.flights.airport.airport_update_dto import AirportUpdateDTO


class IGatewayAirportService:
    @abstractmethod
    def create_airport(self, data: AirportCreateDTO) -> Result[AirportDTO, int]:
        pass

    @abstractmethod
    def get_all_airports(self, page: int, per_page: int) -> Result[PaginatedAirportsDTO, int]:
        pass

    @abstractmethod
    def get_airport(self, airport_id: int) -> Result[AirportDTO, int]:
        pass
    
    @abstractmethod
    def update_airport(self, airport_id: int, data: AirportUpdateDTO) -> Result[AirportDTO, int]:
        pass

    @abstractmethod
    def delete_airport(self, airport_id: int) -> Result[None, int]:
        pass

    @abstractmethod
    def get_airport_info(self, airport_code: str) -> Result[AirportDTO, int]:
        pass