from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from app.domain.dtos.airport_dto import AirportCreateDTO, AirportUpdateDTO
from app.domain.models.flights import Airport
from app.domain.interfaces.repositories.iairport_repository import AirportPaginationResult


class AirportServiceInterface(ABC):
    @abstractmethod
    def create_airport(self, data: AirportCreateDTO) -> Optional[Airport]:
        """Create a new airport."""
        pass

    @abstractmethod
    def get_airport(self, airport_id: int) -> Optional[Airport]:
        """Retrieve an airport by ID."""
        pass

    @abstractmethod
    def get_all_airports(self, page: int = 1, per_page: int = 10) -> AirportPaginationResult:
        """Retrieve all airports with pagination."""
        pass

    @abstractmethod
    def update_airport(self, airport_id: int, data: AirportUpdateDTO) -> Optional[Airport]:
        """Update an existing airport."""
        pass

    @abstractmethod
    def delete_airport(self, airport_id: int) -> bool:
        """Delete an airport by ID."""
        pass

    @abstractmethod
    def fetch_airport_info(self, airport_code: str) -> Optional[Airport]:
        """Fetch airport information by code."""
        pass