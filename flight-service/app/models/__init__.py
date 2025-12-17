# Import all models to register them
from .users import User, Session
from .flights import Airport, Airline, Flight, Booking
from .common import UserRole, GenderType, FlightStatus

__all__ = ['User', 'Session', 'Airport', 'Airline', 'Flight', 'Booking', 'UserRole', 'GenderType', 'FlightStatus']