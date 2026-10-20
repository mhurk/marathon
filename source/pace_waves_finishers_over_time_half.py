import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

import sim_lib

# Simulation parameters
num_runners = 17500
race_distance = 21.1
random_paces = sim_lib.sample_paces(num_runners)
max_time = 180 + 75  # Maximum time in minutes (180 for half marathon, 360 for full)
time_steps = np.arange(0, max_time + 1)

# Create wave starts: Divide runners into waves
num_waves = 5
wave_intervals = 10    # 10 minute gap between waves
runner_start_times, _ = sim_lib.build_wave_starts(num_runners, num_waves, wave_intervals)

# Precompute the cumulative finisher count for every frame
finishers_over_time = sim_lib.simulate_finishers_over_time(random_paces, runner_start_times, time_steps, race_distance)

# Prepare figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

# Function to update the animation for each time step
def update(frame):
    ax1.clear()
    ax2.clear()
    time_elapsed = time_steps[frame]

    distances = sim_lib.distances_for_active(random_paces, runner_start_times, time_elapsed, race_distance)

    # Plot the updated distribution
    ax1.hist(distances, bins=50, color='purple', alpha=0.6)
    ax1.set_title(f'Distribution of runners at {time_elapsed} minutes\nStart in {num_waves} waves with {wave_intervals} minute interval')
    ax1.set_xlabel('Distance covered (km)')
    ax1.set_ylabel('Number of runners')
    ax1.set_xlim([0, race_distance])
    ax1.set_ylim([0, 2000])
    ax1.grid(True)

    # Plot the number of finishers over time
    ax2.plot(time_steps[:frame + 1], finishers_over_time[:frame + 1], color='purple')
    ax2.set_title('Cumulative number of finishers over time')
    ax2.set_xlabel('Time (minutes)')
    ax2.set_ylabel('Number of finishers')
    ax2.set_xlim([0, max_time])
    ax2.set_ylim([0, num_runners])
    ax2.grid(True)

filename = '../images/' + Path(__file__).stem

sim_lib.save_animation(fig, update, len(time_steps), filename)
