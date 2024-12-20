#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

int main(int argc, char *argv[]) {
    if (argc < 3) {
        printf("Використання: %s <розмірність матриці> <кількість потоків>\n", argv[0]);
        return 1;
    }

    int N = atoi(argv[1]);  // Розмірність матриці
    int num_threads = atoi(argv[2]);  // Кількість потоків

    // Виділення пам'яті для матриці
    double **a = (double **)malloc(N * sizeof(double *));
    for (int i = 0; i < N; i++) {
        a[i] = (double *)malloc(N * sizeof(double));
    }

    // Ініціалізація матриці
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            a[i][j] = i + j;  // Заповнення матриці значеннями для тесту
        }
    }

    omp_set_num_threads(num_threads); // Встановлення кількості потоків

    double start_time = omp_get_wtime(); // Початок вимірювання часу

    // Обчислення суми елементів кожного рядка
    #pragma omp parallel for shared(a, N)
    for (int i = 0; i < N; i++) {
        double sum = 0;
        for (int j = 0; j < N; j++) {
            sum += a[i][j];
        }
        printf("Сума елементів рядка %d: %lf\n", i, sum);
    }

    double end_time = omp_get_wtime(); // Кінець вимірювання часу
    printf("Час виконання обчислення суми рядків: %lf секунд\n", end_time - start_time);

    // Очищення пам'яті
    for (int i = 0; i < N; i++) {
        free(a[i]);
    }
    free(a);

    return 0;
}

