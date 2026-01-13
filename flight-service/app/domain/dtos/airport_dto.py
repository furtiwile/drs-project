from marshmallow import Schema, fields, validate


class AirportCreateDTO(Schema):
    """DTO for creating a new airport"""
    name = fields.Str(required=True, validate=validate.Length(min=3, max=255))
    code = fields.Str(required=True, validate=validate.Length(min=3, max=10))


class AirportUpdateDTO(Schema):
    """DTO for updating airport information"""
    name = fields.Str(required=False, validate=validate.Length(min=3, max=255))
    code = fields.Str(required=False, validate=validate.Length(min=3, max=10))


class AirportResponseDTO(Schema):
    """DTO for airport response"""
    id = fields.Int()
    name = fields.Str()
    code = fields.Str()
    created_at = fields.DateTime()
