CC = gcc
CFLAGS = -lm
WINFLAGS = -lpsapi

OUTPUT_DIR_UNIX = ../../data/output
OUTPUT_DIR_WIN = ..\..\data\output

ifeq ($(OS),Windows_NT)
    EXE = .exe
    WIN = 1
    MKDIR = if not exist $(OUTPUT_DIR_WIN) mkdir $(OUTPUT_DIR_WIN)
    OUTPUT_DIR = $(OUTPUT_DIR_WIN)
else
    EXE =
    WIN = 0
    MKDIR = mkdir -p $(OUTPUT_DIR_UNIX)
    OUTPUT_DIR = $(OUTPUT_DIR_UNIX)
endif

all: test benchmark

test: test/matrix/test_matrix_multiplier.c matrix/matrix_multiplier.c matrix/matrix_multiplier.h
	$(CC) test/matrix/test_matrix_multiplier.c matrix/matrix_multiplier.c -o test_matrix$(EXE) $(CFLAGS)

run_test: test
	./test_matrix$(EXE)

benchmark: test/benchmarking/benchmark_matrix_multiplier.c matrix/matrix_multiplier.c matrix/matrix_multiplier.h
ifeq ($(WIN),1)
	$(CC) test/benchmarking/benchmark_matrix_multiplier.c matrix/matrix_multiplier.c -o benchmark$(EXE) $(WINFLAGS)
else
	$(CC) test/benchmarking/benchmark_matrix_multiplier.c matrix/matrix_multiplier.c -o benchmark$(EXE) $(CFLAGS)
endif

run_benchmark: benchmark
	@$(MKDIR)
	./benchmark$(EXE) $(OUTPUT_DIR)

clean:
	rm -f test_matrix$(EXE) benchmark$(EXE)
ifeq ($(WIN),1)
	rm -f $(OUTPUT_DIR_WIN)\summary_c.csv
else
	rm -f $(OUTPUT_DIR_UNIX)/summary_c.csv
endif

.PHONY: all test run_test benchmark run_benchmark clean