#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "../../matrix/matrix_multiplier.c"

#define DELTA 1e-10

int assert_matrix_almost_equal(double **expected, double **actual, int n, double delta) {
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
            if (fabs(expected[i][j] - actual[i][j]) > delta)
                return 0;
    return 1;
}

void test_multiply() {
    int n = 2;
    double **A = allocate_matrix(n);
    double **B = allocate_matrix(n);
    double **expected = allocate_matrix(n);
    double **result = allocate_matrix(n);

    A[0][0] = 1; A[0][1] = 2;
    A[1][0] = 3; A[1][1] = 4;
    B[0][0] = 5; B[0][1] = 6;
    B[1][0] = 7; B[1][1] = 8;
    expected[0][0] = 19; expected[0][1] = 22;
    expected[1][0] = 43; expected[1][1] = 50;

    multiply(A, B, result, n);

    if (assert_matrix_almost_equal(expected, result, n, DELTA))
        printf("test_multiply PASSED\n");
    else
        printf("test_multiply FAILED\n");

    free_matrix(A, n); free_matrix(B, n); free_matrix(expected, n); free_matrix(result, n);
}

void test_generate_matrices_shape() {
    int n = 5;
    double **A = allocate_matrix(n);
    double **B = allocate_matrix(n);

    generate_matrices(A, B, n);

    int passed = 1;
    if (A && B) {
        for (int i = 0; i < n; ++i) {
            if (!A[i] || !B[i]) {
                passed = 0;
                break;
            }
        }
    } else {
        passed = 0;
    }

    if (passed)
        printf("test_generate_matrices_shape PASSED\n");
    else
        printf("test_generate_matrices_shape FAILED\n");

    free_matrix(A, n); free_matrix(B, n);
}

void test_multiply_with_random_matrices() {
    int n = 3;
    double **A = allocate_matrix(n);
    double **B = allocate_matrix(n);
    double **result = allocate_matrix(n);

    generate_matrices(A, B, n);
    multiply(A, B, result, n);

    int correct_shape = (A && B && result);
    for (int i = 0; i < n; ++i) {
        if (!A[i] || !B[i] || !result[i]) {
            correct_shape = 0;
            break;
        }
    }

    if (correct_shape)
        printf("test_multiply_with_random_matrices PASSED\n");
    else
        printf("test_multiply_with_random_matrices FAILED\n");

    free_matrix(A, n); free_matrix(B, n); free_matrix(result, n);
}

int main() {
    test_multiply();
    test_generate_matrices_shape();
    test_multiply_with_random_matrices();
    return 0;
}