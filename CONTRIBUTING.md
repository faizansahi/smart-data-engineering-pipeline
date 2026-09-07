# Contributing

Install the development dependencies and run Ruff, Pytest, and `python -m pip check` before submitting changes. Include regression coverage for behavior changes and update the relevant API or data contract.

Use small explicit payloads in tests. Cover malformed input and reruns when changing validation or loading. Keep network extraction separate from deterministic checks.

Do not commit credentials, personal data, databases, model caches, or local logs.
