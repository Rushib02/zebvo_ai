from bson import ObjectId
from datetime import datetime
from app.database.mongodb import db

class BaseRepository:
    def __init__(self, collection_name):
        self.collection_name = collection_name
        self.db = db.get_db()
        self.collection = self.db[collection_name] if self.db is not None else None

    def create(self, data):
        if self.collection is None:
            data['_id'] = "mock_id_" + str(datetime.utcnow().timestamp())
            return data
        data['created_at'] = datetime.utcnow()
        data['updated_at'] = datetime.utcnow()
        result = self.collection.insert_one(data)
        data['_id'] = str(result.inserted_id)
        return data

    def get_by_id(self, item_id):
        if not ObjectId.is_valid(item_id):
            return None
        item = self.collection.find_one({"_id": ObjectId(item_id)})
        if item:
            item['_id'] = str(item['_id'])
        return item

    def update(self, item_id, data):
        if not ObjectId.is_valid(item_id):
            return None
        data['updated_at'] = datetime.utcnow()
        self.collection.update_one({"_id": ObjectId(item_id)}, {"$set": data})
        return self.get_by_id(item_id)

    def delete(self, item_id):
        if not ObjectId.is_valid(item_id):
            return False
        result = self.collection.delete_one({"_id": ObjectId(item_id)})
        return result.deleted_count > 0

    def list(self, filters=None, sort=None, page=1, limit=10):
        if self.collection is None:
            return {"items": [], "total": 0, "page": page, "limit": limit, "pages": 0}
        filters = filters or {}
        skip = (page - 1) * limit
        
        cursor = self.collection.find(filters)
        
        if sort:
            cursor = cursor.sort(sort)
        else:
            cursor = cursor.sort("created_at", -1)
            
        items = list(cursor.skip(skip).limit(limit))
        total = self.collection.count_documents(filters)
        
        for item in items:
            item['_id'] = str(item['_id'])
            
        return {
            "items": items,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": (total + limit - 1) // limit
        }

    def find_one(self, filters):
        item = self.collection.find_one(filters)
        if item:
            item['_id'] = str(item['_id'])
        return item
