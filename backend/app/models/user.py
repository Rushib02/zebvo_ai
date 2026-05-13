import bcrypt
from datetime import datetime
from app.database.mongodb import db

class User:
    collection = "users"

    @staticmethod
    def create_user_schema(username, email, password, role="user", subscription_type="free"):
        """Creates a new user document with hashed password."""
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        return {
            "username": username,
            "email": email.lower(),
            "hashed_password": hashed_password.decode('utf-8'),
            "profile_image": None,
            "role": role,
            "subscription_type": subscription_type,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "last_login": None
        }

    @staticmethod
    def verify_password(password, hashed_password):
        """Verifies a password against a hash."""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    @staticmethod
    def find_by_email(email):
        """Finds a user by email."""
        return db.get_db()[User.collection].find_one({"email": email.lower()})

    @staticmethod
    def find_by_username(username):
        """Finds a user by username."""
        return db.get_db()[User.collection].find_one({"username": username})

    @staticmethod
    def find_by_id(user_id):
        """Finds a user by ID."""
        from bson import ObjectId
        return db.get_db()[User.collection].find_one({"_id": ObjectId(user_id)})

    @staticmethod
    def update_last_login(user_id):
        """Updates the last login timestamp."""
        from bson import ObjectId
        db.get_db()[User.collection].update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"last_login": datetime.utcnow()}}
        )
