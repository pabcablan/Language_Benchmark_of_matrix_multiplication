#ifndef MATRIX_MULTIPLIER_H
#define MATRIX_MULTIPLIER_H

double **allocate_matrix(int n);
void free_matrix(double **matrix, int n);
void generate_matrices(double **A, double **B, int n);
void multiply(double **A, double **B, double **C, int n);

#endif