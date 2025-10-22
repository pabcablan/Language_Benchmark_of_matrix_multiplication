package com.pabcablan.matrix;
import java.util.Random;

public class BasicMatrixMultiplier  {
    private final Random random;

    public BasicMatrixMultiplier () {
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


    public double[][] multiply(double[][] firstMatrix, double[][] secondMatrix) {
        int size = firstMatrix.length;
        double[][] resultMatrix = new double[size][size];

        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                for (int k = 0; k < size; k++) {
                    resultMatrix[i][j] += firstMatrix[i][k] * secondMatrix[k][j];
                }
            }
        }
        return resultMatrix;
    }
}