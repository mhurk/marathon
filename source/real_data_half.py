import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pathlib import Path

from import_real_data import *


# Runner parameters
file_path = '../data/Uits04_8_HalfASML.xlsx'
df_cleaned = import_and_clean_results(file_path)

# Simulation parameters
num_runners = len(df_cleaned)
race_distance = 21.1
max_time = 180 + 75  # Maximum time in minutes (180 for half marathon, 360 for full)
time_steps = np.arange(0, max_time + 1)

# Create an array of runner start times based on the start rate
runner_start_times = df_cleaned['StartTimeHalf']

# Create a DataFrame to store runner data, including their start time
runners_df = pd.DataFrame({
    # 'RunnerID': range(1, num_runners + 1),
    'Pace': df_cleaned['Pace'],  
    'StartTime': runner_start_times  # Start time in minutes
})

# Prepare figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

# Initialize list to keep track of the number of finishers over time
finishers_over_time = [0]  # Start with 0 finishers at time 0

# Function to update the animation for each time step
def update(frame):
    ax1.clear()
    ax2.clear()
    time_elapsed = time_steps[frame]
    
    total_finishers = 0
    
    # time_elapsed = time_steps[frame]
    
    # Only consider runners who have started
    active_runners = runners_df[runners_df['StartTime'] <= time_elapsed]
    
    # Calculate how long each active runner has been running
    running_time = time_elapsed - active_runners['StartTime']
    
    # Calculate distance covered for each active runner
    distances = running_time / active_runners['Pace']
    distances = np.where(distances > race_distance, race_distance, distances)
    
    # Count how many runners have finished
    total_finishers += np.sum(distances >= race_distance)
    
    # Ensure the finishers_over_time list matches the current frame count
    if len(finishers_over_time) <= frame:
        finishers_over_time.append(total_finishers)
    else:
        finishers_over_time[frame] = total_finishers
    
    # Plot the updated distribution
    ax1.hist(distances, bins=50, color='deeppink', alpha=0.7)
    ax1.set_title(f'Distribution of runners at {time_elapsed} minutes')
    ax1.set_xlabel('Distance covered (km)')
    ax1.set_ylabel('Number of runners')
    ax1.set_xlim([0, race_distance])
    ax1.set_ylim([0, num_runners/10])
    ax1.grid(True)

    # Plot the number of finishers over time
    ax2.plot(time_steps[:len(finishers_over_time)], finishers_over_time, color='deeppink')
    ax2.set_title('Cumulative number of finishers over time')
    ax2.set_xlabel('Time (minutes)')
    ax2.set_ylabel('Number of finishers')
    ax2.set_xlim([0, max_time])
    ax2.set_ylim([0, num_runners])
    ax2.grid(True)

filename = '../images/' + Path(__file__).stem

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=len(time_steps), repeat=False)
ani.save(filename + '.mp4', writer='ffmpeg', fps=10)

# Store last frame
update(len(time_steps) - 1)  # Update to the last frame
plt.savefig(filename + '_last_frame.png', dpi=300)