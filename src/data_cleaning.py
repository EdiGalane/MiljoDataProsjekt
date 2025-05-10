import pandas as pd

class DataCleaning:
    """
    Klasse for datarensing av miljødatasett.
    Initieres med en pandas DataFrame
    """
    def hent_tid(df):
        """
        Henter og konverterer tidsstempler til pandas datetime
        """
        if "time" not in df.columns:
            raise KeyError("'time' mangler i DataFrame")
        return pd.to_datetime(df["time"])



    def hent_temperatur(df):
        """
        Henter temperaturkolonnen fra API-datasett
        """
        kol = "data_instant_details_air_temperature"
        if kol not in df.columns:
            raise KeyError(f"Kolonne {kol} mangler")
        return df[kol]



    def hent_fuktighet(df):
        """
        Henter fuktighetkolonnen fra API-datasett
        """
        kol = "data_instant_details_relative_humidity"
        if kol not in df.columns:
            raise KeyError(f"Kolonne {kol} mangler")
        return df[kol]



    def hent_trykk(df):
        """
        Henter trykkolonnen fra API-datasett
        """
        kol = "data_instant_details_air_pressure_at_sea_level"
        if kol not in df.columns:
            raise KeyError(f"Kolonne {kol} mangler")
        return df[kol]



    def hent_vind(df):
        """
        Henter vindkolonnen fra API-datasett
        """
        kol = "data_instant_details_wind_speed"
        if kol not in df.columns:
            raise KeyError(f"Kolonne {kol} mangler")
        return df[kol]



    def bygg_renset_dataframe(df_flat):
        """
        Bygger en helt flat, renset DataFrame med nøkkelkolonner
        """
        df_res = pd.DataFrame()

        df_res["Tid"] = hent_tid(df_flat)
        df_res["Temperatur"] = hent_temperatur(df_flat)
        df_res["Fuktighet"] = hent_fuktighet(df_flat)
        df_res["Trykk"] = hent_trykk(df_flat)
        df_res["Vindhastighet"] = hent_vind(df_flat)

        return df_res



    def håndter_manglende_verdier(df, metode = "behold"):
        """
        Håndterer manglende verdier ved drop eller median-imputering
        """
        df_tmp = df.copy()

        if metode.lower() == "drop":
            df_tmp.dropna(inplace = True)
        elif metode.lower() == "median":
            num_kol = df_tmp.select_dtypes(include = ["float", "int"]).columns
            for kol in num_kol:
                med = df_tmp[kol].median()
                df_tmp[kol].fillna(med, inplace = True)
        
        return df_tmp



    def håndter_duplikater(df, behold = True):
        """
        Fjerner duplikater om ønsket
        """
        df_tmp = df.copy()
        if not behold:
            df_tmp.drop_duplicates(inplace = True)

        return df_tmp



    def avrund_kolonne(df,kol, desimaler = 1):
        """
        Avrunder en numerisk kolonne til gitt antall desimaler
        """
        df_tmp=df.copy()
        if kol in df_tmp.coulmns:
            df_tmp[kol] = [round(x,desimaler) if pd.notna(x) else None for x in df_tmp[kol]]
            
        return df_tmp



    def bearbeid_tid(df):
        """
        Formaterer tidskolonnen til '%d.%m.%y - %H:%M'
        """
        df_tmp = df.copy()
        if "Tid" in df_tmp.columns:
            df_tmp["Tid"] = df_tmp["Tid"].dt.strftime("%d.%m.%y - %H:%M")
        return df_tmp



    def rense_stats(df):
        """
        Rapporterer antall duplikater og totalt antall NaN
        """
        ant_dupli = df.duplicated().sum()

        ant_nan = df.isna().sum().sum()

        return ant_dupli, ant_nan



    def filtrer_temp_over(df, temp_grense):
        """
        Filtrerer rader der Temperatur overstiger en grense
        """
        df_tmp = df[df["Temperatur"] > temp_grense].copy()
        return df_tmp