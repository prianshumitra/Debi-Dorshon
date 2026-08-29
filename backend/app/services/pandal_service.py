"""
app/services/pandal_service.py
-------------------------------
Service layer containing all MongoDB queries and business logic for Pandals.
Acts like Controllers / DAO in MVC frameworks (Node/Express).
"""

from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.config import settings


class PandalService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db[settings.PANDAL_COLLECTION_NAME]

    async def get_all_pandals(
        self,
        region: Optional[str] = None,
        cluster: Optional[str] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[dict]:
        """Fetch pandals with optional filtering, search, and pagination."""
        query = {}
        if region:
            query["region"] = {"$regex": region, "$options": "i"}
        if cluster:
            query["cluster"] = {"$regex": cluster, "$options": "i"}
        if search:
            query["name"] = {"$regex": search, "$options": "i"}

        cursor = self.collection.find(query).skip(skip).limit(limit)
        pandals = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])  # Convert BSON ObjectId to string
            doc["id"] = doc["_id"]
            pandals.append(doc)
        return pandals

    async def get_pandal_by_id(self, pandal_id: str) -> Optional[dict]:
        """Fetch a single pandal by its MongoDB ObjectId string."""
        if not ObjectId.is_valid(pandal_id):
            return None
        doc = await self.collection.find_one({"_id": ObjectId(pandal_id)})
        if doc:
            doc["_id"] = str(doc["_id"])
            doc["id"] = doc["_id"]
        return doc

    async def count_pandals(self) -> int:
        """Get total count of pandals in database."""
        return await self.collection.count_documents({})

