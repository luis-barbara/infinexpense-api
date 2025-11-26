.PHONY: help
help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

run:
	docker compose up --build --remove-orphans

clean:
	docker compose down --volumes

migrations:
	poetry run alembic -c src/alembic.ini revision --autogenerate -m "New migration: Creating users table"

## poetry run alembic -c src/alembic.ini upgrade head
upgrade:
	docker exec -it infinexpense-api-api-1 alembic upgrade head

#docker compose run web alembic revision --autogenerate -m "New migration: Creating users table"
migrationsdocker:
	docker exec -it infinexpense-api-api-1 alembic revision --autogenerate -m "add all models"

loadscript:
	python -m src.scripts.load_json_to_db --generate sample.json --products 200 --receipts 20
	python -m src.scripts.load_json_to_db sample.json

test: ## Run tests
	poetry run pytest tests/

coverage: ## Run tests with coverage report
	poetry run pytest --cov=src tests/ --cov-report=term-missing

coverage-html: ## Run tests with HTML coverage report
	poetry run pytest --cov=src tests/ --cov-report=html