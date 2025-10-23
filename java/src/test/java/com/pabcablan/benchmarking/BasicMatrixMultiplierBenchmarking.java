package com.pabcablan.benchmarking;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.pabcablan.matrix.BasicMatrixMultiplier;

import oshi.SystemInfo;
import oshi.software.os.OSProcess;
import oshi.software.os.OperatingSystem;

public class BasicMatrixMultiplierBenchmarking {

    public static void main(String[] args) {
        int[] sizes = {64, 128, 256, 512, 1024};
        int runs = 5;
        String outputDirectory = args[0];
        String outputPath = outputDirectory + "/summary_java.csv";

        System.out.println("Benchmarking in progress...");

        Map<Integer, List<Double>> times = new HashMap<>();
        Map<Integer, List<Double>> memories = new HashMap<>();

        runBenchmarks(sizes, runs, times, memories, outputPath);

        printAverageResults(sizes, times, memories);

        System.out.println("\nBenchmark finished. Results saved at: " + outputPath);
    }

    private static void ensureOutputDirExists(String outputDir) {
        File dir = new File(outputDir);
        if (!dir.exists()) {
            dir.mkdirs();
        }
    }

    private static double getProcessMemoryMB() {
        SystemInfo si = new SystemInfo();
        OperatingSystem os = si.getOperatingSystem();
        int pid = os.getProcessId();
        OSProcess proc = os.getProcess(pid);
        if (proc == null) return -1;
        long rss = proc.getResidentSetSize();
        return rss / (1024.0 * 1024.0);
    }

    private static void runBenchmarks(int[] sizes, int runs, Map<Integer, List<Double>> times, Map<Integer, List<Double>> memories, String outputPath) {
        ensureOutputDirExists(new File(outputPath).getParent());
        try (FileWriter writer = new FileWriter(outputPath)) {
            writer.write("MatrixSize,Run,TimeSeconds,RealMemoryMB\n");

            for (int size : sizes) {
                times.put(size, new ArrayList<>());
                memories.put(size, new ArrayList<>());

                for (int run = 1; run <= runs; run++) {
                    BasicMatrixMultiplier multiplier = new BasicMatrixMultiplier();
                    double[][][] matrices = multiplier.generateMatrices(size);

                    System.gc();
                    double memBefore = getProcessMemoryMB();
                    long start = System.nanoTime();

                    double[][] result = multiplier.multiply(matrices[0], matrices[1]);

                    long end = System.nanoTime();
                    System.gc();
                    double memAfter = getProcessMemoryMB();

                    double timeSeconds = (end - start) / 1_000_000_000.0;
                    double realMemoryMB = Math.max(memBefore, memAfter);

                    timeSeconds = Math.round(timeSeconds * 100000.0) / 100000.0;
                    realMemoryMB = Math.round(realMemoryMB * 100000.0) / 100000.0;

                    times.get(size).add(timeSeconds);
                    memories.get(size).add(realMemoryMB);

                    writer.write(size + "," + run + "," + timeSeconds + "," + realMemoryMB + "\n");
                }
            }
        } catch (IOException e) {
            System.out.println("An error occurred while writing the output file.");
            e.printStackTrace();
        }
    }

    private static void printAverageResults(int[] sizes, Map<Integer, List<Double>> times, Map<Integer, List<Double>> memories) {
        System.out.println("\n===== AVERAGE RESULTS =====");
        System.out.printf("%-10s %-15s %-15s%n", "Size", "Avg Time (s)", "Avg Real Mem (MB)");
        for (int size : sizes) {
            double averageTime = times.get(size).stream().mapToDouble(Double::doubleValue).average().orElse(0.0);
            double averageMemory = memories.get(size).stream().mapToDouble(Double::doubleValue).average().orElse(0.0);

            averageTime = Math.round(averageTime * 100000.0) / 100000.0;
            averageMemory = Math.round(averageMemory * 100000.0) / 100000.0;

            System.out.printf("%-10d %-15.5f %-15.5f%n", size, averageTime, averageMemory);
        }
    }
}