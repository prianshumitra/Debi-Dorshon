"""
app/core/database.py
--------------------
Async MongoDB connection lifecycle manager using Motor driver.
Provides global database instance access across endpoint dependencies.
"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import settings
import logging

logger = logging.getLogger("uvicorn")


class Database:
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None


db = Database()


async def connect_to_mongo():
    """Initializes MongoDB connection on FastAPI app startup."""
    logger.info("Connecting to MongoDB at: %s", settings.MONGODB_URL)
    db.client = AsyncIOMotorClient(settings.MONGODB_URL)
    db.db = db.client[settings.MONGODB_DB_NAME]
    logger.info("Successfully connected to database: %s", settings.MONGODB_DB_NAME)


async def close_mongo_connection():
    """Closes MongoDB connection on FastAPI app shutdown."""
    if db.client:
        logger.info("Closing MongoDB connection...")
        db.client.close()
        logger.info("MongoDB connection closed.")


def get_database() -> AsyncIOMotorDatabase:
    """Dependency injection helper to get MongoDB database instance."""
    return db.db
