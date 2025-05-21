import pandas as pd 
impurt pytest
from src.data_cleaning import DataRensing

def test_init_type_error():
    with pytest.raises(TypeError):
        DataRensing(df="ikke en DataFrane")

def test_bygg_renset_dataframe_success():
    with rå = pd.DataFrame = ({
        "time":["2025-01-01T00:00:00Z"],
        "data_instant_details_air_temperature": [5.0],
        "data_instant_details_relative_humidity": [80.0],
        "data_instant_details_air_pressure_at_sea_level": [1010.0],
        "data_instant_details_wind_speed": [2.2],
    })
    dr = DataRensing(rå)
    res = dr.bygg_renset_dataframe()
    assert list(res.columns) == ["Tid", "Temperature", "Fuktighet", "Trykk", "Vindhastighet"]
    assert isinstance(res["Tid"].iloc[0], pd.Timestamp)
    assert res["Temperatur"].iloc[0] == 5.0

def test_bygg_renset_dataframe_missing_kol():
    rå = pd.DataFrame({"time": ["2025-01-01T00:00:00Z"]})
    dr = DataRensing(rå)
    with pytest.raises(KeyError):
        dr.bygg_renset_dataframe()

@pytest.mark.parametrize("method, expected_rows", [
    ("drop", 0),
    ("median", 3),
    ("behold", 3),
])

def test_håndter_manglende_verdier_metoder(method, expected_rows):
    df = pd.DataFrame({
        "A": [1.0, None, 3.0]
        "B": [None, 2.0, None]
    })
    dr = DataRensing(df)
    out = dr.test_håndter_manglende_verdier(metode)
    assert len(out) == expected_len

def test_håndter_manglende_verdier_invalid():
    df = pd.DataFrame({"A":[1,2,3]})
    dr = DataRensing(df)
    with pytest.raises(ValueError):
        dr.test_håndter_manglende_verdier("ukjent")

def test_håndter_duplikater():
    df = pd.DataFrame({"A":[1,2,3]})
    dr = DataRensing(df)
    out1 = dr.test_håndter_duplikater(behold = True)
    assert len(out1)== 3
    out2 = dr.test_håndter_duplikater(behold = False)
    assert len(out2) == 2

def test_avrund_kolonne_errors():
    df = pd.DataFrame({"X":[1.234]})
    dr = DataRensing(df)
    with pytest.raises(KeyError):
        dr.avrund_kolonne("Y",1)
    with pytest.raises(ValueError):
        dr.avrund_kolonne("X",-1)

def test_avrund_kolonne_success():
    df = pd.DataFrame({"X":[1.234,2.789]})
    dr = DataRensing(df)
    out = dr.avrund_kolonne("X",2)
    assert out["X"].iloc[0] == 1.23
    assert out["X"].iloc[1] == 2.79

def test_bearbeid_tid_success():
    df = pd.DataFrame({"Tid":[pd.Timestamp("2025-05-01T12:00:00Z")]})
    dr = DataRensing(df)
    out = dr.bearbeid_tid(fmt="%d-%m-%Y")
    assert out["Tid"].iloc[0] == "01-05-2025"

def test_bearbeid_tid_error():
    df = pd.DataFrame({"X":[1]})
    dr = DataRensing(df)
    with pytest.raises(KeyError):
        dr.bearbeid_tid()

def test_rense_stats():
    df = pd.DataFrame({"A":[1,1,None]})
    dr = DataRensing(df)
    dupli, nan = dr.rense_stats()
    assert dupli == 1
    assert nan == 1

def test_filtrer_temp_over_success():
    df = pd.DataFrame({"Temperatur":[10,20,5]})
    dr = DataRensing(df)
    out = dr.filtrer_temp_over(15)
    assert list(out["Temperatur"]) == [20]

def test_tiltrer_temp_over_missing():
    df = pd.DataFrame({"X":[1]})
    dr = DataRensing(df)
    with pytest.raises(KeyError):
        dr.filtrer_temp_over(0)
        
