#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>

// Функція, що обчислює підінтегральний вираз
double integrand(double t) {
    return 1.0 / (sin(2 * t) * sin(2 * t));
}

// Функція для обчислення інтегралу методом лівих прямокутників
double leftRectangleIntegral(double a, double b, int n, int num_threads) {
    double h = (b - a) / n;  // Ширина одного прямокутника
    double sum = 0.0;

    omp_set_num_threads(num_threads);

#pragma omp parallel for reduction(+:sum)
    for (int i = 0; i < n; i++) {
        double t = a + i * h;
        sum += integrand(t) * h;
    }

    return sum;
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("Використання: %s <кількість потоків> <кількість кроків>\n", argv[0]);
        return 1;
    }

    int num_threads = atoi(argv[1]); // Кількість потоків
    int n = atoi(argv[2]);           // Кількість кроків

    if (num_threads <= 0 || n <= 0) {
        printf("Помилка: кількість потоків та кількість кроків повинні бути додатніми числами.\n");
        return 1;
    }

    double a = 0.0;            // Початок інтервалу
    double b = M_PI / 2;       // Кінець інтервалу (\pi / 2)

    double start_time = omp_get_wtime();
    double result = leftRectangleIntegral(a, b, n, num_threads);
    double end_time = omp_get_wtime();

    printf("Результат обчислення інтегралу: %f\n", result);
    printf("Час виконання: %f секунд\n", end_time - start_time);

    return 0;
}

