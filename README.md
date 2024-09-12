# Marathon Simulation
Simulation of distribution of runners on a marathon course.

_What it does and does not_
- [x] Uses startwaves, total number of runners equally distributed over waves.
- [x] Normal distribution or gamma distribution is okay to use, based on the 2017 marathon data. (see [distribution_identification.md](https://github.com/mhurk/marathon/blob/main/distribution_identification.md))
- [x] Assumes pace distribution is the same for all start waves. This is not fully correct, faster runners will start in earlier waves.
- [x] Assumes all runners starts simultaneously, per wave. 
- [x] Assumnes constant pace during the entire race.
- [x] Generates animation of distribution over runners over the course
- [x] Show number of runners crossing the finish line as function of time.
- [x] Animated heatmap of runners on the course (this is really cool!)
- [ ] Combine half and full marathon (seperate graphs with match x-asis and a combined graph. Depending on course overlap).
    - Courses meet at around 39.25 km for full and 18.35 for the half marathon.
- [ ] Wave starts not on one moment but n per second (probably does not matter a lot, central limit theorem?).
- [ ] Correct number of runners per wave (currently the same).
- [ ] _Minor improvement_: Correct pace distribution over time (currently assumes constant pace). Based on old data? There is a list of all times with pace per segment of a few km.

Screenshot from animation:
![image](https://github.com/user-attachments/assets/a6059428-960b-4ee8-9cd6-e2f3ceae6930)

Screenshot from runners over time:
![image](https://github.com/user-attachments/assets/b4d1e4df-b8dc-48a1-8020-6c0b60c25d5a)

Screenshot from animated heatmap:
![image](https://github.com/user-attachments/assets/65b3fbeb-0d56-4023-ba01-44e63a08fea0)


