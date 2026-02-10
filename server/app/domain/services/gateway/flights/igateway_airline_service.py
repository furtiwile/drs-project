from abc import abstractmethod
from app.domain.dtos.gateway.flights.airline.airline_create_dto import AirlineCreateDTO
from app.domain.dtos.gateway.flights.airline.airline_dto import AirlineDTO
from app.domain.dtos.gateway.flights.airline.airline_update_dto import AirlineUpdateDTO
from app.domain.types.gateway_result import GatewayResult
from app.domain.dtos.gateway.flights.airline.paginated_airlines_dto import PaginatedAirlinesDTO

class IGatewayAirlineService:
    @abstractmethod
    def create_airline(self, data: AirlineCreateDTO) -> GatewayResult[AirlineDTO]:
        pass
    
    @abstractmethod
    def get_all_airlines(self, page: int, per_page: int) -> GatewayResult[PaginatedAirlinesDTO]:
        pass

    @abstractmethod
    def get_airline(self, airline_id: int) -> GatewayResult[AirlineDTO]:
        pass
    
    @abstractmethod
    def update_airline(self, airline_id: int, data: AirlineUpdateDTO) -> GatewayResult[AirlineDTO]:
        pass
    
    @abstractmethod
    def delete_airline(self, airline_id: int) -> GatewayResult[None]:
        pass