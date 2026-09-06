from datetime import datetime

from airflow.decorators import dag, task


@dag(schedule="0 5 * * *", start_date=datetime(2025, 1, 1), catchup=False, tags=["weather", "etl"])
def open_meteo_weather():
    @task(retries=3)
    def execute():
        from weather_pipeline.cli import main

        main()

    execute()


open_meteo_weather()
