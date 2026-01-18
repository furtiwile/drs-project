from enum import Enum


class FlightStatus(Enum):
    """Enumeration of possible flight statuses."""
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"