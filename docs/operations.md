# Operations Notes

## Local startup

1. copy `.env.example` to `.env`
2. run `docker compose up --build`
3. open the API docs if desired
4. submit a case through the API
5. confirm the worker processes the job

## Health endpoints

- API live: `/health/live`
- API ready: `/health/ready`
- AI live: `/health/live`
- AI ready: `/health/ready`

## Metrics

- API metrics: `/metrics`
- AI metrics: `/metrics`
- Prometheus: enable the `observability` profile

## Running tests

The project requires Python 3.11. To run tests locally:

```bash
pip install -e ".[dev]"
pytest -q
```

To run tests from inside the Docker image (useful for CI or a clean environment):

```bash
docker compose build api
docker compose run --rm --no-deps api pytest -q tests/unit tests/integration
```

Smoke tests require a running stack:

```bash
SMOKE_BASE_URL=http://localhost:8000 pytest tests/smoke -q
```

## Common useful commands

- run migrations: `docker compose run --rm api alembic upgrade head`
- seed demo data: `docker compose run --rm api python scripts/seed_demo_data.py`

## Failure handling in the starter

If AI processing fails:

- the job is marked failed
- the case is marked failed
- the error is recorded on the job row

## Resetting local state

To remove local database state:

- `docker compose down -v --remove-orphans`
