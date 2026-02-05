from abc import ABC, abstractmethod
from typing import Optional
from app.domain.models.flights import Rating
from app.domain.dtos.rating_dto import RatingCreateDTO, RatingUpdateDTO
from app.domain.interfaces.repositories.irating_repository import RatingPaginationResult

class RatingServiceInterface(ABC):
    @abstractmethod
    def create_rating(self, user_id: int, data: RatingCreateDTO) -> Optional[Rating]:
        """Create a new rating."""

    @abstractmethod
    def update_rating(self, rating_id: int, user_id: int, data: RatingUpdateDTO) -> Optional[Rating]:
        """Update an existing rating."""

    @abstractmethod
    def get_rating(self, rating_id: int) -> Optional[Rating]:
        """Retrieve a rating by ID."""

    @abstractmethod
    def get_user_ratings(self, user_id: int, page: int, per_page: int) -> RatingPaginationResult:
        """Retrieve all ratings for a user with pagination."""

    @abstractmethod
    def get_all_ratings(self, page: int, per_page: int) -> RatingPaginationResult:
        """Retrieve all ratings with pagination."""

    @abstractmethod
    def delete_rating(self, rating_id: int) -> bool:
        """Delete a rating by ID."""
