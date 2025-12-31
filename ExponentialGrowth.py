import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import math

# -----------------------
# Dollar formatting helper
# -----------------------
def format_dollars(value):
    if value < 1e6:
        return f"${value:,.2f}"
    else:
        return f"${value:.2e}"

# -----------------------
# Matplotlib GIF-friendly style
# -----------------------
plt.ion()
plt.rcParams.update({
    "figure.figsize": (4, 3),
    "figure.dpi": 150,
    "axes.titlesize": 16,
    "axes.labelsize": 14,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "lines.linewidth": 3,
    "lines.markersize": 8,
})

# -----------------------
# Global animation state
# -----------------------
current_step = 0
x = []
y_values = []
mode = "raw"

fig = None
ax = None
line = None

# -----------------------
# Tkinter setup
# -----------------------
root = tk.Tk()
root.title("Exponential Growth Demo")

# -----------------------
# Input fields
# -----------------------
ttk.Label(root, text="Initial Amount ($):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
initial_entry = ttk.Entry(root)
initial_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(root, text="Growth Factor:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
factor_entry = ttk.Entry(root)
factor_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(root, text="Number of Steps:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
steps_entry = ttk.Entry(root)
steps_entry.grid(row=2, column=1, padx=5, pady=5)

# -----------------------
# Speed slider
# -----------------------
ttk.Label(root, text="Step Speed (ms):").grid(row=3, column=0, sticky="w", padx=5, pady=5)

speed_slider = ttk.Scale(root, from_=100, to=2000, orient="horizontal")
speed_slider.set(500)
speed_slider.grid(row=3, column=1, padx=5, pady=5)

# -----------------------
# Output text
# -----------------------
output_text = tk.Text(
    root,
    height=8,
    width=40,
    font=("Courier New", 14)
)
output_text.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# -----------------------
# Status label
# -----------------------
status_label = ttk.Label(root, text="", foreground="blue")
status_label.grid(row=6, column=0, columnspan=2)

# -----------------------
# Core logic
# -----------------------
def start_animation():
    global current_step, x, y_values, mode, fig, ax, line

    output_text.delete("1.0", tk.END)
    current_step = 0

    try:
        initial = float(initial_entry.get())
        factor = float(factor_entry.get())
        steps = int(steps_entry.get())

        if initial <= 0 or factor <= 0:
            raise ValueError

        x = list(range(steps + 1))
        y_values = []
        mode = "raw"

        for n in x:
            value = initial * (factor ** n)
            if value > 1e308:
                raise OverflowError
            y_values.append(value)

    except OverflowError:
        mode = "log"
        log_initial = math.log10(initial)
        log_factor = math.log10(factor)
        y_values = [log_initial + n * log_factor for n in x]

    except ValueError:
        status_label.config(text="Invalid input. Values must be positive.")
        return

    status_label.config(
        text="Showing raw dollar values" if mode == "raw"
        else "Values too large → showing log₁₀(dollars)"
    )

    fig, ax = plt.subplots()
    line, = ax.plot([], [], marker='o')

    ax.set_xlabel("Step")
    ax.set_ylabel("Dollars ($)" if mode == "raw" else "log₁₀(Dollars)")
    ax.set_title("Exponential Growth")
    ax.grid(True)

    ax.set_xlim(0, x[-1])

    if mode == "raw":
        ax.set_ylim(0, max(y_values))
    else:
        ax.set_ylim(min(y_values), max(y_values))

    plt.show()
    print_next_step()

def print_next_step():
    global current_step

    if current_step >= len(x):
        return

    if mode == "raw":
        text = f"Step {current_step}: {format_dollars(y_values[current_step])}\n"
    else:
        text = f"Step {current_step}: value ≈ $10^{y_values[current_step]:.2f}\n"

    output_text.insert(tk.END, text)
    output_text.see(tk.END)

    line.set_data(x[:current_step + 1], y_values[:current_step + 1])
    fig.canvas.draw()
    fig.canvas.flush_events()

    current_step += 1
    delay = int(speed_slider.get())
    root.after(delay, print_next_step)

# -----------------------
# Start button
# -----------------------
start_button = ttk.Button(root, text="Start Animation", command=start_animation)
start_button.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()