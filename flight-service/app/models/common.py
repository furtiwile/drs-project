from sqlalchemy import Enum

# Enums
UserRole = Enum('USER', 'MANAGER', 'ADMINISTRATOR', name='user_role')
GenderType = Enum('M', 'F', 'OTHER', name='gender_type')
FlightStatus = Enum('PENDING', 'APPROVED', 'REJECTED', 'CANCELLED', 'COMPLETED', name='flight_status')