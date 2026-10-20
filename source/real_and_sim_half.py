import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from tqdm import tqdm

from import_real_data import import_and_clean_results
import sim_lib

# General parameters
race_distance = 21.1                      # km
max_time = 260                            # time for simulation
time_steps = np.arange(0, max_time + 1)

# Runner parameters real data
file_path = '../data/results_marathon_eindhoven_2024.xlsx'
df_real = import_and_clean_results(file_path)
num_runners_real = len(df_real)
pace_real = df_real['Pace'].to_numpy()
start_time_real = df_real['StartTimeHalf'].to_numpy()

# Simulation parameters
num_runners_sim = 15000
pace_sim = sim_lib.sample_paces(num_runners_sim)
# start_rate = num_runners_sim / 90  # Runners per minute
start_rate = 235 # 235 is average number of starting runners per minute, in 2024 data
start_time_sim = sim_lib.build_continuous_starts(num_runners_sim, start_rate)

# Precompute the cumulative finisher counts for every frame
finishers_over_time_real = sim_lib.simulate_finishers_over_time(pace_real, start_time_real, time_steps, race_distance)
finishers_over_time_sim = sim_lib.simulate_finishers_over_time(pace_sim, start_time_sim, time_steps, race_distance)

# Prepare figure with subplots
fig = plt.figure(figsize=(12, 8))
ax1 = plt.subplot2grid((2, 4), (0, 0), colspan=2)
ax2 = plt.subplot2grid((2, 4), (1, 0), colspan=2)
ax3 = plt.subplot2grid((2, 4), (0, 2), rowspan=2, colspan=2)

# Initialize progress bar
progress_bar = tqdm(total=len(time_steps))

# Function to update the animation for each time step
def update(frame):
    ax1.clear()
    ax2.clear()
    ax3.clear()
    time_elapsed = time_steps[frame]

    distances_real = sim_lib.distances_for_active(pace_real, start_time_real, time_elapsed, race_distance)
    distances_sim = sim_lib.distances_for_active(pace_sim, start_time_sim, time_elapsed, race_distance)

    # Plot the updated distribution Real data
    ax1.hist(distances_real, bins=50, color='red', alpha=0.7)
    ax1.set_title(f'Distribution of runners at {time_elapsed} minutes')
    ax1.set_xlabel('Distance covered (km)')
    ax1.set_ylabel('Number of runners')
    ax1.set_xlim([0, race_distance])
    ax1.set_ylim([0, num_runners_real/10])
    ax1.grid(True)

    # Plot the updated distribution Simulation
    ax2.hist(distances_sim, bins=50, color='blue', alpha=0.7)
    ax2.set_title(f'Simulated distribution of runners at {time_elapsed} minutes\n{num_runners_sim / 1000}k runners, start rate of {start_rate:.0f} runners per minute')
    ax2.set_xlabel('Distance covered (km)')
    ax2.set_ylabel('Number of runners')
    ax2.set_xlim([0, race_distance])
    ax2.set_ylim([0, num_runners_sim/10])
    ax2.grid(True)

    # Plot the finishers over time, combined
    ax3.plot(time_steps[:frame + 1],
             finishers_over_time_real[:frame + 1] / num_runners_real * 100,
             color='red',
             label = 'Runners')     # normalized
    ax3.plot(time_steps[:frame + 1],
             finishers_over_time_sim[:frame + 1] / num_runners_sim * 100,
             color='blue',
             label = 'Simulation')
    ax3.set_title('Finished runners over time')
    ax3.set_xlabel('Time (minutes)')
    ax3.set_ylabel('Percentage finished')
    ax3.set_xlim([0, max_time])
    ax3.set_ylim([0, 100])  # 0 - 100%
    ax3.legend(loc="upper left")
    ax3.grid(True)

    plt.tight_layout()

    # Update progress bar
    progress_bar.update(1)

filename = '../images/' + Path(__file__).stem

sim_lib.save_animation(fig, update, len(time_steps), filename)

# Close progress bar
progress_bar.close()
