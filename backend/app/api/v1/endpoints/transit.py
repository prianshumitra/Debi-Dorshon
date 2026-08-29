"""
app/api/v1/endpoints/transit.py
--------------------------------
Endpoints for Ride by Metro and Ride by Train features.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.schemas.transit import (
    MetroStationResponse,
    TrainStationResponse,
    StationPandalsResponse,
)
from app.schemas.pandal import PandalResponse
from app.services.transit_service import TransitService

router = APIRouter()


def get_transit_service(
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> TransitService:
    return TransitService(db)


@router.get(
    "/metro/stations",
    response_model=List[MetroStationResponse],
    summary="Get all available metro stations with pandal counts",
)
async def list_metro_stations(
    service: TransitService = Depends(get_transit_service),
):
    """Retrieve distinct metro stations and the count of nearby pandals."""
    return await service.get_metro_stations()


@router.get(
    "/metro/pandals",
    response_model=StationPandalsResponse,
    summary="Get pandals accessible from a specific Metro station",
)
async def get_pandals_by_metro_station(
    station_name: str = Query(..., description="Metro station name (e.g. Shyambazar, Kalighat)"),
    line: Optional[str] = Query(None, description="Optional Metro line filter (e.g. Blue Line)"),
    service: TransitService = Depends(get_transit_service),
):
    """Retrieve all pandals connected to a given Metro station."""
    pandals = await service.get_pandals_by_metro(station_name=station_name, line=line)
    return StationPandalsResponse(
        station_name=station_name,
        total_pandals=len(pandals),
        pandals=[PandalResponse(**p) for p in pandals],
    )


@router.get(
    "/train/stations",
    response_model=List[TrainStationResponse],
    summary="Get all available railway stations with pandal counts",
)
async def list_train_stations(
    service: TransitService = Depends(get_transit_service),
):
    """Retrieve distinct railway stations and the count of nearby pandals."""
    return await service.get_train_stations()


@router.get(
    "/train/pandals",
    response_model=StationPandalsResponse,
    summary="Get pandals accessible from a specific Train station",
)
async def get_pandals_by_train_station(
    station_name: str = Query(..., description="Railway station name (e.g. Sealdah, Howrah, Kolkata Station)"),
    service: TransitService = Depends(get_transit_service),
):
    """Retrieve all pandals connected to a given Railway station."""
    pandals = await service.get_pandals_by_train(station_name=station_name)
    return StationPandalsResponse(
        station_name=station_name,
        total_pandals=len(pandals),
        pandals=[PandalResponse(**p) for p in pandals],
    )
