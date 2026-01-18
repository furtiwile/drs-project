from abc import ABC, abstractmethod
from typing import Optional, Dict, List, TypedDict
from app.domain.models.flights import Airline


class AirlinePaginationResult(TypedDict):
    airlines: List[Airline]
    page: int
    per_page: int
    total: int
    pages: int


class IAirlineRepository(ABC):
    @abstractmethod
    def save_airline(self, airline: Airline) -> Airline:
        pass

    @abstractmethod
    def get_airline_by_id(self, airline_id: int) -> Optional[Airline]:
        pass

    @abstractmethod
    def get_airline_by_name(self, name: str) -> Optional[Airline]:
        pass

    @abstractmethod
    def get_all_airlines(self, page: int = 1, per_page: int = 10) -> AirlinePaginationResult:
        pass

    @abstractmethod
    def update_airline(self, airline_id: int, data: Dict) -> Optional[Airline]:
        pass

    @abstractmethod
    def delete_airline(self, airline_id: int) -> bool:
        pass