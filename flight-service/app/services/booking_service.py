from typing import Optional, List
from datetime import datetime, timedelta, timezone
from ..domain.models.flights import Booking
from app.domain.interfaces.repositories.ibooking_repository import BookingPaginationResult, IBookingRepository
from app.domain.interfaces.repositories.iflight_repository import IFlightRepository
from app.domain.interfaces.services.booking_service_interface import BookingServiceInterface
from app.domain.dtos.booking_dto import BookingCreateDTO, BookingCreateDTOReturn, BookingDTO
from app.domain.models.enums import FlightStatus
from app.domain.types.task_types import TaskStatus
import time
from app.utils.logger_service import get_logger

logger = get_logger(__name__)


class BookingService(BookingServiceInterface):
    """Service layer for booking operations with comprehensive business logic validation."""
    
    def __init__(self, booking_repository: IBookingRepository, flight_repository: IFlightRepository, task_manager=None):
        self.booking_repository = booking_repository
        self.flight_repository = flight_repository
        self.task_manager = task_manager

    def create_booking(self, user_id: int, booking_data: BookingCreateDTO) -> Optional[BookingDTO]:
        """
        Create a booking
        Returns BookingDTO with booking details
        """
        if not self.task_manager:
            logger.warning("Task manager not available, falling back to synchronous booking")
            return None
        
        print(f"Received booking request for user_id={user_id}, flight_id={booking_data.flight_id}")

        if user_id <= 0 or booking_data.flight_id <= 0:
            return None
        
        print(f"Validating flight_id={booking_data.flight_id}")

        flight = self.flight_repository.get_flight_by_id(booking_data.flight_id)
        if not flight:
            return None
        
        print(f"Flight found: {flight.flight_id}, status={flight.status}, departure_time={flight.departure_time}")
        
        if flight.status != FlightStatus.APPROVED:
            return None
        
        print(f"Flight status is APPROVED, checking departure time for flight_id={flight.flight_id}")
        
        if flight.departure_time.tzinfo is None:
            flight.departure_time = flight.departure_time.replace(tzinfo=timezone.utc)

        print(f"Current time: {datetime.now(timezone.utc)}, flight departure time: {flight.departure_time}")

        if flight.departure_time <= datetime.now(timezone.utc):
            return None
        
        print(f"Flight departure time is in the future, checking available seats for flight_id={flight.flight_id}")

        available_seats = self.flight_repository.get_available_seats(booking_data.flight_id)
        if available_seats <= 0:
            return None
        
        print(f"Seats available: {available_seats}, checking for existing bookings for user_id={user_id} on flight_id={booking_data.flight_id}")
        
        user_bookings = self.booking_repository.get_bookings_by_user(user_id, page=1, per_page=1000)
        for existing_booking in user_bookings.get('bookings', []):
            if existing_booking.flight_id == booking_data.flight_id:
                return None

        print(f"No existing bookings found for user_id={user_id} on flight_id={booking_data.flight_id}, creating booking task")

        time.sleep(1)
        booking = Booking(user_id=user_id, flight_id=booking_data.flight_id)
        saved_booking = self.booking_repository.save_booking(booking)
        time.sleep(1)

        if saved_booking:
            logger.info(f"Booking {saved_booking.id} created for user {user_id}, flight {booking_data.flight_id}")
            return BookingDTO.from_model(saved_booking)
        else:
            logger.error(f"Failed to create booking for user {user_id}, flight {booking_data.flight_id}")
            return None
    
    def get_booking_task_status(self, task_id: str) -> Optional[TaskStatus]:
        """Get the status of an async booking task"""
        if not self.task_manager:
            return None
        return self.task_manager.get_task_status(task_id)

    def get_booking(self, booking_id: int) -> Optional[Booking]:
        """Retrieve a booking by ID."""
        if booking_id <= 0:
            return None
        return self.booking_repository.get_booking_by_id(booking_id)

    def get_user_bookings(self, user_id: int, page: int = 1, per_page: int = 10) -> BookingPaginationResult:
        """Retrieve all bookings for a user with pagination."""
        if user_id <= 0:
            return {'bookings': [], 'page': 1, 'per_page': per_page, 'total': 0, 'pages': 0}
        
        if page < 1:
            page = 1
        if per_page < 1:
            per_page = 10
        if per_page > 100:  # Limit max items per page
            per_page = 100
        
        return self.booking_repository.get_bookings_by_user(user_id, page, per_page)

    def get_all_bookings(self, page: int = 1, per_page: int = 10) -> BookingPaginationResult:
        """Retrieve all bookings with pagination."""
        if page < 1:
            page = 1
        if per_page < 1:
            per_page = 10
        if per_page > 100:  # Limit max items per page
            per_page = 100
        
        return self.booking_repository.get_all_bookings(page, per_page)

    def get_uid_bookings_by_flight_id(self, flight_id: int) -> List[int]:
        """Get list of user IDs who have active bookings for a flight."""
        if flight_id <= 0:
            return []
        
        return self.booking_repository.get_uid_bookings_by_flight_id(flight_id)

    def delete_booking(self, booking_id: int) -> bool:
        """Delete a booking by ID with validation."""
        if booking_id <= 0:
            return False
        
        booking = self.booking_repository.get_booking_by_id(booking_id)
        if not booking:
            return False
        
        # Can only cancel bookings at least 24 hours before departure
        flight = booking.flight
        if flight:
            time_until_departure = flight.departure_time - datetime.now()
            if time_until_departure < timedelta(hours=24):
                return False  # Too close to departure time
            
            # Can't cancel if flight has already departed
            if flight.departure_time <= datetime.now():
                return False
        
        return self.booking_repository.delete_booking(booking_id)
