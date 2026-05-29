import matplotlib.pyplot as plt
import numpy as np

sizes = [360, 720, 1080, 1440, 1800]
procs = [1, 2, 4, 6, 12]

time_data = [
    [0.031888, 0.017229, 0.009108, 0.009909, 0.008427],
    [0.257717, 0.134862, 0.082728, 0.068928, 0.077805],
    [0.885072, 0.513230, 0.322234, 0.265307, 0.286237],
    [3.038790, 1.613340, 0.937441, 0.826099, 0.993092],
    [6.263950, 3.236910, 1.888730, 1.761560, 1.721450]
]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

for i, size in enumerate(sizes):
    ax1.plot(procs, time_data[i], marker='o', label=f'Size {size}')

ax1.set_title('Execution Time vs MPI Processes')
ax1.set_xlabel('Number of Processes')
ax1.set_ylabel('Time (seconds)')
ax1.set_xticks(procs)
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.legend()

for i, size in enumerate(sizes):
    t1 = time_data[i][0]
    speedup = [t1 / tp for tp in time_data[i]]
    ax2.plot(procs, speedup, marker='s', label=f'Size {size}')

ax2.plot(procs, procs, color='black', linestyle='--', alpha=0.3, label='Ideal Speedup')
ax2.set_title('Speedup vs MPI Processes')
ax2.set_xlabel('Number of Processes')
ax2.set_ylabel('S = T1 / Tp')
ax2.set_xticks(procs)
ax2.grid(True, linestyle='--', alpha=0.7)
ax2.legend()

plt.tight_layout()
plt.savefig('mpi_graph.png', dpi=300)