from sqlalchemy import CheckConstraint
from .. import db
from .common import FlightStatus

class Airport(db.Model):
    __bind_key__ = 'flights'
    __tablename__ = 'airports'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(10), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class Airline(db.Model):
    __bind_key__ = 'flights'
    __tablename__ = 'airlines'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class Flight(db.Model):
    __bind_key__ = 'flights'
    __tablename__ = 'flights'

    flight_id = db.Column(db.Integer, primary_key=True)
    flight_name = db.Column(db.String(255), nullable=False)
    airline_id = db.Column(db.Integer, db.ForeignKey('airlines.id', ondelete='CASCADE'))
    flight_distance_km = db.Column(db.Integer, nullable=False)
    flight_duration = db.Column(db.Interval, nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    departure_airport_id = db.Column(db.Integer, db.ForeignKey('airports.id', ondelete='CASCADE'))
    arrival_airport_id = db.Column(db.Integer, db.ForeignKey('airports.id', ondelete='CASCADE'))
    created_by = db.Column(db.Integer, nullable=False)  # Reference to user id from users_db
    price = db.Column(db.Numeric(10, 2), nullable=False)
    total_seats = db.Column(db.Integer, nullable=False)
    status = db.Column(FlightStatus, default='PENDING')
    rejection_reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relationships
    airline = db.relationship('Airline', backref='flights')
    departure_airport = db.relationship('Airport', foreign_keys=[departure_airport_id], backref='departing_flights')
    arrival_airport = db.relationship('Airport', foreign_keys=[arrival_airport_id], backref='arriving_flights')

class Booking(db.Model):
    __bind_key__ = 'flights'
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  # Reference to user id from users_db
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.flight_id', ondelete='CASCADE'))
    purchased_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    rating = db.Column(db.SmallInteger)

    # Add check constraint for rating
    __table_args__ = (
        CheckConstraint('rating IS NULL OR (rating >= 1 AND rating <= 5)', name='check_rating'),
    )

    # Relationship
    flight = db.relationship('Flight', backref='bookings')