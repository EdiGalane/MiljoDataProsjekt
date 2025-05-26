import requests
import pandas as pd
import os 
from dotenv import load_dotenv

class FetchData:
    """
    Klasse for å hente og flate ut JSON-data fra MET.no Locationforcast2.0 API
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

        self.base_url = base_url.rstrip("/")
        self.headers = {
            "User-Agent": user_agent
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
        url = f"{self.base_url}/{edpoint.lstrip('/')}"
        try:
            resp = requests.get(url, params = params, headers = self.headers)
            resp.raise_for_status()
            return resp.json()
        except requests.HTTPError as e:
            raise requests-HTTPError(f"HTTP-feil {e}")
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


    def hent_trondheim_forcast(self):
        """
        Henter kompakt værdata for Trondheim fra Locationforecast
        """
        params = {"lat": 63.4295, "lon": 10.3951}
        data = self.hent_data(endpoint="compcat",params=params)
        return self.flat_ut(data, path="properties.timeseries")

   def lagre_trondheim_forecast(self):
    """
    Henter værdata for Trondheim og lagrer som ukorrigert CSV-fil.

    Retruns:
        pd.DataFrame: DataFrame med hentede data under navnet "trondheim_forecast_uncleaned.csv"
    """
    df = self.hent_trondheim_forcast()

    undermappe = "data/csv"
    os.makedirs(undermappe, exist_ok=True)

    filsti = os.path.join(undermappe, "trondheim_forecast_uncleaned.csv")
    df.to_csv(filsti, index=False)
    return df
