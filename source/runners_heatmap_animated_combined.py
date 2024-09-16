import os
import numpy as np
import pandas as pd
import folium
from folium.plugins import HeatMapWithTime
import gpxpy
import gpxpy.gpx

# Load GPX files
def load_gpx_route(file_path):
    with open(file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
    route_coords = [[point.latitude, point.longitude] for track in gpx.tracks for segment in track.segments for point in segment.points]
    return route_coords

# Mapping runner distance to coordinates along the route
def map_distance_to_coords(distances, route_coords, default_start_coord):
    num_points = len(route_coords)
    max_distance = race_distance_full if len(distances) == num_runners_full else race_distance_half

    # Ensure distances are within the route's bounds
    distances = np.clip(distances, 0, max_distance)

    # Mapping runner's distance covered to indices along the route
    coords_indices = (np.array(distances) / max_distance * (num_points - 1)).astype(int)
    coords_indices = np.clip(coords_indices, 0, num_points - 1)  # Ensure indices are within range

    # Get coordinates for each runner based on their distance covered
    runner_coords = []
    for idx, dist in zip(coords_indices, distances):
        if dist > 0:
            runner_coords.append(route_coords[idx])
        else:
            runner_coords.append(default_start_coord)

    return runner_coords

# Compute the bounding box of the GPX route
def compute_gpx_bounds(route_coords):
    latitudes, longitudes = zip(*route_coords)
    min_lat, max_lat = min(latitudes), max(latitudes)
    min_lon, max_lon = min(longitudes), max(longitudes)
    return [(min_lat, min_lon), (max_lat, max_lon)]

# Create a single HTML heatmap with time-based animation using HeatMapWithTime
def create_heatmap_with_time(runner_coords_over_time_full, runner_coords_over_time_half, route_coords_full, route_coords_half, bounds, output_html='../images/heatmap_animated_combined.html'):
  
    # Initialize the map centered around the bounding box center
    center_lat = (bounds[0][0] + bounds[1][0]) / 2
    center_lon = (bounds[0][1] + bounds[1][1]) / 2
    m = folium.Map(location=[center_lat, center_lon], zoom_start=15)
    
    # Add the entire route as a polyline
    folium.PolyLine(locations=route_coords_full, color='blue', weight=2).add_to(m)
    folium.PolyLine(locations=route_coords_half, color='purple', weight=2).add_to(m)

    # Fit the map to the bounds of the route
    m.fit_bounds(bounds)

    # Prepare data for HeatMapWithTime (list of runner coordinates at each time step)
    heatmap_data = []
    for coords_full, coords_half in zip(runner_coords_over_time_full, runner_coords_over_time_half):
        valid_coords = [[coord[0], coord[1]] for coord in coords_full + coords_half if isinstance(coord, list) and coord[0] is not None and coord[1] is not None]
        heatmap_data.append(valid_coords)

    # Filter out empty lists to avoid issues with empty frames
    heatmap_data = [coords for coords in heatmap_data if coords]

    # Adjust heatmap settings to improve visibility
    HeatMapWithTime(
        heatmap_data,
        min_speed = 4.5,
        radius = 12,          
        auto_play = True,
        max_opacity = 0.95,    
        min_opacity = 0,    
        use_local_extrema = True 
    ).add_to(m)

    # Save the map to an HTML file
    m.save(output_html)
    print(f"Heatmap with time saved to {output_html}")

# Simulation parameters
# Full marathon
race_distance_full = 42.2
num_runners_full = 600      # 10% of actual starters to keep the file size under control
random_paces_full = np.random.normal(5.434008, 0.834381, num_runners_full)  # Random pace in minutes per km
# Create wave starts: Divide runners into waves
num_waves_full = 10
wave_intervals_full = 1
runners_per_wave_full = num_runners_full // num_waves_full
wave_start_times_full = np.array([i * wave_intervals_full for i in range(num_waves_full)])
runner_start_times_full = np.repeat(wave_start_times_full, runners_per_wave_full)
max_time = 360  # Maximum time in minutes (same for both distances)
time_steps = np.arange(5, max_time + 1)  # Every 5 minutes

# Half marathon
race_distance_half = 21.1
num_runners_half = 1750    # 10% of actual starters to keep the file size under control
random_paces_half = np.random.normal(5.434008, 0.834381, num_runners_half)  # Random pace in minutes per km
# Create wave starts: Divide runners into waves
num_waves_half = 5
wave_intervals_half = 15
start_offset = 90 #half marathon starts 90 minutes after the full
runners_per_wave_half = num_runners_half // num_waves_half
wave_start_times_half = np.array([i * wave_intervals_half for i in range(num_waves_half)]) + start_offset
runner_start_times_half = np.repeat(wave_start_times_half, runners_per_wave_half)

# Create DataFrames to store runner data
runners_df_full = pd.DataFrame({
    'RunnerID': range(1, num_runners_full + 1),
    'Pace': random_paces_full,
    'StartTime': runner_start_times_full,
    'Wave': np.repeat(range(num_waves_full), runners_per_wave_full)
})

runners_df_half = pd.DataFrame({
    'RunnerID': range(1, num_runners_half + 1),
    'Pace': random_paces_half,
    'StartTime': runner_start_times_half,
    'Wave': np.repeat(range(num_waves_half), runners_per_wave_half)
})

# Read GPX files
route_coords_full = load_gpx_route("../gpxfiles/Course_Marathon_Eindhoven_2024_full.gpx")
route_coords_half = load_gpx_route("../gpxfiles/Course_Marathon_Eindhoven_2024_half.gpx")

# Get the default start coordinate
default_start_coord_full = route_coords_full[0]
default_start_coord_half = route_coords_half[0]

# Calculate the bounding box of both routes
bounds = compute_gpx_bounds(route_coords_full + route_coords_half)

# Simulate runner distances covered at each time step
runner_coords_over_time_full = []
runner_coords_over_time_half = []
for time_elapsed in time_steps:
    # Full marathon
    running_time_full = np.maximum(0, time_elapsed - runners_df_full['StartTime'])
    distances_covered_full = running_time_full / runners_df_full['Pace']
    distances_covered_full = np.clip(distances_covered_full, 0, race_distance_full)
    runner_coords_full = map_distance_to_coords(distances_covered_full, route_coords_full, default_start_coord_full)
    runner_coords_over_time_full.append(runner_coords_full)

    # Half marathon
    running_time_half = np.maximum(0, time_elapsed - runners_df_half['StartTime'])
    distances_covered_half = running_time_half / runners_df_half['Pace']
    distances_covered_half = np.clip(distances_covered_half, 0, race_distance_half)
    runner_coords_half = map_distance_to_coords(distances_covered_half, route_coords_half, default_start_coord_half)
    runner_coords_over_time_half.append(runner_coords_half)

# Create a time-based heatmap animation and save it to HTML
create_heatmap_with_time(runner_coords_over_time_full, runner_coords_over_time_half, route_coords_full, route_coords_half, bounds)
