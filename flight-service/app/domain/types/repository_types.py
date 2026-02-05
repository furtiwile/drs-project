from typing import TypedDict
from decimal import Decimal
from datetime import datetime


class FlightUpdateData(TypedDict, total=False):
    """Type definition for flight update data"""
    flight_name: str
    airline_id: int
    flight_distance_km: int
    flight_duration: int
    departure_time: datetime
    departure_airport_id: int
    arrival_airport_id: int
    price: Decimal
    total_seats: int
    rejection_reason: str
