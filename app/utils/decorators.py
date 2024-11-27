from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from functools import wraps

def role_required(required_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_user = get_jwt_identity()
            if current_user['role'] not in required_roles:
                return jsonify({"message": "Access denied"}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator