from typing import Optional, Dict
from ..domain.models.flights import Airline
from app.domain.interfaces.repositories.iairline_repository import IAirlineRepository
from app.domain.interfaces.services.airline_service_interface import AirlineServiceInterface
from app.domain.dtos.airline_dto import AirlineCreateDTO, AirlineUpdateDTO
from app.domain.interfaces.repositories.iairline_repository import AirlinePaginationResult


class AirlineService(AirlineServiceInterface):
    """Service layer for airline operations with business logic validation."""
    
    def __init__(self, airline_repository: IAirlineRepository):
        self.airline_repository = airline_repository

    def create_airline(self, data: AirlineCreateDTO) -> Optional[Airline]:
        """Create a new airline."""
        # Normalize data
        data.name = data.name.strip()

        if self.airline_repository.get_airline_by_name(data.name) is not None:
            return None  # Indicate failure - duplicate name
        
        airline = Airline(name=data.name)
        try:
            return self.airline_repository.save_airline(airline)
        except Exception:
            return None

    def get_airline(self, airline_id: int) -> Optional[Airline]:
        """Retrieve an airline by ID."""
        if airline_id <= 0:
            return None
        return self.airline_repository.get_airline_by_id(airline_id)
    
    def get_airline_by_name(self, name: str) -> Optional[Airline]:
        """Retrieve an airline by name."""
        name = name.strip()
        return self.airline_repository.get_airline_by_name(name)

    def get_all_airlines(self, page: int = 1, per_page: int = 10) -> AirlinePaginationResult:
        """Retrieve all airlines with pagination."""
        if page < 1:
            page = 1
        if per_page < 1:
            per_page = 10
        if per_page > 100:  # Limit max items per page to 100
            per_page = 100
        
        return self.airline_repository.get_all_airlines(page, per_page)

    def update_airline(self, airline_id: int, data: AirlineUpdateDTO) -> Optional[Airline]:
        """Update an existing airline."""
        if airline_id <= 0:
            return None
        if not self.airline_repository.get_airline_by_id(airline_id):
            return None
        
        update_dict = {}
        if data.name is not None:
            data.name = data.name.strip()
            update_dict['name'] = data.name
            if self.get_airline_by_name(data.name) is not None:
                return None  # Indicate failure - duplicate or same name
        
        return self.airline_repository.update_airline(airline_id, update_dict)

    def delete_airline(self, airline_id: int) -> bool:
        """Delete an airline by ID."""
        if airline_id <= 0:
            return False
        return self.airline_repository.delete_airline(airline_id)
