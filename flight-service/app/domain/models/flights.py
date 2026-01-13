from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped
from datetime import datetime, timedelta
from typing import Optional
from ... import db
from .enums import FlightStatus

class Airport(db.Model):
    __tablename__ = 'airports'

    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    name: Mapped[str] = db.Column(db.String(255), nullable=False)
    code: Mapped[str] = db.Column(db.String(10), unique=True, nullable=False)
    created_at: Mapped[datetime] = db.Column(db.DateTime, default=db.func.current_timestamp())

class Airline(db.Model):
    __tablename__ = 'airlines'

    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    name: Mapped[str] = db.Column(db.String(255), unique=True, nullable=False)
    created_at: Mapped[datetime] = db.Column(db.DateTime, default=db.func.current_timestamp())

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
    status: Mapped[str] = db.Column(FlightStatus, default='PENDING')
    rejection_reason: Mapped[Optional[str]] = db.Column(db.Text)
    created_at: Mapped[datetime] = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at: Mapped[datetime] = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

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
    rating: Mapped[Optional[int]] = db.Column(db.SmallInteger)

    # Add check constraint for rating
    __table_args__ = (
        CheckConstraint('rating IS NULL OR (rating >= 1 AND rating <= 5)', name='check_rating'),
    )

    # Relationship
    flight = db.relationship('Flight', backref='bookings')