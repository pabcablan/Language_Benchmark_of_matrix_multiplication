#include <stdio.h>
#include <stdlib.h>
#include <time.h>

double **allocate_matrix(int n) {
    double **matrix = malloc(n * sizeof(double *));
    for (int i = 0; i < n; ++i) {
        matrix[i] = malloc(n * sizeof(double));
    }
    return matrix;
}

void free_matrix(double **matrix, int n) {
    for (int i = 0; i < n; ++i) {
        free(matrix[i]);
    }
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

void multiply(double **first_matrix, double **second_matrix, double **result_matrix, int n) {
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            result_matrix[i][j] = 0.0;
            for (int k = 0; k < n; ++k) {
                result_matrix[i][j] += first_matrix[i][k] * second_matrix[k][j];
            }
        }
    }
}