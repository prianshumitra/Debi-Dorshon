"""
app/api/v1/router.py
--------------------
Central API router for Version 1 endpoints.
Aggregates sub-routers (health, pandals, users, etc.).
"""

from fastapi import APIRouter
from app.api.v1.endpoints import health, pandals

api_router = APIRouter()

# Include sub-routers with prefixes and tags for OpenAPI docs
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(pandals.router, prefix="/pandals", tags=["Pandals"])
