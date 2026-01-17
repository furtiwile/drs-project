
from functools import wraps
from types import SimpleNamespace
from flask import g, jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity, verify_jwt_in_request
from app.database import get_redis_client

def authenticate(f):
    @wraps(f)
    def authentication_decorator(*args, **kwargs):
        try:
            verify_jwt_in_request()

            jwt_token = request.headers.get('Authorization').split(' ')[1]
            if(get_redis_client().get(f'blacklist:{jwt_token}') is not None):
                return jsonify({"message": f"Authentication required: Invalid token provided"}), 401

            identity = int(get_jwt_identity())
            claims = get_jwt()
            g.user = SimpleNamespace(
                user_id = identity,
                role = claims.get("role")
            )
        except Exception as e:
            return jsonify({"message": f"Authentication required: {str(e)}"}), 401

        return f(*args, **kwargs)
    return authentication_decorator
        