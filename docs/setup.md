# Setup

## Local execution

Use Python 3.12+ and a separate virtual environment. Install `python -m pip install -e ".[dev,demo]"`. Copy `.env.example` to `.env` only when customizing defaults; settings are read at process startup.

```bash
python -m weather_pipeline.cli --location Berlin --start 2025-01-01 --end 2025-01-07
```

The default database is local SQLite.

## Reproduce evidence

Use a fresh database:

```bash
python scripts/demo_pipeline.py
```

The script saves actual JSON in `docs/results/` and output visuals in `docs/images/`. Rerunning replaces the saved demo artifacts.

## PostgreSQL and Docker

Set a unique URL-safe `POSTGRES_PASSWORD` in your ignored `.env`. Compose requires it and supplies the internal connection URL. Run `docker compose up --build --abort-on-container-exit --exit-code-from pipeline`. Persistent volumes survive ordinary `docker compose down`.

Optional scheduler: `docker compose -f docker-compose.yml -f docker-compose.airflow.yml up --build airflow`. Airflow standalone creates local UI credentials in its startup output. This is a development scheduler. Its image installs the pipeline package; the DAG calls the pipeline directly.

## Validate

```bash
ruff format --check .
ruff check .
pytest --cov=weather_pipeline --cov-report=term-missing
python -m pip check
```

See [verification status](results/verification.md) for environment limits and CI evidence. No paid API credentials are required.
