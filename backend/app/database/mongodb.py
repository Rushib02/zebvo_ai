from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

class MongoDB:
    """
    Singleton-style MongoDB connector for Streamlit applications.
    """
    _instance = None
    _client = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDB, cls).__new__(cls)
        return cls._instance

    def connect(self, uri: str = None):
        """Initializes the connection if not already established."""
        if self._client is None:
            try:
                mongo_uri = uri or os.getenv("MONGO_URI", "mongodb://localhost:27017/ai_creator_studio")
                self._client = MongoClient(mongo_uri, serverSelectionTimeoutMS=2000)
                # Force a connection check
                self._client.admin.command('ping')
                
                # Extract database name
                db_name = "ai_creator_studio"
                path = mongo_uri.split('/')[-1]
                if path and '?' in path:
                    db_name = path.split('?')[0]
                elif path:
                    db_name = path
                    
                self._db = self._client[db_name]
            except Exception as e:
                print(f"MongoDB Connection Warning: {e}")
                self._db = None
        return self._db

    def get_db(self):
        if self._db is None:
            return self.connect()
        return self._db

# Global access point
db = MongoDB()

def get_database():
    return db.get_db()
