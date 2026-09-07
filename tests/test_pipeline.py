from datetime import date

import pytest
from sqlalchemy import create_engine, text

from weather_pipeline.pipeline import normalize, run

FIXTURE = {
    "daily": {
        "time": ["2026-01-01", "2026-01-02", "2026-01-03"],
        "temperature_2m_mean": [2.0, 3.0, 30.0],
        "precipitation_sum": [1.0, 0.0, -1.0],
        "wind_speed_10m_max": [15.0, 20.0, 12.0],
    }
}


def test_validation_and_anomaly():
    clean, rejected = normalize(FIXTURE, "Berlin")
    assert len(clean) == 2 and len(rejected) == 1
    assert set(clean.columns) >= {"location", "is_temperature_anomaly"}


def test_idempotent_complete_etl(tmp_path):
    url = f"sqlite:///{tmp_path / 'etl.db'}"
    first = run(url, "Berlin", date(2026, 1, 1), date(2026, 1, 3), FIXTURE)
    second = run(url, "Berlin", date(2026, 1, 1), date(2026, 1, 3), FIXTURE)
    assert first.run_id == second.run_id
    with create_engine(url).connect() as conn:
        assert conn.scalar(text("SELECT COUNT(*) FROM analytics_weather")) == 2
        assert conn.scalar(text("SELECT status FROM pipeline_runs")) == "SUCCESS"


def test_schema_failure():
    with pytest.raises(ValueError, match="Missing fields"):
        normalize({"daily": {"time": []}}, "Berlin")
