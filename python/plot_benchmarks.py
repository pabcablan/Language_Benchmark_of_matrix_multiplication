import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

def read_summary(path):
    df = pd.read_csv(path)
    grouped = df.groupby("MatrixSize").agg({
        "TimeSeconds": "mean",
        "RealMemoryMB": "mean"
    }).reset_index()
    return grouped

def main():
    if len(sys.argv) > 1:
        folder = sys.argv[1]
    else:
        folder = "data/output"
        print(f"Usando ruta por defecto: {folder}")

    files = {
        "C": os.path.join(folder, "summary_c.csv"),
        "Python": os.path.join(folder, "summary_python.csv"),
        "Java": os.path.join(folder, "summary_java.csv"),
    }

    results = {}
    for lang, file in files.items():
        if not os.path.exists(file):
            print(f"Archivo no encontrado: {file}")
            return
        results[lang] = read_summary(file)

    plt.figure(figsize=(10,6))
    for lang, df in results.items():
        plt.plot(df["MatrixSize"], df["TimeSeconds"], marker="o", label=lang)
    plt.xlabel("Matrix Size (n x n)")
    plt.ylabel("Average Time (seconds)")
    plt.title("Matrix Multiplication Benchmark: Execution Time")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10,6))
    for lang, df in results.items():
        plt.plot(df["MatrixSize"], df["RealMemoryMB"], marker="o", label=lang)
    plt.xlabel("Matrix Size (n x n)")
    plt.ylabel("Average Real Memory (MB)")
    plt.title("Matrix Multiplication Benchmark: Memory Usage")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()