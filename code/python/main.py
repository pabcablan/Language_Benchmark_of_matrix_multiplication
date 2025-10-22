import sys

from code.python.benchmarking.benchmarking import MatrixMultiplicationBenchmark

if __name__ == "__main__":
    matrix_sizes = [64, 128, 256, 512]
    block_sizes = [8, 16, 32, 64]
    num_runs = 3

    benchmark = MatrixMultiplicationBenchmark(matrix_sizes, block_sizes, num_runs, sys.argv[1])

    print("Starting matrix multiplication benchmarks...")
    benchmark.run_all_benchmarks()
    print("Done")

    print("\nGenerating comparison plots...")
    benchmark.plot_results()
    print("Done")

    print("\nSaving results to CSV...")
    benchmark.save_results_to_csv()
    print("Benchmarking completed!")