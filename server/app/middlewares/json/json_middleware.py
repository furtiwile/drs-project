import logging
from functools import wraps
from typing import Any, Callable, TypeVar, cast
from flask import request, jsonify

logger = logging.getLogger(__name__)
F = TypeVar("F", bound=Callable[..., Any])

def require_json(f: F) -> F:
    @wraps(f)
    def json_decorator(*args: Any, **kwargs: Any) -> Any:
        if not request.is_json:
            logger.error("Invalid Content-Type, expected application/json")
            return jsonify(message="Content-Type must be application/json"), 415
        return f(*args, **kwargs)
    return cast(F, json_decorator)