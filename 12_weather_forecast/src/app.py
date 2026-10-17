"""Tkinter GUI for current weather and a seven-day forecast."""
from __future__ import annotations
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from weather_service import search_location, get_forecast, describe_weather_code, WeatherServiceError

class WeatherApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("SkyCast | Weather Forecast")
        self.root.geometry("820x650")
        self.root.minsize(700, 560)
        self.unit = tk.StringVar(value="celsius")
        self.city = tk.StringVar()
        self.status = tk.StringVar(value="Enter a city to view live weather.")
        self._build_ui()

    def _build_ui(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Title.TLabel", font=("Segoe UI", 22, "bold"))
        style.configure("Metric.TLabel", font=("Segoe UI", 12))
        style.configure("Treeview", rowheight=30, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

        outer = ttk.Frame(self.root, padding=20)
        outer.pack(fill="both", expand=True)
        ttk.Label(outer, text="SkyCast Weather", style="Title.TLabel").pack(anchor="w")
        ttk.Label(outer, text="Current conditions • 7-day outlook • Open-Meteo data").pack(anchor="w", pady=(2, 16))

        controls = ttk.Frame(outer)
        controls.pack(fill="x", pady=(0, 14))
        entry = ttk.Entry(controls, textvariable=self.city, font=("Segoe UI", 12))
        entry.pack(side="left", fill="x", expand=True, ipady=7)
        entry.bind("<Return>", lambda _event: self.refresh())
        ttk.Button(controls, text="Get forecast", command=self.refresh).pack(side="left", padx=(8, 0), ipady=5)
        ttk.Label(controls, text="Units:").pack(side="left", padx=(14, 5))
        unit_box = ttk.Combobox(controls, textvariable=self.unit, values=("celsius", "fahrenheit"),
                                state="readonly", width=11)
        unit_box.pack(side="left")
        unit_box.bind("<<ComboboxSelected>>", lambda _event: self.refresh() if self.city.get().strip() else None)

        self.location_label = ttk.Label(outer, text="No location selected", font=("Segoe UI", 14, "bold"))
        self.location_label.pack(anchor="w", pady=(2, 8))
        self.current_label = ttk.Label(outer, text="Your current conditions will appear here.",
                                       style="Metric.TLabel", justify="left")
        self.current_label.pack(anchor="w", pady=(0, 14))

        ttk.Label(outer, text="7-Day Forecast", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(2, 8))
        columns = ("date", "conditions", "min", "max", "rain", "sunrise", "sunset")
        self.table = ttk.Treeview(outer, columns=columns, show="headings", height=8)
        headings = {"date":"Date", "conditions":"Conditions", "min":"Low", "max":"High",
                    "rain":"Rain chance", "sunrise":"Sunrise", "sunset":"Sunset"}
        widths = {"date":100, "conditions":180, "min":65, "max":65, "rain":95, "sunrise":85, "sunset":85}
        for col in columns:
            self.table.heading(col, text=headings[col])
            self.table.column(col, width=widths[col], anchor="center")
        self.table.pack(fill="both", expand=True)
        ttk.Label(outer, textvariable=self.status, wraplength=760).pack(anchor="w", pady=(12, 0))

    def refresh(self):
        city = self.city.get().strip()
        if not city:
            messagebox.showinfo("City required", "Please enter a city name.")
            return
        self.status.set("Loading weather data…")
        # Network work runs on a worker thread so the GUI remains responsive.
        threading.Thread(target=self._load_weather, args=(city, self.unit.get()), daemon=True).start()

    def _load_weather(self, city: str, unit: str):
        try:
            location = search_location(city)
            forecast = get_forecast(location, unit)
            self.root.after(0, lambda: self._render(location, forecast, unit))
        except WeatherServiceError as exc:
            self.root.after(0, lambda msg=str(exc): self._show_error(msg))
        except Exception:
            # Avoid leaking implementation details to end users; detailed diagnostics belong in logs.
            self.root.after(0, lambda: self._show_error("Unexpected error. Please retry and check your connection."))

    def _render(self, location, data, unit):
        current, daily = data["current"], data["daily"]
        degree = "°C" if unit == "celsius" else "°F"
        self.location_label.config(text=f"{location.name}, {location.country}")
        self.current_label.config(text=(
            f"{describe_weather_code(current.get('weather_code'))}\n"
            f"Temperature: {current.get('temperature_2m', '—')}{degree}  |  "
            f"Feels like: {current.get('apparent_temperature', '—')}{degree}\n"
            f"Humidity: {current.get('relative_humidity_2m', '—')}%  |  "
            f"Wind: {current.get('wind_speed_10m', '—')} km/h  |  "
            f"Precipitation: {current.get('precipitation', '—')} mm"
        ))
        for item in self.table.get_children():
            self.table.delete(item)
        dates = daily.get("time", [])
        for i, day in enumerate(dates):
            code = daily.get("weather_code", [])
            low = daily.get("temperature_2m_min", [])
            high = daily.get("temperature_2m_max", [])
            rain = daily.get("precipitation_probability_max", [])
            sunrise = daily.get("sunrise", [])
            sunset = daily.get("sunset", [])
            self.table.insert("", "end", values=(
                day, describe_weather_code(code[i] if i < len(code) else None),
                f"{low[i]}{degree}" if i < len(low) else "—",
                f"{high[i]}{degree}" if i < len(high) else "—",
                f"{rain[i]}%" if i < len(rain) and rain[i] is not None else "—",
                sunrise[i][-5:] if i < len(sunrise) and sunrise[i] else "—",
                sunset[i][-5:] if i < len(sunset) and sunset[i] else "—",
            ))
        self.status.set(f"Updated for {location.timezone}. Forecast values are provided by Open-Meteo.")
    def _show_error(self, message: str):
        self.status.set(message)
        messagebox.showerror("Weather lookup failed", message)

def main():
    root = tk.Tk()
    WeatherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
