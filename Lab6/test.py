
import os
import subprocess
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import LogLocator

# Default parameters
default_threads = [1, 2, 4, 8, 16]
default_steps = [10, 100, 1000, 10000]

# Function to run the simulation
def run_simulation(threads, steps):
    results = []
    for t in threads:
        for s in steps:
            result = subprocess.run(
                ["./wolves_rabbits_simulation", str(t), str(s), "42"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            time = 0.0
            for line in result.stdout.splitlines():
                if "Execution time:" in line:
                    time = float(line.split(":")[-1].strip().split()[0])
            results.append({"Threads": t, "Steps": s, "Time": time})
    return results

# Plot results
def plot_results(results):
    df = pd.DataFrame(results)
    plt.figure(figsize=(10, 6))
    for t in df["Threads"].unique():
        subset = df[df["Threads"] == t]
        plt.plot(subset["Steps"], subset["Time"], marker='o', label=f"{t} Threads")
    
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Number of Steps")
    plt.ylabel("Execution Time (s)")
    plt.title("Execution Time vs Steps for Different Thread Counts")
    plt.legend()
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.tight_layout()
    plt.savefig("execution_time_plot.png")
    plt.show()

# Generate LaTeX table
def generate_latex_table(results):
    df = pd.DataFrame(results)
    table = df.pivot(index="Steps", columns="Threads", values="Time")
    table.to_latex("results_table.tex", float_format="%.3f")

# Main script
if __name__ == "__main__":
    # Run simulation
    if not os.path.exists("wolves_rabbits_simulation"):
        subprocess.run(["gcc", "wolves_rabbits_simulation.c", "-o", "wolves_rabbits_simulation", "-fopenmp"])
    results = run_simulation(default_threads, default_steps)
    
    # Plot and save results
    plot_results(results)
    
    # Generate LaTeX table
    generate_latex_table(results)
