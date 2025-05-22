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
    
    def 