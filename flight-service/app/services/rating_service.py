from typing import Optional
from datetime import datetime
from ..domain.models.flights import Rating
from app.domain.interfaces.repositories.irating_repository import IRatingRepository, RatingPaginationResult
from app.domain.interfaces.repositories.ibooking_repository import IBookingRepository
from app.domain.interfaces.services.rating_service_interface import RatingServiceInterface
from app.domain.dtos.rating_dto import RatingCreateDTO, RatingUpdateDTO


class RatingService(RatingServiceInterface):
    """Service layer for rating operations with comprehensive business logic validation."""

    def __init__(self, rating_repository: IRatingRepository, booking_repository: IBookingRepository):
        self.rating_repository = rating_repository
        self.booking_repository = booking_repository

    def create_rating(self, user_id: int, data: RatingCreateDTO) -> Optional[Rating]:
        """Create a new rating with comprehensive validation."""
        if user_id <= 0 or data.flight_id <= 0:
            return None
        if data.rating < 1 or data.rating > 5:
            return None

        # Check if user has a booking for this flight
        user_bookings = self.booking_repository.get_bookings_by_user(user_id, page=1, per_page=1000)
        has_booking = False
        for b in user_bookings.get('bookings', []):
            if b.flight_id == data.flight_id:
                has_booking = True
                break
        if not has_booking:
            return None  # User must have booked the flight to rate it

        # Check if rating already exists
        user_ratings = self.rating_repository.get_ratings_by_user(user_id, page=1, per_page=1000)
        existing_rating = False
        for r in user_ratings.get('ratings', []):
            if r.flight_id == data.flight_id:
                existing_rating = True
                break
        if existing_rating:
            return None  # User can only rate once per flight

        # Can only rate after flight has completed (arrival time passed)
        from ..domain.models.flights import Flight
        flight = Flight.query.get(data.flight_id)
        if not flight or flight.arrival_time > datetime.now():
            return None  # Can't rate a flight that hasn't completed yet
        try:
            rating = Rating(user_id=user_id, flight_id=data.flight_id, rating=data.rating)
            saved_rating = self.rating_repository.save_rating(rating)
            
            return saved_rating
        except Exception:
            return None

    def update_rating(self, rating_id: int, user_id: int, data: RatingUpdateDTO) -> Optional[Rating]:
        """Update an existing rating with validation."""
        if rating_id <= 0 or user_id <= 0:
            return None

        if data.rating < 1 or data.rating > 5:
            return None

        existing_rating = self.rating_repository.get_rating_by_id(rating_id)
        if not existing_rating:
            return None

        if existing_rating.user_id != user_id:
            return None

        existing_rating.rating = data.rating
        try:
            updated_rating = self.rating_repository.save_rating(existing_rating)
            return updated_rating
        except Exception:
            return None

    def get_rating(self, rating_id: int) -> Optional[Rating]:
        """Retrieve a rating by ID."""
        if rating_id <= 0:
            return None
        return self.rating_repository.get_rating_by_id(rating_id)

    def get_user_ratings(self, user_id: int, page: int = 1, per_page: int = 10) -> RatingPaginationResult:
        """Retrieve all ratings for a user with pagination."""
        if user_id <= 0:
            return {'ratings': [], 'page': 1, 'per_page': per_page, 'total': 0, 'pages': 0}

        if page < 1:
            page = 1
        if per_page < 1:
            per_page = 10
        if per_page > 100:  # Limit max items per page
            per_page = 100

        return self.rating_repository.get_ratings_by_user(user_id, page, per_page)

    def get_all_ratings(self, page: int = 1, per_page: int = 10) -> RatingPaginationResult:
        """Retrieve all ratings with pagination."""
        if page < 1:
            page = 1
        if per_page < 1:
            per_page = 10
        if per_page > 100:  # Limit max items per page
            per_page = 100

        return self.rating_repository.get_all_ratings(page, per_page)

    def delete_rating(self, rating_id: int) -> bool:
        """Delete a rating by ID with validation."""
        if rating_id <= 0:
            return False

        return self.rating_repository.delete_rating(rating_id)