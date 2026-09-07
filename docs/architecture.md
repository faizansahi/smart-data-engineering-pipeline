# Architecture

```mermaid
flowchart LR
  API[Open-Meteo archive API] --> Raw[Daily JSON]
  Raw --> Validate[Pandas validation]
  Validate --> Rejected[Rejected rows]
  Validate --> Load[SQL upsert]
  Load --> DB[(SQLite or PostgreSQL)]
  DB --> Views[Analytics views]
  Views --> Chart[Weather chart]
  Airflow[Optional Airflow DAG] --> API
```

Raw input is JSON, staging is an in-memory Pandas frame, and durable storage consists of SQL tables and views. Airflow is an optional caller of the same pipeline.

See [design decisions](decisions.md) for tradeoffs.
