from flask_jwt_extended import create_access_token
from app.models.user import User
from app.database.mongodb import db
from app.utils.logger import request_logger

class AuthService:
    @staticmethod
    def signup(username, email, password):
        # Check if user already exists
        if User.find_by_email(email):
            return {"error": "Email already registered"}, 400
        
        if User.find_by_username(username):
            return {"error": "Username already taken"}, 400

        # Create user
        user_data = User.create_user_schema(username, email, password)
        result = db.get_db()[User.collection].insert_one(user_data)
        
        user_id = str(result.inserted_id)
        access_token = create_access_token(identity=user_id)
        
        request_logger.info(f"User signed up: {email}")
        
        return {
            "message": "User created successfully",
            "access_token": access_token,
            "user": {
                "username": username,
                "email": email,
                "role": user_data["role"]
            }
        }, 201

    @staticmethod
    def login(email, password):
        user = User.find_by_email(email)
        
        if not user or not User.verify_password(password, user["hashed_password"]):
            request_logger.warning(f"Failed login attempt: {email}")
            return {"error": "Invalid email or password"}, 401

        user_id = str(user["_id"])
        access_token = create_access_token(identity=user_id)
        
        # Update last login
        User.update_last_login(user_id)
        
        request_logger.info(f"User logged in: {email}")
        
        return {
            "message": "Login successful",
            "access_token": access_token,
            "user": {
                "username": user["username"],
                "email": user["email"],
                "role": user["role"]
            }
        }, 200
