"""
app/schemas/pandal.py
---------------------
Pydantic validation models for Durga Puja Pandals matching debi_dorshon.json structure.
Similar to DTOs (Data Transfer Objects) or Mongoose Schemas in Node.js.
"""

from typing import Optional, List
from pydantic import BaseModel, Field


class LocationSchema(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class TransportInfoSchema(BaseModel):
    name: Optional[str] = None
    line: Optional[str] = None


class PandalBase(BaseModel):
    name: str = Field(..., example="Shikdar Bagan")
    region: Optional[str] = Field(None, example="North")
    cluster: Optional[str] = Field(None, example="Shyambazar")
    location: Optional[LocationSchema] = None
    nearest_metro: Optional[TransportInfoSchema] = None
    nearest_station: Optional[TransportInfoSchema] = None
    nearest_ferry: Optional[TransportInfoSchema] = None


class PandalCreate(PandalBase):
    """Schema used when creating a new pandal via POST request."""
    pass


class PandalUpdate(BaseModel):
    """Schema used when updating an existing pandal (partial updates supported)."""
    name: Optional[str] = None
    region: Optional[str] = None
    cluster: Optional[str] = None
    location: Optional[LocationSchema] = None
    nearest_metro: Optional[TransportInfoSchema] = None
    nearest_station: Optional[TransportInfoSchema] = None
    nearest_ferry: Optional[TransportInfoSchema] = None


class PandalResponse(PandalBase):
    """Schema returned in API responses. Includes MongoDB string ID."""
    id: str = Field(..., alias="_id", example="64d3f1a2b... ")

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }
