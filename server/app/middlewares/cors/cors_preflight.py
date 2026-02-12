"""
CORS Preflight Middleware
Handles OPTIONS requests before authentication middleware runs
"""
from flask import request, jsonify
from typing import Callable

def cors_preflight_handler(f: Callable) -> Callable:
    """
    Decorator to handle CORS preflight OPTIONS requests
    Returns 200 OK without authentication for OPTIONS method
    """
    def wrapper(*args, **kwargs):
        if request.method == 'OPTIONS':
            return jsonify({}), 200
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper
