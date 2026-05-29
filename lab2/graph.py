import matplotlib.pyplot as plt
import numpy as np

sizes = [400, 800, 1200, 1600, 2000]
threads = [1, 2, 4, 6, 12]

time_data = [
    [0.055992, 0.028390, 0.014729, 0.010495, 0.010596],
    [0.463130, 0.233293, 0.142750, 0.100375, 0.089942],
    [1.731300, 0.826179, 0.442307, 0.338236, 0.285856],
    [7.853540, 3.989410, 2.182210, 1.666090, 1.201120],
    [11.432300, 5.784520, 3.177770, 2.405380, 2.373570]
]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

for i, size in enumerate(sizes):
    ax1.plot(threads, time_data[i], marker='o', label=f'Size {size}')

ax1.set_title('Execution Time vs Threads')
ax1.set_xlabel('Number of Threads')
ax1.set_ylabel('Time (seconds)')
ax1.set_xticks(threads)
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.legend()

for i, size in enumerate(sizes):
    t1 = time_data[i][0]
    speedup = [t1 / tp for tp in time_data[i]]
    ax2.plot(threads, speedup, marker='s', label=f'Size {size}')

ax2.plot(threads, threads, color='black', linestyle='--', alpha=0.3, label='Ideal Speedup')
ax2.set_title('Speedup vs Threads')
ax2.set_xlabel('Number of Threads')
ax2.set_ylabel('S = T1 / Tp')
ax2.set_xticks(threads)
ax2.grid(True, linestyle='--', alpha=0.7)
ax2.legend()

plt.tight_layout()
plt.savefig('openmp_graph.png', dpi=300)