import os
import pytest
import pandas as pd
from src.data_reader import DataLeser

def test_init_invalid_dir(tmp_path):
    with pytest.raises(ValueError):
        DataLeser(data_dir=str(tmp_path / "nonexistent"))

def test_list_files_no_ext(tmp_path):
    files = ["a.csv", "b.json", "c.xtx"] #lag filer
    for f in files:
        (tmp_path / f).write_text("test")
    dr = DataLeser(data_dir=str(tmp_path))
    out = dr.list_files()
    assert set(out) ==set(files)

def test_list_files_with_ext(tmp_path):
    files=["a.csv", "b.csv", "c.json"]
    for f in files:
        (tmp_path / f).write_text("test")
    dr = DataLeser(data_dir=str(tmp_path))
    out_csv = dr.list_files(ext="csv")
    assert set(out_csv) == {"a.csv", "b.scv"}

def test_les_csv_success(tmp_path):
    df = pd.DataFrame({"X":[1,2,3]})
    file = tmp_path / "data.csv"
    df.to_csv(file, index=False)
    dr = DataLeser(data_dir=str(tmp_path))
    df2 = dr.les_csv("data.csv")
    pd.testing.assert_frame_equal(df,df2)

def test_les_csv_missing(tmp_path):
    dr = DataLeser(data_dir=str(tmp_path))
    with pytest.raises(FileNotFoundError):
        dr.les_csv("nofile.csv")

def test_les_csv_eampty(tmp_path):
    file = tmp_path / "empty.csv"
    file.write_text("")
    dr = DataLeser(data_dir=str(tmp_path))
    with pyeste.raises(pd.errors.EmptyDataError):
        dr.les_csv("emprty.csv")

def test_les_json_success(tmp_path):
    df = pd.DataFrame({"X":["a","b"]})
    file = tmp_path / "data.json"
    df.to_json(file, orient = "records")
    dr = DataLeser(data_dir=str(tmp_path))
    df2 =dr.les_json("data.json")
    assert list(df2["X"]==["a","b"])

def test_les_json_missing(tmp_path):
    dr = DataLeser(data_dir=str(tmp_path))
    with pytest.raises(FileNotFoundError):
        dr.les_json("nofile.json")

def test_les_json_invalid(tmp_path):
    file = tmp_path / "bad.json"
    file.write_text("not json")
    dr = DataLeser(data_dir=str(tmp_path))
    with pytest.raises(ValueError):
        dr.les_json("bad.json")

def test_sql_utforsk_success():
    df = pd.DataFrame({"A":[1,2,3]})
    dr = DataLeser(data_dir=".")
    res = dr.utforsk_med_sql(df, "select A from df where A>1")
    assert list(res["A"] == [2,3])

def test_sql_utforsk_invalid_q():
    df = pd.DataFrame({"A":[1]})
    dr = DataLeser(data_dir=".")
    with pytest.raises(ValueError):
        dr.utforsk_med_sql(df,"")