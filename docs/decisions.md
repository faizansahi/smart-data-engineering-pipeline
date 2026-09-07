# Engineering decisions

## Accepted baseline

Natural-key upserts make reruns idempotent. A deterministic run ID identifies a location/date interval; its metadata describes the latest attempt. SQLite supports quick local tests, while Compose uses PostgreSQL. Anomaly flags use the current validated batch's mean and standard deviation.

## Testing strategy

Airflow 2.10 and this pipeline need different SQLAlchemy major versions. The Airflow image installs the pipeline in a separate virtual environment and uses an external Python task. This follows the [Airflow TaskFlow guidance for conflicting dependencies](https://airflow.apache.org/docs/apache-airflow/2.10.0/tutorial/taskflow.html).

Keep deterministic domain tests separate from HTTP/database integration and real model demos. Unit-test stubs are never presented as model evidence. Capture actual responses and preserve the commands needed to reproduce them.

## Tradeoffs

The local evidence uses SQLite. Open-Meteo data is reanalysis, not a station measurement guarantee. Run metadata is overwritten on rerun rather than retained as an attempt history. Anomaly flags depend on batch boundaries. The CLI does not archive raw data automatically; the demo does. Airflow is optional and its standalone UI is a development setup.

## Next steps

Add per-attempt lineage, persistent raw storage, incremental watermarks, batch-independent anomaly baselines, and broader data-contract tests.
