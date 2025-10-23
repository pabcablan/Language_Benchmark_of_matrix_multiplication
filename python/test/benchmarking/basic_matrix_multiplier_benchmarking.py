import sys
import time
import csv
import os
import psutil
from src.matrix.basic_matrix_multiplier import BasicMatrixMultiplier

def get_process_memory_mb():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)

def run_benchmarks(sizes, runs, csv_path):
    times = {}
    real_memories = {}

    with open(csv_path, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["MatrixSize", "Run", "TimeSeconds", "RealMemoryMB"])

        for size in sizes:
            times[size] = []
            real_memories[size] = []
            for run in range(1, runs+1):

                multiplier = BasicMatrixMultiplier()
                A, B = multiplier.generate_matrices(size)

                mem_before = get_process_memory_mb()
                start = time.time()
                result = multiplier.multiply(A, B)
                end = time.time()
                mem_after = get_process_memory_mb()

                time_seconds = round(end - start, 5)
                real_memory_mb = round(max(mem_before, mem_after), 5)

                times[size].append(time_seconds)
                real_memories[size].append(real_memory_mb)

                writer.writerow([size, run, time_seconds, real_memory_mb])
            avg_mem = round(sum(real_memories[size])/len(real_memories[size]), 5)

def print_average_results(sizes, times, real_memories):
    print("\n===== AVERAGE RESULTS =====")
    print("{:<10} {:<15} {:<25}".format("Size", "Avg Time (s)", "Avg Real Mem (MB)"))
    for size in sizes:
        avg_time = round(sum(times[size]) / len(times[size]), 5)
        avg_real_mem = round(sum(real_memories[size]) / len(real_memories[size]), 5)
        print("{:<10} {:<15.5f} {:<25.5f}".format(size, avg_time, avg_real_mem))

if __name__ == "__main__":
    sizes = [64, 128, 256, 512, 1024]
    runs = 5
    output_directory = sys.argv[1]
    os.makedirs(output_directory, exist_ok=True)
    csv_path = os.path.join(output_directory, "summary_python.csv")

    print("Benchmarking in progress...")

    run_benchmarks(sizes, runs, csv_path)

    times = {size: [] for size in sizes}
    real_memories = {size: [] for size in sizes}
    with open(csv_path, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            size = int(row["MatrixSize"])
            times[size].append(float(row["TimeSeconds"]))
            real_memories[size].append(float(row["RealMemoryMB"]))

    print_average_results(sizes, times, real_memories)

    print("\nBenchmark finished. Results saved at:", csv_path)
