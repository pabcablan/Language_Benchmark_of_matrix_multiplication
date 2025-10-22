import random
import numpy as np


class MatrixMultiplier:

    def __init__(self, default_block_size=32):
        self.default_block_size = default_block_size

    def generate_matrices(self, n):
        A = [[random.random() for _ in range(n)] for _ in range(n)]
        B = [[random.random() for _ in range(n)] for _ in range(n)]
        return A, B

    def standard(self, A, B):
        n = len(A)
        C = [[0 for _ in range(n)] for _ in range(n)]

        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def row_oriented(self, A, B):
        n = len(A)
        C = [[0 for _ in range(n)] for _ in range(n)]

        for i in range(n):
            for k in range(n):
                for j in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def tiled(self, A, B, block_size=None):
        if block_size is None:
            block_size = self.default_block_size

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
                            a_ik = A[i][k]
                            for j in range(j_block, j_limit):
                                C[i][j] += a_ik * B[k][j]
        return C

    def numpy(self, A, B):
        A_np = np.array(A)
        B_np = np.array(B)
        C_np = np.matmul(A_np, B_np)
        return C_np.tolist()
