# Repository instances

from .repositories import (
    SqlAlchemyAirportRepository,
    SqlAlchemyAirlineRepository,
    SqlAlchemyFlightRepository,
    SqlAlchemyBookingRepository
)

airport_repo = SqlAlchemyAirportRepository()
airline_repo = SqlAlchemyAirlineRepository()
flight_repo = SqlAlchemyFlightRepository()
booking_repo = SqlAlchemyBookingRepository()