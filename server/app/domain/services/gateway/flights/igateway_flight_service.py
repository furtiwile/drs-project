from abc import abstractmethod
from typing import Any

from app.domain.types.result import Result
from app.domain.dtos.gateway.flights.flight.flight_create_dto import FlightCreateDTO
from app.domain.dtos.gateway.flights.flight.flight_update_dto import FlightUpdateDTO
from app.domain.dtos.gateway.flights.flight.flight_status_update_dto import FlightStatusUpdateDTO
from app.domain.dtos.gateway.flights.flight.flight_dto import FlightDTO
from app.domain.dtos.gateway.flights.flight.paginated_flights_dto import PaginatedFlightsDTO
from app.domain.dtos.gateway.flights.flight.flight_remaining_time_dto import FlightRemainingTimeDTO
from app.domain.dtos.gateway.flights.flight.flight_available_seats_dto import FlightAvailableSeatsDTO
from app.domain.dtos.gateway.flights.flight.paginated_flights_by_tab import PaginatedFlightsByTabDTO
from app.domain.dtos.gateway.flights.flight.flight_cancel_dto import FlightCancelDTO

class IGatewayFlightService:
    @abstractmethod
    def create_flight(self, data: FlightCreateDTO, created_by: int) -> Result[FlightDTO, int]:
        pass

    @abstractmethod
    def get_all_flights(self, page: int, per_page: int, filters: dict[str, Any] | None = None) -> Result[PaginatedFlightsDTO, int]:
        pass

    @abstractmethod
    def get_flights_by_tab(self, tab: str, page: int, per_page: int, filters: dict[str, Any] | None = None) -> Result[PaginatedFlightsByTabDTO, int]:
        pass

    @abstractmethod
    def get_flight(self, flight_id: int) -> Result[FlightDTO, int]:
        pass

    @abstractmethod
    def update_flight(self, flight_id: int, data: FlightUpdateDTO, updated_by: int) -> Result[FlightDTO, int]:
        pass

    @abstractmethod
    def update_flight_status(self, flight_id: int, data: FlightStatusUpdateDTO, admin_id: int) -> Result[FlightDTO, int]:
        pass

    @abstractmethod
    def cancel_flight(self, flight_id: int, data: FlightCancelDTO, admin_id: int) -> Result[FlightDTO, int]:
        pass

    @abstractmethod
    def delete_flight(self, flight_id: int, deleted_by: int) -> Result[None, int]:
        pass

    @abstractmethod
    def get_available_seats(self, flight_id: int) -> Result[FlightAvailableSeatsDTO, int]:
        pass
    
    @abstractmethod
    def get_flight_remaining_time(self, flight_id: int) -> Result[FlightRemainingTimeDTO, int]:
        pass