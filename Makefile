# Variables
PYTHON := poetry run python
UVICORN := poetry run uvicorn
ALEMBIC := poetry run alembic

# Default target (optional)
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  run              - Start the FastAPI application"
	@echo "  install          - Install dependencies using Poetry"
	@echo "  lint             - Lint code with Flake8"
	@echo "  test             - Run tests with Pytest"
	@echo "  migrate          - Apply Alembic migrations"
	@echo "  makemigrations   - Create a new Alembic migration"
	@echo "  dbshell          - Open the SQLite database shell"

# Poetry
.PHONY: install
install:
	poetry install

# FastAPI
.PHONY: run
run:
	$(UVICORN) taskmanager.main:api --reload

# Alembic
.PHONY: migrate
migrate:
	$(ALEMBIC) upgrade head

.PHONY: makemigrations
makemigrations:
	$(ALEMBIC) revision --autogenerate -m "New migration"


.PHONY: lint
lint:
	poetry run flake8 taskmanager tests

# Testing
.PHONY: test
test:
	poetry run pytest

# Database
.PHONY: dbshell
dbshell:
	sqlite3 taskmanager.db
