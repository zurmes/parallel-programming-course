import subprocess
import re
import sys
import os

sizes = [360, 720, 1080, 1440, 1800]
proc_list = [1, 2, 4, 6, 12]

results = {size: {} for size in sizes}

print("=== Starting MPI automated benchmarks ===")

for size in sizes:
    print(f"\n--- Generating matrices for size {size}x{size} ---")
    subprocess.run([sys.executable, "gen.py", str(size)], check=True)
    
    for procs in proc_list:
        print(f"Running size {size} on {procs} MPI processes...", end="", flush=True)
        
        process = subprocess.Popen(["mpiexec", "-n", str(procs), "main.exe"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        
        match = re.search(r"Time:\s*([\d\.]+)\s*seconds", stdout)
        if match:
            time_val = float(match.group(1))
            results[size][procs] = time_val
            print(f" Success! Time: {time_val:.6f}s")
        else:
            print(" Error parsing result!")
            print(stdout, stderr)

print("\n=== Benchmark Completed! ===")

header = "| Size N | " + " | ".join(f"{p} Procs" for p in proc_list) + " |"
separator = "| :--- | " + " | ".join(":---:" for _ in proc_list) + " |"
print(header)
print(separator)

for size in sizes:
    row = f"| **{size}** | " + " | ".join(f"{results[size][p]:.6f}" for p in proc_list) + " |"
    print(row)

with open("benchmark_results.txt", "w", encoding="utf-8") as f:
    f.write(header + "\n")
    f.write(separator + "\n")
    for size in sizes:
        row = f"| **{size}** | " + " | ".join(f"{results[size][p]:.6f}" for p in proc_list) + " |"
        f.write(row + "\n")