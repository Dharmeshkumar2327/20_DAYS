"""Advanced QR Code Generator - Tkinter desktop application."""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
from pathlib import Path
from PIL import Image, ImageTk
import qrcode
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
from qr_generator import QRGenerator
from history import HistoryManager
from utils import build_payload, open_file, copy_to_clipboard

DEFAULT_URL = "https://github.com/Dharmeshkumar2327"
OUT_DIR = Path("output")
OUT_DIR.mkdir(exist_ok=True)

class QRCodeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Advanced QR Code Generator")
        self.geometry("1000x680")
        self.minsize(850, 600)
        self.configure(bg="#101820")
        self.generator = QRGenerator()
        self.history = HistoryManager()
        self.current_image = None
        self.current_payload = ""
        self.fg_color = "#111111"
        self.bg_color = "#FFFFFF"
        self._build_ui()

    def _build_ui(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background="#101820")
        style.configure("TLabel", background="#101820", foreground="#F2F5F7", font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"), foreground="#FFFFFF")
        style.configure("TButton", padding=7)
        style.configure("TCombobox", padding=5)
        header = ttk.Frame(self, padding=(18, 14))
        header.pack(fill="x")
        ttk.Label(header, text="▦  Advanced QR Code Generator", style="Title.TLabel").pack(anchor="w")
        ttk.Label(header, text="Create, customize, preview, and export QR codes").pack(anchor="w", pady=(4, 0))

        main = ttk.Frame(self, padding=16)
        main.pack(fill="both", expand=True)
        left = ttk.Frame(main, padding=12)
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))
        right = ttk.Frame(main, padding=12)
        right.pack(side="right", fill="both", expand=True)

        ttk.Label(left, text="Content type").pack(anchor="w")
        self.kind = tk.StringVar(value="Website URL")
        kinds = ["Website URL", "Text", "Email", "Phone", "SMS", "Wi-Fi"]
        ttk.Combobox(left, textvariable=self.kind, values=kinds, state="readonly").pack(fill="x", pady=(4, 10))
        self.kind.trace_add("write", lambda *_: self._update_hint())
        ttk.Label(left, text="Content / destination").pack(anchor="w")
        self.content = tk.Text(left, height=5, wrap="word", font=("Consolas", 10))
        self.content.pack(fill="x", pady=(4, 4))
        self.content.insert("1.0", DEFAULT_URL)
        self.hint = ttk.Label(left, text="Use a full URL, e.g. https://example.com")
        self.hint.pack(anchor="w", pady=(0, 12))

        colors = ttk.Frame(left)
        colors.pack(fill="x", pady=(0, 10))
        ttk.Button(colors, text="Foreground color", command=self._choose_fg).pack(side="left", expand=True, fill="x", padx=(0, 5))
        ttk.Button(colors, text="Background color", command=self._choose_bg).pack(side="left", expand=True, fill="x", padx=(5, 0))
        self.color_label = ttk.Label(left, text="Foreground #111111  |  Background #FFFFFF")
        self.color_label.pack(anchor="w", pady=(0, 10))

        options = ttk.Frame(left)
        options.pack(fill="x", pady=(0, 8))
        ttk.Label(options, text="Size (pixels)").grid(row=0, column=0, sticky="w")
        self.size = tk.IntVar(value=420)
        ttk.Spinbox(options, from_=180, to=1200, increment=20, textvariable=self.size, width=10).grid(row=1, column=0, sticky="w", pady=4)
        ttk.Label(options, text="Error correction").grid(row=0, column=1, sticky="w", padx=(18, 0))
        self.correction = tk.StringVar(value="High (H)")
        ttk.Combobox(options, textvariable=self.correction, values=["Low (L)", "Medium (M)", "Quartile (Q)", "High (H)"], state="readonly", width=15).grid(row=1, column=1, sticky="w", padx=(18, 0), pady=4)
        options.columnconfigure(1, weight=1)

        ttk.Label(left, text="Optional center logo").pack(anchor="w", pady=(4, 2))
        logo_row = ttk.Frame(left)
        logo_row.pack(fill="x")
        self.logo_path = tk.StringVar()
        ttk.Entry(logo_row, textvariable=self.logo_path).pack(side="left", fill="x", expand=True)
        ttk.Button(logo_row, text="Browse", command=self._browse_logo).pack(side="left", padx=(6, 0))
        ttk.Button(left, text="Generate QR Code", command=self.generate).pack(fill="x", pady=(16, 6))
        ttk.Button(left, text="Open GitHub profile QR", command=self._generate_github).pack(fill="x")

        ttk.Label(right, text="QR Preview", style="Title.TLabel").pack(anchor="w")
        self.preview = ttk.Label(right, text="Your QR code will appear here", anchor="center")
        self.preview.pack(fill="both", expand=True, pady=10)
        actions = ttk.Frame(right)
        actions.pack(fill="x")
        ttk.Button(actions, text="Save PNG", command=lambda: self.save("png")).pack(side="left", expand=True, fill="x", padx=(0, 4))
        ttk.Button(actions, text="Save JPG", command=lambda: self.save("jpg")).pack(side="left", expand=True, fill="x", padx=4)
        ttk.Button(actions, text="Save SVG", command=lambda: self.save("svg")).pack(side="left", expand=True, fill="x", padx=(4, 0))
        ttk.Button(right, text="Copy destination", command=self.copy_destination).pack(fill="x", pady=(8, 0))
        ttk.Label(right, text="Recent history").pack(anchor="w", pady=(16, 4))
        self.history_list = tk.Listbox(right, height=5, bg="#18232D", fg="#F2F5F7", selectbackground="#246BCE", borderwidth=0)
        self.history_list.pack(fill="x")
        self.history_list.bind("<<ListboxSelect>>", self._load_history)
        self._refresh_history()

    def _update_hint(self):
        hints = {
            "Website URL": "Use a full URL, e.g. https://example.com",
            "Text": "Any text, note, or short message",
            "Email": "Enter an email address; an email draft will open when scanned",
            "Phone": "Enter a phone number including country code if needed",
            "SMS": "Enter a phone number; scanner may open an SMS draft",
            "Wi-Fi": "Format: SSID;PASSWORD;WPA  (use WPA, WEP, or nopass)"
        }
        self.hint.configure(text=hints.get(self.kind.get(), ""))

    def _choose_fg(self):
        c = colorchooser.askcolor(color=self.fg_color, title="Choose QR foreground")
        if c and c[1]:
            self.fg_color = c[1]
            self._update_color_label()

    def _choose_bg(self):
        c = colorchooser.askcolor(color=self.bg_color, title="Choose QR background")
        if c and c[1]:
            self.bg_color = c[1]
            self._update_color_label()

    def _update_color_label(self):
        self.color_label.configure(text=f"Foreground {self.fg_color}  |  Background {self.bg_color}")

    def _browse_logo(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.webp")])
        if path:
            self.logo_path.set(path)

    def _get_payload(self):
        raw = self.content.get("1.0", "end").strip()
        return build_payload(self.kind.get(), raw)

    def _correction_value(self):
        return {
            "Low (L)": ERROR_CORRECT_L,
            "Medium (M)": ERROR_CORRECT_M,
            "Quartile (Q)": ERROR_CORRECT_Q,
            "High (H)": ERROR_CORRECT_H,
        }[self.correction.get()]

    def generate(self):
        try:
            payload = self._get_payload()
            img = self.generator.generate(
                payload, size=int(self.size.get()), fill_color=self.fg_color,
                back_color=self.bg_color, error_correction=self._correction_value(),
                logo_path=self.logo_path.get().strip() or None
            )
            self.current_image = img
            self.current_payload = payload
            display = img.copy()
            display.thumbnail((380, 380))
            self._preview_image = ImageTk.PhotoImage(display)
            self.preview.configure(image=self._preview_image, text="")
            self.history.add(self.kind.get(), payload)
            self._refresh_history()
        except Exception as exc:
            messagebox.showerror("Could not generate QR code", str(exc))

    def _generate_github(self):
        self.kind.set("Website URL")
        self.content.delete("1.0", "end")
        self.content.insert("1.0", DEFAULT_URL)
        self.generate()

    def save(self, fmt):
        if self.current_image is None:
            messagebox.showinfo("Generate first", "Generate a QR code before saving.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=f".{fmt}",
            filetypes=[(f"{fmt.upper()} files", f"*.{fmt}")],
            initialfile=f"qr_code.{fmt}"
        )
        if not path:
            return
        try:
            self.generator.save(self.current_image, path, fmt=fmt,
                                payload=self.current_payload,
                                fill_color=self.fg_color, back_color=self.bg_color,
                                error_correction=self._correction_value())
            messagebox.showinfo("Saved", f"QR code saved to:\n{path}")
        except Exception as exc:
            messagebox.showerror("Save failed", str(exc))

    def copy_destination(self):
        if not self.current_payload:
            messagebox.showinfo("Generate first", "Generate a QR code first.")
            return
        copy_to_clipboard(self, self.current_payload)
        messagebox.showinfo("Copied", "QR destination copied to clipboard.")

    def _refresh_history(self):
        self.history_list.delete(0, "end")
        for item in self.history.items()[:10]:
            self.history_list.insert("end", f'{item["kind"]}: {item["payload"][:55]}')

    def _load_history(self, _event=None):
        selection = self.history_list.curselection()
        if not selection:
            return
        items = self.history.items()
        item = items[selection[0]]
        self.kind.set(item["kind"])
        self.content.delete("1.0", "end")
        self.content.insert("1.0", item["payload"])

if __name__ == "__main__":
    QRCodeApp().mainloop()
