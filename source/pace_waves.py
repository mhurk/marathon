import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Simulation parameters
num_runners = 1000
race_distance = 42.2
random_paces = np.random.normal(5.5, 0.67, num_runners)  # Random pace in minutes per km, normal distribution assumed
max_time = 360  # Maximum time in minutes (180 for half marathon, 360 for full)
time_steps = np.arange(0, max_time + 1)

# Create wave starts: Divide runners intowaves
num_waves = 5
wave_intervals = 15  # 10-minute gaps between each wave
runners_per_wave = num_runners // num_waves
wave_start_times = np.array([i * wave_intervals for i in range(num_waves)])
runner_start_times = np.repeat(wave_start_times, runners_per_wave)

# Create a DataFrame to store runner data, including their start time
runners_df = pd.DataFrame({
    # 'RunnerID': range(1, num_runners + 1),
    'Pace': random_paces,  
    'StartTime': runner_start_times  # Start time in minutes
})

# Prepare figure
fig, ax = plt.subplots(figsize=(10, 6))

# Function to update the animation for each time step
def update(frame):
    ax.clear()
    time_elapsed = time_steps[frame]
    
    # Only consider runners who have started
    active_runners = runners_df[runners_df['StartTime'] <= time_elapsed]
    
    # Calculate how long each active runner has been running
    running_time = time_elapsed - active_runners['StartTime']
    
    # Calculate distance covered for each active runner
    distances = running_time / active_runners['Pace']
    distances = np.where(distances > race_distance, race_distance, distances)
    
    # Plot the updated distribution
    ax.hist(distances, bins=50, color='blue', alpha=0.6)
    ax.set_title(f'Distribution of runners at {time_elapsed} minutes')
    ax.set_xlabel('Distance covered (km)')
    ax.set_ylabel('Number of runners')
    ax.set_xlim([0, race_distance])
    ax.set_ylim([0, 100])
    ax.grid(True)

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=len(time_steps), repeat=False)
ani.save('./images/marathon_wave_simulation_animation.mp4', writer='ffmpeg', fps=10)
