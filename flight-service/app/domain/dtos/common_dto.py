from marshmallow import Schema, fields, validate
from dataclasses import dataclass
from typing import Optional


class PaginationDTO(Schema):
    """DTO for pagination parameters"""
    page = fields.Int(required=False, missing=1, validate=validate.Range(min=1))
    per_page = fields.Int(required=False, missing=10, validate=validate.Range(min=1, max=100))


class MessageResponseDTO(Schema):
    """DTO for simple message responses"""
    message = fields.Str(required=True)
    success = fields.Bool(required=True)


@dataclass
class ErrorResponseDTO:
    """Data transfer object for error responses"""
    error: str
    status_code: int = 400
    details: Optional[dict] = None


@dataclass
class SuccessResponseDTO:
    """Data transfer object for success responses"""
    message: str
    success: bool = True
    data: Optional[dict] = None

