import logging
from functools import wraps
from types import SimpleNamespace
from typing import Any, Callable, Dict, TypeVar, cast
from flask import g, jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity, verify_jwt_in_request # type: ignore

from app.database import get_redis_client

logger = logging.getLogger(__name__)
F = TypeVar("F", bound=Callable[..., Any])

def authenticate(f: F) -> F:
    @wraps(f)
    def authentication_decorator(*args: Any, **kwargs: Any) -> Any:
        try:
            verify_jwt_in_request()

            jwt_token = cast(str, request.headers.get('Authorization')).split(" ")[1]
            if(get_redis_client().get(f'blacklist:{jwt_token}') is not None):
                logger.warning("Authentication failed: Invalid token provided")
                return jsonify({"message": f"Authentication required: Invalid token provided"}), 401

            identity: int = int(get_jwt_identity())
            claims: Dict[str, Any] = cast(Dict[str, Any], get_jwt())
            g.user = SimpleNamespace(
                user_id = identity,
                role = claims.get("role")
            )
        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}")
            return jsonify({"message": f"Authentication required: {str(e)}"}), 401

        return f(*args, **kwargs)
    return cast(F, authentication_decorator)
        