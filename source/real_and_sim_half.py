import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pathlib import Path
from tqdm import tqdm

from import_real_data import *

# General parameters
race_distance = 21.1                      # km
max_time = 260                            # time for simulation
time_steps = np.arange(0, max_time + 1)   

# Runner parameters real data
file_path = '../data/results_marathon_eindhoven_2024.xlsx'
df_real = import_and_clean_results(file_path)
num_runners_real = len(df_real)

# DataFrame to store runner data, including their start time
df_real = pd.DataFrame({
    'Pace': df_real['Pace'],  
    'StartTime': df_real['StartTimeHalf'] 
})

# Simulation parameters
num_runners_sim = 15000
random_paces = np.random.normal(5.434008, 0.834381, num_runners_sim)  # Random pace in minutes per km, normal distribution assumed
start_rate = 15000 / 90  # Runners per minute

# Calculate the total time required to start all runners
total_start_time = num_runners_sim / start_rate  # Time in minutes

# Create a DataFrame to store runner data, including their start time
df_sim = pd.DataFrame({
    'Pace': random_paces,  
    'StartTime': np.linspace(0, total_start_time, num_runners_sim)  # Start time in minutes
})

# Prepare figure with subplots
fig = plt.figure(figsize=(12, 8))
ax1 = plt.subplot2grid((2, 4), (0, 0), colspan=2)
ax2 = plt.subplot2grid((2, 4), (1, 0), colspan=2)
ax3 = plt.subplot2grid((2, 4), (0, 2), rowspan=2, colspan=2)

# Initialize list to keep track of the number of finishers over time
finishers_over_time_real = [0]  # Start with 0 finishers at time 0
finishers_over_time_sim = [0]  # Start with 0 finishers at time 0

# Initialize progress bar
progress_bar = tqdm(total=len(time_steps))

# Function to update the animation for each time step
def update(frame):
    ax1.clear()
    ax2.clear()
    ax3.clear()
    time_elapsed = time_steps[frame]
    
    total_finishers_real = 0
    total_finishers_sim = 0
    
    # Only consider runners who have started
    active_runners_real = df_real[df_real['StartTime'] <= time_elapsed]
    active_runners_sim = df_sim[df_sim['StartTime'] <= time_elapsed]
    
    # Calculate how long each active runner has been running
    running_time_real = time_elapsed - active_runners_real['StartTime']
    running_time_sim = time_elapsed - active_runners_sim['StartTime']
    
    # Calculate distance covered for each active runner
    distances_real = running_time_real / active_runners_real['Pace']
    distances_sim = running_time_sim / active_runners_sim['Pace']
    distances_real = np.where(distances_real > race_distance, race_distance, distances_real)
    distances_sim = np.where(distances_sim > race_distance, race_distance, distances_sim)
    
    # Count how many runners have finished
    total_finishers_real += np.sum(distances_real >= race_distance)
    total_finishers_sim += np.sum(distances_sim >= race_distance)
    
    # Ensure the finishers_over_time list matches the current frame count
    if len(finishers_over_time_real) <= frame:
        finishers_over_time_real.append(total_finishers_real)
        finishers_over_time_sim.append(total_finishers_sim)
    else:
        finishers_over_time_real[frame] = total_finishers_real
        finishers_over_time_sim[frame] = total_finishers_sim
    
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
    ax3.plot(time_steps[:len(finishers_over_time_real)], 
             [float(finishers_over_time_real[i]) / num_runners_real * 100 for i in range(len(finishers_over_time_real))], 
             color='red',
             label = 'Runners')     # normalized
    ax3.plot(time_steps[:len(finishers_over_time_sim)],  
             [float(finishers_over_time_sim[i]) / num_runners_sim * 100 for i in range(len(finishers_over_time_sim))], 
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

# Create animation
ani = animation.FuncAnimation(fig, update, frames=len(time_steps), repeat=False)
ani.save(filename + '.mp4', writer='ffmpeg', fps=10)

# Store last frame
update(len(time_steps) - 1)  # Update to the last frame
plt.savefig(filename + '_last_frame.png', dpi=300)

# Close progress bar
progress_bar.close()
