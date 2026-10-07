"""Tkinter GUI for testing internet download speed, upload speed, and ping."""

import threading
import tkinter as tk
from tkinter import ttk, messagebox

import speedtest


class SpeedTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Test Internet Speed")
        self.root.geometry("380x260")
        self.root.resizable(False, False)

        tk.Label(
            root,
            text="TEST INTERNET SPEED",
            bg="#ffffff",
            fg="#404042",
            font=("Arial", 23, "bold"),
        ).pack(fill="x", pady=(8, 0))

        root.configure(bg="#ffffff")

        self.down_label = tk.Label(
            root, text="⏬ Download Speed - ", bg="#ffffff",
            font=("Arial", 10, "bold")
        )
        self.down_label.place(x=90, y=55)

        self.up_label = tk.Label(
            root, text="⏫ Upload Speed - ", bg="#ffffff",
            font=("Arial", 10, "bold")
        )
        self.up_label.place(x=90, y=85)

        self.ping_label = tk.Label(
            root, text="Your Ping - ", bg="#ffffff",
            font=("Arial", 10, "bold")
        )
        self.ping_label.place(x=90, y=115)

        self.progress = ttk.Progressbar(
            root, orient="horizontal", length=210, mode="indeterminate"
        )
        self.progress.place(x=85, y=145)
        self.progress.place_forget()

        self.button = tk.Button(
            root,
            text="Check Speed ▶",
            width=30,
            bd=0,
            bg="#404042",
            fg="#ffffff",
            pady=5,
            command=self.start_test,
        )
        self.button.place(x=85, y=175)

        tk.Label(
            root, text="Internet Speed Tester",
            bg="#ffffff", fg="#404042",
            font=("Arial", 10)
        ).place(x=125, y=225)

    def start_test(self):
        self.button.config(state="disabled")
        self.progress.place(x=85, y=145)
        self.progress.start(10)

        thread = threading.Thread(target=self.run_test, daemon=True)
        thread.start()

    def run_test(self):
        try:
            st = speedtest.Speedtest()
            download = round(st.download() / 1_000_000, 2)
            upload = round(st.upload() / 1_000_000, 2)

            st.get_servers([])
            ping = round(st.results.ping, 2)

            self.root.after(
                0, self.show_result, download, upload, ping, None
            )
        except Exception as error:
            self.root.after(0, self.show_result, None, None, None, error)

    def show_result(self, download, upload, ping, error):
        self.progress.stop()
        self.progress.place_forget()
        self.button.config(state="normal")

        if error:
            messagebox.showerror("Speed Test Error", str(error))
            return

        self.down_label.config(
            text=f"⏬ Download Speed - {download} Mbps"
        )
        self.up_label.config(
            text=f"⏫ Upload Speed - {upload} Mbps"
        )
        self.ping_label.config(
            text=f"Your Ping - {ping} ms"
        )


def main():
    root = tk.Tk()
    app = SpeedTestApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
