# Marathon
Simulation of distribution of runners on a marathon course.

_What it does and does not_
- Uses startwaves, total number of runners equally distributed over waves.
- ~~Uses a normal distribution for pace, this is not correct as it is usually a bit skewed toward faster runners. Real data is needed.~~
- Normal distribution or gamma distribution is okay to use, based on the 2017 marathon data. (see [distribution_identification.md](https://github.com/mhurk/marathon/blob/main/distribution_identification.md))
- Assumes pace distribution is the same for all start waves. This is not correct, faster runners will start in earlier waves.
- Assumes all runners starts simultaneously, per wave. 
- Assumnes constant pace during the entire race.
- Generates animation of distribution over runners over the course
 
_Future improvement / to-do list_
- combine half and full marathon (same graph or seperate? Depending on course overlap). Where are the overlap areas for Eindhoven 2024?
- Show number of runners crossing the finish line as function of time.
- Wave starts not on one moment but n per secnond (does this matter a lot?).
- Correct number of runners per wave (currently the same).
- Correct distribution of end times (mean pace).
- Correct pace distribution over time (currently assumes constant pace). Based on old data? There is a list of all times with pace per segment of a few km.
- Create a heatmap of a course, based on gpx and number of runners on a location.

Screenshot from animation:
![image](https://github.com/user-attachments/assets/a6059428-960b-4ee8-9cd6-e2f3ceae6930)




