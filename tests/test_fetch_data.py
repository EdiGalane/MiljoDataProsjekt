import unittest
from unittest.mock import patch, MagicMock
import os
import pandas as pd
from src.fetch_data import FetchData

class TestFetchData(unittest.TestCase):
    def setUp(self):
        self.base_url = "https://api.met.no/weatherapi/locationforecast/2.0"
        self.user_agent = "test-agent@eksempel.com"
        self.fetcher = FetchData(base_url=self.base_url, user_agent=self.user_agent)

    def test_init_missing_user_agent(self):
        with patch.dict(os.environ, {"BASE_URL": "https://api", "USER_AGENT": ""}):
            with self.assertRaises(ValueError):
                FetchData()

    def test_init_missing_base_url(self):
        with patch.dict(os.environ, {"BASE_URL": "", "USER_AGENT": "test_agent"}):
                    with self.assertRaises(ValueError):
                        FetchData()

    @patch("src.fetch_data.requests.get")
    def test_hent_data_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"key": "value"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        data = self.fetcher.hent_data(endpoint="compact", params={"lat": 63.4})
        self.assertEqual(data, {"key": "value"})
        mock_get.assert_called_once()

    @patch("src.fetch_data.requests.get")
    def test_hent_data_http_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("404 error")
        mock_get.return_value = mock_response

        with self.assertRaises(Exception):
            self.fetcher.hent_data("compact", {"lat": 63.4})

    def test_flat_ut_success(self):
        nested_json = {
            "properties": {
                "timeseries": [
                    {"time": "2023-01-01", "data": {"instant": {"air_temperature": 4.5}}},
                    {"time": "2023-01-02", "data": {"instant": {"air_temperature": 2.1}}}
                ]
            }
        }
        df = self.fetcher.flat_ut(nested_json, "properties.timeseries")
        self.assertIsInstance(df, pd.DataFrame)
        self.assertIn("time", df.columns)

    def test_flat_ut_missing_key(self):
        with self.assertRaises(KeyError):
            self.fetcher.flat_ut({}, "properties.timeseries")

    @patch.object(FetchData, "hent_data")
    def test_hent_trondheim_forecast(self, mock_hent_data):
        mock_hent_data.return_value = {
            "properties": {
                "timeseries": [{"time": "2023-01-01", "data": {"instant": {"air_temperature": 5}}}]
            }
        }
        df = self.fetcher.hent_trondheim_forecast()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertIn("time", df.columns)

    @patch.object(FetchData, "hent_trondheim_forecast")
    def test_lagre_trondheim_forecast(self, mock_forecast):
        test_df = pd.DataFrame({"time": ["2023-01-01"], "temp": [5]})
        mock_forecast.return_value = test_df

        df = self.fetcher.lagre_trondheim_forecast()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertIn("time", df.columns)

        # sjekk at filen faktisk er skrevet ut
        filsti = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/trondheim_forecast_uncleaned.csv"))
        self.assertTrue(os.path.exists(filsti))

        # fjern filen etter test
        os.remove(filsti)

if __name__ == "__main__":
    unittest.main()


