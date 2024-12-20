import os
import subprocess
import platform
from tkinter import Tk, Label, Entry, Button, Checkbutton, IntVar, Text, Scrollbar, END

MAX_DIMENSION = 5  # Максимальна розмірність для виводу
RESULTS_FILE = "results.txt"  # Файл з результатами програми на C

# Функція для компіляції програми
def compile_c_program():
    os_name = platform.system()
    if os_name == "Windows":
        compile_cmd = "gcc -o task1 task1.c -fopenmp"
    elif os_name == "Linux":
        compile_cmd = "gcc -o task1 task1.c -fopenmp"
    elif os_name == "Darwin":  # macOS
        compile_cmd = "gcc -Xpreprocessor -fopenmp -I/opt/homebrew/opt/libomp/include -L/opt/homebrew/opt/libomp/lib -lomp task1.c -o task1"
    else:
        output_box.insert(END, "Операційна система не підтримується для компіляції.\n")
        return False

    try:
        subprocess.run(compile_cmd, shell=True, check=True)
        output_box.insert(END, "Програму успішно скомпільовано.\n")
        return True
    except subprocess.CalledProcessError as e:
        output_box.insert(END, f"Помилка компіляції: {e}\n")
        return False

# Функція для перевірки наявності скомпільованої програми
def check_compilation():
    return os.path.exists("task1") or os.path.exists("task1.exe")

# Функція для обробки результатів
def display_results_from_file():
    if not os.path.exists(RESULTS_FILE):
        output_box.insert(END, f"Файл {RESULTS_FILE} не знайдено. Перевірте виконання програми.\n")
        return

    with open(RESULTS_FILE, "r") as file:
        lines = file.readlines()

    # Зчитування матриці
    matrix = []
    reading_matrix = False
    for line in lines:
        if "Матриця розширеної системи:" in line:
            reading_matrix = True
            continue
        if reading_matrix:
            if line.strip() == "":
                reading_matrix = False
            else:
                matrix.append([float(num) for num in line.split()])

    # Зчитування розв'язків
    solutions = []
    for line in lines:
        if line.startswith("x["):
            solutions.append(line.strip())

    # Зчитування часу виконання
    execution_time = ""
    for line in lines:
        if "Час виконання" in line:
            execution_time = line.strip()

    # Перевірка розмірності
    if len(matrix) > MAX_DIMENSION:
        output_box.insert(END, "Розмірність матриці перевищує допустиме значення (5).\n")
        output_box.insert(END, f"{execution_time}\n")
    else:
        output_box.insert(END, "Матриця розширеної системи:\n")
        for row in matrix:
            output_box.insert(END, "   " + " ".join(f"{num:8.4f}" for num in row) + "\n")
        output_box.insert(END, "\nРозв'язок системи:\n")
        for solution in solutions:
            output_box.insert(END, f"   {solution}\n")
        output_box.insert(END, f"\n{execution_time}\n")

# Функція для запуску програми
def run_program():
    # Очищення буфера перед запуском
    output_box.delete("1.0", END)

    n = size_input.get()
    threads = threads_input.get()

    if not n.isdigit() or not threads.isdigit():
        output_box.insert(END, "Розмірність та кількість потоків мають бути числами.\n")
        return

    if compile_var.get() or not check_compilation():
        output_box.insert(END, "Перевірка компіляції...\n")
        if not compile_c_program():
            return

    try:
        cmd = f"./task1 {n} {threads}" if platform.system() != "Windows" else f"task1.exe {n} {threads}"
        subprocess.run(cmd, shell=True, check=True)
        display_results_from_file()
    except subprocess.CalledProcessError as e:
        output_box.insert(END, f"Помилка виконання програми: {e}\n")
    except Exception as e:
        output_box.insert(END, f"Помилка запуску: {e}\n")

# Ініціалізація графічного інтерфейсу
root = Tk()
root.title("Запуск C програми - Gruvbox Style")
root.configure(bg="#282828")

# Елементи інтерфейсу
Label(root, text="Розмірність (n):", bg="#282828", fg="#ebdbb2").grid(row=0, column=0, padx=5, pady=5)
size_input = Entry(root, bg="#3c3836", fg="#ebdbb2", insertbackground="#ebdbb2")
size_input.grid(row=0, column=1, padx=5, pady=5)

Label(root, text="Кількість потоків:", bg="#282828", fg="#ebdbb2").grid(row=1, column=0, padx=5, pady=5)
threads_input = Entry(root, bg="#3c3836", fg="#ebdbb2", insertbackground="#ebdbb2")
threads_input.grid(row=1, column=1, padx=5, pady=5)

compile_var = IntVar()
Checkbutton(root, text="Компілювати перед запуском", variable=compile_var, bg="#282828", fg="#ebdbb2", selectcolor="#3c3836").grid(row=2, column=0, columnspan=2, pady=5)

Button(root, text="Запустити", command=run_program, bg="#689d6a", fg="#282828").grid(row=3, column=0, columnspan=2, pady=10)

output_box = Text(root, bg="#282828", fg="#ebdbb2", insertbackground="#ebdbb2", height=20, width=60, wrap="word")
output_box.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

scrollbar = Scrollbar(root, command=output_box.yview)
scrollbar.grid(row=4, column=2, sticky='ns')
output_box['yscrollcommand'] = scrollbar.set

root.mainloop()

