from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from pydantic import ValidationError

from app.services.auth_service import AuthService
from app.validators.auth_validator import SignupSchema, LoginSchema
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400
        
        # Validate input
        signup_data = SignupSchema(**data)
        
        response, status_code = AuthService.signup(
            signup_data.username, 
            signup_data.email, 
            signup_data.password
        )
        return jsonify(response), status_code
        
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400
        
        # Validate input
        login_data = LoginSchema(**data)
        
        response, status_code = AuthService.login(
            login_data.email, 
            login_data.password
        )
        return jsonify(response), status_code
        
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.find_by_id(user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Remove sensitive info
    user.pop('hashed_password', None)
    user['_id'] = str(user['_id'])
    
    return jsonify(user), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # In a simple JWT setup, logout is usually handled on the client by deleting the token.
    # For server-side logout, we could implement a token blocklist.
    # For now, we return a success message.
    return jsonify({"message": "Logout successful"}), 200
