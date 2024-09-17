# Marathon Simulation
Simulation of distribution of runners on a marathon course.

- Uses start waves, total number of runners equally distributed over waves.
- Normal distribution or gamma distribution is okay to use, based on the 2017 marathon data. (see [distribution_identification.md](https://github.com/mhurk/marathon/blob/main/distribution_identification.md))
- Assumes pace distribution is the same for all start waves and distances. This is not fully correct, faster runners will start mainly in earlier waves.
- Assumes all runners starts simultaneously, per wave. 
- Assumes constant pace during the entire race.
- Generate animation of distribution over runners over the course (moving histogram)
- Show number of runners crossing the finish line as function of time.
- Animated heatmap of runners on the course (I think this is really cool!)
- Combine half and full marathon (seperate graphs with match x-asis and a combined graph. Depending on course overlap).
    - Courses meet at around 39.25 km for full and 18.35 for the half marathon.
      - For ASML Marathon Eindhoven 2024:
      - Half marathon has 5 start waves at 11:30, 11:45, 12:00, 12:15 en 12:30 (total 17500 runners). Expected around 250 per minute. Modelleing can be either 1 big wave with 250/minute or 5 waves with 3500 runners each.
      - Full marathon has 1 start wave which lasts around 10 minutes, starting at 10:00 (10:00 - 10:10), 6000 runners.
- [ ] Overlapping sections in heatmap don't show up brighter. That could be improved. Currently there is no interaction between the two heatmaps, jus plotted together on the map.
- [ ] Wave starts not on one moment but n per second (probably does not matter a lot, central limit theorem?).
- [x] Correct number of runners per wave -> distributed evenly.
- [ ] _Minor improvement_: Correct pace distribution over time (currently assumes constant pace). Based on old data? There is a list of all times with pace per segment of a few km.

I estimate the number of finishers at __around 260 per minute__ during the hour after 200 minutes from the start of the full marathon. So for a start at 10:00 this translate to 260 runners per minute from 13:20 - 14:20.

## Moving histogram:
![image](https://github.com/user-attachments/assets/ff8ece7f-6263-408d-9b90-94c2495067ac)

## Screenshot from animated heatmap:
![image](https://github.com/user-attachments/assets/65b3fbeb-0d56-4023-ba01-44e63a08fea0)

## Screenshot from animated heatmap half and full marathon combined:
Number of runners in the simulation is changed to 10% of actual starts to limit the file size. With all runners a >350 Mb html file is created. That runs remarkable smooth on a browser but adds no value to the visualization.
![image](https://github.com/user-attachments/assets/fe1af19e-4ab1-4f4e-a8a3-887d0a762ef6)
