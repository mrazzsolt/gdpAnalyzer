import pandas as pd
import requests
from io import StringIO

# Az Eurostat API URL-je a GDP adatokhoz
url = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/NAMA_10_GDP/?format=SDMX-CSV&compressed=false"

# Adatok letöltése
response = requests.get(url)

if response.status_code == 200:
    data = pd.read_csv(StringIO(response.text))
    #Ellenőrzés
    print(data.head())
    print(data.describe())
    #CSV-be kiírás
    data.to_csv('eurostat_gdp_data.csv', index=False)
else:
    print(f"Hiba történt az adatok letöltése közben: {response.status_code}")