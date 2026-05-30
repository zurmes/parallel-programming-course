import numpy as np
import os

def read_matrix(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File {filename} not found.")
    with open(filename, "r") as f:
        size = int(f.readline().strip())
        data = np.fromfile(f, sep=" ")
        return data.reshape((size, size))

def main():
    try:
        A = read_matrix("matrixA.txt")
        B = read_matrix("matrixB.txt")
        C_cpp = read_matrix("result.txt")
        
        C_py = A @ B
        
        if np.allclose(C_cpp, C_py, rtol=1e-3, atol=1e-3):
            print("Verification PASSED: GPU results match NumPy!")
        else:
            print("Verification FAILED: Results differ!")
            diff = np.abs(C_cpp - C_py)
            print(f"Max absolute difference: {np.max(diff)}")
    except Exception as e:
        print(f"Error during verification: {e}")

if __name__ == "__main__":
    main()