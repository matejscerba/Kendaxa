#!/usr/bin/python3

from main import Graph

import time
import matplotlib.pyplot as plt
import numpy as np

times = []
for i in range(1, 11):
    curr_times = []
    for _ in range(30):
        start = time.time()
        file = "data_cases/case_{:02d}.in".format(i)
        graph = Graph(file)
        print(f"{file}: {graph.count_paths()}")
        end = time.time()
        curr_times.append(end - start)
    times.append([graph._M + 1 ,sum(curr_times) / len(curr_times)])

times = np.array(times)
x = times[:, 0]
y = times[:, 1]

plt.plot(x, y)
plt.xlabel("Number of nodes")
plt.ylabel("Algorithm duration [s]")
plt.savefig("benchmarks.pdf", dpi=500, transparent=True)
    