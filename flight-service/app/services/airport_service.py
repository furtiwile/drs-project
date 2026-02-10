from typing import Optional
from ..domain.models.flights import Airport
from app.domain.interfaces.repositories.iairport_repository import IAirportRepository
from app.domain.interfaces.services.airport_service_interface import AirportServiceInterface
from app.domain.dtos.airport_dto import AirportCreateDTO, AirportUpdateDTO
from app.domain.interfaces.repositories.iairport_repository import AirportPaginationResult


class AirportService(AirportServiceInterface):
    """Service layer for airport operations with business logic validation."""
    
    def __init__(self, airport_repository: IAirportRepository):
        self.airport_repository = airport_repository

    def create_airport(self, data: AirportCreateDTO) -> Optional[Airport]:
        """Create a new airport."""
        data.code = data.code.upper().strip()
        data.name = data.name.strip()
        
        existing = self.airport_repository.get_airport_by_code(data.code)
        if existing:
            return None  # Indicate failure - duplicate code
        
        airport = Airport(name=data.name, code=data.code)
        return self.airport_repository.save_airport(airport)

    def get_airport(self, airport_id: int) -> Optional[Airport]:
        """Retrieve an airport by ID."""
        if airport_id <= 0:
            return None
        return self.airport_repository.get_airport_by_id(airport_id)

    def get_all_airports(self, page: int = 1, per_page: int = 10) -> AirportPaginationResult:
        """Retrieve all airports with pagination."""
        return self.airport_repository.get_all_airports(page=page, per_page=per_page)

    def update_airport(self, airport_id: int, data: AirportUpdateDTO) -> Optional[Airport]:
        if airport_id <= 0:
            return None
        if not self.airport_repository.get_airport_by_id(airport_id):
            return None
        
        # Check if at least one field is provided
        if data.code is None and data.name is None:
            return None  # Nothing to update
        
        update_dict = {}
        if data.name is not None:
            update_dict['name'] = data.name.strip()
        if data.code is not None:
            update_dict['code'] = data.code.upper().strip()
        
        return self.airport_repository.update_airport(airport_id, update_dict)

    def delete_airport(self, airport_id: int) -> bool:
        """Delete an airport by ID."""
        if airport_id <= 0:
            return False
        return self.airport_repository.delete_airport(airport_id)

    def fetch_airport_info(self, airport_code: str) -> Optional[Airport]:
        """Fetch airport information by code."""
        if not airport_code:
            return None
        airport_code = airport_code.upper().strip()
        return self.airport_repository.get_airport_by_code(airport_code)
    
    