#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#ifdef _WIN32
#include <windows.h>
#include <psapi.h>
double get_process_memory_mb() {
    PROCESS_MEMORY_COUNTERS memCounter;
    GetProcessMemoryInfo(GetCurrentProcess(), &memCounter, sizeof(memCounter));
    return (double)memCounter.WorkingSetSize / (1024 * 1024);
}
#else
#include <unistd.h>
#include <sys/resource.h>
double get_process_memory_mb() {
    struct rusage usage;
    getrusage(RUSAGE_SELF, &usage);
    return (double)usage.ru_maxrss / 1024;
}
#endif
#include "../../matrix/matrix_multiplier.h"

int sizes[] = {128, 256, 512, 1024};
int runs = 5;

void run_benchmarks(const char *csv_path, double times[][5], double memories[][5]) {
    FILE *csvfile = fopen(csv_path, "w");
    fprintf(csvfile, "MatrixSize,Run,TimeSeconds,RealMemoryMB\n");
    for (int s = 0; s < sizeof(sizes)/sizeof(sizes[0]); ++s) {
        int n = sizes[s];
        for (int r = 0; r < runs; ++r) {
            double **A = allocate_matrix(n);
            double **B = allocate_matrix(n);
            generate_matrices(A, B, n);
            double mem_before = get_process_memory_mb();
            clock_t start = clock();
            double **C = allocate_matrix(n);
            multiply(A, B, C, n);
            clock_t end = clock();
            double mem_after = get_process_memory_mb();
            double time_seconds = (double)(end - start) / CLOCKS_PER_SEC;
            double real_memory_mb = mem_before > mem_after ? mem_before : mem_after;
            times[s][r] = time_seconds;
            memories[s][r] = real_memory_mb;
            fprintf(csvfile, "%d,%d,%.5f,%.5f\n", n, r+1, time_seconds, real_memory_mb);
            free_matrix(A, n);
            free_matrix(B, n);
            free_matrix(C, n);
        }
    }
    fclose(csvfile);
}

void print_average_results(double times[][5], double memories[][5]) {
    printf("\n===== AVERAGE RESULTS =====\n");
    printf("%-10s %-15s %-25s\n", "Size", "Avg Time (s)", "Avg Real Mem (MB)");
    for (int s = 0; s < sizeof(sizes)/sizeof(sizes[0]); ++s) {
        double sum_time = 0, sum_mem = 0;
        for (int r = 0; r < runs; ++r) {
            sum_time += times[s][r];
            sum_mem += memories[s][r];
        }
        double avg_time = sum_time / runs;
        double avg_mem = sum_mem / runs;
        printf("%-10d %-15.5f %-25.5f\n", sizes[s], avg_time, avg_mem);
    }
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <output_directory>\n", argv[0]);
        return 1;
    }
    char csv_path[256];
    #ifdef _WIN32
    snprintf(csv_path, sizeof(csv_path), "%s\\summary_c.csv", argv[1]);
    #else
    snprintf(csv_path, sizeof(csv_path), "%s/summary_c.csv", argv[1]);
    #endif
    double times[sizeof(sizes)/sizeof(sizes[0])][5] = {0};
    double memories[sizeof(sizes)/sizeof(sizes[0])][5] = {0};
    printf("Benchmarking in progress...\n");
    run_benchmarks(csv_path, times, memories);
    print_average_results(times, memories);
    printf("\nBenchmark finished. Results saved at: %s\n", csv_path);
    return 0;
}