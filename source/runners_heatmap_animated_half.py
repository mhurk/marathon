import numpy as np
from pathlib import Path

import sim_lib
import heatmap_lib

filename = '../images/' + Path(__file__).stem + '.html'

# Simulation parameters
num_runners = 17500
race_distance = 21.1
random_paces = sim_lib.sample_paces(num_runners)
max_time = 180 + 90  # Maximum time in minutes (180 for half marathon, 360 for full). Duration of start waves needs to be added.
time_steps = np.arange(0, max_time + 1, 5)  # Every 5 minutes

# Create wave starts: Divide runners into 5 waves, 10 minutes apart
num_waves = 5
wave_intervals = 10  # 10-minute gaps between each wave, expected around 250 runners per minute.
runner_start_times, _ = sim_lib.build_wave_starts(num_runners, num_waves, wave_intervals)

# Read GPX file
route_coords = heatmap_lib.load_gpx_route("../gpxfiles/Course_Marathon_Eindhoven_2024_half.gpx")

# Get the default start coordinate (the first point of the route)
default_start_coord = route_coords[0]

# Calculate the bounding box of the GPX route
bounds = heatmap_lib.compute_gpx_bounds(route_coords)

# Simulate runner coordinates at each time step
runner_coords_over_time = heatmap_lib.runner_coords_over_time(
    random_paces, runner_start_times, route_coords, race_distance, time_steps, default_start_coord
)

# Build the map and the time-based heatmap animation
m = heatmap_lib.build_folium_map(bounds, [(route_coords, 'purple')])
heatmap_lib.save_heatmap_with_time(
    m, runner_coords_over_time, filename,
    # more settings and details: https://github.com/python-visualization/folium/blob/main/folium/plugins/heat_map_withtime.py
    min_speed = 4.0,
    radius = 12,
    auto_play = True,
    max_opacity = 0.7,
    min_opacity = 0.1,
    use_local_extrema = True,
)
