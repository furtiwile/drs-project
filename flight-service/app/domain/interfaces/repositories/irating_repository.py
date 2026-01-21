from abc import ABC, abstractmethod
from typing import Optional, Dict, List, TypedDict
from app.domain.models.flights import Rating


class RatingPaginationResult(TypedDict):
    ratings: List[Rating]
    page: int
    per_page: int
    total: int
    pages: int


class IRatingRepository(ABC):
    @abstractmethod
    def save_rating(self, rating: Rating) -> Rating:
        pass

    @abstractmethod
    def get_rating_by_id(self, rating_id: int) -> Optional[Rating]:
        pass

    @abstractmethod
    def get_ratings_by_user(self, user_id: int, page: int = 1, per_page: int = 10) -> RatingPaginationResult:
        pass

    @abstractmethod
    def get_all_ratings(self, page: int = 1, per_page: int = 10) -> RatingPaginationResult:
        pass

    @abstractmethod
    def delete_rating(self, rating_id: int) -> bool:
        pass