"""
backend/tests/test_backend.py
------------------------------
Unit tests for Debi-Dorshon backend initialization, routes, and utilities.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.utils.geo import haversine_distance, sort_pandals_by_distance


client = TestClient(app)


def test_app_import_and_root():
    """Verify that FastAPI application initializes and root endpoint returns 200."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Welcome to Debi-Dorshon API!"


def test_haversine_distance():
    """Test Haversine distance calculation between known Kolkata coordinates."""
    # Distance between Shyambazar (22.6000, 88.3700) and Esplanade (22.5647, 88.3517) ~ 4.3 km
    dist = haversine_distance(22.6000, 88.3700, 22.5647, 88.3517)
    assert 3.5 <= dist <= 5.0


def test_sort_pandals_by_distance():
    """Test sorting pandals by geographical proximity."""
    origin_lat, origin_lng = 22.5986, 88.3712  # Shyambazar
    pandals = [
        {"name": "Far Pandal", "location": {"latitude": 22.5186, "longitude": 88.3432}},
        {"name": "Near Pandal", "location": {"latitude": 22.6000, "longitude": 88.3700}},
    ]
    sorted_pandals = sort_pandals_by_distance(origin_lat, origin_lng, pandals)
    assert len(sorted_pandals) == 2
    assert sorted_pandals[0]["name"] == "Near Pandal"
    assert sorted_pandals[0]["distance_km"] < sorted_pandals[1]["distance_km"]
