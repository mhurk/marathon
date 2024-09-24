import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

while True:
    edition = input("""
                    Choose marathon edition 
                    [1] 2024 edition with start at 10:00 and 11:30
                    [2] 2023 edition with start at 10:00 and 14:00\n
                    """)
    try:
        if edition == '1':
            max_time = 370              # Maximum time for simulation in minutes (370 for 2024 edition, 500 for 2023)
            start_offset = 90           # Half marathon starts 90 minutes after the full in 2024, 240 minutes in 2023 (the reference)
            edition_name = "2024"
            print(f"2024 Edition: Max time {max_time}, Start offset {start_offset}")
            break
        elif edition == '2':
            max_time = 500
            start_offset = 240
            edition_name = "reference"
            print(f"Reference (2023) Edition: Max time {max_time}, Start offset {start_offset}")
            break
        elif edition not in ['1', '2']:
            print("Please choose either 1 or 2")
    except ValueError:
        print("Invalid input, please enter a valid option")

filename = '../images/'+ Path(__file__).stem + "_" + edition_name + '.png'

# Simulation parameters
num_runners_full = 6000
num_runners_half = 17500
race_distance_full = 42.2  # Full marathon distance in km
race_distance_half = 21.1  # Half marathon distance in km
random_paces_full = np.random.normal(5.434008, 0.834381, num_runners_full)  # Random pace in minutes per km, normal distribution assumed
random_paces_half = np.random.normal(5.434008, 0.834381, num_runners_half)  # Random pace in minutes per km
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
wave_intervals_half = 15    # 1 minute gap to simulate 10 minutes for the start pen to clear
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

# Initialize lists to keep track of the number of finishers over time for full and half
finishers_over_time_full = [0]
finishers_over_time_half = [0]
finishers_over_time_combined = [0]

# Initialize DataFrame to store the results
finishers_data = pd.DataFrame(columns=['Time', 'CumulativeFinishersFull', 'CumulativeFinishersHalf', 'CumulativeFinishersCombined'])

# Modify the update function to include the regression
def update(frame):
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
    
    # Store the current frame's data in the DataFrame
    finishers_data.loc[frame] = [
        time_elapsed,
        total_finishers_full,
        total_finishers_half,
        finishers_over_time_combined[-1]
    ]

for frame in range(len(time_steps)):
    update(frame)

#print(finishers_df.head())

# create plots
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 12))

## Create a line plot of Time vs. CumulativeFinishers
ax1.plot(finishers_data['Time'], finishers_data['CumulativeFinishersCombined'], linestyle = '-', color = "orange", linewidth = 2)
ax1.set_title('Cumulative number of finishers over time, full and half')
ax1.set_xlabel('Time')
ax1.set_ylabel('Cumulative finishers')
ax1.grid(True)

# Calculate the growth rate of finishers
finishers_data['GrowthRate'] = finishers_data['CumulativeFinishersCombined'].diff().fillna(0)

# Apply a moving average to smooth the growth rate curve
window_size = 5
finishers_data['SmoothedGrowthRate'] = finishers_data['GrowthRate'].rolling(window=window_size, center=True).mean()

## Plot the growth rate over time
ax2.plot(finishers_data['Time'], finishers_data['GrowthRate'], marker = '.', color = "orange",  alpha=0.5, label = 'Growth rate')
ax2.plot(finishers_data['Time'], finishers_data['SmoothedGrowthRate'], color = 'red', linewidth = 2, label = 'Smoothed growth rate')
ax2.set_title('Growth rate of finishers over time')
ax2.set_xlabel('Time')
ax2.set_ylabel('Growth rate')
ax2.grid(True)
ax2.legend()


## Add FWHM to growth rate

# Find the maximum smoothed growth rate value
max_smoothed_growth_rate = finishers_data['SmoothedGrowthRate'].max()

# Calculate half of the maximum smoothed growth rate
half_max_smoothed = max_smoothed_growth_rate / 2

# Identify the points where the smoothed growth rate crosses half of the maximum value
crossing_indices_smoothed = np.where(finishers_data['SmoothedGrowthRate'] >= half_max_smoothed)[0]

# Determine the time values at these crossing points
if len(crossing_indices_smoothed) >= 2:  # Ensure there are at least two crossing points
    fwhm_start_smoothed = finishers_data['Time'][crossing_indices_smoothed[0]]
    fwhm_end_smoothed = finishers_data['Time'][crossing_indices_smoothed[-1]]
    
    # Calculate the FWHM for the smoothed curve
    fwhm_smoothed = fwhm_end_smoothed - fwhm_start_smoothed
else:
    fwhm_smoothed = None  # If there are not enough crossing points to determine the FWHM

# Plot the smoothed growth rate over time and indicate the FWHM
ax3.plot(finishers_data['Time'], finishers_data['SmoothedGrowthRate'], color='red', label='Smoothed growth rate', linewidth=2)

# Find the time where the maximum smoothed growth rate occurs
max_smoothed_growth_rate_time = finishers_data.loc[finishers_data['SmoothedGrowthRate'].idxmax(), 'Time']

# Add a label for the maximum smoothed growth rate
ax3.annotate(f'Max Growth Rate: {max_smoothed_growth_rate:.0f}',
             xy = (max_smoothed_growth_rate_time, max_smoothed_growth_rate), 
             xytext = (max_smoothed_growth_rate_time + 10, max_smoothed_growth_rate + 1),  # Position of the text label
             arrowprops =  dict(facecolor = 'black', shrink = 0.05, headwidth = 4, headlength = 5),
             fontsize = 8, color = 'black')

# Highlight the FWHM region on the plot
if fwhm_smoothed is not None:
    ax3.axvline(x=fwhm_start_smoothed, color='blue', linestyle='--', label='FWHM Start')
    ax3.axvline(x=fwhm_end_smoothed, color='green', linestyle='--', label='FWHM End')
    ax3.fill_betweenx([0, max_smoothed_growth_rate], fwhm_start_smoothed, fwhm_end_smoothed, color='gray', alpha = 0.2, label = f'FWHM = {fwhm_smoothed:.2f} minutes')

ax3.set_title('Smoothed growth rate of finishers over time with FWHM')
ax3.set_xlabel('Time')
ax3.set_ylabel('Growth rate')
ax3.grid(True)
ax3.legend()

plt.tight_layout()

plt.savefig(filename, dpi=300)

