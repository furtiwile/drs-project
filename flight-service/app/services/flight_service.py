from typing import Optional, Dict, Any, cast
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from ..domain.models.flights import Flight
from app.domain.interfaces.repositories.iflight_repository import IFlightRepository
from app.domain.interfaces.repositories.iairport_repository import IAirportRepository
from app.domain.interfaces.repositories.iairline_repository import IAirlineRepository
from app.domain.interfaces.services.flight_service_interface import FlightServiceInterface
from app.domain.interfaces.repositories.iflight_repository import FlightPaginationResult
from ..domain.models.enums import FlightStatus
from ..domain.validators.flight_validator import FlightValidator
from ..domain.dtos.flight_dto import (
    FlightCreateDTO,
    FlightStatusUpdateDTO,
    FlightUpdateDTO,
    FlightResponseDTO)

from dataclasses import asdict

class FlightService(FlightServiceInterface):
    """Service layer for flight operations with comprehensive business logic validation."""
    
    def __init__(self, flight_repository: IFlightRepository, 
                 airport_repository: IAirportRepository,
                 airline_repository: IAirlineRepository):
        self.flight_repository = flight_repository
        self.airport_repository = airport_repository
        self.airline_repository = airline_repository

    def create_flight(self, data: FlightCreateDTO) -> Optional[Flight]:
        """Create a new flight with comprehensive validation."""
        if data.departure_airport_id == data.arrival_airport_id:
            return None
        if not self.airport_repository.get_airport_by_id(data.departure_airport_id):
            return None
        if not self.airport_repository.get_airport_by_id(data.arrival_airport_id):
            return None
        if not self.airline_repository.get_airline_by_id(data.airline_id):
            return None
        if data.departure_time <= datetime.now(timezone.utc):
            return None
        
        flight = Flight(
            flight_name=data.flight_name,
            airline_id=data.airline_id,
            flight_distance_km=data.flight_distance_km,
            flight_duration=data.flight_duration,
            departure_time=data.departure_time,
            departure_airport_id=data.departure_airport_id,
            arrival_airport_id=data.arrival_airport_id,
            price=float(data.price),
            total_seats=data.total_seats,
            available_seats=data.total_seats
        )
        
        try:
            saved_flight = self.flight_repository.save_flight(flight)
            
            return saved_flight
        except Exception:
            return None

    def update_flight(self, flight_id: int, data: FlightUpdateDTO) -> Optional[Flight]:
        """Update a flight with validation."""
        if flight_id <= 0:
            return None
        
        flight = self.flight_repository.get_flight_by_id(flight_id)
        if not flight:
            return None
        
        if data.departure_airport_id is not None and not self.airport_repository.get_airport_by_id(data.departure_airport_id):
            return None
        if data.arrival_airport_id is not None and not self.airport_repository.get_airport_by_id(data.arrival_airport_id):
            return None
        if data.airline_id is not None and not self.airline_repository.get_airline_by_id(data.airline_id):
            return None
        
        # Validate departure and arrival airports are different if both provided
        dep_id = data.departure_airport_id if data.departure_airport_id is not None else flight.departure_airport_id
        arr_id = data.arrival_airport_id if data.arrival_airport_id is not None else flight.arrival_airport_id
        if dep_id == arr_id:
            return None
        
        if data.departure_time is not None and data.departure_time <= datetime.now(timezone.utc):
            return None
        
        update_data = {k: v for k, v in asdict(data).items() if v is not None}

        try:
            return self.flight_repository.update_flight_details(flight_id, update_data)
        except Exception:
            return None

    def get_flight(self, flight_id: int) -> Optional[Flight]:
        """Retrieve a flight by ID."""
        if flight_id <= 0:
            return None
        return self.flight_repository.get_flight_by_id(flight_id)

    def get_all_flights(self, page: int = 1, per_page: int = 10, filters: Optional[Dict] = None) -> FlightPaginationResult:
        """Retrieve all flights with pagination and filters."""
        if page < 1:
            page = 1
        if per_page < 1:
            per_page = 10
        if per_page > 100:  # Limit max items per page
            per_page = 100
        
        filters = FlightValidator.validate_filters(filters)
        
        return self.flight_repository.get_all_flights(page, per_page, filters)

    def update_flight_status(self, flight_id: int, data: FlightStatusUpdateDTO) -> bool:
        """Update flight status with validation."""
        if flight_id <= 0:
            return False
        
        flight = self.flight_repository.get_flight_by_id(flight_id)
        if not flight:
            return False
        
        if not FlightValidator.validate_status_transition(flight.status, FlightStatus(data.status), data.rejection_reason):
            return False
        
        old_status = flight.status
        success = self.flight_repository.update_flight(flight_id, data.status, data.rejection_reason)
        
        return success

    def delete_flight(self, flight_id: int) -> bool:
        """Delete a flight by ID."""
        if flight_id <= 0:
            return False
        
        flight = self.flight_repository.get_flight_by_id(flight_id)
        if not flight:
            return False
        
        if flight.status not in [FlightStatus.PENDING.value, FlightStatus.REJECTED.value]:
            return False
        
        return self.flight_repository.delete_flight(flight_id)

    def get_available_seats(self, flight_id: int) -> int:
        """Get available seats for a flight."""
        if flight_id <= 0:
            return 0
        return self.flight_repository.get_available_seats(flight_id)
