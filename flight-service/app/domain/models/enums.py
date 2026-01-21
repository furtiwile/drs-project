from enum import Enum

# Enums
class Role(Enum):
    USER = "USER"
    MANAGER = "MANAGER"
    ADMINISTRATOR = "ADMINISTRATOR"

class Gender(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"

class FlightStatus(Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    IN_PROGRESS = "IN_PROGRESS"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"