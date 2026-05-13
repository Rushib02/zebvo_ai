import os
from datetime import datetime
from pymongo import MongoClient
from app.config.config import Config

class ThumbnailStorage:
    def __init__(self):
        self.save_dir = "generated/thumbnails"
        os.makedirs(self.save_dir, exist_ok=True)
        
        # Connect to MongoDB
        self.client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
        self.db = self.client.ai_creator_studio
        self.collection = self.db.thumbnails

    def save_image(self, project_id: str, image_bytes: bytes) -> str:
        """Saves image bytes to a local file."""
        filename = f"{project_id}_{int(datetime.now().timestamp())}.png"
        filepath = os.path.join(self.save_dir, filename)
        
        with open(filepath, "wb") as f:
            f.write(image_bytes)
            
        return filepath

    def save_metadata(self, project_id: str, image_path: str, prompt: str):
        """Saves thumbnail metadata to MongoDB."""
        metadata = {
            "project_id": project_id,
            "image_path": image_path,
            "image_prompt": prompt,
            "created_at": datetime.utcnow()
        }
        self.collection.update_one(
            {"project_id": project_id},
            {"$set": metadata},
            upsert=True
        )
