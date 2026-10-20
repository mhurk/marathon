"""Shared GPX-loading and folium HeatMapWithTime plumbing used by the
runners_heatmap_animated_*.py scripts."""

import numpy as np
import folium
from folium.plugins import HeatMapWithTime
import gpxpy

import sim_lib


def load_gpx_route(file_path):
    """Parse a GPX file and return its track points as [lat, lon] pairs."""
    with open(file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
    return [[point.latitude, point.longitude] for track in gpx.tracks for segment in track.segments for point in segment.points]


def compute_gpx_bounds(route_coords):
    """Bounding box of a route, as [(min_lat, min_lon), (max_lat, max_lon)]."""
    latitudes, longitudes = zip(*route_coords)
    min_lat, max_lat = min(latitudes), max(latitudes)
    min_lon, max_lon = min(longitudes), max(longitudes)
    return [(min_lat, min_lon), (max_lat, max_lon)]


def map_distance_to_coords(distances, route_coords, default_start_coord, race_distance):
    """Map each runner's distance covered onto a point along the route.

    race_distance is passed explicitly by the caller rather than guessed.
    """
    num_points = len(route_coords)
    distances = np.clip(distances, 0, race_distance)

    coords_indices = (np.array(distances) / race_distance * (num_points - 1)).astype(int)
    coords_indices = np.clip(coords_indices, 0, num_points - 1)

    runner_coords = []
    for idx, dist in zip(coords_indices, distances):
        if dist > 0:
            runner_coords.append(route_coords[idx])
        else:
            runner_coords.append(default_start_coord)
    return runner_coords


def runner_coords_over_time(pace, start_time, route_coords, race_distance, time_steps, default_start_coord):
    """Per-frame runner coordinates over the course of the race."""
    coords_over_time = []
    for time_elapsed in time_steps:
        distances = sim_lib.distances_for_all(pace, start_time, time_elapsed, race_distance)
        coords_over_time.append(map_distance_to_coords(distances, route_coords, default_start_coord, race_distance))
    return coords_over_time


def build_folium_map(bounds, polylines):
    """Map centered on `bounds`, with one folium.PolyLine per (route_coords, color) pair."""
    center_lat = (bounds[0][0] + bounds[1][0]) / 2
    center_lon = (bounds[0][1] + bounds[1][1]) / 2
    m = folium.Map(location=[center_lat, center_lon], zoom_start=15)

    for route_coords, color in polylines:
        folium.PolyLine(locations=route_coords, color=color, weight=2).add_to(m)

    m.fit_bounds(bounds)
    return m


def save_heatmap_with_time(m, heatmap_data, output_html, **heatmap_kwargs):
    """Validate per-frame coordinates, build the HeatMapWithTime layer, and save the map."""
    validated_data = []
    for time_step, coords in enumerate(heatmap_data):
        valid_coords = [[lat, lon] for lat, lon in coords if lat is not None and lon is not None]
        if not valid_coords:
            print(f"Warning: no valid coordinates at time step {time_step}")
        validated_data.append(valid_coords)

    validated_data = [coords for coords in validated_data if coords]
    if not validated_data:
        print("Error: no valid data for the heatmap.")
        return

    HeatMapWithTime(validated_data, **heatmap_kwargs).add_to(m)
    m.save(output_html)
    print(f"Heatmap with time saved to {output_html}")
