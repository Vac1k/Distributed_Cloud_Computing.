
#include <stdio.h>
#include <omp.h>
#include <stdlib.h>
#include <time.h>

int main(int argc, char *argv[]) {
    // Аргументи командного рядка
    if (argc != 3) {
        printf("Usage: %s <number_of_threads> <number_of_samples>\n", argv[0]);
        return 1;
    }

    int num_threads = atoi(argv[1]);
    long num_samples = atol(argv[2]);
    long inside_circle = 0;

    // Вимірювання часу
    double start_time, end_time;
    start_time = omp_get_wtime();

    // Встановлення кількості потоків
    omp_set_num_threads(num_threads);

    #pragma omp parallel
    {
        unsigned int seed = omp_get_thread_num();
        long local_count = 0;

        #pragma omp for
        for (long i = 0; i < num_samples; i++) {
            double x = (double)rand_r(&seed) / RAND_MAX * 2.0 - 1.0;
            double y = (double)rand_r(&seed) / RAND_MAX * 2.0 - 1.0;

            if (x * x + y * y <= 1.0) {
                local_count++;
            }
        }

        #pragma omp atomic
        inside_circle += local_count;
    }

    double pi = 4.0 * (double)inside_circle / (double)num_samples;

    // Вимірювання часу виконання
    end_time = omp_get_wtime();

    printf("Calculated pi: %.15f\n", pi);
    printf("Execution time: %.6f seconds\n", end_time - start_time);

    return 0;
}
