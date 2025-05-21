import requests
import pandas as pd

class MetAPI:
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
        self.headers = {"User-Agent": user_agent}
    
    def hent_data(self, endpoint, params)

    def flat_ut(self, data, path)
