import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from typing import Tuple, Union
import matplotlib.pyplot as plt
import seaborn as sns

from data_vizualisation import DataVisualisering
from data_cleaning import DataRensing

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
            målvariabel: kolonnen som skal predikeres
            test_størrelse: andel av data brukt til testing, setter som =0.2
        """
        self.df = df.copy()

        if målvariabel not in df.columns:
            raise ValueError(f"Målevaribelen {målvariabel} finnes ikke")
        
        self.målvariabel = målvariabel
        X = self.df.drop(columns=[målvariabel, "Tid"], errors="ignore")
        y = self.df[målvariabel]

        self.kategoriske = X.select_dtypes(include=["object", "category"]).columns.tolist()
        self.numeriske = X.select_dtypes(include=[np.number]).columns.tolist()

        self.preprocessor = ColumnTransformer(
            transformers=[
                ("num", StandardScaler(), self.numeriske),
                ("cat", OneHotEncoder(drop="first", handle_unknown="ignore"), self.kategoriske)
            ]
        )

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=test_størrelse, random_state=42)

        self.modeller = {}
        self.resultater = {}
        self.modell = None

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
        self.modell = modell
        return modell

    def evaluer_modell(self):
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
            rmse = np.sqrt(mean_squared_error(self.y_test, y_pred))
            self.resultater[navn] = {"R^2": r2, "RMSE": rmse}
        return self.resultater

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
        df_vis["Tid"] = self.df.loc[self.y_test.index, "Tid"].values if "Tid" in self.df.columns else pd.NaT 
        df_vis["Feil"] = abs(df_vis["Faktisk"] - df_vis["Predikert"])
        df_vis["Dag"] = pd.to_datetime(df_vis["Tid"], errors="coerce").dt.date
        df_vis = df_vis.sort_values(by="Tid")
        return df_vis

    def visualiser_tidserie(self):
        """
        Lager to linjediagrammer, et som viser den faktiske dataen og en som viser predikert.
        Vurdere modellens eve til å følge trender og tidsavhengige varaisjoner.
        """
        df_vis = self.visualiseringsgrunnlag()
        if df_vis is None:
            return

        plt.figure(figsize=(10,5))

        plt.plot(df_vis["Tid"], df_vis["Faktisk"], label="Faktisk", linewidth=2)
        plt.title(f"Faktisk {self.målvariabel} over tid")
        plt.xlabel("Tid")
        plt.ylabel(self.målvariabel)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.xticks(rotation=45, ha="right")
        plt.show()

        plt.figure(figsize=(10,5))

        plt.plot(df_vis["Tid"], df_vis["Predikert"], label="Predikert", linewidth=2, color="red")
        plt.title(f"Predikert {self.målvariabel} over tid")
        plt.xlabel("Tid")
        plt.ylabel(self.målvariabel)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.xticks(rotation=45, ha="right")
        plt.show()

    def visualiser_scatter(self):
        """
        Scatter av faktisk vs predikert verdi.
        Evaluerer nøyaktighet og om prediskjonene den ideelle diagonalen.
        """
        df_vis = self.visualiseringsgrunnlag()
        if df_vis is None:
            return 
        
        plt.figure(figsize=(8,6))
        sns.scatterplot(data=df_vis, x="Faktisk", y="Predikert", alpha=0.7)
        plt.plot([df_vis["Faktisk"].min(), df_vis["Faktisk"].max()],
             [df_vis["Faktisk"].min(), df_vis["Faktisk"].max()],
             color="red", linestyle="--", label="Perfekt prediksjon")
        plt.title("Faktisk vs Predikert")
        plt.xlabel("Faktisk")
        plt.ylabel("Predikert")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    def visualiser_feil_pr_dag(self):
        """
        Boxplot som viser fordeling av absolutt prediksjonsfeil per dag. 
        Innsikt i når modellen predikerer dårligere og virderer stabiliteten over tid.
        """
        df_vis = self.visualiseringsgrunnlag()
        if df_vis is None:
            return 

        plt.figure(figsize=(10,6))
        sns.boxplot(data=df_vis, x="Dag", y="Feil")
        plt.title("Fordeling av prediksjonsfeil per dag")
        plt.xlabel("Dag")
        plt.ylabel("Absolutt feil")
        plt.grid(True, axis="y")
        plt.tight_layout()
        plt.show()

