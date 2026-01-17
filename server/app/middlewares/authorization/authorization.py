import logging
from functools import wraps
from typing import Any, Callable, TypeVar, cast
from flask import g, jsonify

from app.domain.enums.role import Role

logger = logging.getLogger(__name__)
F = TypeVar("F", bound=Callable[..., Any])

def authorize(*roles: Role) -> Callable[[F], F]:
    def authorize_decorator(f: F) -> F:
        @wraps(f)
        def authorize_fn(*args: Any, **kwargs: Any) -> Any:
            if not hasattr(g, "user") or g.user is None:
                logger.warning("User context was not provided")
                return jsonify({"message": "User context not found"}), 401
            
            user_role = g.user.role
            allowed_roles = [r.value for r in roles]

            if user_role not in allowed_roles:
                logger.warning("Access denied: insufficient permissions")
                return jsonify({"message": "Forbidden: Insufficient permissions"}), 403
            
            return f(*args, **kwargs)
        return cast(F, authorize_fn)
    return authorize_decorator
    