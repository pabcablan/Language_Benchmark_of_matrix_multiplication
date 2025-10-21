import random


def generate_matrices(n):
    A = [[random.random() for _ in range(n)] for _ in range(n)]
    B = [[random.random() for _ in range(n)] for _ in range(n)]
    return A, B


def matrix_multiply_standard(A, B):
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C


def matrix_multiply_row_oriented(A, B):
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for k in range(n):
            for j in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C


def matrix_multiply_tiled(A, B, block_size=32):
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]

    for i_block in range(0, n, block_size):
        for j_block in range(0, n, block_size):
            for k_block in range(0, n, block_size):

                i_limit = min(i_block + block_size, n)
                j_limit = min(j_block + block_size, n)
                k_limit = min(k_block + block_size, n)

                for i in range(i_block, i_limit):
                    for k in range(k_block, k_limit):
                        for j in range(j_block, j_limit):
                            C[i][j] += A[i][k] * B[k][j]
    return C
