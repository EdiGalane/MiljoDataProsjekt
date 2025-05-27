import unittest
import os
import pandas as pd
import tempfile
import shutil
from src.data_reader import DataLeser

class TestDataLeser(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp() # midlertidig mappe og testfiler

        self.csv_path = os.path.join(self.test_dir, "test.csv") #test csv fil
        pd.DataFrame({"a": [1, 2], "b": [3, 4]}).to_csv(self.csv_path, index=False)

        self.json_path = os.path.join(self.test_dir, "test.json") #test json fil
        pd.DataFrame({"x": [5, 6], "y": [7, 8]}).to_json(self.json_path, orient="records")

        self.leser= DataLeser(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir) # sletter mdilertidige mapper og filer

    def test_init_with_valid_directory(self):
        self.assertIsInstance(self.leser, DataLeser)

    def test_init_with_invalid_directory(self):
        with self.assertRaises(ValueError):
            DataLeser("ugyldig/sti")

    def test_list_filer_csv(self):
        result = self.leser.list_filer("csv")
        self.assertIn("test.csv", result)

    def test_les_csv_success(self):
        df = self.leser.les_csv("test.csv")
        self.assertEqual(df.shape, (2, 2))
        self.assertIn("a", df.columns)

    def test_les_csv_missing(self):
        with self.assertRaises(FileNotFoundError):
            self.leser.les_csv("finnes_ikke.csv")

    def test_les_json_success(self):
        df = self.leser.les_json("test.json")
        self.assertIn("x", df.columns)
        self.assertEqual(len(df), 2)

    def test_les_json_missing(self):
        with self.assertRaises(FileNotFoundError):
            self.leser.les_json("finnes_ikke.json")

    def test_sql_utforsk_valid(self):
        df = pd.DataFrame({"navn": ["a", "b"], "verdi": [1, 2]})
        result = self.leser.sql_utforsk(df, "SELECT * FROM df WHERE verdi > 1")
        self.assertEqual(result.shape[0], 1)
        self.assertIn("navn", result.columns)

    def test_sql_utforsk_invalid_query(self):
        df = pd.DataFrame({"x": [1, 2]})
        with self.assertRaises(ValueError):
            self.leser.sql_utforsk(df, "")

    def test_beskriv_dataframe_print(self):
        df = pd.DataFrame({"col1": [10, 20], "col2": [30, 40]})
        try:
            self.leser.beskriv_dataframe(df, "TestDataFrame")  # output til terminal
        except Exception as e:
            self.fail(f"beskriv_dataframe feilet: {e}")

if __name__ == "__main__":
    unittest.main()