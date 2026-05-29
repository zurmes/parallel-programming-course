import matplotlib.pyplot as plt
import numpy as np

sizes = [200, 400, 600, 800, 1200, 1600, 2000]
times = [0.0053402, 0.0488091, 0.162983, 0.404315, 1.6675, 7.95192, 10.2344]

plt.figure(figsize=(10, 6))
plt.plot(sizes, times, marker='o', color='#2c3e50', linewidth=2, label='Sequential Algorithm')

plt.title('Execution Time vs Matrix Dimension (Lab 1)', fontsize=14, fontweight='bold')
plt.xlabel('Matrix Dimension (N x N)', fontsize=12)
plt.ylabel('Time (seconds)', fontsize=12)
plt.xticks(np.arange(0, 2100, 200))

plt.grid(True, linestyle='--', alpha=0.7)
plt.xlim(0, 2100)
plt.ylim(-0.5, max(times) + 1.5)
plt.legend()

# Сохраняем график в файл graph.png
plt.savefig('graph.png', dpi=300, bbox_inches='tight')
print("Graph saved successfully as graph.png")