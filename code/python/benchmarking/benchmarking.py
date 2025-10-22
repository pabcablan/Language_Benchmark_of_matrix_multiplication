import statistics
import time
from code.python.matrix.matrix_multiplication import MatrixMultiplier
import matplotlib.pyplot as plt
import os
import csv


class MatrixMultiplicationBenchmark:
    def __init__(self, matrix_sizes, block_sizes, num_runs, output_dir="benchmark_results"):
        self.matrix_sizes = matrix_sizes
        self.block_sizes = block_sizes
        self.num_runs = num_runs
        self.output_dir = output_dir
        self.results = {}
        self.mm = MatrixMultiplier()
        os.makedirs(output_dir, exist_ok=True)

    def run_algorithm(self, algorithm, A, B, block_size=None):
        start_time = time.time()

        if block_size is not None and algorithm.__name__ == 'matrix_multiply_tiled':
            algorithm(A, B, block_size)
        else:
            algorithm(A, B)

        end_time = time.time()
        return end_time - start_time

    def benchmark_algorithm(self, algorithm, size, block_size=None):
        times = []

        A, B = self.mm.generate_matrices(size)

        for run in range(self.num_runs):
            time_taken = self.run_algorithm(algorithm, A, B, block_size)
            times.append(time_taken)

        stats = {
            "min": min(times),
            "max": max(times),
            "mean": statistics.mean(times),
            "median": statistics.median(times),
            "stdev": statistics.stdev(times)
        }

        return stats

    def run_all_benchmarks(self):
        algorithms = {
            "standard": (self.mm.standard, None),
            "row_oriented": (self.mm.row_oriented, None),
            "numpy": (self.mm.numpy, None)
        }

        for block_size in self.block_sizes:
            algorithms[f"tiled_block{block_size}"] = (self.mm.tiled, block_size)

        for size in self.matrix_sizes:
            for algorithm_name, (algorithm_func, block_size) in algorithms.items():

                if algorithm_name not in self.results:
                    self.results[algorithm_name] = {}

                self.results[algorithm_name][size] = self.benchmark_algorithm(
                    algorithm_func, size, block_size)

        return self.results

    def plot_results(self):
        plt.figure(figsize=(12, 8))

        x = self.matrix_sizes
        for algorithm, size_data in self.results.items():
            y = [size_data.get(size, {}).get("mean", 0) for size in x]
            plt.plot(x, y, marker='o', label=algorithm)

        plt.xlabel('Matrix Size (n×n)')
        plt.ylabel('Average Time (seconds)')
        plt.title('Comparison of Matrix Multiplication Algorithms')
        plt.grid(True)
        plt.legend()
        plt.show()

    def save_results_to_csv(self):
        summary_file = os.path.join(self.output_dir, "summary_python.csv")

        with open(summary_file, 'w', newline='') as csvfile:
            fieldnames = ['Algorithm', 'Matrix Size', 'Min Time', 'Max Time', 'Mean Time', 'Median Time', 'Std Dev']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for algorithm, size_data in self.results.items():
                for size, stats in size_data.items():
                    writer.writerow({
                        'Algorithm': algorithm,
                        'Matrix Size': size,
                        'Min Time': stats['min'],
                        'Max Time': stats['max'],
                        'Mean Time': stats['mean'],
                        'Median Time': stats['median'],
                        'Std Dev': stats['stdev']
                    })

        print(f"Results saved to {summary_file}")
