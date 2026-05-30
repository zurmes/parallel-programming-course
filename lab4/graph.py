import matplotlib.pyplot as plt
import numpy as np

sizes = [200, 400, 800, 1200, 1600, 2000]

time_8x8 = [0.29, 1.42, 9.85, 32.14, 73.50, 142.10]
time_16x16 = [0.22, 1.15, 7.92, 25.48, 58.20, 112.50]
time_32x32 = [0.25, 1.28, 8.44, 27.12, 61.40, 119.80]

plt.figure(figsize=(10, 6))

plt.plot(sizes, time_8x8, marker='o', label='Block 8x8', color='#e74c3c', linewidth=2)
plt.plot(sizes, time_16x16, marker='s', label='Block 16x16', color='#2ecc71', linewidth=2)
plt.plot(sizes, time_32x32, marker='^', label='Block 32x32', color='#3498db', linewidth=2)

plt.title('CUDA Shared Memory Kernel Performance Comparison (RTX 3050 Laptop)', fontsize=14)
plt.xlabel('Matrix Dimension (N x N)', fontsize=12)
plt.ylabel('Execution Time (ms)', fontsize=12)

plt.xticks(sizes)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()

plt.savefig('cuda_graph.png', dpi=300)