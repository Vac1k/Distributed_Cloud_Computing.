
#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <time.h>

#define EMPTY 0
#define RABBIT 2
#define WOLF 1
#define ROWS 20
#define COLS 20

void print_grid(int grid[ROWS][COLS]) {
    for (int i = 0; i < ROWS; i++) {
        for (int j = 0; j < COLS; j++) {
            printf("%d ", grid[i][j]);
        }
        printf("\n");
    }
    printf("\n");
}

void simulate_step(int grid[ROWS][COLS], int new_grid[ROWS][COLS]) {
    #pragma omp parallel for collapse(2)
    for (int i = 0; i < ROWS; i++) {
        for (int j = 0; j < COLS; j++) {
            int wolves = 0, rabbits = 0;
            for (int di = -1; di <= 1; di++) {
                for (int dj = -1; dj <= 1; dj++) {
                    if (di == 0 && dj == 0) continue;
                    int ni = i + di, nj = j + dj;
                    if (ni >= 0 && ni < ROWS && nj >= 0 && nj < COLS) {
                        if (grid[ni][nj] == WOLF) wolves++;
                        if (grid[ni][nj] == RABBIT) rabbits++;
                    }
                }
            }
            if (grid[i][j] == EMPTY && rabbits >= 3) {
                new_grid[i][j] = RABBIT;
            } else if (grid[i][j] == RABBIT) {
                if (wolves > 0) {
                    new_grid[i][j] = EMPTY; // Rabbit eaten
                } else {
                    new_grid[i][j] = (rabbits >= 2 && rabbits <= 5) ? RABBIT : EMPTY;
                }
            } else if (grid[i][j] == WOLF) {
                if (rabbits > 0) {
                    new_grid[i][j] = WOLF; // Wolf survives by eating a rabbit
                } else {
                    new_grid[i][j] = EMPTY; // Wolf dies from starvation
                }
            } else {
                new_grid[i][j] = EMPTY;
            }
        }
    }
}

int main(int argc, char *argv[]) {
    if (argc != 4) {
        fprintf(stderr, "Usage: %s <threads> <steps> <seed>\n", argv[0]);
        return EXIT_FAILURE;
    }

    int threads = atoi(argv[1]);
    int steps = atoi(argv[2]);
    int seed = atoi(argv[3]);
    omp_set_num_threads(threads);

    srand(seed);

    int grid[ROWS][COLS] = {0};
    int new_grid[ROWS][COLS] = {0};

    // Initialize grid with random values
    for (int i = 0; i < ROWS; i++) {
        for (int j = 0; j < COLS; j++) {
            int r = rand() % 10;
            if (r < 2) {
                grid[i][j] = WOLF;
            } else if (r < 5) {
                grid[i][j] = RABBIT;
            } else {
                grid[i][j] = EMPTY;
            }
        }
    }

    printf("Initial grid:\n");
    print_grid(grid);

    double start_time = omp_get_wtime();

    for (int step = 0; step < steps; step++) {
        simulate_step(grid, new_grid);

        // Copy new_grid back to grid
        #pragma omp parallel for collapse(2)
        for (int i = 0; i < ROWS; i++) {
            for (int j = 0; j < COLS; j++) {
                grid[i][j] = new_grid[i][j];
            }
        }

        printf("After step %d:\n", step + 1);
        print_grid(grid);
    }

    double end_time = omp_get_wtime();

    printf("Execution time: %.2f seconds\n", end_time - start_time);

    return EXIT_SUCCESS;
}
