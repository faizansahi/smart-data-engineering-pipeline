import os
from datetime import date, timedelta

from .pipeline import run


def main():
    end = date.today() - timedelta(days=7)
    start = end - timedelta(days=30)
    print(
        run(
            os.getenv(
                "DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/weather"
            ),
            os.getenv("LOCATION", "Berlin"),
            start,
            end,
        )
    )


if __name__ == "__main__":
    main()
