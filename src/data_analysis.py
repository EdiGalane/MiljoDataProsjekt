import pandas as pd
import numpy as np
from typing import Union

class DataAnalyse:
    """
    Klasse av metoder for å beregne statistiske mål og utføre analyse. 
    """

    def __init__(self, df):
        """
        Initialiserer analysemodulen med en numerisk DataFrame

        args:
            df: renset pandas DataFrame med numeriske miljødata.
                det er forvented at dette er cleaned data til Trondhiem Forecast
        """
        self.df = df.select_dtypes(include=[np.number])
    
    def beregn_gjennomsnitt(self):
        """
        Beregner gjennomsnitt for hver kolonne.

        Returnes:
            pd.Series: gjennomsnittsverider per variabel
        """
        return self.df.mean()
    
    def beregn_median(self):
        """
        Beregner median for hver kolonne

        Returns;
            pd.Series: Medianverdier per varaibel
        """
        return self.df.median()

    def beregn_standardavvik(self):
        """
        Beregner standardavvik for hver kolonne

        Returns:
            pd.Series: Standardavvik per variabel
        """
        return self.df.std()

    def beskriv_data(self):
        return pd.DataFrame({
            "Gjennomsnitt": self.beregn_gjennomsnitt(),
            "Median": self.beregn_median(),
            "Standardavvik": self.beregn_standardavvik()
        })

    def korrelasjon(self, kol1, kol2):
        """
        Beregner korrelasjonskoeffisient mellom to valgte kolonner

        args:
            kol1: navn på første kolonne
            kol2: navn på andre kolonne

        returns:
            float. korrelasjonskoeffiseient
        
        raises:
            ValueError: dersom en eller begge kolonner ikke finnes i dataframe
        """
        if kol1 in self.df.columns and kol2 in self.df.columns:
            return self.df[[kol1,kol2]].corr().iloc[0,1]
        else:
            raise ValueError("En eller begge kolonnenavnene finnes ikke i df")

    def identifiser_outliers(self, threshold=3.0):
        """
        identifiserer de radene med verdier "score" over terskelverdiern "threshold"

        Args:
            threshold: terskel for score. default er på 3.0

        Returns:
            pd.DataFrame: Rader hvor minst en verdi overstiger score terskel.
        """
        try:
            scores = np.abs((self.df-self.df.mean()) / self.df.std())
            return self.df[(scores > threshold).any(axis=1)]
        except Exception as e:
            raise RuntimeError(f"Feil under utregning av outliers: {e}")

    def kolonne_trend(self, kol, vindu = 7):
        """
        Returnerer en rullende gjennomsnitt for en spesifisert kolonne.

        args:
            kol: navn på kolonnen som skal analyseres
            vindu: størelse på glidende vindu
        
        returns:
            union: glidende gjennomsnitt som Series
        """
        if kol in self.df.columns:
            return self.df[kol].rolling(window=vindu, min_periods=1).mean()
        else:
            raise ValueError(f"kolonnen {kol} finnes ikke i df")
