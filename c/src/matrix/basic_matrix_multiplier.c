#include "basic_matrix_multiplier.h"
#include <stdlib.h>

double **allocate_matrix(int n) {
    double **matrix = (double **)malloc(n * sizeof(double *));
    for (int i = 0; i < n; ++i)
        matrix[i] = (double *)malloc(n * sizeof(double));
    return matrix;
}

void free_matrix(double **matrix, int n) {
    for (int i = 0; i < n; ++i)
        free(matrix[i]);
    free(matrix);
}

void generate_matrices(double **A, double **B, int n) {
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            A[i][j] = (double)rand() / RAND_MAX;
            B[i][j] = (double)rand() / RAND_MAX;
        }
    }
}

void multiply(double **A, double **B, double **C, int n) {
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            C[i][j] = 0.0;
            for (int k = 0; k < n; ++k)
                C[i][j] += A[i][k] * B[k][j];
        }
    }
}