.PHONY: setup install check format test test-unit test-integration run docker-up docker-down docker-logs clean

# Create venv if not exists and install dependencies
setup:
	if [ ! -d "venv" ]; then python3 -m venv venv; fi
	$(MAKE) install

# Install dependencies and download ML corpuses
install:
	./venv/bin/pip install -r requirements.txt
	./venv/bin/pip install -r requirements-test.txt
	./venv/bin/python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt_tab'); nltk.download('averaged_perceptron_tagger_eng')"

# Run Ruff linter to statically analyze code
check:
	./venv/bin/ruff check src/ tests/

# Format code with Ruff automatically
format:
	./venv/bin/ruff format src/ tests/
	./venv/bin/ruff check --fix src/ tests/

# Run pytest for unit tests without triggering the 80% coverage trap
test-unit:
	DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/postgres" ./venv/bin/pytest tests/unit --cov-fail-under=0

# Run pytest for integration tests
test-integration:
	DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/postgres" ./venv/bin/pytest tests/integration --cov-fail-under=0

# Run all test suites
test:
	DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/postgres" ./venv/bin/pytest

# Start local server fast via uvicorn in VENV
run:
	./venv/bin/uvicorn src.app.main:app --reload --host 0.0.0.0 --port 8000

# Docker orchestration commands
docker-up:
	docker compose up -d --build

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f web

# Clean temporary folders
clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -r {} \+
