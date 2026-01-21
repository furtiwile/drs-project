from dataclasses import asdict
from typing import Optional, Dict, Any
from sqlalchemy import func
from ..domain.models.flights import Booking, Flight
from .. import db
from app.domain.interfaces.repositories.iflight_repository import IFlightRepository, FlightPaginationResult
from app.domain.dtos.flight_dto import FlightUpdateDTO


class SqlAlchemyFlightRepository(IFlightRepository):
    def save_flight(self, flight: Flight) -> Flight:
        db.session.add(flight)
        db.session.commit()
        db.session.refresh(flight)
        return flight
    
    def get_flight_by_id(self, flight_id: int) -> Optional[Flight]:
        flight = Flight.query.options(
            db.joinedload(Flight.airline),
            db.joinedload(Flight.departure_airport),
            db.joinedload(Flight.arrival_airport)
        ).get(flight_id)
        return flight

    def get_all_flights(self, page: int = 1, per_page: int = 10, filters: Optional[Dict] = None) -> FlightPaginationResult:
        query = Flight.query.options(
            db.joinedload(Flight.airline),
            db.joinedload(Flight.departure_airport),
            db.joinedload(Flight.arrival_airport)
        )

        # Apply filters
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

        # Pagination
        total = query.count()
        orms = query.offset((page - 1) * per_page).limit(per_page).all()
        flights = [orm for orm in orms]
        pages = (total + per_page - 1) // per_page

        return {
            'flights': flights,
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': pages
        }

    def update_flight(self, flight_id: int, status: str, rejection_reason: Optional[str] = None) -> bool:
        flight = Flight.query.get(flight_id)
        if not flight:
            return False
        flight.status = status
        if rejection_reason:
            flight.rejection_reason = rejection_reason
        flight.updated_at = db.func.current_timestamp()
        db.session.commit()
        return True

    def update_flight_details(self, flight_id: int, data: dict[str,Any]) -> Optional[Flight]:
        flight = Flight.query.get(flight_id)
        if not flight:
            return None
        update_data = {k: v for k, v in data.items() if v is not None}
        for key, value in update_data.items():
            if hasattr(flight, key):
                setattr(flight, key, value)
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