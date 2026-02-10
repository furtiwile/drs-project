from abc import abstractmethod
from app.domain.dtos.gateway.flights.airline.airline_create_dto import AirlineCreateDTO
from app.domain.dtos.gateway.flights.airline.airline_dto import AirlineDTO
from app.domain.dtos.gateway.flights.airline.airline_update_dto import AirlineUpdateDTO
from app.domain.types.result import Result
from app.domain.dtos.gateway.flights.airline.paginated_airlines_dto import PaginatedAirlinesDTO

class IGatewayAirlineService:
    @abstractmethod
    def create_airline(self, data: AirlineCreateDTO) -> Result[AirlineDTO, int]:
        pass
    
    @abstractmethod
    def get_all_airlines(self, page: int, per_page: int) -> Result[PaginatedAirlinesDTO, int]:
        pass

    @abstractmethod
    def get_airline(self, airline_id: int) -> Result[AirlineDTO, int]:
        pass
    
    @abstractmethod
    def update_airline(self, airline_id: int, data: AirlineUpdateDTO) -> Result[AirlineDTO, int]:
        pass
    
    @abstractmethod
    def delete_airline(self, airline_id: int) -> Result[None, int]:
        pass