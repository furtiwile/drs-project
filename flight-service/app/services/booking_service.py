from typing import Optional, Dict
from datetime import datetime, timedelta
from ..domain.models.flights import Booking
from app.domain.interfaces.repositories.ibooking_repository import BookingPaginationResult, IBookingRepository
from app.domain.interfaces.repositories.iflight_repository import IFlightRepository
from app.domain.interfaces.services.booking_service_interface import BookingServiceInterface
from app.domain.dtos.booking_dto import BookingCreateDTO, BookingResponseDTO
from app.domain.models.flights import FlightStatus
import time


class BookingService(BookingServiceInterface):
    """Service layer for booking operations with comprehensive business logic validation."""
    
    def __init__(self, booking_repository: IBookingRepository, flight_repository: IFlightRepository):
        self.booking_repository = booking_repository
        self.flight_repository = flight_repository

    def create_booking(self, user_id: int, data: BookingCreateDTO) -> Optional[Booking]:
        """Create a new booking with comprehensive validation."""
        if user_id <= 0 or data.flight_id <= 0:
            return None
        
        flight = self.flight_repository.get_flight_by_id(data.flight_id)
        if not flight:
            return None
        
        if flight.status != FlightStatus.APPROVED:
            return None
        
        # Can't book flights that have already departed
        if flight.departure_time <= datetime.now():
            return None
        
        # # Can't book flights too close to departure (e.g., within 2 hours)
        # # In theory.. We can add this check later on if needed
        # time_until_departure = flight.departure_time - datetime.now()
        # if time_until_departure < timedelta(hours=2):
        #     return None
        
        available_seats = self.flight_repository.get_available_seats(data.flight_id)
        if available_seats <= 0:
            return None
        
        # Check if user already has a booking for this flight
        user_bookings = self.booking_repository.get_bookings_by_user(user_id, page=1, per_page=1000)
        for existing_booking in user_bookings.get('bookings', []):
            if existing_booking.flight_id == data.flight_id:
                return None  # User already has a booking for this flight
        
        try:
            print(f"Starting async booking processing for user {user_id}, flight {data.flight_id}")
            time.sleep(3)  # Simulate processing delay (adjust for testing)
            
            booking = Booking(user_id=user_id, flight_id=data.flight_id)
            saved_booking = self.booking_repository.save_booking(booking)
            
            if saved_booking:
                print(f"Booking confirmed for user {user_id}")
            
            return saved_booking
        except Exception as e:
            print(f"Booking creation failed: {str(e)}")
            return None

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
