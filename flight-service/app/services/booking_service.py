from typing import Optional
from datetime import datetime, timedelta, timezone
from ..domain.models.flights import Booking
from app.domain.interfaces.repositories.ibooking_repository import BookingPaginationResult, IBookingRepository
from app.domain.interfaces.repositories.iflight_repository import IFlightRepository
from app.domain.interfaces.services.booking_service_interface import BookingServiceInterface
from app.domain.dtos.booking_dto import BookingCreateDTO
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

    def create_booking(self, user_id: int, booking_data: BookingCreateDTO) -> Optional[str]:
        """
        Create a booking
        Returns task_id for tracking the booking process
        """
        if not self.task_manager:
            logger.warning("Task manager not available, falling back to synchronous booking")
            return None
        
        if user_id <= 0 or booking_data.flight_id <= 0:
            return None
        
        flight = self.flight_repository.get_flight_by_id(booking_data.flight_id)
        if not flight:
            return None
        
        if flight.status != FlightStatus.APPROVED:
            return None
        
        if flight.departure_time <= datetime.now(timezone.utc):
            return None
        
        available_seats = self.flight_repository.get_available_seats(booking_data.flight_id)
        if available_seats <= 0:
            return None
        
        user_bookings = self.booking_repository.get_bookings_by_user(user_id, page=1, per_page=1000)
        for existing_booking in user_bookings.get('bookings', []):
            if existing_booking.flight_id == booking_data.flight_id:
                return None
        
        # Submit to background task queue
        task_id = self.task_manager.submit_task(
            self._process_booking_async,
            user_id=user_id,
            flight_id=booking_data.flight_id
        )
        
        logger.info(f"Booking task {task_id} submitted for user {user_id}, flight {booking_data.flight_id}")
        return task_id
    
    def _process_booking_async(self, user_id: int, flight_id: int) -> dict:
        """
        Internal method to process booking
        This simulates a long-running process
        """
        try:
            logger.info(f"Processing async booking for user {user_id}, flight {flight_id}")
            
            # Simulate long processing time
            time.sleep(5)  # 5 seconds - adjust for testing
            
            booking = Booking(user_id=user_id, flight_id=flight_id)
            saved_booking = self.booking_repository.save_booking(booking)
            
            if saved_booking:
                logger.info(f"Booking {saved_booking.id} completed for user {user_id}")
                return {
                    'success': True,
                    'booking_id': saved_booking.id,
                    'flight_id': flight_id,
                    'user_id': user_id,
                    'message': 'Booking processed successfully'
                }
            else:
                return {
                    'success': False,
                    'error': 'Failed to save booking',
                    'flight_id': flight_id,
                    'user_id': user_id
                }
        except Exception as e:
            logger.error(f"Async booking processing failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'flight_id': flight_id,
                'user_id': user_id
            }
    
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
