.PHONY: install
install:
	pip install -r requirements-dev.txt && \
	pre-commit install

.PHONY: db_init
db_init:
	docker-compose up -d database

.PHONY: db_generate_migration
db_generate_migration: db_init
	PYTHONPATH=. \
	alembic revision --autogenerate -m "$(description)"

.PHONY: db_run_migrations
db_run_migrations: db_init
	PYTHONPATH=. \
	alembic upgrade head

.PHONY: test
test:
	docker-compose down && \
	PYTHONPATH=. \
	python -m pytest --cov=app

.PHONY: run
run: db_init db_run_migrations
	uvicorn --reload app.api:api
