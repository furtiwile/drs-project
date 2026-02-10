from app.domain.enums.error_type import ErrorType

def normalize_status_code(code: int | ErrorType) -> int:
    return code if isinstance(code, int) else error_type_to_http(code)

def error_type_to_http(err_type: ErrorType) -> int:
    match err_type:
        case ErrorType.BAD_REQUEST:
            return 400
        case ErrorType.UNAUTHORIZED:
            return 401
        case ErrorType.FORBIDDEN:
            return 403
        case ErrorType.NOT_FOUND:
            return 404
        case ErrorType.CONFLICT:
            return 409
        case ErrorType.TOO_MANY_REQUESTS:
            return 429
        case ErrorType.INTERNAL_ERR:
            return 500
        case _:
            return 500