from datetime import date

import pytest
from sqlalchemy import create_engine, text

from weather_pipeline.pipeline import normalize, run


@pytest.mark.parametrize("bad", [None, "invalid", float("inf"), -1])
def test_invalid_wind_rejected(bad):
    clean, rejected = normalize(
        {
            "daily": {
                "time": ["2026-01-01"],
                "temperature_2m_mean": [2],
                "precipitation_sum": [0],
                "wind_speed_10m_max": [bad],
            }
        },
        "Berlin",
    )
    assert clean.empty
    assert len(rejected) == 1


def test_invalid_date_rejected():
    clean, rejected = normalize(
        {
            "daily": {
                "time": ["not-a-date"],
                "temperature_2m_mean": [2],
                "precipitation_sum": [0],
                "wind_speed_10m_max": [2],
            }
        },
        "Berlin",
    )
    assert clean.empty and len(rejected) == 1


def test_failed_run_metadata(tmp_path):
    url = f"sqlite:///{tmp_path / 'failed.db'}"
    with pytest.raises(ValueError):
        run(url, "Berlin", date(2026, 1, 1), date(2026, 1, 2), {})
    engine = create_engine(url)
    with engine.connect() as conn:
        assert conn.scalar(text("SELECT status FROM pipeline_runs")) == "FAILED"
    engine.dispose()


def test_invalid_range():
    with pytest.raises(ValueError):
        run("sqlite://", "Berlin", date(2026, 2, 1), date(2026, 1, 1))


def test_out_of_range_rows_rejected(tmp_path):
    result = run(
        f"sqlite:///{tmp_path / 'range.db'}",
        "Berlin",
        date(2026, 1, 1),
        date(2026, 1, 2),
        {
            "daily": {
                "time": ["2026-01-01", "2026-02-01"],
                "temperature_2m_mean": [2, 3],
                "precipitation_sum": [0, 1],
                "wind_speed_10m_max": [2, 3],
            }
        },
    )
    assert result.rows == 1 and result.rejected == 1
