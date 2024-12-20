import os
import subprocess
import platform
from tkinter import Tk, Label, Entry, Button, IntVar, Checkbutton, Text, END, messagebox

# Стиль Gruvbox
BG_COLOR = "#282828"
FG_COLOR = "#ebdbb2"
BTN_COLOR = "#689d6a"
ENTRY_COLOR = "#3c3836"
TEXT_COLOR = "#fabd2f"

def compile_program(c_file, output_name):
    """Компілює програму залежно від ОС."""
    system = platform.system()
    compile_command = ["gcc", "-Xpreprocessor", "-fopenmp", "-I/opt/homebrew/opt/libomp/include",
                       "-L/opt/homebrew/opt/libomp/lib", "-lomp", c_file, "-o", output_name]

    try:
        if system == "Linux":
            # Компіляція для Linux
            subprocess.run(["gcc", "-fopenmp", c_file, "-o", output_name, "-lm"], check=True)
        elif system == "Windows":
            # Компіляція для Windows (MinGW)
            subprocess.run(["gcc", "-fopenmp", c_file, "-o", output_name, "-lmingw32", "-lm"], check=True)
        else:
            subprocess.run(compile_command, check=True)
        return True
    except subprocess.CalledProcessError:
        messagebox.showerror("Помилка", f"Не вдалося скомпілювати {c_file}.")
        return False

def run_program(program_name, threads, steps, compile_first, c_file):
    """Запускає програму з переданими аргументами."""
    if compile_first or not os.path.exists(program_name):
        if not compile_program(c_file, program_name):
            return

    try:
        result = subprocess.run([f"./{program_name}" if platform.system() != "Windows" else program_name, str(threads), str(steps)],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            output_text.delete(1.0, END)
            output_text.insert(END, result.stdout)
        else:
            messagebox.showerror("Помилка виконання", result.stderr)
    except Exception as e:
        messagebox.showerror("Помилка", str(e))

def execute_task1():
    """Виконує перше завдання."""
    threads = int(threads_entry.get())
    steps = int(steps_entry.get())
    run_program("task1", threads, steps, compile_var.get(), "task1.c")

def execute_task2():
    """Виконує друге завдання."""
    threads = int(threads_entry.get())
    steps = int(steps_entry.get())
    run_program("task2", threads, steps, compile_var.get(), "task2.c")

# Налаштування GUI
root = Tk()
root.title("OpenMP Launcher")
root.configure(bg=BG_COLOR)

# Заголовок
Label(root, text="Запуск програм OpenMP", bg=BG_COLOR, fg=FG_COLOR, font=("Helvetica", 16)).grid(row=0, columnspan=2, pady=10)

# Введення кількості потоків
Label(root, text="Кількість потоків:", bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=0, sticky="e", padx=10, pady=5)
threads_entry = Entry(root, bg=ENTRY_COLOR, fg=FG_COLOR)
threads_entry.grid(row=1, column=1, pady=5)

# Введення кількості кроків
Label(root, text="Кількість кроків:", bg=BG_COLOR, fg=FG_COLOR).grid(row=2, column=0, sticky="e", padx=10, pady=5)
steps_entry = Entry(root, bg=ENTRY_COLOR, fg=FG_COLOR)
steps_entry.grid(row=2, column=1, pady=5)

# Checkbox для компілювання
compile_var = IntVar()
compile_checkbox = Checkbutton(root, text="Компілювати перед запуском", variable=compile_var, bg=BG_COLOR, fg=FG_COLOR, selectcolor=BG_COLOR, activebackground=BG_COLOR)
compile_checkbox.grid(row=3, columnspan=2, pady=5)

# Кнопки запуску
Button(root, text="Запустити Завдання 1", command=execute_task1, bg=BTN_COLOR, fg=FG_COLOR, activebackground=TEXT_COLOR).grid(row=4, column=0, pady=10, padx=5)
Button(root, text="Запустити Завдання 2", command=execute_task2, bg=BTN_COLOR, fg=FG_COLOR, activebackground=TEXT_COLOR).grid(row=4, column=1, pady=10, padx=5)

# Виведення результату
Label(root, text="Результат:", bg=BG_COLOR, fg=FG_COLOR).grid(row=5, columnspan=2, pady=5)
output_text = Text(root, height=10, bg=ENTRY_COLOR, fg=FG_COLOR)
output_text.grid(row=6, columnspan=2, padx=10, pady=5)

# Запуск програми
root.mainloop()

