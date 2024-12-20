#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <time.h>

// Функція для друку матриці у файл
void writeMatrixToFile(FILE *file, double **matrix, int n) {
    fprintf(file, "Матриця розширеної системи:\n");
    for (int i = 0; i < n; i++) {
        for (int j = 0; j <= n; j++) {
            fprintf(file, "%lf ", matrix[i][j]);
        }
        fprintf(file, "\n");
    }
    fprintf(file, "\n");
}

// Основна програма
int main(int argc, char *argv[]) {
    srandom(time(NULL));
    if (argc != 3) {
        printf("Використання: %s <розмірність> <кількість потоків>\n", argv[0]);
        return 1;
    }

    int n = atoi(argv[1]);        // Розмірність матриці
    int threads = atoi(argv[2]); // Кількість потоків

    omp_set_num_threads(threads); // Установлення кількості потоків

    double **matrix = malloc(n * sizeof(double *));
    for (int i = 0; i < n; i++) {
        matrix[i] = malloc((n + 1) * sizeof(double));
        for (int j = 0; j <= n; j++) {
            matrix[i][j] = rand() % 10 + 1; // Заповнення матриці випадковими числами
        }
    }

    double *solution = malloc(n * sizeof(double));
    double start_time, end_time;

    FILE *file = fopen("results.txt", "w");
    if (file == NULL) {
        printf("Помилка відкриття файлу results.txt\n");
        return 1;
    }

    // Запис матриці у файл
    writeMatrixToFile(file, matrix, n);

    // Прямий хід
    start_time = omp_get_wtime();
    for (int i = 0; i < n; i++) {
        double tmp = matrix[i][i];
        for (int j = i; j <= n; j++) {
            matrix[i][j] /= tmp;
        }

        #pragma omp parallel for
        for (int j = i + 1; j < n; j++) {
            double factor = matrix[j][i];
            for (int k = i; k <= n; k++) {
                matrix[j][k] -= factor * matrix[i][k];
            }
        }
    }

    // Зворотний хід
    solution[n - 1] = matrix[n - 1][n];
    for (int i = n - 2; i >= 0; i--) {
        solution[i] = matrix[i][n];
        for (int j = i + 1; j < n; j++) {
            solution[i] -= matrix[i][j] * solution[j];
        }
    }
    end_time = omp_get_wtime();

    // Запис результатів у файл
    fprintf(file, "Розв'язок системи:\n");
    for (int i = 0; i < n; i++) {
        fprintf(file, "x[%d] = %lf\n", i, solution[i]);
    }
    fprintf(file, "Час виконання: %lf секунд\n", end_time - start_time);

    fclose(file);

    // Повідомлення користувачу
    printf("Результати записано в файл results.txt\n");

    // Очищення пам'яті
    for (int i = 0; i < n; i++) {
        free(matrix[i]);
    }
    free(matrix);
    free(solution);

    return 0;
}

