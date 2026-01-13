from marshmallow import Schema, fields, validate


class BookingCreateDTO(Schema):
    """DTO for creating a new booking"""
    flight_id = fields.Int(required=True, validate=validate.Range(min=1))


class BookingUpdateDTO(Schema):
    """DTO for updating booking information"""
    rating = fields.Int(required=False, validate=validate.Range(min=1, max=5))


class BookingResponseDTO(Schema):
    """DTO for booking response"""
    id = fields.Int()
    user_id = fields.Int()
    flight_id = fields.Int()
    flight = fields.Nested('FlightResponseDTO', exclude=['bookings'])
    purchased_at = fields.DateTime()
    rating = fields.Int()


class BookingWithUserDTO(Schema):
    """DTO for booking with user information (for admin view)"""
    id = fields.Int()
    user_id = fields.Int()
    user_name = fields.Str()
    user_email = fields.Str()
    flight_id = fields.Int()
    flight_name = fields.Str()
    rating = fields.Int()
    purchased_at = fields.DateTime()
