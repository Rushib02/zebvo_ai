from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models.user import User

def roles_required(*roles):
    """Decorator to restrict access to specific roles."""
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = User.find_by_id(user_id)
            
            if not user:
                return jsonify({"error": "User not found"}), 404
            
            if user.get("role") not in roles:
                return jsonify({"error": "Unauthorized access. Insufficient permissions."}), 403
            
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def token_required(fn):
    """Simple decorator for protected routes."""
    @wraps(fn)
    def decorator(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception as e:
            return jsonify({"error": str(e)}), 401
        return fn(*args, **kwargs)
    return decorator
