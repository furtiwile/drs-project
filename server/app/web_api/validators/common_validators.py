from datetime import date
import re
from enum import Enum
from app.domain.types.validation_result import ValidationResult

EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

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