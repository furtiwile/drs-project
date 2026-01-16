from typing import List, Optional, Dict
from ..domain.models.flights import Airport
from ..repositories.interfaces import IAirportRepository
from .interfaces import AirportServiceInterface

class AirportService(AirportServiceInterface):
    def __init__(self, airport_repository: IAirportRepository):
        self.airport_repository = airport_repository

    def create_airport(self, data: Dict) -> Airport:
        airport = Airport(**data)
        return self.airport_repository.save_airport(airport)

    def get_airport(self, airport_id: int) -> Optional[Airport]:
        return self.airport_repository.get_airport_by_id(airport_id)

    def get_all_airports(self) -> List[Airport]:
        result = self.airport_repository.get_all_airports()
        return result['airports']

    def update_airport(self, airport_id: int, data: Dict) -> Optional[Airport]:
        return self.airport_repository.update_airport(airport_id, data)

    def delete_airport(self, airport_id: int) -> bool:
        return self.airport_repository.delete_airport(airport_id)

    def fetch_airport_info(self, airport_code: str) -> Optional[Airport]:
        return self.airport_repository.get_airport_by_code(airport_code)