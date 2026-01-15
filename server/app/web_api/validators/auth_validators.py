import re
from app.domain.enums.Gender import Gender
from app.domain.types.validation_result import ValidationResult
from app.services.auth_service import LoginUserDTO, RegisterUserDTO
from app.web_api.validators.common_validators import validate_date, validate_email, validate_enum, validate_number, validate_password, validate_text

EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

def validate_login(data: LoginUserDTO)-> ValidationResult:
    if not (valid_email := validate_email(data.email, 100)):
        return valid_email
    if not (valid_password := validate_password(data.password)):
        return valid_password
    return ValidationResult.ok()

def validate_registration(data: RegisterUserDTO)-> ValidationResult:
    if not (valid_first_name := validate_text(data.first_name, "First Name", 1, 50)):
        return valid_first_name
    if not (valid_last_name := validate_text(data.last_name, "Last Name", 1, 50)):
        return valid_last_name
    if not (valid_email := validate_email(data.email, 100)):
        return valid_email
    if not (valid_password := validate_password(data.password)):
        return valid_password
    if not (valid_birth_date := validate_date(data.birth_date, "Birth Date")):
        return valid_birth_date
    if not (valid_gender := validate_enum(data.gender, Gender, "Gender")):
        return valid_gender
    if not (valid_country := validate_text(data.country, "Country", 1, 50)):
        return valid_country
    if not (valid_city := validate_text(data.city, "City", 1, 50)):
        return valid_city
    if not (valid_street := validate_text(data.street, "Street", 1, 50)):
        return valid_street
    if not (valid_house_number := validate_number(data.house_number, "House Number", 1, 99999)):
        return valid_house_number
    return ValidationResult.ok()