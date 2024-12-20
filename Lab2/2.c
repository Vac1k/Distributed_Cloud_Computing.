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

    // Виділення пам'яті для матриць
    double **a = (double **)malloc(N * sizeof(double *));
    double **b = (double **)malloc(N * sizeof(double *));
    double **c = (double **)malloc(N * sizeof(double *));
    for (int i = 0; i < N; i++) {
        a[i] = (double *)malloc(N * sizeof(double));
        b[i] = (double *)malloc(N * sizeof(double));
        c[i] = (double *)malloc(N * sizeof(double));
    }

    // Ініціалізація матриць a та b
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            a[i][j] = i + j;
            b[i][j] = i - j;
            c[i][j] = 0.0; // Ініціалізація матриці результату
        }
    }

    omp_set_num_threads(num_threads); // Встановлення кількості потоків

    double start_time = omp_get_wtime(); // Початок вимірювання часу

    // Обчислення множення матриць
    int i, j, k;
    #pragma omp parallel for private(i, j, k) shared(a, b, c, N)
    for (i = 0; i < N; i++) {
        for (j = 0; j < N; j++) {
            for (k = 0; k < N; k++) {
                c[i][j] += a[i][k] * b[k][j];
            }
        }
    }

    double end_time = omp_get_wtime(); // Кінець вимірювання часу
    printf("Час виконання множення матриць: %lf секунд\n", end_time - start_time);

    // Очищення пам'яті
    for (int i = 0; i < N; i++) {
        free(a[i]);
        free(b[i]);
        free(c[i]);
    }
    free(a);
    free(b);
    free(c);

    return 0;
}

