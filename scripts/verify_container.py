"""Run actual PostgreSQL load and SQL views using an explicit test fixture."""

import json
import os
from dataclasses import asdict
from datetime import date
from pathlib import Path

from sqlalchemy import create_engine, text

from weather_pipeline.pipeline import run

ROOT = Path(__file__).resolve().parents[1]


def main():
    payload = {
        "daily": {
            "time": ["2025-01-01", "2025-01-02"],
            "temperature_2m_mean": [2, 3],
            "precipitation_sum": [0, 1],
            "wind_speed_10m_max": [10, 20],
        }
    }
    url = os.environ["DATABASE_URL"]
    first = run(url, "Berlin", date(2025, 1, 1), date(2025, 1, 2), payload)
    second = run(url, "Berlin", date(2025, 1, 1), date(2025, 1, 2), payload)
    assert first.run_id == second.run_id
    engine = create_engine(url)
    assert engine.dialect.name == "postgresql"
    with engine.begin() as conn:
        for statement in (ROOT / "sql/analytics.sql").read_text().split(";"):
            if statement.strip():
                conn.execute(text(statement))
        assert conn.scalar(text("SELECT COUNT(*) FROM analytics_weather")) == 2
        rows = [
            dict(row)
            for row in conn.execute(text("SELECT * FROM weather_location_summary")).mappings()
        ]
    print(
        json.dumps(
            {
                "database": "PostgreSQL 16",
                "input": "explicit synthetic test fixture",
                "first_run": asdict(first),
                "second_run": asdict(second),
                "summary": rows,
            },
            indent=2,
        )
    )
    engine.dispose()


if __name__ == "__main__":
    main()
