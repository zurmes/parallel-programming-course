import numpy as np
import sys

def generate_matrices(size):
    A = np.random.uniform(-10, 10, (size, size))
    B = np.random.uniform(-10, 10, (size, size))
    
    with open("matrixA.txt", "w") as f:
        f.write(f"{size}\n")
        np.savetxt(f, A, fmt="%.6f")
        
    with open("matrixB.txt", "w") as f:
        f.write(f"{size}\n")
        np.savetxt(f, B, fmt="%.6f")
        
    print(f"Matrices of size {size}x{size} generated successfully.")

if __name__ == "__main__":
    size = int(sys.argv[1]) if len(sys.argv) > 1 else 1024
    generate_matrices(size)