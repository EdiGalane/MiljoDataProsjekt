import unittest
import pandas as pd
import numpy as numpy
from src.data_analysis import DataAnalyse

class TestDataAnalyse(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            "Temperatur": [10, 12, 13, 15, 99],
            "Fuktighet": [70, 72, 71, 73, 75],
            "Trykk": [1002, 1003, 1004, 1005, 1006]
        })
        self.analyse = DataAnalyse(self.df)

    def test_beregn_gjennomsnitt(self):
        gj = self.analyse.beregn_gjennomsnitt()
        self.assertAlmostEqual(gj["Temperatur"], np.mean(self.df["Temperatur"]))

    def test_beregn_median(self):
        med = self.analyse.beregn_median()
        self.assertEqual(med["Fuktighet"], 72)

    def test_beregn_standardavvik(self):
        std = self.analyse.beregn_standardavvik()
        self.assertTrue("Trykk" in std.index)
        self.assertGreater(std["Trykk"], 0)

    def test_beskriv_data_structure(self):
        desc = self.analyse.beskriv_data()
        self.assertIn("Gjennomsnitt", desc.columns)
        self.assertEqual(desc.shape[0], self.df.shape[1])

    def test_korrelasjon_valid(self):
        kor = self.analyse.korrelasjon("Temperatur", "Fuktighet")
        self.assertTrue(isinstance(kor, float))
        self.assertGreaterEqual(kor, -1)
        self.assertLessEqual(kor, 1)

    def test_korrelasjon_invalid_column(self):
        with self.assertRaises(ValueError):
            self.analyse.korrelasjon("Temperatur", "UgyldigKolonne")

    def test_identifiser_outliers_default_threshold(self):
        outliers = self.analyse.identifiser_outliers()
        self.assertGreaterEqual(outliers.shape[0], 1)  

    def test_identifiser_outliers_custom_threshold(self):
        outliers = self.analyse.identifiser_outliers(threshold=10.0)
        self.assertEqual(outliers.shape[0], 0)

    def test_kolonne_trend_valid(self):
        trend = self.analyse.kolonne_trend("Trykk", vindu=2)
        self.assertEqual(len(trend), len(self.df))
        self.assertAlmostEqual(trend.iloc[1], np.mean([1012, 1013]))

    def test_kolonne_trend_invalid_column(self):
        with self.assertRaises(ValueError):
            self.analyse.kolonne_trend("FeilKolonne", vindu=3)

if __name__ == "__main__":
    unittest.main()