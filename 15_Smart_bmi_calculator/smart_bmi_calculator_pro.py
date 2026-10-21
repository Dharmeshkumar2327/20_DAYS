"""
Smart BMI Calculator Pro
-----------------------
An interactive BMI calculator with metric/imperial input, validation,
a color-coded BMI scale, and a simple text report.

Run:
    python smart_bmi_calculator_pro.py

Uses only the Python standard library.
"""

from __future__ import annotations

import os
import sys


USE_COLOR = sys.stdout.isatty() and "NO_COLOR" not in os.environ


class Style:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    CYAN = "\033[96m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[95m"


def paint(text: str, color: str) -> str:
    """Apply terminal color when supported."""
    return f"{color}{text}{Style.RESET}" if USE_COLOR else text


def line(char: str = "─", width: int = 62) -> str:
    return char * width


def show_header() -> None:
    print()
    print(paint("╔" + "═" * 60 + "╗", Style.CYAN))
    print(paint("║" + " " * 18 + "SMART BMI CALCULATOR PRO" + " " * 18 + "║", Style.CYAN + Style.BOLD))
    print(paint("║" + " " * 12 + "Your personal wellness snapshot" + " " * 17 + "║", Style.CYAN))
    print(paint("╚" + "═" * 60 + "╝", Style.CYAN))
    print(paint("A simple guide to understanding your Body Mass Index", Style.DIM))
    print()


def get_number(prompt: str, minimum: float = 0.0) -> float:
    """Prompt until the user enters a number greater than minimum."""
    while True:
        try:
            value = float(input(prompt).strip())
        except ValueError:
            print(paint("  Enter a valid number, for example 65 or 1.72.", Style.YELLOW))
            continue

        if value <= minimum:
            print(paint(f"  Value must be greater than {minimum}. Try again.", Style.YELLOW))
            continue
        return value


def get_choice(prompt: str, choices: set[str]) -> str:
    """Prompt until a valid option is selected."""
    while True:
        choice = input(prompt).strip().lower()
        if choice in choices:
            return choice
        print(paint(f"  Choose one of: {', '.join(sorted(choices))}", Style.YELLOW))


def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculate BMI from weight in kilograms and height in metres."""
    if weight_kg <= 0 or height_m <= 0:
        raise ValueError("Weight and height must be greater than zero.")
    return weight_kg / (height_m ** 2)


def get_bmi_category(bmi: float) -> tuple[str, str, str]:
    """Return the adult BMI category, color, and general guidance."""
    if bmi < 18.5:
        return (
            "Underweight",
            Style.BLUE,
            "Consider discussing nutrition and weight goals with a healthcare professional.",
        )
    if bmi < 25.0:
        return (
            "Normal weight",
            Style.GREEN,
            "Your BMI is within the commonly used healthy adult range.",
        )
    if bmi < 30.0:
        return (
            "Overweight",
            Style.YELLOW,
            "Sustainable lifestyle habits can support overall health.",
        )
    return (
        "Obesity",
        Style.RED,
        "Consider discussing your overall health with a healthcare professional.",
    )


def bmi_scale(bmi: float, width: int = 40) -> str:
    """Create a compact color-coded scale and mark the BMI position."""
    segments = [
        (0.0, 18.5, "░", Style.BLUE),
        (18.5, 25.0, "▒", Style.GREEN),
        (25.0, 30.0, "▓", Style.YELLOW),
        (30.0, 40.0, "█", Style.RED),
    ]
    marker_pos = min(width - 1, max(0, int(min(bmi, 40.0) / 40.0 * width)))
    chars = []
    for i in range(width):
        value = (i + 0.5) / width * 40.0
        for low, high, char, color in segments:
            if low <= value < high:
                chars.append(paint(char, color))
                break
    chars[marker_pos] = paint("▲", Style.BOLD + Style.MAGENTA)
    return "".join(chars)


def read_measurements() -> tuple[float, float, str]:
    """Read measurements and convert them to kilograms and metres."""
    print(paint("Choose your measurement system:", Style.BOLD))
    print("  [1] Metric   — kilograms and centimetres")
    print("  [2] Imperial — pounds, feet and inches")
    choice = get_choice("Enter 1 or 2: ", {"1", "2"})

    if choice == "1":
        weight_kg = get_number("Weight (kg): ")
        height_cm = get_number("Height (cm): ")
        if not 50 <= height_cm <= 260:
            print(paint("  This height is unusual for an adult; please check it.", Style.YELLOW))
            if get_choice("Use this height anyway? (y/n): ", {"y", "n"}) == "n":
                return read_measurements()
        return weight_kg, height_cm / 100, "Metric"

    weight_lb = get_number("Weight (lb): ")
    feet = get_number("Height — feet: ", minimum=-1)
    inches = get_number("Additional inches (0–11): ", minimum=-1)
    if inches >= 12:
        print(paint("  Inches must be less than 12. Please enter the measurements again.", Style.YELLOW))
        return read_measurements()

    total_inches = feet * 12 + inches
    if total_inches <= 0:
        print(paint("  Total height must be greater than zero. Please try again.", Style.YELLOW))
        return read_measurements()

    return weight_lb * 0.45359237, total_inches * 0.0254, "Imperial"


def show_results(weight_kg: float, height_m: float, units: str) -> None:
    """Print BMI, category, scale, reference weight range, and disclaimer."""
    bmi = calculate_bmi(weight_kg, height_m)
    category, color, message = get_bmi_category(bmi)
    healthy_min = 18.5 * height_m ** 2
    healthy_max = 24.9 * height_m ** 2

    print()
    print(paint(line("═"), Style.CYAN))
    print(paint("                    YOUR BMI REPORT", Style.BOLD + Style.CYAN))
    print(paint(line("═"), Style.CYAN))
    print(f"  Measurement system : {units}")
    print(f"  Weight             : {weight_kg:.1f} kg")
    print(f"  Height             : {height_m:.2f} m")
    print()
    print(f"  Your BMI           : {paint(f'{bmi:.1f}', Style.BOLD + color)}")
    print(f"  Category           : {paint(category, Style.BOLD + color)}")
    print()
    print(paint("  BMI scale (marker = your result)", Style.BOLD))
    print("  " + bmi_scale(bmi))
    print("  0       18.5          25          30          40+")
    print()
    print(paint("  Reference healthy-weight range for your height:", Style.BOLD))
    print(f"  {healthy_min:.1f}–{healthy_max:.1f} kg")
    print()
    print(paint("  Wellness note:", Style.BOLD))
    print(f"  {message}")
    print()
    print(paint("  Important:", Style.BOLD + Style.MAGENTA))
    print("  BMI is a screening tool, not a diagnosis, and does not measure body fat directly.")
    print("  It may not be suitable for children, teens, pregnancy, or some athletes.")
    print(paint(line(), Style.CYAN))
    print()


def main() -> None:
    show_header()
    print("For general information only; designed for adults.")
    print()

    while True:
        try:
            weight_kg, height_m, units = read_measurements()
            show_results(weight_kg, height_m, units)
        except (KeyboardInterrupt, EOFError):
            print("\n\nThanks for using Smart BMI Calculator Pro. Stay well!")
            break

        if get_choice("Calculate BMI again? (y/n): ", {"y", "n"}) == "n":
            print(paint("\nThanks for using Smart BMI Calculator Pro. Stay well!", Style.CYAN + Style.BOLD))
            break
        print()


if __name__ == "__main__":
    main()
