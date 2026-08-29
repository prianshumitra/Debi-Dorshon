"""
app/services/route_service.py
------------------------------
Business logic for Puja Parikrama / trip planning.
Fetches candidate pandals from MongoDB and generates an optimized itinerary
using Haversine distance calculations.
"""

from typing import Dict, List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.config import settings
from app.schemas.trip import TripPlanRequest, TripPlanResponse, ItineraryItem
from app.schemas.pandal import PandalResponse
from app.utils.geo import sort_pandals_by_distance


class RouteService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db[settings.PANDAL_COLLECTION_NAME]

    async def plan_trip(self, request: TripPlanRequest) -> TripPlanResponse:
        """
        Generate a Puja Parikrama trip plan given starting GPS coordinates.
        Optionally filter by region/cluster and return top nearest N pandals.
        """
        query = {}
        if request.region:
            query["region"] = {"$regex": request.region, "$options": "i"}
        if request.cluster:
            query["cluster"] = {"$regex": request.cluster, "$options": "i"}

        cursor = self.collection.find(query)
        candidates = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            doc["id"] = doc["_id"]
            candidates.append(doc)

        sorted_candidates = sort_pandals_by_distance(
            request.origin_latitude, request.origin_longitude, candidates
        )

        selected = sorted_candidates[: request.max_pandals]

        itinerary = []
        total_dist = 0.0
        for idx, item in enumerate(selected, start=1):
            dist = item.pop("distance_km", 0.0)
            pandal_resp = PandalResponse(**item)
            itinerary.append(
                ItineraryItem(step=idx, pandal=pandal_resp, distance_km=dist)
            )
            total_dist += dist

        avg_distance = round(total_dist, 2) if itinerary else 0.0

        return TripPlanResponse(
            origin={
                "latitude": request.origin_latitude,
                "longitude": request.origin_longitude,
            },
            total_pandals=len(itinerary),
            estimated_distance_km=avg_distance,
            itinerary=itinerary,
        )
