# InfinExpense — API (projeto-orm)

A lightweight FastAPI backend for tracking receipts, merchants, products and categories. This repository contains the API, static frontend assets and migration scripts (Alembic) used by the InfinExpense project.

## Quick Overview
- **Tech stack**: `FastAPI`, `SQLAlchemy (2.x)`, `Alembic`, `Postgres`, `Uvicorn`.
- **Packaging**: `pyproject.toml` (Poetry-compatible metadata).
- **Run options**: Docker Compose (recommended) or local Python environment with Uvicorn.

## Features
- Merchant, Product, Category and Receipt CRUD endpoints.
- File uploads for product/merchant/receipt photos (served from `/uploads`).
- Static frontend served from `static/` and integrated example pages.
- Database migrations via Alembic located in `alembic/`.

## Requirements
- Python >= 3.12
- Docker & Docker Compose (for containerized setup)

## Environment variables
The application reads DB configuration from environment variables (used by `src/settings.py`).

- `DATABASE_DRIVER` (default: `postgresql`)
- `DATABASE_USERNAME` (default: `user`)
- `DATABASE_PASSWORD` (default: `password`)
- `DATABASE_HOST` (default: `database`)
- `DATABASE_PORT` (default: `5432`)
- `DATABASE_NAME` (default: `db`)

These are configured already in `docker-compose.yaml` for the development stack.

## Quickstart (Docker Compose)
Recommended for local development — sets up API, Postgres and Adminer.

1. Build and start services:

```bash
docker-compose up --build
```

2. API will be available at: `http://localhost:8000`

3. FastAPI interactive docs:
- Swagger UI: `http://localhost:8000/docs`
- Redoc: `http://localhost:8000/redoc`

4. Adminer (DB GUI) is exposed on port `5432` (see `docker-compose.yml` mapping).

## Run locally (without Docker)
If you prefer running locally in a virtualenv or via Poetry:

1. Create virtual environment and install dependencies (example using pip):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r <(poetry export -f requirements.txt --without-hashes)
```

Or use Poetry directly:

```bash
poetry install
poetry run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

2. Ensure a Postgres instance is running and environment variables point to it, or use the `docker-compose` database service.

## Database and Migrations (Alembic)
The database URL is assembled in `src/database.py` from `src/settings.py` (environment variables listed above).

Typical Alembic commands (run from repo root):

```bash
# Initialize (if needed):
alembic init alembic

# Create a new migration (autogenerate):
alembic revision --autogenerate -m "describe change"

# Apply migrations:
alembic upgrade head

# Verify current revision:
alembic current
```

Alembic configuration lives in `alembic.ini` and migration scripts are in `alembic/versions/`.

## Project Layout

Key files and folders:

- `pyproject.toml` — project metadata and dependencies
- `docker-compose.yaml` — containerized development services (api, database, adminer)
- `ops/poetry.Dockerfile` — Dockerfile used by the `api` service in compose
- `src/` — Python application code
	- `main.py` — FastAPI application factory and router mounting
	- `settings.py` — Pydantic settings for environment configuration
	- `database.py` — SQLAlchemy engine, SessionLocal and Base
	- `routers/` — route modules (`receipts`, `products`, `categories`, `merchants`, `measurement_units`, `reports`, `uploads`)
	- `models/` — SQLAlchemy models
	- `schemas/` — Pydantic schemas
	- `services/` — CRUD helper functions and business logic
- `static/` — frontend HTML/CSS/JS (example UI pages and docs)
- `uploads/` — runtime folder for uploaded images (mounted/served by FastAPI)
- `alembic/` — Alembic migrations

## API notes
- Routers are included in `src/main.py` and mounted under their respective paths. The API exposes Swagger UI at `/docs` when running.
- File upload endpoints expect `multipart/form-data` and store files in `uploads/` which are exposed by the app at `/uploads`.

## Development tips
- To serve static UI while developing the backend, the app mounts `static/` at `/static` (see `src/main.py`).
- Keep `uploads/` writable (`UPLOAD_DIR.mkdir(parents=True, exist_ok=True)` is executed at startup).
- Use the existing `static/docs/API_INTEGRATION_GUIDE.md` for frontend integration examples and API expectations.

## Tests
There are no automated tests included in the repo currently. Recommended next steps:

- Add unit tests for service/crud functions (pytest + test database fixture)
- Add simple integration tests for API endpoints (httpx or requests + test DB)

## Contributing
- Fork the repo and open a pull request for changes.
- Keep migrations small and descriptive; run `alembic revision --autogenerate` and review generated code before committing.

## Contact
Project author: Luis Barbara — `luisbarbara@live.com.pt`

---
Generated README: summarizes how to run, develop and extend the InfinExpense API. If you'd like, I can also:

- add a small `Makefile` or `scripts/` entries with common commands (run, migrate, shell)
- create a `requirements.txt` or `poetry.lock` export for CI
- add basic pytest scaffolding and one example test

If you want any of those, tell me which and I will add them.

