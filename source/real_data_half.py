import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from import_real_data import import_and_clean_results
import sim_lib

# Runner parameters
file_path = '../data/Uits04_8_HalfASML.xlsx'
df_cleaned = import_and_clean_results(file_path)

# Simulation parameters
num_runners = len(df_cleaned)
race_distance = 21.1
max_time = 180 + 75  # Maximum time in minutes (180 for half marathon, 360 for full)
time_steps = np.arange(0, max_time + 1)

pace = df_cleaned['Pace'].to_numpy()
start_time = df_cleaned['StartTimeHalf'].to_numpy()

# Precompute the cumulative finisher count for every frame
finishers_over_time = sim_lib.simulate_finishers_over_time(pace, start_time, time_steps, race_distance)

# Prepare figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

# Function to update the animation for each time step
def update(frame):
    ax1.clear()
    ax2.clear()
    time_elapsed = time_steps[frame]

    distances = sim_lib.distances_for_active(pace, start_time, time_elapsed, race_distance)

    # Plot the updated distribution
    ax1.hist(distances, bins=50, color='deeppink', alpha=0.7)
    ax1.set_title(f'Distribution of runners at {time_elapsed} minutes')
    ax1.set_xlabel('Distance covered (km)')
    ax1.set_ylabel('Number of runners')
    ax1.set_xlim([0, race_distance])
    ax1.set_ylim([0, num_runners/10])
    ax1.grid(True)

    # Plot the number of finishers over time
    ax2.plot(time_steps[:frame + 1], finishers_over_time[:frame + 1], color='deeppink')
    ax2.set_title('Cumulative number of finishers over time')
    ax2.set_xlabel('Time (minutes)')
    ax2.set_ylabel('Number of finishers')
    ax2.set_xlim([0, max_time])
    ax2.set_ylim([0, num_runners])
    ax2.grid(True)

filename = '../images/' + Path(__file__).stem

sim_lib.save_animation(fig, update, len(time_steps), filename)
