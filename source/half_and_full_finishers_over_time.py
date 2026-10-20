import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

import sim_lib

# Simulation parameters
num_runners_full = 6000
num_runners_half = 17500
race_distance_full = 42.2  # Full marathon distance in km
race_distance_half = 21.1  # Half marathon distance in km
random_paces_full = sim_lib.sample_paces(num_runners_full)
random_paces_half = sim_lib.sample_paces(num_runners_half)
max_time = 360 + 10  # Maximum time in minutes
time_steps = np.arange(0, max_time + 1)

# Create wave starts: Divide runners into waves
# full
num_waves_full = 10
wave_intervals_full = 1  # 1 minute gap to simulate 10 minutes for the start pen to clear
runner_start_times_full, _ = sim_lib.build_wave_starts(num_runners_full, num_waves_full, wave_intervals_full)

# half
num_waves_half = 5
wave_intervals_half = 10    # 10 minute gap between waves
start_offset = 90 #half marathon starts 90 minutes after the full
runner_start_times_half, _ = sim_lib.build_wave_starts(num_runners_half, num_waves_half, wave_intervals_half, offset=start_offset)

# Precompute the cumulative finisher counts for every frame
finishers_over_time_full = sim_lib.simulate_finishers_over_time(random_paces_full, runner_start_times_full, time_steps, race_distance_full)
finishers_over_time_half = sim_lib.simulate_finishers_over_time(random_paces_half, runner_start_times_half, time_steps, race_distance_half)
finishers_over_time_combined = finishers_over_time_full + finishers_over_time_half

# Prepare figure with four subplots
fig = plt.figure(figsize=(12, 8))
ax1 = plt.subplot2grid((2, 4), (0, 0))
ax2 = plt.subplot2grid((2, 4), (0, 1))
ax3 = plt.subplot2grid((2, 4), (1, 0))
ax4 = plt.subplot2grid((2, 4), (1, 1))
ax5 = plt.subplot2grid((2, 4), (0, 2), rowspan=2, colspan=2)

titleFont = 9

# Function to update the animation for each time step
def update(frame):
    ax1.clear()
    ax2.clear()
    ax3.clear()
    ax4.clear()
    ax5.clear()

    time_elapsed = time_steps[frame]

    distances_full = sim_lib.distances_for_active(random_paces_full, runner_start_times_full, time_elapsed, race_distance_full)
    distances_half = sim_lib.distances_for_active(random_paces_half, runner_start_times_half, time_elapsed, race_distance_half)

    # Plot the updated distribution for full marathon
    ax1.hist(distances_full, bins=50, color='blue', alpha=0.6)
    ax1.set_title(f'Full marathon at {time_elapsed} minutes',
                  fontsize = titleFont)
    ax1.set_xlabel('Distance covered (km)')
    ax1.set_ylabel('Number of runners')
    ax1.set_xlim([0, race_distance_full])
    ax1.set_ylim([0, num_runners_full // num_waves_full])
    ax1.grid(True)

    # Plot the updated distribution for half marathon
    ax2.hist(distances_half, bins=50, color='purple', alpha=0.6)
    ax2.set_title(f'Half marathon at {time_elapsed - start_offset} minutes',
                  fontsize = titleFont)
    ax2.set_xlabel('Distance covered (km)')
    ax2.set_ylabel('Number of runners')
    ax2.set_xlim([0, race_distance_half])
    ax2.set_ylim([0, num_runners_half // num_waves_half])
    ax2.grid(True)

    # Plot the number of finishers over time for full marathon
    ax3.plot(time_steps[:frame + 1], finishers_over_time_full[:frame + 1], color='blue')
    ax3.set_title('Cumulative finishers - full marathon',
                  fontsize = titleFont)
    ax3.set_xlabel('Time (minutes)')
    ax3.set_ylabel('Number of finishers')
    ax3.set_xlim([0, max_time])
    ax3.set_ylim([0, num_runners_full])
    ax3.grid(True)

    # Plot the number of finishers over time for half marathon
    ax4.plot(time_steps[:frame + 1], finishers_over_time_half[:frame + 1], color='purple')
    ax4.set_title('Cumulative finishers - half marathon',
                  fontsize = titleFont)
    ax4.set_xlabel('Time (minutes) after start full')
    ax4.set_ylabel('Number of finishers')
    ax4.set_xlim([0, max_time])
    ax4.set_ylim([0, num_runners_half])
    ax4.grid(True)

    # Plot of number of fnishers half and full marathon
    ax5.plot(time_steps[:frame + 1], finishers_over_time_combined[:frame + 1], color='green')
    ax5.set_title('Cumulative finishers - full and half marathon')
    ax5.set_xlabel('Time (minutes)')
    ax5.set_ylabel('Number of finishers')
    ax5.set_xlim([0, max_time])
    ax5.set_ylim([0, num_runners_half + num_runners_full])
    ax5.grid(True, color='grey', alpha=0.2, which='minor')
    ax5.grid(True, color='grey', alpha=0.4, which='major')
    ax5.minorticks_on()

    plt.tight_layout()


filename = '../images/' + Path(__file__).stem

sim_lib.save_animation(fig, update, len(time_steps), filename)
