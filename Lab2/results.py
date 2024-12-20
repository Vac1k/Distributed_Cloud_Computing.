import subprocess
import os
import matplotlib.pyplot as plt
import numpy as np
import re

# Параметри тестування
programs = {"2": "Час виконання множення матриць", 
            "3": "Час виконання обчислення суми рядків",
            "3_2": "Час виконання обчислення загальної суми"}
num_threads = [1, 2, 4, 8, 16]  # тільки степені 2 до 16
matrix_sizes = [100, 200, 400, 800, 1600]

# Створення папок для збереження результатів
if not os.path.exists("results"):
    os.makedirs("results")
if not os.path.exists("graphs"):
    os.makedirs("graphs")

# Зберігання результатів часу виконання
results = {program: {size: {} for size in matrix_sizes} for program in programs}

# Функція для вилучення часу виконання з виводу
def extract_time(output, keyword):
    # Знаходить число після ключового слова (наприклад, "Час виконання множення матриць:")
    match = re.search(fr"{re.escape(keyword)}:\s*([\d.]+)", output)
    return float(match.group(1)) if match else None

# Запуск програм з різними параметрами
for program, keyword in programs.items():
    for size in matrix_sizes:
        for threads in num_threads:
            output_file = f"./{program}"
            args = [str(size), str(threads)]
            try:
                # Запуск програми та зчитування часу виконання
                result = subprocess.run([output_file] + args, capture_output=True, text=True)
                exec_time = extract_time(result.stdout, keyword)
                if exec_time is None:
                    raise ValueError("Час виконання не знайдено")
                results[program][size][threads] = exec_time
            except Exception as e:
                print(f"Помилка під час виконання {program} з розміром {size} і {threads} потоків: {e}")
                results[program][size][threads] = None

# Побудова графіків для кожної програми
for program in programs:
    plt.figure(figsize=(10, 6))
    for threads in num_threads:
        times = [results[program][size][threads] for size in matrix_sizes]
        plt.bar(
            [str(size) for size in matrix_sizes],
            times,
            alpha=0.7,
            label=f"{threads} потоків"
        )
    
    plt.xlabel("Розмірність матриці")
    plt.ylabel("Час виконання (с)")
    plt.title(f"Залежність часу виконання від розмірності для програми {program}")
    plt.legend()
    plt.savefig(f"graphs/{program}_performance.png")
    plt.close()

# Генерація таблиці в LaTeX
with open("results/performance_table.tex", "w") as f:
    # Запис заголовку таблиці
    f.write("\\begin{table}[h!]\n")
    f.write("\\centering\n")
    f.write("\\begin{tabular}{|c|" + "c|" * len(num_threads) + "}\n")
    f.write("\\hline\n")
    f.write("Розмірність & " + " & ".join([f"{t} потоків" for t in num_threads]) + " \\\\\n")
    f.write("\\hline\n")

    # Запис результатів для кожної програми
    for program in programs:
        f.write(f"\\multicolumn{{{len(num_threads)+1}}}{{|c|}}{{Програма {program}}} \\\\\n")
        f.write("\\hline\n")
        for size in matrix_sizes:
            row = [f"{size}"]
            for threads in num_threads:
                time = results[program][size][threads]
                row.append(f"{time:.6f}" if time is not None else "-")
            f.write(" & ".join(row) + " \\\\\n")
            f.write("\\hline\n")

    f.write("\\end{tabular}\n")
    f.write("\\caption{Час виконання програм при різній кількості потоків і розмірності матриці}\n")
    f.write("\\end{table}\n")

