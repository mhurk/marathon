import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Simulation parameters
num_runners = 1000
race_distance = 42.2  # km
race_start_time = 10 * 60  # 10:00 AM in minutes from midnight
simulation_time = 240  # Simulate 3 hours (in minutes) after race starts
random_paces = np.random.uniform(4, 6, num_runners)  # Random pace in minutes per km

max_time = 240  # Maximum time in minutes (3 hours)
time_steps = np.arange(0, max_time + 1)  # Every minute from 0 to 180 minutes

# Create a DataFrame to store runner data
runners_df = pd.DataFrame({
    'RunnerID': range(1, num_runners + 1),
    'Pace': random_paces  # Pace in minutes per mile
})

# # Simulate distance covered by each runner at a given time (e.g., 3 hours into the race)
# time_elapsed = simulation_time  # in minutes
# runners_df['DistanceCovered'] = time_elapsed / runners_df['Pace']  # Distance in miles

# # Cap distances at the total race distance (26.2 miles)
# runners_df['DistanceCovered'] = np.where(runners_df['DistanceCovered'] > race_distance, race_distance, runners_df['DistanceCovered'])

# # Visualize distribution of runners along the course
# plt.figure(figsize=(10, 6))
# plt.hist(runners_df['DistanceCovered'], bins=30, color='blue', alpha=0.7)
# plt.title(f'Distribution of Runners after {simulation_time} minutes')
# plt.xlabel('Distance Covered (km)')
# plt.ylabel('Number of Runners')
# plt.grid(True)
# plt.show()



# Prepare figure
fig, ax = plt.subplots(figsize=(10, 6))

# Function to update the animation for each time step
def update(frame):
    ax.clear()
    time_elapsed = time_steps[frame]
    distances = time_elapsed / runners_df['Pace']  # Distance in km
    distances = np.where(distances > race_distance, race_distance, distances)
    
    # Plot the updated distribution
    ax.hist(distances, bins=50, color='blue', alpha=0.5)
    ax.set_title(f'Distribution of Runners at {time_elapsed} minutes')
    ax.set_xlabel('Distance Covered (km)')
    ax.set_ylabel('Number of Runners')
    ax.set_xlim([0, race_distance])
    ax.set_ylim([0, 100])
    ax.grid(True)

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=len(time_steps), repeat=False)

# Save animation as a video file
ani.save('.\images\marathon_simulation_animation.mp4', writer='ffmpeg', fps=10)

# To show the animation in a window
plt.show()
