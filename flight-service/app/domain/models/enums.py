from sqlalchemy import Enum

# Enums
Role = Enum('USER', 'MANAGER', 'ADMINISTRATOR', name='role')
Gender = Enum('MALE', 'FEMALE', 'OTHER', name='gender')
FlightStatus = Enum('PENDING', 'APPROVED', 'REJECTED', 'CANCELLED', 'COMPLETED', name='flight_status')