"""
app/core/config.py
------------------
Application settings powered by Pydantic BaseSettings.
Loads environment variables from `.env` automatically.
Your FastAPI dev friend can easily add JWT keys, CORS origins, Redis URLs here later!
"""

import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App Settings
    PROJECT_NAME: str = "Debi-Dorshon API"
    API_V1_STR: str = "/api/v1"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # MongoDB Settings
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "debi_dorshon_db"
    PANDAL_COLLECTION_NAME: str = "pandals"

    # Routing Engine Settings (OSRM)
    OSRM_BASE_URL: str = "http://router.project-osrm.org"
    OSRM_TIMEOUT_SECONDS: float = 10.0

    # Configure Pydantic to read from `.env` file
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


# Instantiate single global settings object
settings = Settings()
