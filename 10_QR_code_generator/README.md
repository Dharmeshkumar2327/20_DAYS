# Advanced QR Code Generator (Python)

A desktop mini-project that creates customizable QR codes for websites, text, email, phone numbers, SMS, and Wi-Fi credentials. It includes a Tkinter GUI, logo support, PNG/JPG/SVG export, input validation, and a local generation history.

**Default destination:** [Dharmeshkumar2327 on GitHub](https://github.com/Dharmeshkumar2327)

## GitHub profile QR code

A ready-to-scan QR image pointing to the author profile is included at `assets/github_profile_qr.png`. Scan it with a phone camera to open the GitHub profile. The desktop app can also generate this QR code from its **Open GitHub profile QR** button.

## Features

- User-friendly desktop GUI built with Tkinter/ttk
- QR codes for URLs, text, email, phone, SMS, and Wi-Fi
- Foreground/background color selection
- Adjustable output size and error-correction level
- Optional center logo
- Export as PNG, JPG, or SVG
- JSON-backed recent history
- Validation and unit tests
- Modular code separated into UI, QR logic, history, and utilities

## Requirements

- Python 3.10 or newer recommended
- `qrcode[pil]`
- `Pillow`
- Tkinter (usually included with standard Python installations; Linux may require installing the OS package `python3-tk`)

## Quick start

### 1. Clone the repository

Replace `YOUR_USERNAME` with your GitHub username if you publish under another account.

```bash
git clone https://github.com/Dharmeshkumar2327/advanced-qr-code-generator.git
cd advanced-qr-code-generator
```

Or download this project ZIP and extract it.

### 2. Create a virtual environment (recommended)

**Windows PowerShell**
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the app

```bash
python app.py
```

Click **Open GitHub profile QR** to generate a QR code pointing to the configured GitHub profile.

## Wi-Fi format

Enter Wi-Fi data as:

```text
NETWORK_NAME;PASSWORD;WPA
```

For an open network, use `NETWORK_NAME;;nopass`. Be careful when sharing Wi-Fi QR codes because they can reveal network credentials.

## Run tests

From the project root:

```bash
python -m unittest discover -s tests -v
```

## Project structure

```text
advanced-qr-code-generator/
├── app.py
├── qr_generator.py
├── history.py
├── utils.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── assets/
│   └── github_profile_qr.png
├── data/
├── output/
└── tests/
    └── test_utils.py
```

## How to upload to GitHub

1. Create a new **public** repository named `advanced-qr-code-generator` on GitHub. Do not initialize it with a README if you plan to push this folder as-is.
2. Open a terminal in the extracted project folder.
3. Run:

```bash
git init
git add .
git commit -m "Build advanced Python QR code generator"
git branch -M main
git remote add origin https://github.com/Dharmeshkumar2327/advanced-qr-code-generator.git
git push -u origin main
```

If Git asks you to authenticate, complete GitHub's normal sign-in/token flow. Never put passwords or access tokens in source code.

## Limitations and notes

- SVG export recreates the QR pattern from the payload; the optional center logo is included in raster output, not SVG.
- A logo can reduce scannability. High error correction helps, but always test the final code with multiple phone cameras.
- Some scanner apps handle `tel:`, `mailto:`, `SMSTO:`, and Wi-Fi payloads differently.
- The history file is local to the computer and is not uploaded to GitHub.
- Do not encode passwords, private links, or sensitive information into a publicly shared QR code.

## Future enhancements

- Gradient colors and drag-and-drop logo placement
- Batch generation from CSV
- QR code decoding and validation
- Browser-based deployment with Streamlit
- Packaging as a Windows executable

## Author

**Dharmesh Kumar**

Educational mini-project for practicing Python GUI development, modular programming, validation, file export, and unit testing.
