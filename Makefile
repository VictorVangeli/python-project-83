install:
	uv sync

run:
	uv run gunicorn page_analyzer.core.app:app --bind 0.0.0.0:8000 --timeout 180

lint:
	uv run ruff check .

fix:
	uv run ruff check --fix

build:
	./build.sh