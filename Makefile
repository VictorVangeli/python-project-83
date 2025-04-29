install_dev:
	uv sync && \
	uv run pre-commit install

install_prod:
	uv sync
	cp -r ./static/* ./static/

migrate_dev:
	export ENV_FOR_DYNACONF=dev; uv run alembic upgrade head
migrate_prod:
	export ENV_FOR_DYNACONF=prod; uv run alembic upgrade head
run_dev:
	export ENV_FOR_DYNACONF=dev; uv run gunicorn page_analyzer.core.app:app --bind 0.0.0.0:8000 --timeout 180

run_prod: install_prod migrate_prod
	export ENV_FOR_DYNACONF=prod; uv run gunicorn page_analyzer.core.app:app --bind 0.0.0.0:8000 --timeout 180

lint:
	uv run ruff check .

fix:
	uv run ruff check --fix

build:
	./build.sh