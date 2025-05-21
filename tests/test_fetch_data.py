import pytest
import pandas as pd
import requests
from src.fetch_data import FetchData

class DummyResponse:
    def __init__(self,json_data,status_code):
        self._json = json_data
        self.status_code = status_code
    def raise_for_status(self):
        if self.status_code != 200:
            raise requests.HTTPError(f"status {self.status_code}")
    def json(self):
        return self._json


def test_init_eampty_base_url():
    with pytest.raises(ValueError):
        FetchData(base_url="", user_agent="agent")

def test_init_eampty_user_agent():
    with pytest.raises(ValueError):
        FetchData(base_url="https://api.met.no", user_agent="")


def test_hent_data_success(monkeypatch):
    dummy = DummyResponse({"foo":123}, 200)
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: dummy)
    api = FetchData(base_url="https://api.met.no", user_agent="agent")
    res = api.hent_data(endpoint="compact", params={"x":1})
    assert red == {"foo": 123}

def test_hent_data_error(monkeypatch):
    dummy = DummyResponse(None, 404)
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: dummy)
    api = FetchData(base_url="https://api.met.no", user_agent="agent")
    with pytest.raises(requests.HTTPError):
        api.hent_data(endpoint="compact")


def flat_ut_success():
    data = {"properties": {"timeseries": [{"a":1}, {"a":2}]}}
    api = FetchData(base_url="b", user_agent="u")
    df = api.flat_ut(data)
    assert isinstance(df,pd.DataFrame)
    assert list(df["a"]) == [1, 2]

def flat_ut_error():
    data = {}
    api = FetchData(base_url="b", user_agent="u")
    with pytest.raises(KeyError):
        api.flat_ut(data)