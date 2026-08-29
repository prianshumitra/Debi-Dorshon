"""
app/api/v1/endpoints/trip.py
-----------------------------
Stateless Puja Parikrama / Trip Planning API endpoints.
"""

from fastapi import APIRouter, Depends, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.schemas.trip import TripPlanRequest, TripPlanResponse
from app.services.route_service import RouteService

router = APIRouter()


def get_route_service(
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> RouteService:
    return RouteService(db)


@router.post(
    "/plan",
    response_model=TripPlanResponse,
    status_code=status.HTTP_200_OK,
    summary="Plan a Puja Parikrama trip based on starting GPS coordinates",
)
async def plan_trip(
    request: TripPlanRequest,
    service: RouteService = Depends(get_route_service),
):
    """
    Stateless endpoint that receives user coordinates and optional region/cluster filters,
    calculates distances to candidate pandals, and returns an ordered itinerary.
    """
    return await service.plan_trip(request)
