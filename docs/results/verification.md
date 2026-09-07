# Verification status

Local Windows execution on 7 September 2026 passed 11 tests with 70% statement coverage. Ruff lint, formatting, and source compilation passed. Raw reports are in this directory.

The live Open-Meteo demo loaded **7 Berlin observations for 1–7 January 2025**, rejected 0 rows, and kept 7 rows after a second execution. The SQL summary returned 31.0 mm total precipitation. The chart is drawn from those loaded rows. The saved local execution used SQLite; PostgreSQL/container verification is recorded separately.

Docker and PostgreSQL execution were unavailable locally. GitHub Actions container verification is pending publication; this record will be updated after an actual run.
