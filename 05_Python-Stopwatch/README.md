# Python Stopwatch ⏱️

A beginner-friendly stopwatch application built with **Python** and **Tkinter**. It displays elapsed time in minutes, seconds, and centiseconds.

## Features

- Start the stopwatch
- Stop/pause the timer
- Reset the timer to zero
- Simple graphical user interface (GUI)
- Uses Python's high-resolution `time.perf_counter()` clock

## Requirements

- Python 3.9 or newer recommended
- Tkinter (included with many Python installations)

No third-party Python packages are required.

## Run the project

1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Run:

   ```bash
   python stopwatch.py
   ```

   On some Windows systems, use:

   ```bash
   py stopwatch.py
   ```

If Tkinter is unavailable, install the Tk support appropriate for your Python distribution.

## How it works

- `time.perf_counter()` measures elapsed time.
- `start()` begins timing only when the stopwatch is stopped.
- `stop()` saves elapsed time so timing can resume later.
- `reset()` clears the elapsed time and display.
- `root.after()` refreshes the GUI without blocking the application.

## Project structure

```text
Python-Stopwatch/
├── stopwatch.py
├── README.md
├── requirements.txt
├── .gitignore
└── screenshots/
    └── README.md
```

## Future improvements

- Add a lap/split-time feature
- Save lap records to CSV
- Add keyboard shortcuts
- Add a countdown timer

## License

This project is available under the MIT License. See [LICENSE](LICENSE).
