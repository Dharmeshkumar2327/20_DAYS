# Project Notes

## Upgrade summary

The source notebook contained two Tkinter examples using OpenWeatherMap and local image assets. The packaged project keeps the original learning intent (a GUI for looking up weather) while restructuring it into reusable modules.

The new version uses Open-Meteo instead of embedded OpenWeatherMap API keys. This avoids committing credentials and removes the need to manage an API key for the core app.

## Design choices

- **Separation of concerns:** `weather_service.py` handles API and data validation; `app.py` handles presentation.
- **Responsiveness:** network calls run in a worker thread; UI updates are sent back through `root.after`.
- **Defensive behavior:** blank city names, no geocoding results, request failures, invalid JSON, and incomplete payloads are handled.
- **Testability:** the service functions can be tested without launching the GUI, and network calls are mocked in tests.

## Potential next enhancements

- Add weather icons and a map view.
- Add a saved-city list and recent searches.
- Add hourly charts using Matplotlib.
- Add data caching and retry/backoff policies.
- Add CI using GitHub Actions and type checking with mypy.
- Add screenshots or a short demo GIF to the README.

## API references

- https://open-meteo.com/en/docs
- https://open-meteo.com/en/docs/geocoding-api
