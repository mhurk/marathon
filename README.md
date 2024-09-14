# Marathon Simulation
Simulation of distribution of runners on a marathon course.

- Uses startwaves, total number of runners equally distributed over waves.
- Normal distribution or gamma distribution is okay to use, based on the 2017 marathon data. (see [distribution_identification.md](https://github.com/mhurk/marathon/blob/main/distribution_identification.md))
- Assumes pace distribution is the same for all start waves. This is not fully correct, faster runners will start in earlier waves.
- Assumes all runners starts simultaneously, per wave. 
- Assumes constant pace during the entire race.
- [x] Generate animation of distribution over runners over the course (moving histogram)
- [x] Show number of runners crossing the finish line as function of time.
- [x] Animated heatmap of runners on the course (this is really cool!)
- [ ] Combine half and full marathon (seperate graphs with match x-asis and a combined graph. Depending on course overlap).
    - Courses meet at around 39.25 km for full and 18.35 for the half marathon.
      - For ASML Marathon Eindhoven 2024:
      - Half marathon has 5 start waves at 11:30, 11:45, 12:00, 12:15 en 12:30 (total 17500 runners). Expected around 250 per minute. Modelleing can be either 1 big wave with 250/minute or 5 waves with 3500 runners each.
      - Full marathon has 1 start wave which lasts around 10 minutes, starting at 10:00 (10:00 - 10:10), 6000 runners.
- [ ] Wave starts not on one moment but n per second (probably does not matter a lot, central limit theorem?).
- [ ] Correct number of runners per wave (currently the same).
- [ ] _Minor improvement_: Correct pace distribution over time (currently assumes constant pace). Based on old data? There is a list of all times with pace per segment of a few km.

## Animation / moving histogram (screenshot from full marathon):
![image](https://github.com/user-attachments/assets/5e833fae-7ec2-4cf4-b7b3-4a5f78844f13)

## Runners over time (half marathon):
![image](https://github.com/user-attachments/assets/ad15bbc5-cbda-4503-8c41-340ea5fefd1e)


## Screenshot from animated heatmap:
![image](https://github.com/user-attachments/assets/65b3fbeb-0d56-4023-ba01-44e63a08fea0)


