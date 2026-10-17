import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import weather_service as ws

class WeatherServiceTests(unittest.TestCase):
    def test_empty_city_is_rejected_without_network_call(self):
        with patch.object(ws.requests, "get") as get:
            with self.assertRaisesRegex(ws.WeatherServiceError, "Enter a city"):
                ws.search_location("  ")
            get.assert_not_called()

    def test_weather_code_descriptions(self):
        self.assertEqual(ws.describe_weather_code(0), "Clear sky")
        self.assertEqual(ws.describe_weather_code(95), "Thunderstorm")
        self.assertEqual(ws.describe_weather_code(12345), "Unknown conditions")

    def test_invalid_unit_rejected(self):
        location = ws.Location("Bengaluru", "India", 12.97, 77.59, "Asia/Kolkata")
        with self.assertRaises(ValueError):
            ws.get_forecast(location, "kelvin")

    @patch.object(ws.requests, "get")
    def test_location_search_success(self, mock_get):
        response = Mock()
        response.json.return_value = {"results": [{
            "name": "Bengaluru", "country": "India", "latitude": 12.97,
            "longitude": 77.59, "timezone": "Asia/Kolkata"
        }]}
        response.raise_for_status.return_value = None
        mock_get.return_value = response
        result = ws.search_location("Bengaluru")
        self.assertEqual(result.name, "Bengaluru")
        self.assertAlmostEqual(result.latitude, 12.97)

if __name__ == "__main__":
    unittest.main()
