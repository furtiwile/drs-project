from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from ..domain.models.flights import Airport

class AirportServiceInterface(ABC):
    @abstractmethod
    def create_airport(self, data: Dict) -> Airport:
        """Create a new airport."""
        pass

    @abstractmethod
    def get_airport(self, airport_id: int) -> Optional[Airport]:
        """Retrieve an airport by ID."""
        pass

    @abstractmethod
    def get_all_airports(self) -> List[Airport]:
        """Retrieve all airports."""
        pass

    @abstractmethod
    def update_airport(self, airport_id: int, data: Dict) -> Optional[Airport]:
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