install_dev:
	uv sync && \
	uv run pre-commit install

install_prod:
	uv sync
	cp -r ./static_files/* ./static/

migrate_dev:
	export ENV_FOR_DYNACONF=dev; uv run alembic upgrade head

migrate_prod:
	export ENV_FOR_DYNACONF=prod; uv run alembic upgrade head

start:
	export ENV_FOR_DYNACONF=dev; uv run gunicorn page_analyzer.app:app --bind 0.0.0.0:8000 --timeout 180

run_dev:
	export ENV_FOR_DYNACONF=dev; uv run gunicorn page_analyzer.app:app --bind 0.0.0.0:8000 --timeout 180

run_prod:
	export ENV_FOR_DYNACONF=prod; uv run gunicorn page_analyzer.app:app --bind 0.0.0.0:8000 --timeout 180

# Для uvicorn
#run_dev:
#	export ENV_FOR_DYNACONF=dev; uv run app
#run_prod: install_prod migrate_prod
#	export ENV_FOR_DYNACONF=prod; uv run app

clean_db:
	export ENV_FOR_DYNACONF=dev; uv run clean_db


playwright_prepare:
	uv pip install pytest-playwright

test_dev: playwright_prepare clean_db
	uv run pytest

lint:
	uv run ruff check .

fix:
	uv run ruff check --fix

build:
	./build.sh
