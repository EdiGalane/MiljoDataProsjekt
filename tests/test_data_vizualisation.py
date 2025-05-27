import unittest
import pandas as pd
import os
from unittest.mock import patch
from src.data_visualisation import DataVisualisering

class TestDataVisualisering(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            "Tid": pd.date_range("2023-01-01", periods=5, freq="D"),
            "Temperatur": [10, 12, 14, 13, 15],
            "Fuktighet": [70, 71, 72, 74, 73],
            "Trykk": [1010, 1011, 1013, 1014, 1012]
        })
        self.viz = DataVisualisering(self.df)

    def test_plott_tidserie_valid(self):
        try:
            self.viz.plott_tidserie("Temperatur", save=False)
        except Exception as e:
            self.fail(f"plott_tidserie feilet: {e}")

    def test_plott_tidserie_invalid(self):
        with self.assertRaises(ValueError):
            self.viz.plott_tidserie("FeilKolonne", save=False)

    def test_plott_sammenheng_valid(self):
        try:
            self.viz.plott_sammenheng("Temperatur", "Fuktighet", vis_outliers=False, thresh=3.0, save=False)
        except Exception as e:
            self.fail(f"plott_sammenheng feilet: {e}")

    def test_plott_sammenheng_invalid(self):
        with self.assertRaises(ValueError):
            self.viz.plott_sammenheng("Temp", "Fukt", vis_outliers=False, thresh=3.0, save=False)

    def test_plott_histogram_valid(self):
        try:
            self.viz.plott_histogram("Temperatur", save=False)
        except Exception as e:
            self.fail(f"plott_histogram feilet: {e}")

    def test_plott_histogram_invalid(self):
        with self.assertRaises(ValueError):
            self.viz.plott_histogram("UgyldigKol", save=False)

    def test_plott_korrelasjonsmatrise(self):
        try:
            self.viz.plott_korrelasjonsmatrise(save=False)
        except Exception as e:
            self.fail(f"plott_korrelasjonsmatrise feilet: {e}")

    def test_plott_pairplot(self):
        try:
            self.viz.plott_pairplot(save=False)
        except Exception as e:
            self.fail(f"plott_pairplot feilet: {e}")

    def test_plott_jointplot(self):
        try:
            self.viz.plott_jointplot("Temperatur", "Fuktighet", save=False)
        except Exception as e:
            self.fail(f"plott_jointplot feilet: {e}")

    @patch("src.data_visualisation.DataVisualisering.lagre_plot")  # om du har en intern hjelpefunksjon
    def test_plott_trend_vs_rådata(self, mock_save):
        try:
            self.viz.plott_trend_vs_rådata("Temperatur", vindu=2, save=False)
        except Exception as e:
            self.fail(f"plott_trend_vs_rådata feilet: {e}")

    def test_visualiser_manglende_verdier(self):
        df_with_nan = self.df.copy()
        df_with_nan.loc[1, "Trykk"] = None
        viz_nan = DataVisualisering(df_with_nan)
        try:
            viz_nan.visualiser_manglende_verdier(save=False)
        except Exception as e:
            self.fail(f"visualiser_manglende_verdier feilet: {e}")

if __name__ == "__main__":
    unittest.main()