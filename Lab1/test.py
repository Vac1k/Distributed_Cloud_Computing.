import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button, Text, END, IntVar
import pandas as pd

# Функція для запуску програм і збору даних
def run_program(program_name, threads, steps):
    try:
        result = subprocess.run([f"./{program_name}", str(threads), str(steps)],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            output = result.stdout.splitlines()
            for line in output:
                if "Час виконання" in line:
                    time = float(line.split(":")[1].strip().split()[0])
                    return time
        return None
    except Exception as e:
        print(f"Помилка виконання {program_name}: {e}")
        return None

# Функція для виконання експериментів
def execute_experiments(program_name, steps_list, max_threads=16):
    data = {"Кількість кроків": steps_list}
    for threads in [1] + [2 ** i for i in range(1, int(np.log2(max_threads)) + 1)]:
        times = []
        for steps in steps_list:
            time = run_program(program_name, threads, steps)
            times.append(time if time is not None else 0)
        data[f"Час для {threads} потоків"] = times
    return data

# Побудова графіка
def plot_results(data, program_name):
    steps = data["Кількість кроків"]
    plt.figure(figsize=(12, 8))
    for column in data:
        if column != "Кількість кроків":
            plt.plot(steps, data[column], label=column, alpha=0.8, linewidth=2, marker='o')

    plt.title(f"Час виконання залежно від кількості кроків для {program_name}", fontsize=16, fontweight="bold")
    plt.xlabel("Кількість кроків (log scale)", fontsize=14)
    plt.ylabel("Час виконання (секунди) (log scale)", fontsize=14)
    plt.xscale("log")
    plt.yscale("log")
    plt.grid(True, which="both", linestyle="--", alpha=0.6)
    plt.legend(fontsize=12, loc="upper left")
    plt.tight_layout()
    plt.savefig(f"{program_name}_results.png")
    plt.show()

# Збереження в LaTeX таблицю
def save_latex_table(data, filename):
    df = pd.DataFrame(data)
    with open(filename, "w") as f:
        f.write(df.to_latex(index=False, float_format="%.6f"))

# Інтерфейс
def run_gui():
    def execute():
        program_name = program_entry.get()
        steps_list = list(map(int, steps_entry.get().split(",")))
        max_threads = int(threads_entry.get())
        data = execute_experiments(program_name, steps_list, max_threads)
        save_latex_table(data, f"{program_name}_results.tex")
        plot_results(data, program_name)
        output_text.delete(1.0, END)
        output_text.insert(END, f"Результати збережено у {program_name}_results.tex\n")
        output_text.insert(END, f"Графік збережено у {program_name}_results.png\n")

    root = Tk()
    root.title("OpenMP Experiment Launcher")
    root.geometry("700x500")
    root.configure(bg="#282828")

    Label(root, text="OpenMP Experiment Launcher", bg="#282828", fg="#ebdbb2", font=("Helvetica", 16, "bold")).grid(row=0, columnspan=2, pady=10)

    Label(root, text="Назва програми:", bg="#282828", fg="#ebdbb2", font=("Helvetica", 12)).grid(row=1, column=0, sticky="e", padx=10, pady=10)
    program_entry = Entry(root, width=40, bg="#3c3836", fg="#ebdbb2", font=("Helvetica", 12))
    program_entry.insert(0, "task1")
    program_entry.grid(row=1, column=1, pady=5)

    Label(root, text="Кількість кроків (через кому):", bg="#282828", fg="#ebdbb2", font=("Helvetica", 12)).grid(row=2, column=0, sticky="e", padx=10, pady=10)
    steps_entry = Entry(root, width=40, bg="#3c3836", fg="#ebdbb2", font=("Helvetica", 12))
    steps_entry.insert(0, "1000,5000,10000,50000,100000")
    steps_entry.grid(row=2, column=1, pady=5)

    Label(root, text="Максимальна кількість потоків:", bg="#282828", fg="#ebdbb2", font=("Helvetica", 12)).grid(row=3, column=0, sticky="e", padx=10, pady=10)
    threads_entry = Entry(root, width=40, bg="#3c3836", fg="#ebdbb2", font=("Helvetica", 12))
    threads_entry.insert(0, "16")
    threads_entry.grid(row=3, column=1, pady=5)

    Button(root, text="Виконати експерименти", command=execute, bg="#689d6a", fg="#ebdbb2", font=("Helvetica", 12, "bold"), activebackground="#8ec07c").grid(row=4, columnspan=2, pady=20)

    output_text = Text(root, height=10, width=80, bg="#3c3836", fg="#ebdbb2", font=("Helvetica", 12))
    output_text.grid(row=5, columnspan=2, padx=10, pady=10)

    root.mainloop()

# Запуск GUI
if __name__ == "__main__":
    run_gui()

