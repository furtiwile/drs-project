from app.domain.dtos.rating_dto import RatingCreateDTO, RatingCreateValidationSchema, RatingUpdateDTO, RatingUpdateValidationSchema


def validate_create_rating_data(data: dict, user_id: int) -> RatingCreateDTO:
    """
    Validates the data for creating a rating.

    Args:
        data (dict): The data to validate.
        user_id (int): The user ID from headers.

    Returns:
        RatingCreateDTO: The validated data transfer object.

    Raises:
        ValueError: If the data is invalid.
    """
    schema = RatingCreateValidationSchema()
    errors = schema.validate(data)
    if errors:
        raise ValueError(errors)

    return RatingCreateDTO(
        user_id=user_id,
        flight_id=data['flight_id'],
        rating=data['rating']
    )


def validate_update_rating_data(data: dict) -> RatingUpdateDTO:
    """
    Validates the data for updating a rating.

    Args:
        data (dict): The data to validate.

    Returns:
        RatingUpdateDTO: The validated data transfer object.

    Raises:
        ValueError: If the data is invalid.
    """
    schema = RatingUpdateValidationSchema()
    errors = schema.validate(data)
    if errors:
        raise ValueError(errors)

    return RatingUpdateDTO(
        rating=data['rating']
    )