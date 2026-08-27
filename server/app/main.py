"""
app/main.py
-----------
Main entry point for Debi-Dorshon FastAPI Application.
Handles app lifecycle (MongoDB connection setup), CORS middleware, and API router registration.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import connect_to_mongo, close_mongo_connection
from app.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown events (Lifespan Context)."""
    # Startup: Connect to MongoDB
    await connect_to_mongo()
    yield
    # Shutdown: Close MongoDB connection
    await close_mongo_connection()


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API for Debi-Dorshon Durga Puja Guide App",
    version="0.1.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",       # Interactive Swagger UI docs at http://localhost:8000/docs
    redoc_url="/redoc",     # ReDoc documentation at http://localhost:8000/redoc
    lifespan=lifespan
)

# Set up CORS (Cross-Origin Resource Sharing) middleware for Frontend / Mobile apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API v1 router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["Root"])
async def root():
    """Welcome root endpoint."""
    return {
        "message": "Welcome to Debi-Dorshon API!",
        "docs": "/docs",
        "health": f"{settings.API_V1_STR}/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
