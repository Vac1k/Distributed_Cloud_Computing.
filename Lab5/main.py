
import os
import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter.ttk import Label, Button, Entry, Checkbutton, Style

# Створення вікна
root = tk.Tk()
root.title("Run C Programs")
root.geometry("600x500")

# Застосування теми Darcula
style = Style()
style.theme_use('clam')
style.configure("TLabel", background="#282C34", foreground="#ABB2BF", font=("Courier", 12))
style.configure("TButton", background="#61AFEF", foreground="#FFFFFF", font=("Courier", 12))
style.configure("TEntry", fieldbackground="#282C34", foreground="#ABB2BF", font=("Courier", 12))
style.configure("TCheckbutton", background="#282C34", foreground="#ABB2BF", font=("Courier", 12))

root.configure(bg="#282C34")

# Імена програм
programs = {"Program 1": "1", "Program 2": "2"}

# Функція для компіляції
def compile_program(program):
    try:
        subprocess.run(["gcc", "-Xpreprocessor", "-fopenmp", "-I/opt/homebrew/opt/libomp/include",
                        "-L/opt/homebrew/opt/libomp/lib", "-lomp", f"{program}.c", "-o", program], check=True)
        messagebox.showinfo("Success", f"{program}.c compiled successfully!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Compilation of {program}.c failed: {e}")

# Функція для запуску програми
def run_program():
    selected_program = program_var.get()
    program_name = programs[selected_program]

    num_threads = threads_entry.get()
    num_samples = samples_entry.get()

    if not num_threads.isdigit() or not num_samples.isdigit():
        messagebox.showerror("Input Error", "Please enter valid numeric values for threads and samples.")
        return

    if compile_var.get() or not os.path.exists(program_name):
        compile_program(program_name)

    if os.path.exists(program_name):
        try:
            result = subprocess.run([f"./{program_name}", num_threads, num_samples], capture_output=True, text=True)
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, result.stdout)
        except Exception as e:
            messagebox.showerror("Error", f"Execution of {program_name} failed: {e}")

# Інтерфейс
Label(root, text="Select Program:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
program_var = tk.StringVar(value="Program 1")
program_menu = tk.OptionMenu(root, program_var, *programs.keys())
program_menu.grid(row=0, column=1, padx=10, pady=10)

Label(root, text="Number of Threads:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
threads_entry = Entry(root, width=20)
threads_entry.grid(row=1, column=1, padx=10, pady=10)

Label(root, text="Number of Samples:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
samples_entry = Entry(root, width=20)
samples_entry.grid(row=2, column=1, padx=10, pady=10)

compile_var = tk.BooleanVar()
Checkbutton(root, text="Compile before run", variable=compile_var).grid(row=3, column=0, columnspan=2, pady=10)

Button(root, text="Run Program", command=run_program).grid(row=4, column=0, columnspan=2, pady=10)

Label(root, text="Output:").grid(row=5, column=0, columnspan=2, pady=10, sticky="w")
output_text = tk.Text(root, height=10, width=70, bg="#1E2127", fg="#ABB2BF", font=("Courier", 12))
output_text.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
