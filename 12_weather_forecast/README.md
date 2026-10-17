# SkyCast — Advanced Weather Forecast GUI

A modular Python desktop application that looks up a city and displays current weather plus a seven-day forecast in a clean Tkinter interface. It uses the free [Open-Meteo](https://open-meteo.com/) geocoding and forecast APIs, so **no API key or secret is required**.

## Features

- Search cities by name, with clear handling for blank or unknown locations.
- Current conditions: temperature, feels-like temperature, humidity, wind, and precipitation.
- Seven-day forecast: daily high/low, weather description, rain probability, sunrise, and sunset.
- Celsius/Fahrenheit selection.
- Network requests run on a background thread to keep the GUI responsive.
- Request timeouts, input validation, structured error handling, and unit tests.
- Modular code separated into interface and weather-service logic.

## Preview

The application opens as a desktop window with a current-conditions summary and a forecast table. Add your own screenshot to `assets/` and link it here, for example:

```markdown
![SkyCast application screenshot](assets/skycast-screenshot.png)
```

## Requirements

- Python 3.10+
- Internet connection
- Tkinter (usually included with standard Python; Linux may require installing the OS package `python3-tk`)

## Quick start

### Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

Enter a city such as `Bengaluru`, then select **Get forecast**. Change the units selector to refresh in Fahrenheit or Celsius.

## Run tests

From the project root:

```bash
python -m unittest discover -s tests -v
```

Tests cover empty input, weather-code descriptions, invalid temperature units, and successful location parsing. They mock network requests, so the unit tests do not require a live API connection.

## Project structure

```text
advanced-weather-forecast/
├── main.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── app.py
│   └── weather_service.py
├── tests/
│   └── test_weather_service.py
├── notebooks/
│   └── original_weather_gui_sanitized.ipynb
├── docs/
│   └── PROJECT_NOTES.md
└── assets/
    └── (add screenshots here)
```

## Architecture

1. `main.py` is the entry point and adds `src/` to the Python import path.
2. `src/app.py` owns the Tkinter interface and launches network work in a daemon thread.
3. `src/weather_service.py` validates input, resolves city coordinates, calls the forecast API, and maps WMO codes to descriptions.
4. `tests/` contains unit tests for core service behavior.

## Data source and limitations

- Geocoding: Open-Meteo Geocoding API.
- Weather: Open-Meteo Forecast API.
- Data and availability depend on the upstream provider. This app is for learning and general information, not emergency or safety-critical decisions.
- The displayed wind speed uses the API's default unit (km/h). Temperature units can be changed in the interface.

## Troubleshooting

- **No city found:** try a more specific name, such as `Springfield, United States`.
- **Connection error:** check internet access and retry.
- **Tkinter missing on Linux:** install your distribution's `python3-tk` package.
- **PowerShell blocks activation:** you can run `.venv\Scripts\python.exe -m pip install -r requirements.txt` and `.venv\Scripts\python.exe main.py` without activating the environment.

## Learning outcomes

Practice GUI development, REST APIs, JSON parsing, input validation, exception handling, background threads, modular architecture, and unit testing.

## GitHub upload

1. Extract the ZIP file.
2. Create a repository named `advanced-weather-forecast`.
3. Upload the **contents** of this folder (not an extra nested folder) to the repository.
4. Commit with a message such as `Build advanced SkyCast weather forecast GUI`.
5. Add a screenshot to `assets/` and update the Preview section.

## License

MIT — see [LICENSE](LICENSE).
