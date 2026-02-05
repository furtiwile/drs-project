from abc import ABC, abstractmethod
from typing import Optional
from app.domain.models.flights import Airline
from app.domain.dtos.airline_dto import AirlineCreateDTO, AirlineUpdateDTO
from app.domain.interfaces.repositories.iairline_repository import AirlinePaginationResult


class AirlineServiceInterface(ABC):
    @abstractmethod
    def create_airline(self, data: AirlineCreateDTO) -> Optional[Airline]:
        """Create a new airline."""

    @abstractmethod
    def get_airline(self, airline_id: int) -> Optional[Airline]:
        """Retrieve an airline by ID."""

    @abstractmethod
    def get_all_airlines(self, page: int, per_page: int) -> AirlinePaginationResult:
        """Retrieve all airlines with pagination."""

    @abstractmethod
    def update_airline(self, airline_id: int, data: AirlineUpdateDTO) -> Optional[Airline]:
        """Update an existing airline."""

    @abstractmethod
    def delete_airline(self, airline_id: int) -> bool:
        """Delete an airline by ID."""
