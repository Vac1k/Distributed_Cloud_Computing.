
import os
import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def compile_c_program():

    if not os.path.exists("wolves_rabbits_simulation"):  # Check if the binary exists
        dir = "wolves_rabbits_simulation"

        result = subprocess.run(["gcc", "-Xpreprocessor", "-fopenmp", "-I/opt/homebrew/opt/libomp/include",
                        "-L/opt/homebrew/opt/libomp/lib", "-lomp", f"{dir}.c", "-o", dir],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            messagebox.showinfo("Compilation", "Compilation successful!")
        else:
            messagebox.showerror("Compilation", f"Compilation failed:\n{result.stderr.decode()}")
    else:
        messagebox.showinfo("Compilation", "Program is already compiled.")

def parse_output(output):
    steps = []
    current_grid = []
    parsing_grid = False
    for line in output.splitlines():
        if line.startswith("Initial grid") or line.startswith("After step"):
            if current_grid:
                steps.append(current_grid)
                current_grid = []
            parsing_grid = True
        elif parsing_grid:
            if line.strip():
                current_grid.append([int(cell) for cell in line.split()])
            else:
                if current_grid:
                    steps.append(current_grid)
                    current_grid = []
                    parsing_grid = False
    if current_grid:
        steps.append(current_grid)
    return steps

def plot_grid(grid):
    fig, ax = plt.subplots()
    ax.imshow(grid, cmap="viridis", origin="upper")
    ax.set_xticks([])
    ax.set_yticks([])
    return fig

def update_plot(step):
    global canvas, grids, current_step
    current_step = step
    fig = plot_grid(grids[current_step])
    canvas.figure = fig
    canvas.draw()

def next_step():
    global current_step, grids
    if current_step < len(grids) - 1:
        update_plot(current_step + 1)

def prev_step():
    global current_step, grids
    if current_step > 0:
        update_plot(current_step - 1)

def run_simulation():
    global grids, current_step, canvas
    threads = thread_entry.get()
    steps = steps_entry.get()
    seed = seed_entry.get()

    if not os.path.exists("wolves_rabbits_simulation"):
        messagebox.showwarning("Error", "The program is not compiled. Please compile it first.")
        return

    if not (threads.isdigit() and steps.isdigit() and seed.isdigit()):
        messagebox.showwarning("Input Error", "Please enter valid numeric values for all inputs.")
        return

    try:
        process = subprocess.run(["./wolves_rabbits_simulation", threads, steps, seed],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if process.returncode == 0:
            grids = parse_output(process.stdout)
            current_step = 0
            update_plot(current_step)
        else:
            messagebox.showerror("Execution Error", f"Error:\n{process.stderr}")
    except Exception as e:
        messagebox.showerror("Execution Error", f"An error occurred:\n{str(e)}")

# Set up the GUI
root = tk.Tk()
root.title("Wolves and Rabbits Simulation")
root.geometry("800x600")

# Style configuration
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Helvetica", 12), padding=5)
style.configure("TLabel", font=("Helvetica", 12))
style.configure("TEntry", font=("Helvetica", 12))

# Input frame
input_frame = ttk.Frame(root, padding=10)
input_frame.pack(fill=tk.X)

# Input fields
thread_label = ttk.Label(input_frame, text="Threads:")
thread_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
thread_entry = ttk.Entry(input_frame)
thread_entry.grid(row=0, column=1, padx=5, pady=5)

steps_label = ttk.Label(input_frame, text="Steps:")
steps_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
steps_entry = ttk.Entry(input_frame)
steps_entry.grid(row=1, column=1, padx=5, pady=5)

seed_label = ttk.Label(input_frame, text="Seed:")
seed_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
seed_entry = ttk.Entry(input_frame)
seed_entry.grid(row=2, column=1, padx=5, pady=5)

# Checkbox for compilation
compile_var = tk.BooleanVar()
compile_check = ttk.Checkbutton(input_frame, text="Compile before running", variable=compile_var)
compile_check.grid(row=3, columnspan=2, pady=5)

# Buttons
button_frame = ttk.Frame(root, padding=10)
button_frame.pack(fill=tk.X)

compile_button = ttk.Button(button_frame, text="Compile", command=compile_c_program)
compile_button.pack(side=tk.LEFT, padx=5)

run_button = ttk.Button(button_frame, text="Run Simulation", command=lambda: (compile_c_program() if compile_var.get() else None) or run_simulation())
run_button.pack(side=tk.LEFT, padx=5)

prev_button = ttk.Button(button_frame, text="Previous Step", command=prev_step)
prev_button.pack(side=tk.LEFT, padx=5)

next_button = ttk.Button(button_frame, text="Next Step", command=next_step)
next_button.pack(side=tk.LEFT, padx=5)

# Output frame
output_frame = ttk.Frame(root, padding=10)
output_frame.pack(fill=tk.BOTH, expand=True)

fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=output_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Initialize global variables
grids = []
current_step = 0

# Start the GUI event loop
root.mainloop()
