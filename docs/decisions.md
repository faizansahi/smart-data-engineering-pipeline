# Loading and orchestration decisions

A location/date natural key makes loads repeatable. Upserts allow provider revisions. The run ID hashes the location and interval; metadata stores the latest attempt rather than an append-only history.

Pandas checks aligned arrays, valid dates, finite numbers, nonnegative wind/precipitation, and interval membership. Invalid rows are excluded and counted. An empty valid batch fails. Only the demo archives raw JSON; rejected-row details are not persisted.

The temperature anomaly flag uses two standard deviations within the current batch. Different windows can change flags for the same date, so this is an exploration aid rather than an operational detector.

Airflow 2.10 requires SQLAlchemy 1 while the pipeline uses SQLAlchemy 2. A separate virtual environment and external Python task isolate those dependencies. CI verifies image build and DAG import, not scheduled execution. The task uses wall-clock dates rather than Airflow logical intervals; reliable backfills need that corrected.
