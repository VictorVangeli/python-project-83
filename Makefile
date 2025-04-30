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

run_dev:
	export ENV_FOR_DYNACONF=dev; uv run app

run_prod: install_prod migrate_prod
	export ENV_FOR_DYNACONF=prod; uv run app

lint:
	uv run ruff check .

fix:
	uv run ruff check --fix

build:
	./build.sh