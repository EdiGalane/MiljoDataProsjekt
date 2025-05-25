import os
import pandas as pd
from pandasql import sqldf

class DataLeser:
    """
    Klasse for å lese inn og utforske lokale datafiler (CSV, JSON) for miljødata.
    """

    def __init__(self,data_dir):
        """
        Initiliserer DataLeser med katalogen der data ligger.
        Args:
            data_dir: Sti til mappen som inneholder datafiler

        Raises:
            ValueError: Dersom data:dir ikke finnes eller ikke er en katalog
        """
        if not os.path.isdir(data_dir):
            raise ValueError(f"Data-katalogen '{data_dir}' finnes ikke eller er ikke en katalog")
        self.data_dir = data_dir

    def list_filer(self, ext):
        """
        Lister alle filer i data_dir

        Args:
            ext: Filendelse uten punktum, (csv, json, osv...)

        Returns:
            List[str]: liste over filnavn som treng
        """
        alle = os.listdir(self.data_dir)
        if ext:
            alle = [f for f in alle if f.lower().endswith(f".{ext.lower()}")]
        return alle

    def les_csv(self, filnavn. **kwargs):
        """
        Leser en CSV-fil fra data_dir til en DataFrame

        Agrs:
            filnavn: navnet på csv-filen
            **kwargs: parametre til pd.read_cvs.
        
        Retruns:
            pd.DataFrame: Inneholdet i CSV-filen 

        Raisen:
            FileNotFoundError: filen ikke finnes
            pd.errors.EamptyDataError: filen er tom
        """
        path = os.path.join(self.data_dir, filnavn)
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Finner ikke CSV-filen {filnavn} i {self.data_dir}")
        return pd.read_csv(path, **kwargs)

    def les_json(self, filnavn, **kwargs):
        """
        Leser en JSON fil fra datadir til en Dataframe

        args:
            filnavn: Navnet pp JSON-filen
            **kwargs: parametre til pd.read_json
        
        returns:
            pd.DataFrane: innholdet av JSOn-filen
        
        raise:
            FileNotFoundERROR: dersom filen ikke finnes
            ValueError: dersom JSOn-parsing feiler
        """
        path = os.path.join(self.data_dir,filnavn)
        if not os.path.isfile(path):
            raise FileNotFoundError(f"finner ikke JSON-filen {filnavn} i {self,data_dir}")
        return pd.read_json(path, **kwargs)

    
    def sql_utforsk(self, df, query):
        """
        Utfører en SQL-spørring mot DataFrame ved hjelp av pandasql.

        args:
            df: dataframen som vi kjører sql spørringen mot
            query: sql-spørring som skal kjøres, eksempler: "SELECT * FROM df WHERE ...".
        
        Returns:
            pd.DataFrame: Resultatet av SQL-Spørring
        
        Reises:
            ValueError: dersom query er tom
        """
        if not query or not isinstance(query, self):
            raise ValueError("Ugyldig SQL-spørring.")
        pysqldf = lambda q: sqldf(q, {"df": df}) #bygg in-memory env for sqldf!
        return pysqldf(query)

    def beskriv_dataframe(self, df, navn):
        """
        Lager en kort beskrivelse av et datasett

        args:
            df: dataframen som skal beskrives
            navn: navnet til dataframen/filen
        """
        print(f"\n--- {navn} ---")
        print(f"Antall rader: {df.shape[0]}")
        print(f"Antall kolonner: {df.hape[1]}")
        print(f"De 5 første radene:")
        print(df.head(5))