from abc import ABC, abstractmethod
from typing import Optional, List, TypedDict
from app.domain.models.flights import Airport

class AirportPaginationResult(TypedDict):
    airports: List[Airport]
    page: int
    per_page: int
    total: int
    pages: int


class IAirportRepository(ABC):
    @abstractmethod
    def save_airport(self, airport: Airport) -> Airport:
        pass

    @abstractmethod
    def get_airport_by_id(self, airport_id: int) -> Optional[Airport]:
        pass

    @abstractmethod
    def get_airport_by_code(self, airport_code: str) -> Optional[Airport]:
        pass

    @abstractmethod
    def get_all_airports(self, page: int = 1, per_page: int = 10) -> AirportPaginationResult:
        pass

    @abstractmethod
    def update_airport(self, airport_id: int, data: dict) -> Optional[Airport]:
        pass

    @abstractmethod
    def delete_airport(self, airport_id: int) -> bool:
        pass