"""
app/utils/geo.py
----------------
Geographical utilities for distance calculation and spatial sorting.
Uses the Haversine formula to compute great-circle distances between GPS coordinates.
"""

import math
from typing import Dict, List, Optional, Tuple


def haversine_distance(
    lat1: float, lon1: float, lat2: float, lon2: float
) -> float:
    """
    Calculate the great-circle distance between two points in kilometers
    using the Haversine formula.
    """
    R = 6371.0  # Earth radius in kilometers

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2.0) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2.0) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)


def sort_pandals_by_distance(
    origin_lat: float, origin_lng: float, pandals: List[Dict]
) -> List[Dict]:
    """
    Computes distance from origin to each pandal that has valid coordinates,
    and returns a sorted list of pandals with distance_km attached.
    """
    result = []
    for pandal in pandals:
        loc = pandal.get("location") or {}
        p_lat = loc.get("latitude")
        p_lng = loc.get("longitude")

        if p_lat is not None and p_lng is not None:
            dist = haversine_distance(origin_lat, origin_lng, p_lat, p_lng)
            pandal_copy = dict(pandal)
            pandal_copy["distance_km"] = dist
            result.append(pandal_copy)

    result.sort(key=lambda x: x["distance_km"])
    return result
