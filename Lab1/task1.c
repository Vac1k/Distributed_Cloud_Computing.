#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>

// Функція для обчислення інтегралу методом редукції
double integralReduction(double a, double b, int steps, int num_threads) {
    double dx = (b - a) / steps;
    double result = 0.0;

    omp_set_num_threads(num_threads);

#pragma omp parallel for reduction(+:result)
    for (int i = 0; i < steps; i++) {
        double x = a + i * dx;
        double function = log(x) - (3 * sin(3 * x));
        result += function * dx;
    }

    return result;
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("Використання: %s <кількість потоків> <кількість кроків>\n", argv[0]);
        return 1;
    }

    int num_threads = atoi(argv[1]); // Кількість потоків
    int steps = atoi(argv[2]);       // Кількість кроків

    if (num_threads <= 0 || steps <= 0) {
        printf("Помилка: кількість потоків та кількість кроків повинні бути додатніми числами.\n");
        return 1;
    }

    double a = 1.0;       // Початок інтервалу
    double b = 2.0;       // Кінець інтервалу

    double start_time = omp_get_wtime();
    double result = integralReduction(a, b, steps, num_threads);
    double end_time = omp_get_wtime();

    printf("Результат обчислення інтегралу: %f\n", result);
    printf("Час виконання: %f секунд\n", end_time - start_time);

    return 0;
}

