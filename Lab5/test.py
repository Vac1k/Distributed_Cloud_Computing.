
import os
import subprocess
import matplotlib.pyplot as plt
import numpy as np
from tkinter import Tk, Label, Entry, Button, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

# Default Parameters
default_steps = [100000, 500000, 1000000, 5000000]
default_threads = [1, 2, 4, 8, 16]
programs = {"1.c": "1", "2.c": "2"}

def run_experiments(steps, threads):
    results = {prog: [] for prog in programs}
    for prog, prog_id in programs.items():
        if not os.path.exists(prog_id):
            subprocess.run(["gcc", prog, "-fopenmp", "-o", prog_id], check=True)

        for n_steps in steps:
            row = {"steps": n_steps}
            for n_threads in threads:
                result = subprocess.run(
                    [f"./{prog_id}", str(n_threads), str(n_steps)],
                    capture_output=True,
                    text=True
                )
                time_taken = float(
                    [line for line in result.stdout.splitlines() if "Execution time" in line][0].split()[-2]
                )
                row[f"threads_{n_threads}"] = time_taken
            results[prog].append(row)
    return results

def plot_results(results, steps, threads):
    figures = []
    for prog, data in results.items():
        df = pd.DataFrame(data)
        fig, ax = plt.subplots()
        for n_threads in threads:
            ax.plot(df["steps"], df[f"threads_{n_threads}"], label=f"{n_threads} Threads", alpha=0.7)

        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_title(f"Execution Time for {prog}")
        ax.set_xlabel("Number of Steps")
        ax.set_ylabel("Execution Time (s)")
        ax.legend()
        figures.append(fig)
    return figures

def save_results(results):
    for prog, data in results.items():
        df = pd.DataFrame(data)
        table_path = f"{prog}_results.tex"
        df.to_latex(table_path, index=False)
        print(f"Results for {prog} saved to {table_path}")

def generate_report(results):
    report_path = "report.tex"
    with open(report_path, "w") as report:
        report.write("\\documentclass{article}\n\\usepackage{graphicx}\n\\begin{document}\n")
        report.write("\\section*{Experiment Results}\n")
        for prog in programs.keys():
            report.write(f"\\subsection*{{Results for {prog}}}\n")
            report.write(f"\\input{{{prog}_results.tex}}\n")
            report.write(f"\\includegraphics[width=\\textwidth]{{{prog}.png}}\n")
        report.write("\\end{document}\n")
    print(f"Report generated at {report_path}")

# GUI
def run_gui():
    def on_run():
        steps = list(map(int, steps_entry.get().split(",")))
        threads = list(map(int, threads_entry.get().split(",")))
        results = run_experiments(steps, threads)
        save_results(results)
        figures = plot_results(results, steps, threads)

        for prog, fig in zip(programs.keys(), figures):
            fig.savefig(f"{prog}.png")

        generate_report(results)

        for fig in figures:
            canvas = FigureCanvasTkAgg(fig, master=output_frame)
            canvas.draw()
            canvas.get_tk_widget().pack()

    root = Tk()
    root.title("C Program Benchmarking")

    Label(root, text="Steps (comma-separated):").grid(row=0, column=0)
    steps_entry = Entry(root)
    steps_entry.insert(0, ",".join(map(str, default_steps)))
    steps_entry.grid(row=0, column=1)

    Label(root, text="Threads (comma-separated):").grid(row=1, column=0)
    threads_entry = Entry(root)
    threads_entry.insert(0, ",".join(map(str, default_threads)))
    threads_entry.grid(row=1, column=1)

    Button(root, text="Run Experiments", command=on_run).grid(row=2, column=0, columnspan=2)

    output_frame = Label(root)
    output_frame.grid(row=3, column=0, columnspan=2)

    root.mainloop()

if __name__ == "__main__":
    run_gui()
