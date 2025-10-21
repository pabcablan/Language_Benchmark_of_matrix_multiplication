import random
from time import *

n = 1024


def multiplication_matrix_standard():
    A = [[random.random() for _ in range(n)] for _ in range(n)]
    B = [[random.random() for _ in range(n)] for _ in range(n)]
    C = [[0 for _ in range(n)] for _ in range(n)]
    start = time()

    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]

    end = time()

    print("%.6f" % (end - start))


def multiplication_matrix_rows():
    A = [[random.random() for _ in range(n)] for _ in range(n)]
    B = [[random.random() for _ in range(n)] for _ in range(n)]
    C = [[0 for _ in range(n)] for _ in range(n)]
    start = time()

    for i in range(n):
        for k in range(n):
            for j in range(n):
                C[i][j] += A[i][k] * B[k][j]

    end = time()

    print("%.6f" % (end - start))



def multiplication_matrix_tiled(block_size=256):
    A = [[random.random() for _ in range(n)] for _ in range(n)]
    B = [[random.random() for _ in range(n)] for _ in range(n)]
    C = [[0 for _ in range(n)] for _ in range(n)]

    start = time()
    for i_blocks in range(0, n, block_size):
        for k_blocks in range(0, n, block_size):
            for j_blocks in range(0, n, block_size):
                for i in range(i_blocks, min(i_blocks+block_size, n)):
                    for j in range(j_blocks, min(j_blocks + block_size, n)):
                        for k in range(k_blocks, min(k_blocks + block_size, n)):
                            C[i][j] += A[i][k] * B[k][j]

    end = time()
    print("%.6f" % (end - start))






if __name__ == "__main__":
    print("--- Standard Matrix Multiplication ---")
    multiplication_matrix_standard()
    print("\n--- Rows Matrix Multiplication ---")
    multiplication_matrix_rows()
    print("\n--- Tiled Matrix Multiplication ---")
    multiplication_matrix_tiled()





