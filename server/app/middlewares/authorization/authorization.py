import logging
from functools import wraps
from flask import g, jsonify

logger = logging.getLogger(__name__)

def authorize(*roles):
    def authorize_decorator(f):
        @wraps(f)
        def authorize_fn(*args, **kwargs):
            if not hasattr(g, "user") or g.user is None:
                logger.warning("User context was not provided")
                return jsonify({"message": "User context not found"}), 401
            
            user_role = g.user.role
            allowed_roles = [r.value for r in roles]

            if user_role not in allowed_roles:
                logger.warning("Access denied: insufficient permissions")
                return jsonify({"message": "Forbidden: Insufficient permissions"}), 403
            
            return f(*args, **kwargs)
        return authorize_fn
    return authorize_decorator
    