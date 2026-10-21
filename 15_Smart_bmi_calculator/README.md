# Smart BMI Calculator Pro 🧮

An interactive command-line Body Mass Index (BMI) calculator built with Python. It supports metric and imperial measurements, validates input, displays a color-coded BMI scale, and prints a readable report.

## ✨ Features

- **Metric and imperial units** — kilograms/centimetres or pounds/feet/inches
- **BMI calculation** — calculates BMI using weight and height
- **BMI categories** — underweight, normal weight, overweight, and obesity
- **Color-coded terminal output** — clearer report in supported terminals
- **Visual BMI scale** — shows the approximate position of the result
- **Reference weight range** — estimates the adult BMI 18.5–24.9 range for the entered height
- **Input validation** — handles invalid numbers and non-positive measurements
- **Repeat calculations** — calculate BMI for multiple people in one run
- **No external dependencies** — uses only the Python standard library

## 🖥️ Requirements

- Python 3.10 or later (type annotations use built-in generic types)
- A terminal or IDE such as VS Code, PyCharm, or IDLE

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/smart-bmi-calculator-pro.git
cd smart-bmi-calculator-pro
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Run the program

```bash
python smart_bmi_calculator_pro.py
```

If your system uses `python3`, run:

```bash
python3 smart_bmi_calculator_pro.py
```

### 3. Follow the prompts

Choose metric or imperial units, enter your measurements, and read the BMI report.

## 📂 Project Structure

```text
smart-bmi-calculator-pro/
├── smart_bmi_calculator_pro.py   # Main application
├── README.md                     # Project overview and setup instructions
├── LICENSE                       # MIT license
├── .gitignore                    # Files Git should ignore
├── requirements.txt              # No third-party dependencies
└── screenshots/
    └── README.md                 # Notes for adding screenshots
```

## 🧠 Formula

BMI is calculated as:

\[
BMI = \frac{\text{weight in kilograms}}{(\text{height in metres})^2}
\]

For imperial input, the program converts pounds to kilograms and inches to metres before calculating BMI.

## 📊 Adult BMI Categories

| BMI | Category |
|---:|---|
| Below 18.5 | Underweight |
| 18.5 to below 25.0 | Normal weight |
| 25.0 to below 30.0 | Overweight |
| 30.0 or above | Obesity |

These are commonly used adult screening categories. They are not a diagnosis and may not be appropriate for children, teens, pregnancy, or some athletes.

## 🧪 Example

```text
Choose your measurement system:
  [1] Metric   — kilograms and centimetres
  [2] Imperial — pounds, feet and inches
Enter 1 or 2: 1
Weight (kg): 70
Height (cm): 175

Your BMI: 22.9
Category: Normal weight
```

The exact display includes a visual scale and additional context.

## 🛠️ Technologies Used

- Python
- Functions and modular design
- Input validation and exception handling
- String formatting
- ANSI terminal colors
- Standard library (`os`, `sys`)

## 🔮 Future Improvements

- Add a graphical user interface with Tkinter or Streamlit
- Save reports to CSV
- Add unit tests
- Add optional BMI history tracking
- Add a web version

## ⚠️ Disclaimer

This project is for educational and general informational purposes only. BMI is a screening measure, not a diagnosis, and does not directly measure body fat or overall health. Consult a qualified healthcare professional for personal medical advice.

## 📄 License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for details.
