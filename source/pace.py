import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Simulation parameters
num_runners = 1000
race_distance = 42.2  # km
race_start_time = 10 * 60  # 10:00 AM in minutes from midnight
simulation_time = 300  # Simulate 5 hours (in minutes) after race starts
random_paces = np.random.normal(5.434008, 0.834381, num_runners)  # Random pace in minutes per km, normal distribution assumed

max_time = 300  # Maximum time in minutes (5 hours)
time_steps = np.arange(0, max_time + 1)  # Every minute from 0 to 180 minutes

# Create a DataFrame to store runner data
runners_df = pd.DataFrame({
    'RunnerID': range(1, num_runners + 1),
    'Pace': random_paces  # Pace in minutes per km
})

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
    ax.set_title(f'Distribution of runners at {time_elapsed} minutes')
    ax.set_xlabel('Distance covered (km)')
    ax.set_ylabel('Number of runners')
    ax.set_xlim([0, race_distance])
    ax.set_ylim([0, 100])
    ax.grid(True)
    #ax.text(0, -12, "1000 runners, average pace of 5.43 min/km and st.dev of 0.83, no waves.")

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=len(time_steps), repeat=False)

# Save animation as a video file
ani.save('./images/marathon_simulation_animation_no_waves.mp4', writer='ffmpeg', fps=10)

