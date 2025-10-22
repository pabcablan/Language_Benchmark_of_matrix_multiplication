package com.pabcablan.matrix;
import java.util.Random;

public class MatrixMultiplication {
    private final int defaultBlockSize;
    private final Random random;


    public MatrixMultiplication(int defaultBlockSize) {
        this.defaultBlockSize = defaultBlockSize;
        this.random = new Random();
    }


    public double[][][] generateMatrices(int n) {
        double[][] A = new double[n][n];
        double[][] B = new double[n][n];

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                A[i][j] = random.nextDouble();
                B[i][j] = random.nextDouble();
            }
        }

        return new double[][][] {A, B};
    }


    public double[][] standard(double[][] A, double[][] B) {
        int n = A.length;
        double[][] C = new double[n][n];

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                for (int k = 0; k < n; k++) {
                    C[i][j] += A[i][k] * B[k][j];
                }
            }
        }

        return C;
    }


    public double[][] rowOriented(double[][] A, double[][] B) {
        int n = A.length;
        double[][] C = new double[n][n];

        for (int i = 0; i < n; i++) {
            for (int k = 0; k < n; k++) {
                for (int j = 0; j < n; j++) {
                    C[i][j] += A[i][k] * B[k][j];
                }
            }
        }

        return C;
    }


    public double[][] tiled(double[][] A, double[][] B, Integer blockSize) {
        if (blockSize == null) {
            blockSize = this.defaultBlockSize;
        }

        int n = A.length;
        double[][] C = new double[n][n];

        for (int iBlock = 0; iBlock < n; iBlock += blockSize) {
            for (int jBlock = 0; jBlock < n; jBlock += blockSize) {
                for (int kBlock = 0; kBlock < n; kBlock += blockSize) {

                    int iLimit = Math.min(iBlock + blockSize, n);
                    int jLimit = Math.min(jBlock + blockSize, n);
                    int kLimit = Math.min(kBlock + blockSize, n);

                    for (int i = iBlock; i < iLimit; i++) {
                        for (int k = kBlock; k < kLimit; k++) {
                            double aik = A[i][k];
                            for (int j = jBlock; j < jLimit; j++) {
                                C[i][j] += aik * B[k][j];
                            }
                        }
                    }
                }
            }
        }

        return C;
    }
}