package com.pabcablan.matrix;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class TestMatrixMultiplication {

    private double[][] A;
    private double[][] B;
    private double[][] expected;
    private MatrixMultiplication multiplier;

    @Before
    public void setUp() {
        A = new double[][] {{1, 2}, {3, 4}};
        B = new double[][] {{5, 6}, {7, 8}};
        expected = new double[][] {{19, 22}, {43, 50}};
        multiplier = new MatrixMultiplication();
    }

    @Test
    public void testStandardMultiplication() {
        double[][] result = multiplier.standard(A, B);
        assertMatrixEquals(expected, result, 1e-10);
    }

    @Test
    public void testRowOrientedMultiplication() {
        double[][] result = multiplier.rowOriented(A, B);
        assertMatrixEquals(expected, result, 1e-10);
    }

    @Test
    public void testTiledMultiplication() {
        int[] blockSizes = {1, 2, 4};

        for (int blockSize : blockSizes) {
            double[][] result = multiplier.tiled(A, B, blockSize);
            assertMatrixEquals(expected, result, 1e-10);
        }
    }

    @Test
    public void testAlgorithmsEquivalence() {
        int n = 8;
        double[][][] matrices = multiplier.generateMatrices(n);
        double[][] randomA = matrices[0];
        double[][] randomB = matrices[1];

        double[][] resultStandard = multiplier.standard(randomA, randomB);
        double[][] resultRow = multiplier.rowOriented(randomA, randomB);
        double[][] resultTiled = multiplier.tiled(randomA, randomB);

        assertMatrixEquals(resultStandard, resultRow, 1e-10);
        assertMatrixEquals(resultStandard, resultTiled, 1e-10);
    }

    private void assertMatrixEquals(double[][] expected, double[][] actual, double delta) {
        assertEquals("Matrices should have the same number of rows", expected.length, actual.length);
        for (int i = 0; i < expected.length; i++) {
            assertEquals("Row " + i + " should have the same length", expected[i].length, actual[i].length);
            for (int j = 0; j < expected[i].length; j++) {
                assertEquals("Element at position [" + i + "][" + j + "] differs",
                        expected[i][j], actual[i][j], delta);
            }
        }
    }
}