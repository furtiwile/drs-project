from marshmallow import Schema, fields, validate


class PaginationDTO(Schema):
    """DTO for pagination parameters"""
    page = fields.Int(required=False, missing=1, validate=validate.Range(min=1))
    per_page = fields.Int(required=False, missing=10, validate=validate.Range(min=1, max=100))


class MessageResponseDTO(Schema):
    """DTO for simple message responses"""
    message = fields.Str(required=True)
    success = fields.Bool(required=True)
