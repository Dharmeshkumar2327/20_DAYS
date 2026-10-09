"""A simple GUI stopwatch built with Python and Tkinter."""

import time
import tkinter as tk
from tkinter import ttk


class StopwatchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Stopwatch")
        self.root.geometry("440x300")
        self.root.resizable(False, False)

        self.running = False
        self.start_time = 0.0
        self.elapsed_time = 0.0
        self.after_id = None

        self.root.configure(bg="#1e1e2f")

        tk.Label(
            root,
            text="PYTHON STOPWATCH",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#1e1e2f",
        ).pack(pady=(24, 12))

        self.display = tk.Label(
            root,
            text="00:00.00",
            font=("Consolas", 38, "bold"),
            fg="#00ffcc",
            bg="#1e1e2f",
        )
        self.display.pack(pady=12)

        buttons = tk.Frame(root, bg="#1e1e2f")
        buttons.pack(pady=18)

        ttk.Button(buttons, text="Start", command=self.start).grid(
            row=0, column=0, padx=6
        )
        ttk.Button(buttons, text="Stop", command=self.stop).grid(
            row=0, column=1, padx=6
        )
        ttk.Button(buttons, text="Reset", command=self.reset).grid(
            row=0, column=2, padx=6
        )

        tk.Label(
            root,
            text="Start • Stop • Reset",
            font=("Arial", 10),
            fg="#c8c8d8",
            bg="#1e1e2f",
        ).pack(pady=(4, 0))

        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def format_time(self, seconds):
        minutes = int(seconds // 60)
        whole_seconds = int(seconds % 60)
        centiseconds = int((seconds * 100) % 100)
        return f"{minutes:02d}:{whole_seconds:02d}.{centiseconds:02d}"

    def refresh_display(self):
        if self.running:
            elapsed = self.elapsed_time + (time.perf_counter() - self.start_time)
            self.display.config(text=self.format_time(elapsed))
            self.after_id = self.root.after(10, self.refresh_display)

    def start(self):
        if not self.running:
            self.start_time = time.perf_counter()
            self.running = True
            self.refresh_display()

    def stop(self):
        if self.running:
            self.elapsed_time += time.perf_counter() - self.start_time
            self.running = False
            if self.after_id is not None:
                self.root.after_cancel(self.after_id)
                self.after_id = None
            self.display.config(text=self.format_time(self.elapsed_time))

    def reset(self):
        self.running = False
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self.start_time = 0.0
        self.elapsed_time = 0.0
        self.display.config(text="00:00.00")

    def close(self):
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
        self.root.destroy()


if __name__ == "__main__":
    window = tk.Tk()
    app = StopwatchApp(window)
    window.mainloop()
