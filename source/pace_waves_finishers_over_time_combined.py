import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Simulation parameters
num_runners_full = 6000
num_runners_half = 17500
race_distance_full = 42.2
race_distance_half = 21.1
random_paces_full = np.random.normal(5.434008, 0.834381, num_runners_full)  # Random pace in minutes per km, normal distribution assumed
random_paces_half = np.random.normal(5.434008, 0.834381, num_runners_half)  # two varables to give the possibility for different paces
max_time = 360 + 10  # Maximum time in minutes (180 for half marathon, 360 for full)
time_steps = np.arange(0, max_time + 1)

# Create wave starts: Divide runners into waves
# full
num_waves_full = 10
wave_intervals_full = 1  # 1 minute gap to simulate 10 minutes for the start pen to clear
runners_per_wave_full = num_runners_full // num_waves_full
wave_start_times_full = np.array([i * wave_intervals_full for i in range(num_waves_full)])
runner_start_times = np.repeat(wave_start_times_full, runners_per_wave_full)

# half
num_waves_half = 10
wave_intervals_half = 1  # 1 minute gap to simulate 10 minutes for the start pen to clear
runners_per_wave_half = num_runners_half // num_waves_half
wave_start_times_half = np.array([i * wave_intervals_half for i in range(num_waves_half)])
runner_start_times = np.repeat(wave_start_times_half, runners_per_wave_half)



# Create a DataFrame to store runner data, including their start time
# three dataframes for each marathon distance and combined. Perhaps the combined only is sufficient
runners_df_full = pd.DataFrame({
    # 'RunnerID': range(1, num_runners + 1),
    'Pace': random_paces_full,  
    'StartTime': runner_start_times  # Start time in minutes
})

runners_df_half = pd.DataFrame({
    # 'RunnerID': range(1, num_runners + 1),
    'Pace': random_paces_half,  
    'StartTime': runner_start_times  # Start time in minutes
})

runners_df_combined = pd.DataFrame({
    # 'RunnerID': range(1, num_runners + 1),
    'Pace': random_paces_full,  
    'Pace': random_paces_full,  
    'StartTime': runner_start_times  # Start time in minutes
})


# Prepare figure with two subplots
fig, (ax1, ax2, ax3, ax4) = plt.subplots(2, 2, figsize=(10, 10))

# Initialize list to keep track of the number of finishers over time
finishers_over_time = [0]  # Start with 0 finishers at time 0

# Function to update the animation for each time step
def update(frame):
    ax1.clear()
    ax2.clear()
    ax3.clear()
    ax4.clear()
    
    
    time_elapsed = time_steps[frame]
    
    all_distances = []
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
    
    # Plot the updated distribution full marathon
    ax1.hist(distances, bins=50, color='blue', alpha=0.6)
    ax1.set_title(f'Distribution of runners at {time_elapsed} minutes')
    ax1.set_xlabel('Distance covered (km)')
    ax1.set_ylabel('Number of runners')
    ax1.set_xlim([0, race_distance])
    ax1.set_ylim([0, num_runners/num_waves])
    ax1.grid(True)

    # Plot the updated distribution half marathon
    ax2.hist(distances, bins=50, color='blue', alpha=0.6)
    ax2.set_title(f'Distribution of runners of the full marathon at {time_elapsed} minutes')
    ax2.set_xlabel('Distance covered (km)')
    ax2.set_ylabel('Number of runners')
    ax2.set_xlim([0, race_distance])
    ax2.set_ylim([0, num_runners/num_waves])
    ax2.grid(True)

    # Plot the updated distribution full and half marathon combined
    ax3.hist(distances, bins=50, color='purple', alpha=0.6)
    ax3.set_title(f'Distribution of runners of the half marathon at {time_elapsed} minutes')
    ax3.set_xlabel('Distance covered (km)')
    ax3.set_ylabel('Number of runners')
    ax3.set_xlim([0, race_distance_full])
    ax3.set_ylim([0, num_runners/num_waves])
    ax3.grid(True)

    # Plot the number of finishers over time
    ax4.plot(time_steps[:len(finishers_over_time)], finishers_over_time, color='purple')
    ax4.set_title('Cumulative number of finishers over time')
    ax4.set_xlabel('Time (minutes)')
    ax4.set_ylabel('Number of finishers')
    ax4.set_xlim([0, max_time])
    ax4.set_ylim([0, num_runners])
    ax4.grid(True)

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=len(time_steps), repeat=False)
ani.save('../images/marathon_wave_simulation_animation_finishers_full.mp4', writer='ffmpeg', fps=10)

# Store last frame
update(len(time_steps) - 1)  # Update to the last frame
plt.savefig('../images/marathon_wave_simulation_finishers_last_frame_full.png', dpi=300)