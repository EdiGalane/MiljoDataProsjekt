import requests
import pandas as pd
import os 
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), os.pardir, ".env")
load_dotenv(dotenv_path)

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY amngler. Legg til i .env")

class FetchData:
    """
    Klasse for å hente og flate ut JSON-data fra MET.no Locationforcast API
    """

    def __init__(self, base_url: str, user_agent: str):
        """
        initialiserer MetApi med base-URL og User-Agent

        Args:
            base_url(str): grunn_URL til MET.no API
            user_agent(str): påkrevd HTTP-header for legitim forespørsel.
        raise:
            ValueError: dersom base url eller user agent er tomme
        """
        if not base_url:
            raise ValueError("base_url kan ikke være tom")
        if not user_agent:
            raise ValueError("user_agent kan ikke være tom")
        self.base_url=base_url.rstrip("/")
        self.headers = {
            "User-Agent": user_agent,
            "x-api-key": API_KEY
        }
    
    def hent_data(self, endpoint, params):
        """
        Henter JSON-data fra MET.no API

        Args: 
            endpoint(str): Sti eller base_url
            params (dict): URL-parametre som dictionary
        
        Returns:
            dict: Deserialisert JSON-respons
        
        Raise:
            requets.HTTPError: Ved HTTP-feil.
            ValueError: Ved feil under JSON-parsing
        """
        url = f"{self.base_url}/{edpoint-lstrip('/')}"
        try:
            resp = requests.get(url, params = params, headers = self.headers)
            resp.raise_for_status()
            return resp.json()
        except ValueError as e:
            raise ValueError(f"Kunne ikke parse JSON: {e}")

    def flat_ut(self, data, path):
        """
        Flater ut en nested liste i JSON til flat DataFrame

        Args:
            data (dict): JSON-data fra hent_data()
            path (str): punktum separert sti til listen som skal flates ut
        
        retruns:
            pd.dataFrame: flat DataFrame med kolonnenavn samlet med '_'
        
        raise: 
            keyError: dersom en nøkkel i sti ikke finnes i data
        """
        node = data 
        for nøkkel in path.split("."):
            if nøkkel not in node:
                raise KeyError(f"Nøkkel {nøkkel} mangler i API-data")
            node = node[nøkkel]
        return pd.json_normalize(node, sep="_")


    def trondheim_forcast(self):
        """
        Henter kompakt værdata for Trondheim
        """
        params = {"lat": 63.4295, "lon": 10.3951}
        data = self.hent_data(endpoint="compcat",params=params)
        return self.flatut(data)

    def save_raw(self, data, filename, data_dir="data"):
        """
        lagre rå JSON data til en fil i data_dir.

        args:
            data: rå JSON som skal lagres
            Filename: filnavn med .json endelse 
            data_dir: katalog for lagring (data)
        """
        os.makedirs(data_dir, exist_ok=True)
        path = os.path.join(data_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data,f,ensure_ascii=False, indent=2)
        
    def save_forecast_csv(self, df, filename, data_dir="data"):
        """
        lagre flated forcast DataFrame som CSV i data_dir

        Args 
            df: dataframe av forecast
            filename: filnavn med .csvendelse
            data_dir: katalog for lagring(Data)
        
        Raises:
            ValueError: dersom dataframe er tom
        """
        os.makedirs(data_dir, exist_ok=True)
        if df.empty:
            raise ValueError("Forecast dataframe er tom")
        path = os.path.join(data_dir, filename)
        df.to_csv(path, index=False)
        
