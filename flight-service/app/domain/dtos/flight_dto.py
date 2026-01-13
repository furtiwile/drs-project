from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import datetime, timedelta


class FlightCreateDTO(Schema):
    """DTO for creating a new flight"""
    flight_name = fields.Str(required=True, validate=validate.Length(min=3, max=255))
    airline_id = fields.Int(required=True, validate=validate.Range(min=1))
    flight_distance_km = fields.Int(required=True, validate=validate.Range(min=1))
    flight_duration = fields.Int(required=True, validate=validate.Range(min=1))  # in minutes
    departure_time = fields.DateTime(required=True)
    departure_airport_id = fields.Int(required=True, validate=validate.Range(min=1))
    arrival_airport_id = fields.Int(required=True, validate=validate.Range(min=1))
    price = fields.Decimal(required=True, validate=validate.Range(min=0.01))
    total_seats = fields.Int(required=True, validate=validate.Range(min=1))

    @validates('departure_time')
    def validate_departure_time(self, value):
        if value < datetime.now():
            raise ValidationError('Departure time must be in the future')

    @validates('arrival_airport_id')
    def validate_airports(self, value):
        # Note: actual validation of same airport will be in controller/service
        # This is just placeholder for future logic
        pass


class FlightUpdateDTO(Schema):
    """DTO for updating flight information"""
    flight_name = fields.Str(required=False, validate=validate.Length(min=3, max=255))
    airline_id = fields.Int(required=False, validate=validate.Range(min=1))
    flight_distance_km = fields.Int(required=False, validate=validate.Range(min=1))
    flight_duration = fields.Int(required=False, validate=validate.Range(min=1))  # in minutes
    departure_time = fields.DateTime(required=False)
    departure_airport_id = fields.Int(required=False, validate=validate.Range(min=1))
    arrival_airport_id = fields.Int(required=False, validate=validate.Range(min=1))
    price = fields.Decimal(required=False, validate=validate.Range(min=0.01))
    total_seats = fields.Int(required=False, validate=validate.Range(min=1))
    rejection_reason = fields.Str(required=False)

    @validates('departure_time')
    def validate_departure_time(self, value):
        if value and value < datetime.now():
            raise ValidationError('Departure time must be in the future')


class FlightStatusUpdateDTO(Schema):
    """DTO for updating flight status"""
    status = fields.Str(required=True, validate=validate.OneOf(['APPROVED', 'REJECTED', 'CANCELLED', 'COMPLETED']))
    rejection_reason = fields.Str(required=False)

    @validates('rejection_reason')
    def validate_rejection_reason(self, value):
        status = self.context.get('status')
        if status == 'REJECTED' and not value:
            raise ValidationError('Rejection reason is required when rejecting a flight')


class FlightResponseDTO(Schema):
    """DTO for flight response"""
    flight_id = fields.Int()
    flight_name = fields.Str()
    airline_id = fields.Int()
    airline = fields.Nested('AirlineResponseDTO', only=['id', 'name'])
    flight_distance_km = fields.Int()
    flight_duration = fields.Str()  # Will be formatted as string
    departure_time = fields.DateTime()
    arrival_time = fields.DateTime()
    departure_airport_id = fields.Int()
    departure_airport = fields.Nested('AirportResponseDTO', only=['id', 'name', 'code'])
    arrival_airport_id = fields.Int()
    arrival_airport = fields.Nested('AirportResponseDTO', only=['id', 'name', 'code'])
    created_by = fields.Int()
    price = fields.Decimal(as_string=True)
    total_seats = fields.Int()
    available_seats = fields.Int()
    status = fields.Str()
    rejection_reason = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class FlightFilterDTO(Schema):
    """DTO for filtering flights"""
    flight_name = fields.Str(required=False)
    airline_id = fields.Int(required=False)
    status = fields.Str(required=False, validate=validate.OneOf(['PENDING', 'APPROVED', 'REJECTED', 'CANCELLED', 'COMPLETED']))
    departure_airport_id = fields.Int(required=False)
    arrival_airport_id = fields.Int(required=False)
    min_price = fields.Decimal(required=False)
    max_price = fields.Decimal(required=False)
    departure_date = fields.Date(required=False)
