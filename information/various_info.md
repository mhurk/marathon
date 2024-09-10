De parcours komen bij km 39.25 km van de hele bij elkaar. Dus op ongeveer 18.35 km van de halve. 

Two plots combined (from https://discuss.python.org/t/how-to-combine-2-graphs-in-one-figure/15252/3)

more on subplots: https://www.activestate.com/resources/quick-reads/how-to-display-a-plot-in-python/
```
import matplotlib.pyplot as plt
import pandas as pd

# Create some example data similar to yours
df = pd.DataFrame({"year": [1, 2, 3, 4, 5], "TAVG": [20, 25, 23, 27, 30]})
df["MA"] = df["TAVG"].rolling(window=2).mean()

# Create a common figure for both with 2 columns and 1 row of subplots
figure, axes = plt.subplots(2, 1, figsize=(10, 7))

# Create each subplot on the specified axes
df.plot(x="year", y="TAVG", kind="line", ax=axes[0])
df.plot(x="year", y="MA", kind="bar", ax=axes[1])

plt.show()
```


