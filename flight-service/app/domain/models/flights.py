from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped
from datetime import datetime, timedelta
from typing import Optional
from ... import db
from .enums import FlightStatus

class Airport(db.Model):
    __tablename__ = 'airports'

    id: Mapped[int] = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = db.Column(db.String(255), nullable=False)
    code: Mapped[str] = db.Column(db.String(10), unique=True, nullable=False)
    created_at: Mapped[datetime] = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, name: str, code: str, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.code = code

class Airline(db.Model):
    __tablename__ = 'airlines'

    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    name: Mapped[str] = db.Column(db.String(255), unique=True, nullable=False)
    created_at: Mapped[datetime] = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, name: str, **kwargs):
        super().__init__(**kwargs)
        self.name = name

class Flight(db.Model):
    __tablename__ = 'flights'

    flight_id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    flight_name: Mapped[str] = db.Column(db.String(255), nullable=False)
    airline_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('airlines.id', ondelete='CASCADE'))
    flight_distance_km: Mapped[int] = db.Column(db.Integer, nullable=False)
    flight_duration: Mapped[timedelta] = db.Column(db.Interval, nullable=False)
    departure_time: Mapped[datetime] = db.Column(db.DateTime, nullable=False)
    arrival_time: Mapped[datetime] = db.Column(db.DateTime, nullable=False)
    departure_airport_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('airports.id', ondelete='CASCADE'))
    arrival_airport_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('airports.id', ondelete='CASCADE'))
    created_by: Mapped[int] = db.Column(db.Integer, nullable=False)  # Reference to user id from users_db
    price: Mapped[float] = db.Column(db.Numeric(10, 2), nullable=False)
    total_seats: Mapped[int] = db.Column(db.Integer, nullable=False)
    status: Mapped[FlightStatus] = db.Column(db.Enum(FlightStatus), default=FlightStatus.PENDING)
    rejection_reason: Mapped[Optional[str]] = db.Column(db.Text)
    created_at: Mapped[datetime] = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at: Mapped[datetime] = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, flight_name: str, airline_id: int, flight_distance_km: int, 
                 flight_duration: int, departure_time: datetime, departure_airport_id: int, 
                 arrival_airport_id: int, price: float, total_seats: int, 
                 available_seats: Optional[int] = None, status: FlightStatus = FlightStatus.PENDING, 
                 rejection_reason: Optional[str] = None, created_by: int = 1, **kwargs):
        super().__init__(**kwargs)
        self.flight_name = flight_name
        self.airline_id = airline_id
        self.flight_distance_km = flight_distance_km
        self.flight_duration = timedelta(minutes=flight_duration)  # Convert minutes to timedelta
        self.departure_time = departure_time
        self.arrival_time = departure_time + self.flight_duration  # Calculate arrival time
        self.departure_airport_id = departure_airport_id
        self.arrival_airport_id = arrival_airport_id
        self.price = price
        self.total_seats = total_seats
        self.status = status
        self.rejection_reason = rejection_reason
        self.created_by = created_by

    # Relationships
    airline = db.relationship('Airline', backref='flights')
    departure_airport = db.relationship('Airport', foreign_keys=[departure_airport_id], backref='departing_flights')
    arrival_airport = db.relationship('Airport', foreign_keys=[arrival_airport_id], backref='arriving_flights')

class Booking(db.Model):
    __tablename__ = 'bookings'

    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    user_id: Mapped[int] = db.Column(db.Integer, nullable=False)  # Reference to user id from users_db
    flight_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('flights.flight_id', ondelete='CASCADE'))
    purchased_at: Mapped[datetime] = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, user_id: int, flight_id: int, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.flight_id = flight_id

    # Relationship
    flight = db.relationship('Flight', backref='bookings')

class Rating(db.Model):
    __tablename__ = 'ratings'

    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    user_id: Mapped[int] = db.Column(db.Integer, nullable=False)  # Reference to user id from users_db
    flight_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('flights.flight_id', ondelete='CASCADE'))
    rating: Mapped[int] = db.Column(db.SmallInteger, nullable=False)
    created_at: Mapped[datetime] = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Add check constraint for rating
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating_value'),
        db.UniqueConstraint('user_id', 'flight_id', name='unique_user_flight_rating'),
    )

    def __init__(self, user_id: int, flight_id: int, rating: int, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.flight_id = flight_id
        self.rating = rating

    # Relationship
    flight = db.relationship('Flight', backref='ratings')