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

    double total_sum = 0.0;
    double start_time = omp_get_wtime(); // Початок вимірювання часу

    // Обчислення загальної суми елементів матриці з використанням редукції
    #pragma omp parallel for reduction(+:total_sum) shared(a, N)
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            total_sum += a[i][j];
        }
    }

    double end_time = omp_get_wtime(); // Кінець вимірювання часу
    printf("Загальна сума елементів матриці: %lf\n", total_sum);
    printf("Час виконання обчислення загальної суми: %lf секунд\n", end_time - start_time);

    // Очищення пам'яті
    for (int i = 0; i < N; i++) {
        free(a[i]);
    }
    free(a);

    return 0;
}

