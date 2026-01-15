
from app.domain.enums.Gender import Gender
from app.domain.enums.Role import Role
from app.domain.types.validation_result import ValidationResult
from app.repositories.user_repository import UpdateUserDTO
from app.web_api.validators.auth_validators import validate_enum
from app.web_api.validators.common_validators import validate_date, validate_email, validate_number, validate_password, validate_text

def validate_user_id(user_id: int) -> ValidationResult:
    return validate_number(user_id, "User ID", 1)

def validate_update_user_role_by_id(user_id: int, role: str) -> ValidationResult:
    if not (valid_id := validate_number(user_id, "User ID", 1)):
        return valid_id
    if not (valid_role := validate_enum(role, Role, "Role")):
        return valid_role
    return ValidationResult.ok()

def validate_update_user(user_id: int, data: UpdateUserDTO) -> ValidationResult:
    if not (valid_id := validate_number(user_id, "User ID", 1)):
        return valid_id    
    if data.first_name is not None and not (valid_first_name := validate_text(data.first_name, "First Name", 1, 50)):
        return valid_first_name
    if data.last_name is not None and not (valid_last_name := validate_text(data.last_name, "Last Name", 1, 50)):
        return valid_last_name
    if data.email is not None and not (valid_email := validate_email(data.email, 100)):
        return valid_email
    if data.password is not None and not (valid_password := validate_password(data.password)):
        return valid_password
    if data.birth_date is not None and not (valid_birth_date := validate_date(data.birth_date, "Birth Date")):
        return valid_birth_date
    if data.gender is not None and not (valid_gender := validate_enum(data.gender, Gender, "Gender")):
        return valid_gender
    if data.country is not None and not (valid_country := validate_text(data.country, "Country", 1, 50)):
        return valid_country
    if data.city is not None and not (valid_city := validate_text(data.city, "City", 1, 50)):
        return valid_city
    if data.street is not None and not (valid_street := validate_text(data.street, "Street", 1, 50)):
        return valid_street
    if data.house_number is not None and not (valid_house_number := validate_number(data.house_number, "House Number", 1, 99999)):
        return valid_house_number
    return ValidationResult.ok()
