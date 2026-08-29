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

        if (
            isinstance(p_lat, (int, float))
            and isinstance(p_lng, (int, float))
            and -90 <= p_lat <= 90
            and -180 <= p_lng <= 180
        ):
            dist = haversine_distance(origin_lat, origin_lng, float(p_lat), float(p_lng))
            pandal_copy = dict(pandal)
            pandal_copy["distance_km"] = dist
            result.append(pandal_copy)

    result.sort(key=lambda x: x["distance_km"])
    return result


def distance_point_to_segment(
    p_lat: float,
    p_lng: float,
    a_lat: float,
    a_lng: float,
    b_lat: float,
    b_lng: float,
) -> Tuple[float, float]:
    """
    Calculate the minimum distance in km from point P to line segment AB,
    and return (distance_km, t_projection).
    """
    # Equirectangular projection coordinates relative to A
    cos_lat = math.cos(math.radians(a_lat))
    x_b = (b_lng - a_lng) * cos_lat
    y_b = b_lat - a_lat
    x_p = (p_lng - a_lng) * cos_lat
    y_p = p_lat - a_lat

    seg_len_sq = x_b * x_b + y_b * y_b
    if seg_len_sq == 0:
        t = 0.0
    else:
        t = (x_p * x_b + y_p * y_b) / seg_len_sq
        t = max(0.0, min(1.0, t))

    # Closest point Q on segment AB
    q_lat = a_lat + t * (b_lat - a_lat)
    q_lng = a_lng + t * (b_lng - a_lng)

    dist = haversine_distance(p_lat, p_lng, q_lat, q_lng)
    return dist, t


def distance_point_to_polyline(
    p_lat: float, p_lng: float, polyline_coords: List[List[float]]
) -> Tuple[float, float]:
    """
    Calculate the minimum distance from point P to a polyline of GeoJSON coordinates [[lng, lat], ...].
    Returns (min_distance_km, progress_ratio).
    """
    if not polyline_coords:
        return 0.0, 0.0

    if len(polyline_coords) == 1:
        single_lng, single_lat = polyline_coords[0][0], polyline_coords[0][1]
        return haversine_distance(p_lat, p_lng, single_lat, single_lng), 0.0

    num_segments = len(polyline_coords) - 1
    min_dist = float("inf")
    best_progress = 0.0

    for i in range(num_segments):
        a_lng, a_lat = polyline_coords[i][0], polyline_coords[i][1]
        b_lng, b_lat = polyline_coords[i + 1][0], polyline_coords[i + 1][1]

        dist, t = distance_point_to_segment(p_lat, p_lng, a_lat, a_lng, b_lat, b_lng)
        if dist < min_dist:
            min_dist = dist
            best_progress = (i + t) / float(num_segments)

    return round(min_dist, 3), round(best_progress, 4)


def order_pandals_along_polyline(
    pandals: List[Dict],
    polyline_coords: List[List[float]],
    max_detour_km: float = 1.0,
) -> List[Dict]:
    """
    Filters pandals within max_detour_km of the route polyline,
    eliminates duplicate pandals, and orders them sequentially along the route progress.
    """
    candidates = []
    seen_ids = set()

    for pandal in pandals:
        loc = pandal.get("location") or {}
        p_lat = loc.get("latitude")
        p_lng = loc.get("longitude")

        # Validate coordinates
        if (
            not isinstance(p_lat, (int, float))
            or not isinstance(p_lng, (int, float))
            or not (-90 <= p_lat <= 90)
            or not (-180 <= p_lng <= 180)
        ):
            continue

        pandal_id = str(pandal.get("id") or pandal.get("_id") or pandal.get("name"))
        if pandal_id in seen_ids:
            continue

        detour_dist, progress = distance_point_to_polyline(
            float(p_lat), float(p_lng), polyline_coords
        )

        if detour_dist <= max_detour_km:
            pandal_copy = dict(pandal)
            pandal_copy["detour_distance_km"] = detour_dist
            pandal_copy["route_progress_ratio"] = progress
            candidates.append(pandal_copy)
            seen_ids.add(pandal_id)

    # Sort along route progress (Point A -> Point B)
    candidates.sort(key=lambda x: x["route_progress_ratio"])
    return candidates

