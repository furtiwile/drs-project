from typing import List, Optional, Dict
from ..domain.models.flights import Booking, Flight 
from .. import db
from app.domain.interfaces.repositories.ibooking_repository import IBookingRepository, BookingPaginationResult

class SqlAlchemyBookingRepository(IBookingRepository):
    def save_booking(self, booking: Booking) -> Booking:
        db.session.add(booking)
        db.session.commit()
        db.session.refresh(booking)
        return booking
    
    def get_booking_by_id(self, booking_id: int) -> Optional[Booking]:
        booking = Booking.query.options(
            db.joinedload(Booking.flight).joinedload(Flight.airline),
            db.joinedload(Booking.flight).joinedload(Flight.departure_airport),
            db.joinedload(Booking.flight).joinedload(Flight.arrival_airport)
        ).get(booking_id)
        return booking if booking else None

    def get_bookings_by_user(self, user_id: int, page: int = 1, per_page: int = 10) -> BookingPaginationResult:
        query = Booking.query.filter_by(user_id=user_id).options(
            db.joinedload(Booking.flight).joinedload(Flight.airline),
            db.joinedload(Booking.flight).joinedload(Flight.departure_airport),
            db.joinedload(Booking.flight).joinedload(Flight.arrival_airport)
        )

        total = query.count()
        orms = query.offset((page - 1) * per_page).limit(per_page).all()
        bookings = [orm for orm in orms]
        pages = (total + per_page - 1) // per_page

        return {
            'bookings': bookings,
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': pages
        }

    def get_all_bookings(self, page: int = 1, per_page: int = 10) -> BookingPaginationResult:
        query = Booking.query.options(
            db.joinedload(Booking.flight).joinedload(Flight.airline),
            db.joinedload(Booking.flight).joinedload(Flight.departure_airport),
            db.joinedload(Booking.flight).joinedload(Flight.arrival_airport)
        )

        total = query.count()
        orms = query.offset((page - 1) * per_page).limit(per_page).all()
        bookings = [orm for orm in orms]
        pages = (total + per_page - 1) // per_page

        return {
            'bookings': bookings,
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': pages
        }

    def get_bookings_by_flight_id(self, flight_id: int) -> List[Booking]:
        bookings = Booking.query.filter_by(flight_id=flight_id).options(
            db.joinedload(Booking.flight).joinedload(Flight.airline),
            db.joinedload(Booking.flight).joinedload(Flight.departure_airport),
            db.joinedload(Booking.flight).joinedload(Flight.arrival_airport)
        ).all()
        return bookings

    def delete_booking(self, booking_id: int) -> bool:
        booking = Booking.query.get(booking_id)
        if not booking:
            return False
        db.session.delete(booking)
        db.session.commit()
        return True