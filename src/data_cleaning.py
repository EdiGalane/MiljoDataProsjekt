import pandas as pd 
import os

class DataRensing:
    """
    Klasse for å rense og forberede DataFrame for videre analyse.
    Inneholder metoder for å bygge renset datasett, håntere menglende verdier,
    fjerne duplikater, avrunding, tidsformatering, statistikk og filtrering.
    """
    def __init__(self, df: pd.DataFrame):
        """
        initialiserer DataRensing med en DataFrame.

        Args:
            df (pd.DataFrame): Inndata-DataFrame som skal renses.
        
        Raises:
            TypeError: dersom df ikke er en pandas DataFrame
        """
        if not isinstance(pd, pd.DataFrame):
            raise TypeError(f"forventet pd.DataFrame, fikk {type(df).__name__}")
        sekf._df = df.copy() 

    def hent_tid(self):
        """
        Henter og konverterer tidsstempler til pandas datetime 
        fra API-datasett

        Return: 
            pd.Series: Kolonne med datetime-objekter.
        
        Raise:
            KeyError: dersom kolonne time ikke finnes
        """
        if "time" not in self._df.columns:
            raise KeyError("Kolonne 'time' mangler i DataFrame")
        # antar ISO-format med Z-sone
        tid = pd.to_datetime(self._df["time"], utc=True)
        return tid



    def hent_temperatur(self):
        """
        Henter temperaturkolonnen fra API-datasett

        Returns:
            pd.Series: Kolonne med temperaturverdier som float.

        Raises:
            KeyError: hvis nøkkelkildenummer mangler.
        """
        kol = "data_instant_details_air_temperature"
        if kol not in self._df.columns:
            raise KeyError(f"Kolonne {kol} mangler")
        return self._df[kol].astype(float)



    def hent_fuktighet(self):
        """
        Henter fuktighetkolonnen fra API-datasett

        Returns:
            pd.Series: kolonne med fuktighetsverdier som float
        """
        kol = "data_instant_details_relative_humidity"
        if kol not in self._df.columns:
            raise KeyError(f"Kolonne {kol} mangler")
        return self._df[kol].astype(float)



    def hent_trykk(self):
        """
        Henter trykkolonnen fra API-datasett

        returns: 
            pd:series: kolonne med trykkverdier som float
        """
        kol = "data_instant_details_air_pressure_at_sea_level"
        if kol not in self._df.columns:
            raise KeyError(f"Kolonne {kol} mangler")
        return self._df[kol].astype(float)



    def hent_vind(self):
        """
        Henter vindkolonnen fra API-datasett

        Returns:
            pd.Series: kolonne med vindhastighetsverdier som float
        """
        kol = "data_instant_details_wind_speed"
        if kol not in self._df.columns:
            raise KeyError(f"Kolonne {kol} mangler")
        return self._df[kol].astype(float)



    def bygg_renset_dataframe(self):
        """
        Bygger en ny DataFrame med utvalgte kolonner for videre analyse:
        Tid, Temperatur, Fuktighet, trykk, Vindhastighet.

        Return:
            pd.DataFrame: Renset DataFrame med faste kolonner.
        
        Raises:
            KeyError: hvis nødvendige underliggende metoder kaster feil.
        """
        df_res = pd.DataFrame()
        df_res["Tid"] = self.hent_tid()
        df_res["Temperatur"] = self.hent_temperatur()
        df_res["Fuktighet"] = self.hent_fuktighet()
        df_res["Trykk"] = self.hent_trykk()
        df_res["Vindhastighet"] = self.hent_vind()
        return df_res



    def håndter_manglende_verdier(self, metode:str = "behold"):
        """
        Håndterer manglende verdier etter valgt metode.

        Args:
            metode(str): "drop" for å fjerne rader, "median" for imputasjoner, eller behold
        
        Returns: 
            pd.Dataframe: DataFrame med utførte operasjoner
        """
        df_tmp = self._df.copy()
        met = metode.lower()
        if met == "drop":
            def_tmp = df_tmp.dropna(inplace = True)
        elif met == "median":
            for kol in df_tmp.select_dtypes(include=["float","int"]):
                df_tmp[kol].fillna(df[kol].median(), inplace=True)
        elif met == "behold":
            pass
        else:
            raise ValueError(f"Ukjent metode {metode} for manglende verdier")
        return df_tmp



    def håndter_duplikater(self, behold: bool = True):
        """
        Fjerner duplikater om behold = False

        Args:
            behold: True for å beholde alle, false for å droppe duplikater
        Returns:
            pd.Dataframe: Dataframe uten duplikater om ønsket
        """
        df_tmp = self._df.copy()
        if not behold:
            df_tmp = df_tmp.drop_duplicates(inplace = True)
        return df_tmp



    def avrund_kolonne(self,kol, desimaler = 1):
        """
        Avrunder en numerisk kolonne til gitt antall desimaler

        Args:
            kol (str): kolonenavn som skal avrundes.
            desimaler (int): antall desimaler, må være >= 0
        
        Return: 
            pd.Dataframe: dataframe med avrundet kolonne

        Raises:
            KeyError: hvis kolonne ikke finnes
            ValueError: hvis dsiamaler er negative
        """
        if kol not in self._df.columns:
            raise KeyError(f"Kolonnen {kol} ikke funnet")
        if desimaler < 0:
            raise ValueError(f"Antall desimaler må være >= 0")
        df_tmp = self._df.copy()
        df_tmp[kol] = df_tmp[kol].round(desimaler)
        return df_tmp



    def bearbeid_tid(self, fmt: str = "%d.%m.%y - %H:%M"):
        """
        Formaterer tidskolonnen til '%d.%m.%y - %H:%M'

        Args:
            fmt(str): datetime-strftime format.
        Returns:
            pd.Dataframe: DataFrame med formatert "Tid"
        Raise:
            KeyError: hvis "tid" ikke finnes i DataFrame.
        """
        df_tmp = self._df.copy()
        if "Tid" not in df_tmp.columns:
            raise KeyError("Kolonnen mangler for tidsformatering")
        df_tmp["Tid"] = pd.to_datetime(df_tmp["Tid"]).df.strftime(fmt)
        return df_tmp



    def rense_stats(self):
        """
        Beregner statistikk om duplikater og NaN-verdier

        Returns:
            tuple[int, int]: Antall duplikater, antall manglende verdier totalt
        """
        ant_dupli = self._df.duplicated().sum()
        ant_nan = self._df.isna().sum().sum()
        return ant_dupli, ant_nan



    def filtrer_temp_over(self, temp_grense:float ):
        """
        Filtrerer rader der Temperatur overstiger en grense

        Args:
            temp_grense (float): Temeperaturgrensen i grader
        Returns:
            pd.DataFrame: DataFrame med kun rader der Temperatur > temp_grense
        """
        if "Temperatur" not in self._df.columns:
            raise KeyError("Kolonnen 'Temperatur' mangler for filtrering")
        return self._df[self._df["Temperatur"] > temp_grense].copy()

    def lagre_renset_data(self, filnavn="trondheim_forecast_cleaned.csv", undermappe="data/csv"):
        """
        Lagrer den rensede dataen til data mappen.

        args:
            filnavn: hva den ferdigrensede filen skal hete
            undermappe: undermappen som filen lagres til
        """
        if self._df is None or self._df.empty:
            raise ValueError("ingen renset DataFrame tilgjengelig for lagring")
        
        os.makedirs(undermappe, exist_ok=True)
        full_sti = os.path.join(undermappe, filnavn)
        self._df.to_csv(full_sti, index=False)
        return full_sti

    def data_rens(self, desimaler=1, temp_grense=None, filnavn="trondheim_forecast_cleaned.csv", undermappe="data"):
        """
        Utfører alle metodene for rensing.

        args:
            desimaler: antall desimaler for avrunding
            temp_grense: dersom satt, filtrerer over denne
            filnavn: navn på outputfil
            undermappe: mappen som filen skal lagres til
        """
        self.df = self.bygg_renset_dataframe()
        print("Ny dataframe bygget")

        dups, nans = self.rense_stats()
        print(f"Antall duplikater: {dups}, Antall manglende verdier: {nans}")

        self._df = self.håndter_manglende_verdier(metode="median")
        self._df = self.håndter_duplikater(behold=False)
        print("MAnglende verdier og fuplikater håndtert")

        self._df=self.bearbeid_tid()
        print("Tid formatert")

        if avrund_kol:
            try: 
                self._df = self.avrund_kolonne(avrund_kol, desimaler)
                print(f"Kolonne {avrund_kol} avrundet til {desimaler} desimaler")
            except Exception as e:
                print(f"Feil i avrunding: {e}")
        else:
            pass

        if temp_grense is not None:
            try:
                self._df = self.filtrer_temp_over(temp_grense)
                print(f"Filtrert alle rader med Temperatur > {temp_grense}")
            except Exception as e:
                print(f"Feil i filtrering: {e}")
        else:
            pass
        
        try:
            sti = self.lagre_renset_data(filnavn=filnavn, undermappe=undermappe)
            print(f"Data lagret til {sti}")
        except Exception as e:
            print(f"Feil ved lagring: {e}")

        print("Data er ferdigrenset")
        return self._df