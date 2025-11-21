# InfinExpense — API (projeto-orm)

A lightweight FastAPI backend for tracking receipts, merchants, products and categories. This repository contains the API, static frontend assets and migration scripts (Alembic) used by the InfinExpense project.

## TL;DR

- **Start development stack:** `docker compose up --build`
- **API:** `http://localhost:8000`
- **Swagger UI:** `http://localhost:8000/docs`

## Table of Contents

- [Quick Summary](#-quick-summary)
- [What Each Folder Does](#-what-each-folder-does)
- [Full Example: Create a Product (Flow)](#-full-example-create-a-product-flow)
- [Quick Start (TL;DR)](#-quick-start-tldr)
- [Project Layout](#project-layout)
- [API notes](#api-notes)
- [Development tips](#development-tips)
- [Detailed Code Reference](#detailed-code-reference)
 - [Examples](#examples)

## Examples

Quick practical examples you can run locally (adjust IDs as needed).

- Create a merchant:

```bash
curl -s -X POST http://localhost:8000/merchants \
	-H "Content-Type: application/json" \
	-d '{"name":"Test Merchant","location":"Lisbon","notes":"dev"}'
```

- Create a product (master product list):

```bash
curl -s -X POST http://localhost:8000/products \
	-H "Content-Type: application/json" \
	-d '{"name":"Apple","price":1.5,"category_id":1}'
```

- Create a receipt (uses existing merchant and product IDs):

```bash
curl -s -X POST http://localhost:8000/receipts \
	-H "Content-Type: application/json" \
	-d '{"merchant_id":1,"purchase_date":"2025-11-21","products":[{"product_list_id":1,"price":1.5,"quantity":2}]}'
```

- Upload a receipt photo (multipart/form-data):

```bash
curl -s -X POST http://localhost:8000/uploads/receipt/1/photo \
	-F "file=@/path/to/receipt.jpg"
```

- List receipts:

```bash
curl -s http://localhost:8000/receipts
```

Notes:
- Replace IDs (`merchant_id`, `product_list_id`, `receipt_id`) with values returned by the API.
- If you run the app with Docker Compose the API base URL is `http://localhost:8000`.

## 🏗️ FastAPI Architecture — Complete Guide

## 📦 The Flow: From Client to the Database

```
Client (Frontend)
	↓
MAIN.PY (entry point)
	↓
ROUTERS (receive the request)
	↓
SCHEMAS (validate payloads)
	↓
SERVICES (business logic)
	↓
MODELS (ORM layer)
	↓
DATABASE (persistent storage)
```

---

## 🎯 Quick Summary

- **ROUTERS** = HTTP endpoints (e.g. `/products`)
- **SCHEMAS** = Pydantic models for request/response validation
- **SERVICES** = Business logic and CRUD operations
- **MODELS** = SQLAlchemy models that define DB tables
- **DATABASE** = The actual database (Postgres in this project)
- **SETTINGS** = Configuration (credentials, hostnames, ports)
- **ALEMBIC** = Migrations for schema changes

---

## 📁 What Each Folder Does

### 1️⃣ `main.py` — The Entry Point
- Starts the FastAPI app
- Registers routers (receipts, products, categories, merchants, etc.)
- Mounts static files and upload folders

Example (`src/main.py`):
```python
from fastapi import FastAPI
from src.routers import products, categories

app = FastAPI()

app.include_router(products.router)
app.include_router(categories.router)
```

---

### 2️⃣ `routers/` — Request Handlers
- Parse HTTP requests and parameters
- Validate input using Pydantic schemas (automatically)
- Delegate to services for business logic
- Map exceptions to HTTP responses

Example (`src/routers/products.py`):
```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.schemas.product import ProductListCreate, ProductList as ProductListSchema
from src.services.crud_product_list import ProductListService
from src.database import get_db

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductListSchema)
def create_product(product: ProductListCreate, db: Session = Depends(get_db)):
	return ProductListService.create_product_list(db, product)
```

---

### 3️⃣ `schemas/` — Validation Layer
- Define input and output JSON shapes with Pydantic
- Provide automatic validation and helpful error messages
- Configure `from_attributes=True` to allow returning ORM models directly

Example (`src/schemas/product.py`):
```python
from pydantic import BaseModel
from decimal import Decimal

class ProductListCreate(BaseModel):
	name: str
	price: Decimal
	category_id: int

class ProductList(BaseModel):
	id: int
	name: str
	price: Decimal
	category_id: int
	class Config:
		from_attributes = True
```

---

### 4️⃣ `services/` — Business Logic
- Centralize application rules and DB operations
- Ensure validation that depends on DB state (e.g., "category exists")
- Keep routers thin; services talk to models and the DB

Example (`src/services/crud_product_list.py`):
```python
from sqlalchemy.orm import Session
from src.models.product import ProductList

def create_product_list(db: Session, product_data):
	db_product = ProductList(**product_data.model_dump())
	db.add(db_product)
	db.commit()
	db.refresh(db_product)
	return db_product
```

---

### 5️⃣ `models/` — Database Schema (ORM)
- SQLAlchemy models map Python classes to DB tables
- Keep models focused on structure; business rules belong to services

Example (`src/models/product.py`):
```python
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base

class ProductList(Base):
	__tablename__ = "product_list"
	id = Column(Integer, primary_key=True, index=True)
	name = Column(String(255), nullable=False, unique=True)
	category_id = Column(Integer, ForeignKey("category.id"))
	category = relationship("Category")
```

---

### 6️⃣ `database.py` — DB Connection
- Builds the DB URL from `settings` and creates the SQLAlchemy engine
- Exposes `SessionLocal` and the `get_db()` dependency used in routers

Example (`src/database.py`):
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.settings import settings

SQLALCHEMY_DATABASE_URL = (
	f"{settings.database_driver}://"
	f"{settings.database_username}:{settings.database_password}@"
	f"{settings.database_host}:{settings.database_port}/"
	f"{settings.database_name}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()
```

---

### 7️⃣ `settings.py` — Configuration
- Uses Pydantic BaseSettings to read environment variables
- Defaults match `docker compose.yaml` for local development

Example (`src/settings.py`):
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
	database_driver: str = "postgresql"
	database_username: str = "user"
	database_password: str = "password"
	database_host: str = "database"
	database_port: int = 5432
	database_name: str = "db"

settings = Settings()
```

---

### 8️⃣ `alembic/` — Migrations
- Manage schema changes separately from application code
- Use autogenerate carefully and review generated scripts

Common commands:
```bash
alembic revision --autogenerate -m "add stock column"
alembic upgrade head
alembic downgrade -1
```

---

## ✨ Full Example: Create a Product (Flow)

1. Client sends: POST `/products` { "name": "Apple", "price": 1.5, "category_id": 2 }
2. `src/main.py` routes the request to `src/routers/products.py`
3. Router validates input using `src/schemas/product.py` (`ProductListCreate`)
4. Router calls `src/services/crud_product_list.py`
5. Service checks that `category_id=2` exists
6. Service creates a `ProductList` model instance (`src/models/product.py`)
7. `src/database.py` persists the record
8. Service returns the created product
9. Router returns `201 Created` to the client

---

## 🔁 Quick Code Flow Summary

Frontend request:
```javascript
fetch('http://localhost:8000/products', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ name: 'Apple', price: 1.5, category_id: 2 })
})
```

Router handler:
```python
@router.post("/", response_model=ProductListSchema)
def create_product(product: ProductListCreate, db: Session = Depends(get_db)):
	return ProductListService.create_product_list(db, product)
```

Service persists the product:
```python
def create_product_list(db: Session, product):
	db_product = ProductList(**product.model_dump())
	db.add(db_product)
	db.commit()
	db.refresh(db_product)
	return db_product
```

---

## ✅ Quick Start (TL;DR)

1. Start development stack (recommended):

```bash
docker compose up --build
```

2. API: `http://localhost:8000`
3. Swagger UI: `http://localhost:8000/docs`




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

These are configured already in `docker compose.yaml` for the development stack.

## Quickstart (Docker Compose)
Recommended for local development — sets up API, Postgres and Adminer.

1. Build and start services:

```bash
docker compose up --build
```

2. API will be available at: `http://localhost:8000`

3. FastAPI interactive docs:
- Swagger UI: `http://localhost:8000/docs`
- Redoc: `http://localhost:8000/redoc`

4. Adminer (DB GUI) is exposed on host port `5432` mapped to container port `8080` in `docker compose.yml`. This can conflict with a local Postgres instance that also listens on `5432`; consider changing the host mapping (for example to `8080:8080`) to avoid port collisions.

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

2. Ensure a Postgres instance is running and environment variables point to it, or use the `docker compose` database service.

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
- `docker compose.yaml` — containerized development services (api, database, adminer)
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
- Luís Barbara (@luis-barbara )
- Adrien Dejonc (@Huniity)
- Giulio Marani (@cstriker421)
- Nuno Silva (@nuno2msilva)


 
## Detailed Code Reference
The following section explains the purpose and key functionality of the main files and folders in the repository. It is intended to help new contributors quickly understand where to look for functionality and how the pieces fit together.

**Top-level files**
- `pyproject.toml`: Project metadata and dependency declarations. Lists runtime dependencies (FastAPI, SQLAlchemy, Alembic, psycopg2-binary, etc.) and Python version requirement (>=3.12).
- `docker compose.yaml`: Development stack that spins up the `api` service (built using `ops/poetry.Dockerfile`), a `database` service (Postgres 17) and `adminer` for DB browsing. It mounts the repo into the container for fast local development.
- `alembic.ini`: Alembic configuration for database migrations. Points to `alembic/` for migration scripts.

**`ops/`**
- `poetry.Dockerfile`: Dockerfile used to build the API image in development. It sets up a Python environment, installs dependencies (Poetry/poetry export used), copies the app and runs Uvicorn. Use this file to customize container build steps (C extension dependencies, non-Python system libs, etc.).
- `initdb.d/`: Initialization scripts mounted into Postgres container; useful to seed initial database users, schema or data during first container run.

**`src/` — Application code**
- `src/main.py`:
	- FastAPI application instance and global configuration (title, description, version).
	- Mounts static files at `/static` and `uploads/` at `/uploads` so the frontend and uploaded photos are served directly by the app in development.
	- Registers routers for receipts, products, categories, merchants, measurement units, reports and uploads.
	- Adds `CORSMiddleware` preconfigured for typical localhost frontend development ports.
- `src/settings.py`:
	- Pydantic `BaseSettings` class for loading environment variables. Fields mirror the `docker compose.yaml` environment variables for DB configuration (driver, username, password, host, port, name).
	- Instantiates `settings` which is used by `src/database.py`.
- `src/database.py`:
	- Builds the SQLAlchemy database URL from `settings`.
	- Creates the `engine`, `SessionLocal` factory, and `Base` declarative base used by models.
	- Exposes `get_db()` dependency generator used by routers to obtain a DB session and ensure it is closed after requests.

**`src/models/` — SQLAlchemy models**
Files represent the relational schema and key relationships used by Alembic and SQLAlchemy:
- `category.py` — `Category` master list. Fields: `id`, `name`, `color`. Relationship: `product_lists` back to `ProductList`.
- `measurement_unit.py` — `MeasurementUnit` master list (e.g., kg, L). Fields: `name`, `abbreviation` with uniqueness constraints.
- `product.py` — `ProductList` (master product definitions). Fields: `name`, `barcode`, `category_id`, `measurement_unit_id`, `product_list_photo`. Relationships to `Category`, `MeasurementUnit`, and `Product` (receipt items).
- `merchant.py` — `Merchant` with `name`, `location`, `notes`. Relationship `receipts` references `Receipt` and uses cascading delete-orphan to prevent stray rows.
- `receipt.py` — `Receipt` entity representing a purchase. Fields: `merchant_id`, `purchase_date`, `barcode`, `receipt_photo`, timestamps `created_at`/`updated_at`. Relationship to `Merchant` and `Product` (items).
- `receipt_product.py` — `Product` items on a `Receipt` (line items). Fields: `price`, `quantity`, `description`, `receipt_id`, `product_list_id`. Contains constraints to ensure price >= 0 and quantity > 0.

These models are the authoritative source for Alembic autogeneration. Keep them concise and stable to avoid migration complexity.

**`src/schemas/` — Pydantic schemas (request/response models)**
Each file contains Pydantic models used to validate incoming data and structure outgoing JSON responses.
- `category.py`: `CategoryCreate`, `CategoryUpdate`, `Category` (read model includes `id`, `color`, `item_count`, `item_percentage`, `total_spent`).
- `measurement_unit.py`: `MeasurementUnitCreate`, `MeasurementUnitUpdate`, `MeasurementUnit`.
- `product.py`: Contains two groups:
	- `ProductList*` schemas for the master product list (`ProductListCreate`, `ProductListUpdate`, `ProductList`).
	- `Product*` schemas for receipt line items (`ProductCreate`, `ProductUpdate`, `Product`).
- `merchant.py`: `MerchantCreate`, `MerchantUpdate`, `Merchant` read model.
- `receipt.py`: `ReceiptCreate`, `ReceiptUpdate`, `Receipt` (read model with `total_price`, nested `merchant` and `products`, and timestamps).
- `reports.py`: Schemas used by report endpoints (`ReportSpendingByEntity`, `MerchantReportData`).

These schemas define the shape of API payloads, apply validation, and include `model_config` settings to allow ORM model attribute conversion where convenient.

**`src/services/` — Business logic and CRUD helpers**
Services encapsulate DB access patterns used by routers and keep route functions thin:
- `crud_category.py` — CategoryService: listing with aggregated counts & totals, create/update/delete with color auto-assignment and validation.
- `crud_measurement_unit.py` — MeasurementUnitService: basic CRUD for units.
- `crud_product_list.py` — ProductListService: CRUD for master product definitions. Prevents deletion if associated with receipts.
- `crud_receipt.py` — ReceiptService: complex logic to create, read (with joinedload for performance), update receipts, calculate totals (price * quantity), update receipt products (re-create items), and delete receipts.
- `crud_merchant.py` — MerchantService: CRUD and delete-protection when receipts exist.
- `crud_receipt_product.py` — (if present) handles line-item-specific behavior — check repo for implementation.
- `file_services.py` — file upload helpers for product and receipt photos. Validates MIME type, extension, file size, writes files to `/app/uploads/...`, deletes previous files, and updates DB file path fields.
- `report_services.py` — complex SQL queries to generate analytics: spending by category, enriched merchant lists and dashboard KPIs. Uses SQLAlchemy `func`, `join`, `group_by` and subqueries to produce efficient aggregated results.

Notes about services:
- Services use SQLAlchemy sessions passed in by `get_db()` and are designed to raise `ValueError` or `HTTPException` upstream in routers for user-facing errors.
- Keep business rules (e.g., "validations") in services rather than routers so they are reusable by background jobs or CLI scripts.

**`src/routers/` — API endpoints**
Each router registers an `APIRouter` and exposes a small set of endpoints that delegate to services. Routers are intentionally thin and primarily handle parameter parsing, authorization (if added), and HTTP-level error mapping.

- `receipts.py` (`/receipts`):
	- POST `/` — create receipt (accepts nested receipt products in `ReceiptCreate`).
	- GET `/` — list receipts with pagination and filters (merchant, barcode, date range).
	- GET `/{receipt_id}` — get receipt by id (includes products and merchant).
	- GET `/barcode/{barcode}` — get receipt by barcode.
	- GET `/merchant/{merchant_id}` — get receipts for a merchant.
	- PUT `/{receipt_id}` — update receipt metadata.
	- PUT `/{receipt_id}/products` — replace products for a receipt (service deletes old items and inserts provided list).
	- DELETE `/{receipt_id}` — delete receipt (cascades items).

- `products.py` (`/products`): master product list endpoints.
	- POST `/` — create master product.
	- GET `/` — list product lists (supports pagination, filters planned in service layer).
	- GET `/barcode/{barcode}` and `/name/{name}` — lookup by barcode or name.
	- PUT `/{product_id}` — update master product.
	- DELETE `/{product_id}` — delete master product (service prevents deletion if used in receipts).

- `categories.py` (`/categories`): category CRUD and listing with aggregates.

- `merchants.py` (`/merchants`): merchant CRUD; delete prevents removing merchants with receipts.

- `measurement_units.py` (`/measurement-units`): unit CRUD.

- `reports.py` (`/reports`): analytical endpoints used by the frontend dashboard and admin screens.
	- GET `/spending-by-category` — spending totals per category.
	- GET `/enriched-merchants` — merchants list with totals and counts (analytics screen).
	- GET `/dashboard-kpis` — KPIs used by the dashboard.

- `uploads.py` (`/uploads`): file upload endpoints (multipart/form-data):
	- POST `/product-list/{id}/photo` — upload photo for product list item.
	- POST `/receipt/{id}/photo` — upload photo for receipt.

Routers use response models from `src/schemas` so responses are self-documenting in Swagger UI.

**`static/` — Frontend and docs**
- Contains a simple vanilla HTML/CSS/JS frontend used by the original project. Pages live under subfolders (`merchant/`, `product/`, `receipt/`, `category/`) and reference a JavaScript API client in `static/js/` that expects the backend endpoints described above.
- `static/docs/API_INTEGRATION_GUIDE.md` — extensive documentation and frontend integration guide (already included in the repo). Useful when integrating another frontend or mobile client.

**`alembic/` — Migrations**
- `alembic/versions/` contains historic migration scripts. Use `alembic revision --autogenerate` to generate migrations from model changes and `alembic upgrade head` to apply them.

**`scripts/`**
- `scripts/load_json_to_db.py` — helper script to import sample data into the DB (check file for exact behavior). Useful for populating dev DB with example merchants, products and receipts.

## Example: Creating a Receipt (end-to-end)
1. Create (or ensure) a `Merchant` exists by POST `/merchants` with JSON matching `MerchantCreate` (fields `name`, `location`, `notes`).
2. Ensure `ProductList` entries exist for each product used (POST `/products`).
3. POST `/receipts` with a JSON body matching `ReceiptCreate` schema, including `merchant_id`, `purchase_date` and `products` list (items include `product_list_id`, `price`, `quantity`).
4. Optionally upload a photo with POST `/uploads/receipt/{receipt_id}/photo` using `multipart/form-data`.



