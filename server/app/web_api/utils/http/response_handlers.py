from typing import Any, Callable, TypeVar
from flask import jsonify
from flask.wrappers import Response
from flask_jwt_extended import create_access_token # type: ignore

from app.domain.types.result import Result, ok
from app.web_api.utils.converters.error_type_converter import error_type_to_http, normalize_status_code
from app.domain.models.user import User
from app.domain.dtos.user.user_dto import UserDTO
from app.domain.enums.error_type import ErrorType
from app.domain.protocols.serialization import Serializable

T = TypeVar("T")
E = TypeVar("E", int, ErrorType)

def handle_auth_response(result: Result[User, ErrorType], success_status: int = 200) -> tuple[Response, int]:
    if isinstance(result, ok):
        user = result.data
        token = create_access_token(identity=str(user.user_id), additional_claims={"role": user.role.value})

        return jsonify({
            "token": token,
            "user": UserDTO.from_model(user).to_dict(),
        }), success_status

    return jsonify(message=result.message), error_type_to_http(result.status_code)

def handle_response(
        result: Result[T, E], 
        to_json: Callable[[T], Any] | None = None, 
        success_code: int = 200
) -> tuple[Response, int]:
    if isinstance(result, ok):
        if to_json is not None:
            data = to_json(result.data)
        elif isinstance(result.data, Serializable):
            data = result.data.to_dict()
        else:
            raise TypeError(f"Cannot serialize {type(result.data).__name__}")
        
        return jsonify(data), success_code
    
    else:
        return jsonify({"message": result.message}), normalize_status_code(result.status_code)
