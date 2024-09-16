import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Simulation parameters
num_runners_full = 6000
num_runners_half = 17500
race_distance_full = 42.2  # Full marathon distance in km
race_distance_half = 21.1  # Half marathon distance in km
random_paces_full = np.random.normal(5.434008, 0.834381, num_runners_full)  # Random pace in minutes per km, normal distribution assumed
random_paces_half = np.random.normal(5.434008, 0.834381, num_runners_half)  # Random pace in minutes per km
max_time = 360 + 10  # Maximum time in minutes
time_steps = np.arange(0, max_time + 1)

# Create wave starts: Divide runners into waves
# full
num_waves_full = 10
wave_intervals_full = 1  # 1 minute gap to simulate 10 minutes for the start pen to clear
runners_per_wave_full = num_runners_full // num_waves_full
wave_start_times_full = np.array([i * wave_intervals_full for i in range(num_waves_full)])
runner_start_times_full = np.repeat(wave_start_times_full, runners_per_wave_full)

# half
num_waves_half = 5
wave_intervals_half = 15  # 1 minute gap to simulate 10 minutes for the start pen to clear
start_offset = 90 #half marathon starts 90 minutes after the full
runners_per_wave_half = num_runners_half // num_waves_half
wave_start_times_half = np.array([i * wave_intervals_half for i in range(num_waves_half)]) + start_offset
runner_start_times_half = np.repeat(wave_start_times_half, runners_per_wave_half)

# Create DataFrames to store runner data, including their start time
runners_df_full = pd.DataFrame({
    'Pace': random_paces_full,  
    'StartTime': runner_start_times_full  # Start time in minutes
})

runners_df_half = pd.DataFrame({
    'Pace': random_paces_half,  
    'StartTime': runner_start_times_half  # Start time in minutes
})

# Combine DataFrames for both full and half marathon
runners_df_combined = pd.concat([
    runners_df_full.assign(RaceType='Full', RaceDistance=race_distance_full),
    runners_df_half.assign(RaceType='Half', RaceDistance=race_distance_half)
])

# Prepare figure with four subplots
fig = plt.figure(figsize=(12, 8))
ax1 = plt.subplot2grid((2, 4), (0, 0))
ax2 = plt.subplot2grid((2, 4), (0, 1))
ax3 = plt.subplot2grid((2, 4), (1, 0))
ax4 = plt.subplot2grid((2, 4), (1, 1))
ax5 = plt.subplot2grid((2, 4), (0, 2), rowspan=2, colspan=2)

# Initialize lists to keep track of the number of finishers over time for full and half
finishers_over_time_full = [0]
finishers_over_time_half = [0]
finishers_over_time_combined = [0]

titleFont = 9

# Function to update the animation for each time step
def update(frame):
    ax1.clear()
    ax2.clear()
    ax3.clear()
    ax4.clear()
    ax5.clear()
    
    time_elapsed = time_steps[frame]

    # Full marathon calculations
    active_runners_full = runners_df_full[runners_df_full['StartTime'] <= time_elapsed]
    running_time_full = time_elapsed - active_runners_full['StartTime']
    distances_full = running_time_full / active_runners_full['Pace']
    distances_full = np.where(distances_full > race_distance_full, race_distance_full, distances_full)
    total_finishers_full = np.sum(distances_full >= race_distance_full)
    
    # Half marathon calculations
    active_runners_half = runners_df_half[runners_df_half['StartTime'] <= time_elapsed]
    running_time_half = time_elapsed - active_runners_half['StartTime']
    distances_half = running_time_half / active_runners_half['Pace']
    distances_half = np.where(distances_half > race_distance_half, race_distance_half, distances_half)
    total_finishers_half = np.sum(distances_half >= race_distance_half)
      
    # Update finishers over time lists
    if len(finishers_over_time_full) <= frame:
        finishers_over_time_full.append(total_finishers_full)
    else:
        finishers_over_time_full[frame] = total_finishers_full

    if len(finishers_over_time_half) <= frame:
        finishers_over_time_half.append(total_finishers_half)
    else:
        finishers_over_time_half[frame] = total_finishers_half
        
    if len(finishers_over_time_half) == len(finishers_over_time_full):
        finishers_over_time_combined = [h + f for h, f in zip(finishers_over_time_half, finishers_over_time_full)]
    else:
        min_length = min(len(finishers_over_time_half), len(finishers_over_time_full))
        finishers_over_time_combined = [finishers_over_time_half[i] + finishers_over_time_full[i] for i in range(min_length)]
      
    
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
    ax3.plot(time_steps[:len(finishers_over_time_full)], finishers_over_time_full, color='blue')
    ax3.set_title('Cumulative finishers - full marathon',
                  fontsize = titleFont)
    ax3.set_xlabel('Time (minutes)')
    ax3.set_ylabel('Number of finishers')
    ax3.set_xlim([0, max_time])
    ax3.set_ylim([0, num_runners_full])
    ax3.grid(True)

    # Plot the number of finishers over time for half marathon
    ax4.plot(time_steps[:len(finishers_over_time_half)], finishers_over_time_half, color='purple')
    ax4.set_title('Cumulative finishers - half marathon',
                  fontsize = titleFont)
    ax4.set_xlabel('Time (minutes) after start full')
    ax4.set_ylabel('Number of finishers')
    ax4.set_xlim([0, max_time])
    ax4.set_ylim([0, num_runners_half])
    ax4.grid(True)
      
    # Plot of number of fnishers half and full marathon
    ax5.plot(time_steps[:len(finishers_over_time_full)], finishers_over_time_combined, color='green')
    ax5.set_title('Cumulative finishers - full and half marathon')
    ax5.set_xlabel('Time (minutes)')
    ax5.set_ylabel('Number of finishers')
    ax5.set_xlim([0, max_time])
    ax5.set_ylim([0, num_runners_half + num_runners_full])
    ax5.grid(True)

    plt.tight_layout()


# Create the animation
ani = animation.FuncAnimation(fig, update, frames=len(time_steps), repeat=False)
ani.save('../images/wave_simulation_animation_finishers_combined.mp4', writer='ffmpeg', fps=10)

# Store last frame
update(len(time_steps) - 1)  # Update to the last frame
plt.savefig('../images/wave_simulation_finishers_last_frame_combined.png', dpi=300)
