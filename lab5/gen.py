import numpy as np
import sys

def create_files(size):
    for name in ['matrixA.txt', 'matrixB.txt']:
        matrix = np.random.uniform(0, 10, (size, size)).astype(np.float32)
        with open(name, 'w') as f:
            f.write(f"{size}\n")
            np.savetxt(f, matrix, fmt='%.2f')
    print(f"Matrices {size}x{size} created.")

if __name__ == "__main__":
    create_files(int(sys.argv[1]) if len(sys.argv) > 1 else 500)