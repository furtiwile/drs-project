from functools import wraps
from flask import request, jsonify

def require_json(f):
    @wraps(f)
    def json_decorator(*args, **kwargs):
        if not request.is_json:
            return jsonify(message="Content-Type must be application/json"), 415
        return f(*args, **kwargs)
    return json_decorator