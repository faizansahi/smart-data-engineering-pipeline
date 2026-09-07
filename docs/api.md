# Data and CLI contracts
This pipeline has no HTTP server. Its external input is Open-Meteo's archive API.

```bash
python -m weather_pipeline.cli --location Berlin --start 2025-01-01 --end 2025-01-07
```

Locations: Berlin, Hamburg, Munich. Dates use YYYY-MM-DD. If omitted, end is seven days before today and start is 30 days before end.

The daily response requires time, temperature_2m_mean, precipitation_sum, and wind_speed_10m_max arrays of equal length. Invalid rows are rejected; an empty valid batch fails. Network extraction retries at most three times.

| SQL object | Purpose |
|---|---|
| analytics_weather | One row per location/date, updated on rerun |
| pipeline_runs | Latest status, counts, timestamps, and error per interval |
| weather_daily_trend | Daily average temperature and total precipitation |
| weather_location_summary | Per-location averages and precipitation total |
| weather_anomaly_rate | Percentage flagged by the batch anomaly rule |

Apply `sql/analytics.sql` to create PostgreSQL views. The demo also supports SQLite view creation.

[Actual extracted payload](results/source.json) · [Recorded SQL results](results/demo.json).
