import numpy as np
from pathlib import Path

import sim_lib
import heatmap_lib

filename = '../images/' + Path(__file__).stem + '.html'

# Simulation parameters
# Full marathon
race_distance_full = 42.2
num_runners_full = 600      # 10% of actual starters to keep the file size under control
random_paces_full = sim_lib.sample_paces(num_runners_full)
num_waves_full = 10
wave_intervals_full = 1
max_time = 360  # Maximum time in minutes (same for both distances)
time_steps = np.arange(5, max_time + 1)  # Every 5 minutes
runner_start_times_full, _ = sim_lib.build_wave_starts(num_runners_full, num_waves_full, wave_intervals_full)

# Half marathon
race_distance_half = 21.1
num_runners_half = 1750    # 10% of actual starters to keep the file size under control
random_paces_half = sim_lib.sample_paces(num_runners_half)
num_waves_half = 5
wave_intervals_half = 15
start_offset = 90 #half marathon starts 90 minutes after the full
runner_start_times_half, _ = sim_lib.build_wave_starts(num_runners_half, num_waves_half, wave_intervals_half, offset=start_offset)

# Read GPX files
route_coords_full = heatmap_lib.load_gpx_route("../temp/Course_Marathon_Eindhoven_2025_full_fixed_density.gpx")
route_coords_half = heatmap_lib.load_gpx_route("../gpxfiles/Course_Marathon_Eindhoven_2024_half.gpx")

# Get the default start coordinate
default_start_coord_full = route_coords_full[0]
default_start_coord_half = route_coords_half[0]

# Calculate the bounding box of both routes
bounds = heatmap_lib.compute_gpx_bounds(route_coords_full + route_coords_half)

# Simulate runner coordinates at each time step
runner_coords_over_time_full = heatmap_lib.runner_coords_over_time(
    random_paces_full, runner_start_times_full, route_coords_full, race_distance_full, time_steps, default_start_coord_full
)
runner_coords_over_time_half = heatmap_lib.runner_coords_over_time(
    random_paces_half, runner_start_times_half, route_coords_half, race_distance_half, time_steps, default_start_coord_half
)

# Merge the full and half marathon runner coordinates into a single per-frame dataset
heatmap_data = [coords_full + coords_half for coords_full, coords_half in zip(runner_coords_over_time_full, runner_coords_over_time_half)]

# Build the map and the time-based heatmap animation
m = heatmap_lib.build_folium_map(bounds, [(route_coords_full, 'blue'), (route_coords_half, 'purple')])
heatmap_lib.save_heatmap_with_time(
    m, heatmap_data, filename,
    min_speed = 4.5,
    radius = 12,
    auto_play = True,
    max_opacity = 0.95,
    min_opacity = 0,
    use_local_extrema = True,
)
