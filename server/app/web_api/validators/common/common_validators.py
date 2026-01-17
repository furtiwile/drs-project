import base64
from datetime import date
import io
import re
from enum import Enum
from PIL import Image
from app.domain.types.validation_result import ValidationResult

EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
ALLOWED_IMAGE_MIME_TYPES = {"image/png", "image/jpeg", "image/jpg", "image/gif"}
MAX_IMAGE_SIZE_BYTES = 1 * 1024 * 1024

def validate_email(email: str, max_length: int | None = None) -> ValidationResult:
    if not email:
        return ValidationResult.fail("Email address is required")
    if not EMAIL_REGEX.match(email):
        return ValidationResult.fail("Invalid email address format")
    if max_length is not None and len(email) > max_length:
        return ValidationResult.fail("Email address too long")
    return ValidationResult.ok()

def validate_password(password: str) -> ValidationResult:
    if not password:
        return ValidationResult.fail("Password is required")
    if len(password.strip()) < 6:
        return ValidationResult.fail("Password must contain at least 6 characters")
    return ValidationResult.ok()

def validate_text(value: str, field_name: str, min_length: int = 1, max_length: int | None = None) -> ValidationResult:
    if value is None:
        return ValidationResult.fail(f"{field_name} is required")
    if len(value.strip()) < min_length:
        return ValidationResult.fail(f"{field_name} must contain at least {min_length} characters")
    if max_length is not None and len(value.strip()) > max_length:
        return ValidationResult.fail(f"{field_name} cannot exceed {max_length} characters")
    return ValidationResult.ok()

def validate_number(value: int | float, field_name: str, min_value: int | float | None = None, max_value: int | float | None = None) -> ValidationResult:
    if value is None:
        return ValidationResult.fail(f"{field_name} is required")
    if not isinstance(value, (int, float)):
        return ValidationResult.fail(f"{field_name} must be a number")
    if min_value is not None and value < min_value:
        return ValidationResult.fail(f"{field_name} must be at least {min_value}")
    if max_value is not None and value > max_value:
        return ValidationResult.fail(f"{field_name} cannot exceed {max_value}")
    return ValidationResult.ok()

def validate_date(value: date, field_name: str, allow_future: bool = False) -> ValidationResult:
    if not isinstance(value, date):
        return ValidationResult.fail(f"{field_name} must be a valid date")
    if not allow_future and value > date.today():
        return ValidationResult.fail(f"{field_name} cannot be in the future")
    return ValidationResult.ok()

def validate_enum(value: str | int | Enum, enum_type: type[Enum], field_name: str) -> ValidationResult:
    if value is None:
        return ValidationResult.fail(f"{field_name} is required")
    if isinstance(value, Enum):
        value_to_check = value.value
    else:
        value_to_check = value
    if value_to_check not in [e.value for e in enum_type]:
        return ValidationResult.fail(f"Invalid {field_name} provided")
    return ValidationResult.ok()

def validate_image(img_b64: str, field_name: str, allowed_mime_types: set[str] | None = None, max_size_bytes: int | None = None) -> ValidationResult:
    if not img_b64:
        return ValidationResult.fail(f"{field_name} is required")
    if img_b64.startswith("data:"):
        try:
            _, img_b64 = img_b64.split(",", 1)
        except ValueError:
            return ValidationResult.fail(f"{field_name} has an invalid data URI format")
    
    try:
        image_bytes = base64.b64decode(img_b64, validate=True)
    except Exception:
        return ValidationResult.fail(f"{field_name} is not valid Base64")
    
    max_size_bytes = max_size_bytes or MAX_IMAGE_SIZE_BYTES
    
    if len(image_bytes) > max_size_bytes:
        return ValidationResult.fail(f"{field_name} cannot exceed {max_size_bytes // (1024 * 1024)} MB")
    try:
        img = Image.open(io.BytesIO(image_bytes))
        img.verify()
    except Exception:
        return ValidationResult.fail(f"{field_name} is not a valid image")

    if allowed_mime_types:
        mime_type = Image.MIME.get(img.format)
        if mime_type not in allowed_mime_types:
            return ValidationResult.fail(f"{field_name} must be one of: {', '.join(allowed_mime_types)}")

    return ValidationResult.ok()