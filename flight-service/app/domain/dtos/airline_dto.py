from marshmallow import Schema, fields, validate


class AirlineCreateDTO(Schema):
    """DTO for creating a new airline"""
    name = fields.Str(required=True, validate=validate.Length(min=2, max=255))


class AirlineUpdateDTO(Schema):
    """DTO for updating airline information"""
    name = fields.Str(required=False, validate=validate.Length(min=2, max=255))


class AirlineResponseDTO(Schema):
    """DTO for airline response"""
    id = fields.Int()
    name = fields.Str()
    created_at = fields.DateTime()
