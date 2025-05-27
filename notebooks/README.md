# Refleksjon og drøfting – Notebooks:

Denne mappen inneholder Jupyter Notebooks som er delt i ulike kategorier for å vise resultater og drøfte.

## Flyt:

1. hent_og_rens:
   - **Formål:** Starte prosjektet med datainnhenting og rensing
   - **Innhold:**
     - Henter data via fetch_data.py
     - Leser og visualiserer rådata (før rensing)
     - Bruker data_cleaning.py til å behandle manglende verdier, duplikater og tid
     - Viser effekten av rensing ved å sammenligne før og etter
   - **Drøfting:** Hvordan manglende verdier påvirker datasettet og valget av median-metoden

2. analyse -> visualisering:
   - **Formål:** Utføre statistisk analyse og visualisere innsikt
   - **Innhold:**
     - Beregner gjennomsnitt, median og standardavvik med data_analysis.py
     - Utfører korrelasjonsanalyse og forklarer sammenhenger
     - Visualiserer tidsserier, fordelinger og korrelasjonsmatrise med data_visualisation.py
   - **Drøfting:** Hvilke variabler korrelerer, hvilke visualiseringer gir mest innsikt, og hvorfor

3. prediksjon:
   - **Formål:** Trene, evaluere og tolke en prediktiv modell
   - **Innhold:**
     - Bygger lineær regresjonsmodell med data_prediction.py
     - Evaluerer ytelse med R2 og RMSE
     - Visualiserer faktisk vs. predikert og feil per dag
   - **Drøfting:** Modellens styrker og svakheter

## KI:
- Hjelp til markdown av outliers identifisering (fikk ikke til å implementere en formel)
- Prøvde å få hjelp til hvorfor interaktiv visualisering ikke returnerer noe, den fikk det ikke til. 
- Prøvde å få hjelp til fjerning av UserWarning i printing av plotts, den fikk det ikke til. 
- Generere en passende sql_spørring i hent_og_rens.ipynb basert på koden våres fra data_reader.
- Forslag til hjelp med feilmeldinger.
