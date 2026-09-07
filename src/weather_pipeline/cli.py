import argparse
import json
import logging
import os
from dataclasses import asdict
from datetime import date, timedelta

from dotenv import load_dotenv

from .pipeline import LOCATIONS, run


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Validate and load Open-Meteo daily weather")
    parser.add_argument(
        "--location", choices=sorted(LOCATIONS), default=os.getenv("LOCATION", "Berlin")
    )
    parser.add_argument("--start", type=date.fromisoformat)
    parser.add_argument("--end", type=date.fromisoformat)
    args = parser.parse_args()
    end = args.end or date.today() - timedelta(days=7)
    start = args.start or end - timedelta(days=30)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s %(message)s")
    result = run(os.getenv("DATABASE_URL", "sqlite:///./weather.db"), args.location, start, end)
    print(json.dumps(asdict(result)))


if __name__ == "__main__":
    main()
