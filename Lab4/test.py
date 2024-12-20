import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tkinter import Tk, Label, Entry, Button, Text, Scrollbar, END

RESULTS_FILE = "results.txt"

# Функція для читання часу виконання з results.txt
def read_execution_time():
    if not os.path.exists(RESULTS_FILE):
        return None
    with open(RESULTS_FILE, "r") as file:
        for line in file:
            if "Час виконання" in line:
                return float(line.split(":")[1].strip().split()[0])
    return None

# Функція для запуску програми та збору даних
def run_program(param_list, threads_range):
    results = []
    for params in param_list:
        row = {"Кількість параметрів": params}
        for threads in threads_range:
            cmd = f"./task1 {params} {threads}" if os.name != "nt" else f"task1.exe {params} {threads}"
            os.system(cmd)
            time = read_execution_time()
            if time is not None:
                row[f"Час для {threads} потоків"] = time
        results.append(row)
    return pd.DataFrame(results)

# Функція для створення графіків
def generate_plots(df, threads_range):
    plt.figure(figsize=(12, 8))
    colors = plt.cm.viridis(np.linspace(0, 1, len(threads_range)))

    for threads, color in zip(threads_range, colors):
        plt.plot(df["Кількість параметрів"], df[f"Час для {threads} потоків"], label=f"{threads} потоків", marker="o", alpha=0.8, color=color)

    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Кількість параметрів", fontsize=14)
    plt.ylabel("Час виконання (с)", fontsize=14)
    plt.title("Залежність часу виконання від кількості параметрів", fontsize=16)
    plt.grid(which="both", linestyle="--", linewidth=0.5, alpha=0.7)
    plt.legend(fontsize=12)
    plt.tight_layout()
    plt.savefig("performance_plot.png")
    plt.show()

# Функція для створення таблиці LaTeX
def generate_latex_table(df, output_file):
    latex = df.to_latex(index=False, longtable=True, float_format="%.6f", column_format="|c|" + "c|" * len(df.columns))
    with open(output_file, "w") as f:
        f.write(latex)

# GUI
def start_analysis():
    param_list = list(map(int, param_list_entry.get().split(",")))
    threads_max = int(threads_max_entry.get())
    output_box.delete("1.0", END)

    threads_range = [2**i for i in range(0, int(np.log2(threads_max)) + 1)]
    output_box.insert(END, "Генерація даних...\n")
    df = run_program(param_list, threads_range)

    output_box.insert(END, "Створення графіків...\n")
    generate_plots(df, threads_range)

    output_box.insert(END, "Генерація LaTeX таблиці...\n")
    generate_latex_table(df, "results_table.tex")

    output_box.insert(END, "Результати збережено в 'results_table.tex' та 'performance_plot.png'.\n")

# GUI створення
root = Tk()
root.title("Аналіз продуктивності програми")
root.geometry("600x400")

Label(root, text="Список параметрів (через кому)").grid(row=0, column=0, padx=10, pady=5)
param_list_entry = Entry(root)
param_list_entry.insert(0, "2,4,8,16,32,64,128,256,512,1024")
param_list_entry.grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Максимальна кількість потоків").grid(row=1, column=0, padx=10, pady=5)
threads_max_entry = Entry(root)
threads_max_entry.insert(0, "16")
threads_max_entry.grid(row=1, column=1, padx=10, pady=5)

Button(root, text="Запустити аналіз", command=start_analysis).grid(row=2, column=0, columnspan=2, pady=20)

output_box = Text(root, height=10, width=60)
output_box.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

scrollbar = Scrollbar(root, command=output_box.yview)
scrollbar.grid(row=3, column=2, sticky="ns")
output_box["yscrollcommand"] = scrollbar.set

root.mainloop()

