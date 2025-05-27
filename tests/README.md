# Enhetstester:

Denne mappen inneholder enhetstester for hver av modulene i "src/"-mappen. Følger struktur, rammeverk og tar i bruk unittest-metoder.

## Mål:

- Hver metode i koden oppfører seg som forventet
- Feilhåntering og robusthet er beholdt (negative tester)
- Prosjektet følger god programvarepraksis for applikasjonsutvikling
- Vise forståelse for Arrange - Act - Assert prinsippet

## Dekning:

Testfilene dekker:
- Success scenario (positiv-test): forventet oppførsel ved gyldig input
- Negativ scenario (negativ-test): forventet oppførsel ved feil-input eller manglende/ugyldige data
- setUp() brukt for initialisering av klassen
- assertEqual, assertRaises, assertTrue, assertIsNone, osv...  

## Struktur:
Testene er plassert i "tests/unit/", altså en test fil per src/ modul

## kjøring

samlet kjøring: 
- kjør kommando "python -m unittest discover tests/" og deretter kjør en etter en fil
