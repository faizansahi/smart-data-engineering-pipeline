# Executed checks

On 7 September 2026, Python 3.12.6 on Windows passed **11 tests** with
**70% statement coverage**. Ruff lint, formatting checks, dependency resolution,
`pip check`, and source compilation passed. The API demos import and run the application;
compilation alone is not a runtime import test.

Fetched Berlin weather for 1–7 January 2025 from Open-Meteo, loaded seven rows into SQLite, and loaded the same interval again without duplicates. Zero rows were rejected; the SQL summary returned 31.0 mm precipitation.

[Actual local responses](demo.json) · [Test report](tests.txt) · [Check exit codes](checks.json)

Absolute virtual-environment paths in reports are replaced with `<venv>` for portability.


Docker is unavailable on the local Windows machine. [CI run 34073502743](https://github.com/faizansahi/smart-data-engineering-pipeline/actions/runs/34073502743)
passed quality and container jobs on GitHub-hosted Ubuntu with PostgreSQL 16.
This includes dependency installation, tests, lint, formatting, Compose validation,
image build, and the running container workflow.

The container loaded a labeled two-row fixture twice without duplicates and queried SQL analytics views. Airflow image build and DAG import also passed; no scheduled task or UI execution is claimed.

[Downloaded container results](docker-demo.json) are the actual artifact from that run.

The Airflow image and DAG import are checked separately; neither a scheduled task nor the UI is claimed as verified.
