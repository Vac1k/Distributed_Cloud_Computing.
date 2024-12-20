#include <stdio.h>
#include <omp.h>
#include <stdlib.h>
#include <time.h>

// Функція для обчислення значення інтегралу
double f(double x) {
    return 4.0 / (1.0 + x * x);
}

int main(int argc, char *argv[]) {
    // Аргументи командного рядка
    if (argc != 3) {
        printf("Usage: %s <number_of_threads> <number_of_steps>\n", argv[0]);
        return 1;
    }

    int num_threads = atoi(argv[1]);
    long num_steps = atol(argv[2]);
    double step = 1.0 / (double)num_steps;
    double pi = 0.0;

    // Вимірювання часу
    double start_time, end_time;
    start_time = omp_get_wtime();

    // Встановлення кількості потоків
    omp_set_num_threads(num_threads);

    double global_sum = 0.0;

    #pragma omp parallel
    {
        double x, local_sum = 0.0;
        int i;

        #pragma omp for private(x)
        for (i = 0; i < num_steps; i++) {
            x = (i + 0.5) * step;
            local_sum += f(x);
        }

        #pragma omp atomic
        global_sum += local_sum;
    }

    pi = global_sum * step;

    // Вимірювання часу виконання
    end_time = omp_get_wtime();

    printf("Calculated pi: %.15f\n", pi);
    printf("Execution time: %.6f seconds\n", end_time - start_time);

    return 0;
}
