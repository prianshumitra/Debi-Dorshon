"""
app/schemas/trip.py
-------------------
Pydantic schemas for Puja Parikrama / Trip Planning endpoints.
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from app.schemas.pandal import PandalResponse, LocationSchema


class TripPlanRequest(BaseModel):
    origin_latitude: float = Field(..., json_schema_extra={"example": 22.5986}, description="User's starting latitude")
    origin_longitude: float = Field(..., json_schema_extra={"example": 88.3712}, description="User's starting longitude")
    region: Optional[str] = Field(None, json_schema_extra={"example": "North"}, description="Optional filter by region")
    cluster: Optional[str] = Field(None, json_schema_extra={"example": "Shyambazar"}, description="Optional filter by cluster")
    max_pandals: int = Field(5, ge=1, le=20, description="Maximum number of pandals to include in itinerary")


class ItineraryItem(BaseModel):
    step: int = Field(..., json_schema_extra={"example": 1})
    pandal: PandalResponse
    distance_km: float = Field(..., json_schema_extra={"example": 0.45}, description="Distance from origin in kilometers")


class TripPlanResponse(BaseModel):
    origin: LocationSchema
    total_pandals: int = Field(..., json_schema_extra={"example": 5})
    estimated_distance_km: float = Field(..., json_schema_extra={"example": 3.2})
    itinerary: List[ItineraryItem]
