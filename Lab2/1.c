#include <stdio.h>
#include <omp.h>

int main() {
    // Перевірка підтримки OpenMP і вивід версії
    #ifdef _OPENMP
        printf("OpenMP is supported! Version: %d\n\n", _OPENMP);
    #else
        printf("OpenMP is not supported.\n\n");
    #endif

    // Вимірювання часу та точності системного таймера
    double start_time, end_time, tick;
    start_time = omp_get_wtime();
    end_time = omp_get_wtime();
    tick = omp_get_wtick();
    
    printf("Час на вимірювання часу: %lf секунд\n", end_time - start_time);
    printf("Точність таймеру: %lf секунд\n\n", tick);

    // Паралельне виведення "Hello World"
    #pragma omp parallel
    {
        printf("Hello World from thread %d!\n", omp_get_thread_num());
    }

    return 0;
}

