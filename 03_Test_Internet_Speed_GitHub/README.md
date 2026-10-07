# Internet Speed Tester & Website IP Lookup

A Python mini-project for testing internet connection speed and resolving a website hostname to its IP address.

## Features

- Test internet **download speed**
- Test internet **upload speed**
- Measure **ping/latency**
- Tkinter graphical user interface
- Resolve a website hostname to an IPv4 address
- Original Jupyter Notebook included

## Project Structure

```text
005_Test_Internet_Speed/
│
├── 005_Test_Internet_Speed.ipynb
├── README.md
├── requirements.txt
├── LICENSE
├── .gitignore
│
├── src/
│   ├── internet_speed_test.py
│   ├── internet_speed_gui.py
│   └── website_ip_lookup.py
│
└── assets/
```

## Requirements

- Python 3.9+
- Internet connection
- `speedtest-cli`
- Tkinter (normally included with standard Python installations; Linux users may need to install their OS Tk package)

## Installation

Clone the repository and open the project folder:

```bash
git clone https://github.com/YOUR_USERNAME/005_Test_Internet_Speed.git
cd 005_Test_Internet_Speed
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Command-Line Speed Test

```bash
python src/internet_speed_test.py
```

The program displays:

- Download speed in Mbps
- Upload speed in Mbps
- Ping in milliseconds

## Run the GUI

```bash
python src/internet_speed_gui.py
```

Click **Check Speed** and wait for the test to complete.

## Find a Website IP Address

```bash
python src/website_ip_lookup.py
```

Example:

```text
Please enter website address (e.g., google.com): google.com
Hostname: google.com
IP Address: ...
```

## Jupyter Notebook

Open:

```text
005_Test_Internet_Speed.ipynb
```

The notebook contains the original learning material and examples for the project.

## How It Works

The speed-test program uses the `speedtest-cli` Python package to communicate with Speedtest infrastructure and measure network performance.

The website IP lookup uses Python's built-in `socket` module:

```python
socket.gethostbyname("google.com")
```

## Important Notes

- Internet speed results can vary depending on network traffic, Wi-Fi signal, server selection, VPN usage, and other factors.
- The GUI version uses a background thread so the interface remains responsive while the speed test runs.
- The original notebook is retained as a learning/reference file. The standalone scripts in `src/` are organized versions for easier execution.

## Learning Topics

This project demonstrates:

- Python modules and imports
- Third-party package installation
- Functions
- Exception handling
- Classes and GUI programming
- Tkinter widgets
- Threads
- Network speed measurement
- DNS/hostname resolution
- Formatted output

## Author

**Dharmesh Kumar**

Python | Data Analytics | AI/ML | Computer Science
