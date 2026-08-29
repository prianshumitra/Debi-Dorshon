"""
app/api/v1/endpoints/route.py
------------------------------
A -> B Road Route-Based Puja Pandal Planner API endpoints.
"""

from fastapi import APIRouter, Depends, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.schemas.route import RoutePlanRequest, RoutePlanResponse
from app.services.route_planner import RoutePlannerService

router = APIRouter()


def get_route_planner_service(
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> RoutePlannerService:
    return RoutePlannerService(db)


@router.post(
    "/plan",
    response_model=RoutePlanResponse,
    status_code=status.HTTP_200_OK,
    summary="Plan an A -> B road route Puja Parikrama itinerary",
)
async def plan_route(
    request: RoutePlanRequest,
    service: RoutePlannerService = Depends(get_route_planner_service),
):
    """
    Plan a Puja Parikrama itinerary along an actual road route from Point A (origin) to Point B (destination).

    - Obtains road route geometry from OSRM routing engine.
    - Filters candidate pandals within 1.0 km (or custom `max_detour_km`) of the road polyline.
    - Orders selected pandals sequentially along the path of travel from Point A toward Point B.
    - Returns full route polyline geometry for map rendering.
    """
    return await service.plan_route(request)
