FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml .
COPY src src
COPY sql sql
COPY scripts/verify_container.py scripts/verify_container.py
RUN pip install --no-cache-dir .
CMD ["python","-m","weather_pipeline.cli"]
