# Evidence provenance
The demo fetched Open-Meteo historical daily weather for Berlin, 1–7 January 2025. The actual raw response is `source.json`; validated SQL rows and run metadata are in `demo.json`.

The local database was SQLite. The chart in `../images/demo.png` uses the loaded temperature and precipitation values. It is a data chart, not an Airflow screenshot. PostgreSQL integration uses a separately labeled fixture in CI.

Weather data attribution: Open-Meteo, https://open-meteo.com/ and its underlying reanalysis providers. Historical API documentation: https://open-meteo.com/en/docs/historical-weather-api . Open-Meteo data is provided under CC BY 4.0: https://open-meteo.com/en/licence .

Reproduce with `python scripts/demo_pipeline.py`. Network access is required.
