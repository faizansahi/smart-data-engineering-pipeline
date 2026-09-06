# Architecture
The pipeline separates extraction, validation, normalized staging, idempotent loading, analytics views, and run metadata. Airflow owns scheduling and retries.
