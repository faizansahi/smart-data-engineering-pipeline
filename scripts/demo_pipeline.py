"""Execute real Open-Meteo extraction, validation, SQL loading and idempotency checks."""

import json
import os
from dataclasses import asdict
from datetime import date
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text

from weather_pipeline.pipeline import extract, run


def main():
    root = Path(__file__).resolve().parents[1]
    output = root / "docs/results"
    images = root / "docs/images"
    output.mkdir(parents=True, exist_ok=True)
    images.mkdir(parents=True, exist_ok=True)
    url = os.getenv("DATABASE_URL", "sqlite:///./weather-demo.db")
    start, end = date(2025, 1, 1), date(2025, 1, 7)
    payload = extract("Berlin", start, end)
    (output / "source.json").write_text(json.dumps(payload, indent=2) + "\n")
    first = run(url, "Berlin", start, end, payload)
    second = run(url, "Berlin", start, end, payload)
    assert first.run_id == second.run_id
    engine = create_engine(url)
    with engine.begin() as conn:
        for statement in (root / "sql/analytics.sql").read_text().split(";"):
            if statement.strip():
                if engine.dialect.name == "sqlite":
                    statement = statement.replace(
                        "CREATE OR REPLACE VIEW", "CREATE VIEW IF NOT EXISTS"
                    )
                conn.execute(text(statement))
        rows = [
            dict(row)
            for row in conn.execute(
                text("SELECT * FROM analytics_weather ORDER BY observed_on")
            ).mappings()
        ]
        summary = [
            dict(row)
            for row in conn.execute(text("SELECT * FROM weather_location_summary")).mappings()
        ]
        metadata = [
            dict(row) for row in conn.execute(text("SELECT * FROM pipeline_runs")).mappings()
        ]
    assert len(rows) == first.rows
    result = {
        "source": "Open-Meteo historical API",
        "database": engine.dialect.name,
        "date_range": [str(start), str(end)],
        "first_run": asdict(first),
        "second_run": asdict(second),
        "idempotency_verified": True,
        "analytics": rows,
        "summary": summary,
        "runs": metadata,
    }
    (output / "demo.json").write_text(json.dumps(result, indent=2, default=str) + "\n")
    fig, axes = plt.subplots(2, 1, figsize=(9, 6), sharex=True)
    dates = [str(row["observed_on"]) for row in rows]
    axes[0].plot(dates, [row["temperature_mean"] for row in rows], marker="o", color="#187c9a")
    axes[0].set(title="Berlin | Open-Meteo daily weather", ylabel="Mean temperature (deg C)")
    axes[1].bar(dates, [row["precipitation_sum"] for row in rows], color="#469d76")
    axes[1].set(ylabel="Precipitation (mm)")
    axes[1].tick_params(axis="x", rotation=25)
    fig.text(
        0.02,
        0.01,
        "Actual extracted and loaded data | Open-Meteo attribution: docs/results/provenance.md",
        fontsize=8,
    )
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(images / "demo.png", dpi=150)
    print(json.dumps(result, indent=2, default=str))
    engine.dispose()


if __name__ == "__main__":
    main()
