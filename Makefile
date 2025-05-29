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
	export ENV_FOR_DYNACONF=dev; uv run gunicorn page_analyzer.app:app --bind 0.0.0.0:8000 -w 5 --timeout 180

run_dev:
	export ENV_FOR_DYNACONF=dev; uv run gunicorn page_analyzer.app:app --bind 0.0.0.0:8000 --timeout 180

run_prod:
	SKIP_MIGRATIONS=true ENV_FOR_DYNACONF=prod uv run gunicorn page_analyzer.app:app --bind 0.0.0.0:8000 --timeout 180
# Для uvicorn
#run_dev:
#	export ENV_FOR_DYNACONF=dev; uv run app
#run_prod: install_prod migrate_prod
#	export ENV_FOR_DYNACONF=prod; uv run app

local_clean_db:
	export ENV_FOR_DYNACONF=dev; uv run local_clean_db

prod_test_clean_db:
	export ENV_FOR_DYNACONF=prod; uv run prod_test_clean_db


playwright_prepare:
	uv pip install pytest-playwright
	uv run playwright install

test_dev: playwright_prepare local_clean_db
	uv run pytest

test_prod: playwright_prepare prod_test_clean_db
	ENV_FOR_DYNACONF=prod SKIP_MIGRATIONS=true uv run pytest

lint:
	uv run ruff check .

lint_pre-commit:
	uv run pre-commit run --all-files

fix:
	uv run ruff check --fix

build:
	./build.sh
