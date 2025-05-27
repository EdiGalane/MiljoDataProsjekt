import unittest
import pandas as pd
import tempfile
import os
from src.data_cleaning import DataRensing

class TestDataRensing(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            "time": ["2023-01-01T00:00:00Z", "2023-01-01T01:00:00Z", "2023-01-01T01:00:00Z"],
            "data_instant_details_air_temperature": [5.1, None, 7.3],
            "data_instant_details_relative_humidity": [80, 82, None],
            "data_instant_details_air_pressure_at_sea_level": [1013, 1012, None],
            "data_instant_details_wind_speed": [4.5, 3.8, None],
        })
        self.renser = DataRensing(self.df)

    def test_init_with_valid_dataframe(self):
        self.assertIsInstance(self.renser, DataRensing)

    def test_init_with_invalid_input(self):
        with self.assertRaises(TypeError):
            DataRensing("ikke en dataframe")

    def test_hent_tid_success(self):
        tid = self.renser.hent_tid()
        self.assertIsInstance(tid, pd.Series)
        self.assertEqual(tid.dtype, "datetime64[ns, UTC]")

    def test_hent_tid_missing_column(self):
        df = self.df.drop(columns=["time"])
        with self.assertRaises(KeyError):
            DataRensing(df).hent_tid()

    def test_bygg_renset_dataframe(self):
        df_renset = self.renser.bygg_renset_dataframe()
        self.assertIn("Tid", df_renset.columns)
        self.assertIn("Temperatur", df_renset.columns)

    def test_håndter_manglende_verdier_median(self):
        df_med = self.renser.håndter_manglende_verdier("median")
        self.assertFalse(df_med.isnull().any().any())

    def test_håndter_manglende_verdier_drop(self):
        df_drop = self.renser.håndter_manglende_verdier("drop")
        self.assertLess(df_drop.shape[0], self.df.shape[0])

    def test_håndter_manglende_verdier_invalid(self):
        with self.assertRaises(ValueError):
            self.renser.håndter_manglende_verdier("ugyldig")

    def test_håndter_duplikater(self):
        df_nodups = self.renser.håndter_duplikater(behold=False)
        self.assertEqual(df_nodups.duplicated().sum(), 0)

    def test_avrund_kolonne_success(self):
        df_rounded = self.renser.avrund_kolonne("data_instant_details_air_temperature", 1)
        self.assertTrue(df_rounded["data_instant_details_air_temperature"].equals(
            df_rounded["data_instant_details_air_temperature"].round(1)
        ))

    def test_avrund_kolonne_invalid_kol(self):
        with self.assertRaises(KeyError):
            self.renser.avrund_kolonne("feil_kol", 1)

    def test_avrund_kolonne_invalid_desimal(self):
        with self.assertRaises(ValueError):
            self.renser.avrund_kolonne("data_instant_details_air_temperature", -1)

    def test_bearbeid_tid(self):
        df_rens = self.renser.bygg_renset_dataframe()
        self.renser._df = df_rens
        df_tidy = self.renser.bearbeid_tid()
        self.assertIsInstance(df_tidy["Tid"].iloc[0], str)

    def test_bearbeid_tid_missing_column(self):
        self.renser._df.drop(columns=["time"], inplace=True, errors="ignore")
        with self.assertRaises(KeyError):
            self.renser.bearbeid_tid()

    def test_rense_stats(self):
        dupli, nans = self.renser.rense_stats()
        self.assertGreaterEqual(dupli, 0)
        self.assertGreaterEqual(nans, 0)

    def test_filtrer_temp_over(self):
        self.renser._df["Temperatur"] = [1.0, 6.0, 8.0]
        df_filtered = self.renser.filtrer_temp_over(5.0)
        self.assertTrue((df_filtered["Temperatur"] > 5.0).all())

    def test_filtrer_temp_over_missing(self):
        self.renser._df.drop(columns=["data_instant_details_air_temperature"], inplace=True)
        with self.assertRaises(KeyError):
            self.renser.filtrer_temp_over(5)

    def test_lagre_renset_data_and_file(self):
        # bygg opp renset DataFrame
        self.renser._df = self.renser.bygg_renset_dataframe()

        filnavn = "test_renset.csv"
        sti = self.renser.lagre_renset_data(filnavn=filnavn)
        self.assertTrue(os.path.exists(sti))
        os.remove(sti)

    def test_data_rens_pipeline(self):
        # Endrer _df til startformat
        self.renser._df = self.df
        self.renser._df["Tid"] = pd.to_datetime(self.df["time"])
        self.renser._df.rename(columns={"data_instant_details_air_temperature": "Temperatur"}, inplace=True)
        self.renser._df = self.renser.avrund_kolonne("Temperatur", 1)

        # Midlertidig deaktivering av faktisk filskriving
        self.renser.lagre_renset_data = lambda filnavn: "/dev/null"
        df_resultat = self.renser.data_rens(desimaler=1, temp_grense=2, filnavn="dummy.csv")
        self.assertIsInstance(df_resultat, pd.DataFrame)

if __name__ == "__main__":
    unittest.main()
