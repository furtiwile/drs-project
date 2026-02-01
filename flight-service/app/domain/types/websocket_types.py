from typing import TypedDict


class FlightNotificationData(TypedDict):
    """Type definition for flight notification data sent via WebSocket"""
    flight_id: int
    flight_name: str
    status: str
    departure_time: str
