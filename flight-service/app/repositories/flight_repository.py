from typing import Optional, List, Dict
from datetime import datetime
from sqlalchemy import func
from ..domain.models.flights import Booking, Flight
from ..domain.models.enums import FlightStatus
from .. import db
from app.domain.interfaces.repositories.iflight_repository import IFlightRepository, FlightPaginationResult
from app.domain.types.repository_types import FlightUpdateData
from app.utils.logger_service import get_logger, LoggerService

logger = get_logger(__name__)


class SqlAlchemyFlightRepository(IFlightRepository):
    def save_flight(self, flight: Flight) -> Flight:
        LoggerService.log_database_operation(logger, 'INSERT', 'flights',
                                           flight_name=flight.flight_name,
                                           status=flight.status.value)
        db.session.add(flight)
        db.session.commit()
        db.session.refresh(flight)
        LoggerService.log_with_context(logger, 'DEBUG', 'Flight saved to database',
                                     flight_id=flight.flight_id)
        return flight
    
    def get_flight_by_id(self, flight_id: int) -> Optional[Flight]:
        LoggerService.log_database_operation(logger, 'SELECT', 'flights',
                                           flight_id=flight_id)
        flight = Flight.query.options(
            db.joinedload(Flight.airline),
            db.joinedload(Flight.departure_airport),
            db.joinedload(Flight.arrival_airport)
        ).get(flight_id)
        if flight:
            LoggerService.log_with_context(logger, 'DEBUG', 'Flight retrieved from database',
                                         flight_id=flight_id,
                                         found=True)
        else:
            LoggerService.log_with_context(logger, 'DEBUG', 'Flight not found in database',
                                         flight_id=flight_id,
                                         found=False)
        return flight

    def get_all_flights(self, page: int = 1, per_page: int = 10, filters: Optional[Dict] = None) -> FlightPaginationResult:
        query = Flight.query.options(
            db.joinedload(Flight.airline),
            db.joinedload(Flight.departure_airport),
            db.joinedload(Flight.arrival_airport)
        )

        if filters:
            if filters.get('flight_name'):
                search_filter = f"%{filters['flight_name']}%"
                query = query.filter(Flight.flight_name.ilike(search_filter))

            if filters.get('airline_id'):
                query = query.filter_by(airline_id=filters['airline_id'])

            if filters.get('status'):
                query = query.filter_by(status=filters['status'])

            if filters.get('departure_airport_id'):
                query = query.filter_by(departure_airport_id=filters['departure_airport_id'])

            if filters.get('arrival_airport_id'):
                query = query.filter_by(arrival_airport_id=filters['arrival_airport_id'])

            if filters.get('min_price'):
                query = query.filter(Flight.price >= filters['min_price'])

            if filters.get('max_price'):
                query = query.filter(Flight.price <= filters['max_price'])

            if filters.get('departure_date'):
                departure_date = filters['departure_date']
                query = query.filter(
                    func.date(Flight.departure_time) == departure_date
                )

        total = query.count()
        orms = query.offset((page - 1) * per_page).limit(per_page).all()
        
        # Calculate available_seats for each flight
        flights = []
        for orm in orms:
            booked_seats = Booking.query.filter_by(flight_id=orm.flight_id).count()
            orm.available_seats = orm.total_seats - booked_seats
            flights.append(orm)
        
        pages = (total + per_page - 1) // per_page

        return {
            'flights': flights,
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': pages
        }

    def update_flight(self, flight: Flight) -> Optional[Flight]:
        """Update flight entity"""
        try:
            db.session.merge(flight)
            db.session.commit()
            db.session.refresh(flight)
            return flight
        except Exception:
            db.session.rollback()
            return None

    def update_flight_status(self, flight_id: int, status: str, rejection_reason: Optional[str] = None, 
                            approved_by: Optional[int] = None) -> bool:
        """Update flight status with optional rejection reason and approver"""
        flight = Flight.query.get(flight_id)
        if not flight:
            return False
        flight.status = FlightStatus[status]
        if rejection_reason:
            flight.rejection_reason = rejection_reason
        if approved_by:
            flight.approved_by = approved_by
        flight.updated_at = db.func.current_timestamp()
        db.session.commit()
        return True

    def update_flight_details(self, flight_id: int, data: FlightUpdateData) -> Optional[Flight]:
        from datetime import timedelta
        
        flight = Flight.query.get(flight_id)
        if not flight:
            return None
        update_data = {k: v for k, v in data.items() if v is not None}
        
        # Track if we need to recalculate arrival_time
        duration_changed = False
        departure_changed = False
        
        for key, value in update_data.items():
            if hasattr(flight, key):
                # Convert flight_duration from minutes (int) to timedelta for database
                if key == 'flight_duration' and isinstance(value, int):
                    setattr(flight, key, timedelta(minutes=value))
                    duration_changed = True
                elif key == 'departure_time':
                    setattr(flight, key, value)
                    departure_changed = True
                else:
                    setattr(flight, key, value)
        
        # Recalculate arrival_time if departure_time or flight_duration changed
        if duration_changed or departure_changed:
            flight.arrival_time = flight.departure_time + flight.flight_duration
        
        db.session.commit()
        return flight

    def get_available_seats(self, flight_id: int) -> int:
        flight = Flight.query.get(flight_id)
        if not flight:
            return 0
        booked_seats = Booking.query.filter_by(flight_id=flight_id).count()
        return flight.total_seats - booked_seats
    
    def delete_flight(self, flight_id: int) -> bool:
        flight = Flight.query.get(flight_id)
        if not flight:
            return False
        db.session.delete(flight)
        db.session.commit()
        return True
    
    def get_flights_by_status(self, status: str, page: int = 1, per_page: int = 10) -> FlightPaginationResult:
        """Get flights filtered by status"""
        query = Flight.query.options(
            db.joinedload(Flight.airline),
            db.joinedload(Flight.departure_airport),
            db.joinedload(Flight.arrival_airport)
        ).filter_by(status=FlightStatus[status])
        
        total = query.count()
        flights = query.offset((page - 1) * per_page).limit(per_page).all()
        pages = (total + per_page - 1) // per_page
        
        return {
            'flights': flights,
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': pages
        }
    
    def get_flights_to_start(self, current_time: datetime) -> List[Flight]:
        """Get approved flights that should start"""
        return Flight.query.filter(
            Flight.status == FlightStatus.APPROVED,
            Flight.departure_time <= current_time
        ).all()
    
    def get_flights_to_complete(self, current_time: datetime) -> List[Flight]:
        """Get in-progress flights that should complete"""
        return Flight.query.filter(
            Flight.status == FlightStatus.IN_PROGRESS,
            Flight.arrival_time <= current_time
        ).all()
    
    def get_flight_price(self, flight_id: int) -> Optional[float]:
        """Get the price of a flight"""
        flight = Flight.query.get(flight_id)
        if not flight:
            return None
        return flight.price