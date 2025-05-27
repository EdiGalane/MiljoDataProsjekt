import unittest
import pandas as pd
import numpy as np
from src.data_prediction import DataPrediksjon

class TestDataPrediksjon(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            "Tid": pd.date_range("2023-01-01", periods=10, freq="D"),
            "Temperatur": [10 + i for i in range(10)],
            "Fuktighet": [70 + i for i in range(10)],
            "Trykk": [1010 + (i % 3) for i in range(10)]
        })
        self.pred = DataPrediksjon(self.df, målvariabel="Temperatur")

    def test_init_valid(self):
        self.assertEqual(self.pred.målvariabel, "Temperatur")
        self.assertEqual(len(self.pred.X_train) + len(self.pred.X_test), len(self.df))

    def test_init_invalid_column(self):
        with self.assertRaises(ValueError):
            DataPrediksjon(self.df, målvariabel="UgyldigKolonne")

    def test_tren_lineær_modell(self):
        modell = self.pred.tren_lineær_modell()
        self.assertIsNotNone(modell)
        self.assertIn("Lineær", self.pred.modeller)

    def test_evaluer_modell(self):
        self.pred.tren_lineær_modell()
        resultater = self.pred.evaluer_modell()
        self.assertIn("Lineær", resultater)
        self.assertIn("R^2", resultater["Lineær"])
        self.assertIn("RMSE", resultater["Lineær"])

    def test_visualiseringsgrunnlag(self):
        self.pred.tren_lineær_modell()
        df_vis = self.pred.visualiseringsgrunnlag()
        self.assertIsInstance(df_vis, pd.DataFrame)
        self.assertIn("Faktisk", df_vis.columns)
        self.assertIn("Predikert", df_vis.columns)
        self.assertIn("Feil", df_vis.columns)
        self.assertIn("Dag", df_vis.columns)

if __name__ == "__main__":
    unittest.main()