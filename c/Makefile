CC = gcc
CFLAGS = -O3 -march=native -lm
WINFLAGS = -O3 -march=native -lpsapi

OUTPUT_DIR_UNIX = ../data/output
OUTPUT_DIR_WIN = ..\data\output

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

test: test/matrix/basic_matrix_multiplier_test.c src/matrix/basic_matrix_multiplier.c src/matrix/basic_matrix_multiplier.h
	$(CC) test/matrix/basic_matrix_multiplier_test.c src/matrix/basic_matrix_multiplier.c -o test_matrix$(EXE) $(CFLAGS)

run_test: test
	./test_matrix$(EXE)

benchmark: test/benchmarking/basic_matrix_multiplier_benchmarking.c src/matrix/basic_matrix_multiplier.c src/matrix/basic_matrix_multiplier.h
ifeq ($(WIN),1)
	$(CC) test/benchmarking/basic_matrix_multiplier_benchmarking.c src/matrix/basic_matrix_multiplier.c -o benchmark$(EXE) $(WINFLAGS)
else
	$(CC) test/benchmarking/basic_matrix_multiplier_benchmarking.c src/matrix/basic_matrix_multiplier.c -o benchmark$(EXE) $(CFLAGS)
endif

run_benchmark: benchmark
	@$(MKDIR)
	./benchmark$(EXE) $(OUTPUT_DIR)

clean:
ifeq ($(WIN),1)
	-if exist test_matrix$(EXE) del /Q test_matrix$(EXE)
	-if exist benchmark$(EXE) del /Q benchmark$(EXE)
	-if exist $(OUTPUT_DIR_WIN)\summary_c.csv del /Q $(OUTPUT_DIR_WIN)\summary_c.csv
else
	rm -f test_matrix$(EXE) benchmark$(EXE)
	rm -f $(OUTPUT_DIR_UNIX)/summary_c.csv
endif

.PHONY: all test run_test benchmark run_benchmark clean