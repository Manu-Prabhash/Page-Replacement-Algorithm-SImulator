import tkinter as tk
from tkinter import scrolledtext
import tkinter.font as font

def simulate_page_replacement(pages, frame_size, algorithm):
    """Simulates page replacement algorithms (FCFS, OPR, LRU)."""
    if algorithm == "FCFS":
        return fcfs(pages, frame_size)
    elif algorithm == "OPR":
        return optimal(pages, frame_size)
    elif algorithm == "LRU":
        return lru(pages, frame_size)
    else:
        return None, None

def fcfs(pages, frame_size):
    """Simulates the FCFS (FIFO) page replacement algorithm."""
    frames = []
    page_faults = 0
    frame_states = []
    frame_queue = []

    for page in pages:
        if page not in frames:
            page_faults += 1
            if len(frames) < frame_size:
                frames.append(page)
                frame_queue.append(page)
            else:
                replaced_page = frame_queue.pop(0)
                frames[frames.index(replaced_page)] = page
                frame_queue.append(page)
        frame_states.append(frames[:])
    return page_faults, frame_states

def lru(pages, frame_size):
    """Simulates the LRU page replacement algorithm."""
    frames = []
    page_faults = 0
    frame_states = []
    last_used = {}

    for i, page in enumerate(pages):
        if page not in frames:
            page_faults += 1
            if len(frames) < frame_size:
                frames.append(page)
            else:
                lru_page = min(frames, key=lambda p: last_used.get(p, -1))
                frames[frames.index(lru_page)] = page
        last_used[page] = i
        frame_states.append(frames[:])
    return page_faults, frame_states

def optimal(pages, frame_size):
    """Simulates the Optimal page replacement algorithm."""
    frames = []
    page_faults = 0
    frame_states = []

    for i, page in enumerate(pages):
        if page not in frames:
            page_faults += 1
            if len(frames) < frame_size:
                frames.append(page)
            else:
                future_use = {}
                for f_page in frames:
                    try:
                        future_use[f_page] = pages[i + 1:].index(f_page)
                    except ValueError:
                        future_use[f_page] = float('inf')
                optimal_page = max(future_use, key=future_use.get)
                frames[frames.index(optimal_page)] = page
        frame_states.append(frames[:])
    return page_faults, frame_states

def run_simulation(algorithm):
    """Runs the simulation and displays the results."""
    try:
        frames_input = int(frames_entry.get())
        pages_input = [int(p.strip()) for p in sequence_entry.get().split(',')]
    except ValueError:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Invalid input. Please enter valid numbers.")
        return

    faults, states = simulate_page_replacement(pages_input, frames_input, algorithm)

    result_text.delete(1.0, tk.END)
    if faults is not None:
        result_text.insert(tk.END, f"{algorithm} Algorithm:\n")
        result_text.insert(tk.END, f"Page Faults: {faults}\n")
        result_text.insert(tk.END, "Frame States:\n")
        for state in states:
            result_text.insert(tk.END, f"{state}\n")
    else:
        result_text.insert(tk.END, "Invalid Algorithm")

def reset_fields():
    """Resets the input fields and result text."""
    frames_entry.delete(0, tk.END)
    sequence_entry.delete(0, tk.END)
    result_text.delete(1.0, tk.END)

# Main window setup
window = tk.Tk()
window.title("Simulator")
window.geometry("500x600")
bg_color = "#282c34"
window.configure(bg=bg_color)

roboto_font = font.Font(family="Roboto", size=12)

# Title
title_label = tk.Label(window, text="Simulator", font=font.Font(family="Roboto", size=24), fg="white", bg=bg_color)
title_label.grid(row=0, column=0, columnspan=4, pady=20, sticky="ew")

# Number of Frames input
frames_label = tk.Label(window, text="Enter Number of Frames", font=roboto_font, fg="white", bg=bg_color)
frames_label.grid(row=1, column=0, pady=5, sticky="e")
frames_entry = tk.Entry(window, font=roboto_font, bg="white", width=20)
frames_entry.grid(row=1, column=1, pady=5, sticky="w")

# Page Sequence input
sequence_label = tk.Label(window, text="Enter The Page Sequence", font=roboto_font, fg="white", bg=bg_color)
sequence_label.grid(row=2, column=0, pady=5, sticky="e")
sequence_entry = tk.Entry(window, font=roboto_font, bg="white", width=20)
sequence_entry.grid(row=2, column=1, pady=5, sticky="w")

# Buttons
button_width = 60
button_height = 30
button_color = "#e53935"

tk.Button(window, text="FCFS", command=lambda: run_simulation("FCFS"), width=8, height=2).grid(row=3, column=0, pady=20)
tk.Button(window, text="OPR", command=lambda: run_simulation("OPR"), width=8, height=2).grid(row=3, column=1, pady=20)
tk.Button(window, text="LRU", command=lambda: run_simulation("LRU"), width=8, height=2).grid(row=3, column=2, pady=20)
tk.Button(window, text="RESET", command=reset_fields, width=8, height=2).grid(row=3, column=3, pady=20)

# Result display
result_text = scrolledtext.ScrolledText(window, height=10, width=50, font=roboto_font, bg=bg_color, fg="white")
result_text.grid(row=4, column=0, columnspan=4, pady=20, sticky="nsew")

# Configure grid weights
for i in range(4):
    window.grid_columnconfigure(i, weight=1)
window.grid_rowconfigure(4, weight=1)

window.mainloop()