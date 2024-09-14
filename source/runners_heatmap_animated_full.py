import os
import numpy as np
import pandas as pd
import folium
from folium.plugins import HeatMapWithTime
import gpxpy
import gpxpy.gpx

# Load the GPX file to get route coordinates
def load_gpx_route(file_path):
    with open(file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    # Extract latitude and longitude points
    route_coords = [[point.latitude, point.longitude] for track in gpx.tracks for segment in track.segments for point in segment.points]
    return route_coords

# Mapping runner distance to coordinates along the route
def map_distance_to_coords(distances, route_coords, default_start_coord):
    num_points = len(route_coords)
    max_distance = 42.2

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
            # Use the default start coordinate if the runner hasn't moved yet
            runner_coords.append(default_start_coord)

    # Ensure there are no invalid coordinates
    valid_runner_coords = [(lat, lon) for lat, lon in runner_coords if lat is not None and lon is not None]

    return valid_runner_coords

# Create a single HTML heatmap with time-based animation using HeatMapWithTime
def create_heatmap_with_time(runner_coords_over_time, route_coords, bounds, output_html='../images/heatmap_animated_full.html'):
  
    # Initialize the map centered around the bounding box center
    center_lat = (bounds[0][0] + bounds[1][0]) / 2
    center_lon = (bounds[0][1] + bounds[1][1]) / 2
    m = folium.Map(location=[center_lat, center_lon], zoom_start=15)  # Increased zoom level for better visibility
    
     # Keep the full course visible by adding the entire route as a polyline
    folium.PolyLine(locations=route_coords, color='blue', weight=2).add_to(m)

    # Fit the map to the bounds of the route
    m.fit_bounds(bounds)

    # Prepare data for HeatMapWithTime (list of runner coordinates at each time step)
    heatmap_data = []
    for time_step, coords in enumerate(runner_coords_over_time):
        # Validate each coordinate pair before adding it to the heatmap
        valid_coords = [[coord[0], coord[1]] for coord in coords if isinstance(coord, tuple) and coord[0] is not None and coord[1] is not None]
        
        # Add debug output to ensure all coordinates are properly validated
        if not valid_coords:
            print(f"Warning: No valid coordinates at time step {time_step}")
        
        heatmap_data.append(valid_coords)

    # Check if data is correctly structured
    if len(heatmap_data) == 0:
        print("Error: No heatmap data to display.")
        return
    
    # Filter out empty lists to avoid issues with empty frames
    heatmap_data = [coords for coords in heatmap_data if coords]
    
    if not heatmap_data:
        print("Error: No valid data for the heatmap.")
        return

    # Adjust heatmap settings to improve visibility
    # more settings and details: https://github.com/python-visualization/folium/blob/main/folium/plugins/heat_map_withtime.py
    HeatMapWithTime(
        heatmap_data,
        min_speed=2.0,
        radius=12,          
        auto_play=True,
        max_opacity=0.7,    
        min_opacity=0.1,    
        use_local_extrema=True  
    ).add_to(m)

    # Save the map to an HTML file
    m.save(output_html)
    print(f"Heatmap with time saved to {output_html}")

# Compute the bounding box of the GPX route
def compute_gpx_bounds(route_coords):
    latitudes, longitudes = zip(*route_coords)
    min_lat, max_lat = min(latitudes), max(latitudes)
    min_lon, max_lon = min(longitudes), max(longitudes)
    return [(min_lat, min_lon), (max_lat, max_lon)]

# Simulation parameters
num_runners = 6000
race_distance = 42.2
random_paces = np.random.normal(5.434008, 0.834381, num_runners)  # Random pace in minutes per km, normal distribution assumed
max_time = 360 + 10  # Maximum time in minutes (180 for half marathon, 360 for full)
time_steps = np.arange(0, max_time + 1, 5)  # Every 5 minutes

# Create wave starts: Divide runners into 4 waves starting 15 minutes apart
num_waves = 10
wave_intervals = 1  # 1-minute gaps between each wave, to simulate the 0 minute start period (this is not the preferred solution but the least code change, for now)
runners_per_wave = num_runners // num_waves
wave_start_times = np.array([i * wave_intervals for i in range(num_waves)])
runner_start_times = np.repeat(wave_start_times, runners_per_wave)

# Create a DataFrame to store runner data, including their start time and wave
runners_df = pd.DataFrame({
    'RunnerID': range(1, num_runners + 1),
    'Pace': random_paces,  # Pace in minutes per km
    'StartTime': runner_start_times,  # Start time in minutes
    'Wave': np.repeat(range(num_waves), runners_per_wave)  # Assign a wave number to each runner
})

# Read GPX file
route_coords = load_gpx_route("../gpxfiles/Course_Marathon_Eindhoven_2024_full.gpx")

# Get the default start coordinate (the first point of the route)
default_start_coord = route_coords[0]

# Calculate the bounding box of the GPX route
bounds = compute_gpx_bounds(route_coords)

# Simulate runner distances covered at each time step
runner_coords_over_time = []
for time_elapsed in time_steps:
    # Calculate the running time for each runner
    running_time = np.maximum(0, time_elapsed - runners_df['StartTime'])  # Runners can't start before their wave

    # Calculate the distances covered for each runner (pace is in minutes per mile, so distance = time / pace)
    distances_covered = running_time / runners_df['Pace']  # Distance in miles
    distances_covered = np.clip(distances_covered, 0, race_distance)  # Cap at race distance

    # Map runner distances to coordinates on the route; use the default start coordinate if they haven't started
    runner_coords = map_distance_to_coords(distances_covered, route_coords, default_start_coord)
    runner_coords_over_time.append(runner_coords)

# Create a time-based heatmap animation and save it to HTML
create_heatmap_with_time(runner_coords_over_time, route_coords, bounds)