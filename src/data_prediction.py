import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression, RANSACRegressor
from sklearn.preprocessing import PolynomialFeature, StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from typing import Tuple, Union
import matplotlib.pyplot as plt
import seaborn as sns

class DataPrediksjon:
    """
    Klasse for prediktiv analyse. Bruker regresjonsmodeller til å forutsi en valgt
    målvariabel basert på historiske og rensede data. Klassen inkluderer feature scaling,
    håntering av kategoriske variabler, et treningsett og testsett og ulike visualiseringer og evalueringer. 
    """
    def __init__(self, df, målvariabel, test_størrelse = 0.2):
        """
        Initialiserer prediksjonsmodellen. forbereder datasettet ved å skille mellom numeriske og 
        kategoriske variabler, håntere manglende verdier, og splitte til et trenings
        og et testsett.

        Args:
            df: renset datasett (Trondheim forecast)
            målevariabel: kolonnen som skal predikeres
            test_størrelse: andel av data brukt til testing, setter som =0.2
        """
        if målvariabel not in df.columns:
            raise ValueError(f"Målevaribelen {målevaribel} finnes ikke")
        
        self.df= df.dropna() 
        self.målevaribel = målevaribel

        X = self.df.drop(columns=[målevariabel, "Tid"], errors="ignore")
        y = self.df[målevariabel]

        self.kategoriske = X.select_dtypes(include=["object", "category"]).columns.tolist()
        self.numeriske X.select_dtypes(include=[np.number]).columns.tolist()

        self.preprocessor = ColumnTransformer(
            transformer=[
                ("num", StandardScaler(), self.numeriske),
                ("cat", OneHotEncoder(drop="first", handle_unknown="ignore"), self.kategoriske)
            ]
        )

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_sixe=test_størrelse, random_state=42)

        self.modeller = {}
        self.resultater = {}

    def tren_lineær_modell(self):
        """
        Trener en lineær regresjonsmodell med preprocessing. 
        Lagres i modellregisteret som 'Lineær'

        Returnerer: 
            Pipeline: den trente modellen.
        """
        modell = Pipeline([
            ("preprocessing", self.preprocessor),
            ("regression", LinearRegression())
        ])
        modell.fit(self.X_train, self.y_train)
        self.modeller["Lineær"] = modell
        return modell

    def evaluer_modeller(self):
        """
        Evaluerer alle trente modeller på testsettet ved hjelp av r^2 og RMSE
        R^2: Hvor mye variasjon modellen faktisk greier å formidle.
        RMSE: gjennomsnittlig avvik mellom prediksjonene og virkeligheten. Nøyaktigheten. 
        Return:
            dict: ordbok av modellnavn med tilhørende evalueringer. 
        """
        for navn, modell in self.modeller.items():
            y_pred = modell.predict(self.X_test)
            r2 = r2_score(self.y_test, y_pred)
            rmse = mean_squared_error(self.y_test, y_pred, squared=False)
            self.resultater[navn] = {"R^2": r2, "RMSE": rmse}
        return self.resultater

    def prediker_ny_data(self, ny_df):
        """
        Predikerer nye verdier basert på en DataFrame 

        args:
            ny_df: datasett med samme struktur som treningssettet. (renset_trondheim_forecast)

        returns:
            np.ndarray: predikerte verdier
        """
        if self.modell is None:
            print("Modellen er ikke trent enda")
            return None

        X_ny = ny_df.drop(columns=[self.målevariabel, "Tid"], errors="ignore")
        return self.modell.predict(X_ny)

    def visualiseringsgrunnlag(self):
        """
        Lager et visualiseringsgrunnlag for testsettet med faktisk og predikert verdi
        """
        if self.modell is None:
            return None
        
        y_pred = self.modell.predict(self.X_test)
        df_vis = self.X_test.copy()
        df_vis["Faktisk"] = self.y_test.values
        df_vis["Predikert"] = y_pred
        df["Tid"] = self.df.loc[self.y_test.index, "Tid"].values if "Tid" in self.df.columns else pd.NaT 
        df_vis["Feil"] = abs(df_vis["Faktisk"] - df_vis["Predikert"])
        df_vis["Uke"] = pd.to_datetime(df_vis["Tid"], errors="coerce").dt.isocalendar().week

    def visualiser_tidserie(self):
        """
        Lager to linjediagrammer, et som viser den faktiske dataen og en som viser predikert.
        Vurdere modellens eve til å følge trender og tidsavhengige varaisjoner.
        """
        df_vis = self.visualiseringsgrunnlag()
        if df_vis is None:
            return
        vis = DataVisualisering(df_vis)
        vis.plott_tidserie("Faktisk", tittel=f"Faktisk {self.målevariabel} over tid")
        vis.plott_tidserie("Predikert", tittel=f"Predikert {self.målvariabel} over tid")

    def visualiser_scatter(self):
        """
        Scatter av faktisk vs predikert verdi.
        Evaluerer nøyaktighet og om prediskjonene den ideelle diagonalen.
        """
        df_vis = self.lag_visualiseringsgrunnlag()
        if df_vis is None:
            return
        vis = DataVisualisering(df_vis)
        vis.plott_scatter("Faktisk", "Predikert", tittel=f"Faktisk vs Predikert")

    def visualiser_feil_pr_uke(self):
        """
        Boxplot som viser fordeling av absolutt prediksjonsfeil per uke. 
        Innsikt i når modellen predikerer dårligere og virderer stabiliteten over tid.
        """
        df_vis = self.lag_visualiseringsgrunnlag()
        if df_vis is None:
            return
        vis = DataVisualisering(df_vis)
        vis.plott_boxplot("Uke", "Feil", tittel=f"Feil per uke – fordeling")