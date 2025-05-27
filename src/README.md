# kildekode - "src":

denne mappen inneholder alle hovedmetoder i modulær struktur. Modulene er organiserte etter formpl og oppgavekrav.

## Innhold:
- fetch_data.py: henter værdata og lagrer som csv eller json fil. bruker requests for fleksibilitet.
- data_reader.py: leser inn datafiler og utforsker filens struktur. tilbyr SQL spørringer med pandasql
- data_cleaner.py: utfører statistisk analyse, beregner korrelasjoner og detekterer outliers.
- data_vizualisation.py: lager grafiske fremstillinger av atasettet ved bruk av Seaborn og Matplolib metoder.
- data_prediction.py: trener en lineær modell til å predikere en valgt variabel og evaluerer resultatene ved bruk av R2 og RMSE i tillegg til grafisk sammenligning av faktiske vs predikerte verdier.

# .env:
- .env ligger i .gitnore, men strukturen er:
    ### .env.example:
    - BASE_URL = https://api.met.no/weatherapi/locationforecast/2.0/
    - USER_AGENT = sett-inn-gyldig-brukeragent-her
    