import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import platform

# Створюємо головне вікно
root = tk.Tk()
root.title("Компиляція та запуск C програм")
root.geometry("550x500")
root.configure(bg="#2b2b2b")

# Налаштування темної теми
root.option_add("*Foreground", "white")
root.option_add("*Background", "#2b2b2b")
root.option_add("*Button.Background", "#3c3f41")
root.option_add("*Button.Foreground", "white")

# Список файлів і відповідних назв завдань (скорочені назви)
tasks = {
    "1.c": "1 - Версія OpenMP і точність таймера",
    "2.c": "2 - Множення матриць",
    "3.c": "3.1 - Сума рядків матриці",
    "3_2.c": "3.2 - Загальна сума матриці"
}

def compile_file(file_name):
    """Компіляція вказаного файлу C."""
    output_file = file_name.split('.')[0]  # Ім'я виконуваного файлу

    # Перевірка операційної системи

    compile_command = ["gcc","-Xpreprocessor" , "-fopenmp", "-I/opt/homebrew/opt/libomp/include",
                           "-L/opt/homebrew/opt/libomp/lib","-lomp",file_name, "-o", output_file]

    
    try:
        result = subprocess.run(compile_command, capture_output=True, text=True)
        if result.returncode == 0:
            messagebox.showinfo("Успіх", f"{tasks[file_name]} успішно скомпільовано.")
        else:
            messagebox.showerror("Помилка компіляції", result.stderr)
    except Exception as e:
        messagebox.showerror("Помилка", f"Не вдалося скомпілювати {tasks[file_name]}.\n{e}")

def run_file(file_name):
    """Запуск скомпільованого файлу з введеними параметрами."""
    output_file = f"./{file_name.split('.')[0]}"
    if platform.system() == "Windows":
        output_file += ".exe"

    if not os.path.exists(output_file):
        messagebox.showerror("Помилка", f"Файл {output_file} не знайдено. Спочатку скомпілюйте його.")
        return

    # Отримання параметрів від користувача
    matrix_size = matrix_size_entry.get()
    num_threads = num_threads_entry.get()

    if not matrix_size.isdigit() or not num_threads.isdigit():
        messagebox.showerror("Помилка", "Будь ласка, введіть коректні числові значення для розмірності матриці та кількості потоків.")
        return

    args = [matrix_size, num_threads]

    try:
        result = subprocess.run([output_file] + args, capture_output=True, text=True)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result.stdout + result.stderr)
    except Exception as e:
        messagebox.showerror("Помилка", f"Не вдалося запустити {output_file}.\n{e}")

# Інтерфейс для введення параметрів
param_frame = tk.Frame(root, bg="#2b2b2b")
param_frame.pack(pady=10)

matrix_size_label = tk.Label(param_frame, text="Розмірність матриці:")
matrix_size_label.grid(row=0, column=0, padx=5, pady=5)
matrix_size_entry = tk.Entry(param_frame, width=10)
matrix_size_entry.grid(row=0, column=1, padx=5, pady=5)

num_threads_label = tk.Label(param_frame, text="Кількість потоків:")
num_threads_label.grid(row=1, column=0, padx=5, pady=5)
num_threads_entry = tk.Entry(param_frame, width=10)
num_threads_entry.grid(row=1, column=1, padx=5, pady=5)

# Інтерфейс для компіляції та запуску завдань
frame = tk.Frame(root, bg="#2b2b2b")
frame.pack(pady=20, fill="x")

for file_name, task_name in tasks.items():
    btn_frame = tk.Frame(frame, bg="#2b2b2b")
    btn_frame.pack(pady=5, fill="x")

    label = tk.Label(btn_frame, text=task_name, anchor="w")
    label.pack(side="left", padx=10)

    compile_btn = tk.Button(btn_frame, text="Компіліювати", command=lambda fn=file_name: compile_file(fn))
    run_btn = tk.Button(btn_frame, text="Запустити", command=lambda fn=file_name: run_file(fn))
    
    # Праве вирівнювання кнопок
    compile_btn.pack(side="right", padx=10, anchor="e")
    run_btn.pack(side="right", padx=10, anchor="e")

# Текстове поле для виведення результату
output_text = tk.Text(root, height=10, wrap="word", bg="#3c3f41", fg="white")
output_text.pack(fill="both", padx=10, pady=10)

# Запуск вікна
root.mainloop()

