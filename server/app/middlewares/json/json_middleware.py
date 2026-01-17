import logging
from functools import wraps
from flask import request, jsonify

logger = logging.getLogger(__name__)

def require_json(f):
    @wraps(f)
    def json_decorator(*args, **kwargs):
        if not request.is_json:
            logger.error("Invalid Content-Type, expected application/json")
            return jsonify(message="Content-Type must be application/json"), 415
        return f(*args, **kwargs)
    return json_decorator