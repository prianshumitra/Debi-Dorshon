"""
app/services/transit_service.py
--------------------------------
Service layer for Ride by Metro and Ride by Train features.
Queries MongoDB for distinct transit hubs and associated pandals.
"""

from typing import List, Optional, Dict
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.config import settings


class TransitService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db[settings.PANDAL_COLLECTION_NAME]

    async def get_metro_stations(self) -> List[Dict]:
        """Aggregate all distinct metro stations with pandal counts."""
        pipeline = [
            {"$match": {"nearest_metro.name": {"$exists": True, "$ne": None}}},
            {
                "$group": {
                    "_id": {
                        "name": "$nearest_metro.name",
                        "line": "$nearest_metro.line"
                    },
                    "pandal_count": {"$sum": 1}
                }
            },
            {"$sort": {"pandal_count": -1, "_id.name": 1}}
        ]
        results = []
        async for doc in self.collection.aggregate(pipeline):
            results.append({
                "name": doc["_id"]["name"],
                "line": doc["_id"].get("line"),
                "pandal_count": doc["pandal_count"]
            })
        return results

    async def get_pandals_by_metro(
        self, station_name: str, line: Optional[str] = None
    ) -> List[Dict]:
        """Get all pandals near a specific metro station."""
        query = {
            "nearest_metro.name": {"$regex": f"^{station_name}$", "$options": "i"}
        }
        if line:
            query["nearest_metro.line"] = {"$regex": f"^{line}$", "$options": "i"}

        cursor = self.collection.find(query)
        pandals = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            doc["id"] = doc["_id"]
            pandals.append(doc)
        return pandals

    async def get_train_stations(self) -> List[Dict]:
        """Aggregate all distinct railway stations with pandal counts."""
        pipeline = [
            {"$match": {"nearest_station.name": {"$exists": True, "$ne": None}}},
            {
                "$group": {
                    "_id": "$nearest_station.name",
                    "pandal_count": {"$sum": 1}
                }
            },
            {"$sort": {"pandal_count": -1, "_id": 1}}
        ]
        results = []
        async for doc in self.collection.aggregate(pipeline):
            results.append({
                "name": doc["_id"],
                "pandal_count": doc["pandal_count"]
            })
        return results

    async def get_pandals_by_train(self, station_name: str) -> List[Dict]:
        """Get all pandals near a specific railway station."""
        query = {
            "nearest_station.name": {"$regex": f"^{station_name}$", "$options": "i"}
        }
        cursor = self.collection.find(query)
        pandals = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            doc["id"] = doc["_id"]
            pandals.append(doc)
        return pandals
