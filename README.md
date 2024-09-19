![GitHub Created At](https://img.shields.io/github/created-at/mhurk/marathon)
![GitHub repo file or directory count](https://img.shields.io/github/directory-file-count/mhurk/marathon)
![GitHub repo size](https://img.shields.io/github/repo-size/mhurk/marathon)
![GitHub language count](https://img.shields.io/github/languages/count/mhurk/marathon)
![GitHub last commit](https://img.shields.io/github/last-commit/mhurk/marathon)

# Marathon Simulation
Simulation of distribution of runners on a marathon course. Simulated for full and half marathon only, not for other distances like 1/4 marathon or business run.

- Uses start waves, total number of runners equally distributed over waves.
- Normal distribution or gamma distribution is okay to use, based on the 2017 marathon data. (see [distribution_identification.md](https://github.com/mhurk/marathon/blob/main/distribution_identification.md))
- Assumes pace distribution is the same for all start waves and distances. This is not fully correct, faster runners will start mainly in earlier waves.
- Assumes all runners starts simultaneously, per wave. Number of runners distributed evenly over waves.
- Assumes constant pace during the entire race.
- Generate animation of distribution over runners over the course (moving histogram)
- Show number of runners crossing the finish line as function of time.
- Animated heatmap of runners on the course (I think this is really cool!)
- Combine half and full marathon
    - For ASML Marathon Eindhoven 2024:
    - Half marathon has 5 start waves at 11:30, 11:45, 12:00, 12:15 en 12:30 (total 17500 runners). 
    - Full marathon has 1 start wave which lasts around 10 minutes, starting at 10:00 (10:00 - 10:10), 6000 runners. (modelled as 10 waves with 1 minute interval)
- Added event with start times as in previous editions of this even (full at 10:00, half at 14:00). Compared effect of both schedules on number of finishers over time

I estimate the number of finishers at **around 260 per minute** during the hour after 200 minutes from the start of the full marathon. So for a start at 10:00 this translate to 260 runners per minute from 13:20 - 14:20.

## Moving histogram and finishers over time
![image](https://github.com/user-attachments/assets/ff8ece7f-6263-408d-9b90-94c2495067ac)
<sub>Screenshot from moving histogram (top left) and the number of finishers as function of time for full and half marathon, and for the sum of these distances.</sub>

## Animated heatmap
![image](https://github.com/user-attachments/assets/65b3fbeb-0d56-4023-ba01-44e63a08fea0)
<sub>Screenshot from an animated heatmap for full distance.</sub>

## Animated heatmap half and full marathon combined
Number of runners in the simulation is changed to 10% of actual starts to limit the file size. With all runners a >350 Mb html file is created. That runs remarkable smooth on a browser but adds no value to the visualization.
![image](https://github.com/user-attachments/assets/fe1af19e-4ab1-4f4e-a8a3-887d0a762ef6)
<sub>Screenshot from an animated heatmap for both distances</sub>

# Reference marathon
As 260 finishers per minute seems quite a lot to me I made a reference (as suggested by @CanCakiroglu) for a previous marathon in Eindhoven. In 2023 the start for the full marathon was at 10:00 and the half started at 14:00 in the afternoon. I don't exactly know the number of runners for that edition but I used the same numbers as for the 2024 edition. Below graph shows the finishers over time. In the steepest part the number of runners crossing the finishline is **approximately 145 per minute**. Significantly lower that the predicted number for the 2024 edition.

<img src="https://github.com/user-attachments/assets/1eb5fd93-c4e7-48e0-98a8-33b3bc8e909b" height="400">

<sub>Number of finishers over time for the start schedule as used in 2023.</sub>

# Comparison
I order to compare the number of finishers over time the growth rate, maximum groth rate, and Full Wifhth at Half Maximum (FWHM) was calcualted. The growth rate essentially tells how fast runners are finishing at any given point in time. The peak growth rate shows the maximum at which runners are crossing the finish line. FWHM shows the time window over which the majority of the runners are finishing, helping race organizers understand congestion patterns at the finish line.

Below graphs show this information for a reference marathon where the half marathon starts 4 hours (240 minutes) after the full marathon. In the 2024 marathon the start between full and half is 90 minutes. 
For both editions calculation was done with 6000 full marathanon runners in a 10 minute start wave, and 17500 half marathon runners in 5 start waves, every 15 minutes.

| 2024 Marathon | Reference Marathon |
| --- | --- |
| ![image](https://github.com/user-attachments/assets/204ef063-8755-4bee-b92e-36fd8d5c38d7) | ![image](https://github.com/user-attachments/assets/3902ace9-9e1b-477c-a10b-63c2e361e877) |

 <sub>Note that the y-axis of both reference and 2024 marathon are not the same</sub>

# File description
Several files are located in the source directory. Output of graphs and animation (HTML) are located in th images directory.

Function of files in source:
| File name | Description |
| --- | --- |
|finishers_over_time_analysis.py | The graphs used for comparing effect on finishers over time of different start times of full and half.|
|half_and_full_finishers_over_time.py | Creates animation of a moving histogram for full and half marathon, together with individual number of finishers over tima and combined number over time|
|pace_waves_finishers_over_time_full.py | Animation of moving histogram with finishers over time for full marathon. This is a subset of half_and_full_finishers_over_time.py |
|pace_waves_finishers_over_time_half.py | Animation of moving histogram with finishers over time for half marathon. This is a subset of half_and_full_finishers_over_time.py |
|reference_half_and_full_finishers_over_time.py | almost identical to half_and_full_finishers_over_time.py but with marathon parameters for reference marathon, i.e. longer time between starts |
|runners_heatmap_animated_combined.py | Animated HTML heatmap of 2024 Marathon Eindhoven with both half and full and correct start times. Number of runners is 10% of actual starts because the size of the resulting file would be too large. This does not run smooth on older machines. Does not matter for visualisation |
|runners_heatmap_animated_full.py | Animated HTML heatmap of 2024 Marathon Eindhoven, full distance | 
|runners_heatmap_animated_half.py | Animated HTML heatmap of 2024 Marathon Eindhoven, half distance |


As you see, there is no file with standard parameters like number of runners or some functions. This could be a future improvement.

# Getting started
Why is this at the end you may ask? Well, that seems a nice place.

Run ```pip install -r requirements.txt``` to retrieve the packages used in the simulation.

R 4.3.3. was used with lubridate_1.9.3 and fitdistrplus_1.2-1 for determining the distribution, the mean pace, and the standard deviation.





