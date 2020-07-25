from generator import *

import matplotlib.pyplot as plt
import numpy as np

settings = read_settings('sample/settings.json')

print("generating")

sample = list(map(lambda a: a["average"], [generate(settings, (4, 6)) for _ in range(300)]))

print("generated")

x = list(range(len(sample)))
y = sample

nb = 0
for average in sample:
    if average >= 4 and average <= 6:
        nb += 1
        
print("Number inside the interval :", nb)
print("Number outside the interval:", 300-nb)
print("Frequency of inside the interval :", nb/300)

plt.scatter(x,y)      # probabilities store a series of float numbers
plt.ylabel("Average")
plt.xlabel("Rank")
plt.show()