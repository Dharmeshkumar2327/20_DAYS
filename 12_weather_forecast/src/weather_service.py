"""Weather data client built on the free Open-Meteo APIs (no API key required)."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
TIMEOUT_SECONDS = 12

class WeatherServiceError(Exception):
    """Raised when a location cannot be found or weather data cannot be loaded."""

@dataclass(frozen=True)
class Location:
    name: str
    country: str
    latitude: float
    longitude: float
    timezone: str

def search_location(city: str) -> Location:
    """Find a city and return its coordinates; validate input before network calls."""
    city = city.strip()
    if not city:
        raise WeatherServiceError("Enter a city name first.")
    try:
        response = requests.get(
            GEOCODING_URL,
            params={"name": city, "count": 1, "language": "en", "format": "json"},
            timeout=TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        raise WeatherServiceError("Could not reach the location service. Check your internet connection.") from exc
    except ValueError as exc:
        raise WeatherServiceError("The location service returned invalid data.") from exc

    results = payload.get("results") or []
    if not results:
        raise WeatherServiceError(f"No matching city found for '{city}'. Try a city and country name.")
    item = results[0]
    return Location(
        name=item.get("name", city),
        country=item.get("country", "Unknown country"),
        latitude=float(item["latitude"]),
        longitude=float(item["longitude"]),
        timezone=item.get("timezone", "auto"),
    )

def get_forecast(location: Location, temperature_unit: str = "celsius") -> dict[str, Any]:
    """Fetch current conditions and a 7-day daily forecast for a resolved location."""
    if temperature_unit not in {"celsius", "fahrenheit"}:
        raise ValueError("temperature_unit must be 'celsius' or 'fahrenheit'")
    params = {
        "latitude": location.latitude,
        "longitude": location.longitude,
        "timezone": location.timezone or "auto",
        "temperature_unit": temperature_unit,
        "current": [
            "temperature_2m", "relative_humidity_2m", "apparent_temperature",
            "is_day", "precipitation", "weather_code", "wind_speed_10m"
        ],
        "daily": [
            "weather_code", "temperature_2m_max", "temperature_2m_min",
            "precipitation_probability_max", "sunrise", "sunset"
        ],
        "forecast_days": 7,
    }
    try:
        response = requests.get(FORECAST_URL, params=params, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as exc:
        raise WeatherServiceError("Could not load forecast data. Please try again shortly.") from exc
    except ValueError as exc:
        raise WeatherServiceError("The forecast service returned invalid data.") from exc

    if not isinstance(data.get("current"), dict) or not isinstance(data.get("daily"), dict):
        raise WeatherServiceError("The forecast service returned incomplete weather data.")
    return data

def describe_weather_code(code: int | None) -> str:
    """Convert Open-Meteo WMO weather codes to readable descriptions."""
    descriptions = {
        0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Fog", 48: "Depositing rime fog",
        51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
        56: "Light freezing drizzle", 57: "Dense freezing drizzle",
        61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
        66: "Light freezing rain", 67: "Heavy freezing rain",
        71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow", 77: "Snow grains",
        80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
        85: "Slight snow showers", 86: "Heavy snow showers",
        95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail",
    }
    return descriptions.get(code, "Unknown conditions")
