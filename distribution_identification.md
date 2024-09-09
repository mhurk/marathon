# Data distribution
  
Which distribution of the data sould we use for generating random data?

Based on the chiptime from the marathon in Eindhoven in 2017 (for this marathon the data was easily downloaded without the need for a scraper or other tricks) the following results were found:

Goodness-of-fit statistics (Lower values generally suggest a better fit). 
|   |                                 Weibull   |   gamma | lognormal |  normal|
| --- | --- | --- | --- | --- |
|Kolmogorov-Smirnov statistic | 0.07392903 | 0.02604989 | 0.0331185 | 0.04102891 |
|Cramer-von Mises statistic | 2.83313761 | 0.25859331 | 0.5181630 | 0.40188463 |
|Anderson-Darling statistic | 18.44509324 | 1.56169558 | 3.1752235 | 2.26093465 |


Goodness-of-fit criteria

|  | Weibull | gamma | lognormal | normal |
| --- | --- | --- | --- | --- |
|Akaike's Information Criterion | 21517.23 | 21309.33 |  21333.51 | 21318.15 |
|Bayesian Information Criterion | 21528.57 | 21320.67 |  21344.85 | 21329.49 |

This means that the gamma distribution has the best fit to this data (chiptime). The normal distribution is close to this and could also be used. Lognormal moderate and Weibull is the worst fit for this data.

Visually it looks like this, on the x-axis the chiptime in minutes is given.
![image](https://github.com/user-attachments/assets/04d2236d-bbab-4050-847f-25f3b898e15e)



## Mean pace and variation

From the same dataset the mean pace (again, chiptime) and standard deviation is calculated.

- mean: 229.29 minutes (03:49:17)
- standard deviation: 35.21 minutes (00:35:12)
