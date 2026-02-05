from typing import Optional, Dict, cast
from datetime import datetime, timezone
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
    FlightUpdateDTO)
from ..domain.types.websocket_types import FlightNotificationData
from ..domain.types.repository_types import FlightUpdateData

from dataclasses import asdict
from app.utils.logger_service import get_logger, LoggerService

logger = get_logger(__name__)


class FlightService(FlightServiceInterface):
    """Service layer for flight operations with comprehensive business logic validation."""
    
    def __init__(self, flight_repository: IFlightRepository, 
                 airport_repository: IAirportRepository,
                 airline_repository: IAirlineRepository,
                 socket_manager=None):
        self.flight_repository = flight_repository
        self.airport_repository = airport_repository
        self.airline_repository = airline_repository
        self.socket_manager = socket_manager

    def create_flight(self, data: FlightCreateDTO, created_by: int) -> Optional[Flight]:
        """Create a new flight with comprehensive validation."""
        LoggerService.log_service_call(logger, 'FlightService', 'create_flight',
                                      flight_name=data.flight_name,
                                      created_by=created_by)
        
        if data.departure_airport_id == data.arrival_airport_id:
            LoggerService.log_with_context(logger, 'WARNING', 
                                         'Flight creation failed: same departure and arrival airport',
                                         airport_id=data.departure_airport_id)
            return None
        if not self.airport_repository.get_airport_by_id(data.departure_airport_id):
            LoggerService.log_with_context(logger, 'WARNING',
                                         'Flight creation failed: invalid departure airport',
                                         airport_id=data.departure_airport_id)
            return None
        if not self.airport_repository.get_airport_by_id(data.arrival_airport_id):
            LoggerService.log_with_context(logger, 'WARNING',
                                         'Flight creation failed: invalid arrival airport',
                                         airport_id=data.arrival_airport_id)
            return None
        if not self.airline_repository.get_airline_by_id(data.airline_id):
            LoggerService.log_with_context(logger, 'WARNING',
                                         'Flight creation failed: invalid airline',
                                         airline_id=data.airline_id)
            return None
        if data.departure_time <= datetime.now(timezone.utc):
            LoggerService.log_with_context(logger, 'WARNING',
                                         'Flight creation failed: departure time in the past',
                                         departure_time=data.departure_time.isoformat())
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
            created_by=created_by,
            status=FlightStatus.PENDING
        )
        
        try:
            saved_flight = self.flight_repository.save_flight(flight)
            
            LoggerService.log_business_event(logger, 'FLIGHT_CREATED_IN_SERVICE',
                                           flight_id=saved_flight.flight_id,
                                           flight_name=saved_flight.flight_name,
                                           status=saved_flight.status.value)
            
            # Notify admins via WebSocket about new pending flight
            if self.socket_manager:
                flight_data: FlightNotificationData = {
                    'flight_id': saved_flight.flight_id,
                    'flight_name': saved_flight.flight_name,
                    'status': saved_flight.status.value,
                    'departure_time': saved_flight.departure_time.isoformat()
                }
                self.socket_manager.notify_new_flight(flight_data)
                LoggerService.log_with_context(logger, 'INFO',
                                             'Notified admins about new flight',
                                             flight_id=saved_flight.flight_id)
            
            return saved_flight
        except Exception as e:
            LoggerService.log_error(logger, e, {'operation': 'create_flight', 'flight_name': data.flight_name})
            return None

    def update_flight(self, flight_id: int, data: FlightUpdateDTO) -> Optional[Flight]:
        """Update a flight with validation."""
        if flight_id <= 0:
            return None
        
        flight = self.flight_repository.get_flight_by_id(flight_id)
        if not flight:
            return None
        
        # Only allow updates to PENDING or REJECTED flights
        if flight.status not in [FlightStatus.PENDING, FlightStatus.REJECTED]:
            logger.warning(f"Cannot update flight {flight_id} with status {flight.status}")
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
        
        update_data: FlightUpdateData = cast(FlightUpdateData, {k: v for k, v in asdict(data).items() if v is not None})

        try:
            return self.flight_repository.update_flight_details(flight_id, update_data)
        except Exception as e:
            logger.error(f"Error updating flight: {str(e)}")
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

    def update_flight_status(self, flight_id: int, data: FlightStatusUpdateDTO, admin_id: int) -> Optional[Flight]:
        """Update flight status (approve/reject/cancel) by admin."""
        if flight_id <= 0:
            return None
        
        flight = self.flight_repository.get_flight_by_id(flight_id)
        if not flight:
            return None
        
        # Validate status transition
        new_status = FlightStatus[data.status]
        if not FlightValidator.validate_status_transition(flight.status, new_status, data.rejection_reason):
            logger.warning(f"Invalid status transition from {flight.status} to {new_status}")
            return None
        
        success = self.flight_repository.update_flight_status(
            flight_id, 
            data.status, 
            data.rejection_reason, 
            admin_id
        )
        
        if not success:
            return None
        
        updated_flight = self.flight_repository.get_flight_by_id(flight_id)
        
        # Notify manager via WebSocket about status update (approved/rejected)
        if self.socket_manager and updated_flight:
            flight_data: FlightNotificationData = {
                'flight_id': updated_flight.flight_id,
                'flight_name': updated_flight.flight_name,
                'status': updated_flight.status.value,
                'departure_time': updated_flight.departure_time.isoformat()
            }
            self.socket_manager.notify_flight_status_update(updated_flight.created_by, flight_data)
            logger.info(f"Notified manager about flight {flight_id} status update")
        
        return updated_flight

    def cancel_flight(self, flight_id: int, admin_id: int) -> Optional[Flight]:
        """Cancel an approved flight and notify users."""
        flight = self.flight_repository.get_flight_by_id(flight_id)
        if not flight:
            logger.warning(f"Flight {flight_id} not found")
            return None
        
        # Only allow cancellation of approved flights that haven't started or completed
        if flight.status not in [FlightStatus.APPROVED]:
            logger.warning(f"Cannot cancel flight {flight_id} with status {flight.status}")
            return None
        
        if flight.actual_start_time:
            logger.warning(f"Cannot cancel flight {flight_id} that has already started")
            return None
        
        success = self.flight_repository.update_flight_status(
            flight_id, 
            'CANCELLED', 
            None, 
            admin_id
        )
        
        if not success:
            return None
        
        updated_flight = self.flight_repository.get_flight_by_id(flight_id)
        
        # Get users who booked this flight for potential refund processing
        user_ids = self.flight_repository.get_user_bookings_for_flight(flight_id)
        
        if user_ids:
            logger.info(f"Flight {flight_id} cancelled. {len(user_ids)} users affected. Server will handle notifications.")
        
        if self.socket_manager and updated_flight:
            flight_data: FlightNotificationData = {
                'flight_id': updated_flight.flight_id,
                'flight_name': updated_flight.flight_name,
                'status': 'CANCELLED',
                'departure_time': updated_flight.departure_time.isoformat()
            }
            self.socket_manager.notify_flight_cancelled(flight_data)
            logger.info(f"Broadcasted cancellation of flight {flight_id}")
        
        return updated_flight

    def delete_flight(self, flight_id: int) -> bool:
        """Delete a flight by ID (admin only)."""
        if flight_id <= 0:
            return False
        
        flight = self.flight_repository.get_flight_by_id(flight_id)
        if not flight:
            return False
        
        return self.flight_repository.delete_flight(flight_id)

    def get_available_seats(self, flight_id: int) -> int:
        """Get available seats for a flight."""
        if flight_id <= 0:
            return 0
        return self.flight_repository.get_available_seats(flight_id)
    
    def get_flights_by_tab(self, tab: str, page: int, per_page: int, filters: Optional[Dict] = None) -> FlightPaginationResult:
        """
        Get flights by tab:
        - upcoming: APPROVED flights that haven't started
        - in-progress: IN_PROGRESS flights
        - completed: COMPLETED and CANCELLED flights
        """
        current_time = datetime.now(timezone.utc)
        
        if tab == 'upcoming':
            # Approved flights that haven't started yet
            if filters is None:
                filters = {}
            filters['status'] = FlightStatus.APPROVED.value
            result = self.flight_repository.get_all_flights(page, per_page, filters)
            # Filter out flights that have already started
            result['flights'] = [f for f in result['flights'] if f.departure_time > current_time]
            result['total'] = len(result['flights'])
            result['pages'] = (result['total'] + per_page - 1) // per_page
            return result
        elif tab == 'in-progress':
            return self.flight_repository.get_flights_by_status('IN_PROGRESS', page, per_page)
        elif tab == 'completed':
            # Get both completed and cancelled flights
            completed = self.flight_repository.get_flights_by_status('COMPLETED', 1, 1000)
            cancelled = self.flight_repository.get_flights_by_status('CANCELLED', 1, 1000)
            all_flights = completed['flights'] + cancelled['flights']
            
            total = len(all_flights)
            start = (page - 1) * per_page
            end = start + per_page
            paginated_flights = all_flights[start:end]
            pages = (total + per_page - 1) // per_page
            
            return {
                'flights': paginated_flights,
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': pages
            }
        else:
            return self.get_all_flights(page, per_page, filters)
    
    def get_flight_remaining_time(self, flight_id: int) -> Optional[Dict]:
        """Get remaining time for in-progress flight."""
        flight = self.flight_repository.get_flight_by_id(flight_id)
        if not flight or flight.status != FlightStatus.IN_PROGRESS:
            return None
        
        current_time = datetime.now(timezone.utc)
        remaining = flight.arrival_time - current_time
        
        if remaining.total_seconds() < 0:
            return {
                'flight_id': flight_id,
                'remaining_seconds': 0,
                'remaining_minutes': 0,
                'status': 'completed'
            }
        
        return {
            'flight_id': flight_id,
            'remaining_seconds': int(remaining.total_seconds()),
            'remaining_minutes': int(remaining.total_seconds() / 60),
            'arrival_time': flight.arrival_time.isoformat(),
            'status': 'in_progress'
        }

