from datetime import datetime

from airflow.decorators import dag, task


@dag(schedule="0 5 * * *", start_date=datetime(2025, 1, 1), catchup=False, tags=["weather", "etl"])
def open_meteo_weather():
    @task.external_python(
        python="/opt/airflow/pipeline-venv/bin/python", expect_airflow=False, retries=3
    )
    def execute():
        import os
        from datetime import date, timedelta

        from weather_pipeline.pipeline import run

        end = date.today() - timedelta(days=7)
        run(
            os.environ["DATABASE_URL"],
            os.getenv("LOCATION", "Berlin"),
            end - timedelta(days=30),
            end,
        )

    execute()


open_meteo_weather()
